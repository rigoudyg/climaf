ccdfstdmoy : computes the standard deviation and mean value of any variable
--------------------------------------------------------------------------------

Computes the standard deviation and mean value of any variable. This
computation is direct and does not required a pre-processing with any
of the cdfmoy tools. This is the wrapping around the native cdfstd
operator assuming its usage is::  

 cdfstd [-save] **[-spval0]** **[-nomissincl]** **[-stdopt]**
 ... list_of_files  

CliMAF optional arguments are the ones surrounded with '**'.

See also:

  - :doc:`ccdfstd <ccdfstd>` for only getting the standard deviation
    of the variable   

**References** : http://www.drakkar-ocean.eu/tools

**Provider / contact** : climaf at meteo dot fr for the wrapping

**Inputs** (in the order of CliMAF call): 

  - any dataset forming a time-series (but only one)

**Mandatory arguments**: None

**Optional arguments**:

  - ``opt`` may be used to pass following keys :

    - ``-spval0`` : set missing_value attribute to 0 for all output
      variables and take care of the input missing_value. This option
      is usefull if missing_values differ from files to files  

    - ``-nomissincl`` : with this option, the output std and mean are
      set to missing value at any gridpoint where the variable
      contains a missing value for at least one timestep. You should
      combine with -spval0 if missing values are not 0 in all the
      input files 

    - ``-stdopt`` : use a  more optimal algorithm to compute std and
      std is unbiased 

**Required files**: None

**Outputs**:

  - main output : a netcdf file for standard deviation (variable :
    IN-var_std, same units than input variables)  
  - secondary outputs and their names :
     - ``moy`` : field mean value (variable: IN-var, same units than input variables)

**Climaf call example**:: 

  >>> duo=ds(simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O") # some dataset, with whatever variable
  >>> my_cdfstd_moy=ccdfstdmoy(duo)
  >>> cfile(my_cdfstd_moy) # compute the mean value and standard deviation of "uo" field (sea water velocity)
  >>> moy_var=my_cdfstd_moy.moy # moy_var receives operator output named "moy", namely the field mean value

**Implementation**: The operator is implemented as a binary using
cdftools cdfstd operator. 
