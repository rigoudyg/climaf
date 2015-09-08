ccdfvar : computes the spatial variance of field (2D or 3D)
---------------------------------------------------------------

Computes the spatial variance of a 2D or 3D field. This is the wrapping
around the native cdfmean operator assuming its usage is:: 

 cdfmean  IN-file IN-var T|U|V|F|W **[imin imax jmin jmax kmin kmax]** 
 ... **[-full]** [-var] [-zeromean]

CliMAF optional arguments are the ones surrounded with '**'.

If a spatial window is specified, the spatial variance is computed
only in this window. See also:

  - :doc:`ccdfvar_profile <ccdfvar_profile>` for getting a vertical
    profile of spatial variance for each level for 3D fields 

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call):

  - any dataset (but only one)

**Mandatory argument**: 

  - ``pos_grid`` : position of cdfvar on the C-grid : T|U|V|F|W
  
**Optional arguments**:

  - ``imin``, ``imax``, ``jmin``, ``jmax``,  ``kmin``, ``kmax`` : for
    defining spatial windows 

  - ``opt`` : may be used to pass key ``-full`` (compute the mean for
    full steps, instead of default partial steps)

  
**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc must be in
the current directory (use function :py:func:`~climaf.operators.fixed_fields()` for that; see
example below).  

**Outputs**:

  - main output : a netcdf file (variable : var_3D_cdfvar)

**Climaf call example**:: 

  >>> # How to get required files for cdftools cdfmean binary
  >>> fixed_fields('ccdfvar',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # some dataset, with whatever variable
  >>> my_cdfvar=ccdfvar(d1,pos_grid='U')
  >>> cfile(my_cdfvar) # to compute the spatial variance and get a filename with the result 

  >>> my_cdfvar2=ccdfvar(d1,pos_grid='U',opt='-full')
  >>> cfile(my_cdfvar2)

  >>> my_cdfvar3=ccdfvar(d1,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
  >>> cfile(my_cdfvar3)

**Implementation**: The operator is implemented as a binary using
cdftools cdfmean operator.  
