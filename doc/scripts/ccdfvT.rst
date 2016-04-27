ccdfvT : computes the time average values for V.T, V.S, U.T and U.S 
--------------------------------------------------------------------

Computes the time average values for second order products V.T, V.S,
U.T and U.S used in heat and salt transport computation. This is the
wrapping around a modified version of the native cdfvT operator
(adapted to set 4 files with only one variable in input) assuming its
usage is::     

 cdfvT T-file S-file U-file V-file [-o output_file ] [-nc4 ]
 ... 'list_of_tags'  

There are not CliMAF optional arguments.

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call): 4 datasets

  - a dataset with temperature [T-file]
  - a dataset with salinity [S-file]
  - a dataset with zonal velocity component [U-file]
  - a dataset with meridional velocity component [V-file]

**Mandatory arguments**: None

**Optional arguments**: None
      
**Required files**: None

**Outputs**:

  - main output : a netcdf file (variables : vozout, vozous, vomevt and vomevs)

**Climaf call example**:: For more examples which are systematically
tested, see :download:`cdftools.py <../../examples/cdftools.py>` and
:download:`cdftransport.py <../../examples/cdftransport.py>` 

  >>> cdef("period","198807")
  >>> dt=ds(simulation="PRE6CPLCr2alb", variable="thetao", realm="O") # dataset with temperature
  >>> ds=ds(simulation="PRE6CPLCr2alb", variable="so", realm="O") # dataset with salinity
  >>> du=ds(simulation="PRE6CPLCr2alb", variable="uo", realm="O") # dataset with zonal velocity component
  >>> dv=ds(simulation="PRE6CPLCr2alb", variable="vo", realm="O") # dataset with meridional velocity component
  >>> my_cdfvT=ccdfvT(dt,ds,du,dv)
  >>> cfile(my_cdfvT) # to compute the time average values for V.T, V.S, U.T and U.S 

**Implementation**: The operator is implemented as a binary using
cdftools cdfvT operator.  

