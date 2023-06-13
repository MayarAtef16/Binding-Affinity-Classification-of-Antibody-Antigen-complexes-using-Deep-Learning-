# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

class ContactUsForm(FlaskForm):
    name = StringField('name',
                         id='username_create',
                         validators=[DataRequired()])
    
    email = StringField('email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    

    
    gender = StringField('gender',
                         id='gender_create',
                         validators=[DataRequired()])
    
    city = StringField('city',
                         id='city_create',
                         validators=[DataRequired()])
    
    text_area = StringField('text_area',
                         id='text_area_create',
                         validators=[DataRequired()])
    

class FeedbackForm(FlaskForm):
    name = StringField('name',
                         id='username_create',
                         validators=[DataRequired()])
    
    email = StringField('email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    
  
    
    gender = StringField('gender',
                         id='gender_create',
                         validators=[DataRequired()])
    
    city = StringField('city',
                         id='city_create',
                         validators=[DataRequired()])
    
    text_area = StringField('text_area',
                         id='text_area_create',
                         validators=[DataRequired()])
    satisfied = StringField('satisfied',
                         id='satisfied_create',
                         validators=[DataRequired()])