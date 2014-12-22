__author__ = 'swei'

import numpy as np
from numpy import ma
import matplotlib.pylab as plt
import glob
import os
import pandas as pd
import libtiff
import datetime


path=r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\LAI'
'''set the path'''
os.chdir(path)


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
# image=libtiff.TIFF.open(files[0])
# image=image.read_image()
# image=ma.masked_where(image>200,image)

# plt.imshow(image)
# plt.colorbar()
# plt.show()
# del image


site=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\KoppenClimateAnalysis\PP_JJA.csv')
'''Read the fluxnets tower latitudes and longitudes'''
num_site=len(site['siteID'])
siteID=site['siteID']


'''initilize the input'''
output=np.zeros((num_files,num_site),dtype=float)

for i in range(0,len(files)):    
    image=libtiff.TIFF.open(files[i])
    image=image.read_image()
    for cnt in range(0,num_site):
            ilat=site['lat'][cnt]
            ilon=site['lon'][cnt]
            lat_ind,lon_ind=read_lat_lon(ilat,ilon,0.5,0.5)
            output[i,cnt]=float(image[lat_ind,lon_ind])
            #tem_data=tem_data.compressed()

month=list(range(0,num_files))
month[0]=datetime.date(2004,1,1).isoformat()
old_date=datetime.date(2004,1,1)
i=0
while i<num_files-1:
    i+=1
    old_date=old_date+datetime.timedelta(days=8)
    print i
    month[i]=old_date.isoformat()

lai_DF=pd.DataFrame(output/255.0,index=month,columns=siteID)
out_path=r'G:\Research\modelling\model_development\predicting_pp'
out_file=os.path.join(out_path,'lai_DF.csv')
lai_DF.to_csv(out_file)
