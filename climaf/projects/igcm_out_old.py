"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies, and where the data is
at IPSL and on Ciclad

Example for an IGCM_OUT_old dataset declaration ::

 >>> tas1pc=ds(project='IGCM_OUT_old', model='IPSLCM6', experiment='piControl', variable='tas', frequency='monthly', period='1860-1861')


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


p=cproject("IGCM_OUT_old", "clim_period", "model", "status", "simulation", "variable", "frequency", "experiment", "OUT", "DIR", "login", "period", "root", ensemble=["model","simulation"], separator="%")

cdef('root',        root,         project='IGCM_OUT_old')
cdef('clim_period', '????_????',  project='IGCM_OUT_old')
cdef('model',       '*',          project='IGCM_OUT_old')
cdef('status',      '*',          project='IGCM_OUT_old')
cdef('simulation',  '*',          project='IGCM_OUT_old')
cdef('variable',    '*',          project='IGCM_OUT_old')
cdef('frequency',   'monthly',    project='IGCM_OUT_old')
cdef('experiment',  '*',          project='IGCM_OUT_old')
cdef('OUT',         '*',          project='IGCM_OUT_old')
cdef('DIR',         '*',          project='IGCM_OUT_old')
cdef('login',       '*',          project='IGCM_OUT_old')
cdef('period',      '0001-3000',  project='IGCM_OUT_old')


# Frequency alias
cfreqs('IGCM_OUT_old', {'monthly':'1M' , 'daily':'1D' , 'annual_cycle':'SE', 'seasonal':'SE'})

urls_IGCM_OUT_old=[
              "${root}/${login}/IGCM_OUT/${model}/*/${experiment}/${simulation}/${DIR}/${OUT}/*/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
	      "${root}/${login}/IGCM_OUT/${model}/*/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc",
              "${root}/${login}/IGCM_OUT/${model}/${status}/${experiment}/${simulation}/${DIR}/${OUT}/SE_50Y/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
              ]


# Next command will lead to explore all directories in 'urls_IGCM_OUT_old'
# for searching data for a CliMAF dataset (by function ds) except if 
# a more specific dataloc entry matches the arguments to 'ds'
dataloc(project="IGCM_OUT_old", organization="generic", url=urls_IGCM_OUT_old)

# OCE
calias("IGCM_OUT_old", 'tos'     ,'sosstsst' , offset=273.15   ,filenameVar='grid_T')
calias("IGCM_OUT_old", 'sos'     ,'sosaline'                   ,filenameVar='grid_T')
calias("IGCM_OUT_old", 'to'      ,'thetao'   , offset=273.15   ,filenameVar='grid_T')
calias("IGCM_OUT_old", 'so'      ,'vosaline'                   ,filenameVar='grid_T')
calias("IGCM_OUT_old", 'zos'     ,'sossheig'                   ,filenameVar='grid_T')
calias("IGCM_OUT_old", 'mlotst'  ,'somxl010'                   ,filenameVar='grid_T')
calias("IGCM_OUT_old", 'hc300'   ,'sohtc300' , scale=1.E-9     ,filenameVar='grid_T')

# ICE
calias("IGCM_OUT_old", 'sic',    'soicecov',   scale=100 ,filenameVar="grid_T") 

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
calias("IGCM_OUT_old", 'ta'   ,'ta'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'ua'   ,'ua'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'va'   ,'va'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'zg'   ,'zg'    ,filenameVar='histmthNMC')
calias("IGCM_OUT_old", 'hus'  ,'hus'   ,filenameVar='histmthNMC')


# -> Turbulent fluxes
calias("IGCM_OUT_old", 'hfls'   ,'flat' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT_old", 'hfss'   ,'sens' , scale=-1 ,filenameVar='histmth')
calias("IGCM_OUT_old", 'tauu'   ,'taux'  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'tauv'   ,'tauy'  ,filenameVar='histmth')

# -> Clouds
calias("IGCM_OUT_old", 'clt'   ,'cldt'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_old", 'cldl'  ,'cldl'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_old", 'cldm'  ,'cldm'  , scale=100, filenameVar='histmth')
calias("IGCM_OUT_old", 'cldh'  ,'cldh'  , scale=100, filenameVar='histmth')

# -> Clouds radiative forcing
calias("IGCM_OUT_old", 'rlwcrf'   ,''  ,filenameVar='histmth')
calias("IGCM_OUT_old", 'rswcrf'   ,''  ,filenameVar='histmth')

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


