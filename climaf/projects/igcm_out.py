"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies, and where the data is
at IPSL and on Ciclad

Example for an IGCM_OUT dataset declaration ::

 >>> tas1pc=ds(project='IGCM_OUT', model='IPSLCM6', experiment='piControl', variable='tas', frequency='monthly', period='1860-1861')

"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip

# Rajouter login et disk (ou filesystem) = scratch/store/work

# ajouter realm? atmos -> ATM; ocean -> OCE
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


p=cproject("IGCM_OUT", "clim_period", "model", "status", "simulation", "variable", "frequency", "experiment", "OUT", "DIR", "login", "period", "root", ensemble=["model","simulation"], separator="%")

cdef('root',        root,         project='IGCM_OUT')
cdef('clim_period', '????_????',  project='IGCM_OUT')
cdef('model',       '*',          project='IGCM_OUT')
cdef('status',      '*',          project='IGCM_OUT')
cdef('simulation',  '*',          project='IGCM_OUT')
cdef('variable',    '*',          project='IGCM_OUT')
cdef('frequency',   'monthly',    project='IGCM_OUT')
cdef('experiment',  '*',          project='IGCM_OUT')
cdef('OUT',         '*',          project='IGCM_OUT')
cdef('DIR',         '*',          project='IGCM_OUT')
cdef('login',       '*',          project='IGCM_OUT')
cdef('period',      '0001-3000',  project='IGCM_OUT')
#cdef('SpaceName',   '*',          project='IGCM_OUT')


# Frequency alias
cfreqs('IGCM_OUT', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE'})

urls_IGCM_OUT=[
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/*/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
	      "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc",
	      "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/SE_50Y/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
              ]


# Next command will lead to explore all directories in 'urls_IGCM_OUT'
# for searching data for a CliMAF dataset (by function ds) except if 
# a more specific dataloc entry matches the arguments to 'ds'
dataloc(project="IGCM_OUT", organization="generic", url=urls_IGCM_OUT)

# OCE
calias("IGCM_OUT", 'tos'     ,'tos'    , offset=273.15 , filenameVar='grid_T')
calias("IGCM_OUT", 'sos'     ,'sos'                    , filenameVar='grid_T')
calias("IGCM_OUT", 'to'      ,'thetao' , offset=273.15 , filenameVar='grid_T')
calias("IGCM_OUT", 'so'      ,'so'                     , filenameVar='grid_T')
calias("IGCM_OUT", 'zos'     ,'zos'                    , filenameVar='grid_T')
calias("IGCM_OUT", 'mlotst'  ,'mldr10_1'               , filenameVar='grid_T')
calias("IGCM_OUT", 'hc300'   ,'hc300'  ,   scale=1.E-9 , filenameVar='grid_T')
	

# ICE
calias("IGCM_OUT", 'sic'   ,    'siconc',   scale=100 , filenameVar="icemod") 
calias("IGCM_OUT", 'sithic',    'sithic',   filenameVar="icemod") 
calias("IGCM_OUT", 'sivolu',    'sivolu',   filenameVar="icemod") 

# ATM general variables
calias("IGCM_OUT", 'pr'      ,'precip'  ,filenameVar='histmth')
calias("IGCM_OUT", 'prw'     ,'prw'     ,filenameVar='histmth')
calias("IGCM_OUT", 'psl'     ,'slp'     ,filenameVar='histmth')
calias("IGCM_OUT", 'tas'     ,'t2m'     ,filenameVar='histmth')
calias("IGCM_OUT", 'huss'    ,'q2m'     ,filenameVar='histmth')
calias("IGCM_OUT", 'uas'     ,'u10m'    ,filenameVar='histmth')
calias("IGCM_OUT", 'vas'     ,'v10m'    ,filenameVar='histmth')
calias("IGCM_OUT", 'sfcWind' ,'wind10m' ,filenameVar='histmth')


# 3D Variables
calias("IGCM_OUT", 'ta'   ,'ta'    ,filenameVar='histmthNMC')
calias("IGCM_OUT", 'ua'   ,'ua'    ,filenameVar='histmthNMC')
calias("IGCM_OUT", 'va'   ,'va'    ,filenameVar='histmthNMC')
calias("IGCM_OUT", 'zg'   ,'zg'    ,filenameVar='histmthNMC')
calias("IGCM_OUT", 'hus'  ,'hus'   ,filenameVar='histmthNMC')


# -> Turbulent fluxes
calias("IGCM_OUT", 'hfls'   ,'flat' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT", 'hfss'   ,'sens' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT", 'tauu'   ,'taux'  ,filenameVar='histmth')
calias("IGCM_OUT", 'tauv'   ,'tauy'  ,filenameVar='histmth')

# -> Clouds
calias("IGCM_OUT", 'clt'   ,'cldt'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT", 'cldl'  ,'cldl'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT", 'cldm'  ,'cldm'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT", 'cldh'  ,'cldh'  , scale=100, filenameVar='histmth')

# -> Clouds radiative forcing
calias("IGCM_OUT", 'rlwcrf'   ,''  ,filenameVar='histmth')
calias("IGCM_OUT", 'rswcrf'   ,''  ,filenameVar='histmth')

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



