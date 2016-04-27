ccdfzonalmean : compute the global zonal mean of the given variable 
---------------------------------------------------------------------

Compute the zonal mean of the given variable from the input
file. Zonal mean is in fact the mean value computed along the I
coordinate. The result is a vertical slice, in the meridional
direction. 
       
This is the wrapping around the native cdfzonalmean operator
assuming its usage is:: 

 cdfzonalmean IN-file point_type [ BASIN-file] **[-debug]**
 ... [-var var1,var2,..] [-max ] **[-pdep | --positive_depths]
 [-ndep_in ]** 

CliMAF optional arguments are the ones between '**'

See also :doc:`ccdfzonalmean_bas <ccdfzonalmean_bas>` for getting
a zonal mean in a specified sub-basin. 

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call):

  - any dataset (but only one)

**Mandatory argument**: 

  - ``point_type`` : indicate the location on C-grid (T|U|V|F|W)
  
**Optional arguments**:

  - ``opt`` : may be used to pass keys ``-pdep`` (use positive depths
    in the output file), ``-ndep_in`` (negative depths are used in the
    input file) and/or ``-debug`` (to add some print for debug)

**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc must be in
the current directory (use :py:func:`~climaf.operators.fixed_fields()` for that; see
example below).  

**Outputs**:

  - main output : a netcdf file (variable : zoxxxx_glo, where zo
    replace vo/so prefix of the input variable) 
                     
**Climaf call example**:: For more examples which are systematically
tested, see :download:`cdftools.py <../../examples/cdftools.py>`  

  >>> # How to get required files for Cdftools cdfzonalmean binary
  >>> fixed_fields('ccdfzonalmean',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> # For example, define dataset with meridional velocity component ("vo")
  >>> dvo=ds(simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O")
  >>> my_cdfzmean=ccdfzonalmean(dvo,point_type='V')
  >>> cfile(my_cdfzmean) # to compute the global zonal mean and get a filename with the result   

  >>> my_cdfzmean2=ccdfzonalmean(dvo,point_type='V', opt='-debug -pdep')
  >>> cfile(my_cdfzmean2)

**Implementation**: The operator is implemented as a binary using
cdftools cdfzonalmean operator. 
