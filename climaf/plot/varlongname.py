#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

import re

from env.environment import *


dict_std_name = dict(
    # -- ATMOSPHERE VARIABLES
    tas=("2M Temperature", "2M Temp."),
    pr=('Precipitation', 'Precip.'),
    psl=('Sea Level Pressure', 'Sea Level Pres.'),
    ua=('Zonal Wind', 'U-Wind'),
    va=('Meridional Wind', 'V-Wind'),
    uas=('Zonal Wind at 10m', 'U-Wind 10m'),
    vas=('Meridional Wind at 10m', 'V-Wind 10m'),
    ta=('Temperature', 'Air Temp.'),
    hur=('Relative Humidity', 'Rel. Humidity'),
    hus=('Specific Humidity', 'Sp. Humidity'),
    huss=('Specific Humidity at Surface', 'Sp. Humidity (surf)'),
    hurs=('Relative Humidity at Surface', 'Rel. Humidity (surf)'),
    rstt=('Rad SW Total TOA', 'Rad SW Total TOA'),
    rsts=('Total SW rad surface', 'Total SW rad surf.'),
    rtt=('Total Radiation TOA', 'Total Rad. TOA'),
    crelt=('Longwave Cloud Radiative Effect TOA', 'LW CRE TOA'),
    crest=('Shortwave Cloud Radiative Effect TOA', 'SW CRE TOA'),
    crett=('Total CRE TOA', 'Total CRE TOA'),
    hfls=('Latent Heat Flux', 'Latent HF'),
    hfss=('Sensible Heat Flux', 'Sensible HF'),
    hfns=('Surface Total Heat Flux', 'Surf. Tot. HF'),
    zg=('Geopotential Height', ''),
    rsut=('Upward SW rad TOA', ''),
    rlut=('Outgoing Long Wave Radiation', 'OLR'),
    rlutcs=('Clear Sky OLR', 'Clear Sky OLR'),
    albs=('Surface albedo', ''),
    albt=('Planetary albedo', ''),
    cress=('SW CRE surface', ''),
    crels=('LW CRE surface', ''),
    crets=('Total CRE surface', ''),
    rst=('Total radiation surface', ''),
    rah=('Atm. Rad. Heat.', ''),
    rahcs=('Atm. Rad. Heat. - clear sky', ''),
    rahcre=('Atm. rad. Heat. - CRE', ''),
    rsah=('Atm. SW Heat.', ''),
    rsahcs=('Atm. SW Heat. - Clear sky', ''),
    rsahcre=('Atm. SW Heat. - CRE', ''),
    rlah=('Atm. LW Heat.', ''),
    rlahcs=('Atm. LW Heat. - Clear sky', ''),
    rlahcre=('Atm. LW Heat. - CRE', ''),
    cltcalipso=('Total Cloud Cover', ''),
    cllcalipso=('cllcalipso', ''),
    clmcalipso=('Medium Cloud Cover', ''),
    clhcalipso=('High Cloud Cover', ''),
    rlds=('Downward LW rad at Surface', ''),
    rldscs=('Upward LW rad at Surface - Clear Sky', ''),
    rlus=('Upward SW rad at Surface', ''),
    rsdscs=('Downward SW rad at Surface - Clear Sky', ''),
    rsds=('Downward SW rad at Surface', ''),
    rsucs=('Upward SW rad at Surface - Clear Sky', ''),
    rsutcs=('Upward SW rad at TOA - Clear Sky', ''),
    pme=('P-E Precip-Evap(hfls/2.5e6) mm/day', ''),
    # -- OCEAN VARIABLES
    tos=('Sea Surface Temperature', ''),
    sos=('Sea Surface Salinity', ''),
    zos=('Sea Surface Height', ''),
    to200=('Potential Temperature at 200m', ''),
    to1000=('Potential Temperature at 1000m', ''),
    to2000=('Potential Temperature at 2000m', ''),
    so200=('Salinity at 200m', ''),
    so1000=('Salinity at 1000m', ''),
    so2000=('Salinity at 2000m', ''),
    mlotst=('MLD (SigmaT 0.03)', ''),
    wfo=('E-P Budget', ''),
    tauu=('Zonal Wind Stress', ''),
    tauv=('Meridional Wind Stress', ''),
    sic=('Sea Ice Concentration', ''),
    sit=('Sea Ice Thickness', ''),
    thetao=('Potential Temperature', ''),
    so=('Salinity', ''),
    moc=('Merid. Overturning Circulation', ''),
    # -- ORCHIDEE VARIABLES
    fluxlat=('Latent Heat Flux', ''),
    fluxsens=('Sensible Heat Flux', ''),
    albvis=('Albedo Visible', ''),
    albnir=('Albedo Near Infra Red', ''),
    tair=('Air Temperature', ''),
    swdown=('ShortWave Down', ''),
    lwdown=('LongWave Down', ''),
    evapnu=('Evaporation Bare soil', ''),
    evap=('Evaporation', ''),
    subli=('Sublimation', ''),
    Qs=('Runoff', ''),
    runoff=('Runoff', ''),
    drainage=('Drainage', ''),
    frac_snow=('Snow Cover', ''),
    total_soil_carb=('Total Soil Carbon Content', ''),
    snow=('Snow quantity - water equivalent', ''),
    O2_=('Oxygen', ''),
    Si_=('Silicate', ''),
    NO3_=('Nitrate', ''),
    PO4=('Phosphate', ''),
    # -- ORCHIDEE variables by PFT
    transpir=("Transpiration", ""),
    inter=("Interception (evaporation)", ""),
    gpp=('Global Primary Productivity', ''),
    GPP=('Global Primary Productivity', ''),
    lai=('Leaf Area Index', ''),
    maint_resp=('Maintenance Respiration', ''),
    growth_resp=('Growth Respiration', ''),
    hetero_resp=('Heterotrophic Respiration', ''),
    auto_resp=('Autotrophic Respiration', ''),
    nee=('Net Carbon Flux', ''),
    vegetfrac=('Vegetation Fraction', ''),
    maxvegetfrac=('Max Vegetation Fraction', '')
)


variable_regexp = re.compile(r"^(?P<var>([a-zA-Z]+|\w+_))(?P<nb>\d+)(?P<meter>m?)$")


def varlongname(variable):
    """
   Returns the long name of variable
   """
    if variable in dict_std_name:
        longvarname, shortvarname = dict_std_name[variable]
    else:
        match_regexp = variable_regexp.match(variable)
        if match_regexp is not None:
            var = match_regexp.groupdict()["var"]
            nb = match_regexp.groupdict()["nb"]
            meter = match_regexp.groupdict()["meter"] in ["m", ]
            longvarname, shortvarname = dict_std_name.get(var, ('', ''))
            if meter:
                suffix = "%dm" % nb
            else:
                suffix = "%dmb" % nb
            if longvarname in ["", ]:
                longvarname = variable
            else:
                longvarname += " at %s" % suffix
            if shortvarname not in ["", ]:
                shortvarname += " %s" % suffix
        else:
            longvarname = variable
            shortvarname = ""
    if "PFT" in variable:
        longvarname += " %s" % variable.replace(variable + "_", '')
    return longvarname
