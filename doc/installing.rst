---------------------------------
Installing, configuring, using 
---------------------------------

.. _installing:

Using CliMAF at CNRM, on Ciclad or Climserv: fast track
-----------------------------------------------------------

- If working on IPSL's Ciclad, Climserv, at CNRM or on MF's Beaufix HPC machine, you do not need to install CliMAF; just 
  do as indicated below (as e.g. in section :ref:`running_inter`), replacing ``<some_installation_dir>`` by :

  - ``/cnrm/est/COMMON/climaf/climaf_x.y.z`` at CNRM

  - ``~senesi/climaf_installs/climaf_x.y.`` on Beaufix


    
- On the IPSL - ESPRI Mesocenter (Ciclad and Climserv):
      
  - do not forget to submit an interactive session if you want to run your code interactively:
     * qsub -IVX -q std -l mem=9g -l vmem=9g (don't need the X if you
       don't want interactive display, and add ``-l nodes=1:ppn=10``
       for parallel processing on 10 procs)
     
  - do::
    
      module load climaf

    to set your environment:
      - point to a CliMAF install ($CLIMAF environment variable)
      - set your CliMAF cache ($CLIMAF_CACHE environment variable)
      - use a miniconda install and activate a suitable environment
      - load cdo, ncl, nco, and netcdf4 modules

    See 'Configuring CliMAF' below to customize your environment (use another CliMAF install, another cache...)

  - use CliMAF in an interactive IPython session (launch IPython and import CliMAF at once)::

      climaf

  - if you want to use Jupyter notebooks, use::

      climaf-notebook

    and follow the instructions

  - get the CliMAF demo notebooks::
    
     cp -r /ciclad-home/jservon/TP_CliMAF ~
     cd TP_CliMAF
     climaf-notebook

  - lastly, use::
    
     from climaf.api import *

    at the beginning of your python script or notebook to import CliMAF


Installing CliMAF (if you are not at CNRM, on Ciclad or Climserv) 
------------------------------------------------------------------

- Installing CliMAF, if necessary, is quick, through only a few commands, using `CliMAF GitHub
  repository <https://github.com/senesis/climaf>`_ ; this will also
  copy some data allowing for testing the installation and for running a few examples

  - first check the listed :ref:`requirements` ;

  - execute:: 

     cd some_installation_dir
     git clone https://github.com/senesis/climaf climaf
     cd climaf
     export PYTHONPATH=$PYTHONPATH:$(pwd)
     cd testing
     ./test_install.sh 


  
    and check the output of last command. Contact 'climaf at meteo dot
    fr' in case of problem at that stage

  - for getting the development version, you may rather execute::

      git clone -b dev https://github.com/senesis/climaf climaf


.. _configuring:

Configuring CliMAF
---------------------

- CliMAF do interpret some environment variables :

 - CLIMAF : path to CliMAF install 

 - CLIMAF_CACHE : a directory used for storing intermediate results,
   and those final results which are not explicitly copied elsewhere;
   defaults to ~/tmp/climaf_cache. 

 - CLIMAF_REMOTE_CACHE : a directory used for storing local copies
   of remote data; defaults to $CLIMAF_CACHE/remote_data. 
 
 - CLIMAF_LOG_DIR : for setting the directory holdong climaf logs
   (defaults to current working directory

 - CLIMAF_LOG_LEVEL and CLIMAF_LOGFILE_LEVEL : for setting the
   verbosity level on stderr (resp. on file climaf.log); defaults to
   'error' (resp. 'info'). See :py:func:`~climaf.clogging.clog`
   (resp. :py:func:`~climaf.clogging.clog_file`) for details

 - CLIMAF_FIX_NEMO_TIME : if set to anything but 'no', this will
   automatic fix CNRM’s Nemo old data time_axis issues. This adresses
   the wrong time coordinate variable t_ave_01month and
   t_ave_00086400. This will add processing cost

 - CLIMAF_FIX_ALADIN_COORD : if set to anything but 'no', this will
   automatic fix Aladin outputs attribute 'coordinates' issues. This
   adresses the wrong variable attribute 'coordinates' with 'lat lon'
   to 'latitude longitude'.

- Configuration file : you may put in file ``~/.climaf`` any python code using CliMAF
  functions; this will be executed at the end of climaf import; the code 
  must use fully qualified names for Python functions (as in e.g. ``climaf.operators.cscript``): it des not
  benefit from the intractive shortcuts defined in climaf.api (as
  described below in :ref:`running_inter`)

- Environment :

  - If running on Beaufix, you must setup your environment by::

    $ module load python/2.7.5 nco ncview ncl

  - If running on Ciclad, you must setup your environment by::

    $ module load climaf

  - On some systems, if CDO fails at allocating memory, you may have
    to put e.g. in your ~/.bash_profile::

    $ ulimit -s unlimited 

    in csh::

    $ unlimit stacksize

.. _running_inter:

Running CliMAF interactively
-----------------------------

For running CliMAF as easily as possible under the Python prompt,
without having to know details about CliMAF functions location, and
just mimicking one of the :ref:`examples`, please first make sur you
have write permission in the current directory (used for some log
files); then, you can either :

- use binary ``climaf`` for launching Python while importing CliMAF :

  - set your PATH e.g. in your ``~/.profile`` file::

    $ export PATH=$PATH:<some_installation_dir>/bin

  - and then launch CliMAF ::

    $ climaf

    >>>         #(this is the Python prompt)

  - you may of course also directly type ::  

    $ <some_installation_dir>/bin/climaf


- or import ``climaf.api.*`` in your python environment :

  - set your PYTHONPATH , e.g. in your ``~/.profile`` file::

    $ export PYTHONPATH=$PYTHONPATH:<some_installation_dir>/

  - type ::

    $ python

    >>> from climaf.api import *
    >>> ...

   You may also use **CDAT** instead of Python. It is working at least
   for CDAT version using Python from 2.6.5.

Please see also : :ref:`examples`


.. _backend:

Using CliMAF as a back end in your scripts 
--------------------------------------------

Binary ``climaf`` described above (and located in ``<some_installation_dir>/bin``) can
be used with a string argument which is a series of valid CliMAF
commands. It will then run silently in the background (up to the point
where an error occurs) and may be used e.g. to get the filename for a
result handled by CliMAF in its cache. 

As an example, if your CliMAF startup file (see :ref:`configuring`) does import the necessary
modules for defining function ``season.clim``, you may write::

 $ climaf "print cfile(season.clim('CNRM-CM','PRE6.2T127Cr2E','pr','JJAS','1980-1999'))"

or even:: 

 $ file=$(climaf "print cfile(season.clim('CNRM-CM','PRE6.2T127Cr2E','pr','JJAS','1980-1999'))")


This can be handy for letting CliMAF handle your climatology files in
its cache

.. _library:

Using CliMAF as a library
-----------------------------

If you wish to have the same facilities (shortcuts) than in interactive
sessions, then insert ::

>>> from climaf.api import *

in each module making use of CliMAF functions. 

But you may prefer to make only explicit imports, and then use::

>>> import climaf

In that case: 

- you must use fully qualified python names for climaf functions, such
  as ``climaf.classes.ds()``; you may have a look at module climaf.api
  to know in which module is each useful CliMAF function

- please note that all CliMAF operators declared using
  e.g. :py:func:`~climaf.operators.cscript` must be prefixed with
  "climaf.operators" as e.g. in ::

   >>> avg=climaf.operators.time_average(ds)

- the same applies for macros, *mutatis mutandis*  ::

   >>> avg=climaf.macros.my_macro(ds)



 
