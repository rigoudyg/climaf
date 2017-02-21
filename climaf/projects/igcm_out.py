"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies,
on Ciclad and at TGCC.

The project IGCM_OUT presents many possible keywords (facets) to determine precisely the dataset and render the data location as efficient as possible.
We have chosen to provide 'wild cards' (*) to many keywords by default. This way, ds() has a greater chance to feed the user back with a result (even if it contains too many simulations),
even if the user specifies just a few keywords.

Three projects are available to access the IGCM_OUT outputs; they are aimed at dealing with the diversity of variable names seen among the IPSL outputs (that can vary with time and users).
They all provide aliases to the CMIP variables names and to the old names (taking advantage of the mechanisms linked with calias).
- IGCM_OUT corresponds to the more up-to-date combination of variable names (mix of CMIP and old names)
- IGCM_OUT_old : links with the old variable names
- IGCM_OUT_CMIP : simply uses calias to provide the scale, offset and filenameVar


The attributes are:
  - root : path (without the login) to the top of the IGCM_OUT tree
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

 >>> dat1 = ds(project='IGCM_OUT',
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
 >>> dat1 = ds(project='IGCM_OUT',
               model='IPSLCM6',
               simulation='O1T09V04',
               period='1850-1900',
               variable='tas'
               )


Example 2:
- On Curie, access to a 'SE_50Y' dataset of the variable tas, providing values to all facets;
Note that we set frequency to 'seasonal' (or 'annual_cycle'), specify clim_period and clim_period_length (to specify either _50Y or _100Y)

 >>> dat2 = ds(project='IGCM_OUT',
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

 >>> dat_ens = eds(project='IGCM_OUT',
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
   root="/ccc/store/cont003/dsm"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/data/jservon/IPSL_DATA/SIMULATIONS"
if onSpip:
   # Declare a list of root directories for IPSL data at TGCC
   root="/Users/marti/Volumes/CURIE/ccc/store/cont003/dsm"
   print 'igcm_out : declaration root sur Spip : ', root

if root:

   p=cproject("IGCM_OUT", "root", "login", "model", "status", "experiment", "simulation", "DIR", "OUT", "ave_length", "frequency", "period", "clim_period", "clim_period_length", ensemble=["model","simulation","clim_period"], separator="%")
   
   cdef('root'               , root       ,  project='IGCM_OUT')
   cdef('clim_period'        , '????_????',  project='IGCM_OUT')
   cdef('clim_period_length' , '*'        ,  project='IGCM_OUT') # --> Takes the following values: '*', '' (to access only to SE), '_50Y', '_100Y'
   cdef('ave_length'         , '*'        ,  project='IGCM_OUT') # --> Takes the following values: MO, DA...
   cdef('model'              , '*'        ,  project='IGCM_OUT')
   cdef('status'             , '*'        ,  project='IGCM_OUT') # --> PROD, DEVT, TEST
   cdef('simulation'         , '*'        ,  project='IGCM_OUT')
   cdef('variable'           , '*'        ,  project='IGCM_OUT')
   cdef('frequency'          , 'monthly'  ,  project='IGCM_OUT')
   cdef('experiment'         , '*'        ,  project='IGCM_OUT')
   cdef('OUT'                , 'Analyse'  ,  project='IGCM_OUT') # --> Output, Analyse
   cdef('DIR'                , '*'        ,  project='IGCM_OUT') # --> ATM, OCE, SRF...
   cdef('login'              , '*'        ,  project='IGCM_OUT')
   cdef('period'             , 'fx'       ,  project='IGCM_OUT')
   
   
   # Frequency alias
   cfreqs('IGCM_OUT', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE'})
   
   urls_IGCM_OUT=[
      "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${ave_length}/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
      "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}${clim_period_length}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
   ]
   
   
   # Next command will lead to explore all directories in 'urls_IGCM_OUT'
   # for searching data for a CliMAF dataset (by function ds) except if 
   # a more specific dataloc entry matches the arguments to 'ds'
   dataloc(project="IGCM_OUT", organization="generic", url=urls_IGCM_OUT)
   
   
   # -- Note:
   # -- In the project IGCM_OUT, we have defined aliases for both the CMIP variable names (aliased to the old igcm names when necessary)
   # -- and the old IGCM names to take advantage of the mechanisms behind calias (scale, offset, filenameVar)
   
   
   
   # ---------------------------------------- #
   # -- Aliases to the CMIP variable names -- #
   
   # OCE
   calias("IGCM_OUT", 'tos'                 , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT", 'sos'                                 , filenameVar='grid_T')
   calias("IGCM_OUT", 'thetao'              , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT", 'so'                                  , filenameVar='grid_T')
   calias("IGCM_OUT", 'zos'                                 , filenameVar='grid_T')
   calias("IGCM_OUT", 'mlotst'  ,'mldr10_3'                 , filenameVar='grid_T')
   calias("IGCM_OUT", 'mlddt02' ,'mld_dt02'                 , filenameVar='grid_T')
   calias("IGCM_OUT", 'hc300'               ,   scale=1.E-9 , filenameVar='grid_T')
   
   # ICE
   calias("IGCM_OUT", 'sic'   ,    'siconc',   scale=100 , filenameVar="icemod") 
   calias("IGCM_OUT", 'sit'   ,    'sithic'              , filenameVar="icemod") 
   
   # ATM general variables
   calias("IGCM_OUT", 'pr'      ,'precip'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'prw'                ,filenameVar='histmth')
   calias("IGCM_OUT", 'psl'     ,'slp'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'tas'     ,'t2m'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'huss'    ,'q2m'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'uas'     ,'u10m'    ,filenameVar='histmth')
   calias("IGCM_OUT", 'vas'     ,'v10m'    ,filenameVar='histmth')
   calias("IGCM_OUT", 'sfcWind' ,'wind10m' ,filenameVar='histmth')
   
   # 3D Variables
   calias("IGCM_OUT", 'ta'  , filenameVar='histmthNMC')
   calias("IGCM_OUT", 'ua'  , filenameVar='histmthNMC')
   calias("IGCM_OUT", 'va'  , filenameVar='histmthNMC')
   calias("IGCM_OUT", 'zg'  , filenameVar='histmthNMC')
   calias("IGCM_OUT", 'hus' , filenameVar='histmthNMC')
   
   # -> Turbulent fluxes
   calias("IGCM_OUT", 'hfls'   ,'flat' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT", 'hfss'   ,'sens' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT", 'tauu'   ,'taux'            , filenameVar='histmth')
   calias("IGCM_OUT", 'tauv'   ,'tauy'            , filenameVar='histmth')
   
   # -> Clouds
   calias("IGCM_OUT", 'clt'   ,'cldt'  , scale=100, filenameVar='histmth')
   calias("IGCM_OUT", 'cldl'           , scale=100, filenameVar='histmth')
   calias("IGCM_OUT", 'cldm'           , scale=100, filenameVar='histmth')
   calias("IGCM_OUT", 'cldh'           , scale=100, filenameVar='histmth')
   
   # -> Radiative up at TOA
   calias("IGCM_OUT", 'rlut'   ,'topl'        ,filenameVar='histmth')
   calias("IGCM_OUT", 'rsut'   ,'SWupTOA'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'rlutcs' ,'topl0'       ,filenameVar='histmth')
   calias("IGCM_OUT", 'rsutcs' ,'SWupTOAclr'  ,filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT", 'rsdt'   ,'SWdnTOA'     ,filenameVar='histmth')
   
   # -> Radiative up at Surface
   calias("IGCM_OUT", 'rlus'   ,'LWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'rsus'   ,'SWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'rsuscs' ,'SWupSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'rluscs' ,'LWupSFCclr'  ,filenameVar='histmth')
   
   # -> Radiative down at Surface
   calias("IGCM_OUT", 'rlds'   ,'LWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'rsds'   ,'SWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'rldscs' ,'LWdnSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'rsdscs' ,'SWdnSFCclr'  ,filenameVar='histmth')
   
   
   
   # ---------------------------------------------------------------------------------------------- #
   # --> Aliases to the old IGCM_OUT names (to take advantage of offset, scale and filenameVar)  -- #
   
   # OCE
   calias("IGCM_OUT", 'sosstsst'            , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT", 'sosaline'                            , filenameVar='grid_T')
   calias("IGCM_OUT", 'votemper'            , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT", 'vosaline'                            , filenameVar='grid_T')
   calias("IGCM_OUT", 'mldr10_3'                            , filenameVar='grid_T')
   calias("IGCM_OUT", 'somx3010'                            , filenameVar='grid_T')
   calias("IGCM_OUT", 'sohtc300'            ,   scale=1.E-9 , filenameVar='grid_T')
   calias("IGCM_OUT", 'mld_dt02'                            , filenameVar='grid_T')
   
   # ICE
   calias("IGCM_OUT", 'siconc' ,  scale=100 , filenameVar="icemod")
   calias("IGCM_OUT", 'sithic'              , filenameVar="icemod")
   calias("IGCM_OUT", 'sivolu'              , filenameVar="icemod")
   
   # ATM general variables
   calias("IGCM_OUT", 'precip'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'prw'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'slp'     ,filenameVar='histmth')
   calias("IGCM_OUT", 't2m'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'q2m'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'u10m'    ,filenameVar='histmth')
   calias("IGCM_OUT", 'v10m'    ,filenameVar='histmth')
   calias("IGCM_OUT", 'wind10m' ,filenameVar='histmth')
   
   # -> Turbulent fluxes
   calias("IGCM_OUT", 'flat' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT", 'sens' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT", 'taux'            , filenameVar='histmth')
   calias("IGCM_OUT", 'tauy'            , filenameVar='histmth')
   
   # -> Clouds
   calias("IGCM_OUT", 'cldt'           , scale=100, filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT", 'SWdnTOA'     ,filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT", 'topl'        ,filenameVar='histmth')
   calias("IGCM_OUT", 'SWupTOA'     ,filenameVar='histmth')
   calias("IGCM_OUT", 'topl0'       ,filenameVar='histmth')
   calias("IGCM_OUT", 'SWupTOAclr'  ,filenameVar='histmth')
   
   # -> Radiative up at Surface
   calias("IGCM_OUT", 'LWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'SWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'SWupSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'LWupSFCclr'  ,filenameVar='histmth')
   
   # -> Radiative down at Surface
   calias("IGCM_OUT", 'LWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'SWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'LWdnSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT", 'SWdnSFCclr'  ,filenameVar='histmth')
   
   
