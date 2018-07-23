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
login= None
if atTGCC:
   # Declare a list of root directories for IPSL data at TGCC
   root="/ccc/store/cont003/thredds"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/ccc/store/cont003/thredds"
   login="fabric"
if onSpip:
   # Declare a list of root directories for IPSL data at TGCC
   root="/Users/marti/Volumes/CURIE/ccc/store/cont003/dsm"
   print 'igcm_out : declaration root sur Spip : ', root

if root:

   p=cproject("IGCM_OUT_fast", "root", "login", "model", "status", "experiment", "simulation", "DIR", "OUT", "ave_length", "frequency", "period", "clim_period", "clim_period_length", "IGCM_OUT", ensemble=["model","simulation","clim_period"], separator="%")
   
   cdef('root'               , root       ,  project='IGCM_OUT_fast')
   if login: cdef('login' , login, project='IGCM_OUT_fast')
   cdef('clim_period'        , '????_????',  project='IGCM_OUT_fast')
   cdef('clim_period_length' , '*'        ,  project='IGCM_OUT_fast') # --> Takes the following values: '*', '' (to access only to SE), '_50Y', '_100Y'
   cdef('ave_length'         , '*'        ,  project='IGCM_OUT_fast') # --> Takes the following values: MO, DA...
   cdef('model'              , '*'        ,  project='IGCM_OUT_fast')
   cdef('status'             , '*'        ,  project='IGCM_OUT_fast') # --> PROD, DEVT, TEST
   cdef('simulation'         , '*'        ,  project='IGCM_OUT_fast')
   cdef('variable'           , '*'        ,  project='IGCM_OUT_fast')
   cdef('frequency'          , 'monthly'  ,  project='IGCM_OUT_fast')
   cdef('experiment'         , '*'        ,  project='IGCM_OUT_fast')
   cdef('OUT'                , 'Analyse'  ,  project='IGCM_OUT_fast') # --> Output, Analyse
   cdef('DIR'                , '*'        ,  project='IGCM_OUT_fast') # --> ATM, OCE, SRF...
   cdef('login'              , '*'        ,  project='IGCM_OUT_fast')
   cdef('period'             , 'fx'       ,  project='IGCM_OUT_fast')
   cdef('IGCM_OUT'           , ''         ,  project='IGCM_OUT_fast')
   
   
   # Frequency alias
   cfreqs('IGCM_OUT_fast', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE', 'yearly':'1Y'})
   
   urls_IGCM_OUT=[
      "${root}/${login}/${IGCM_OUT}/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${ave_length}/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
      "${root}/${login}/${IGCM_OUT}/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}${clim_period_length}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc",
   ]
   
   
   # Next command will lead to explore all directories in 'urls_IGCM_OUT'
   # for searching data for a CliMAF dataset (by function ds) except if 
   # a more specific dataloc entry matches the arguments to 'ds'
   dataloc(project="IGCM_OUT_fast", organization="generic", url=urls_IGCM_OUT)
   
   
   # -- Note:
   # -- In the project IGCM_OUT, we have defined aliases for both the CMIP variable names (aliased to the old igcm names when necessary)
   # -- and the old IGCM names to take advantage of the mechanisms behind calias (scale, offset, filenameVar)
   
   
   
   # ---------------------------------------- #
   # -- Aliases to the CMIP variable names -- #
   
   # OCE
   calias("IGCM_OUT_fast", 'tos'                 , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'sos'                                 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'thetao'              , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'so'                                  , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'zos'                                 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'mlotst'  ,'mldr10_3'                 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'mlddt02' ,'mld_dt02'                 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'hc300'               ,   scale=1.E-9 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'wfo'                                 , filenameVar='grid_T')
   
   # ICE
   calias("IGCM_OUT_fast", 'sic'   ,    'siconc',   scale=100 , filenameVar="icemod") 
   calias("IGCM_OUT_fast", 'sit'   ,    'sithic'              , filenameVar="icemod") 
   calias("IGCM_OUT_fast", 'sivolu'                       , filenameVar="icemod")

   # ATM general variables
   calias("IGCM_OUT_fast", 'pr'      ,'precip'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'prw'                ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'psl'     ,'slp'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'tas'     ,'t2m'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'huss'    ,'q2m'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'uas'     ,'u10m'    ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'vas'     ,'v10m'    ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'sfcWind' ,'wind10m' ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'hurs'    ,'rh2m'    ,filenameVar='histmth')
   
   # 3D Variables
   calias("IGCM_OUT_fast", 'ta'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_fast", 'ua'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_fast", 'va'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_fast", 'zg'  , filenameVar='histmthNMC')
   calias("IGCM_OUT_fast", 'hus' , filenameVar='histmthNMC')
   calias("IGCM_OUT_fast", 'hur' , filenameVar='histmthNMC')
   
   # -> Turbulent fluxes
   calias("IGCM_OUT_fast", 'hfls'   ,'flat' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_fast", 'hfss'   ,'sens' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_fast", 'tauu'   ,'taux'            , filenameVar='histmth')
   calias("IGCM_OUT_fast", 'tauv'   ,'tauy'            , filenameVar='histmth')
   
   # -> Clouds
   calias("IGCM_OUT_fast", 'clt'   ,'cldt'  , scale=100, filenameVar='histmth')
   calias("IGCM_OUT_fast", 'cldl'           , scale=100, filenameVar='histmth')
   calias("IGCM_OUT_fast", 'cldm'           , scale=100, filenameVar='histmth')
   calias("IGCM_OUT_fast", 'cldh'           , scale=100, filenameVar='histmth')
   
   # -> Radiative up at TOA
   calias("IGCM_OUT_fast", 'rlut'   ,'topl'        ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rsut'   ,'SWupTOA'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rlutcs' ,'topl0'       ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rsutcs' ,'SWupTOAclr'  ,filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT_fast", 'rsdt'   ,'SWdnTOA'     ,filenameVar='histmth')
   
   # -> Radiative up at Surface
   calias("IGCM_OUT_fast", 'rlus'   ,'LWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rsus'   ,'SWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rsuscs' ,'SWupSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rluscs' ,'LWupSFCclr'  ,filenameVar='histmth')
   
   # -> Radiative down at Surface
   calias("IGCM_OUT_fast", 'rlds'   ,'LWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rsds'   ,'SWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rldscs' ,'LWdnSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'rsdscs' ,'SWdnSFCclr'  ,filenameVar='histmth')
   
   # -- Land surface - ORCHIDEE
   #calias("IGCM_OUT_fast", 'gpp'   , scale=1000  ,filenameVar='sechiba_history')
   # --> !!! This will not stay in the param file !!! --------------------
   calias("IGCM_OUT_fast", 'fluxlat' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'fluxsens' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'albnir', 'alb_nir' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'albvis', 'alb_vis' ,filenameVar='sechiba_history')
   #derive("IGCM_OUT_fast", 'tmp_alb_mean', 'plus', 'alb_nir', 'alb_vis')
   #derive("IGCM_OUT_fast", 'alb_mean', 'ccdo', 'tmp_alb_mean', operator='divc,2')
   calias("IGCM_OUT_fast", 'tair' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'swdown' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'lwdown' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'transpir' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'evapnu' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'inter' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'subli' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'evap' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'Qs' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'runoff' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'drainage' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'frac_snow' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'snow' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'lai' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'maint_resp' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'growth_resp' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'hetero_resp' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'maintresp', 'maint_resp', filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'growthresp', 'growth_resp', filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'heteroresp', 'hetero_resp', filenameVar='sechiba_history')
   #derive("IGCM_OUT_fast", 'auto_resp', 'plus', 'growth_resp', 'maint_resp')
   #derive("IGCM_OUT_fast", 'autoresp', 'plus', 'growth_resp', 'maint_resp')
   calias("IGCM_OUT_fast", 'nee' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'total_soil_carb', 'TOTAL_SOIL_CARB' ,filenameVar='stomate_history')
   calias("IGCM_OUT_fast", 'totalsoilcarb', 'TOTAL_SOIL_CARB' ,filenameVar='stomate_history')
   calias("IGCM_OUT_fast", 'maxvegetfrac' ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'vegetfrac' ,filenameVar='sechiba_history')
   #calias("IGCM_OUT_fast", 'gpp'   , scale=0.001  ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'lai' ,filenameVar='stomate_ipcc_history')
   calias("IGCM_OUT_fast", 'cfracgpp', 'gpp' ,filenameVar='stomate_ipcc_history')
   #derive("IGCM_OUT_fast", 'gpptot', 'divide', 'cfracgpp','Contfrac')
   # -> alias for the obs
   calias("ref_climatos", 'gpptot', 'gpp')
   calias("IGCM_OUT_fast", 'GPP'   ,'gpp' , scale=0.001 ,filenameVar='sechiba_history')
   calias("IGCM_OUT_fast", 'Contfrac' ,filenameVar='sechiba_history')



   # ---------------------------------------------------------------------------------------------- #
   # --> Aliases to the zonal average (computed on the x axis of the ORCA grid)                  -- #

   calias('IGCM_OUT_fast', 'zotemglo', offset=273.15, filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zotempac', offset=273.15, filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zotematl', offset=273.15, filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zotemind', offset=273.15, filenameVar='diaptr')

   calias('IGCM_OUT_fast', 'zosalglo', filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zosalpac', filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zosalatl', filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zosalind', filenameVar='diaptr')

   calias('IGCM_OUT_fast', 'zomsfglo', filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zomsfpac', filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zomsfatl', filenameVar='diaptr')
   calias('IGCM_OUT_fast', 'zomsfind', filenameVar='diaptr')

   
   # ---------------------------------------------------------------------------------------------- #
   # --> Aliases to the old IGCM_OUT_fast names (to take advantage of offset, scale and filenameVar)  -- #
   
   # OCE
   calias("IGCM_OUT_fast", 'sosstsst'            , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'sosaline'                            , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'votemper'            , offset=273.15 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'vosaline'                            , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'mldr10_3'                            , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'somx3010'                            , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'sohtc300'            ,   scale=1.E-9 , filenameVar='grid_T')
   calias("IGCM_OUT_fast", 'mld_dt02'                            , filenameVar='grid_T')

   # -- Wind stress curl
   calias('IGCM_OUT_fast', 'tauuo', filenameVar='grid_U')
   calias('IGCM_OUT_fast', 'tauvo', filenameVar='grid_V')

   # -> Biogeochemistry
   calias('IGCM_OUT_fast', 'NO3', filenameVar='ptrc_T')
   calias('IGCM_OUT_fast', 'PO4', filenameVar='ptrc_T')
   calias('IGCM_OUT_fast', 'Si', filenameVar='ptrc_T')
   calias('IGCM_OUT_fast', 'O2', filenameVar='ptrc_T')
   
   # ICE
   calias("IGCM_OUT_fast", 'siconc' ,  scale=100 , filenameVar="icemod")
   calias("IGCM_OUT_fast", 'sithic'              , filenameVar="icemod")
   calias("IGCM_OUT_fast", 'sivolu'              , filenameVar="icemod")
   
   # ATM general variables
   calias("IGCM_OUT_fast", 'precip'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'prw'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'slp'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 't2m'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'q2m'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'u10m'    ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'v10m'    ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'wind10m' ,filenameVar='histmth')
   
   # -> Turbulent fluxes
   calias("IGCM_OUT_fast", 'flat' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_fast", 'sens' , scale=-1 , filenameVar='histmth')
   calias("IGCM_OUT_fast", 'taux'            , filenameVar='histmth')
   calias("IGCM_OUT_fast", 'tauy'            , filenameVar='histmth')
   
   # -> Clouds
   calias("IGCM_OUT_fast", 'cldt'           , scale=100, filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT_fast", 'SWdnTOA'     ,filenameVar='histmth')
   
   # -> Radiative down at TOA
   calias("IGCM_OUT_fast", 'topl'        ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'SWupTOA'     ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'topl0'       ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'SWupTOAclr'  ,filenameVar='histmth')
   
   # -> Radiative up at Surface
   calias("IGCM_OUT_fast", 'LWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'SWupSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'SWupSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'LWupSFCclr'  ,filenameVar='histmth')
   
   # -> Radiative down at Surface
   calias("IGCM_OUT_fast", 'LWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'SWdnSFC'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'LWdnSFCclr'  ,filenameVar='histmth')
   calias("IGCM_OUT_fast", 'SWdnSFCclr'  ,filenameVar='histmth')
   
   
