ccdfsaltc : computes the salt content in the specified area
------------------------------------------------------------

Computes the salt content in the specified area (Joules). A sub-domain
can be specified in option. This is the wrapping around the new
cdfsaltc operator assuming its usage is::  
 
 cdfsaltc  T-file ...
 ... **[imin imax jmin jmax kmin kmax]** **[-full]**

CliMAF optional arguments are the ones surrounded with '**'.

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot for the wrapping

**Inputs** (in the order of CliMAF call): 

  - a dataset with salinity [T-file]

**Mandatory arguments**: None

**Optional arguments**:

  - ``imin``, ``imax``, ``jmin``, ``jmax``,  ``kmin``, ``kmax`` :
    limit of a sub domain where the salt content will be calculated
   
  - ``opt`` : may be used to pass key ``-full`` (assume full step
    model output instead of default partial steps)
       
**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc must be in
the current directory (use function :py:func:`~climaf.operators.fixed_fields()` for that; see
example below). 

**Outputs**:

  - main output : a netcdf file (variables : saltc_2D, saltc_3D) and
    standard output

**Climaf call example**:: For more examples which are systematically
tested, see :download:`cdftools.py <../../examples/cdftools.py>`  

  >>> # Use "data_CNRM" project, where netcdf files with 'so'values are defined
  >>> cdef("project","data_CNRM")
  >>> # How to get required files for cdftools cdfsaltc binary
  >>> fixed_fields('ccdfsaltc',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> dso=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O")
  >>> my_cdfsaltc=ccdfsaltc(dso,imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2,opt='-full')
  >>> cfile(my_cdfsaltc) # to compute the salt content in the specified area 

**Implementation**: The operator is implemented as a binary using the
new cdftools cdfsaltc operator.  
