-------------------------
Installing and/or running
-------------------------


Installing
-------------------------

Installing CliMAF, if necessary, is quick, through only a few commands, using CliMAF GitHub
repository; this will also copy some data allowing for testing the installation and for running a few examples

- if you wish or need to install :

 - first check the listed :ref:`requirements` ;

 - execute :: 

    cd some_installation_dir
    git clone https://github.com/senesis/climaf climaf
    cd climaf
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    cd testing
    ./test_install.sh 
  
  and check the installation test results

Configuring for running without installing
--------------------------------------------

You can run CliMAF on Ciclad and at CNRM without installing it; just 
do as indicated below, replacing ``<some_installation_dir>`` by :

 - ``/cnrm/aster/data1/UTILS/climaf/current`` at CNRM

 - ``~ssenesi/climaf`` on Ciclad


.. _running:

Running
-------------------------

From that point, for running CliMAF, you can either :

- use binary ``climaf`` for launching Python while importing CliMAF :

  - set your PATH e.g. in your ``~/.profile`` file::

    $ export PATH=$PATH::<some_installation_dir>/climaf/bin

  - launch CliMAF ::

    $ climaf

    >>>         (this is the Python prompt)

  Notes : 

   - you may also provide multiple python scripts as arguments to
     command ``climaf``

   - you may **not** (yet) use option ``-i`` as with Python, for
     combining launching a script and getting the prompt afterwards


- or import climaf in your python environment :

  - set your PYTHONPATH , e.g. in your ``~/.profile`` file::

    $ export PYTHONPATH=$PYTHONPATH:<some_installation_dir>/climaf

  - import ``climaf.api`` in your Python session or script, preferably as in::

    $ python

    >>> from climaf.api import *
    >>> ...

Please see also : :ref:`examples`

Configuration file
-------------------

You may put in file ``~/.climaf`` any python code using CliMAF
functions; this will be executed at the end of climaf.api import 

Environment variables 
------------------------

CliMAF do interpret some environment variables :

- CLIMAF_CACHE : a directory used for storing intermediate results,
  and those final results which are not explicitly copied elsewhere;
  defaults to ~/tmp/climaf_cache. 

- CLIMAF_LOG_LEVEL and CLIMAF_LOGFILE_LEVEL : for setting the
  verbosity level on stderr (resp. on file climaf.log); defaults to
  'error' (resp. 'info'). See :py:func:`~climaf.cache.clog` for details

