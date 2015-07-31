# Example for cdftools cdftransport operator :
# - computes the transports accross a section

#----------------
#  cdftransport
#----------------
#
# CDFtools usage :
# cdftransport [-test  u v ] [-noheat ] [-plus_minus ] [-obc]...
#                   ... [VT-file] U-file V-file [-full] |-time jt] ...
#                   ... [-time jt ] [-zlimit limits of level]
#
# CliMAF usage :
#

from climaf.api import *

if not atCNRM:
    return

# Declare "NEMO" project, where VT-files (netcdf file with mean values
# of vt, vs, ut, us for heat and salt transport) are defined
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
from climaf.site_settings import atCNRM

cproject('NEMO','grid','table',separator='&')

root1="/cnrm/aster/data3/aster/senesi/NO_SAVE/expes/PRE6/PRE6CPLCr2alb/O/PRE6CPLCr2alb_1m_"
root2="/cnrm/aster/data3/aster/chevalli/Monitoring/PRE6/SORTIE/PRE6/PRE6CPLCr2alb/MONITOR/VT/PRE6CPLCr2alb_1m_"
suffix="YYYYMMDD_YYYYMMDD"
url_nemo1=root1+suffix+"_${grid}_${table}.nc"
url_nemo2=root2+suffix+"_${grid}.nc"   #grid='VT'
dataloc(project='NEMO', organization='generic', url=[url_nemo1,url_nemo2])

# Use "NEMO" project
cdef("project","NEMO")
cdef("frequency","monthly")
tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'

# How to get required files for cdftransport
# fixed_fields('ccdftransport',
#             target=[tpath+'ORCA1_mesh_hgr.nc',tpath+'ORCA1_mesh_zgr.nc'],
#             link=[lpath+'mesh_hgr.nc',lpath+'mesh_zgr.nc'])

fixed_fields('ccdftransport',
             ('mask.nc',tpath+'ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',tpath+'ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',tpath+'ORCA1_mesh_zgr.nc'))

# Define dataset with uo ("uo" in .nc <=> "vozocrtx" for cdftools),
# vo ("vo" in .nc <=> "vomecrty" for cdftools), vt (:=vomevt), vs (:=vomevs),
# ut (:=vozout), us (:=vozous) for heat and salt transport
d1=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807",grid='grid_U',table='table2.3')
d2=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807",grid='grid_V',table='table2.3')
d3=ds(simulation="PRE6CPLCr2alb", variable="vomevt", period="199807",grid='VT')
d4=ds(simulation="PRE6CPLCr2alb", variable="vomevs", period="199807",grid='VT')
d5=ds(simulation="PRE6CPLCr2alb", variable="vozout", period="199807",grid='VT')
d6=ds(simulation="PRE6CPLCr2alb", variable="vozous", period="199807",grid='VT')

# Compute the transports accross specified section
my_cdftransport=ccdftransport(d3,d4,d5,d6,d1,d2,imin=117,imax=117,jmin=145,jmax=147,opt2='-full')
cfile(my_cdftransport)
cfile(my_cdftransport.htrp)
cfile(my_cdftransport.strp)

#diff= transports("PRE6CPLCr2alb","199807") - transports("PRE6CPL_toto","199810") 
