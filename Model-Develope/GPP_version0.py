import numpy as np
from scipy.io import netcdf
import scipy.misc as sm
from scipy.ndimage import zoom
from scipy import io
import matplotlib.pylab as plt
import glob
import pandas as pd
from pyhdf import SD, HDF
from mpl_toolkits import basemap


class gridData():
    '''GPP (Gross Primary Production) is calculated as GPP=alpha*fPAR*PAR; alpha is the specific light use efficiency at monthly step;PAR is partial
     active radiation ; fPAR is the fraction of partial active radiation '''

    def fPAR(self, month, year):
        '''fPar is an unitless value ranging from 0 to 1, with monthly step and 0.5 x 0.5 spatial resolution'''
        hdf_files = glob.glob(r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\fPAR200{0}\*.HDF'.format(year))
        cnt = 0
        for fn in hdf_files:
            if fn.endswith('HDF'):
               cnt += 1
               if cnt == month:
                  data = SD.SD(fn).select('fapar').get()
                  data = np.ma.masked_where(data == 255, data) / 255.0
                  return data


    def PAR(self, month, year):
        '''long_name: Monthly Mean of Net Shortwave Radiation Flux
        units: W/m^2; precision: 1'''
        f = netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\nswrs.sfc.mon.mean.nc', 'r')
        Var = f.variables['nswrs']
        sta = np.linspace(636, 756, 10)
        end = sta + 12
        # Par is considered as 45% of the net shortwave radiation, divided by 11.58 to get MJ
        data = Var[int(sta[year]):int(end[year]), :, :] * 0.45 / 11.58
        #  Resize the data into 0.5x0.5 degree ([360,720])
        sr = -zoom(data[month - 1, :, :], [360 / 94.0, 720 / 192.0], mode='nearest')
        # plt.imshow(sr)
        # plt.colorbar()
        # plt.show()
        # print np.max(sr),np.min(sr),np.max(data[mon,:,:]),np.min(data[mon,:,:])
        return sr



class TowerAlpha():
    # def __init__(self,siteName,lat,lon):
    #     self.siteName=siteName
    #     self.lat=lat
    #     self.lon=lon
    def Alpha(self,month):
        files = glob.glob(r'G:\Research\modelling\model_development1\*.npy')
        # print files

        list = []
        rank = []

        for f in files:
            name = f.split('\\')[-1]
            if name.startswith('alpha'):
                list.append(f)
                rank.append(int(name.split('_')[-1].split('.')[0]))
        dic = dict(zip(rank, list))
        return np.load(dic.get(month))




 #------------------Main Function--------------------------------------------------------------------------------------
GPP=gridData()

for month in range(1, 13):
    ten_year_mean = np.zeros((360, 720, 1), dtype=float)
    for year in range(1, 6):
        fpar = GPP.fPAR(month, year)
        PAR = GPP.PAR(month, year)
        alpha = TowerAlpha().Alpha(month)
        # print alpha
        output = alpha * fpar * PAR
        output.dump('GppMeanLUE{0}_{1}'.format(year,month))
