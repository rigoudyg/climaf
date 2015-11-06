ncdump : show only the header information of a netCDF file
------------------------------------------------------------

Show only the header information (also called the schema or metadata)
of a netCDF file on standard output. The output contains only the
declarations for the netCDF dimensions, variables, and attributes of
the input file, but no data values for any variables. 

**References** : https://www.unidata.ucar.edu/software/netcdf/workshops/2009/utilities/Ncdump.html

**Provider / contact** : climaf at meteo dot fr

**Inputs** : any dataset (but only one)

**Mandatory arguments**: none

**Optional arguments**:
  - none

**Output** : the header information of the dataset

**Climaf call example**::
 
  >>> cdef("frequency","monthly")
  >>> cdef("period","198001")
  >>> tas=ds(project="example", simulation="AMIPV6ALB2G", variable="tas") # some dataset, with whatever variable
  >>> header=ncdump(tas)
  >>> cfile(header)

**Side effects** : none

**Implementation** : NetCDF utilities 

