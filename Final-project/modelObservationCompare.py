import numpy as np
import pandas as pd
from scipy import io
import glob
import matplotlib.pylab as plt
from matplotlib import rc
font = {'family': 'Times New Roman ',
        'weight': 'bold',
        'size': 28}
rc('font', **font)

# lc = io.loadmat(r'G:\Research\Gridded Data\PDSI\lc.mat')['lc']
files = glob.glob(r'D:\Research\modelling\model_development1\RFR-LUE-GPP\*.npy')
files1 = glob.glob(r'D:\Research\modelling\model_development1\tower-LUE-GPP\*.npy')
files2 = glob.glob(r'D:\Research\modelling\model_development1\RandomForest_GPP\*.npy')
# data = np.load(files1[0])
# plt.imshow(data)
# plt.colorbar()
# plt.show()
def AverageGpp(file):
    data = np.zeros([len(file), 360, 720], dtype=float)
    for i in range(0, len(file)):
        data[i, :, :] = np.load(file[i])
    gpp = np.sum(data, axis=0) / 6
    gpp = np.ma.masked_where(gpp == 0, gpp)
    return gpp

''' get tower GPP data'''
def getGpp( year):
    year = str(year)
    df = pd.read_csv("D:\Research\modelling\machine learning\gpp.monthly.csv")
    gppValue = {}
    totalSite = 0
    # for item in df.columns:
    #     if np.isnan(df.ix[0, item]):
    #         df.ix[0, item] = 0
    # df = df.interpolate(method='linear', axis=1)

    for item in df.columns[1:]:
        site, yr = item.split('.')
        if yr == year:
            dfSite = df[item].interpolate(method='linear')
            if np.any(dfSite.as_matrix() is np.nan):
                pass
            else:
                totalSite += 1
                gppValue[site] = np.mean(df[item].as_matrix());
    gpp=pd.DataFrame.from_dict(gppValue,orient='index')
    return gpp

def gridToPoint(lat, lon):
    if -90 <= lat <= 90:
        lat = 90 - lat
        lat_ind = int(lat // 0.5)

    if -180 <= lon <= 180:
        lon += 180
        lon_ind = int(lon // 0.5)
    return lat_ind, lon_ind

#-------Main funtion starts here----------------------------------------------------------
'''get the tower GPP from 2000-2005'''
df1 = getGpp(2000)
df2 = getGpp(2001)
df3 = getGpp(2002)
df4 = getGpp(2003)
df5 = getGpp(2004)
df6 = getGpp(2005)
#
result = pd.concat([df1,df2,df3,df4,df5,df6],axis = 1, join ='outer')

'''get the modeled GPP by from different RFR-LUE-GPP model, tower-LUE-GPP model and FRF-GPP model'''
rfrLUEgpp = AverageGpp(files)*30/365.0
towerLUEgpp =AverageGpp(files1)/365.0
rfrGpp = AverageGpp(files2)*6*30/365.0
# plt.imshow(rfrGpp)
# plt.colorbar()
# plt.show()
# #
df1 = pd.ExcelFile(r"D:\Research\modelling\machine learning\fluxnet_2004-2005-monthly.xlsx", header=0, index_col=0,
                   parse_cols=0, has_index_name=True)
df1 = pd.ExcelFile.parse(df1, header=0)
siteName = df1.site_id
siteLat = {}
siteLon = {}
siteVeg = {}
rfrLUE_DownGPP = {}
towerLUE_DownGPP = {}
RFR_DownGPP = {}
for s in result.index:
    cnt = 0
    for site in siteName:
        if (s == site):
            latitude = df1.latitude.as_matrix()[cnt]
            siteLat[site] = latitude
            longitude = df1.longitude.as_matrix()[cnt]
            siteLon[site] = longitude
            siteVeg[site] = df1.igbp_veg_type.as_matrix()[cnt]
            indRow, indCol = gridToPoint(latitude,longitude)
            rfrLUE_DownGPP[site] = rfrLUEgpp[indRow,indCol]
            towerLUE_DownGPP[site] = towerLUEgpp[indRow,indCol]
            RFR_DownGPP[site] = rfrGpp[indRow,indCol]
        cnt += 1
lat=pd.DataFrame.from_dict(siteLat,orient='index')
lon = pd.DataFrame.from_dict(siteLon, orient='index')
veg = pd.DataFrame.from_dict(siteVeg, orient='index')
rfrLUEdf = pd.DataFrame.from_dict(rfrLUE_DownGPP,orient='index')
towerLUEdf = pd.DataFrame.from_dict(towerLUE_DownGPP,orient='index')
RFRdf = pd.DataFrame.from_dict(RFR_DownGPP,orient='index')
result = pd.concat([veg,lat,lon,result,rfrLUEdf,towerLUEdf,RFRdf], axis = 1, join = 'inner')
result.to_excel('results.xlsx')
