#!/usr/bin/python
# -*- coding: utf-8 -*-

from climaf.api import *

if not atCNRM: exit(0)
if 'ccdfmean' not in cscripts :
    print("CDFtools not available")
    exit(0)

# Declare "data_CNRM" project, both for Nemo raw outputs and for Monitoring outputs
# (with VT-files : mean values of vt, vs, ut, us for heat and salt transport)
#
cproject('data_CNRM')

# For 'standard' Nemo output files (actually, they are easier accessible using project "EM")
#root1="/cnrm/est/USERS/senesi/NO_SAVE/expes/PRE6/${simulation}/O/"
root1="/cnrm/est/COMMON/climaf/test_data/${simulation}/O/"
suffix="${simulation}_1m_YYYYMMDD_YYYYMMDD_${variable}.nc"
url_nemo_standard=root1+suffix

# For VT files from Monitoring
#root2="/cnrm/ioga/Users/chevallier/chevalli/Monitoring/Results/NO_SAVE/PRE6/SORTIE/PRE6/${simulation}/MONITOR/VT/"
root2="/cnrm/est/COMMON/climaf/test_data/${simulation}/VT/"
url_nemo_monitoring=root2+suffix
#
dataloc(project='data_CNRM', organization='generic', url=[url_nemo_standard,url_nemo_monitoring])
#
# Declare how variables are scattered/grouped among files
# (and with mixed variable names conventions - CNRM and  MONITORING)
calias("data_CNRM","uo",filenameVar="grid_U_table2.3")
calias("data_CNRM","vo",filenameVar="grid_V_table2.3")
calias("data_CNRM","so,thetao",filenameVar="grid_T_table2.2")

# Declare a special variable, composed of variables grouped in a file
products="vomevt,vomevs,vozout,vozous"
calias("data_CNRM",products,filenameVar="VT")

# Define defaults facets for datasets
cdef("project","data_CNRM")
cdef("frequency","monthly")
cdef("simulation","PRE6CPLCr2alb")
cdef("period","199808-199809")

# Define datasets
duo=ds(variable="uo")
dvo=ds(variable="vo")
dx=ds(variable=products)

# Tell how to bring required fixed files to cdftransport
# (this can use wildcards ${model}, ${project}, ${simulation}, ${realm})
#tpath='/cnrm/ioga/Users/chevallier/chevalli/Monitoring/MONITORING_v3.1/config/'
tpath='/cnrm/est/COMMON/climaf/test_data/fixed/'
fixed_fields('ccdftransport',
             ('mesh_hgr.nc',tpath+'ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',tpath+'ORCA1_mesh_zgr.nc'))

# Compute transport
trsp=ccdftransport(dx,duo,dvo,imin=117,imax=117,jmin=145,jmax=147)

# Create files for the various cdftransport outputs
cfile(trsp) #main output is mass transport
cfile(trsp.htrp)
cfile(trsp.strp)

# Compute products another way, and transport
dso=ds(variable="so")
dtho=ds(variable="thetao")
dx2=ccdfvT(dtho,dso,duo,dvo)
trsp2=ccdftransport(dx2,duo,dvo,imin=117,imax=117,jmin=145,jmax=147)
cfile(trsp2)

# Bonus : an alternate way deal with multivariable : how to extract a
# single variable from a multi-variable dataset
dut=ccdo(dx,operator="selname,vozout")
cfile(dut)

