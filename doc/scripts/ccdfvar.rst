ccdfvar : computes the spatial variance of field (2D or 3D)
---------------------------------------------------------------

Computes the spatial variance of 2D or 3D field. If a spatial window
is specified, the spatial variance is computed only in this
window. For 3D fields, a vertical profile of spatial variance for each
level is given using 'ccdfvar_profile'.

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - any dataset (but only one)

**Mandatory arguments**: 

  - ``var`` : name of netcdf variable to work with
  - ``pos_grid`` : position of cdfvar on the C-grid : T|U|V|F|W
  
**Optional arguments**:

  - ``imin``, ``imax``, ``jmin``, ``jmax``,  ``kmin``, ``kmax`` :
    spatial windows where mean value is computed (use by imin=...,
    imax=..., etc) : 

    - if imin = 0 then ALL i are taken
    - if jmin = 0 then ALL j are taken
    - if kmin = 0 then ALL k are taken
  - ``-full`` : compute the mean for full steps, instead of default
    partial steps (use by opt='-full')

**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc must be in
the current directory. 

**Outputs**:

  - main output : a netcdf file (variable : var_3D_cdfvar)

**Climaf call example**::

  >>> from climaf.api import *
  >>> from climaf.operators import fixed_fields
  >>> cdef("frequency","monthly") 
  >>> cdef("project","EM")
  >>> # How to get required files for cdfmean cdftools binary
  >>> tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
  >>> lpath='/cnrm/aster/data3/aster/vignonl/code/climaf/'
  >>> fixed_fields('ccdfmean',
             target=[tpath+'ORCA1_mesh_mask.nc',tpath+'ORCA1_mesh_hgr.nc',tpath+'ORCA1_mesh_zgr.nc'],
             link=[lpath+'mask.nc',lpath+'mesh_hgr.nc',lpath+'mesh_zgr.nc'])
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # some dataset, with whatever variable
  >>> my_cdfvar=ccdfvar(d1,pos_grid='U')
  >>> cfile(my_cdfvar) # to compute the spatial variance and get a filename with the result 

  >>> my_cdfvar2=ccdfvar(d1,pos_grid='U',opt='-full')
  >>> cfile(my_cdfvar2)

  >>> my_cdfvar3=ccdfvar(d1,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
  >>> cfile(my_cdfvar3)

**Implementation**: The operator is implemented as a binary using
cdfmean cdftools operator. 

**CliMAF call sequence pattern** (for reference)::
  
  >>> 'cdfmean ${in} ${var} ${pos_grid} ${imin} ${imax} ${jmin} ${jmax} ${kmin} ${kmax} -var ${opt}; ncks -O -x -v mean_${var},mean_3D${var},var_${var} cdfmean.nc ${out}; rm -f cdfmean.nc cdfmean.txt cdfvar.txt'       
