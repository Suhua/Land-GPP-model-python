import numpy as np
from scipy.io import netcdf
import scipy.misc as sm
from scipy.ndimage import zoom
from scipy import io
import matplotlib.pylab as plt
import glob
import os
from pyhdf import SD,HDF
from mpl_toolkits import basemap
import glob

files= glob.glob(r'G:\Research\modelling\model_development1\gpp\*npy')
dtFiles = glob.glob(r'G:\Research\modelling\machine learning\*npy')
dtLatMea=np.mean(np.sum(np.load(dtFiles[0]),axis=1))



for i in range(1,len(dtFiles)):
    dtLatMea=np.add(dtLatMea,np.sum(np.load(dtFiles[i]),axis=1))
dtLatMea=dtLatMea/6


latMea=np.sum(np.load(files[0]),axis=1)
# print len(latMea)
for i in range(1,len(files)):
    latMea=np.add(latMea,np.sum(np.load(files[i]),axis=1))
latMea=latMea/6

# print np.ma.getdata(latMea)
def smooth(vector):
    # arr=vector.copy()
    arr=np.ma.getdata(vector)
    for i in range(2,len(arr)-2):
        if arr[i] is np.ma.masked or arr[i+1] is np.ma.masked:
            pass
        else:
           arr[i]=sum(arr[i-2:i+2])/5
    return arr

# latMea=smooth(latMea)
latMea=np.ma.masked_where(latMea<0.00001,latMea)

# dtLatMea=smooth(dtLatMea)
dtLatMea=np.ma.masked_where(dtLatMea<0.00001,dtLatMea)
x=np.linspace(-90,90,361)
x=np.flipud(x)
# print len(x[51:]),len(latMea[51:])
plt.plot(x[61:-40],latMea[60:-40]*1000,x[61:-40],dtLatMea[60:-40]*1000,linewidth=3)
plt.xlabel('Latitudes ($^0N$)',size=16)
plt.ylabel('GPP (Gkg/yr)',size=16)
plt.xticks(size=14)
plt.yticks(size=14)
plt.ylim([0,1800])
plt.show()


