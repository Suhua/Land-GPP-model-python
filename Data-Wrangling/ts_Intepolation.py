__author__ = 'swei'
''' Interpolate time series LAI  missing values (255) '''
import os
import numpy as np
import pandas as pd
import datetime
import matplotlib.pylab as plt
from scipy import interpolate


#Set work directory
os.chdir(r'G:/Vegetation Index/LAI and FPAR/Monthly 2004to2005')


#Set up data
dat=np.load('LAI.npy')
# print type(dat)
# print dat.shape
f=pd.read_csv('G:/Flux Data/flux_PP/siteInfo.csv')
# print f.head
site_name=f['sitename']
# pft=f['IGBP']
#Get time stamp
def monthly_time_stamp(sta_year,sta_month,sta_day,delta_month,period):
    time_stamp=[]
    year=sta_year
    month=sta_month
    day=sta_day
    period=period
    for i in range(0,period):
        if month>1 and (month%12)==1:
           year+=1
           month=delta_month
        stamp=datetime.date(year,month,day)
        # print time_stamp
        time_stamp.append(stamp)
        month+=delta_month
    return time_stamp

time_stamp=monthly_time_stamp(2003,1,1,1,dat.shape[0])
# for item in time_stamp:
#     print item

df=pd.DataFrame(dat,index=time_stamp,columns=site_name) #group by sitename/plant function types
# print dir(df)
# df.replace(255,df.replace([255],[np.nan]))
df[df==255]=np.nan
# print df[site_name[45]]
print type(df)
df.interpolate(method='spline',order=2)

#plot data
df[site_name[45]].plot()
plt.show()
