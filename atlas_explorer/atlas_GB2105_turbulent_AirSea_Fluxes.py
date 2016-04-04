from climaf.api import *


def get_product(file):
    dum = str.split(file,'/') ; filename = dum[len(dum)-1] ; dum2 = str.split(filename,'_')
    product = dum2[2]
    return product


cscript('cdo_ensavg', 'cdo ensavg ${mmin} ${out}')
cscript('cdo_ensmin', 'cdo ensmin ${mmin} ${out}')
cscript('cdo_ensmax', 'cdo ensmax ${mmin} ${out}')

cscript('cdo_gt','cdo gt ${in_1} ${in_2} ${out}')
cscript('cdo_lt','cdo lt ${in_1} ${in_2} ${out}')


def stat_ref_ensemble_GB2015(var,climatology='annual_cycle',statistic='mean'):
    """
    Returns a statistic on the ensemble of turbulent fluxes reference products defined in
    Gainusa-Bogdan et al. (2015)
    
    Default values are:
    - season = 'annual_cycle'
    - statistic = 'mean'
    
    For 'climatology', the user can choose among the values handled by clim_average (see help(clim_average))
    For 'statistic', the user can choose among 'mean' (uses 'avg' in cdo), 'min' and 'max'
    """
    # -- We get the list of files available in the ref_climatos project for variable var
    # -- From this list, we extract the names (ens_products) of the products to construct an ensemble with eds()
    listfiles = ds(project='ref_climatos', variable=var)
    files = set(str.split(listfiles.baseFiles(),' '))
    ens_products = []
    for f in files:
        print get_product(f)
        if get_product(f) in ['NCEP2','OAFlux','CORE2','FSU3','NOCS-v2','J-OFURO2','GSSTFM3','IFREMER',
                              'DFS4.3','TropFlux']:
        #    ens_products.append(get_product(f))
            ens_products.append(get_product(f))
        #if get_product(f) in ['NCEP2','JRA25','CORE2','FSU3','NOCS-v2',
        #                      'J-OFURO2','IFREMER','GSSTFM3','HOAPS3','DFS4.3','TropFlux']:
        #    ens_products.append(get_product(f))
    print 'ens_products => ',ens_products
    #
    # -- Get the ensemble of products on project ref_climatos
    ens = eds(project='ref_climatos',product=ens_products, variable=var)
    #
    # -- Computes the climatologies on each ensemble member for the climatology specified by the user
    if climatology=='annual_cycle':
        ens_clim = ens
    else:
        ens_clim = clim_average(ens,climatology)
    #
    # -- Remapping all the datasets on a 360x180 grid
    rgrd_ens_clim = regridn(ens_clim,cdogrid='r360x180')
    #
    # -> Return the ensemble statistic
    if statistic=='mean':
        print 'statistic = ',statistic
        return cdo_ensavg(rgrd_ens_clim)
    if statistic=='min':
        print 'statistic = ',statistic
        return cdo_ensmin(rgrd_ens_clim)
    if statistic=='max':
        print 'statistic = ',statistic
        return cdo_ensmax(rgrd_ens_clim)
#

def plot_bias_TurbFlux_vs_GB2015(dat,climatology='ANM'):
    #
    var = dat.variable
    period = dat.period
    # -- Reference mean
    ref_clim = stat_ref_ensemble_GB2015(var,climatology=climatology)
    #
    # -- Upper and lower ensemble boundary
    max_clim = stat_ref_ensemble_GB2015(var,statistic='max',climatology=climatology)
    min_clim = stat_ref_ensemble_GB2015(var,statistic='min',climatology=climatology)
    #
    sim_clim = regrid(clim_average(dat,climatology),ref_clim)
    #
    # -- Calcul du biais
    bias_clim = minus(sim_clim,ref_clim)
    #
    test_sup = cdo_gt(sim_clim,max_clim)
    test_inf = cdo_lt(sim_clim,min_clim)
    test = plus(test_sup,test_inf)
    cfile(test)
    #
    # -- On fait un mask a partir de la moyenne d'ensemble des obs
    mask = divide(ref_clim,ref_clim)
    #
    res   = llbox(mul(bias_clim,mask),lonmin=0,lonmax=360,latmin=-30,latmax=30)
    ptest = llbox(mul(test,mask),lonmin=0,lonmax=360,latmin=-30,latmax=30)
    #
    return plot(res, ptest, title=dat.model+' '+dat.simulation,tiMainFontHeightF=0.015,
                shade_above=0.5,aux_options='cnLineThicknessF=3',contours='0.5',shading_options='gsnShadeHigh=17',
                colors='-50 -40 -35 -30 -25 -20 -15 -10 -5 5 10 15 20 25 30 35 40 50',color='hotcold_18lev',
                gsnLeftString=period,gsnRightString=climatology,gsnCenterString=var)
#
