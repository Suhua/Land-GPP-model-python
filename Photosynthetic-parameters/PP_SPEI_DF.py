author__ = 'swei'
from netCDF4 import Dataset,netcdftime
import numpy as np
import pandas as pd
import numpy.ma as ma
import matplotlib.pylab as plt
from datetime import datetime
import os
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


''' load the Standard Precipitation Evapotransporation Index (SPEI) netCDF data. SPEI is scaled
from one months to 2 years, denoted by the number after underscore (in months) in the filename. It comprises of three
dimensions, time (monthly), latitudes and longitudes  (0.5 x 0.5 degree)'''
f=Dataset('SPEI_48.nc','r')
# print f
#Get the time  index
timevar = f.variables['time']
''' Select the start time and end time,years go from 1911 to 2011, months range from 1 to 12, keep the day unchanged'''

t_start=netcdftime.date2index(datetime(2004,1,16),timevar)
t_end=netcdftime.date2index(datetime(2006,1,16),timevar)
spei_data=f.variables['spei'][t_start:t_end,:]

'''Initialize the output datasets'''
data=np.zeros(spei_data.shape,float)
data=spei_data.copy()
data=ma.getdata(data)
data=ma.masked_where(data==data.max(),data)
data=data[:,::-1,:]

plt.imshow(data[1,:,:])
plt.colorbar()
plt.show()
site=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\KoppenClimateAnalysis\PP_JJA.csv')
siteID=site['siteID']
num_site=len(siteID)

spei_output=np.zeros((24,num_site),float)
for i in range(24):
    for cnt in range(0,num_site,1):
            ilat=site['lat'][cnt]
            ilon=site['lon'][cnt]
            site_name=siteID[cnt]
            # pft=site['IGBP'][cnt]
            lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
            spei_output[i,cnt]=data[i,lat_ind,lon_ind]


''' Create DataFrame, index is the monthly time series from 2004-1-1 to 2005-12-1, columns are the site names'''

SPEI_DF=pd.DataFrame(spei_output,columns=siteID)

out_path=r'G:\Research\modelling\model_development\predicting_pp'
out_file=os.path.join(out_path,'SPEI_DF.csv')
SPEI_DF.to_csv(out_file)
