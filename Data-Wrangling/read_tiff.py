__author__ = 'swei'
import numpy as np
from numpy import ma
import matplotlib.pylab as plt
import glob
import os
import pandas as pd
import libtiff

# Configure the path
path=r'G:/Vegetation Index/LAI and FPAR/Monthly 2004to2005'
os.chdir(path)

# Match the lat and lon info to the array locations
def read_lat_lon(lat,lon,lat_r,lon_r):
    '''read the lat and lon at specific lat and lon resolution(lat_r and lon_r), return the index of lat and lon at
     gridded data set, by default, lat ranges from -90 to 90 northward and lon ranges -180 to 180 eastward '''
    if (lat>=-90 and lat<=90):
        lat=90-lat
    if (lon>=-180 and lon<=180):
        lon=lon+180
    lat_ind=int(lat//lat_r)
    lon_ind=int(lon//lon_r)
    return lat_ind, lon_ind
# get the tiff image data
files=glob.glob('*.tiff')
num_files=len(files)

#plot image of the data
image=libtiff.TIFF.open(files[0])
image=image.read_image()
image=ma.masked_where(image==255,image)
plt.imshow(image)
plt.colorbar()
plt.show()
del image
# get the tower locations from CSV files
f_csv=pd.read_csv('G:/Flux Data/flux_PP/siteInfo.csv')

lat=f_csv['Lat']
site_name=f_csv['sitename']



# initilize the input
ifile=0
output=np.zeros((num_files,len(site_name)),dtype=float)

for i in range(0,len(files)):
    print i
    image=libtiff.TIFF.open(files[i])
    image=image.read_image()
    for cnt in range(0,len(lat)):
            ilat=f_csv['Lat'][cnt]
            ilon=f_csv['Lon'][cnt]
            pft=f_csv['IGBP'][cnt]
            lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
            output[i,cnt]=float(image[lat_ind,lon_ind])
            #tem_data=tem_data.compressed()
# for i in range(0,204):
#     print site_name[i]
#     print output[:,i]

np.save('LAI'+'.npy','output')

