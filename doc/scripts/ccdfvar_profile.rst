ccdfvar_profile : computes the vertical profile of spatial variance for 3D fields
-----------------------------------------------------------------------------------

Computes the vertical profile of spatial variance for 3D fields. This
is the wrapping around the native cdfmean operator assuming its usage
is::  

 cdfmean  IN-file IN-var T|U|V|F|W **[imin imax jmin jmax kmin kmax]** 
 ... **[-full]** [-var] [-zeromean]

CliMAF optional arguments are the ones surrounded with '**'.

If a spatial window is specified, the vertical profile is computed
only in this window. 

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
the current directory(use function :py:func:`~climaf.operators.fixed_fields()` for that; see
example below). 

**Outputs**:

  - main output : a netcdf file (variable : var_cdfvar)

**Climaf call example**:: For more examples which are systematically
tested, see :download:`cdftools.py <../../examples/cdftools.py>`  

  >>> # How to get required files for cdftools cdfmean binary
  >>> fixed_fields('ccdfvar_profile',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # some dataset, with whatever variable
  >>> my_cdfvar_prof=ccdfvar_profile(duo,pos_grid='U')
  >>> cfile(my_cdfvar_prof) # to compute the vertical profile of spatial variance and get a filename with the result 

  >>> my_cdfvar_prof2=ccdfvar_profile(duo,pos_grid='U',opt='-full')
  >>> cfile(my_cdfvar_prof2)

  >>> my_cdfvar_prof3=ccdfvar_profile(duo,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
  >>> cfile(my_cdfvar_prof3)

**Implementation**: The operator is implemented as a binary using
cdftools cdfmean operator. 

