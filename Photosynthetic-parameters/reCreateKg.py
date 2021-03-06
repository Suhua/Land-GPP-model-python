__author__ = 'swei'
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from mpl_toolkits import basemap


file_path = r'G:\Research\Gridded Data\Koppen Climate\1976-2000_ASCII.txt'

'''open txt file, load koppen climate data as list with its latitude and longitude information; latitudates
and longitudes are gridded by 0.5 times 0.5 degree of spatial resolution, with ocean information are missing. '''

datain = pd.read_table(file_path, sep='\s+', header=False)

# print datain.index,'\n', datain.columns
''' create DataFrame for the existing land kg types'''
kg = datain['Cls']
lats = datain['Lat']
lons = datain['Lon']
land_DF = pd.DataFrame({'kg': kg, 'lats': lats, 'lons': lons})

'''with filling the ocean area with NAN data, we create a grided dataset covering the whole globe. This is accomplised by three
steps. First, create a list of lat and lon covering the whole globe; Second, create a complete DataFrame out of it. Third, merge the
existing land kg dataFrame with the complete DataFrame, the ocearn spots will be filled with 'nan' aumomatically'''
glat = np.linspace(-89.75, 89.75, num=360)
glon = np.linspace(-179.75, 179.75, num=720)
lat = np.zeros(len(glat) * len(glon))
lon = np.zeros(len(glat) * len(glon))
cnt = 0
for i in glat:
    for j in glon:
        cnt += 1
        lon[cnt - 1] = j
        lat[cnt - 1] = i

complete_DF = pd.DataFrame({'lats': lat, 'lons': lon})
merg = pd.merge(complete_DF, land_DF, how='left', left_index=False, right_index=False)

#save the data
# os.chdir(r'G:\Research\modelling\model_development\predicting_pp')
# merg.to_csv('filled_kg.csv')

'''emuerate the kg types'''

kg = merg['kg']
kg_name = sorted(list(set(kg)))


kg_num = range(0, len(kg_name))


# tem=kg_name[1]
# kg_name[1]=kg_name[23]
# kg_name[23]=tem
# del tem

'''create kg_type look-up table'''
dic= dict(zip(kg_name,kg_num))
print dic

''' set numeric value to kg_types by its look-up table'''
num = np.zeros(len(kg), dtype=float)
i = 0
for item in kg:
    cnt = 0
    i += 1
    for k in kg_name:
        cnt += 1
        if item == k:
            num[i - 1] = kg_num[cnt - 1]

'''reshape the data into [360,720]'''
data = num.reshape((360, 720))
data= np.flipud(data)
# data.dump('kg.npy')
''' data visualization'''
im = np.ma.masked_where(data == 0, data)
fig = plt.figure()
ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
lats = np.linspace(90, -90, 360)
lons = np.linspace(-180, 180, 720)
m = basemap.Basemap(projection='robin', lon_0=0.0, resolution='c')
m.drawparallels(np.arange(-90, 90, 30))
m.drawmeridians(np.arange(-180, 180, 60))
m.drawcoastlines()
lons, lats = np.meshgrid(lons, lats)
im = m.pcolormesh(lons, lats, im, cmap=plt.cm.jet, latlon=True)
# mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax.set_title('Koppen Climate Classification', fontsize=24)
cb = m.colorbar(im, 'right', size='1%')
cb.set_clim(vmin=0, vmax=31)
plt.show()
