# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
import subprocess

from flask import render_template, redirect, request, url_for,current_app,Flask
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from werkzeug.utils import secure_filename


from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import *
from apps.authentication.models import *

from apps.authentication.util import verify_pass

@blueprint.route('/')
def route_default():
    try:
        image = '/static/assets/images/'+current_user.username+ '.jpg'
    except:
        image = ''

    return render_template('home/index.html', img=image)

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    image = '/static/assets/images/'+current_user.username+ '.jpg'

    return redirect(url_for('home_blueprint.index'),img=image)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    print('register',request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully',
                               success=True,
                               form=create_account_form)

    else:
        
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    
    contact_form = ContactUsForm(request.form)
    if 'submit' in request.form:

        email = request.form['email']
        name = request.form['name']
        if not email == current_user.email:
            image = '/static/assets/images/'+current_user.username+ '.jpg'

            return render_template('home/contact_us.html',
                               msg='The email is incorrect',
                               form=contact_form,img=image)
        elif not name == current_user.username:
            image = '/static/assets/images/'+current_user.username+ '.jpg'

            return render_template('home/contact_us.html',
                               msg='The Username is incorrect',
                               form=contact_form,img=image)
        
        
        # else we can create the user
        user = contact_us_info(name=request.form['name'],email=request.form['email'],gender=request.form['gender'],city=request.form['city'],text_area=request.form['text_area'])
        db.session.add(user)
        db.session.commit()

        
        image = '/static/assets/images/'+current_user.username+ '.jpg'

        return render_template('home/contact_us.html',
                               msg='the message is created successfully',
                               form=contact_form,img=image)

    else:
        image = '/static/assets/images/'+current_user.username+ '.jpg'

        return render_template('home/contact_us.html', form=contact_form,img=image)

@blueprint.route('/forget_pass', methods=['GET', 'POST'])
def forget_pass():
    if request.method == 'GET':
        return render_template('home/forget_pass.html')
    elif request.method == 'POST':
        body = request.form
        print(body)
        if 'sign in' in request.form:
            return render_template('accounts/login.html')
        else:
            return render_template('home/forget_pass.html')


@blueprint.route('/Setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'GET':
        user= current_user
        image = '/static/assets/images/'+current_user.username+ '.jpg'

        return render_template('home/Setting.html',current_user=user,img=image)
    elif request.method == 'POST':
        body = request.form
        print(body)
        if 'clear' in request.form:
            user= current_user
            image = '/static/assets/images/'+current_user.username+ '.jpg'
            return render_template('home/Setting.html',current_user=user,img=image)
        elif 'save' in request.form:
            username = body['name']
            user = Users.query.filter_by(username=username).first()
            user.email = request.form['email']
            user.username = body['name']
            #user.password = body['password']
            db.session.commit()
            print(request.files)
            # Handle profile image upload
            if 'file' in request.files:
                print('entered')
                image_file = request.files['file']
                print(image_file)
                if image_file.filename != '':
                    filename,file_extension = os.path.splitext(image_file.filename)
                    os.chdir('D:/Graduation Project Website/Binding-Affinity-Classification-of-Antibody-Antigen-complexes-using-Deep-Learning-/apps/static/assets/images')

                    print("Current working directory: {0}".format(os.getcwd()))
                    filename = current_user.username+ '.jpg'
                    image_file.save(filename)
            user= current_user
            image = '/static/assets/images/'+current_user.username+ '.jpg'
            return render_template('home/Setting.html',current_user=user,img=image)

@blueprint.route('/Discover', methods=['GET', 'POST'])
def discover():
    if request.method == 'GET':
            user = current_user
            image = '/static/assets/images/'+current_user.username+ '.jpg'
            return render_template('home/Discover.html',current_user=user,img=image)
    
@blueprint.route('/Feedback_form', methods=['GET', 'POST'])
def feedback():
  if request.method == 'GET':
        user = current_user
        image = '/static/assets/images/'+current_user.username+ '.jpg'
        return render_template('home/Feedback_form.html',current_user=user,img=image)
  else:
    feedback_form = FeedbackForm(request.form)
    print(request.form)
    if 'submit' in request.form:

        email = request.form['email']
        name = request.form['name']
        if not email == current_user.email:
            image = '/static/assets/images/'+current_user.username+ '.jpg'

            return render_template('home/Feedback_form.html',
                               msg='The email is incorrect',
                               form=feedback_form,img=image)
        elif not name == current_user.username:
            image = '/static/assets/images/'+current_user.username+ '.jpg'

            return render_template('home/Feedback_form.html',
                               msg='The Username is incorrect',
                               form=feedback_form,img=image)
        
        
        # else we can create the user
        user = feedback_info(name=request.form['name'],email=request.form['email'],gender=request.form['gender'],city=request.form['city'],satistfied=request.form['optionsRadios'],text_area=request.form['text_area'])
        db.session.add(user)
        db.session.commit()

        
        image = '/static/assets/images/'+current_user.username+ '.jpg'

        return render_template('home/Feedback_form.html',
                               msg='the form is created successfully',
                               form=feedback_form,img=image)

    else:
        image = '/static/assets/images/'+current_user.username+ '.jpg'

        return render_template('home/Feedback_form.html', form=feedback_form,img=image)

@blueprint.route('/AbAgIntPre', methods=['GET', 'POST'])
def AbAgIntPre():

    if request.method == 'GET':
            print(request.form)

            user = current_user
            image = '/static/assets/images/'+current_user.username+ '.jpg'
            return render_template('home/AbAgIntPre.html',img=image)
    elif request.method == 'POST':
        print(request.form,'hereeeeeeeeeeeeee')

        if 'submit' in request.form:
            print(request.form)
            command = ['python', 'test.py', '--antibody_seq', request.form['Hchain'], '--antibody_cdr', request.form['Lchain'], '--antigen_seq', request.form['antigen']]
            output = subprocess.run(command, capture_output=True, text=True)
            # Check if the execution was successful
            if output.returncode == 0:
                print("Script executed successfully.")
                print("Output:")
                print(output.stdout)
                image = '/static/assets/images/'+current_user.username+ '.jpg'

                return render_template('home/AbAgIntPre.html', out=output.stdout,img=image)

            else:
                print("Script execution failed.")
                print("Error message:")
                print(output.stderr)
                image = '/static/assets/images/'+current_user.username+ '.jpg'

                return render_template('home/AbAgIntPre.html', out=output,img=image)

        elif 'example' in request.form:
                print(request.form)

                image = '/static/assets/images/'+current_user.username+ '.jpg'
                hchain='EIQLQQSGAELVRPGALVKLSCKASGFNIKDYYMHWVKQRPEQGLEWIGLIDPENGNTIYDPKFQGKASITADTSSNTAYLQLSSLTSEDTAVYYCARDNSYYFDYWGQGTTLTVSSAKTTPPSVYPLAPGSAAQTNSMVTLGCLVKGYFPEPVTVTWNSGSLSSGVHTFPAVLQSDLYTLSSSVTVPSSTWPSETVTCNVAHPASSTKVDKKI'
                lchain='DIKMTQSPSSMYASLGERVTITCKASQDIRKYLNWYQQKPWKSPKTLIYYATSLADGVPSRFSGSGSGQDYSLTISSLESDDTATYYCLQHGESPYTFGGGTKLEINRADAAPTVSIFPPSSEQLTSGGASVVCFLNNFYPKDINVKWKIDGSERQNGVLNSWTDQDSKDSTYSMSSTLTLTKDEYERHNSYTCEATHKTSTSPIVKSFNRNEC'
                antigen='SGTTNTVAAYNLTWKSTNFKTILEWEPKPVNQVYTVQISTKSGDWKSKCFYTTDTECDLTDEIVKDVKQTYLARVFSYPAGNVESTGSAGEPLYENSPEFTPYLETNLGQPTIQSFEQVGTKVNVTVEDERTLVRRNNTFLSLRDVFGKDLIYTLYYWKSSSSGKKTAKTNTNEFLIDVDKGENYCFSVQAVIPSRTVNRKSTDSPVECMGQEKGEFRE'
                return render_template('home/AbAgIntPre.html',img=image,lchain=lchain,hchain=hchain,antigen=antigen)
        
        elif 'clear' in request.form:
                        return render_template('home/AbAgIntPre.html',img=image)



        

@blueprint.route('/visualize_pdb', methods=['GET', 'POST'])
def visualize():
    if request.method == 'GET':
            print(request.form)
            user = current_user
            image = '/static/assets/images/'+current_user.username+ '.jpg'
            return render_template('home/visualize_pdb.html',img=image)
    
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
