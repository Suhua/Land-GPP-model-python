'''
This purpose of this code is to calculate gross primary production (GPP) by tower-LUE-GPP model from 2000-2005. GPP is calculated as GPP=alpha*fPAR*PAR; alpha is the specific light use efficiency at monthly step;PAR is partial
     active radiation ; fPAR is the fraction of partial active radiation 
'''

import numpy as np
from scipy.io import netcdf
import scipy.misc as sm
from scipy.ndimage import zoom
from scipy import io
import matplotlib.pylab as plt
import glob
from pyhdf import SD,HDF
from mpl_toolkits import basemap

class GPP:
    def fPAR(self,month,year):
        '''fPar is an unitless value ranging from 0 to 1, with monthly step and 0.5 x 0.5 spatial resolution'''
        hdf_files=glob.glob(r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\fPAR200{0}\*HDF'.format(year))
        cnt=0
        for fn in hdf_files:
            if fn.endswith('HDF'):
                cnt+=1
                if cnt==int(month)+1:
                    data=SD.SD(fn).select('fapar').get()
                    data=np.ma.masked_where(data==255,data)/255.0
                    return data

    def PAR(self,month,year):
        '''long_name: Monthly Mean of Net Shortwave Radiation Flux
        units: W/m^2; precision: 1'''
        f=netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\nswrs.sfc.mon.mean.nc','r')
        Var=f.variables['nswrs']
        sta=np.linspace(636,756,11)
        end=sta+12
        # Par is considered as 45% of the net shortwave radiation, divided by 11.58 to get MJ
        data=Var[int(sta[year]):int(end[year]),:,:]*0.45/11.58
        #  Resize the data into 0.5x0.5 degree ([360,720])
        sr=-zoom(data[month-1,:,:],[360/94.0,720/192.0],mode='nearest')
        # print np.max(sr),np.min(sr),np.max(data[mon,:,:]),np.min(data[mon,:,:])
        return sr

    def Alpha(self,month):
        '''
        the Alpha data is aggregated from tower level to biome level calcuated as an average
        '''
        files=glob.glob(r'G:\Research\modelling\model_development1\*npy')
        for f in files:
            if f.endswith('alpha_{0}.npy'.format(month+1)):
                alpha=np.load(f)
                alpha=np.ma.masked_where(alpha==0,alpha)
                return alpha

    # def veg_Lookup(self,vegValue,lc,map):
    #     lc=io.loadmat('G:\Research\Gridded Data\PDSI\lc.mat')['lc']
    #     map[lc!=vegValue]=np.nan
    #     sum=np.sum(np.sum(map))
    #     return sum


#--------------------------Main funtion starts here---------------------------------------------------------------------
GPP=GPP()
total_GPP=0
gpp_lue=np.ones([360,720,72],dtype=float)  # pre define an array to store results 
area_weight = io.loadmat(r'G:\Research\Gridded Data\NC\area_360x720.mat')  
area = area_weight['area_global']
for year in range(0,6):
    total_GPP=0
    for month in range(0,12):
        output=np.zeros([360,720])
        fpar=GPP.fPAR(month,year)
        # print fpar
        PAR=GPP.PAR(month,year)
        # print PAR
        alpha=GPP.Alpha(month)
        # print alpha
        output=alpha*fpar*PAR*30   # convert daily value to monthly value
        ind=year*12+month
        yr = year+2000;
        if len(str(month)<2):
            mo = ''.join([str(0),str(month)])
        else:
            mo = str(month)
        name=''.join([str(yr),mo])
        output.dump('towerLUEgpp{0}.npy'.format(name))
        
        

    # fig=plt.figure()
    # ax = fig.add_axes([0.05,0.05,0.9,0.9])
    # map=np.ma.fix_invalid(gpp_lue,copy=True,fill_value=0)
    # map=np.ma.masked_where(map==0,map)
    # plt.imshow(output)
    # plt.colorbar()
    # plt.show()
    # lats=np.linspace(90,-90,360)
    # lons=np.linspace(-180,180,720)
    # lons, lats = np.meshgrid(lons,lats)
    # m =basemap.Basemap(projection='robin',lon_0=0.0,resolution=None)
    # m.drawmapbourndary(fill_color='0.3')

    # im1= m.pcolormesh(lons,lats,map,shading='flat',cmap=plt.cm.jet,latlon=True)
    # m.drawparallels(np.arange(-90.,99.,30.))
    # m.drawmeridians(np.arange(-180.,180.,60.))
    # mstr=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # ax.set_title(''.join([mstr[month-1],' Mean GPP ']),fontsize=16)
    # cb = m.colorbar(im1,"bottom", size="5%", pad="2%",ax=[])
    # m.pcolor(im1, vmin=0, vmax=18)
    # plt.savefig(''.join(['Mean Global Gross Primary Production in ' , mstr[month-1],'.jpg']))


        # plt.imshow(output)
        # plt.colorbar()
