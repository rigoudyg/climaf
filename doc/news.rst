.. _news:

------------
Whats' new
------------

Changes, newest first :

.. _news_0.7:

- 2015/05/20 - Version 0.7 :

 - Handle **explicitly defined objects ensembles** (see
   :py:class:`~climaf.classes.cens`) and **explicit dataset ensembles**
   (see :py:func:`~climaf.classes.eds`. Operators which are not
   ensemble-capable will be automagically looped over members. See  
   examples in :download:`ensemble.py <../examples/ensemble.py>`.
 - New standard operator ``lines`` for plotting profiles or other xy 
   curves for ensembles; see :doc:`scripts/lines`
 - Standard operator ``plot`` has new arguments : ``contours`` for
   adding contour lines, ``domain`` for greying out land or ocean
 - Special keyword ``crs`` is replaced by keyowrd ``title`` : the
   value of CRS expression for an object is provided to script-based
   operators under keyword ``title``, if no title value is provided
   when invoking the operator. Scripts can also independanlty use
   keyword ``crs`` for getting the CRS value
 - cpage keywords changed : widths_lits -> widths, heights_list -> heights

.. _news_0.6:

- 2015/05/11 - Version 0.6.1 :

 - Add a **macro** feature : easy definition of a macro from a
   compound object; you can save, edit, load... and macros are used for
   interpreting cache content. See :py:func:`~climaf.cmacros.cmacro`
   and an example in :download:`macro <../examples/macro.py>`.
 - A **general purpose plot operator**, named ``plot``, is fine for
   plotting 1D and 2D datasets (maps, cross-sections, profiles, but
   not Hoevmoeller...) and replaces plotxesc and plotmap. It allows
   for setting explicit levels in palette, stereopolar projection,
   vertical coordinate ... See :doc:`scripts/plot`
 - Can **list or erase cache content using various filters** (on
   age, size, modif date ...); disk usage can be displayed. 
   See :py:func:`~climaf.cache.clist()`, :py:func:`~climaf.cache.cls`, :py:func:`~climaf.cache.crm`,
   :py:func:`~climaf.cache.cdu`, :py:func:`~climaf.cache.cwc`
 - Can create an **array of figures** using
   :py:func:`~climaf.classes.cpage`. See example :download:`figarray <../examples/figarray.py>`.
 - Can **cope with un-declared missing values in data files**, as
   e.g. Gelato outputs with value=1.e+20 over land, which is not the
   declared missing value ; See :py:func:`~climaf.classes.calias()`
   and :py:mod:`~climaf.projects.em`
 - When declaring data re-scaling, can declare units of the result (see 
   :py:func:`~climaf.classes.calias`) 
 - Can declare correspondance between **project-specific frequency names** 
   and normalized names (see :py:func:`~climaf.classes.cfreqs`).
 - Add : howto :ref:`record`
 - Cache content index is saved on exit
 - Add an example of **seaice data handling and plotting**. See :download:`seaice.py <../examples/seaice.py>`

- 2015/04/22 - Version 0.6.0 :

 - Add operator ``plotxsec`` (removed in 0.6.1, see
   replacement at :doc:`scripts/plot` )
 - **A number of 'projects' are built-in**, which describe data
   organization and data location for a number of analyses and
   experiments datasets available at one of our data centers, 
   as e.g. CMIP5, OBS4MIPS, OCMPI5, EM, ...) ; see :ref:`known_datasets` 
 - **Variable alias** and **variable scaling** are now managed, on a
   per-project basis. 
   See function :py:func:`~climaf.classes.calias()`
 - Derived variables can now be defined on a per-project basis. See function :py:func:`~climaf.operators.derive()`
 - CliMAF was proved to **work under a CDAT** install which uses
   Python 2.6
 - Better explain how to install CliMAf (or not), to run it or to use
   it as a library; see :ref:`installing` and :ref:`library`

.. _news_0.5:

- 2015/04/14 - Version 0.5.0 :

 - A versionning scheme is now used, which is based on recommendations found at http://semver.org. 

 - Starting CliMAF :

  - Binary ``climaf`` allows to launch Python and import Climaf at
    once. See :ref:`running_inter`
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
    variables. See :ref:`configuring`
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
