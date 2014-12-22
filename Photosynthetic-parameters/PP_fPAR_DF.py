__author__ = 'swei'

from pyhdf import SD,HDF
import matplotlib.pylab as plt
from numpy import ma
import pandas as pd
import numpy as np
import datetime
import glob
import os

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

files=os.listdir(r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\2004to2005fPAR')
hdf_files=glob.glob('*.HDF')
num_files=len(hdf_files)

site=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\KoppenClimateAnalysis\PP_JJA.csv')
siteID=site['siteID']
num_site=len(siteID)


fpar_output=np.zeros((num_files,num_site),float)
t_cnt=0
for fn in files:
    if fn.endswith('HDF'):
        data=SD.SD(fn).select('fapar').get()
        # data=ma.masked_where(data==255,data)
        for cnt in range(0,num_site,1):
                ilat=site['lat'][cnt]
                ilon=site['lon'][cnt]
                site_name=siteID[cnt]
                # pft=site['IGBP'][cnt]
                lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
                fpar_output[t_cnt,cnt]=data[lat_ind,lon_ind]
        t_cnt+=1

''' Create DataFrame, index is the monthly time series from 2004-1-1 to 2005-12-1, columns are the site names'''
month=list(range(0,24))
i=0
while i<24:
      if i<12:
         month[i]=datetime.date(2004,i,1).isoformat()
          i+=1
      else:
         i+=1
         month[i-1]=datetime.date(2005,i-12,1).isoformat()


fPARDF=pd.DataFrame(fpar_output,index=month,columns=siteID)

out_path=r'G:\Research\modelling\model_development\predicting_pp'
out_file=os.path.join(out_path,'fPAR_DF.csv')
fPARDF.to_csv(out_file)
