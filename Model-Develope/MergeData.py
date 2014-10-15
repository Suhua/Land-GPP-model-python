__author__ = 'swei'

import pandas as pd
import numpy as np
from numpy import ma
import matplotlib.pylab as plt
import pandas as pd

LAI=np.load(r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\2004to2005\LAI.npy')
# print LAI.shape
EVI=np.load(r"G:\Research\Gridded Data\Vegetation Index\EVI\resize_EVI\EVI_output.npy")
print EVI.shape
fPAR=np.load(r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\2004to2005fPAR\fPAR.npy')
print fPAR.shape
Precip=np.load(r'G:\Research\Gridded Data\NC\NC_data\precip_towers.npy')
print Precip.shape
Nswr=np.load(r'G:\Research\Gridded Data\NC\NC_data\nr_towers.npy')
print Nswr.shape
Ta=np.load(r'G:\Research\Gridded Data\NC\NC_data\Ta.npy')
print Ta.shape
SPEI=np.load(r"G:\Research\Gridded Data\SPI\SPEI\SPEI.npy")
print SPEI.shape

# print 'LAI',LAI,'\n','EVI', EVI,'\n','fPAR',fPAR,'\n','Precip',Precip,'\n','Nswr',Nswr,'\n','Ta',Ta,'\n','SPEI',SPEI
# LAI=ma.masked_where(LAI==255,LAI)
# plt.imshow(LAI)
# plt.colorbar()
# plt.show()

gridded_flux=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\siteInfo.csv')
site_name=gridded_flux['sitename']
# Remove the string Quotation Mark of the site_name
for i in range(0,len(site_name)):
    site_name[i]= site_name[i][1:7]
print site_name




fluxnet=pd.read_csv(r'fluxnet_2004-2005-monthly.csv')
# print fluxnet.head
site_data=fluxnet.groupby('site_id')
# for name,grouped in site_data:
#     print name,grouped.shape,'\n',grouped[['yyyy','mm','igbp_veg_type','kg_climate_type','nee_f_avg']]
cnt=0

merge=[]
mLAI=np.zeros([24,114])
mEVI=np.zeros([24,114])
mfPAR=np.zeros([24,114])
mPrecip=np.zeros([24,114])
mNswr=np.zeros([24,114])
mTa=np.zeros([24,114])
mSPEI=np.zeros([24,114])
for name,grouped in site_data:
    if grouped.shape[0]==24:
       isn=0
       for sn in site_name:
           isn+=1
           if name==sn:
               mLAI[:,cnt]=LAI[:,isn-1]
               mEVI[:,cnt]=EVI[:-1,isn-1]
               mfPAR[:,cnt]=fPAR[:,isn-1]
               mPrecip[:,cnt]=Precip[:,isn-1]
               mNswr[:,cnt]=Nswr[:,isn-1]
               mTa[:,cnt]=Ta[:,isn-1]
               mSPEI[:,cnt]=SPEI[:,isn-1]
               mNee=grouped[['nee_f_avg']]
               merge.append(name)
               cnt=+1
