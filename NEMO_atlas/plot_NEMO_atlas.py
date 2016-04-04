from climaf.api import *
from reference import *
from plot_params import *

StringFontHeight=0.019


def apply_scale_offset(dat,scale,offset):
    """
    Returns a CliMAF object after applying a scale and offset
    ! Shortcut to: ccdo(ccdo(dat,operator='mulc,'+str(float(scale))),operator='addc,'+str(float(offset)))
    """
    return ccdo(ccdo(dat,operator='mulc,'+str(float(scale))),operator='addc,'+str(float(offset)))
#



# -----------------------------------------------------------------------------------------------
# Basic functions
# -- S. Senesi & E. Sanchez
#######################
def model_vs_obs_profile_oce(variable,model,obs,masks='/data/esanchez/Atlas/oce/mask'):
    """
    Given two dataset specifications, and an oceanic variable name,
    create a figure for profile for the variable in both sources

    dataset specifications are dictionnaries

    specifics :
     - space averaging uses cdftools for model variable, on grid T
     - obs data are supposed to be an annual cycle

    Example :
    >>> model=dict(project="CMIP5", model='CNRM-CM5', frequency='mon',
    >>>       realm='ocean', table='Omon',
    >>>       experiment='historical', period='1980-1981')
    >>> obs=dict(project="ref_pcmdi", product='NODC-Levitus',clim_period='*')
    >>> fig=model_vs_obs_profile_oce('thetao',model,obs)

    """
    modvar=ds(variable=variable,**model)
    obsvar=ds(variable=variable,**obs)

    #- Compute temporal means
    tmean_modvar=ccdo(modvar,operator='timavg -yearmonmean')
    tmean_obsvar=ccdo(obsvar,operator='yearmonmean')

    #- Compute model profile using CdfTools (this requires some pre-processing)
    fixed_fields('ccdfmean_profile',
             ('mask.nc',    masks+'/ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',masks+'/ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',masks+'/ORCA1_mesh_zgr.nc'))
    cscript("rename_time","ncrename -d time,time_counter ${in} ${out}")
    aux=rename_time(tmean_modvar)
    vertprof_modvar=ccdfmean_profile(aux,pos_grid='T')

    # Obs profile is simpler to compute, thanks to a regular grid
    vertprof_obsvar=ccdo(tmean_obsvar,operator='mermean -zonmean')

    #- Plot vertical profile of model & obs data
    myplot=plot( vertprof_obsvar, vertprof_modvar, title='MOD&OBS - '+variable,
                 y="index",aux_options="xyLineColor='red'",invXY=False)

    return(myplot)



def plot_basin_moc(model, variable="msftmyz", basin=1):
    # Plot a model MOC slice
    moc_model=ds(variable=variable, **model)
    moc_model_mean=time_average(moc_model)
    # extraire le bassin de rang 'basin' (def: Atlantique=1)
    moc_model_mean_atl=slice(moc_model_mean, dim='x', num=basin)
    # masquer les valeurs
    moc_model_mean_atl_mask=mask(moc_model_mean_atl,miss=0.0)
    # Plot
    plot_moc_slice=plot(moc_model_mean_atl_mask, title="MOC", y="lin",
                        min=-10.,max=30.,delta=1.,scale=1e-3,units="Sv",options="trXMinF=-30.")
    return(plot_moc_slice)


# Profil de MOC, vs Obs RAPID
def moc_profile_vs_obs_rapid(model,variable="msftmyz",basin=1):
    """
    Model is a dict defining the model dataset (except variable)
    """
    # Comparer les profil de MOC modele/RAPID a la latitude 26
    mod=model.copy()
    mod.update({'variable': variable})
    moc_model=ds(**mod)
    moc_model_mean=time_average(moc_model)
    #extraire le bassin Atlantique de la MOC modele
    moc_model_mean_atl=slice(moc_model_mean, dim='x', num=basin)
    #masquer les valeurs et extraire la latitude 26
    moc_model_mean_atl_mask=mask(moc_model_mean_atl,miss=0.0)
    moc_model_26=slice(moc_model_mean_atl_mask, dim='lat', num=26.5)
    #
    moc_obs=ds(project="ref_climatos",variable='moc')
    moc_obs_mean=time_average(moc_obs)
    #
    plot_profile_obs=plot(moc_model_26,moc_obs_mean, title='RAPID',
                          y="lin", units="Sv", aux_options="xyLineColor='red'")
    return plot_profile_obs




# -----------------------------------------------------------------------
# -- J. Servonnat
# -- 2D Maps
def plot_climato_map(variable,dat,season,mpCenterLonF='200',customname='default'):
    # -- Get the dataset
    wdat = dat.copy()
    wdat.update(dict(variable=variable))
    print wdat
    ds_dat = ds(**wdat)
    print 'ds_dat',ds_dat
    # -- Compute the seasonal climatology
    climato_dat = regridn(clim_average(ds_dat,season),cdogrid="r360x180")
    #
    if 'clim_period' in dat:
        tmp_period = ds_dat.clim_period
    else:
        tmp_period = str(ds_dat.period)
    # -- Plot the field
    if customname not in 'default':
       title = customname
    else:
        if 'product' in dat:
           title = ds_dat.kvp['product']
        else:
           title = ds_dat.model+' '+ds_dat.simulation
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = season
    p = plot_params(variable,'full_field')
    #if mpCenterLonF:
    #    p.update(dict(mpCenterLonF=mpCenterLonF))
    print 'p = ',p
    myplot = plot(climato_dat,
                  title = title,
                  mpCenterLonF=200,
                  gsnStringFontHeightF = StringFontHeight,
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot


def plot_bias_map(variable,model,ref,season, add_product_in_title=True,mpCenterLonF=200, customname='default', **kwarsg):
    # -- Get the datasets of the model and the ref
    ds_model = ds(variable=variable, **model)
    ds_ref   = ds(**ref)
    # -- Compute the seasonal climatology
    climato_sim = regridn(clim_average(ds_model,season),cdogrid="r360x180")
    climato_ref = regridn(clim_average(ds_ref  ,season),cdogrid="r360x180")
    #
    # -- Compute the bias map
    bias = minus(climato_sim,climato_ref)
    #
    if 'clim_period' in ds_model.kvp:
        tmp_period = ds_model.kvp['clim_period']
    else:
        tmp_period = str(ds_model.period)
    # -- Plot the field
    if customname not in 'default':
       title = customname
    else:
        title = ds_model.model+' '+ds_model.simulation
    if add_product_in_title:
        title = title+' (vs '+ref["product"]+')'
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = season
    p = plot_params(variable,'bias')
    ref_aux_params = plot_params(variable,'full_field')
    p.update(dict(contours=ref_aux_params['colors']))
    if 'offset' in ref_aux_params:
        offset = ref_aux_params['offset']
    else:
        offset = 0.0
    if 'scale' in ref_aux_params:
        scale  = ref_aux_params['scale']
    else:
        scale = 1.0
    # -- We apply the scale and offset with apply_scale_offset()
    aux_ref = apply_scale_offset(climato_ref,scale,offset)

    #if mpCenterLonF:
    #    p.update(dict(mpCenterLonF=mpCenterLonF))
    myplot = plot(bias,aux_ref,
                  title = title,
                  mpCenterLonF=200,
                  gsnStringFontHeightF = StringFontHeight,
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot


# -- Sea Ice Plots

def plot_sea_ice_climato(variable,model,ref,season,pole, customname='default', add_product_in_title=True):
    # -- Get the datasets of the model and the ref
    wmodel = model.copy()
    wmodel.update(dict(table='OImon'))
    ds_model = ds(variable=variable, **wmodel)
    ds_ref   = ds(**ref)
    # -- Compute the seasonal climatology
    climato_sim = regridn(clim_average(ds_model,season),cdogrid='r360x180')
    climato_ref = clim_average(ds_ref  ,season)
    #
    if 'clim_period' in ds_model.kvp:
        tmp_period = ds_model.kvp['clim_period']
    else:
        tmp_period = str(ds_model.period)
    # -- Plot the field
    if customname not in 'default':
       title = customname
    else:
        title = ds_model.model+' '+ds_model.simulation
    if add_product_in_title:
        title = title+' (vs '+ref["product"]+')'
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = season
    p = plot_params(variable,'full_field')
    ref_aux_params = plot_params(variable,'full_field')
    p.update(dict(contours=15))
    # -- Manage the projection
    if pole=='Arctic':
       proj='NH'
    if pole=='Antarctic':
       proj='SH'
    #if mpCenterLonF:
    #    p.update(dict(mpCenterLonF=mpCenterLonF))
    myplot = plot(climato_sim,climato_ref,
                  title = title,
                  proj=proj,
                  gsnStringFontHeightF = StringFontHeight,
                  #options='gsnAddCyclic=True',
                  aux_options='cnLineThicknessF=10',
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot


def plot_sea_ice_bias(variable,model,ref,season,pole, customname='default', add_product_in_title=True):
    # -- Get the datasets of the model and the ref
    wmodel = model.copy()
    wmodel.update(dict(table='OImon'))
    ds_model = ds(variable=variable, **wmodel)
    ds_ref   = ds(**ref)
    # -- Compute the seasonal climatology
    climato_sim = regridn(clim_average(ds_model,season),cdogrid='r360x180')
    climato_ref = regridn(clim_average(ds_ref  ,season),cdogrid='r360x180')
    #
    # -- Compute the bias map
    bias = minus(climato_sim,climato_ref)
    #
    if 'clim_period' in ds_model.kvp:
        tmp_period = ds_model.kvp['clim_period']
    else:
        tmp_period = str(ds_model.period)
    # -- Plot the field
    if customname not in 'default':
       title = customname
    else:
        title = ds_model.model+' '+ds_model.simulation
    if add_product_in_title:
        title = title+' - '+ref["product"]
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = season
    p = plot_params(variable,'bias')
    ref_aux_params = plot_params(variable,'full_field')
    p.update(dict(contours=ref_aux_params['colors']))
    #if 'offset' in ref_aux_params:
    #    offset = ref_aux_params['offset']
    #else:
    #    offset = 0.0
    #if 'scale' in ref_aux_params:
    #    scale  = ref_aux_params['scale']
    #else:
    #    scale = 1.0
    # -- We apply the scale and offset with apply_scale_offset()
    #aux_ref = apply_scale_offset(climato_ref,scale,offset)
    #
    # -- Manage the projection
    if pole=='Arctic':
       proj='NH'
    if pole=='Antarctic':
       proj='SH'
    myplot = plot(bias,climato_ref,
                  title = title,
                  proj=proj,
                  #options='gsnAddCyclic=True',
                  gsnStringFontHeightF = StringFontHeight,
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot


# -- MLD Climatos

def plot_MLD_climato(variable,dat,diag='JFM', customname='default',region='NAtl'):
    # -- Get the datasets of the model and the ref
    dat.update(dict(variable=variable))
    ds_dat = ds(**dat)
    # -- Compute the seasonal climatology
    climato_diag = regridn(clim_average(ds_dat,diag),cdogrid='r360x180')
    #
    if 'clim_period' in ds_dat.kvp:
        tmp_period = ds_dat.kvp['clim_period']
    else:
        tmp_period = str(ds_dat.period)
    # -- Plot the field
    if 'product' in ds_dat.kvp:
        title = ds_dat.kvp['product']
    else:
        if customname not in 'default':
            title = customname
        else:
            title = ds_dat.model+' '+ds_dat.simulation
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = diag
    p = plot_params(variable,'full_field')
    # -- Manage the projection
    if region=='NAtl':
       NAtl = dict(lonmin=-80,lonmax=30,latmin=0,latmax=90)
       wclimato_diag = llbox(regridn(climato_diag,cdogrid='r360x180'),**NAtl)
    if region=='Austral':
       p.update(dict(proj='SH30'))
       wclimato_diag = climato_diag
    myplot = plot(wclimato_diag,
                  title = title,
                  #options='gsnAddCyclic=True',
                  gsnStringFontHeightF = StringFontHeight,
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot


def plot_MLD_bias(variable,model,ref,diag='JFM',region='NAtl', customname='default', add_product_in_title=True):
    # -- Get the datasets of the model and the ref
    model.update(dict(variable=variable))
    ds_model = ds(**model)
    ds_ref   = ds(**ref)
    # -- Compute the seasonal climatology
    ref_climato_diag   = clim_average(ds_ref,diag)
    model_climato_diag = regrid(clim_average(ds_model,diag),ref_climato_diag)
    bias = minus(model_climato_diag,ref_climato_diag)
    #
    #
    if 'clim_period' in ds_model.kvp:
        tmp_period = ds_model.kvp['clim_period']
    else:
        tmp_period = str(ds_model.period)
    # -- Plot the field
    if customname not in 'default':
        title = customname
    else:
        title = ds_model.model+' '+ds_model.simulation
    if add_product_in_title:
        title = title+' - '+ref["product"]
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = diag
    p = plot_params(variable,'bias')
    # -- Manage the projection
    if region=='NAtl':
       NAtl = dict(lonmin=-80,lonmax=30,latmin=0,latmax=90)
       wbias = llbox(bias,**NAtl)
    if region=='Austral':
       p.update(dict(proj='SH30'))
       wbias = bias
    myplot = plot(wbias,
                  title = title,
                  #options='gsnAddCyclic=True',
                  gsnStringFontHeightF = StringFontHeight,
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot



def plot_MLD_climato(variable,dat,diag='JFM',region='NAtl', customname='default'):
    # -- Get the datasets of the model and the ref
    dat.update(dict(variable=variable))
    ds_dat = ds(**dat)
    # -- Compute the seasonal climatology
    climato_diag = clim_average(ds_dat,diag)
    #
    if 'clim_period' in ds_dat.kvp:
        tmp_period = ds_dat.kvp['clim_period']
    else:
        tmp_period = str(ds_dat.period)
    # -- Plot the field
    if 'product' in ds_dat.kvp:
        title = ds_dat.kvp['product']
    else:
        if customname not in 'default':
            title = customname
        else:
            title = ds_dat.model+' '+ds_dat.simulation
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = diag
    p = plot_params(variable,'full_field')
    # -- Manage the projection
    if region=='NAtl':
       NAtl = dict(lonmin=-80,lonmax=30,latmin=0,latmax=90)
       wclimato_diag = llbox(regridn(climato_diag,cdogrid='r360x180'),**NAtl)
    if region=='Austral':
       p.update(dict(proj='SH30'))
       wclimato_diag = climato_diag
    myplot = plot(wclimato_diag,
                  title = title,
                  #options='gsnAddCyclic=True',
                  gsnStringFontHeightF = StringFontHeight,
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot


def plot_MLD_bias(variable,model,ref,diag='JFM',region='NAtl', customname='default', add_product_in_title=True):
    # -- Get the datasets of the model and the ref
    model.update(dict(variable=variable))
    ds_model = ds(**model)
    ds_ref   = ds(**ref)
    # -- Compute the seasonal climatology
    ref_climato_diag   = regridn(clim_average(ds_ref,diag),cdogrid='r360x180')
    model_climato_diag = regridn(clim_average(ds_model,diag),cdogrid='r360x180')
    bias = minus(model_climato_diag,ref_climato_diag)
    #
    #
    if 'clim_period' in ds_model.kvp:
        tmp_period = ds_model.kvp['clim_period']
    else:
        tmp_period = str(ds_model.period)
    # -- Plot the field
    if customname not in 'default':
        title = customname
    else:
        title = ds_model.model+' '+ds_model.simulation
    if add_product_in_title:
        title = title+' - '+ref["product"]
    #
    LeftString = tmp_period
    CenterString = variable
    RightString = diag
    p = plot_params(variable,'bias')
    # -- Manage the projection
    if region=='NAtl':
       NAtl = dict(lonmin=-80,lonmax=30,latmin=0,latmax=90)
       wbias = llbox(bias,**NAtl)
    if region=='Austral':
       p.update(dict(proj='SH30'))
       wbias = bias
    myplot = plot(wbias,
                  title = title,
                  #options='gsnAddCyclic=True',
                  gsnStringFontHeightF = StringFontHeight,
                  gsnRightString  = RightString,
                  gsnCenterString = CenterString,
                  gsnLeftString   = LeftString,
                  **p)
    return myplot




