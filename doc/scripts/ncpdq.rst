ncpdq: netCDF Permute Dimensions Quickly
------------------------------------------

Permute quickly dimensions of a variable.  

**References** : http://nco.sourceforge.net/nco.html#ncpdq-netCDF-Permute-Dimensions-Quickly

**Provider / contact** : climaf at meteo dot fr

**Inputs** : any dataset (but only one)

**Mandatory arguments**: 
  - ``arg`` : ncpdq arguments (as e.g. -a lon,lat ...)

**Optional arguments**:
  - none

**Output** : the permuted object

**Climaf call example**::
 
  >>> cdef("frequency","monthly")
  >>> cdef("period","198001")
  >>> tas=ds(project="example", simulation="AMIPV6ALB2G", variable="tas")
  >>> # Show dimension order of 'tas' variable => tas(time, lat, lon) 
  >>> ncdump(tas) 
  >>> # Permute dimension lat and lon
  >>> tas_permute=ncpdq(tas,arg="-a lon,lat")
  >>> # Show dimension order of 'tas' variable after permutation => tas(time, lon, lat)
  >>> ncdump(tas_permute)  

**Side effects** : none

**Implementation** : using NCO with operator ncpdq
