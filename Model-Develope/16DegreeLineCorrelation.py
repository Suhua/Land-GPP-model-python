
import numpy as np
import matplotlib.pylab as plt

Precip=[0.07,0.35,0.46]
Ta=[-0.05,0.42,0.13]

width=0.3
ind=np.arange(3)
fig,ax = plt.subplots()
taControlled=ax.bar(0.15+ind,Precip,width,alpha=0.6,color='b',label='Partial correlation between GPP and Precipitation')
PreControlled=ax.bar(0.15+ind+width,Ta,width,alpha=0.6,color='r',label='Partial correlation between GPP and Temperature')


# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, '%d' % int(height),
#                 ha='center', va='bottom')

plt.ylabel('Correlation Coefficients',fontsize=20)
plt.xticks(0.15+ind+width,('Below 16 degree area','Boundary area','Above 16 degree area'),fontsize=20)
plt.yticks(fontsize=20)
# autolabel(taControlled)
# autolabel(PreControlled)
plt.legend(loc=2,fontsize = 18)
plt.show()
