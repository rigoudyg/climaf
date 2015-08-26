ccdfmxlheatc : computes the heat content in the mixed layer 
--------------------------------------------------------------

Computes the heat content in the mixed layer (Joules/m2). This is the
wrapping around the native cdfmxlheatc operator assuming its usage
is:: 

 cdfmxlheatc T-file **[-full]**

CliMAF optional argument is the only argument available, surrounded
with '**'. 

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call): 

  - a dataset with temperature (gridT)
  - a dataset with mld (gridT)

**Mandatory arguments**: None

**Optional argument**:

  - ``opt`` : may be used to pass key ``-full`` (for full step
    configurations, default is partial step)    

**Required files**: Files mesh_zgr.nc, mask.nc must be in the current
directory (use function 'fixed_fields' for that; see example below).   

**Outputs**:

  - main output : a netcdf file (variable : somxlheatc (Joules/m2))

**Climaf call example**:: 

  >>> # How to get required files for cdftools cdfmxlheatc binary
  >>> fixed_fields('ccdfmxlheatc',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") # dataset with temperature
  >>> d2=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807", realm="O") # dataset with mld
  >>> my_cdfmxlheatc=ccdfmxlheatc(d1,d2)
  >>> cfile(my_cdfmxlheatc) # to compute the heat content in the mixed layer and get a filename with the result 

**Implementation**: The operator is implemented as a binary using
cdftools cdfmxlheatc operator.  
