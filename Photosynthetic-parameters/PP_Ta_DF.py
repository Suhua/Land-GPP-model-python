#__author__ = 'swei'

import os
import numpy as np
from scipy.io import netcdf
from scipy import misc
import glob
import datetime
import pandas as pd
import matplotlib.pylab as plt


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



f=netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\air.mon.mean.nc','r')
''' Read the monthly mean temperature data. The air.mon.mean.nc data set comprises of three dimensions: time,
 lat, and lon; the time feature reference is 1900-1-1-0. Unit is hours. Lat and Lon are 0.5 x 0.5 degree
 in spatial resolution '''
print f.dimensions,'\n', f.history,'\n'
print dir(f)
print f.references,'\n'
time=f.variables['time']
lats=f.variables['lat']
lons=f.variables['lon']
Var=f.variables['air']
print Var.add_offset, '\n',Var.units,'\n',Var.scale_factor

''' read the the time information'''
print  '\n',dir(time)
print time.shape
print time.units
print time.shape,'\n',time.units,'\n',lats.shape,'\n',lons.shape,'\n'
time_base=datetime.date(1900,1,1)
# print time_base
time_start=datetime.date(2004,1,1)  # Input the starting time
# print (time_start-time_base)*24
time_end=datetime.date(2006,1,1)  # Input the ending time
# print (time_end-time_base)*24
time=time.data

for i in range(0,time.shape[0]):
    if time[i]==911640 or time[i]==929184 :
        print i
        print time[i]

'''Slice data for the years 2004-1-1 to 2005-12-1'''
data=Var.data[672:696,:,:]
data=data*Var.scale_factor+Var.add_offset

'''shift the data 180 degree eastwards, because the orginal data starts from Meridian line,
we want the Meridian line in the middle'''
new_data=np.zeros((24,360,720),dtype=float)
new_data[:,:,360:]=data[:,:,:360]
new_data[:,:,:360]=data[:,:,360:]
del data


'''Read the fluxnet towers latitudes and longitudes, '''
site=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\KoppenClimateAnalysis\PP_JJA.csv')
num_site=len(site['siteID'])
siteID=site['siteID']
Var_output=np.zeros((24,num_site),float)
'''initialize the output array'''

for cnt in range(0,num_site): # loop through all the sites
    lat=site['lat'][cnt]
    lon=site['lon'][cnt]
    ilat,ilon=read_lat_lon(lat,lon,0.5,0.5)
    Var_output[:,cnt]=new_data[:,ilat,ilon]

'''Plot the output data'''
plt.imshow(Var_output)
plt.colorbar()
plt.show()


''' Save is to Pandas Data Frame, index is the time series, and columns are site name'''
month=list(range(0,24))
i=0
while i<24:
      if i<12:
         month[i]=datetime.date(2004,i+1,1).isoformat()
         i+=1
      else:
         i+=1
         month[i-1]=datetime.date(2005,i-12,1).isoformat()
ta_DF=pd.DataFrame(Var_output,index=month,columns=siteID)
out_path=r'G:\Research\modelling\model_development\predicting_pp'
out_file=os.path.join(out_path,'ta_DF.csv')
ta_DF.to_csv(out_file)
