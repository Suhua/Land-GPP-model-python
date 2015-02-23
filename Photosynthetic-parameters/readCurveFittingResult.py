from scipy import io
import pandas as pd
import numpy as np
import glob

filename=glob.glob('*.mat')
name_list=[]
for item in filename:
    sl=[item[:2],'-',item[2:5]]
    name_list.append(''.join(sl))
name_list=name_list[:-1]

pp=io.loadmat(r'C:\Users\swei\Research\fluxdata\LaThuile\hourly\zz_output.mat')
pp=pp['output']

data=np.zeros(pp.shape,dtype=float)
for i in range(pp.shape[0]):
    for k in range(pp.shape[1]):
        for v in range(pp.shape[2]):
            data[i,k,v]=round(pp[i,k,v],4)

key=['alpha','Amax','Reco','r2']
panel=pd.Panel(data,items=name_list,major_axis=range(1,13),minor_axis=key)

season=pd.read_csv(r'C:\Users\swei\Research\fluxdata\Flux Data\flux_PP\PP\newJJA.csv',index_col=1)
print season.index
siteID=season.index.tolist()
lats=season['Latitudes']
lons=season['Longitudes']


site_list=[]
lats=[]
lons=[]
pft=[]
for site in name_list:
    site_list.append(site)
    if site in siteID:
        lats.append(season.get_value(site,'Latitudes'))
        lons.append(season.get_value(site,'Longitudes'))
        pft.append(season.get_value(site,'IGBP'))
    else:
        lats.append(0)
        lons.append(0)
        pft.append(0)

print site_list,'\n',lats,'\n',lons

import os
os.chdir(r'C:\Users\swei\Research\fluxdata\Flux Data\flux_PP\PP')
df=pd.DataFrame({'sitename':site_list,'lat':lats,'lon':lons,'pft':pft})
