ccdftransport : computes the transports accross a section
-----------------------------------------------------------

Computes the transports accross a section. This is the wrapping around
the native cdftransport operator assuming its usage is:: 
 
 cdftransport **[-test  u v ]** [-noheat ] [-plus_minus ] [-obc] 
 ... [VT-file] U-file V-file **[-full]**   
 ... **[-time jt ]** **[-zlimit limits of level]** 

CliMAF optional arguments are the ones surrounded with '**'.

Only the case where VT files (netcdf file with mean values of vt, vs,
ut, us for heat and salt transport) must be given is treated. Indeed,
cdftools cdftransport operator have '-noheat', '-plus_minus' and
'-obc' options. If these options are used, VT files must be
omitted. Here, only the case where VT files must be given is treated
so this options are not considered.   

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping 

**Inputs** (in the order of CliMAF call): 6 datasets

  - a dataset with mean values of vt for heat and salt transport [VT-file]
  - a dataset with mean values of vs for heat and salt transport [VT-file]
  - a dataset with mean values of ut for heat and salt transport [VT-file]
  - a dataset with mean values of us for heat and salt transport [VT-file]
  - a dataset with the zonal velocity component [U-file]
  - a dataset with the meridional velocity component [V-file] 
    
**Mandatory arguments**: None

**Optional arguments**:

  - ``imin``, ``imax``, ``jmin``, ``jmax``,  ``kmin``, ``kmax`` :
    spatial windows where the transports are computed 

  - ``opt1`` : may be used to pass key ``-test u v`` (use constant the
    u and v velocity components for sign test purpose) 

  - ``opt2`` may be used to pass following keys (corresponding to the
    optional arguments used after the file names in the native
    cdftransport operator): 

    - ``-full`` : use for full step configurations

    - ``-time jt`` : compute transports for time index jt. Default
      is 1. 

    - ``-zlimit list of depth`` : specify depths limits defining
      layers where the transports will be computed. If not used, the
      transports are computed for the whole water column. If used,
      this option must be the last on the command line.

**Required files**: Files mesh_hgr.nc, mesh_zgr.nc must be in the
current directory (use function 'fixed_fields' for that; see example
below). 

**Outputs**:

  - main output : a netcdf file for volume transport (variable : vtrp)
  - secondary outputs and their names :
     - ``htrp`` : field heat transport
     - ``strp`` : field salt transport

**Climaf call example**:: 

  >>> # Use "NEMO" project, where VT files (netcdf file with mean
  >>> # values of vt, vs, ut, us for heat and salt transport) are defined
  >>> cdef("project","NEMO")
  >>> # How to get required files for cdftools cdftransport binary
  >>> fixed_fields('ccdftransport',
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
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
calls a binary using cdftools cdftransport operator.
    
**Shortcomings**:
 - computes only one section by launch
