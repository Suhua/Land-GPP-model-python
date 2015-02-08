import pandas as pd
import numpy as np
import statsmodels.tsa.api as sa
import matplotlib.pylab as plt
import os


def load(path):
    data=pd.read_csv(path,index_col=0,header=0)
    return data


evi_path=r'G:\Research\modelling\model_development\data\evi_DBF_DF.csv'
par_path=r'G:\Research\modelling\model_development\data\PAR_DBF_DF.csv'
ta_path=r'G:\Research\modelling\model_development\data\ta_DBF_DF.csv'
spei_path=r'G:\Research\modelling\model_development\data\SPEI_DBF_DF.csv'
alpha_path=r'G:\Research\modelling\model_development\predicting_pp\pp1.csv'

evi=load(evi_path)
ta=load(ta_path)
spei=load(spei_path)
par=load(par_path)
info=load(alpha_path)
site_number=len(evi.columns)
os.chdir(r'G:\Research\modelling\model_development\data')

cnt=0
alpha=np.zeros([12,10])
for pft,group in info.groupby(['pft']):
    alpha[:,cnt]=np.mean(group.iloc[:,5:].as_matrix(),axis=0)
    cnt+=1
# print alpha
    # group.iloc[:,5:].boxplot()
    # plt.xlabel(pft)
    # plt.show()

x=np.zeros([12,5])
x[:,1]=np.mean(evi.iloc()[:12].as_matrix(),axis=1)
par=load(par_path)
x[:,2]=np.mean(par.iloc()[:12].as_matrix(),axis=1)
ta=load(ta_path)
x[:,3]=np.mean(ta.iloc()[:12].as_matrix(),axis=1)
x[:,4]=np.mean(spei.iloc()[:12].as_matrix(),axis=1)
x[:,0]=alpha[:,5]

model=sa.VAR(x)
results=model.fit(1)
print results.summary()
results.plot()
plt.show()
os.chdir(r'G:\Research\modelling\model_development\data\biomeRegression')
x=pd.DataFrame(x)
x.to_csv('dbf_reg.csv')
