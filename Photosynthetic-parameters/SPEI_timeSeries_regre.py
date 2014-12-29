
author__ = 'swei'
from netCDF4 import Dataset,netcdftime
import numpy as np
import pandas as pd
import numpy.ma as ma
import matplotlib.pylab as plt
from datetime import datetime
import glob
import os
from scipy.stats import pearsonr

os.chdir(r'G:\Research\Gridded Data\SPI\SPEI')
''' load the Standard Precipitation Evapotransporation Index (SPEI) netCDF data. SPEI is scaled
from one months to 2 years, denoted by the number after underscore (in months) in the filename. It comprises of three
dimensions, time (monthly), latitudes and longitudes  (0.5 x 0.5 degree)'''
files=glob.glob('*.nc')
JJA_mean=np.zeros([len(files),360,720])
cnt=0
for f in files:
    cnt+=1
    f=Dataset(f,'r')
    timevar = f.variables['time']
    ''' Select the start time and end time,years go from 1911 to 2011, months range from 1 to 12, keep the day unchanged'''

    t_start=netcdftime.date2index(datetime(2005,1,16),timevar)
    t_end=netcdftime.date2index(datetime(2006,1,16),timevar)
    spei_data=f.variables['spei'][t_start:t_end,:]

    '''Initialize the output datasets'''
    data=np.zeros(spei_data.shape,float)
    data=spei_data.copy()
    data=ma.getdata(data)
    data=ma.masked_where(data==data.max(),data)

    '''slice the data of June, July, and August, and calculate mean values'''
    JJA_mean[cnt-1,:,:]=np.mean(data[5:7,::-1,:],axis=0)

# JJA_mean=np.load(r'G:\Research\Gridded Data\SPI\SPEI\JJA_mean_spei_all.npy')

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
alpha=site['Amax']
alpha=np.array(alpha)

SPEI_output=np.zeros((48,num_site),float)
t_cnt=0
'''initialize the output array, rows are monthly time series, columns are each tower location alphabetically'''
for i in range(0,48):
    t_cnt+=1
    '''loop through each evi file, and read the data for each fluxnet tower sites'''
    for cnt in range(0,num_site,1):
        ilat=site['lat'][cnt]
        ilon=site['lon'][cnt]
        lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
        SPEI_output[t_cnt-1,cnt]=JJA_mean[i,lat_ind,lon_ind]

# print SPEI_output[1,:],'\n',alpha
pearsonr_corr=np.zeros([48,2])
for i in range(1,48):
    pearsonr_corr[i]=pearsonr(SPEI_output[i,:],alpha)
print pearsonr_corr
plt.plot(range(1,49),pearsonr_corr[:,1],'*-')
plt.show()
