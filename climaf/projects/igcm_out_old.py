"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies,
on Ciclad and at TGCC.

The project IGCM_OUT_old presents many possible keywords (facets) to determine precisely the dataset and render the data location as efficient as possible.
We have chosen to provide 'wild cards' (*) to many keywords by default. This way, ds() has a greater chance to feed the user back with a result (even if it contains too many simulations),
even if the user specifies just a few keywords.

Three projects are available to access the IGCM_OUT outputs; they are aimed at dealing with the diversity of variable names seen among the IPSL outputs (that can vary with time and users).
They all provide aliases to the CMIP variables names and to the old names (taking advantage of the mechanisms linked with calias).
- IGCM_OUT corresponds to the more up-to-date combination of variable names (mix of CMIP and old names)
- IGCM_OUT_old : links with the old variable names
- IGCM_OUT_CMIP : simply uses calias to provide the scale, offset and filenameVar

The attributes are:
  - root : path (without the login) to the top of the IGCM_OUT_old tree
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
  - clim_period_length : can be set to '_50Y' or '_100Y' to access the annual cycles averaged over 50yr long or 100yr long periods

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
 >>> dat1 = ds(project='IGCM_OUT_old',
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
 >>> dat1 = ds(project='IGCM_OUT_old',
               model='IPSLCM6',
               simulation='O1T09V04',
               period='1850-1900',
               variable='tas'
               )


Example 2:
- On Curie, access to a 'SE_50Y' dataset of the variable tas, providing values to all facets;
Note that we set frequency to 'seasonal' (or 'annual_cycle'), specify clim_period and clim_period_length (to specify either _50Y or _100Y)
 >>> dat2 = ds(project='IGCM_OUT_old',
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

Contact: jerome.servonnat@lsce.ipsl.fr

"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip



root = None
if atTGCC:
   # Declare a list of root directories for IPSL data at TGCC
   root="/ccc/store/cont003/dsm"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/data/jservon/IPSL_DATA/SIMULATIONS"
if onSpip:
   # Declare a list of root directories for IPSL data at TGCC
   root="/Users/marti/Volumes/CURIE/ccc/store/cont003/dsm"
   print 'igcm_out : declaration root sur Spip : ', root


p=cproject("IGCM_OUT_old", "root", "login", "model", "status", "experiment", "simulation", "DIR", "OUT", "ave_length", "frequency", "period", "clim_period", "clim_period_length", ensemble=["model","simulation","clim_period"], separator="%")

cdef('root'               , root       ,  project='IGCM_OUT_old')
cdef('clim_period'        , '????_????',  project='IGCM_OUT_old')
cdef('clim_period_length' , '*'        ,  project='IGCM_OUT_old') # --> Takes the following values: '*', '' (to access only to SE), '_50Y', '_100Y'
cdef('ave_length'         , '*'        ,  project='IGCM_OUT_old') # --> Takes the following values: MO, DA...
cdef('model'              , '*'        ,  project='IGCM_OUT_old')
cdef('status'             , '*'        ,  project='IGCM_OUT_old') # --> PROD, DEVT, TEST
cdef('simulation'         , '*'        ,  project='IGCM_OUT_old')
cdef('variable'           , '*'        ,  project='IGCM_OUT_old')
cdef('frequency'          , 'monthly'  ,  project='IGCM_OUT_old')
cdef('experiment'         , '*'        ,  project='IGCM_OUT_old')
cdef('OUT'                , 'Analyse'  ,  project='IGCM_OUT_old') # --> Output, Analyse
cdef('DIR'                , '*'        ,  project='IGCM_OUT_old') # --> ATM, OCE, SRF...
cdef('login'              , '*'        ,  project='IGCM_OUT_old')
cdef('period'             , 'fx'       ,  project='IGCM_OUT_old')


# Frequency alias
cfreqs('IGCM_OUT_old', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE'})

urls_IGCM_OUT_old=[
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${ave_length}/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
	      "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}${clim_period_length}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
              ]


# Next command will lead to explore all directories in 'urls_IGCM_OUT_old'
# for searching data for a CliMAF dataset (by function ds) except if 
# a more specific dataloc entry matches the arguments to 'ds'
dataloc(project="IGCM_OUT_old", organization="generic", url=urls_IGCM_OUT_old)


# -- Note:
# -- In the project IGCM_OUT_old, we have defined aliases for both the CMIP variable names (aliased to the old igcm names when necessary)
# -- and the old IGCM names to take advantage of the mechanisms behind calias (scale, offset, filenameVar)



# ---------------------------------------- #
# -- Aliases to the CMIP variable names -- #

# OCE
calias("IGCM_OUT_old", 'tos'     ,'sosstsst' , offset=273.15 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'sos'     ,'sosaline'                 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'thetao'  ,'votemper' , offset=273.15 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'so'      ,'vosaline'                 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'zos'     ,'sossheig'                 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'mlotst'  ,'mldr10_3'                 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'mlddt02' ,'mld_dt02'                 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'hc300'   ,'sohtc300' ,   scale=1.E-9 , filenameVar='grid_T')

# ICE
calias("IGCM_OUT_old", 'sic'   ,    'siconc',   scale=100 , filenameVar="icemod") 
calias("IGCM_OUT_old", 'sit'   ,    'sithic'              , filenameVar="icemod") 

# ATM general variables
calias("IGCM_OUT_old", 'pr'      ,'precip'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'prw'     ,'prw'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'psl'     ,'slp'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'tas'     ,'t2m'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'huss'    ,'q2m'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'uas'     ,'u10m'    ,filenameVar='histmth')
calias("IGCM_OUT_old", 'vas'     ,'v10m'    ,filenameVar='histmth')
calias("IGCM_OUT_old", 'sfcWind' ,'wind10m' ,filenameVar='histmth')

# 3D Variables
calias("IGCM_OUT_old", 'ta'  , filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'ua'  , filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'va'  , filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'zg'  , filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'hus' , filenameVar='histmthNMC')

# -> Turbulent fluxes
calias("IGCM_OUT_old", 'hfls'   ,'flat' , scale=-1 , filenameVar='histmth')
calias("IGCM_OUT_old", 'hfss'   ,'sens' , scale=-1 , filenameVar='histmth')
calias("IGCM_OUT_old", 'tauu'   ,'taux'            , filenameVar='histmth')
calias("IGCM_OUT_old", 'tauv'   ,'tauy'            , filenameVar='histmth')

# -> Clouds
calias("IGCM_OUT_old", 'clt'   ,'cldt'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_old", 'cldl'           , scale=100, filenameVar='histmth')
calias("IGCM_OUT_old", 'cldm'           , scale=100, filenameVar='histmth')
calias("IGCM_OUT_old", 'cldh'           , scale=100, filenameVar='histmth')

# -> Radiative up at TOA
calias("IGCM_OUT_old", 'rlut'   ,'topl'        ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rsut'   ,'SWupTOA'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rlutcs' ,'topl0'       ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rsutcs' ,'SWupTOAclr'  ,filenameVar='histmth')

# -> Radiative down at TOA
calias("IGCM_OUT_old", 'rsdt'   ,'SWdnTOA'     ,filenameVar='histmth')

# -> Radiative up at Surface
calias("IGCM_OUT_old", 'rlus'   ,'LWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rsus'   ,'SWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rsuscs' ,'SWupSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rluscs' ,'LWupSFCclr'  ,filenameVar='histmth')

# -> Radiative down at Surface
calias("IGCM_OUT_old", 'rlds'   ,'LWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rsds'   ,'SWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rldscs' ,'LWdnSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rsdscs' ,'SWdnSFCclr'  ,filenameVar='histmth')



# ---------------------------------------------------------------------------------------------- #
# --> Aliases to the old IGCM_OUT names (to take advantage of offset, scale and filenameVar)  -- #

# OCE
calias("IGCM_OUT_old", 'sosstsst'            , offset=273.15 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'sosaline'                            , filenameVar='grid_T')
calias("IGCM_OUT_old", 'votemper'            , offset=273.15 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'vosaline'                            , filenameVar='grid_T')
calias("IGCM_OUT_old", 'mldr10_3'                            , filenameVar='grid_T')
calias("IGCM_OUT_old", 'somx3010'                            , filenameVar='grid_T')
calias("IGCM_OUT_old", 'sohtc300'            ,   scale=1.E-9 , filenameVar='grid_T')
calias("IGCM_OUT_old", 'mld_dt02'                            , filenameVar='grid_T')

# ICE
calias("IGCM_OUT_old", 'siconc' ,  scale=100 , filenameVar="icemod")
calias("IGCM_OUT_old", 'sithic'              , filenameVar="icemod")
calias("IGCM_OUT_old", 'sivolu'              , filenameVar="icemod")

# ATM general variables
calias("IGCM_OUT_old", 'precip'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'prw'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'slp'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 't2m'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'q2m'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'u10m'    ,filenameVar='histmth')
calias("IGCM_OUT_old", 'v10m'    ,filenameVar='histmth')
calias("IGCM_OUT_old", 'wind10m' ,filenameVar='histmth')

# -> Turbulent fluxes
calias("IGCM_OUT_old", 'flat' , scale=-1 , filenameVar='histmth')
calias("IGCM_OUT_old", 'sens' , scale=-1 , filenameVar='histmth')
calias("IGCM_OUT_old", 'taux'            , filenameVar='histmth')
calias("IGCM_OUT_old", 'tauy'            , filenameVar='histmth')

# -> Clouds
calias("IGCM_OUT_old", 'cldt'           , scale=100, filenameVar='histmth')

# -> Radiative down at TOA
calias("IGCM_OUT_old", 'SWdnTOA'     ,filenameVar='histmth')

# -> Radiative down at TOA
calias("IGCM_OUT_old", 'topl'        ,filenameVar='histmth')
calias("IGCM_OUT_old", 'SWupTOA'     ,filenameVar='histmth')
calias("IGCM_OUT_old", 'topl0'       ,filenameVar='histmth')
calias("IGCM_OUT_old", 'SWupTOAclr'  ,filenameVar='histmth')

# -> Radiative up at Surface
calias("IGCM_OUT_old", 'LWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'SWupSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'SWupSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'LWupSFCclr'  ,filenameVar='histmth')

# -> Radiative down at Surface
calias("IGCM_OUT_old", 'LWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'SWdnSFC'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'LWdnSFCclr'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'SWdnSFCclr'  ,filenameVar='histmth')




