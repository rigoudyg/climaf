ccdfzonalmean_bas : compute the zonal mean of the given variable in a specified sub-basin
-------------------------------------------------------------------------------------------

Compute the zonal mean of the given variable in a specified sub-basin
from the input file. Zonal mean is in fact the mean value computed
along the I coordinate. The result is a vertical slice, in the
meridional direction.  
       
This is the wrapping around the native cdfzonalmean operator
assuming its usage is:: 

 cdfzonalmean IN-file point_type [ BASIN-file] **[-debug]**
 ... [-var var1,var2,..] [-max ] **[-pdep | --positive_depths]
 [-ndep_in ]** 

CliMAF optional arguments are the ones between '**'

See also :doc:`ccdfzonalmean <ccdfzonalmean>` for getting the global
zonal mean. 

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call):

  - any dataset (but only one)

**Mandatory argument**: 

  - ``point_type`` : indicate the location on C-grid (T|U|V|F|W)
  - ``basin`` : sub-basin where zonal mean will be computed

**Optional arguments**:

  - ``opt`` : may be used to pass keys ``-pdep`` (use positive depths
    in the output file), ``-ndep_in`` (negative depths are used in the
    input file) and/or ``-debug`` (to add some print for debug)

**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc and
new_maskglo.nc (netcdf file describing sub basins) must be in the
current directory (use :py:func:`~climaf.operators.fixed_fields()` for
that; see example below).  

**Outputs**:

  - main output : a netcdf file (variable : zoxxxx_bas, where zo
    replace vo/so prefix of the input variable and where bas is a
    suffix for the specified sub-basin)  
                     
**Climaf call example**:: For more examples which are systematically
tested, see :download:`cdftools.py <../../examples/cdftools.py>`  

  >>> # How to get required files for Cdftools cdfzonalmean binary
  >>> fixed_fields('ccdfzonalmean_bas',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'),
   ... ('new_maskglo.nc','/data/climaf/${project}/${model}/ORCA1_new_maskglo.nc'))
  >>> # For example, define dataset with ocean mass component ("vmo") for period "1998"
  >>> dvmo=ds(simulation="PRE6CPLCr2alb", variable="vmo", period="1998", realm="O")
  >>> # Compute the zonal mean of "vmo" in sub-basin 'atl' and get a filename with the result   
  >>> my_cdfzmean_bas=ccdfzonalmean_bas(dvmo,point_type='V',basin='atl')
  >>> cfile(my_cdfzmean_bas) 
  >>> # Plot result
  >>> plot_mycdfzmean_bas=plot(my_cdfzmean_bas,title='Zonal mean in sub-basin atl')
  >>> cshow(plot_mycdfzmean_bas)

**Implementation**: The operator is implemented as a binary using
cdftools cdfzonalmean operator. 
