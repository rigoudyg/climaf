ccdftransport : computes the transports accross a section
-----------------------------------------------------------

Computes the transports accross a section. Only the case where VT
files (netcdf file with mean values of vt, vs, ut, us for heat and
salt transport) must be given is treated.  

Indeed, cdftransport CDFTools operator have '-noheat', '-plus_minus'
and '-obc' options. If these options are used, VT files must be
omitted. Here, only the case where VT files must be given is treated
so this options are not considered.  

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call): 6 datasets

  - a dataset with mean values of vt for heat and salt transport ([VT-file])
  - a dataset with mean values of vs for heat and salt transport ([VT-file])
  - a dataset with mean values of ut for heat and salt transport ([VT-file])
  - a dataset with mean values of us for heat and salt transport ([VT-file])
  - a dataset with the zonal velocity component ([U-file])
  - a dataset with the meridional velocity component ([V-file]) 
    
**Mandatory arguments**: None

**Optional arguments**:

  - ``imin``, ``imax``, ``jmin``, ``jmax``,  ``kmin``, ``kmax`` :
    spatial windows where the transports are computed (use by imin=...,
    imax=..., etc) 
  - ``-test u v`` : use constant the u and v velocity components for
    sign test purpose (use by opt1='-test u v', defined by 'opt1'
    because must be used before the file names) 
  - ``-full`` : use for full step configurations (use by opt2='-full',
    defined by 'opt2' because must be used after the file names)
  - ``-time jt`` : compute transports for time index jt. Default
    is 1. (use by opt2='-time jt', defined by 'opt2' because must be
    used after the file names) 
  - ``-zlimit list of depth`` : Specify depths limits defining layers
    where the transports will be computed. If not used, the transports
    are computed for the whole water column. If used, this option must
    be the last on the command line. (use by opt2='-zlimit list of
    depth', defined by 'opt2' because must be used after the file
    names)  

**Required files**: Files mesh_hgr.nc, mesh_zgr.nc must be in the
current directory. 

**Outputs**:

  - main output : a netcdf file for volume transport (variable : vtrp)
  - secondary outputs and their names :
     - ``htrp`` : field heat transport
     - ``strp`` : field salt transport

**Climaf call example**::

  >>> from climaf.api import *
  >>> from climaf.operators import fixed_fields
  >>> cdef("frequency","monthly") 
  >>> # Use "NEMO" project, where VT files (netcdf file with mean
  >>> # values of vt, vs, ut, us for heat and salt transport) are defined
  >>> cdef("project","NEMO")
  >>> # How to get required files for cdftransport cdftools binary
  >>> tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
  >>> lpath='/cnrm/aster/data3/aster/vignonl/code/climaf/'
  >>> fixed_fields('ccdftransport',
             target=[tpath+'ORCA1_mesh_hgr.nc',tpath+'ORCA1_mesh_zgr.nc'],
             link=[lpath+'mesh_hgr.nc',lpath+'mesh_zgr.nc'] 
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="vomevt", period="199807",grid='VT') # dataset with vt
  >>> d2=ds(simulation="PRE6CPLCr2alb", variable="vomevs", period="199807",grid='VT') # dataset with vs
  >>> d3=ds(simulation="PRE6CPLCr2alb", variable="vozout", period="199807",grid='VT') # dataset with ut
  >>> d4=ds(simulation="PRE6CPLCr2alb", variable="vozous", period="199807",grid='VT') # dataset with us
  >>> d5=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807",grid='grid_U',table='table2.3') # dataset with zonal velocity component
  >>> d6=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807",grid='grid_V',table='table2.3') # dataset with meridional velocity component
  >>> my_cdftransport=ccdftransport(d1,d2,d3,d4,d5,d6,imin=117,imax=117,jmin=145,jmax=147,opt1='-test u v',opt2='-full')
  >>> cfile(my_cdftransport) # computes the transports accross specified section
  >>> htrp_var=my_cdftransport.htrp # htrp_var receives operator output named "htrp", namely the field heat transport
  >>> strp_var=my_cdftransport.strp # strp_var receives operator output named "strp", namely the field salt transport

**Implementation**: The operator is implemented as a script which
calls a binary using cdftransport cdftools operator.

**CliMAF call sequence pattern** (for reference)::
  
  >>> scriptpath+'cdftransport.sh ${in_1} ${in_2} ${in_3} ${in_4} ${in_5} ${in_6} ${imin} ${imax} ${jmin} ${jmax} "${opt1}" "${opt2}" ${out} ${out_htrp} ${out_strp}'
    
**Shortcomings**:
 - computes only one section by launch
