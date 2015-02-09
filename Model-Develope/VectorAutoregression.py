import pandas as pd
import numpy as np
import statsmodels.tsa.api as sa
import matplotlib.pylab as plt
import os


def load(path):
    data=pd.read_csv(path,index_col=0,header=0)
    return data

def fr_missing_value(df):
    df=df.replace(0,np.nan)
    df=df.dropna(axis=1)
    index_col=df.columns
    return df,index_col

def remove_missing_value(df,index_col):
    columns=df.columns.tolist()
    for site in columns:
        if site not in index_col:
            columns.remove(site)
    return df[columns]

def alpha_data():
    alpha=pd.read_csv(r'G:\Research\modelling\model_development\predicting_pp\pp1.csv',index_col=0,header=0)
    index_col=alpha['sitename'].tolist()
    columns=alpha.columns[5:]
    data=alpha.iloc[:,5:].as_matrix()
    data=np.transpose(data)
    data=pd.DataFrame(data,index=columns,columns=index_col)
    return data


evi_path=r'G:\Research\modelling\model_development\data\evi_DBF_DF.csv'
par_path=r'G:\Research\modelling\model_development\data\PAR_DBF_DF.csv'
ta_path=r'G:\Research\modelling\model_development\data\ta_DBF_DF.csv'
spei_path=r'G:\Research\modelling\model_development\data\SPEI_DBF_DF.csv'


spei=load(spei_path)
evi=load(evi_path)
ta=load(ta_path)
par=load(par_path)


# remove missing values
spei,col_spei=fr_missing_value(spei)
evi,col_evi=fr_missing_value(evi)

columns=[]
for s in col_evi.tolist():
    if s in col_spei.tolist():
        columns.append(s)


evi=remove_missing_value(evi,columns)
spei=remove_missing_value(spei,columns)
ta=remove_missing_value(ta,columns)
par=remove_missing_value(par,columns)


site_number=len(columns)
alpha=alpha_data()
pft_alpha=np.mean(alpha[columns].as_matrix(),axis=1)


# for site in alpha.index():
#     if site in col_evi


# print alpha
    # group.iloc[:,5:].boxplot()
    # plt.xlabel(pft)
    # plt.show()

x=np.zeros([12,4])
x[:,1]=np.mean(evi.iloc()[:12].as_matrix(),axis=1)
par=load(par_path)
# x[:,2]=np.mean(par.iloc()[:12].as_matrix(),axis=1)
ta=load(ta_path)
x[:,2]=np.mean(ta.iloc()[:12].as_matrix(),axis=1)
x[:,3]=np.mean(spei.iloc()[:12].as_matrix(),axis=1)
x[:,0]=pft_alpha


model=sa.VAR(x)
results=model.fit(1)
print results.summary()
results.plot()
plt.show()
os.chdir(r'G:\Research\modelling\model_development\data\biomeRegression')
x=pd.DataFrame(x)
x.to_csv('DBF_woPar.csv')
