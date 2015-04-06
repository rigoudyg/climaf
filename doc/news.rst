.. _news:

------------
Whats' new
------------

Changes, newest first :

- 2015/04/06 : 

  - time period in CRS and as an argument to 'ds' is shortened unambiguously and may show only one date
  - function cfile has new arguments : target and link
  - CMIP5 facets 'realm' and 'table' are handled by 'ds', 'dataloc' and 'cdef'
  - organization called 'generic' allow to describe any data file hierarchy and naming
  - organization called 'EM' introduced, and allows to handle CNRM-CM outputs as managed by EM
  - default option for operator regrid is now 'remapbil' rather than 'remapcon2'
  - log messages are tabulated
  - a log file is added, with own severity level, set by clog_file
  - operators with format=None are also evaluated as soon as applied - i.e. cshow no more needednon ncview(...)