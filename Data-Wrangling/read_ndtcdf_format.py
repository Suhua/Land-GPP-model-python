from netCDF4 import Dataset,netcdftime
import numpy as np
import numpy.ma as ma
from mpl_toolkits import basemap
import matplotlib.pylab as plt
from datetime import datetime
# load the netCDF data
f=Dataset('SPEI_48.nc','r')
#Get the time index
timevar = f.variables['time']
#Select the start time and end time,years go from 1911 to 2011, months range from 1 to 12, keep the day unchanged
t_start=netcdftime.date2index(datetime(2011,1,16),timevar)
t_end=netcdftime.date2index(datetime(2011,12,16),timevar)
t_start0=netcdftime.date2index(datetime(1911,1,16),timevar)
t_end0=netcdftime.date2index(datetime(1911,12,16),timevar)
spei_data1=f.variables['spei'][t_start:t_end,:]
spei_data0=f.variables['spei'][t_start0:t_end0,:]
spei_data=spei_data1-spei_data0
MissValue=ma.getdata(spei_data)
print MissValue
print f.variables['spei']
# Group analysis: sum/ average
spei_data=np.mean(spei_data,axis=0)
# Calculate the average over the time span
#spei_data=np.flipud(spei_data)
##Plot data
# Get the latitudes/longitudes
lats=f.variables['lat'][:]
lons=f.variables['lon'][:]
lons, lats = np.meshgrid(lons,lats)
fig = plt.figure()
ax = fig.add_axes([0.05,0.05,0.9,0.9])
m = basemap.Basemap(projection='robin',lon_0=0, resolution=None)
# missing values over land will show up this color.
m.drawmapboundary(fill_color='0.7')
h = m.pcolormesh(lons,lats,spei_data,shading='flat',cmap=plt.cm.BrBG,latlon=True)
#h=plt.imshow(spei_data[0:300,:],vmin=-3,vmax=4,cmap='jet',aspect=1)
# Cut off data from 60 degree south and southward, because of no data available
#plt.title('SPEI_48 months time scale (2011)')
#plt.xlabel('Longitude(degree E)')
#plt.ylabel('latitude(degree N)')
m.drawparallels(np.arange(-90.,90.,30.))
m.drawmeridians(np.arange(-180.,180.,60.))
# add colorbar
cb = m.colorbar(h,"bottom", size="4%", pad="5%")
# add a title.
ax.set_title('SPEI change from 1911 to 2011 based on 48 months time scale')
#xt=range(0,720,60)
#yt=range(0,300,60)
#xl=range(-180,180,30)
#yl=range(90,-60,-30)
#plt.xticks(xt,xl)
#plt.yticks(yt,yl)
#plt.colorbar(h,orientation='horizontal',pad=0.1)
#plt.grid(True)
plt.show()
