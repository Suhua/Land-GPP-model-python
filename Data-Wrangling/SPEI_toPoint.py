
from netCDF4 import Dataset,netcdftime
import numpy as np
import pandas as pd
import numpy.ma as ma
import matplotlib.pylab as plt
from datetime import datetime

def read_lat_lon(lat,lon,lat_r,lon_r):
    if (lat>=-90 and lat<=90):
        lat=90-lat
    if (lon>=-180 and lon<=180):
        lon=lon+180
    lat_ind=int(lat//lat_r)
    lon_ind=int(lon//lon_r)
    return lat_ind, lon_ind

# load the netCDF data
f=Dataset('SPEI_03.nc','r')
# print f
#Get the time  index
timevar = f.variables['time']
# Select the start time and end time,years go from 1911 to 2011, months range from 1 to 12, keep the day unchanged

t_start=netcdftime.date2index(datetime(2004,1,16),timevar)
t_end=netcdftime.date2index(datetime(2006,1,16),timevar)
spei_data0=f.variables['spei'][t_start:t_end,:]


data=np.zeros(spei_data0.shape,float)
data=spei_data0.copy()
data=ma.getdata(data)
data=ma.masked_where(data==data.max(),data)
print data.max(),data.min()



f_csv=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\siteInfo.csv')
lat=f_csv['Lat']
site_name=f_csv['sitename']


output=np.zeros((data.shape[0],len(site_name)),dtype=float)

for i in range(0,data.shape[0]):
    print i
    for cnt in range(0,len(lat)):
            ilat=f_csv['Lat'][cnt]
            ilon=f_csv['Lon'][cnt]
            pft=f_csv['IGBP'][cnt]
            lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
            tem_data=data[i,::-1,]
            output[i,cnt]=float(tem_data[lat_ind,lon_ind])
            #tem_data=tem_data.compressed()

output=np.array(output)
np.save('SPEI.npy',output)
print output
