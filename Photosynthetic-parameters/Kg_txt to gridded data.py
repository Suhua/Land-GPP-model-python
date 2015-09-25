__author__ = 'swei'
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


file_path=r'G:\Research\Gridded Data\Koppen Climate\1976-2000_ASCII.txt'

'''open txt file, load koppen climate data as list with its latitude and longitude information; latitudates 
and longitudes are gridded by 0.5 times 0.5 degree of spatial resolution, with ocean information are missing. '''


datain=pd.read_table(file_path,sep='\s+',header=False)

# print datain.index,'\n', datain.columns
''' create DataFrame for the existing land kg types'''
kg=datain['Cls']
lats=datain['Lat']
lons=datain['Lon']
land_DF=pd.DataFrame({'kg':kg,'lats':lats,'lons':lons})


'''with filling the ocean area with NAN data, we create a grided dataset covering the whole globe. This is accomplised by three 
steps. First, create a list of lat and lon covering the whole globe; Second, create a complete DataFrame out of it. Third, merge the 
existing land kg dataFrame with the complete DataFrame, the ocearn spots will be filled with 'nan' aumomatically'''
glat=np.linspace(-89.75,89.75,num=360)
glon=np.linspace(-179.75,179.75,num=720)
lat=np.zeros(len(glat)*len(glon))
lon=np.zeros(len(glat)*len(glon))
cnt=0
for i in glat:
    for j in glon: 
        cnt+=1
        lon[cnt-1]=j
        lat[cnt-1]=i

complete_DF=pd.DataFrame({'lats':lat,'lons':lon})
merg=pd.merge(complete_DF,land_DF,how='left',left_index=False,right_index=False)

#save the data
# os.chdir(r'G:\Research\modelling\model_development\predicting_pp')
# merg.to_csv('filled_kg.csv')

'''emuerate the kg types'''

kg=merg['kg']
kg_name=list(set(kg))
kg_num=range(0,len(kg_name))

# tem=kg_name[1]
# kg_name[1]=kg_name[23]
# kg_name[23]=tem
# del tem

'''create kg_type look-up table'''
print zip(kg_num,kg_name)


''' set numeric value to kg_types by its look-up table'''
num=np.zeros(len(kg),dtype=float)
i=0
for item in kg:
    cnt=0
    i+=1
    for k in kg_name:
        cnt+=1
        if item==k:
           num[i-1]=kg_num[cnt-1]


'''reshape the data into [360,720]'''
data=num.reshape((360,720))

''' data visualization'''
plt.imshow(np.flipud(data))
plt.colorbar()
plt.show()

#save data to csv
# data=pd.DataFrame(data)
# os.chdir(r'G:\Research\modelling\model_development\datasets_for_PP_prediction')
# data.to_csv('kg_numeric.csv')


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


'''Read the fluxnet towers latitudes and longitudes, '''
site=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\KoppenClimateAnalysis\PP_JJA.csv')
num_site=len(site['siteID'])
siteID=site['siteID']
Var_output=np.zeros(num_site,float)
'''initialize the output array'''

for cnt in range(0,num_site): # loop through all the sites
    lat=site['lat'][cnt]
    lon=site['lon'][cnt]
    ilat,ilon=read_lat_lon(lat,lon,0.5,0.5)
    Var_output[cnt]=kg[ilat,ilon]
Var_output=[Var_output]*24
# '''Plot the output data'''
# plt.imshow(Var_output)
# plt.colorbar()
# plt.show()


''' Save is to Pandas Data Frame, index is the time series, and columns are site name'''
month=list(range(0,24))
i=0
while i<24:
      if i<12:
         month[i]=datetime.date(2004,i+1,1).isoformat()
         i+=1
      else:
         i+=1
         month[i-1]=datetime.date(2005,i-12,1).isoformat()
kg_DF=pd.DataFrame(Var_output,index=month,columns=siteID)
out_path=r'G:\Research\modelling\model_development\predicting_pp'
out_file=os.path.join(out_path,'kg_DF.csv')
kg_DF.to_csv(out_file)
