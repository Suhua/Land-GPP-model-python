_author__ = 'swei'
from pyhdf import SD,HDF
import matplotlib.pylab as plt
from numpy import ma
import pandas as pd
import numpy as np
import glob
# set up the path
import os
files=os.listdir(r'G:/Vegetation Index/LAI and FPAR/2004to2005fPAR')
hdf_files=glob.glob('*.HDF')
num_files=len(hdf_files)
print num_files
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
    site=pd.read_csv('G:/Flux Data/flux_PP/siteInfo.csv')
    num_site=len(site['sitename'])
    print num_site
fpar_output=np.zeros((num_files,num_site),float)
t_cnt=0
for fn in files:
if fn.endswith('HDF'):
data=SD.SD(fn).select('fapar').get()
# data=ma.masked_where(data==255,data)
for cnt in range(0,num_site,1):
    ilat=site['Lat'][cnt]
    ilon=site['Lon'][cnt]
    #print ilat,ilon
    # site_name=site['sitename'][cnt]
    #print site_name
    # pft=site['IGBP'][cnt]
    #cnt+=1
    # print pft
    lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
    #print lat_ind,lon_ind
    #data=spei_data[:,lat_ind,lon_ind]
    fpar_output[t_cnt,cnt]=data[lat_ind,lon_ind]
    t_cnt+=1
    print fpar_output[-10:]
np.save('fPAR.npy',fpar_output)
fpar_output=ma.masked_where(fpar_output==255,fpar_output)
# plot the image
plt.imshow(fpar_output)
plt.colorbar()
plt.show()
