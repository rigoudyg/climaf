#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies,
on Ciclad and at TGCC.

The project NEMO presents many possible keywords (facets) to determine precisely the dataset and render the data
location as efficient as possible.
We have chosen to provide 'wild cards' (*) to many keywords by default. This way, ds() has a greater chance to feed the
user back with a result (even if it contains too many simulations),
even if the user specifies just a few keywords.

Three projects are available to access the NEMO outputs; they are aimed at dealing with the diversity of variable names
seen among the IPSL outputs (that can vary with time and users).
They all provide aliases to the CMIP variables names and to the old names (taking advantage of the mechanisms linked
with calias).
- NEMO corresponds to the more up-to-date combination of variable names (mix of CMIP and old names)
- NEMO_old : links with the old variable names
- NEMO_CMIP : simply uses calias to provide the scale, offset and filenameVar


The attributes are:
  - root : path (without the login) to the top of the NEMO tree
  - login : login of the producer of the simulation
  - model : explicit
  - experiment : piControl, historical, amip...
  - status : DEVT, PROD, TEST
  - simulation : name of the numerical simulation (JobName in the IGCM syntax)
  - DIR : ATM, OCE, SRF...
  - OUT : Analyse, Output
  - frequency : monthly, daily, annual_cycle (equivalent to 'seasonal')
  - ave_length : MO, DA (optionnal, but can reduce the duration of the localization by ds() )
  - period : explicit
  - variable : explicit
  - clim_period : a character string; there is no mechanism of period selection (like with 'period')
  - clim_period_length : can be set to '_50Y' or '_100Y' to access the annual cycles averaged over 50yr long or 100yr
  long periods


Default values of the attributes:
  - root               : '/ccc/store/cont003/dsm' (at TGCC)
  - login              : '*'
  - model              : '*'
  - experiment         : '*'
  - status             : '*'
  - simulation         : '*'
  - DIR                : '*'
  - OUT                : '*'
  - frequency          : 'monthly'
  - ave_length         : '*'
  - period             : 'fx'
  - variable           : '*'
  - clim_period        : '????_????'
  - clim_period_length : '*'


Example 1:
- On Curie, access to a 'time series' dataset of the variable tas, providing values to all facets:

 >>> dat1 = ds(project='NEMO',
               root='/ccc/store/cont003/dsm',
               login ='p86mart',
               model='IPSLCM6',
               experiment='piControl',
               status='DEVT',
               simulation='O1T09V04',
               DIR='ATM',
               OUT='Analyse',
               frequency='monthly',
               ave_length='MO',
               period='1850-1900',
               variable='tas'
               )

Note that the following request returns the same files (but takes more time):
 >>> dat1 = ds(project='NEMO',
               model='IPSLCM6',
               simulation='O1T09V04',
               period='1850-1900',
               variable='tas'
               )


Example 2:
- On Curie, access to a 'SE_50Y' dataset of the variable tas, providing values to all facets;
Note that we set frequency to 'seasonal' (or 'annual_cycle'), specify clim_period and clim_period_length (to specify
either _50Y or _100Y)

 >>> dat2 = ds(project='NEMO',
               login ='p86mart',
               model='IPSLCM6',
               experiment='piControl',
               status='DEVT',
               simulation='O1T09V04',
               DIR='ATM',
               OUT='Analyse',
               frequency='seasonal',
               clim_period='1850_1899',
               clim_period_length='_50Y',
               variable='tas'
               )

The attributes 'model', 'simulation' and 'clim_period' can be used to define ensembles with eds().
Example 3:
- On Curie, define an ensemble with simulations 'O1T09V01','O1T09V02','O1T09V03':

 >>> dat_ens = eds(project='NEMO',
                   model='IPSLCM6',
                   simulation=['O1T09V01','O1T09V02','O1T09V03'],
                   clim_period='1850_1859',
                   variable='tas'
                   )



Contact: jerome.servonnat@lsce.ipsl.fr

"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip

root = None
if atTGCC:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/ccc/store/cont003/dsm"
if onCiclad:
    # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
    root = "/prodigfs/fabric"
if onSpip:
    # Declare a list of root directories for IPSL data at TGCC
    root = "/Users/marti/Volumes/CURIE/ccc/store/cont003/dsm"
    print 'igcm_out : declaration root sur Spip : ', root

if root:
    p = cproject("NEMO", "root", "login", "model", "config", "status", "experiment", "simulation", "DIR", "OUT",
                 "ave_length", "frequency", "period", "clim_period", "clim_period_length",
                 ensemble=["model", "simulation", "clim_period"], separator="%")

    cdef('root', root, project='NEMO')
    cdef('clim_period', '????_????', project='NEMO')
    cdef('clim_period_length', '*', project='NEMO')  # --> Takes the following values: '*', ''
    # (to access only to SE), '_50Y', '_100Y'
    cdef('ave_length', '*', project='NEMO')  # --> Takes the following values: MO, DA...
    cdef('model', 'NEMO_v6', project='NEMO')
    cdef('config', 'ORCA1_LIM3_PISCES', project='NEMO')
    cdef('status', '*', project='NEMO')  # --> PROD, DEVT, TEST
    cdef('simulation', '*', project='NEMO')
    cdef('variable', '*', project='NEMO')
    cdef('frequency', 'yearly', project='NEMO')
    cdef('experiment', 'ORCA1ia', project='NEMO')
    cdef('OUT', 'Output', project='NEMO')  # --> Output, Analyse
    cdef('DIR', '*', project='NEMO')  # --> ATM, OCE, SRF...
    cdef('login', '*', project='NEMO')
    cdef('period', 'fx', project='NEMO')

    # Frequency alias
    cfreqs('NEMO', {'monthly': '1M', 'daily': '1D', 'seasonal': 'SE', 'annual_cycle': 'SE', 'yearly': '1Y'})

    urls_NEMO = [
        "${root}/${model}/${config}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${ave_length}/"
        "${simulation}_${PERIOD}_${frequency}_${variable}.nc",
        "${root}/${model}/${config}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/"
        "${frequency}${clim_period_length}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
    ]

    # Next command will lead to explore all directories in 'urls_NEMO'
    # for searching data for a CliMAF dataset (by function ds) except if
    # a more specific dataloc entry matches the arguments to 'ds'
    dataloc(project="NEMO", organization="generic", url=urls_NEMO)

    # -- Note:
    # -- In the project NEMO, we have defined aliases for both the CMIP variable names (aliased to the old igcm names
    #    when necessary)
    # -- and the old IGCM names to take advantage of the mechanisms behind calias (scale, offset, filenameVar)

    # ---------------------------------------- #
    # -- Aliases to the CMIP variable names -- #

    # OCE
    calias("NEMO", 'tos', offset=273.15, filenameVar='grid_T')
    calias("NEMO", 'sos', filenameVar='grid_T')
    calias("NEMO", 'thetao', offset=273.15, filenameVar='grid_T')
    calias("NEMO", 'so', filenameVar='grid_T')
    calias("NEMO", 'zos', filenameVar='grid_T')
    calias("NEMO", 'mlotst', 'mldr10_3', filenameVar='grid_T')
    calias("NEMO", 'mlddt02', 'mld_dt02', filenameVar='grid_T')
    calias("NEMO", 'hc300', scale=1.E-9, filenameVar='grid_T')
    calias("NEMO", 'wfo', filenameVar='grid_T')

    # ICE
    calias("NEMO", 'sic', 'siconc', scale=100, filenameVar="icemod")
    calias("NEMO", 'sit', 'sithic', filenameVar="icemod")

    # ATM general variables
    calias("NEMO", 'pr', 'precip', filenameVar='histmth')
    calias("NEMO", 'prw', filenameVar='histmth')
    calias("NEMO", 'psl', 'slp', filenameVar='histmth')
    calias("NEMO", 'tas', 't2m', filenameVar='histmth')
    calias("NEMO", 'huss', 'q2m', filenameVar='histmth')
    calias("NEMO", 'uas', 'u10m', filenameVar='histmth')
    calias("NEMO", 'vas', 'v10m', filenameVar='histmth')
    calias("NEMO", 'sfcWind', 'wind10m', filenameVar='histmth')

    # -> Turbulent fluxes
    calias("NEMO", 'hfls', 'solahdoo', scale=-1, filenameVar='grid_T')
    calias("NEMO", 'hfss', 'sosehdoo', scale=-1, filenameVar='grid_T')
    calias("NEMO", 'tauu', 'tauuo', filenameVar='grid_U')
    calias("NEMO", 'tauv', 'tauvo', filenameVar='grid_V')

    # -> Biogeochemistry
    calias('NEMO', 'NO3', filenameVar='ptrc_T')
    calias('NEMO', 'PO4', filenameVar='ptrc_T')
    calias('NEMO', 'Si', filenameVar='ptrc_T')
    calias('NEMO', 'O2', filenameVar='ptrc_T')

    # ---------------------------------------------------------------------------------------------- #
    # --> Aliases to the zonal average (computed on the x axis of the ORCA grid)                  -- #

    calias('NEMO', 'zotemglo', offset=273.15, filenameVar='diaptr')
    calias('NEMO', 'zotempac', offset=273.15, filenameVar='diaptr')
    calias('NEMO', 'zotematl', offset=273.15, filenameVar='diaptr')
    calias('NEMO', 'zotemind', offset=273.15, filenameVar='diaptr')

    calias('NEMO', 'zosalglo', filenameVar='diaptr')
    calias('NEMO', 'zosalpac', filenameVar='diaptr')
    calias('NEMO', 'zosalatl', filenameVar='diaptr')
    calias('NEMO', 'zosalind', filenameVar='diaptr')

    calias('NEMO', 'zomsfglo', filenameVar='diaptr')
    calias('NEMO', 'zomsfpac', filenameVar='diaptr')
    calias('NEMO', 'zomsfatl', filenameVar='diaptr')
    calias('NEMO', 'zomsfind', filenameVar='diaptr')

    # ---------------------------------------------------------------------------------------------- #
    # --> Aliases to the old NEMO names (to take advantage of offset, scale and filenameVar)  -- #

    # OCE
    calias("NEMO", 'sosstsst', offset=273.15, filenameVar='grid_T')
    calias("NEMO", 'sosaline', filenameVar='grid_T')
    calias("NEMO", 'votemper', offset=273.15, filenameVar='grid_T')
    calias("NEMO", 'vosaline', filenameVar='grid_T')
    calias("NEMO", 'mldr10_3', filenameVar='grid_T')
    calias("NEMO", 'somx3010', filenameVar='grid_T')
    calias("NEMO", 'sohtc300', scale=1.E-9, filenameVar='grid_T')
    calias("NEMO", 'mld_dt02', filenameVar='grid_T')

    # ICE
    calias("NEMO", 'siconc', scale=100, filenameVar="icemod")
    calias("NEMO", 'sithic', filenameVar="icemod")
    calias("NEMO", 'sivolu', filenameVar="icemod")

    # ATM general variables
    calias("NEMO", 'precip', filenameVar='histmth')
    calias("NEMO", 'prw', filenameVar='histmth')
    calias("NEMO", 'slp', filenameVar='histmth')
    calias("NEMO", 't2m', filenameVar='histmth')
    calias("NEMO", 'q2m', filenameVar='histmth')
    calias("NEMO", 'u10m', filenameVar='histmth')
    calias("NEMO", 'v10m', filenameVar='histmth')
    calias("NEMO", 'wind10m', filenameVar='histmth')

    # -> Clouds
    calias("NEMO", 'cldt', scale=100, filenameVar='histmth')

    # -> Radiative down at TOA
    calias("NEMO", 'SWdnTOA', filenameVar='histmth')

    # -> Radiative down at TOA
    calias("NEMO", 'topl', filenameVar='histmth')
    calias("NEMO", 'SWupTOA', filenameVar='histmth')
    calias("NEMO", 'topl0', filenameVar='histmth')
    calias("NEMO", 'SWupTOAclr', filenameVar='histmth')

    # -> Radiative up at Surface
    calias("NEMO", 'LWupSFC', filenameVar='histmth')
    calias("NEMO", 'SWupSFC', filenameVar='histmth')
    calias("NEMO", 'SWupSFCclr', filenameVar='histmth')
    calias("NEMO", 'LWupSFCclr', filenameVar='histmth')

    # -> Radiative down at Surface
    calias("NEMO", 'LWdnSFC', filenameVar='histmth')
    calias("NEMO", 'SWdnSFC', filenameVar='histmth')
    calias("NEMO", 'LWdnSFCclr', filenameVar='histmth')
    calias("NEMO", 'SWdnSFCclr', filenameVar='histmth')
