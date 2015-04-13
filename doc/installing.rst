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

 - ``/cnrm/aster/data1/UTILS/climaf`` at CNRM

 - ``~ssenesi/climaf`` on Ciclad


Running
-------------------------

From that point, for running CliMAF, you will :

- set your PYTHONPATH , e.g. in your ``~/.profile`` file::

   export PYTHONPATH=$PYTHONPATH:<some_installation_dir>/climaf

- import ``climaf.api`` in your Python session or script, preferably as in::

  $ python

  >>> from climaf.api import *
  >>> ...

Please see also : :ref:`examples`
