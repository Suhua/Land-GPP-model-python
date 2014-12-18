__author__ = 'swei'
from pyhdf import SD,HDF
import matplotlib.pylab as plt
from numpy import ma
import pandas as pd
import numpy as np
import glob
import datetime
import os

'''set up the path'''
os.chdir(r"G:\Research\Gridded Data\Vegetation Index\EVI\resize_EVI")
files=os.listdir(r'G:\Research\Gridded Data\Vegetation Index\EVI\resize_EVI')
outpath=r'G:\Research\modelling\model_development\datasets_for_PP_prediction'

def read_lat_lon(lat,lon,lat_r,lon_r):
    '''read the lat and lon at specific lat and lon resolution(lat_r and lon_r), return the index of lat and lon at
gridded data set, by default, lat ranges from -90 to 90 northward and lon ranges -180 to 180 eastward '''
    if lat >= -90 and lat <= 90:
        lat=90-lat
    if lon>=-180 and lon<=180:
        lon=lon+180
    lat_ind=int(lat//lat_r)
    lon_ind=int(lon//lon_r)
    return lat_ind, lon_ind

site=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\KoppenClimateAnalysis\PP_JJA.csv')
'''Read the fluxnets tower latitudes and longitudes'''
num_site=len(site['siteID'])
siteID=site['siteID']

evi_files=glob.glob('*.npy')
'''Read EVI data,which are stored in npy files, each file stores monthly mean of EVI data at global scale, with spatial
resolution of 0.5 x 0.5 degree, covering from Jan-2004 to Dec-2005'''
num_files=len(evi_files)

EVI_output=np.zeros((num_files,num_site),float)
t_cnt=0
'''initialize the output array, rows are monthly time series, columns are each tower location alphabetically'''
for fn in evi_files:
    '''loop through each evi file, and read the data for each fluxnet tower sites'''
    if fn.startswith('resize'):
        data=np.load(fn)/255.0
        file_name=str(fn).split('_')
        data=ma.masked_where(data<0,data)
        for cnt in range(0,num_site,1):
            ilat=site['lat'][cnt]
            ilon=site['lon'][cnt]
            lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
            EVI_output[t_cnt,cnt]=data[lat_ind,lon_ind]
        t_cnt+=1
month=list(range(0,24))
month[0]=datetime.date(2004,1,1).isoformat()

i=0
while i<24:
      if i<12:
         i+=1
         month[i]=datetime.date(2004,i,1).isoformat()
      else:
         i+=1
         month[i-1]=datetime.date(2005,i-12,1).isoformat()
evi_DF=pd.DataFrame(EVI_output,index=month,columns=siteID)
out_path=r'G:\Research\modelling\model_development\predicting_pp'
out_file=os.path.join(out_path,'evi_DF.csv')
evi_DF.to_csv(out_file)
