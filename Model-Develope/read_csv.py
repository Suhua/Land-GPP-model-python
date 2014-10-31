__author__ = 'swei'
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# MAM=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\JJA.csv')
# MAM=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\MAM.csv')
MAM=pd.read_csv(r'G:\Research\fluxdata\Flux Data\flux_PP\PP\SepON.csv')

# print JJA.head,'\n',MAM.head,'\n',SON.head
# Aggregation Analysis
# print 'Spring'
pft=MAM['IGBP']
rsquare=MAM['\'rsquare\'']
alpha=MAM['\'alpha\'']
ta=MAM['\'ta\'']
precip=MAM['\'Pre\'']
Amax=MAM['\'a\'']
VPD=MAM['\'VPD\'']
SprMean=pd.DataFrame({'alpha':alpha,'veg':pft,'rsquare':rsquare,'Amax':Amax,'ta':ta,'precip':precip,'vpd':VPD})
SprMean=SprMean[SprMean['Amax']<80]
SprMean=SprMean[SprMean['alpha']<0.1]

#
# pft=JJA['IGBP']
# rsquare=JJA['\'rsquare\'']
# alpha=JJA['\'alpha\'']
# Amax=JJA['\'a\'']
# SumMean=pd.DataFrame({'alpha':alpha,'veg':pft,'rsquare':rsquare,'Amax':Amax,'ta':ta,'precip':precip})
# SumMean=SumMean[SumMean['Amax']<80]
# SumMean=SumMean[SumMean['alpha']<0.1]
#
#
# pft=SON['IGBP']
# rsquare=SON['\'rsquare\'']
# alpha=SON['\'alpha\'']
# Amax=SON['\'a\'']
# FalMean=pd.DataFrame({'alpha':alpha,'veg':pft,'rsquare':rsquare,'Amax':Amax,'ta':ta,'precip':precip})
# # FalMean=FalMean[FalMean['Amax']<80]
# FalMean=FalMean[FalMean['alpha']<0.1]


# cnt=0
frame=[grouped['vpd'] for name,grouped in SprMean.groupby('veg')]
veg_name=[name for name,grouped in SprMean.groupby('veg')]
Spr_result=pd.concat(frame,axis=1,keys=veg_name)
Spr_mean=Spr_result.get(veg_name).mean()
Spr_mean.to_csv('vpd_fal.csv',index=veg_name)

# frame=[grouped['precip'] for name,grouped in SumMean.groupby('veg')]
# veg_name=[name for name,grouped in SprMean.groupby('veg')]
# Sum_result=pd.concat(frame,axis=1,keys=veg_name)
#
# frame=[grouped['precip'] for name,grouped in FalMean.groupby('veg')]
# veg_name=[name for name,grouped in SprMean.groupby('veg')]
# Fall_result=pd.concat(frame,axis=1,keys=veg_name)

# result=pd.concat([Spr_result,Sum_result,Fall_result],axis=1,keys=['spr','sum','fal'])
# result=result.icol(veg_name)
# print result
# result.mean().plot(kind='bar',color='orange')
# plt.title('Mean Temperature of Biome',fontsize=22)
# plt.ylabel('Temperature(o^C)',fontsize=20)
# plt.show()

  # print 'd{0}'.format(cnt)
      # cnt+=1
# plt.subplot(4,3,cnt)
# grouped.boxplot(column='')
# plt.ylabel(name)


# print plotFrame,cnt
# plotFrame.boxplot()
# plt.show()

# vegName=[]
# alpha=SprMean['\'alpha\'','\'rsquare\'']
# alpha.boxplot()
# plt.show()

# for pft,grouped in SprMean:
#     vegName.append(pft)
#     alpha=grouped['\'alpha\'']
# print type(alpha)

# print 'Summer'
# SumMean=JJA.groupby('IGBP')
# for pft,grouped in SumMean:
#     print pft, grouped['\'alpha\''].mean()

# print 'Fall'
# FalMean=SON.groupby('IGBP')
# for pft,grouped in FalMean:
#     print pft, grouped['\'alpha\''].mean()
# # Plot data
# plt.subplot(3,1,1)
