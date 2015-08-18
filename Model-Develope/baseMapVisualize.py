__author__ = 'Suhua'
import numpy as np
import matplotlib.pylab as plt
import glob
from scipy import io
from mpl_toolkits import basemap

def pft():
    lc = io.loadmat('E:\Research\Gridded Data\PDSI\lc.mat')['lc']
    return lc

fs=glob.glob(r'E:\Research\modelling\machine learning\alpha\*npy')
lc=pft()
# plt.imshow(lc)
# plt.sho/w
def mov_avergage(a,b,c):
    mov_ave=(a+b+c)/3.0
    return mov_ave


for i in range(0,12):
    im=np.load(fs[i])
    if i>1 and i<11:

        im_pre=np.load(fs[i-1])
        im_next=np.load(fs[i+1])
    if i==0:
        im_pre=np.load(fs[11])
        im_next=np.load(fs[1])
    if i==11:
        im_pre=np.load(fs[10])
        im_next=np.load(fs[0])
        for lat in range(0,360):
            for lon in range(0,720):
                if lc[lat,lon]==16:
                    im[lat,lon]=0
                else:
                    im[lat,lon]=mov_avergage(im_next[lat,lon],im_pre[lat,lon],im[lat,lon])



    im=np.ma.masked_where(im==0,im)
    fig=plt.figure()
    ax=fig.add_axes([0.05,0.05,0.9,0.9])
    lats=np.linspace(90,-90,360)
    lons=np.linspace(-180,180,720)
    m=basemap.Basemap(projection='robin',lon_0=0.0,resolution='c')
    m.drawparallels(np.arange(-90,90,30))
    m.drawmeridians(np.arange(-180,180,60))
    m.drawcoastlines()
    lons,lats=np.meshgrid(lons,lats)
    im=m.pcolormesh(lons,lats,im,cmap=plt.cm.jet,latlon=True)
    mon=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    cb=m.colorbar(im,'bottom',size='5%')
    cb.set_clim(vmin=0,vmax=0.1)
    if i>0:
        ax.set_title('{0} LUE Map'.format(mon[i-1]),fontsize=16)
        plt.savefig('LUE Map_1_{0}.jpg'.format(i))
    if i==0:
       ax.set_title('{0} LUE Map'.format(mon[11]),fontsize=16)
       plt.savefig('Map_1_{0}.jpg'.format(12))
