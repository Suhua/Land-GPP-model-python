import numpy as np
from numpy import ma
import pandas as pd
from scipy import io,misc
from scipy.io import netcdf
import datetime
import matplotlib.pylab as plt
import os
import glob
from netCDF4 import Dataset, netcdftime

#----------Define internal functions------------------------------------------------------------------------------------

def look_up(value):
    lc_dic={0:'WAT',1:'ENF',2:'EBF',3:'DBF',4:'DBF',5:'MF',6:'CSH',7:'OSH',8:'WSA',\
    9:'SAV',10:'GRA',11:'WET',12:'CRO',13:'URB',14:'NEM',15:'SNO',16:'BAR'}
    return lc_dic[value]

def alpha_lookUp(veg):
        df=pd.read_csv(r'G:\Research\fluxdata\LaThuile\filestrans\alpha_complete.csv',header=0,index_col=0)
        df[df.ix[:,1:]>0.1]=np.nan
        del_row=[]
        for i in range(0,250):
            dff=df.ix[i,1:]
            # print dff.mean()
            if dff.mean() is np.nan:
               del_row.append(i)
        df=df.drop(df.index[del_row])
        df.ix[:,1]=df.ix[:,1].fillna(0)
        df.ix[:,12]=df.ix[:,12].fillna(0)
        df.ix[:,1:]=df.ix[:,1:].interpolate(kind='linear',axis=1)
        # #save the data
        # alpha.to_csv('alpha_complete.csv')

        # group them by vegetation types
        dic={k:v for (k,v) in df.groupby('IGBP')}
        # del dic[u' TBD']
        for k in dic.keys():
            if k==veg:
               return dic.get(k).mean()*4.6*12

def make_map(map,lc,value,pred):
    map[lc==value]=pred
    return map
#-----------------Main function starts here-----------------------------------------------------------------------------

lc=io.loadmat('G:\Research\Gridded Data\PDSI\lc.mat')['lc']
lc_valid={1:'ENF',2:'EBF',3:'DBF',4:'DBF',5:'MF',6:'CSH',7:'OSH',8:'WSA',\
    9:'SAV',10:'GRA',11:'WET',12:'CRO'}
for mon in range(1,13):
    map=np.zeros([360,720])
    for value in lc_valid.keys():
        veg=look_up(value)
        lue=alpha_lookUp(veg)
        pred=lue[mon-1]
        map=make_map(map,lc,value,pred)
    os.chdir(r'G:\Research\modelling\model_development1')
    map.dump('alpha_{0}.npy'.format(mon))
