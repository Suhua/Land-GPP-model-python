class GPP:
    '''GPP (Gross Primary Production) is calculated as GPP=alpha*fPAR*PAR; alpha is the specific light use efficiency at monthly step;PAR is partial
     active radiation ; fPAR is the fraction of partial active radiation '''
    def fPAR(self, month, year):
        '''fPar is an unitless value ranging from 0 to 1, with monthly step and 0.5 x 0.5 spatial resolution'''
        hdf_files = glob.glob(r'G:\Research\Gridded Data\Vegetation Index\LAI and FPAR\fPAR200{0}\*.HDF'.format(year))
        cnt = 0
        for fn in hdf_files:
            if  fn.endswith('HDF'):
                 # print fn
                 cnt += 1
                 if cnt == month+1:
                    data = SD.SD(fn).select('fapar').get()
                    data = np.ma.masked_where(data == 255, data) / 255.0
                    # plt.imshow(data)
                    # plt.show()
                    return data

    def PAR(self,month,year):
        '''long_name: Monthly Mean of Net Shortwave Radiation Flux
        units: W/m^2; precision: 1'''
        f=netcdf.netcdf_file(r'G:\Research\Gridded Data\NC\NC_data\nswrs.sfc.mon.mean.nc','r')
        Var=f.variables['nswrs']
        sta=np.linspace(624,744,10)
        end=sta+12
        # Par is considered as 45% of the net shortwave radiation, divided by 11.58 to get MJ
        data=Var[int(sta[year]):int(end[year]),:,:]*0.45/11.58
        # print np.shape(data)
        #  Resize the data into 0.5x0.5 degree ([360,720])
        sr=np.abs(zoom(data[month,:,:],[360/94.0,720/192.0],mode='nearest'))
        # plt.imshow(sr)
        # plt.colorbar()
        # plt.show()
        # print np.max(sr),np.min(sr),np.max(data[mon,:,:]),np.min(data[mon,:,:])
        return sr

    def pft(self):
        lc = io.loadmat('G:\Research\Gridded Data\PDSI\lc.mat')['lc']
        return lc

    def Alpha(self,year,month):
        files=glob.glob(r'G:\Research\modelling\machine learning\alpha\alpha\*.npy')
        filenum=year*12+month
        print files[filenum%12]
        alpha=np.load(files[filenum%12])
        return alpha

#--------------------------Main function starts here---------------------------------------------------------------------
GPP=GPP()
total_GPP=0
gpp_half_lue=np.zeros((360,720,6*12),dtype=float)
for year in range(0,6):
    for month in range(0,12):
        print month
        fpar=GPP.fPAR(month,year)
        PAR=GPP.PAR(month,year)
        alpha=GPP.Alpha(year,month)
        # print alpha
        output=alpha*fpar*PAR
        # plt.imshow(output)
        # plt.colorbar()
        # plt.show()

        ind=year*12+month
        output.dump(r'G:\Research\modelling\model_development1\RFR-LUE-GPP\RFRlueGPP{0}.npy'.format(ind))
        gpp_half_lue[:,:,ind]=output
#
#     # ten_year_std=np.std(ten_year_mean,axis=2)
        area_weight=io.loadmat(r'G:\Research\Gridded Data\NC\area_360x720.mat')
        area=area_weight['area_global']


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
        output=output*area/1000000000000000
        total_GPP=total_GPP+np.sum(np.sum(output))*30

    print total_GPP
    total_GPP=0
