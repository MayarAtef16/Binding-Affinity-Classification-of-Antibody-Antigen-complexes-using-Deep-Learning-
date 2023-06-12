import torch
import torch.nn as nn
import torch.utils.data
import numpy as np
import argparse
from itertools import chain, product
from torch.utils.data import Dataset,DataLoader ,RandomSampler,TensorDataset
import pandas as pd

class ckaap_encode(Dataset):
    def __init__(self,antibody_seq,antigen_seq):
        self.antibody_seq=antibody_seq
        self.antigen_seq=antigen_seq
        AA = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        DP = list(product(AA, AA))
        self.DP_list = []
        for i in DP:
            self.DP_list.append(str(i[0]) + str(i[1]))
            
    def __len__(self):
        return len([self.antibody_seq])  
    
    def returnCKSAAPcode(self,query_seq, k):
        code_final = []
        for turns in range(k + 1):
            DP_dic = {}
            code = []
            for i in self.DP_list:
                DP_dic[i] = 0
            for i in range(len(query_seq) - turns - 1):
                tmp_dp_1 = query_seq[i]
                tmp_dp_2 = query_seq[i + turns + 1]
                tmp_dp = tmp_dp_1 + tmp_dp_2
                if tmp_dp in DP_dic.keys():
                    DP_dic[tmp_dp] += 1
                else:
                    DP_dic[tmp_dp] = 1
            for i, j in DP_dic.items():
                if (len(query_seq) - turns - 1)==0:
                    k=1
                else: 
                    k=len(query_seq) - turns - 1
                code.append(j / k)
            code_final += code
        return np.array(code_final)
    
    
    def __getitem__(self,item):
        antibody_seq=[*str(self.antibody_seq)]
        antigen_seq=[*str(self.antigen_seq)]
        antibody_encoding=[]
        antigen_encoding=[]
        for i in range(4):
            target_shape=(1681,1)
            encode_body=self.returnCKSAAPcode(antibody_seq,i)
            temp_body=np.pad(encode_body,[(0, target_shape[i] - encode_body.shape[i]) for i in range(len(encode_body.shape))])
            antibody_encoding.append(np.array(temp_body).reshape(41,41))
            
            
            encode_gen=self.returnCKSAAPcode(antigen_seq,i)
            temp_gen=np.pad(encode_gen,[(0, target_shape[i] - encode_gen.shape[i]) for i in range(len(encode_gen.shape))])
            antigen_encoding.append(np.array(temp_gen).reshape(41,41))
        antibody_encoding=np.array(antibody_encoding)
        antigen_encoding=np.array(antigen_encoding)
        return {
            'antibody_encoding': torch.tensor(antibody_encoding,dtype=torch.float),
            'antigen_encoding': torch.tensor(antigen_encoding,dtype=torch.float),
        }

def returnCKSAAPcode(query_seq, k,DP_list):
    code_final = []
    for turns in range(k + 1):
        DP_dic = {}
        code = []
        for i in DP_list:
            DP_dic[i] = 0
        for i in range(len(query_seq) - turns - 1):
            tmp_dp_1 = query_seq[i]
            tmp_dp_2 = query_seq[i + turns + 1]
            tmp_dp = tmp_dp_1 + tmp_dp_2
            if tmp_dp in DP_dic.keys():
                DP_dic[tmp_dp] += 1
            else:
                DP_dic[tmp_dp] = 1
        for i, j in DP_dic.items():
            if (len(query_seq) - turns - 1)==0:
                k=1
            else: 
                k=len(query_seq) - turns - 1
            code.append(j / k)
        code_final += code
    return np.array(code_final)
    
    
def _get_test_data_loader(batch_size,dataset):
    test_data=ckaap_encode(antibody_seq=np.array(dataset[0]),
                                      antigen_seq=np.array(dataset[1]))
    
    test_dataloader=DataLoader(test_data,batch_size=batch_size)
    return test_dataloader    
        
#model

class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1)


class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn = nn.Sequential(
            nn.Dropout(0.4),
            nn.Conv2d(in_channels=4, out_channels=10, kernel_size=3, stride=1),
            nn.BatchNorm2d(10),
            nn.LeakyReLU(), 
            nn.Conv2d(10, 20, 3, 1),
            nn.BatchNorm2d(20),
            nn.LeakyReLU(),
            Flatten()
        )

        self.fc = nn.Sequential(
            nn.Linear(54760, 64),
            nn.Linear(64, 2),
            nn.Tanh()
        )

    def forward_once(self,x):
        output = self.cnn(x)
        return output


    def forward(self,x1,x2):
        output1 = self.forward_once(x1)
        output2 = self.forward_once(x2)
        output = torch.cat((output1,output2),1)
        output = self.fc(output)
        return output
    

def test(model,test_loader,device):
    model.eval()
    
    with torch.no_grad():
        for batch in test_loader:
            
            antibody_encoding=batch['antibody_encoding'].to(device)
            antigen_encoding=batch['antigen_encoding'].to(device)

        
        outputs=model(antibody_encoding,antigen_encoding)
        _,preds=torch.max(outputs,dim=1)
        if preds==0:
            return "non-binders"
        else:
            return "binders"
        
#test
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--antibody_seq')
    parser.add_argument('--antibody_cdr')
    parser.add_argument('--antigen_seq')

    args = parser.parse_args()

    device=torch.device("cuda")
    model=SiameseNetwork().to(device)
    df=pd.Series(data=[args.antibody_cdr,args.antigen_seq])
    test_loader=_get_test_data_loader(1,df)

    #model.load_state_dict(torch.load("/content/weights.pth")) 
    pred =test(model,test_loader,device)

    return pred

if __name__=="__main__":
    main()
