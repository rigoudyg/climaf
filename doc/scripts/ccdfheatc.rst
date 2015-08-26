ccdfheatc : computes the heat content in the specified area 
--------------------------------------------------------------

Computes the heat content in the specified area (Joules). A sub-domain
can be specified in option. This is the wrapping around the native
cdfheatc operator assuming its usage is:: 
 
 cdfheatc  T-file ...
 ... **[imin imax jmin jmax kmin kmax]** **[-full]**

CliMAF optional arguments are the ones surrounded with '**'.

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call): 

  - a dataset with salinity [T-file]
  - a dataset with temperature [T-file]

**Mandatory arguments**: None

**Optional arguments**:

  - ``imin``, ``imax``, ``jmin``, ``jmax``,  ``kmin``, ``kmax`` :
    limit of a sub domain where the heat content will be calculated
   
  - ``opt`` : may be used to pass key ``-full`` ( assume full step
    model output instead of default partial steps)
       
**Required files**: Files mesh_hgr.nc, mesh_zgr.nc, mask.nc must be in
the current directory (use function 'fixed_fields' for that; see
example below). 

**Outputs**:

  - main output : standard output

**Climaf call example**:: 

  >>> # How to get required files for cdftools cdfheatc binary
  >>> fixed_fields('ccdfheatc',
   ... ('mask.nc',    '/data/climaf/${project}/${model}/ORCA1_mesh_mask.nc'),
   ... ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
   ... ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="so", period="199807", realm="O") # dataset with salinity
  >>> d2=ds(simulation="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O") # dataset with temperature
  >>> my_cdfheatc=ccdfheatc(d1,d2,imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2,opt='-full')
  >>> cfile(my_cdfheatc) # to compute the heat content in the specified area and get the result on standard output

**Implementation**: The operator is implemented as a binary using
cdftools cdfheatc operator.  

