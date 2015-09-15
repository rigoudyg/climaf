ccdfmean_profile : computes the vertical profile of horizontal means for 3D fields
-----------------------------------------------------------------------------------

Computes the vertical profile of horizontal means for 3D fields. This
is the wrapping around the native cdfmean operator assuming its usage
is::  

 cdfmean  IN-file IN-var T|U|V|F|W **[imin imax jmin jmax kmin kmax]** 
 ... **[-full]** [-var] [-zeromean]

CliMAF optional arguments are the ones surrounded with '**'.

If a spatial window is specified, the vertical profile is computed
only in this window. See also:

  - :doc:`ccdfvar_profile <ccdfvar_profile>` for getting a vertical
    profile of spatial variance of the variable

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

  - main output : a netcdf file (variable : mean_cdfvar)

**Climaf call example**:: 

  >>> # How to get required files for cdftools cdfmean binary
  >>> fixed_fields('ccdfmean_profile',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # some dataset, with whatever variable 
  >>> my_cdfmean_prof=ccdfmean_profile(duo,pos_grid='U')
  >>> cfile(my_cdfmean_prof)  # to compute the vertical profile of horizontal means and get a filename with the result 

  >>> my_cdfmean_prof2=ccdfmean_profile(duo,pos_grid='U',opt='-full')
  >>> cfile(my_cdfmean_prof2)

  >>> my_cdfmean_prof3=ccdfmean_profile(duo,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
  >>> cfile(my_cdfmean_prof3)

**Implementation**: The operator is implemented as a binary using
cdftools cdfmean operator.
