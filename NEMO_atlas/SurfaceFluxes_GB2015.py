from climaf.api import *
from reference import *
from plot_params import *

def apply_scale_offset(dat,scale,offset):
    """
    Returns a CliMAF object after applying a scale and offset
    ! Shortcut to: ccdo(ccdo(dat,operator='mulc,'+str(float(scale))),operator='addc,'+str(float(offset)))
    """
    return ccdo(ccdo(dat,operator='mulc,'+str(float(scale))),operator='addc,'+str(float(offset)))
#



def get_product(file):
    dum = str.split(file,'/') ; filename = dum[len(dum)-1] ; dum2 = str.split(filename,'_')
    product = dum2[2]
    return product


#cscript('cdo_ensavg', 'cdo ensavg ${mmin} ${out}')
#cscript('cdo_ensmin', 'cdo ensmin ${mmin} ${out}')
#cscript('cdo_ensmax', 'cdo ensmax ${mmin} ${out}')

#cscript('cdo_gt','cdo gt ${in_1} ${in_2} ${out}')
#cscript('cdo_lt','cdo lt ${in_1} ${in_2} ${out}')


def stat_ref_ensemble_GB2015(var,climatology='annual_cycle',statistic='mean', region='Tropics'):
    """
    Returns a statistic on the ensemble of turbulent fluxes reference products defined in
    Gainusa-Bogdan et al. (2015)
    
    Default values are:
    - season = 'annual_cycle'
    - statistic = 'mean'
    
    For 'climatology', the user can choose among the values handled by clim_average (see help(clim_average))
    For 'statistic', the user can choose among 'mean' (uses 'avg' in cdo), 'min' and 'max'
    """
    #cscript('cdo_ensavg', 'cdo ensavg ${mmin} ${out}')
    #cscript('cdo_ensmin', 'cdo ensmin ${mmin} ${out}')
    #cscript('cdo_ensmax', 'cdo ensmax ${mmin} ${out}')
    
    #cscript('cdo_gt','cdo gt ${in_1} ${in_2} ${out}')
    #cscript('cdo_lt','cdo lt ${in_1} ${in_2} ${out}')

    # -- We get the list of files available in the ref_climatos project for variable var
    # -- From this list, we extract the names (ens_products) of the products to construct an ensemble with eds()
    listfiles = ds(project='ref_climatos', variable=var)
    files = set(str.split(listfiles.baseFiles(),' '))
    ens_products = []
    if region == 'Tropics':
        list_of_ref_files = ['OAFlux','NCEP','NCEP2','CORE2','FSU3','NOCS-v2','J-OFURO2','GSSTFM3','IFREMER',
                             'DFS4.3','TropFlux','DASILVA','HOAPS3','ERAInterim']
    else:
        list_of_ref_files = ['OAFlux','NCEP','NCEP2','CORE2','NOCS-v2','GSSTFM3','J-OFURO2','IFREMER',
                             'DFS4.3','DASILVA','HOAPS3','ERAInterim']
    for f in files:
        if get_product(f) in list_of_ref_files: 
            ens_products.append(get_product(f))
    print 'list_of_ref_files => ',list_of_ref_files
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
        return cdo_ensavg(rgrd_ens_clim)
    if statistic=='min':
        return cdo_ensmin(rgrd_ens_clim)
    if statistic=='max':
        return cdo_ensmax(rgrd_ens_clim)

def plot_bias_TurbFlux_vs_GB2015(dat,climatology='ANM', region = 'Tropics', customname='default', add_product_in_title=True, **kwargs):
    #cscript('cdo_ensavg', 'cdo ensavg ${mmin} ${out}')
    #cscript('cdo_ensmin', 'cdo ensmin ${mmin} ${out}')
    #cscript('cdo_ensmax', 'cdo ensmax ${mmin} ${out}')
    #
    #cscript('cdo_gt','cdo gt ${in_1} ${in_2} ${out}')
    #cscript('cdo_lt','cdo lt ${in_1} ${in_2} ${out}')
    #
    var = dat.variable
    period = dat.period
    # -- Reference mean
    ref_clim = stat_ref_ensemble_GB2015(var,climatology=climatology, region=region)
    #
    # -- Upper and lower ensemble boundary
    max_clim = stat_ref_ensemble_GB2015(var,statistic='max',climatology=climatology, region=region)
    min_clim = stat_ref_ensemble_GB2015(var,statistic='min',climatology=climatology, region=region)
    #
    sim_clim = regrid(clim_average(dat,climatology),ref_clim)
    #
    if 'offset' in kwargs:
        offset = kwargs['offset']
    else:
        offset = 0
    if 'scale' in kwargs:
        scale = kwargs['scale']
    else:
        scale = 1
    wsim_clim = apply_scale_offset(sim_clim,scale,offset)
    # -- Calcul du biais
    bias_clim = minus(wsim_clim,ref_clim)
    #
    test_sup = cdo_gt(wsim_clim,max_clim)
    test_inf = cdo_lt(wsim_clim,min_clim)
    test = plus(test_sup,test_inf)
    #
    # -- On fait un mask a partir de la moyenne d'ensemble des obs
    mask = div(ref_clim,ref_clim)
    #
    plot_specs = plot_params(var,'bias')
    #
    if customname not in 'default':
        title = customname
    else:
        title = dat.model+' '+dat.simulation
    if add_product_in_title:
        title = title+' (vs GB2015)'
    #
    if region=='Tropics':
        res   = llbox(mul(bias_clim,mask),lonmin=0,lonmax=360,latmin=-30,latmax=30)
        ptest = llbox(mul(test,mask),lonmin=0,lonmax=360,latmin=-30,latmax=30)
        plot_specs.update(dict(title=''))
    else:
        res   = mul(bias_clim,mask)
        ptest = mul(test,mask)
        plot_specs.update(dict(title=title))
    #
    options='pmLabelBarWidthF=0.065|pmLabelBarOrthogonalPosF=0.01|lbLabelFontHeightF=0.01|tmXBLabelFontHeightF=0.01|tmYLLabelFontHeightF=0.01'
    #
    plot_specs.update({'focus':'ocean','mpCenterLonF':200,
                       'tiMainFontHeightF':0.015,'shade_above':0.5,'aux_options':'cnLineThicknessF=3',
                       'contours':'0.5','shading_options':'gsnShadeHigh=17','options':options,
                       'gsnStringFontHeightF':0.018,
                       'gsnLeftString':period,'gsnRightString':climatology,'gsnCenterString':var})
    #
    return plot(res, ptest, **plot_specs)


def plot_climato_TurbFlux_GB2015(variable,dat,climatology='ANM', region='Tropics', customname='default', **kwargs):
    #cscript('cdo_ensavg', 'cdo ensavg ${mmin} ${out}')
    #
    var = variable
    # -- Compute the climatology
    if dat=='GB2015':
        period='1979-2005'
        dat_clim = stat_ref_ensemble_GB2015(var,climatology=climatology, region=region)
        title='GB2015 ensemble mean'
    else:
        period = dat.period
        dat_clim = clim_average(dat,climatology)
        if customname not in 'default':
            title = customname
        else:
            title = dat.model+' '+dat.simulation
    #
    if 'offset' in kwargs:
        offset = kwargs['offset']
    else:
        offset = 0
    if 'scale' in kwargs:
        scale = kwargs['scale']
    else:
        scale = 1
    wdat_clim = apply_scale_offset(dat_clim,scale,offset)
    #
    #
    if region=='Tropics':
        res   = llbox(dat_clim,lonmin=0,lonmax=360,latmin=-30,latmax=30)
        options='pmLabelBarWidthF=0.065|pmLabelBarOrthogonalPosF=0.01|lbLabelFontHeightF=0.01|tmXBLabelFontHeightF=0.01|tmYLLabelFontHeightF=0.01'
        common_plot_specs={'title':'','focus':'ocean','mpCenterLonF':200,
                       'tiMainFontHeightF':0.015,'shade_above':0.5,'aux_options':'cnLineThicknessF=3',
                       'contours':'0.5','shading_options':'gsnShadeHigh=17','options':options,
                       'gsnStringFontHeightF':0.018,
                       'gsnLeftString':period,'gsnRightString':climatology,'gsnCenterString':var}
    else:
        res   = dat_clim
        options='pmLabelBarWidthF=0.065|pmLabelBarOrthogonalPosF=0.01|lbLabelFontHeightF=0.01|tmXBLabelFontHeightF=0.01|tmYLLabelFontHeightF=0.01'
        common_plot_specs={'title':title,'focus':'ocean','mpCenterLonF':200,
                       'tiMainFontHeightF':0.015,'shade_above':0.5,'aux_options':'cnLineThicknessF=3',
                       'contours':'0.5','shading_options':'gsnShadeHigh=17','options':options,
                       'gsnStringFontHeightF':0.018,
                       'gsnLeftString':period,'gsnRightString':climatology,'gsnCenterString':var}
    #
    common_plot_specs.update(plot_params(var,'full_field'))
    #
    return plot(res, **common_plot_specs)


