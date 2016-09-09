ccdfmean_profile_box : computes the vertical profile of horizontal means for 3D fields on a given geographical domain
-----------------------------------------------------------------------------------------------------------------------

Computes the vertical profile of horizontal means for 3D fields on a
domain given as a geographical window (instead of i, j space). This is
the wrapping around the native cdfmean and cdffindij operators
assuming their usage are::   

 cdfmean  IN-file IN-var T|U|V|F|W **[imin imax jmin jmax kmin kmax]** 
 ... **[-full]** [-var] [-zeromean]

 cdffindij  xmin xmax ymin ymax  [-c COOR-file] [-p point_type]

CliMAF optional arguments are the ones surrounded with '**'.

See also:

 - :doc:`ccdfmean_profile <ccdfmean_profile>` for getting a horizontal
   mean for each level for 3D fields (if a spatial window is
   specified, the mean value is computed only in this window - in this
   case, spatial window is specified in index). 

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call):

  - any dataset (but only one)

**Mandatory argument**: 

  - ``pos_grid`` : position of cdfvar on the C-grid : T|U|V|F|W
  
  - ``lonmin``, ``lonmax``, ``latmin``, ``latmax`` : geographical
    limits of the window 

**Optional arguments**:

  - ``kmin``, ``kmax`` : for defining levels

  - ``opt`` : may be used to pass key ``-full`` (compute the mean for
    full steps, instead of default partial steps)

**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc must be in
the current directory (use function
:py:func:`~climaf.operators.fixed_fields()` for that; see example
below). 

**Outputs**:

  - main output : a netcdf file (variable : mean_cdfvar)

**Climaf call example**:: For more examples which are systematically
tested, see :download:`cdftools.py <../../examples/cdftools.py>`  

  >>> # How to get required files for cdftools cdfmean and cdffindij binaries
  >>> fixed_fields('ccdfmean_profile_box',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # some dataset, with whatever variable 
  >>> my_cdfmean_prof_box=ccdfmean_profile_box(duo,pos_grid='U',latmin=35.4,latmax=39,lonmin=-14,lonmax=-10)
  >>> cfile(my_cdfmean_prof_box)  # to compute the vertical profile of horizontal means on domain [35.4,39,-14,-10] and get a filename with the result 

  >>> my_cdfmean_prof_box2=ccdfmean_profile_box(duo,pos_grid='U',opt='-full',latmin=35.4,latmax=39,lonmin=-14,lonmax=-10)
  >>> cfile(my_cdfmean_prof_box2)

  >>> my_cdfmean_prof_box3=ccdfmean_profile_box(duo,pos_grid='U',latmin=35.4,latmax=39,lonmin=-14,lonmax=-10,kmin=1,kmax=2)
  >>> cfile(my_cdfmean_prof_box3)

**Implementation**: The operator is implemented as a binary using
cdftools cdfmean and cdffindij operators. 
