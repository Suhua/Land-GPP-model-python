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

kgDF=pd.DataFrame({'s_id':s_id,'kg':kg_climate})
# season=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\JJA.csv')
# season=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\MAM.csv')
season=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\SepON.csv')

# print JJA.head,'\n',season.head,'\n',SON.head
# Aggregation Analysis
# print 'Spring'
siteID=season['\'sitename\'']
# Remove the string Quotation Mark of the site_name

for i in range(0,len(siteID)):
    siteID[i]= siteID[i][1:7]
print siteID

print kgDF['s_id'],siteID
pft=season['IGBP']
rsquare=season['\'rsquare\'']
alpha=season['\'alpha\'']
ta=season['\'ta\'']
precip=season['\'Pre\'']
Amax=season['\'a\'']
VPD=season['\'VPD\'']
Mean=pd.DataFrame({'siteID':siteID,'alpha':alpha,'veg':pft,'rsquare':rsquare,'Amax':Amax,'ta':ta,'precip':precip,'vpd':VPD})
# Join the Mean dataFrame to kg_climate
Mean=Mean[Mean['Amax']<80]
Mean=Mean[Mean['alpha']<0.1]

# pft=JJA['IGBP']
# rsquare=JJA['\'rsquare\'']
# alpha=JJA['\'alpha\'']
# Amax=JJA['\'a\'']
# SumMean=pd.DataFrame({'alpha':alpha,'veg':pft,'rsquare':rsquare,'Amax':Amax,'ta':ta,'precip':precip})
# SumMean=SumMean[SumMean['Amax']<80]
# SumMean=SumMean[SumMean['alpha']<0.1]


# pft=SON['IGBP']
# rsquare=SON['\'rsquare\'']
# alpha=SON['\'alpha\'']
# Amax=SON['\'a\'']
# FalMean=pd.DataFrame({'alpha':alpha,'veg':pft,'rsquare':rsquare,'Amax':Amax,'ta':ta,'precip':precip})
# # FalMean=FalMean[FalMean['Amax']<80]
# FalMean=FalMean[FalMean['alpha']<0.1]


# cnt=0
frame=[grouped['vpd'] for name,grouped in Mean.groupby('veg')]
veg_name=[name for name,grouped in Mean.groupby('veg')]
result=pd.concat(frame,axis=1,keys=veg_name)
mean=result.get(veg_name).mean()
# mean.to_csv('vpd_fal.csv',index=veg_name)



