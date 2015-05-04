__author__ = 'swei'
import numpy as np
import pandas as pd
from scipy import io
import csv
import os
import glob

os.chdir(r'G:\Research\fluxdata\Flux Data')
files = glob.glob('*.csv')
# print len(files)
# enumerate the sitename
def get_df_Index(df):
    keys = ['DoY','GPP_f']
    return df[keys]

def monthlyMean(df):
    output=np.zeros(12,dtype=float)
    i=0
    for month in range (0,12):
        monSta = month * 30*48
        monEnd = (month+1)*30*48
        gpp = df.ix[monSta:monEnd,:]
        output [i] = np.mean(gpp['GPP_f'].as_matrix())
        i+=1
    return output

gpp_f = {}
for fn in files:
    key = ''.join([fn.split('.')[0],'.', fn.split('.')[1]])
    f = pd.read_csv(fn, header=0, index_col=None)
    df = get_df_Index(f)
    gpp_f[key] = monthlyMean(df)

df = pd.DataFrame.from_dict(gpp_f,orient='columns')
df.to_csv('gpp.monthly.csv')
