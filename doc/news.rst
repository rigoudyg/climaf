.. _news:

------------
Whats' new
------------

Changes, newest first :

.. _news_0.5:

- 2005/04/14 - Version 0.5.0 :

 - A versionning scheme is now used, which is based on recommendations found at httm://semver.org. 

 - Starting CliMAF :

  - Binary ``climaf`` allows to launch Python and import Climaf at
    once. See :ref:`running`
  - File ``~/.climaf`` is read as configuration file , at the end of
    climaf.api import

 - Input data :

  - New projects can be defined, with project-specific
    facets/attributes. See :py:class:`~climaf.classes.cproject`
  - A number of projects are 'standard' : CMIP5, OCMPIP5, OBS4MIPS,
    EM, CAMIOBS, and example
  - Data location is automatically declared for
    CMIP5 data at CNRM and on Ciclad (in module site_settings)
  - Discard pre-defined organizations 'OCMPI5_Ciclad', 'example', etc,
    and replace it by smart use of organization 'generic'.  Note : **this
    leads to some upward incompatibility** regarding how data
    locations are declared for these datasets; please refer to the
    examples in :download:`data_generic.py
    <../examples/data_generic.py>`).
  - Access to fixed fields is now possible, and fixed fields may be
    specific to a given experiment. . See examples in
    :download:`data_generic.py <../examples/data_generic.py>`  
    and :download:`data_cmip5drs.py <../examples/data_cmip5drs.py>`        
    
 - Operators : 

  - Explanation is available on how to know how a given operator is declared to CliMAF,
    i.e. what is the calling sequence for the external script or binary; see 
    :ref:`how_to_list_operators`
  - Simplify declaration of scripts with no output (just omit ${out})
  - plotmap : this operator now zoom on the data domain, and plot data across
    Greenwich meridian correctly

 - Running CliMAF - messages, cache, errors :

  - Verbosity, and cache directory, can be set using environment
    variables. See :ref:`running`
  - Simplify use of function :py:func:`~climaf.clogging.clog`
  - Log messages are indented to show recursive calls of ceval()
  - Quite extended use of Python exceptions for error handling

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
