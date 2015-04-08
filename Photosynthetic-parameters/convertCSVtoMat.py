_author__ = 'swei'
import numpy as np
import pandas as pd
from scipy import io
import csv
import glob

files=glob.glob('*.csv')
nameList=list(range(len(files)))

i=0
for fn in files:
    nameList[i]=fn.split('.')[0]
    i+=1

map=dict((nameList[i], i) for i in range(0,len(nameList)))
setList=list(set(map.keys()))

# enumerate the sitename

def get_df_Index(df):
    keys=['DoY','Time','NEE_f','PPFD_f','GPP_f','Ta_f','VPD_f']
    return df[keys]

def concateDF(df1,df2):
    dataframe=pd.concat([df1,df2],axis=0)
    return dataframe

def save_df_mat(name,df):
    ns=name.split('-')
    nm=[''.join(ns),'.mat']
    io.savemat(''.join(nm),{'field':df.values})
    return


i=0
for fn in files:
    print i
    name=fn.split('.')[0]
    if i==0 and name in setList:
       setList.pop(setList.index(name))
       f=pd.read_csv(fn,header=0,index_col=None)
       df1=get_df_Index(f)
    elif i>0 and name in setList:
        save_df_mat(pre_name,df1)
        setList.remove(name)
        f=pd.read_csv(fn,header=0,index_col=None)
        df1=get_df_Index(f)
        pre_name=name
    else:
        f=pd.read_csv(fn,header=0,index_col=None)
        df2=get_df_Index(f)
        df1=concateDF(df1,df2)
        pre_name=name
    i+=1

