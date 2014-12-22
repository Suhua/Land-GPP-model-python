__author__ = 'swei'


import os
import numpy as np
from scipy.io import netcdf
import glob
import datetime
import pandas as pd
import matplotlib.pylab as plt
import scipy.misc as sm


##function to downscale gridded radiation data to tower locations
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


'''Set data reading directory'''
work_dir=r'G:\Research\Gridded Data\NC\NC_data'
os.getcwd()
os.chdir(work_dir)
f=netcdf.netcdf_file('nswrs.sfc.mon.mean.nc','r')
# print f.dimensions,'\n', f.history,'\n'

'''Read the variables, net short wave radiation (nswrs) data set has three dimensions: time, latitdues and longitudes, 
spatial resolution is not 0.5 x 0.5 degree, so we need to resize it to match the targeted resolution'''
time=f.variables['time']
lats=f.variables['lat']
lons=f.variables['lon']
Var=f.variables['nswrs']
# print dir(Var),'\n', Var.add_offset,Var.scale_factor,'\n',Var.shape


'''Par is estimated as 45% of the net shortwave radiation'''
data=Var[672:696,:,:]*0.45


''' read the fluxnet tower locations (latitudes and longitudes)'''
site=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\KoppenClimateAnalysis\PP_JJA.csv')
siteID=site['siteID']
num_site=len(siteID)
Par_output=np.zeros((24,num_site),float)  

''' Resize the data into 0.5x0.5 degree ([360,720])'''
for i in range(0,data.shape[0]):
    sr=sm.imresize(data[i,:,:],[360,720],interp='nearest')
    for cnt in range(0,num_site): # loop through all the sites
        lat=site['lat'][cnt]
        lon=site['lon'][cnt]
        ilat,ilon=read_lat_lon(lat,lon,0.5,0.5)
        Par_output[i,cnt]=sr[ilat,ilon]


'''save the PAR data into DataFrame'''
month=list(range(0,24))
month[0]=datetime.date(2004,1,1).isoformat()
i=0
while i<24:
      if i<12:
         month[i]=datetime.date(2004,i+1,1).isoformat()
         i+=1
      else:
         i+=1
         month[i-1]=datetime.date(2005,i-12,1).isoformat()

Par_output=pd.DataFrame(Par_output,index=month,columns=siteID)

out_path=r'G:\Research\modelling\model_development\predicting_pp'
out_file=os.path.join(out_path,'PAR_DF.csv')
Par_output.to_csv(out_file)
