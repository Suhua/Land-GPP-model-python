__author__ = 'swei'

from netCDF4 import Dataset,netcdftime
import numpy as np
import matplotlib.pylab as plt
from datetime import datetime
import glob
import os
from scipy import io,linalg
from scipy.stats import pearsonr
from sklearn import preprocessing

#process precipitation data
f=io.netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\precip.mon.mean.0.5x0.5.nc','r')
var=f.variables['precip']
data=var.data[624:696,:,:]
pre=np.zeros((72,360,720),dtype=float)
'''shift the data 180 degree eastwards, because the orginal data starts from Meridian line,
we want the Meridian line in the middle'''
pre[:,:,360:]=data[:,:,:360]
pre[:,:,:360]=data[:,:,360:]
del f,data,var

#process temperature data
f=io.netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\air.mon.mean.nc','r')
Var=f.variables['air']
data=Var.data[624:696,:,:]
data=data*Var.scale_factor+Var.add_offset
ta=np.zeros((72,360,720),dtype=float)
ta[:,:,360:]=data[:,:,:360]
ta[:,:,:360]=data[:,:,360:]


os.chdir(r'G:\Research\Gridded Data\SPI\SPEI')
files=glob.glob('*.nc')
cnt=0
for f in files:
    # read SPEI data
    cnt+=1
    if cnt==3:
        f=Dataset(f,'r')
        timevar = f.variables['time']
        ''' Select the start time and end time,years go from 1911 to 2011, months range from 1 to 12, keep the day unchanged'''
        t_start=netcdftime.date2index(datetime(2000,1,16),timevar)
        t_end=netcdftime.date2index(datetime(2006,1,16),timevar)
        spei_data=f.variables['spei'][t_start:t_end,:]

        '''Initialize the output datasets'''
        spe=np.zeros(spei_data.shape,float)
        spe=spei_data.copy()
        spe=ma.getdata(data)
        spe=ma.masked_where(data==data.max(),data)
        spe=data[:,::-1,:]

        #read GPP data
        gpp=np.load('G:\Research\modelling\model_development1\gpp.npy')
        temp=np.swapaxes(gpp,0,2)
        gpp=np.swapaxes(temp,1,2)
        shape=gpp.shape
        print shape

        # gpp=np.divide((gpp-np.repeat(gpp_mean,6,axis=2)),np.repeat(gpp_std,6,axis=2))
        # calculate pearson correlation
        pearsonr_corr=np.zeros([360,720,2])
        a=np.ones([72,2],dtype=float)
        for r in range(0,shape[1]):
            for c in range(0,shape[2]):
                # gpp[:,r,c]=preprocessing.normalize(gpp[:,r,c],axis=1)
                # ta[:,r,c]=preprocessing.normalize(ta[:,r,c],axis=1)
                # spe[:,r,c]=preprocessing.normalize(spe[:,r,c],axis=1)
                # partial correlation between gpp and spei while controlling ta
                a[:,1]=pre[:,r,c]
                beta_1=linalg.lstsq(a,ta[:,r,c])[0]
                beta_2=linalg.lstsq(a,gpp[:,r,c])[0]
                res_1=ta[:,r,c]-a.dot(beta_1)
                res_2=gpp[:,r,c]-a.dot(beta_2)
                pearsonr_corr[r,c,:]=pearsonr(res_1,res_2)
        im=ma.masked_where(pearsonr_corr[:,:,1]>0.05,pearsonr_corr[:,:,0])
        # im.dump('gpp_ta_control_corr.npy')
        plt.clf()
        plt.imshow(im)
        plt.title('Partial Correlation between GPP and Precip controlling Ta')
        plt.colorbar()
        # plt.savefig('GPP_precip_Partial_correlation.jpg')
        plt.show()

