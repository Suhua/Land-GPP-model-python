__author__ = 'swei'
import numpy as np
import pandas as pd
import scipy.misc as sm
from scipy.ndimage import zoom
from scipy.io import netcdf
from scipy import io
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.externals.six import StringIO
import os
import pydot
import glob
from pyhdf import SD
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor


class GridData():
    def __init__(self,filenum):
        self.filenum=filenum

    def temperture(self):
        f = netcdf.netcdf_file(r"E:\Research\Gridded Data\NC\NC_data\air.mon.mean.nc", 'r')
        var = f.variables['air']
        id = self.filenum + 624
        data = var.data[id,:,:]
        temp = data * var.scale_factor + var.add_offset
        ta = np.zeros((360 , 720) , dtype = float)
        ta[: , 360:] = temp[: , :360]
        ta[: , :360] = temp[: , 360:]
        return ta[: , :]

    def fPAR(self,month,year):
        '''fPar is an unitless value ranging from 0 to 1, with monthly step and 0.5 x 0.5 spatial resolution'''
        month=month
        hdf_files = glob.glob(r'E:\Research\Gridded Data\Vegetation Index\LAI and FPAR\fPAR200{0}\*HDF'.format(year))
        cnt = 0
        for fn in hdf_files:
            if fn.endswith('HDF'):
                cnt += 1
                if cnt == int(month) + 1:
                    # print cnt
                    data = SD.SD(fn).select('fapar').get()
                    data = np.ma.masked_where(data == 255, data) / 255.0
                    return data

    def evi(self):
        '''fPar is an unitless value ranging from 0 to 1, with monthly step and 0.5 x 0.5 spatial resolution'''
        hdf_files = glob.glob(r'E:\Research\Gridded Data\Vegetation Index\EVI\*.hdf')
        id=self.filenum
        data = SD.SD(hdf_files[id]).select('CMG 0.05 Deg Monthly EVI').get() * 0.0001
        data = sm.imresize(data, [360, 720], interp='nearest') / 255.0
        evi_data= np.ma.masked_where(data == 0, data)
        return evi_data

    def precip(self):
        f = netcdf.netcdf_file(r'E:\Research\Gridded Data\NC\NC_data\precip.mon.mean.0.5x0.5.nc', 'r')
        # print f.dimensions,f.references
        var = f.variables['precip']
        id=self.filenum+624
        data = var.data[id, :, :].squeeze()
        pre = np.zeros((360, 720), dtype=float)
        pre[:, 360:] = data[:, :360]
        pre[:, :360] = data[:, 360:]
        pre = np.ma.masked_where(pre < -10000, pre)
        # plt.imshow(pre)
        # plt.colorbar()
        # plt.show()
        return pre

    def par(self):
        '''long_name: Monthly Mean of Net Shortwave Radiation Flux
        units: W/m^2; precision: 1'''
        f = netcdf.netcdf_file(r'E:\Research\Gridded Data\NC\NC_data\nswrs.sfc.mon.mean.nc' , 'r')
        var = f.variables['nswrs']
        id = self.filenum + 636
        # Par is considered as 45% of the net shortwave radiation, divided by 11.58 to get MJ
        data = var[id , : , :] * 0.45
        #  Resize the data into 0.5x0.5 degree ([360,720])
        sr = -zoom(data[: , :] , [360 / 94.0 , 720 / 192.0] , mode='nearest')
        return sr

    def kp(self):
        kopTyp=np.load(r'E:\Research\Gridded Data\Koppen Climate\kg.npy')
        return kopTyp

    def pft(self):
        lc = io.loadmat('E:\Research\Gridded Data\PDSI\lc.mat')['lc']
        return lc


class TowerAlpha():
    # def __init__(self,siteName,lat,lon):
    #     self.siteName=siteName
    #     self.lat=lat
    #     self.lon=lon
    def getAlpha(self, df):
        df = df.ix[:, 1:]
        df.ix[:, 5] = df.ix[:, 5].fillna(0)
        df.ix[:, 16] = df.ix[:, 16].fillna(0)
        # for i in range(len(df.index)):
        #     df.ix[i, 5:] = df.ix[i, 5:].fillna(df.ix[i, 5:].mean())

        df.ix[:, 5:] = df.ix[:, 5:].interpolate(method='linear', axis=1).copy()
        # lats = df.Latitude
        # lons = df.Longitude
        alpha = {}
        for site in df.index:
            alpha[site] = df.ix[site, 5:].as_matrix()
        return alpha

def gridToPoint(lats, lons):
    lat_ind=[]
    lon_ind=[]
    for lat in lats:
        if -90 <= lat <= 90:
            lat = 90 -lat
            ind = int(lat // 0.5)
            lat_ind.append(ind)
    for lon in lons:
        if -180 <= lon <= 180:
            lon += 180
            ind = int(lon // 0.5)
            lon_ind.append(ind)
    return lat_ind, lon_ind

def fillMissValue(vector):
     temp=pd.DataFrame(vector)
     temp=temp.fillna(temp.mean())
     return temp.as_matrix()[:,0]

###-------------------------------Main function starts here-------------------------------------------------------------
##------------Training process------------------------------------------------------------------------------------------

df = pd.read_csv(r"E:\Research\modelling\machine learning\complete_info_alpha.csv", header=0, index_col=1)



for month in range(1,13):

    cnt=0
    target=[]
    lats=[]
    lons=[]
    features=np.zeros([6*250+1,7],dtype=float)
    for year in range(2000,2006):
        ## get the tower data
        T = TowerAlpha()
        alpha= T.getAlpha(df)
        sitNam=alpha.keys()


        # get the alpha (monthly GPP for the selected year)

        # get the latitudes and longitude info from tower data, and calculate the grid positions at global raster data sets
        for site in sitNam:
            if site in df.index:
               target.append(alpha[site][month-1])
               lats.append(df[df.index==site]['Latitude'][0])
               lons.append(df[df.index==site]['Longitude'][0])

               # sites.append(site)
        lat_ind,lon_ind = gridToPoint(lats,lons)
        del lats,lons
        lats=[]
        lons=[]




        ## get the explanatory variables
        filenum = (year - 2000) * 12 + month - 1
        G = GridData(filenum)
        pre = G.precip()
        evi = G.evi()
        ra = G.par()
        ta = G.temperture()
        kp = G.kp()
        pft = G.pft()
        fpar= G.fPAR(month-1,year-2000)


        # pre=np.ma.masked_where(pre<-10000,pre)
        # plt.imshow(pre)
        # plt.colorbar()
        # plt.show()

        for (r,c) in zip(lat_ind,lon_ind):
            features[cnt,0] = pre[r,c]
            features[cnt,1] = evi[r,c]
            features[cnt,2] = ra[r,c]
            features[cnt,3] = kp[r,c]
            features[cnt,4] = pft[r,c]
            features[cnt,5] = ta[r,c]
            features[cnt,6] = fpar[r,c]
            cnt+=1


    # deal with missing values by the process defined early
    features[:,1]=fillMissValue(features[:,1])
    features[:,6]=fillMissValue(features[:,6])
    # print features[:,1]
    # for i in range(0,6):
        # print features[:,i]
    print cnt
    expVar=features[0:cnt,:].copy()
    if len(target)==np.size(expVar,0):
        clf=DecisionTreeClassifier()
        clf=clf.fit(expVar,target)
    else:
        print 'GPP length is '+str(len(target))+',while expVar length is '+str(np.size(features,0))

    # os.unlink('iris.dot')
    # dot_data=StringIO()
    # tree.export_graphviz(clf,out_file=dot_data)
    # graph=pydot.graph_from_dot_data(dot_data.getvalue())
    # graph.write_pdf('training.pdf')
##------Prediction process----------------------------------------------------------------------------------------------
    output=np.zeros([360,720],dtype=float)
    output=np.ma.masked_where(pft==0,output)
    for r in range(0,360):
        for c in range (0,720):

            if pft[r,c]==16 or output[r,c] is np.ma.masked or pre[r,c] is np.ma.masked or evi[r,c] is np.ma.masked or fpar[r,c] is np.ma.masked:
                pass
            else:
                features=np.zeros([1,7],dtype=float)
                features[0,0] = pre[r, c]
                features[0,1] = evi[r,c]
                features[0,2] = ra[r, c]
                features[0,3] = kp[r, c]
                features[0,4] = pft[r, c]
                features[0,5] = ta[r, c]
                features[0,6]=fpar[r,c]
                output[r,c]=clf.predict(features)

        # output=np.ma.masked_where(output>9,output)
        # output = np.ma.masked_where(output <0, output)
        #calcalate total GPP

    # area_weight = io.loadmat(r'E:\Research\Gridded Data\NC\area_360x720.mat')
    # area = area_weight['area_global']
    # output = output * area / 1000000000000000*30
    # MonthlyGPP=np.sum(np.sum(output))
    # print MonthlyGPP
    output.dump('decisionTree_alpha_Mo{0}.npy'.format(month))
