_author__ = 'swei'

from netCDF4 import Dataset,netcdftime
import numpy as np
import numpy.ma as ma
import matplotlib.pylab as plt
from scipy import io,linalg
from scipy.stats import pearsonr
from sklearn import preprocessing
from mpl_toolkits import basemap

f=io.netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\precip.mon.mean.0.5x0.5.nc','r')
# print f.dimensions,f.references
var=f.variables['precip']
data=var.data[624:696,:,:]
'''shift the data 180 degree eastwards, because the orginal data starts from Meridian line,
we want the Meridian line in the middle'''
pre=np.zeros((72,360,720),dtype=float)
pre[:,:,360:]=data[:,:,:360]
pre[:,:,:360]=data[:,:,360:]
del f,data,var


f=io.netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\air.mon.mean.nc','r')
Var=f.variables['air']
data=Var.data[624:696,:,:]
data=data*Var.scale_factor+Var.add_offset
ta=np.zeros((72,360,720),dtype=float)
ta[:,:,360:]=data[:,:,:360]
ta[:,:,:360]=data[:,:,360:]

gpp=np.load('G:\Research\modelling\model_development1\gpp.npy')
temp=np.swapaxes(gpp,0,2)
gpp=np.swapaxes(temp,1,2)

pearsonr_corr=np.zeros([360,720,2])
a=np.ones([72,2],dtype=float)
for r in range(0,360):
    for c in range(0,720):
        # gpp[:,r,c]=preprocessing.normalize(gpp[:,r,c],axis=1)
        # ta[:,r,c]=preprocessing.normalize(ta[:,r,c],axis=1)
        # spe[:,r,c]=preprocessing.normalize(spe[:,r,c],axis=1)
        # partial correlation between gpp and spei while controlling ta
        a[:,1]=ta[:,r,c]
        beta_1=linalg.lstsq(a,pre[:,r,c])[0]
        beta_2=linalg.lstsq(a,gpp[:,r,c])[0]
        res_1=pre[:,r,c]-a.dot(beta_1)
        res_2=gpp[:,r,c]-a.dot(beta_2)
        pearsonr_corr[r,c,:]=pearsonr(res_1,res_2)
im=ma.masked_where(pearsonr_corr[:,:,1]>0.05,pearsonr_corr[:,:,0])

# Make figures to show the results
fig=plt.figure()
ax=fig.add_axes([0.05,0.05,0.9,0.9])
lats=np.linspace(90,-90,360)
lons=np.linspace(-180,180,720)
m=basemap.Basemap(projection='robin',lon_0=0.0,resolution='c')
m.drawparallels(np.arange(-90,90,30))
m.drawmeridians(np.arange(-180,180,60))
m.drawcoastlines()
lons,lats=np.meshgrid(lons,lats)
im=m.pcolormesh(lons,lats,im,cmap=plt.cm.RdYlBu,latlon=True)
ax.set_title('Partial Correlation between GPP and Precip controlling Ta',fontsize=16)
cb=m.colorbar(im,'bottom',size='5%')
# plt.savefig('GPP_precip_Partial_correlation.jpg')
plt.show()
