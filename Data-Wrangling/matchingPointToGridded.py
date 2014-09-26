# This module is to extract fluxnet point data from gridded/image data sets
# The global variable of the spatial resolution of gridded data is defined as sr, for example, sr=0.05 or sr=0.5
import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset,netcdftime
from datetime import datetime
import matplotlib.pyplot as plt
def read_lat_lon(lat,lon,lat_r,lon_r):
'''read the lat and lon at specific lat and lon resolution(lat_r and lon_r), return the index of lat and lon at
gridded data set, by default, lat ranges from -90 to 90 northward and lon ranges -180 to 180 eastward '''
if (lat>=-90 and lat<=90):
lat=lat+90
if (lon>=-180 and lon<=180):
lon=lon+180
lat_ind=int(lat//lat_r)
lon_ind=int(lon//lon_r)
return lat_ind, lon_ind
f=pd.read_csv('G:/Flux Data/flux_PP/siteInfo.csv')
fncf=Dataset('G:/SPI/SPEI/SPEI_03.nc','r')
timevar=fncf.variables['time']
# define the period of time needed to be retrieved
t_start=netcdftime.date2index(datetime(1901,1,16),timevar)
t_end=netcdftime.date2index(datetime(2011,1,16),timevar)
time_span= fncf.variables['time'][t_start:t_end].shape[0]
lats = fncf.variables['lat']
lons = fncf.variables['lon']
lons, lats = np.meshgrid(lons,lats)
lat=f['Lat']
site_num=len(lat[:2])
#data=np.zeros((time_span,site_num),dtype=float)
#cnt=0
for cnt in range(0,len(lat),1):
ilat=f['Lat'][cnt]
ilon=f['Lon'][cnt]
#print ilat,ilon
site_name=f['sitename'][cnt]
#print site_name
pft=f['IGBP'][cnt]
#cnt+=1
# print pft
lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
#print lat_ind,lon_ind
#data=spei_data[:,lat_ind,lon_ind]
tem_data=fncf.variables['spei'][t_start:t_end,lat_ind,lon_ind]
#tem_data=tem_data.compressed()
np.save(pft+site_name+'.npy','tem_data')
print site_name,len(tem_data)
#print data
#t=np.arange(0,time_span,1)
#fig=plt.plot(t,tem_data)
#plt.hist(tem_data,bins=15)
#plt.xlabel('Number of months since 2001 Jan')
#plt.ylabel('SPEI')
#plt.title('Histogram of 3 month SPEI at'+site_name)
#plt.show()
#np.savetxt('spei_fluxet_sites.txt',data,header=site_name)
