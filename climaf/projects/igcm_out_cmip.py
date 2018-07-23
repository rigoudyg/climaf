"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies,
on Ciclad and at TGCC.

The project IGCM_OUT_CMIP presents many possible keywords (facets) to determine precisely the dataset and render the data location as efficient as possible.
We have chosen to provide 'wild cards' (*) to many keywords by default. This way, ds() has a greater chance to feed the user back with a result (even if it contains too many simulations),
even if the user specifies just a few keywords.

Three projects are available to access the IGCM_OUT outputs; they are aimed at dealing with the diversity of variable names seen among the IPSL outputs (that can vary with time and users).
They all provide aliases to the CMIP variables names and to the old names (taking advantage of the mechanisms linked with calias).
- IGCM_OUT corresponds to the more up-to-date combination of variable names (mix of CMIP and old names)
- IGCM_OUT_old : links with the old variable names
- IGCM_OUT_CMIP : simply uses calias to provide the scale, offset and filenameVar

The attributes are:
  - root : path (without the login) to the top of the IGCM_OUT_CMIP tree
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

 >>> dat1 = ds(project='IGCM_OUT_CMIP',
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
 >>> dat1 = ds(project='IGCM_OUT_CMIP',
               model='IPSLCM6',
               simulation='O1T09V04',
               period='1850-1900',
               variable='tas'
               )


Example 2:
- On Curie, access to a 'SE_50Y' dataset of the variable tas, providing values to all facets;
Note that we set frequency to 'seasonal' (or 'annual_cycle'), specify clim_period and clim_period_length (to specify either _50Y or _100Y)

 >>> dat2 = ds(project='IGCM_OUT_CMIP',
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

if  root :
   
   p=cproject("IGCM_OUT_CMIP", "root", "login", "model", "status", "experiment", "simulation", "DIR", "OUT", "ave_length", "frequency", "period", "clim_period", "clim_period_length", ensemble=["model","simulation","clim_period"], separator="%")
   
   cdef('root'               , root       ,  project='IGCM_OUT_CMIP')
   cdef('clim_period'        , '????_????',  project='IGCM_OUT_CMIP')
   cdef('clim_period_length' , '*'        ,  project='IGCM_OUT_CMIP') # --> Takes the following values: '*', '' (to access only to SE), '_50Y', '_100Y'
   cdef('ave_length'         , '*'        ,  project='IGCM_OUT_CMIP') # --> Takes the following values: MO, DA...
   cdef('model'              , '*'        ,  project='IGCM_OUT_CMIP')
   cdef('status'             , '*'        ,  project='IGCM_OUT_CMIP') # --> PROD, DEVT, TEST
   cdef('simulation'         , '*'        ,  project='IGCM_OUT_CMIP')
   cdef('variable'           , '*'        ,  project='IGCM_OUT_CMIP')
   cdef('frequency'          , 'monthly'  ,  project='IGCM_OUT_CMIP')
   cdef('experiment'         , '*'        ,  project='IGCM_OUT_CMIP')
   cdef('OUT'                , 'Analyse'  ,  project='IGCM_OUT_CMIP') # --> Output, Analyse
   cdef('DIR'                , '*'        ,  project='IGCM_OUT_CMIP') # --> ATM, OCE, SRF...
   cdef('login'              , '*'        ,  project='IGCM_OUT_CMIP')
   cdef('period'             , 'fx'       ,  project='IGCM_OUT_CMIP')
   
   
   # Frequency alias
   cfreqs('IGCM_OUT_CMIP', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE'})
   
   urls_IGCM_OUT_CMIP=[
      "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${ave_length}/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
      "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}${clim_period_length}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc",
      "${root}/${login}/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${ave_length}/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
      "${root}/${login}/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}${clim_period_length}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
   ]
   
   
   # Next command will lead to explore all directories in 'urls_IGCM_OUT_CMIP'
   # for searching data for a CliMAF dataset (by function ds) except if 
   # a more specific dataloc entry matches the arguments to 'ds'
   dataloc(project="IGCM_OUT_CMIP", organization="generic", url=urls_IGCM_OUT_CMIP)
   
   
   # -- Note:
   # -- In the project IGCM_OUT_CMIP, we have defined aliases for both the CMIP variable names (aliased to the old igcm names when necessary)
   # -- and the old IGCM names to take advantage of the mechanisms behind calias (scale, offset, filenameVar)
   
   
   
   # ---------------------------------------- #
   # -- Aliases to the CMIP variable names -- #
   
   # OCE
   calias("IGCM_OUT_CMIP", 'tos'                 , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'sos'                                 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'thetao'              , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'so'                                  , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'zos'                                 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'mlotst'                              , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'mlddt02' ,'mld_dt02'                 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'hc300'               ,   scale=1.E-9 , filenameVar='grid_T')
   
   # ICE
   calias("IGCM_OUT_CMIP", 'sic' , scale=100 , filenameVar="icemod") 
   calias("IGCM_OUT_CMIP", 'sit'             , filenameVar="icemod") 
   
   # ATM general variables
   calias("IGCM_OUT_CMIP", 'pr'      ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'prw'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'psl'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'tas'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'huss'    ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'uas'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'vas'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'sfcWind' ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 't2m', 'tas'      ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'precip'      ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'nettop'      ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'bils'      ,filenameVar='histmth')
   
   # 3D Variables
   calias("IGCM_OUT_CMIP", 'vitu'  , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'vitv'  , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'vitw'  , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'temp'  , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'ta'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_CMIP", 'ua'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_CMIP", 'va'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_CMIP", 'zg'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_CMIP", 'hus' , filenameVar='histmthNMC')
   
   # -> Turbulent fluxes
   calias("IGCM_OUT_CMIP", 'hfls'  , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'hfss'  , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'tauu'             , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'tauv'             , filenameVar='histmth')
   
   # -> Clouds
   calias("IGCM_OUT_CMIP", 'clt'    , scale=100, filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'cldl'   , scale=100, filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'cldm'   , scale=100, filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'cldh'   , scale=100, filenameVar='histmth')
   
   # -> Radiative up at TOA
   calias("IGCM_OUT_CMIP", 'rlut'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rsut'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rlutcs'   ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rsutcs'   ,filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT_CMIP", 'rsdt'     ,filenameVar='histmth')
   
   # -> Radiative up at Surface
   calias("IGCM_OUT_CMIP", 'rlus'   ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rsus'   ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rsuscs' ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rluscs' ,filenameVar='histmth')
   
   # -> Radiative down at Surface
   calias("IGCM_OUT_CMIP", 'rlds'   ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rsds'   ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rldscs' ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'rsdscs' ,filenameVar='histmth')
   
   
   # ---------------------------------------------------------------------------------------------- #
   # --> Aliases to the old IGCM_OUT_CMIP names (to take advantage of offset, scale and filenameVar)  -- #
   
   # OCE
   calias("IGCM_OUT_CMIP", 'sosstsst'            , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'sosaline'                            , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'votemper'            , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'vosaline'                            , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'mldr10_3'                            , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'somx3010'                            , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'sohtc300'            ,   scale=1.E-9 , filenameVar='grid_T')
   calias("IGCM_OUT_CMIP", 'mld_dt02'                            , filenameVar='grid_T')
   
   # ICE
   calias("IGCM_OUT_CMIP", 'siconc' ,  scale=100 , filenameVar="icemod")
   calias("IGCM_OUT_CMIP", 'sithic'              , filenameVar="icemod")
   calias("IGCM_OUT_CMIP", 'sivolu'              , filenameVar="icemod")
   
   # ATM general variables
   calias("IGCM_OUT_CMIP", 'precip'  ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'prw'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'slp'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 't2m'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'q2m'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'u10m'    ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'v10m'    ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'wind10m' ,filenameVar='histmth')
   
   # -> Turbulent fluxes
   calias("IGCM_OUT_CMIP", 'flat' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'sens' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'taux'            , filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'tauy'            , filenameVar='histmth')
   
   # -> Clouds
   calias("IGCM_OUT_CMIP", 'cldt'           , scale=100, filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT_CMIP", 'SWdnTOA'     ,filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT_CMIP", 'topl'        ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'SWupTOA'     ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'topl0'       ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'SWupTOAclr'  ,filenameVar='histmth')
   
   # -> Radiative up at Surface
   calias("IGCM_OUT_CMIP", 'LWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'SWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'SWupSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'LWupSFCclr'  ,filenameVar='histmth')
   
   # -> Radiative down at Surface
   calias("IGCM_OUT_CMIP", 'LWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'SWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'LWdnSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT_CMIP", 'SWdnSFCclr'  ,filenameVar='histmth')




