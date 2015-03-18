import numpy as np
import pandas as pd
import os
from scipy.io import netcdf
import scipy.io as io
from scipy.ndimage import zoom
import matplotlib.pylab as plt
import glob
from pyhdf import SD,HDF

class GPP:
    '''GPP (Gross Primary Production) is calculated as GPP=alpha*fPAR*PAR; alpha is the specific light use efficiency at monthly step;PAR is partial
     active radiation ; fPAR is the fraction of partial active radiation '''

    def fPAR(self,month):
        '''fPar is an unitless value ranging from 0 to 1, with monthly step and 0.5 x 0.5 spatial resolution'''
        hdf_files=glob.glob(r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\2004to2005fPAR\*.HDF')
        cnt=0
        for fn in hdf_files:
            if fn.endswith('HDF'):
                cnt+=1
                if cnt==month:
                    data=SD.SD(fn).select('fapar').get()
                    data=np.ma.masked_where(data==255,data)/255.0
                    return data

    def PAR(self,month):
        '''long_name: Monthly Mean of Net Shortwave Radiation Flux
        units: W/m^2; precision: 1'''
        f=netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\nswrs.sfc.mon.mean.nc','r')
        Var=f.variables['nswrs']
        # Par is considered as 45% of the net shortwave radiation, divided by 11.58 to get MJ
        data=Var[672:696,:,:]*0.45/11.58
        #  Resize the data into 0.5x0.5 degree ([360,720])
        sr=-zoom(data[month-1,:,:],[360/94.0,720/192.0],mode='nearest')
        # plt.imshow(sr)
        # plt.colorbar()
        # plt.show()
        # print np.max(sr),np.min(sr),np.max(data[mon,:,:]),np.min(data[mon,:,:])
        return sr

    def Alpha(self,month):
        files=glob.glob('*.npy')
        for f in files:
            if f.endswith('_{0}.npy'.format(month)):
                alpha=np.load(f)
                alpha=np.ma.masked_where(alpha==0,alpha)
        return alpha


#--------------------------Main funtion starts here---------------------------------------------------------------------
GPP=GPP()
total_GPP=0
for month in range(1,13):
    fpar=GPP.fPAR(month)
    PAR=GPP.PAR(month)
    alpha=GPP.Alpha(month)
    # print alpha
    output=alpha*fpar*PAR
    area_weight=io.loadmat(r'G:\Research\Gridded Data\NC\area_360x720.mat')
    area=area_weight['area_global']
    output=output*area/1000000000000000
    total_GPP=total_GPP+np.sum(np.sum(output))*30
    # plt.imshow(output)
    # plt.colorbar()
    # plt.show()

print total_GPP*0.85
