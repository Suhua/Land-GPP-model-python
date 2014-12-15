__author__ = 'swei'

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, maskoceans,interp

file_path=r'G:\Research\Gridded Data\Koppen Climate\1976-2000_ASCII.txt'
# f=open(file_path,'r')
datain=pd.read_table(file_path,sep='\s+',header=False)

# print datain.index,'\n', datain.columns
kg=datain['Cls']
lats=datain['Lat']
lons=datain['Lon']
DF1=pd.DataFrame({'kg':kg,'lats':lats,'lons':lons})

glat=np.linspace(-89.75,89.75,num=360)
glon=np.linspace(-179.75,179.75,num=720)
cnt=0
lat=np.zeros(len(glat)*len(glon))
lon=np.zeros(len(glat)*len(glon))
for i in glat:
    for j in glon: 
        cnt+=1
        lon[cnt-1]=j
        lat[cnt-1]=i

DF=pd.DataFrame({'lats':lat,'lons':lon})
merg=pd.merge(DF,DF1,how='left',left_index=False,right_index=False)
os.chdir(r'G:\Research\modelling\model_development\predicting_pp')
merg.to_csv('filled_kg.csv')
