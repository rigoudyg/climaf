ccdfstdmoy : computes the the standard deviation and mean value of any variable
--------------------------------------------------------------------------------

Computes the standard deviation and mean value of any variable. This
computation is direct and does not required a pre-processing with any
of the cdfmoy tools. Only the standard deviation of the variable is
given using 'ccdfstd'. 

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call): 

  - any dataset forming a time-series (but only one)

**Mandatory arguments**: None

**Optional arguments**:

  - ``-spval0`` : set missing_value attribute to 0 for all output
    variables and take care of the input missing_value. This option is
    usefull if missing_values differ from files to files (use by
    opt='-spval0').   
  - ``-nomissincl`` : with this option, the output std and mean are
    set to missing value at any gridpoint where the variable contains
    a missing value for at least one timestep. You should combine
    with -spval0 if missing values are not 0 in all the input files
    (use by opt='-nomissincl').  
  - ``-stdopt`` : use a  more optimal algorithm to compute std and std
    is unbiased (use by opt='-stdopt').

**Required files**: None

**Outputs**:

  - main output : a netcdf file for standard deviation (variable :
    IN-var_std, same units than input variables)  
  - secondary outputs and their names :
     - ``moy`` : field mean value (variable: IN-var, same units than input variables)

**Climaf call example**::

  >>> from climaf.api import *
  >>> cdef("frequency","monthly") 
  >>> cdef("project","EM")
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # some dataset, with whatever variable
  >>> my_cdfstd_moy=ccdfstdmoy(d1)
  >>> cfile(my_cdfstd_moy) # compute the mean value and standard deviation of "uo" field (sea water velocity)
  >>> moy_var=my_cdfstd_moy.moy # moy_var receives operator output named "moy", namely the field mean value

**Implementation**: The operator is implemented as a binary using
cdfstd cdftools operator. 

**CliMAF call sequence pattern** (for reference)::
  
  >>> 'cdfstd -save ${opt} ${ins}; mv cdfstd.nc ${out}; mv cdfmoy.nc ${out_moy} ; rm -f cdfstd.nc cdfmoy.nc'
