.. _news:

------------
Whats' new
------------

Note : Issues with CliMAF and future work are documented at https://github.com/senesis/climaf/issues

.. |indx| image:: html_index.png 
  :scale: 13%

.. _screen_dump: ../../html_index.png 

Changes, newest first :

- 2015/12/10 : 

  - New argument for standard operator ``plot`` : ``trim`` to turn
    on/off triming for PNG figures (see :doc:`scripts/plot`) 

- 2015/12/08 :

 - Changes for :py:func:`~climaf.classes.cpage`  :

   - argument ``orientation`` was removed and replaced by new
     arguments ``page_width`` and ``page_height`` for controling more
     image resolution    
   - best adjustment of figures in height (if ``fig_trim`` is True).


.. _news_0.12:

- 2015/11/27 - Version 0.12 :
  
 - Changes for standard operator ``plot`` (see :doc:`scripts/plot`) :  

   - new arguments : 

    - ``level`` and ``time`` for selecting time  or level;   
    - ``resolution``   for controling image resolution 
    - ``format`` : graphical format : either png (default) or pdf
    - **17 new optional arguments to adjust title, sub-title, color bar, label font, label font height**
      , ... (see :ref:`More plot optional arguments <plot_more_args>` )       

   - optional argument ``levels`` was renamed ``colors``
   - code re-design 
   - if running on Ciclad, you must load NCL Version 6.3.0; see :ref:`configuring` 

 - New arguments for :py:func:`~climaf.classes.cpage` :

   - ``title``. See example :download:`figarray <../examples/figarray.py>`
   - ``format`` : graphical output format : either png (default) or pdf


 - Two new output formats allowed for operators : 'graph' and 'text';
   see :py:func:`~climaf.operators.cscript` 

  - 'graph' allows the user to choose between two graphic output
    formats: 'png' and 'pdf' (new graphic ouput format), if the
    corresponding operator supports it (this is the case for plot()); 
  - 'txt' allows to use any operator that just ouputs text (e.g. 
    'ncdump -h'). The text output is not managed by CliMAF (but only displayed).

 - Two new standard operators :

    - ``ncdump`` : **show only the header information of a netCDF
      file**; see :doc:`scripts/ncdump` 
    - ``cpdfcrop`` : **crop pdf figures to their minimal size,
      preserving metadata**; see :doc:`scripts/cpdfcrop` 

 - An operator for temporary use : ``curves`` (see :doc:`scripts/curves`) :  


- 2015/10/19 - Version 0.11 :

 - For :py:func:`~climaf.classes.cpage` (which creates an **array of
   figures**), default keywords changed : fig_trim=False ->
   fig_trim=True, page_trim=False -> page_trim=True. See example
   :download:`figarray <../examples/figarray.py>`.   

 - New function :py:func:`~climaf.driver.efile()` allows to apply
   :py:func:`~climaf.driver.cfile()` to an ensemble object. It
   writes a single file with variable names suffixed by member label.       
 
 - The **general purpose plot operator** (for plotting 1D and 2D
   datasets: maps, cross-sections and profiles), named ``plot``, was
   significantly enriched. It now allows for plotting an additional
   scalar field displayed as contours and for plotting an optional
   vector field, for setting the reference longitude, the contours
   levels for main or auxiliary field, the reference length used for
   the vector field plot, the rotation of vectors from model grid to
   geographic grid, ... See :doc:`scripts/plot`   


.. _news_0.10:

- 2015/09/23 - Version 0.10 :

 - Interface to Drakkar CDFTools: a number of
   operators now come in two versions : one accepting multi-variable
   inputs, and one accepting only mono-variable inputs (with an 'm' suffix)
   
 - Multi-variable datasets are managed. This is handy for cases where
   variables are grouped in a file. See an example in :
   :download:`cdftransport.py <../examples/cdftransport.py>` , where 
   variable 'products' is assigned

 - Package :py:mod:`climaf.html` has been re-designed : simpler
   function names (:py:func:`~climaf.html.fline()`, 
   :py:func:`~climaf.html.flines()`, addition of basic function
   :py:func:`~climaf.html.line()` for creating a simple links line ;
   improve doc

 - New function :py:func:`~climaf.classes.fds()` allows to define simply 
   a dataset from a single data file. See example in 
   :download:`data_file.py <../examples/data_file.py>`


.. _news_0.9:

- 2015/09/08 - Version 0.9 :

 - Operator 'lines' is smarter re.time axis: (see
   :doc:`scripts/lines`):

   - Tick marks are smartly adapted to the time period duration.  
   - When datasets does not cover the same time period, the user can 
     choose wether time axis will be aligned to the same origin or
     just be the union of all time periods 

 - Interface to Drakkar CDFTools: cdfmean, cdftransport, cdfheatc, cdfmxlheatc,
   cdfsections, cdfstd, cdfvT; you need to have a patched version of
   Cdftools3.0;  see :ref:`CDFTools operators <cdftools>` and examples
   : :download:`cdftransport.py <../examples/cdftransport.py>` and :download:`cdftools.py <../examples/cdftools.py>` 
   

 - CliMAF can provide fixed fields to operators, which path may
   depend on project and simulation of operator's first operand 
   (see  :py:func:`~climaf.operators.fixed_fields()`)

 - Fixes :
 
  - datasets of type 'short' are correctly read
  - operator's secondary output variables are duly renamed, according
    to the name given to operator's the secondary output when
    declaring it using :py:func:`~climaf.operators.script()` 

.. _news_0.8:

- 2015/08/27 - Version 0.8 :

 - Basics

  - **A CHANGE BREAKING BACKWARD COMPATIBILITY : default
    facet/attribute 'experiment' was renamed 'simulation'**. It is
    used for hosting either CMIP5's facet/attribute 'rip', or for
    'EXPID' at CNRM, or for JobName at IPSL. All 'projects' and
    examples, and this documentation too, have been changed
    accordingly. Please upgrade to this version if you want a
    consistent documentation. A facet named 'experiment' was added to
    project CMIP5 (for hosting the 'CMIP5-controlled-vocabulary'
    experiment name, as e.g. 'historical').
  - **default values for facets** are now handled on a per-project
    basis. See :py:func:`~climaf.classes.cdef()` and
    :py:class:`~climaf.classes.cdataset()`. 
  - Binary ``climaf`` can be used as a **back end** in your scripts,
    feeding it with a string argument. See :ref:`backend`

 - Outputs and rendering

  - Package climaf.html allows to **easily create an html index**, which includes
    tables of links (or thumbnails) to image files; iterating on
    e.g. seasons and variables is handled by CliMAF. See :
    
    - a screen_dump for such an index : |indx| 
    - the corresponding rendering code in :download:`index_html.py <../examples/index_html.py>` 
    - the package documentation : :py:mod:`climaf.html`
  - Function :py:func:`~climaf.driver.cfile` can create **hard
    links** : the same datafile (actually : the samer inode) will
    exists with two filenames (one in CliMAF cache, one which is
    yours), while disk usage is counted only for one datafile; you may
    remove any of the two file(name)s as you want, without disturbing
    accessing the data with the other filename.
  - When creating a symlink between a CliMAF cache file and another
    filename with function :py:func:`~climaf.driver.cfile` : **the
    symlink source file is now 'your' filename**; hence, no risk that some
    CliMAF command does erase it 'in your back'; and CliMAf will nicely
    handle broken symlinks, when you erase 'your' files

 - Inputs

  - climatology files, which have a somewhat intricated time axis
    (e.g. monthly averages over a 10 year period) can now be handled
    with CliMAF regular time axis management, on the fly, by modifying 
    the basic data selection script: it can
    enforce a reference time axis by intepreting the data
    filename. This works e.g. for IPSL's averaged annual-cycle
    datafiles. If needed, you may change function timefix() near line 
    30 in :download:`mcdo.sh <../scripts/mcdo.sh>` 
  - automatic fix of CNRM's Nemo old data time_axis issues, provided you
    set environment variable CLIMAF_FIX_NEMO_TIME to anything but
    'no'. This will add processing cost. This adresses the wrong time
    coordinate variable t_ave_01month and t_ave_00086400
  - speed-up datafiles scanning, incl. for transitory data organization
    during simulation run with libIGCM

 - fixes and minor changes:

   - check that no dataset attribute include the separator defined for
     corresponding project
   - fix issues at startup when reading cache index
   - rename an argument for operator 'plot' : domain -> focus
   - scripts argument 'labels' now uses '$' as a separator

.. _news_0.7:

- 2015/05/20 - Version 0.7 :

 - Handle **explicitly defined objects ensembles** (see
   :py:class:`~climaf.classes.cens`) and **explicit dataset ensembles**
   (see :py:func:`~climaf.classes.eds`. Operators which are not
   ensemble-capable will be automagically looped over members. See  
   examples in :download:`ensemble.py <../examples/ensemble.py>`.
 - New standard operator ``lines`` for **plotting profiles or other xy 
   curves for ensembles**; see :doc:`scripts/lines`
 - Standard operator ``plot`` has new arguments : ``contours`` for
   adding contour lines, ``domain`` for greying out land or ocean; see :doc:`scripts/plot`
 - **Extended access to observation data** as managed by VDR at CNRM :
   GPCC, GPCP, ERAI, ERAI-LAND, CRUTS3, CERES (in addition to
   OBS4MIPS, and CAMI); see :ref:`known_datasets` and examples in 
   :download:`data_obs.py <../examples/data_obs.py>`.
 - Special keyword ``crs`` is replaced by keyword ``title`` : the
   value of CRS expression for an object is provided to script-based
   operators under keyword ``title``, if no title value is provided
   when invoking the operator. Scripts can also independanlty use
   keyword ``crs`` for getting the CRS value
 - cpage keywords changed : widths_list -> widths, heights_list -> heights

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
   simulations datasets available at one of our data centers, 
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
    specific to a given simulation. . See examples in
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
