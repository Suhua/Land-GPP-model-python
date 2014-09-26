#__author__ = 'swei'
import os
import numpy as np
from scipy.io import netcdf
import glob
import datetime
import pandas as pd
import matplotlib.pylab as plt
import scipy.misc as sm
##define a function to transfer tower location into positions in gridded data
def read_lat_lon(lat,lon,lat_r,lon_r):
'''read the lat and lon at specific lat and lon resolution(lat_r and lon_r), return the index of lat and lon at
gridded data set, by default, lat ranges from -90 to 90 northward and lon ranges -180 to 180 eastward '''
if (lat>=-90 and lat<=90):
lat=90-lat
if (lon>=-180 and lon<=180):
lon=lon+180
lat_ind=int(lat//lat_r)
lon_ind=int(lon//lon_r)
return lat_ind, lon_ind
## Set working directory
work_dir=r'C:/Users/swei/ABI_lab/Research/NC/NC_data'
os.getcwd()
os.chdir(work_dir)
## Load netcdf files
f=netcdf.netcdf_file('nswrs.sfc.mon.mean.nc','r')
# print f.dimensions,'\n', f.history,'\n'
# Read the variables
time=f.variables['time']
lats=f.variables['lat']
lons=f.variables['lon']
Var=f.variables['nswrs']
print dir(Var),'\n', Var.add_offset,Var.scale_factor,'\n',Var.shape
print time.shape,'\n',time.units,'\n',lats.shape,'\n',lons.shape,'\n'
##get the time information
# time_base=datetime.date(1,1,1)
# print time_base
# time_start=datetime.date(2004,1,3) # Input the starting time
# print (time_start-time_base)*24
# time_end=datetime.date(2006,1,3) # Input the ending time
# print (time_end-time_base)*24
# for i in range(0,time.shape[0]):
# if time[i]==17557968 or time[i]==17575512.0:
# print i
data=Var[672:696,:,:]*0.45
## extract tower point data from resized data
site=pd.read_csv('C:/Users/swei/ABI_lab/Flux Data/flux_PP/siteInfo.csv')
num_site=len(site['sitename'])
Var_output=np.zeros((24,num_site),float) # initialize the output matrix
# Resize the data into 0.5x0.5 degree ([360,720])
for i in range(0,data.shape[0]):
sr=sm.imresize(data[i,:,:],[360,720],interp='nearest')
for cnt in range(0,num_site): # loop through all the sites
lat=site['Lat'][cnt]
lon=site['Lon'][cnt]
ilat,ilon=read_lat_lon(lat,lon,0.5,0.5)
Var_output[i,cnt]=sr[ilat,ilon]
np.save('nr_towers.npy',Var_output)
## Plot data
# plt.imshow(sr)
# plt.colorbar()
# plt.show()
