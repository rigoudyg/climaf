"""
This module declares locations for searching data for IGCM outputs produced by libIGCM for all frequencies, and where the data is
at IPSL and on Ciclad

Attributes for CMIP5 datasets are : model, rip, frequency, table, realm, version

Syntax for these attributes is described in `the CMIP5 DRS document <http://cmip-pcmdi.llnl.gov/cmip5/docs/cmip5_data_reference_syntax.pdf>`_

Example for an IGCM_OUT dataset declaration ::

 >>> tas1pc=ds(project='IGCM_OUT', model='IPSLCM6', experiment='piControl', variable='tas', frequency='monthly', period='1860-1861')


"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad

# Rajouter login et disk (ou filesystem) = scratch/store/work

# ajouter realm? atmos -> ATM; ocean -> OCE
root = None
if atTGCC:
   # Declare a list of root directories for IPSL data at TGCC
   root="/ccc/store/cont003/dsm"
if onCiclad :
   # Declare a list of root directories for CMIP5 data on IPSL's Ciclad file system
   root="/data/jservon/IPSL_DATA/SIMULATIONS"


p=cproject("IGCM_OUT", "clim_period", "model", "simulation", "variable", "frequency", "experiment", "OUT", "DIR", "login", "period", "root", ensemble=["model","simulation"], separator="%")

cdef('root',        root,         project='IGCM_OUT')
cdef('clim_period', '????_????',  project='IGCM_OUT')
cdef('model',       '*',          project='IGCM_OUT')
cdef('simulation',  '*',          project='IGCM_OUT')
cdef('variable',    '*',          project='IGCM_OUT')
cdef('frequency',   'monthly',    project='IGCM_OUT')
cdef('experiment',  '*',          project='IGCM_OUT')
cdef('OUT',         '*',          project='IGCM_OUT')
cdef('DIR',         '*',          project='IGCM_OUT')
cdef('login',       '*',          project='IGCM_OUT')
cdef('period',      '0001-3000',  project='IGCM_OUT')


# Frequency alias
cfreqs('IGCM_OUT', {'monthly':'1M' , 'daily':'1D' , 'seasonal':'SE', 'annual_cycle':'SE'})

urls_IGCM_OUT=[
              "/${root}/${login}/IGCM_OUT/${model}/*/${experiment}/${simulation}/${DIR}/${OUT}/*/${simulation}_YYYYMMDD_YYYYMMDD_${frequency}_${variable}.nc",
	      "/${root}/${login}/IGCM_OUT/${model}/*/${experiment}/${simulation}/${DIR}/${OUT}/${frequency}/${simulation}_${frequency}_${clim_period}_1M_${variable}.nc"
              ]


# Next command will lead to explore all directories in 'urls_IGCM_OUT'
# for searching data for a CliMAF dataset (by function ds) except if 
# a more specific dataloc entry matches the arguments to 'ds'
dataloc(project="IGCM_OUT", organization="generic", url=urls_IGCM_OUT)

# OCE
calias("IGCM_OUT", 'tos'     ,'tos'                ,filenameVar='grid_T')
calias("IGCM_OUT", 'sos'     ,'sos'                ,filenameVar='grid_T')
calias("IGCM_OUT", 'to'      ,'thetao'             ,filenameVar='grid_T')
calias("IGCM_OUT", 'so'      ,'so'                 ,filenameVar='grid_T')
calias("IGCM_OUT", 'zos'     ,'zos'                ,filenameVar='grid_T')
calias("IGCM_OUT", 'mlotst'  ,'mldr10_1'           ,filenameVar='grid_T')

# ICE
calias("IGCM_OUT", 'sic',    'siconc',   scale=100 ,filenameVar="ICE") 

# ATM
calias("IGCM_OUT", 'pr'   ,'precip' ,filenameVar='histmth')
calias("IGCM_OUT", 'psl'  ,'slp'    ,filenameVar='histmth')
calias("IGCM_OUT", 'tas'  ,'tas'    ,filenameVar='histmth')
calias("IGCM_OUT", 'tas'  ,'t2m'    ,filenameVar='histmth')
calias("IGCM_OUT", 'uas'  ,'uas'    ,filenameVar='histmth')
calias("IGCM_OUT", 'vas'  ,'vas'    ,filenameVar='histmth')
calias("IGCM_OUT", 'ua'   ,'ua'     ,filenameVar='histmthNMC')
calias("IGCM_OUT", 'va'   ,'va'     ,filenameVar='histmthNMC')


