#!/usr/bin/env python
# -*- coding: utf-8 -*-


def varlongname(variable):
    """
   Returns the long name of variable
   """
    longvarname = variable
    # -- ATMOSPHERE VARIABLES
    if variable == 'tas':
        longvarname = '2M Temperature'
        shortvarname = '2M Temp.'
    if variable == 'pr':
        longvarname = 'Precipitation'
        shortvarname = 'Precip.'
    if variable == 'psl':
        longvarname = 'Sea Level Pressure'
        shortvarname = 'Sea Level Pres.'
    if variable == 'ua':
        longvarname = 'Zonal Wind'
        shortvarname = 'U-Wind'
    if variable == 'va':
        longvarname = 'Meridional Wind'
        shortvarname = 'V-Wind'
    if variable == 'uas':
        longvarname = 'Zonal Wind at 10m'
        shortvarname = 'U-Wind 10m'
    if variable == 'vas':
        longvarname = 'Meridional Wind at 10m'
        shortvarname = 'U-Wind 10m'
    if variable == 'ta':
        longvarname = 'Air Temperature'
        shortvarname = 'Air Temp.'
    if variable == 'hur':
        longvarname = 'Relative Humidity'
        shortvarname = 'Rel. Humidity'
    if variable == 'hus':
        longvarname = 'Specific Humidity'
        shortvarname = 'Sp. Humidity'
    if variable == 'huss':
        longvarname = 'Specific Humidity at Surface'
        shortvarname = 'Sp. Humidity (surf)'
    if variable == 'hurs':
        longvarname = 'Relative Humidity at Surface'
        shortvarname = 'Rel. Humidity (surf)'
    if variable == 'rstt':
        longvarname = 'Rad SW Total TOA'
        shortvarname = 'Rad SW Total TOA'
    if variable == 'rsts':
        longvarname = 'Total SW rad surface'
        shortvarname = 'Total SW rad surf.'
    if variable == 'rtt':
        longvarname = 'Total Radiation TOA'
        shortvarname = 'Total Rad. TOA'
    if variable == 'crelt':
        longvarname = 'Longwave Cloud Radiative Effect TOA'
        shortvarname = 'LW CRE TOA'
    if variable == 'crest':
        longvarname = 'Shortwave Cloud Radiative Effect TOA'
        shortvarname = 'SW CRE TOA'
    if variable == 'crett':
        longvarname = 'Total CRE TOA'
        shortvarname = 'Total CRE TOA'
    if variable == 'hfls':
        longvarname = 'Latent Heat Flux'
        shortvarname = 'Latent HF'
    if variable == 'hfss':
        longvarname = 'Sensible Heat Flux'
        shortvarname = 'Sensible HF'
    if variable == 'hfns':
        longvarname = 'Surface Total Heat Flux'
        shortvarname = 'Surf. Tot. HF'
    if variable == 'zg500':
        longvarname = '500mb geopotential height'
        shortvarname = ''
    if variable == 'rsut':
        longvarname = 'Upward SW rad TOA'
        shortvarname = ''
    if variable == 'rlut':
        longvarname = 'Outgoing Long Wave Radiation'
        shortvarname = 'OLR'
    if variable == 'rlutcs':
        longvarname = 'Clear Sky OLR'
        shortvarname = 'Clear sky OLR'
    if variable == 'albs':
        longvarname = 'Surface albedo'
        shortvarname = ''
    if variable == 'albt':
        longvarname = 'Planetary albedo'
        shortvarname = ''
    if variable == 'cress':
        longvarname = 'SW CRE surface'
        shortvarname = ''
    if variable == 'crels':
        longvarname = 'LW CRE surface'
        shortvarname = ''
    if variable == 'crets':
        longvarname = 'Total CRE surface'
        shortvarname = ''
    if variable == 'rts':
        longvarname = 'Total radiation surface'
        shortvarname = ''
    if variable == 'rah':
        longvarname = 'Atm. Rad. Heat.'
        shortvarname = ''
    if variable == 'rahcs':
        longvarname = 'Atm. Rad. Heat. - clear sky'
        shortvarname = ''
    if variable == 'rahcre':
        longvarname = 'Atm. rad. Heat. - CRE'
        shortvarname = ''
    if variable == 'rsah':
        longvarname = 'Atm. SW Heat.'
        shortvarname = ''
    if variable == 'rsahcs':
        longvarname = 'Atm. SW Heat. - Clear sky'
        shortvarname = ''
    if variable == 'rsahcre':
        longvarname = 'Atm. SW Heat. - CRE'
        shortvarname = ''
    if variable == 'rlah':
        longvarname = 'Atm. LW Heat.'
        shortvarname = ''
    if variable == 'rlahcs':
        longvarname = 'Atm. LW Heat. - Clear sky'
        shortvarname = ''
    if variable == 'rlahcre':
        longvarname = 'Atm. LW Heat. - CRE'
        shortvarname = ''
    if variable == 'cltcalipso':
        longvarname = 'Total Cloud Cover'
        shortvarname = ''
    if variable == 'cllcalipso':
        longvarname = 'Low Cloud Cover'
        shortvarname = ''
    if variable == 'clmcalipso':
        longvarname = 'Medium Cloud Cover'
        shortvarname = ''
    if variable == 'clhcalipso':
        longvarname = 'High Cloud Cover'
        shortvarname = ''
    if variable == 'rlds':
        longvarname = 'Downward LW rad at Surface'
        shortvarname = ''
    if variable == 'rldscs':
        longvarname = 'Upward LW rad at Surface - Clear Sky'
        shortvarname = ''
    if variable == 'hurs':
        longvarname = 'Relative Humidity at Surface'
        shortvarname = ''
    if variable == 'rlus':
        longvarname = 'Upward SW rad at Surface'
        shortvarname = ''
    if variable == 'rsdscs':
        longvarname = 'Downward SW rad at Surface - Clear Sky'
        shortvarname = ''
    if variable == 'rsds':
        longvarname = 'Downward SW rad at Surface'
        shortvarname = ''
    if variable == 'rsucs':
        longvarname = 'Upward SW rad at Surface - Clear Sky'
        shortvarname = ''
    if variable == 'rsutcs':
        longvarname = 'Upward SW rad at TOA - Clear Sky'
        shortvarname = ''
    if variable == 'pme':
        longvarname = 'P-E Precip-Evap(hfls/2.5e6) mm/day'
        shortvarname = ''
    #
    # -- OCEAN VARIABLES
    if variable == 'tos':
        longvarname = 'Sea Surface Temperature'
    if variable == 'sos':
        longvarname = 'Sea Surface Salinity'
    if variable == 'zos':
        longvarname = 'Sea Surface Height'
    if variable == 'to200':
        longvarname = 'Potential Temperature at 200m'
    if variable == 'to1000':
        longvarname = 'Potential Temperature at 1000m'
    if variable == 'to2000':
        longvarname = 'Potential Temperature at 2000m'
    if variable == 'so200':
        longvarname = 'Salinity at 200m'
    if variable == 'so1000':
        longvarname = 'Salinity at 1000m'
    if variable == 'so2000':
        longvarname = 'Salinity at 2000m'
    if variable == 'mlotst':
        longvarname = 'MLD (SigmaT 0.03)'
    if variable == 'wfo':
        longvarname = 'E-P Budget'
    if variable == 'tauu':
        longvarname = 'Zonal Wind Stress'
    if variable == 'tauv':
        longvarname = 'Meridional Wind Stress'
    if variable == 'hfls':
        longvarname = 'Latent Heat Flux'
    if variable == 'hfss':
        longvarname = 'Sensible Heat Flux'
    if variable == 'sic':
        longvarname = 'Sea Ice Concentration'
    if variable == 'sit':
        longvarname = 'Sea Ice Thickness'
    if variable == 'thetao':
        longvarname = 'Potential Temperature'
    if variable == 'so':
        longvarname = 'Salinity'
    if variable.lower() == 'moc':
        longvarname = 'Merid. Overturning Circulation'
    # -- ORCHIDEE VARIABLES
    if variable == 'fluxlat':
        longvarname = 'Latent Heat Flux'
    if variable == 'fluxsens':
        longvarname = 'Sensible Heat Flux'
    if variable == 'albvis':
        longvarname = 'Albedo Visible'
    if variable == 'albnir':
        longvarname = 'Albedo Near Infra Red'
    if variable == 'tair':
        longvarname = 'Air Temperature'
    if variable == 'swdown':
        longvarname = 'ShortWave Down'
    if variable == 'lwdown':
        longvarname = 'LongWave Down'
    if variable == 'evapnu':
        longvarname = 'Evaporation Bare soil'
    if variable == 'evap':
        longvarname = 'Evaporation'
    if variable == 'subli':
        longvarname = 'Sublimation'
    if variable == 'Qs':
        longvarname = 'Runoff'
    if variable == 'runoff':
        longvarname = 'Runoff'
    if variable == 'drainage':
        longvarname = 'Drainage'
    if variable == 'frac_snow':
        longvarname = 'Snow Cover'
    if variable == 'total_soil_carb':
        longvarname = 'Total Soil Carbon Content'
    if variable == 'snow':
        longvarname = 'Snow quantity - water equivalent'
    # -- ORCHIDEE variables by PFT
    # -- transpir
    shortvar = 'transpir'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Transpiration ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Transpiration'
    # -- inter
    shortvar = 'inter'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Interception (evaporation) ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Interception (evaporation)'
    # -- gpp
    shortvar = 'gpp'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Global Primary Productivity ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Global Primary Productivity'
    # -- GPP
    shortvar = 'GPP'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Global Primary Productivity ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Global Primary Productivity'
    # -- lai
    shortvar = 'lai'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Leaf Area Index ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Leaf Area Index'
    # -- maint_resp
    shortvar = 'maint_resp'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Maintenance Respiration ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Maintenance Respiration'
    # -- growth_resp
    shortvar = 'growth_resp'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Growth Respiration ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Growth Respiration'
    # -- hetero_resp
    shortvar = 'hetero_resp'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Heterotrophic Respiration ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Heterotrophic Respiration'
    # -- auto_resp
    shortvar = 'auto_resp'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Autotrophic Respiration ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Autotrophic Respiration'
    # -- nee
    shortvar = 'nee'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Net Carbon Flux ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Net Carbon Flux'
    # -- vegetfrac
    shortvar = 'vegetfrac'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Vegetation Fraction ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Vegetation Fraction'
    # -- maxvegetfrac
    shortvar = 'maxvegetfrac'
    if shortvar in variable:
        if 'PFT' in variable:
            longvarname = 'Max Vegetation Fraction ' + str.replace(variable, shortvar + '_', '')
        else:
            longvarname = 'Max Vegetation Fraction'
    #
    # -- Zonal wind on the column
    if 'ua' in variable:
        tmpvar = str.replace(variable, 'ua', '')
        if tmpvar in ['850', '700', '500', '200']:
            longvarname = 'Zonal Wind at ' + tmpvar + 'mb'
    #
    # -- Meridional wind on the column
    if 'va' in variable:
        tmpvar = str.replace(variable, 'va', '')
        if tmpvar in ['850', '700', '500', '200']:
            longvarname = 'Meridional Wind at ' + tmpvar + 'mb'
    #
    # -- Meridional wind on the column
    if 'ta' in variable:
        tmpvar = str.replace(variable, 'ta', '')
        if tmpvar in ['850', '700', '500', '200']:
            longvarname = 'Temperature at ' + tmpvar + 'mb'
    #
    # -- Geopotential height
    if 'zg' in variable:
        tmpvar = str.replace(variable, 'zg', '')
        if tmpvar in ['850', '700', '500', '200']:
            longvarname = 'Geopotential Height at ' + tmpvar + 'mb'
    #
    # -- O2
    if 'O2_' in variable:
        tmpvar = str.replace(variable, 'O2_', '')
        if tmpvar in ['surf', '300m', '1000m', '2500m']:
            longvarname = 'Oxygen at ' + tmpvar
    #
    # -- Si
    if 'Si_' in variable:
        tmpvar = str.replace(variable, 'Si_', '')
        if tmpvar in ['surf', '300m', '1000m', '2500m']:
            longvarname = 'Silicate at ' + tmpvar
    #
    # -- NO3
    if 'NO3_' in variable:
        tmpvar = str.replace(variable, 'NO3_', '')
        if tmpvar in ['surf', '300m', '1000m', '2500m']:
            longvarname = 'Nitrate at ' + tmpvar
    #
    # -- NO3
    if 'PO4_' in variable:
        tmpvar = str.replace(variable, 'PO4_', '')
        if tmpvar in ['surf', '300m', '1000m', '2500m']:
            longvarname = 'Phosphate at ' + tmpvar
    #
    #
    return longvarname
