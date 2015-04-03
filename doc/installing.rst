Installing and running
----------------------

First check the listed :ref:`requirements`

Installing CliMAF is quick, through only a few commands, using CliMAF GitHub
repository; this will also copy some data allowing for testing the installation and for running a few examples::

  cd some_installation_dir
  git clone https://github.com/senesis/climaf climaf
  cd climaf
  export PYTHONPATH=$PYTHONPATH:$(pwd)
  cd testing
  test_install.sh 

After successful installation, for running CliMAF, you will :

- set your PYTHONPATH , e.g. in your ``~/.profile`` file::

   export PYTHONPATH=$PYTHONPATH:<some_installation_dir>/climaf

- import ``climaf.api`` in your Python session or script::

  $ python

  >>> import climaf.api
  >>> ...

Please see also : :ref:`examples`
