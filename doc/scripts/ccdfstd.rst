ccdfstd : computes the standard deviation of any variable
-----------------------------------------------------------

Computes the standard deviation of any variable. This computation is
direct and does not required a pre-processing with any of the cdfmoy
tools. The mean value of the field is also given using 'ccdfstdmoy'.  

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

  - main output : a netcdf file (variable : IN-var_std, same units
    than input variables) 

**Climaf call example**::

  >>> from climaf.api import *
  >>> cdef("frequency","monthly") 
  >>> cdef("project","EM")
  >>> d1=ds(simulation="PRE6CPLCr2alb", variable="omlmax", period="199807-199810", realm="O") # some dataset, with whatever variable
  >>> my_cdfstd=ccdfstd(d1)
  >>> cfile(my_cdfstd) # to compute the standard deviation of variable "omlmax"

  >>> my_cdfstd2=ccdfstd(d1,opt='-full')
  >>> cfile(my_cdfstd2)

**Implementation**: The operator is implemented as a binary using
cdfstd cdftools operator. 

**CliMAF call sequence pattern** (for reference)::
  
  >>> 'cdfstd ${opt} ${ins}; mv cdfstd.nc ${out}; rm -f cdfstd.nc'
