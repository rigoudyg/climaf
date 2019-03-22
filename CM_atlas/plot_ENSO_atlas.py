from CM_atlas import *
from time_manager import *

ENSO_domain = [-30, 30, 120, 290]
# nino3 = [-5,5,210,270]
nino3 = "-5,5,210,270"
plot_domain = dict(lonmin=120, lonmax=290, latmin=-30, latmax=30)

curves_options = 'vpXF=0|' + \
                 'vpWidthF=0.66|' + \
                 'vpHeightF=0.43|' + \
                 'tmXBLabelFontHeightF=0.016|' + \
                 'tmYLLabelFontHeightF=0.014|' + \
                 'lgLabelFontHeightF=0.016|' + \
                 'tmXMajorGrid=True|' + \
                 'tmYMajorGrid=True|' + \
                 'tmXMajorGridLineDashPattern=2|' + \
                 'tmYMajorGridLineDashPattern=2|' + \
                 'xyLineThicknessF=6|' + \
                 'gsnStringFontHeightF=0.017'


def ENSO_ts_ssta(dat_dict, do_cfile=True, safe_mode=True, custom_plot_params={}, apply_period_manager=True):
    #
    # -- Add the variable and the domain
    # -- Apply the frequency and time manager (IGCM_OUT)
    wdat_dict = dat_dict.copy()
    wdat_dict.update(dict(variable='tos'))
    if apply_period_manager:
        frequency_manager_for_diag(wdat_dict, diag='TS')
        get_period_manager(wdat_dict)
    #
    dat = ds(**wdat_dict)
    # -- Compute the annual cycle
    scyc = annual_cycle(dat)
    #
    # -- Compute the SST anomalies (dat - annual cycle)
    ssta = minus(dat, scyc)
    #
    # -- Compute the average over the Nino3 area
    nino3 = dict(latmin=-5, latmax=5, lonmin=210, lonmax=270)
    ssta_nino3 = ccdo(space_average(llbox(ssta, **nino3)), operator='detrend')
    #
    # -- Get the period
    tmp_period = str.replace(str.replace(build_period_str(wdat_dict), '-', ''), '-', '')
    print "tmp_period = ", tmp_period
    #
    # -- Title
    title = build_plot_title(wdat_dict, None)
    #
    # -- Plot parameters
    curves_options = 'vpXF=0|' + \
                     'vpWidthF=0.66|' + \
                     'vpHeightF=0.43|' + \
                     'tmXBLabelFontHeightF=0.016|' + \
                     'tmYLLabelFontHeightF=0.014|' + \
                     'lgLabelFontHeightF=0.016|' + \
                     'tmXMajorGrid=True|' + \
                     'tmYMajorGrid=True|' + \
                     'tmXMajorGridLineDashPattern=2|' + \
                     'tmYMajorGridLineDashPattern=2|' + \
                     'xyLineThicknessF=8|' + \
                     'gsnYRefLine=0.0|' + \
                     'gsnStringFontHeightF=0.017'
    p = dict(options=curves_options + "|" + "tiMainFontHeightF=0.023|tiMainFont=helvetica-bold|"
                                            "gsnStringFontHeightF=0.019|gsnCenterString=SSTA Nino3|gsnLeftString="
                                            + tmp_period + "|gsnRightString=degC"
             )
    #
    # -- Update the custom plot params
    p.update(custom_plot_params)
    #
    # -- Plot
    plot_ts_ssta = curves(ssta_nino3, title=title, min=-4, max=4, **p)
    #
    return safe_mode_cfile_plot(plot_ts_ssta, do_cfile, safe_mode)
    #


def ENSO_std_ssta(dat_dict, do_cfile=True, safe_mode=True, custom_plot_params={}, apply_period_manager=True):
    #
    # -- Add the variable and the domain
    # -- Apply the frequency and time manager (IGCM_OUT)
    wdat_dict = dat_dict.copy()
    wdat_dict.update(dict(variable='tos'))
    if apply_period_manager:
        frequency_manager_for_diag(wdat_dict, diag='TS')
        get_period_manager(wdat_dict)
    #
    dat = ds(**wdat_dict)
    # -- Compute the annual cycle
    scyc = annual_cycle(dat)
    #
    # -- Compute the SST anomalies (dat - annual cycle)
    # ssta = llbox(regridn(ccdo(minus(dat,scyc),operator='detrend'),cdogrid='r180x90'),
    #              lonmin=120,lonmax=290,latmin=-30,latmax=30))
    std_ssta = llbox(regridn(ccdo(ccdo(minus(dat, scyc), operator='detrend'), operator='timstd'), cdogrid='r360x180'),
                     lonmin=120, lonmax=290, latmin=-30, latmax=30)

    #
    #
    # -- Get the period
    tmp_period = build_period_str(wdat_dict)
    #
    # -- Title
    title = build_plot_title(wdat_dict, None)
    #
    # -- Plot parameters
    p = dict(contours='0.4 0.6 0.8 1.0 1.2', colors='0.6 0.8 1.0 1.2',
             color='sunshine_9lev', focus='ocean',
             gsnLeftString='SST std.dev. (K)',
             gsnRightString=tmp_period,
             title=title
             )
    #
    # -- Update the custom plot params
    p.update(custom_plot_params)
    #
    # -- Plot
    # JS#plot_std_ssta   = plot(ccdo(ssta,operator='timstd'), **p)
    plot_std_ssta = plot(std_ssta, **p)
    #
    return safe_mode_cfile_plot(plot_std_ssta, do_cfile, safe_mode)


def ENSO_pr_clim(dat_dict, do_cfile=True, safe_mode=True, custom_plot_params={}, apply_period_manager=True):
    #
    # -- Add the variable and the domain
    wdat_dict = dat_dict.copy()
    if 'variable' not in wdat_dict:
        wdat_dict.update(dict(variable='pr'))
    # -- Apply the frequency and time manager (IGCM_OUT)
    wdat_dict = dat_dict.copy()
    wdat_dict.update(dict(variable='pr'))
    if apply_period_manager:
        frequency_manager_for_diag(wdat_dict, diag='SE')
        get_period_manager(wdat_dict)
    #
    dat = ds(domain=[-30, 30, 120, 290], **wdat_dict)
    # -- Compute the climatology
    pr_dat = clim_average(dat, 'ANM')
    #
    # -- Get the period
    tmp_period = build_period_str(wdat_dict)
    #
    # -- Title
    title = build_plot_title(dat_dict, None)
    #
    # -- Plot parameters
    pr_plot_params = dict(contours='2 4 6 8 10', colors='2 4 6 8', focus='ocean',
                          color='precip3_16lev', scale=86400.,
                          gsnLeftString='Annual mean (mm/day)',
                          gsnCenterString='Precip.',
                          gsnRightString=tmp_period,
                          title=title
                          )
    #
    # -- Update the custom plot params
    pr_plot_params.update(custom_plot_params)
    #
    # -- Plot
    plot_pr_clim = plot(pr_dat, **pr_plot_params)
    #
    return safe_mode_cfile_plot(plot_pr_clim, do_cfile, safe_mode)


def ENSO_tauu_clim(dat_dict, do_cfile=True, safe_mode=True, custom_plot_params={}, apply_period_manager=True):
    #
    # -- Add the variable and the domain
    wdat_dict = dat_dict.copy()
    if 'variable' not in wdat_dict:
        wdat_dict.update(dict(variable='tauu'))
    # -- Apply the frequency and time manager (IGCM_OUT)
    wdat_dict = dat_dict.copy()
    wdat_dict.update(dict(variable='tauu'))
    if apply_period_manager:
        frequency_manager_for_diag(wdat_dict, diag='SE')
        get_period_manager(wdat_dict)
    dat = ds(domain=[-30, 30, 120, 290], **wdat_dict)
    # -- Compute the climatology
    tauu_dat = clim_average(dat, 'ANM')
    #
    # -- Get the period
    tmp_period = build_period_str(wdat_dict)
    #
    # -- Title
    title = build_plot_title(dat_dict, None)
    #
    # -- Plot parameters
    tauu_plot_params = dict(min=-0.1, max=0.1, delta=0.01, focus='ocean',
                            color='NCV_jaisnd', contours=1,
                            gsnLeftString='Annual mean (N/m)',
                            gsnCenterString='Zonal Wind Stress',
                            gsnRightString=tmp_period,
                            title=title
                            )
    #
    # -- Update the custom plot params
    tauu_plot_params.update(custom_plot_params)
    #
    # -- Plot
    plot_tauu_clim = plot(tauu_dat, **tauu_plot_params)
    #
    return safe_mode_cfile_plot(plot_tauu_clim, do_cfile, safe_mode)


def ENSO_linreg_tauuA_on_SSTANino3(tauu_dat_dict, tos_dat_dict, do_cfile=True, safe_mode=True, custom_plot_params={},
                                   apply_period_manager=True):
    # -- Tau U anomalies model
    # -- Apply the frequency and time manager (IGCM_OUT)
    wtauu_dat_dict = tauu_dat_dict.copy()
    if apply_period_manager:
        frequency_manager_for_diag(wtauu_dat_dict, diag='TS')
        get_period_manager(wtauu_dat_dict)
    #
    # -- SSTA Nino3
    # -- Apply the frequency and time manager (IGCM_OUT)
    wtos_dat_dict = tos_dat_dict.copy()
    if apply_period_manager:
        frequency_manager_for_diag(wtos_dat_dict, diag='TS')
        get_period_manager(wtos_dat_dict)
    #
    # -- Find a common period to tos and rsds
    tauu_period = wtauu_dat_dict['period']
    tos_period = wtos_dat_dict['period']
    print 'tauu_period ', tauu_period
    print 'tos_period ', tos_period
    tauu_tos_common_period = find_common_period(tauu_period, tos_period)
    wtauu_dat_dict.update(dict(period=tauu_tos_common_period))
    wtos_dat_dict.update(dict(period=tauu_tos_common_period))
    #
    # -- SSTA Nino3
    print 'nino3 = ', nino3
    print 'wtauu_dat_dict = ', wtauu_dat_dict
    print 'wtos_dat_dict = ', wtos_dat_dict
    SST_nino3 = space_average(ds(domain=nino3, **wtos_dat_dict))
    scyc_SST_nino3 = annual_cycle(SST_nino3)
    SSTA_nino3 = minus(SST_nino3, scyc_SST_nino3)

    # -- Get Tau U anomalies model
    tauu_dat = ds(**wtauu_dat_dict)
    scyc_tauu = annual_cycle(tauu_dat)
    tauua = llbox(regridn(ccdo(minus(tauu_dat, scyc_tauu), operator='detrend'),
                          cdogrid='r180x90'), **plot_domain)

    # -- Linear regression = tauu anomalies / SSTA Nino3
    tauua_on_SSTA_nino3 = cLinearRegression(SSTA_nino3, tauua)
    #
    # -- Get the period
    tmp_period = build_period_str(wtauu_dat_dict)
    #
    # -- Title
    title = build_plot_title(wtauu_dat_dict, None)
    #
    # -- Plot parameters
    tauua_on_SSTA_nino3_params = dict(scale=1000., colors='-15 -12.5 -10 -7.5 -5 -2.5 0 2.5 5 7.5 10 12.5 15',
                                      contours=1, color='ViBlGrWhYeOrRe', focus='ocean',
                                      gsnLeftString='d(tauuA)/d(sstaNino3)',
                                      gsnCenterString='',
                                      gsnRightString=tmp_period,
                                      title=title
                                      )
    #
    # -- Update the custom plot params
    tauua_on_SSTA_nino3_params.update(custom_plot_params)

    plot_tauua_on_SSTA_nino3 = plot(tauua_on_SSTA_nino3, **tauua_on_SSTA_nino3_params)

    return safe_mode_cfile_plot(plot_tauua_on_SSTA_nino3, do_cfile, safe_mode)


def find_common_period(period1, period2):
    '''Returns the period covered both by period1 and period2'''
    if str(period1) == 'fx' or str(period2) == 'fx':
        print '--'
        print 'Warning in find_common_period => cant work on fx period'
        print '--'
        common_period = 'fx'
    else:
        sep_period1 = ('-' if '-' in period1 else '_')
        start_period1 = int(str.split(period1, sep_period1)[0][0:4])
        end_period1 = int(str.split(period1, sep_period1)[1][0:4])
        #
        sep_period2 = ('-' if '-' in period2 else '_')
        start_period2 = int(str.split(period2, sep_period2)[0][0:4])
        end_period2 = int(str.split(period2, sep_period2)[1][0:4])
        #
        start = str(sorted([start_period1, start_period2], reverse=True)[0])
        end = str(sorted([end_period1, end_period2])[0])
        #
        common_period = start + '-' + end
    #
    return common_period


def ENSO_linreg_rsds_on_SSTANino3(rsds_dat_dict, tos_dat_dict, do_cfile=True, safe_mode=True, custom_plot_params={},
                                  apply_period_manager=True):
    #
    # -- Short Wave
    # -- Apply the frequency and time manager (IGCM_OUT)
    wrsds_dat_dict = rsds_dat_dict.copy()
    if apply_period_manager:
        frequency_manager_for_diag(wrsds_dat_dict, diag='TS')
        get_period_manager(wrsds_dat_dict)
    #
    # -- SSTA Nino3
    # -- Apply the frequency and time manager (IGCM_OUT)
    wtos_dat_dict = tos_dat_dict.copy()
    if apply_period_manager:
        frequency_manager_for_diag(wtos_dat_dict, diag='TS')
        get_period_manager(wtos_dat_dict)
    #
    # -- Find a common period to tos and rsds
    rsds_period = wrsds_dat_dict['period']
    tos_period = wtos_dat_dict['period']
    print 'rsds_period ', rsds_period
    print 'tos_period ', tos_period
    rsds_tos_common_period = find_common_period(rsds_period, tos_period)
    wrsds_dat_dict.update(dict(period=rsds_tos_common_period))
    wtos_dat_dict.update(dict(period=rsds_tos_common_period))
    #
    # -- Get SW data
    rsds_dat = llbox(regridn(ds(**wrsds_dat_dict), cdogrid='r180x90'), **plot_domain)
    # -- Get SST Nino3 data
    SST_nino3 = space_average(ds(domain=nino3, **wtos_dat_dict))
    scyc_SST_nino3 = annual_cycle(SST_nino3)
    SSTA_nino3 = minus(SST_nino3, scyc_SST_nino3)

    # -- Linear regression = rsds / SSTA Nino3
    rsds_on_SSTA_nino3 = cLinearRegression(SSTA_nino3, rsds_dat)
    #
    # -- Get the period
    tmp_period = build_period_str(wrsds_dat_dict)
    #
    # -- Title
    title = build_plot_title(wrsds_dat_dict, None)
    #
    # -- Plot parameters
    rsds_on_SSTA_nino3_params = dict(colors='-20 -17.5 -15 -12.5 -10 -7.5 -5 -2.5 0 2.5 5 7.5 10 12.5 15 17.5 20',
                                     contours=1, color='ViBlGrWhYeOrRe', focus='ocean',
                                     gsnLeftString='d(rsds)/d(sstaNino3)',
                                     gsnCenterString='',
                                     gsnRightString=tmp_period,
                                     title=title
                                     )
    #
    # -- Update the custom plot params
    rsds_on_SSTA_nino3_params.update(custom_plot_params)

    plot_rsds_on_SSTA_nino3 = plot(rsds_on_SSTA_nino3, **rsds_on_SSTA_nino3_params)

    return safe_mode_cfile_plot(plot_rsds_on_SSTA_nino3, do_cfile, safe_mode)


def plot_ENSO_annual_cycles(models, ref='default', do_cfile=True, safe_mode=True, apply_period_manager=True):
    # -- Nino3 Box
    nino3 = [-5, 5, 210, 270]
    names_in_plot = []
    # -- Start the ensemble dictionary
    scyc_SST_ens_dict = dict()
    scyc_SSTA_ens_dict = dict()
    scyc_STD_ens_dict = dict()
    # -- Process the reference
    # -> Identify which reference is requested: 'default' or a dictionary
    if ref == 'default':
        ref_dict = dict(variable='tos', domain=nino3, project='ref_ts',
                        product='HadISST', period='2001-2010')
    else:
        ref_dict = ref.copy()
        ref_dict.update(dict(domain=nino3))
    #
    # -- Reference
    SST_nino3_ref = fsub(space_average(ds(**ref_dict)), 273.15)
    # -> Annual cycle SST
    scyc_SST_nino3_ref = annual_cycle(SST_nino3_ref)
    # -> Annual cycle SSTA
    SSTA_nino3_ref = minus(SST_nino3_ref, scyc_SST_nino3_ref)
    scyc_SSTA_nino3_ref = ccdo(scyc_SST_nino3_ref, operator='subc,' +
                                                            str(cMA(time_average(scyc_SST_nino3_ref))[0][0][0]))
    # -> Annual cycle monthly standard deviation
    STDscyc_SSTA_nino3_ref = ccdo(SSTA_nino3_ref, operator='ymonstd')
    # -- Store the results in the dictionaries
    if safe_mode:
        try:
            cfile(scyc_SST_nino3_ref)
            scyc_SST_ens_dict.update(dict(REF=scyc_SST_nino3_ref))
            scyc_SSTA_ens_dict.update(dict(REF=scyc_SSTA_nino3_ref))
            scyc_STD_ens_dict.update(dict(REF=STDscyc_SSTA_nino3_ref))
            names_in_plot.append('REF')
        except:
            print 'No data to compute the SST annual cycles for reference ', ref
    else:
        scyc_SST_ens_dict.update(dict(REF=scyc_SST_nino3_ref))
        scyc_SSTA_ens_dict.update(dict(REF=scyc_SSTA_nino3_ref))
        scyc_STD_ens_dict.update(dict(REF=STDscyc_SSTA_nino3_ref))
        names_in_plot.append('REF')
    #
    # -- Loop on the models
    for model in models:
        wmodel = model.copy()
        wmodel.update(dict(variable='tos'))
        if apply_period_manager:
            frequency_manager_for_diag(wmodel, 'TS')
            get_period_manager(wmodel)
        # -- Get the name that will be used in the plot
        if 'customname' in wmodel:
            name_in_plot = wmodel['customname']
        else:
            name_in_plot = build_plot_title(wmodel, None)
            # if wmodel['project']=='CMIP5':
            #   name_in_plot = wmodel['model']
            # else:
            #   name_in_plot = wmodel['simulation']
        SST_nino3 = space_average(ccdo(ds(domain=nino3, **wmodel), operator='subc,273.15'))
        scyc_SST_nino3 = annual_cycle(SST_nino3)
        SSTA_nino3 = minus(SST_nino3, scyc_SST_nino3)
        if safe_mode:
            try:
                print 'time_average(scyc_SST_nino3) ', time_average(scyc_SST_nino3)
                print 'cMA(time_average(scyc_SST_nino3)) = ', cMA(time_average(scyc_SST_nino3))
                scyc_SSTA_nino3 = ccdo(scyc_SST_nino3,
                                       operator='subc,' + str(cMA(time_average(scyc_SST_nino3))[0][0][0]))
                STDscyc_SSTA_nino3 = ccdo(SSTA_nino3, operator='ymonstd')
                cfile(scyc_SST_nino3)
                scyc_SST_ens_dict.update({name_in_plot: scyc_SST_nino3})
                scyc_SSTA_ens_dict.update({name_in_plot: scyc_SSTA_nino3})
                scyc_STD_ens_dict.update({name_in_plot: STDscyc_SSTA_nino3})
                names_in_plot.append(name_in_plot)
            except:
                print 'No data to compute the SST annual cycles for model ', model
        else:
            scyc_SSTA_nino3 = ccdo(scyc_SST_nino3, operator='subc,' + str(cMA(time_average(scyc_SST_nino3))[0][0][0]))
            STDscyc_SSTA_nino3 = ccdo(SSTA_nino3, operator='ymonstd')
            scyc_SST_ens_dict.update({name_in_plot: scyc_SST_nino3})
            scyc_SSTA_ens_dict.update({name_in_plot: scyc_SSTA_nino3})
            scyc_STD_ens_dict.update({name_in_plot: STDscyc_SSTA_nino3})
            names_in_plot.append(name_in_plot)

    #
    # -- Build the CliMAF ensembles
    scyc_SST_ens = cens(scyc_SST_ens_dict)
    scyc_SSTA_ens = cens(scyc_SSTA_ens_dict)
    scyc_STD_ens = cens(scyc_STD_ens_dict)
    #
    print 'names_in_plot = ', names_in_plot
    print 'scyc_SST_ens.keys() = ', scyc_SST_ens.keys()
    # -- Set the order
    scyc_SST_ens.set_order(names_in_plot)
    scyc_SSTA_ens.set_order(names_in_plot)
    scyc_STD_ens.set_order(names_in_plot)
    #
    # -- Plot options
    plot_options = 'vpXF=0|' + \
                   'vpWidthF=0.33|' + \
                   'vpHeightF=0.66|' + \
                   'tmXBLabelFontHeightF=0.012|' + \
                   'tmYLLabelFontHeightF=0.014|' + \
                   'lgLabelFontHeightF=0.016|' + \
                   'tmXMajorGrid=True|' + \
                   'tmYMajorGrid=True|' + \
                   'tmXMajorGridLineDashPattern=2|' + \
                   'tmYMajorGridLineDashPattern=2|' + \
                   'xyLineThicknessF=10|' + \
                   'gsnYRefLineThicknessF=3|' + \
                   'pmLegendHeightF=0.4|' + \
                   'pmLegendWidthF=0.12|' + \
                   'pmLegendSide=Bottom|' + \
                   'lgLabelFontHeightF=0.014|' + \
                   'gsnYRefLine=0.0|' + \
                   'gsnStringFontHeightF=0.017'
    # 'pmLegendOrthogonalPosF=-0.14|'+\
    # 'pmLegendParallelPosF=0|'+\
    # 'gsnMaximize=False|'+\
    #
    # -- Do the plots
    plot_scyc_SST = curves(scyc_SST_ens, title='SST Nino3',
                           X_axis='aligned', options=plot_options, min=23, max=29, lgcols=2)
    plot_scyc_SSTA = curves(scyc_SSTA_ens, title='SSTA Nino3',
                            X_axis='aligned', options=plot_options, min=-2, max=2, lgcols=2)
    plot_STDscyc_SSTA = curves(scyc_STD_ens, title='STD SSTA Nino3',
                               X_axis='aligned', options=plot_options, min=0, max=2, lgcols=2)
    #
    # -- Build the multiplot
    # cdrop(plot_scyc_SST)
    # cdrop(plot_scyc_SSTA)
    # cdrop(plot_STDscyc_SSTA)
    multiplot_annual_cycles = cpage(fig_lines=[[plot_scyc_SST, plot_scyc_SSTA, plot_STDscyc_SSTA]],
                                    page_trim=True, fig_trim=True)
    #
    cdrop(multiplot_annual_cycles)
    return safe_mode_cfile_plot(multiplot_annual_cycles, do_cfile, safe_mode)


def plot_ZonalWindStress_long_profile(models, ref='default', safe_mode=True, do_cfile=True, apply_period_manager=True):
    # -- Create a dictionary that will receive the meridional averages
    ens_dict = dict()
    # -- Process the reference
    # -> Identify which reference is requested: 'default' or a dictionary
    if ref == 'default':
        ref_dict = variable2reference('tauu')
    else:
        ref_dict = ref.copy()
    # -- Compute the climatology
    taux_ref = clim_average(ds(domain=[-5, 5, 120, 290], **ref_dict), 'ANM')
    # -- Compute the meridional mean
    mermean_taux_ref = ccdo(taux_ref, operator='mermean')
    # -- Update the dictionary ens_dict
    ens_dict.update(dict(REF=mermean_taux_ref))
    #
    names_in_plot = []
    for model in models:
        wmodel = model.copy()
        # -- Compute the climatology
        # -- Apply the frequency and time manager (IGCM_OUT)
        wmodel.update(dict(variable='tauu'))
        if apply_period_manager:
            frequency_manager_for_diag(wmodel, diag='SE')
            get_period_manager(wmodel)
        print 'ENSO wmodel = ', wmodel
        taux_model = regrid(clim_average(ds(domain=[-5, 5, 120, 290], **wmodel), 'ANM'), taux_ref)
        # -- Compute the meridional mean
        mermean_taux_model = ccdo(taux_model, operator='mermean')
        # -- Update the dictionary ens_dict
        if safe_mode:
            try:
                cfile(mermean_taux_model)
                if 'customname' in wmodel:
                    name_in_plot = wmodel['customname']
                else:
                    name_in_plot = build_plot_title(wmodel, None)
                    # if wmodel['project']=='CMIP5':
                    #   name_in_plot = wmodel['model']
                    # else:
                    #   name_in_plot = wmodel['simulation']
                names_in_plot.append(name_in_plot)
                ens_dict.update({name_in_plot: mermean_taux_model})
            except:
                print 'No data to compute the Zonal Wind Stress Equatorial prodile for ', wmodel
        else:
            cfile(mermean_taux_model)
            if 'customname' in wmodel:
                name_in_plot = wmodel['customname']
            else:
                name_in_plot = build_plot_title(wmodel, None)
                # if wmodel['project']=='CMIP5':
                #   name_in_plot = wmodel['model']
                # else:
                #   name_in_plot = wmodel['simulation']
            names_in_plot.append(name_in_plot)
            ens_dict.update({name_in_plot: mermean_taux_model})

    #
    # -- Build the ensemble
    mermean_ens = cens(ens_dict)
    #
    plot_options = 'vpXF=0|' + \
                   'vpWidthF=0.55|' + \
                   'vpHeightF=0.35|' + \
                   'tmXBLabelFontHeightF=0.016|' + \
                   'tmYLLabelFontHeightF=0.014|' + \
                   'lgLabelFontHeightF=0.012|' + \
                   'tmXMajorGrid=True|' + \
                   'tmYMajorGrid=True|' + \
                   'tmXMajorGridLineDashPattern=2|' + \
                   'tmYMajorGridLineDashPattern=2|' + \
                   'xyLineThicknessF=12|' + \
                   'gsnYRefLineThicknessF=3|' + \
                   'gsnYRefLine=0.0|' + \
                   'gsnStringFontHeightF=0.017'
    # 'pmLegendHeightF=0.4|'+\
    # 'pmLegendHeightF=0.4|'+\

    # -- Set the order
    mermean_ens.set_order(['REF'] + names_in_plot)
    #
    # -- Plot
    plot_tauu_profile = curves(mermean_ens, title='Zonal Wind Stress (-5/5N) Climato ANM',
                               X_axis='aligned', lgcols=2, options=plot_options, min=-0.1, max=0.07)
    return safe_mode_cfile_plot(plot_tauu_profile, do_cfile, safe_mode)
