__author__ = 'swei'
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

fluxnet=pd.read_csv(r'G:\Research\modelling\model_development\data\fluxnet_2004-2005-monthly.csv')
site_aggr=pd.DataFrame(fluxnet).groupby('site_id',as_index=False)

s_id=[]
s_reorder=[]
kg_climate=[]
kg_climate_reorder=[]
for name,grouped in site_aggr:
    pft=grouped['kg_climate_type'][0:1].values[0]
    s_id.append(name)
    kg_climate.append(pft)

kgDF=pd.DataFrame({'siteID':s_id,'kg':kg_climate})


# season=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\JJA.csv')
season=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\MAM.csv')
# season=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\SepON.csv')

# print JJA.head,'\n',season.head,'\n',SON.head
# Aggregation Analysis
# print 'Spring'
siteID=season['\'sitename\'']
# Remove the string Quotation Mark of the site_name
del s_id
s_id=list(range(0,len(siteID)))
for i in range(0,len(siteID)):
    s_id[i]= siteID[i][1:7]
# print siteID
#
# print kgDF['s_id'],siteID
pft=season['IGBP']
rsquare=season['\'rsquare\'']
alpha=season['\'alpha\'']
ta=season['\'ta\'']
precip=season['\'Pre\'']
Amax=season['\'a\'']
VPD=season['\'VPD\'']
Mean=pd.DataFrame({'siteID':s_id,'alpha':alpha,'veg':pft,'rsquare':rsquare,'Amax':Amax,'ta':ta,'precip':precip,'vpd':VPD})

merg=pd.merge(Mean,kgDF,how='left',on=None,left_index=False,right_index=False,copy=True)
print merg
## Join the Mean dataFrame to kg_climate



merg=merg[merg['Amax']<80]
merg=merg[merg['alpha']<0.1]

# cnt=0
frame=[grouped['vpd'] for name,grouped in merg.groupby('kg')]
veg_name=[name for name,grouped in merg.groupby('kg')]
result=pd.concat(frame,axis=1,keys=veg_name)
merg=result.get(veg_name).mean()
merg.to_csv('vpd_kg_spr.csv',index=veg_name)
