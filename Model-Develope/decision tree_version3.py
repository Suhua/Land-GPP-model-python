_author__ = 'swei'
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


class TowerData():
    # def __init__(self,siteName,lat,lon):
    #     self.siteName=siteName
    #     self.lat=lat
    #     self.lon=lon
    def getGpp(self,year):
        year=str(year)
        df=pd.read_csv("E:\Research\modelling\machine learning\gpp.monthly.csv")
        # print df.columns.tolist
        gppYear={}
        totalSite=0
        for item in df.columns:
            if np.isnan(df.ix[0, item]):
                df.ix[0, item] = 0

        df = df.interpolate(method='linear', axis=1)
        for item in df.columns[1:]:
            # print item
            site,yr=item.split('.')
            if yr==year:
               dfSite=df[item].interpolate(method='linear')
               if np.any(dfSite.as_matrix() is np.nan):
                   pass
               else:
                   totalSite+=1
                   gppYear[site]=df[item].as_matrix()
        return gppYear,totalSite


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

for year in range(2000,2006):
    total_GPP=0
    for month in range(1,13):
        T = TowerData()
        gpp,totalSite= T.getGpp(year)
        features=np.zeros([totalSite,7],dtype=float)
        sitNam=gpp.keys()
        target=[]
        for site in sitNam:
            target.append(gpp[site][month-1])

        df_info=pd.ExcelFile(r"E:\Research\modelling\machine learning\fluxnet_2004-2005-monthly.xlsx",header=0,index_col=0,parse_cols=0,has_index_name=True)
        df_info=pd.ExcelFile.parse(df_info,index_col=0,header=0)
        df = df_info[df_info.mm==1]
        lats=[]
        lons=[]
        sites=[]
        for site in sitNam:
            if site in df.index:
               lats.append(df[df.index==site]['latitude'][0])
               lons.append(df[df.index==site]['longitude'][0])
               sites.append(site)

        # print lats,'\n',lons
        filenum = (year - 2000) * 12 + month - 1
        G = GridData(filenum)
        pre = G.precip()
        evi = G.evi()
        ra = G.par()
        ta = G.temperture()
        kp = G.kp()
        pft = G.pft()
        fpar= G.fPAR(month-1,year-2000)

        lat_ind,lon_ind = gridToPoint(lats,lons)
        # print lat_ind,'\n',lon_ind
        cnt=0
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

        def fillMissValue(vector):
            temp=pd.DataFrame(vector)
            temp=temp.fillna(temp.mean())
            return temp.as_matrix()[:,0]

        features[:,1]=fillMissValue(features[:,1])
        features[:,6]=fillMissValue(features[:,6])
        # print features[:,1]
        # for i in range(0,6):
            # print features[:,i]
        clf=DecisionTreeClassifier()
        clf=clf.fit(features,target)

    # os.unlink('iris.dot')
    # dot_data=StringIO()
    # tree.export_graphviz(clf,out_file=dot_data)
    # graph=pydot.graph_from_dot_data(dot_data.getvalue())
    # graph.write_pdf('training.pdf')

        output=np.zeros([360,720],dtype=float)
        output=np.ma.masked_where(pft==0,output)
        for r in range(0,360):
            for c in range (0,720):
                if output[r,c]==0:
                    features=np.zeros([1,7],dtype=float)
                    if pre[r,c] is np.ma.masked:
                        features[0,0]=0
                    else:
                        features[0,0] = pre[r, c]

                    if evi[r,c] is np.ma.masked:
                        features[0,1]=0
                    else:
                        features[0,1] = evi[r,c]

                    features[0,2] = ra[r, c]
                    features[0,3] = kp[r, c]
                    features[0,4] = pft[r, c]
                    features[0,5] = ta[r, c]
                    if fpar[r,c] is np.ma.masked:
                        features[0,6]=0
                    else:
                        features[0,6]=fpar[r,c]


                    output[r,c]=clf.predict(features)

        # output=np.ma.masked_where(output>9,output)
        # output = np.ma.masked_where(output <0, output)
        #calcalate total GPP
        area_weight = io.loadmat(r'E:\Research\Gridded Data\NC\area_360x720.mat')
        area = area_weight['area_global']
        output = output * area / 1000000000000000*30
        output.dump('decisionTreeYr{0}Mo{1}.npy'.format(year,month))
        del output
