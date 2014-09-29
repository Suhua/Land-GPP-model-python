__author__ = 'swei'

import os
import urllib
import datetime
import time
import glob
from dateutil import*

def file_date_name(year,month,day):
    if month<10:
       month='0'+str(month)
    if day<10:
       day='0'+str(day)
    return str(year)+'.'+str(month)+'.'+str(day)+str('/')
    
    
# print os.getcwd()

URL = 'http://e4ftl01.cr.usgs.gov/MOLT/MOD15A2.005/'

st=datetime.date(2003,1,01)  
for i in range(100): # Input the number of files to retrieve
    path_name= os.path.join(URL,file_date_name(st.year,st.month,st.day))
    print "the {0} th file".format(i)
    if (st.month==12 and st.day>23): # Change into next year
        st=datetime.date(st.year+1,1,01)
    else:
        # path_name= os.path.join(URL,file_date_name(st.year,st.month,st.day))
        st=st+datetime.timedelta(days=8) # Add 8-days increase to st
    response=urllib.urlopen(path_name)
    
    
    
    for line in response:
        temElement=line.split('\"')
        for name in temElement:
            if name[:20]>='MOD15A2.A2003001.h26' and name.endswith('hdf'):
                file_path=os.path.join(path_name,name)
                # urllib.urlretrieve(file_path,name)
                print file_path

