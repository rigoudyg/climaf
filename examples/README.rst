.. sidebar:: Ipython notebooks

   An Ipython notebook is a way to mix Python commands, their results, comments and notes; results can be graphics; you can also edit and replay the commands, and edit the comments at length; 

   You can save the resulting notebook and restore it with or without re-executing the Python code; some people see it as the ultimate form of a laboratory notebook, allowing for recording a research/analysis interactive session after some house-cleaning for false tries

   This is documented at length at `Ipython notebooks <http://ipython.org/notebook.html>`_. 

   **For running the example Ipython notebook**::
     
     $ cd <climaf_dir>
     $ export PYTHONPATH=$PYTHONPATH:$(pwd)
     $ cd examples
     $ ipython notebook 

     # Once the notebook server tab shows in your favorite Web Browser, 
     # just click on "ATourOfClimaf"


:download:`A Tour Of Climaf <../examples/ATourOfCliMAF.html>` is **a progressive but quite comprehensive tour**, which is :download:`here presented as an html page <../examples/ATourOfCliMAF.html>` , but which can also be run as an IPython notebook (see sidenote)

For **running CliMAF**, or running one of the Python scripts example described below, you will use a Python shell, after telling Python where the CliMAF code is:: 

    $ export PYTHONPATH=$PYTHONPATH:<climaf_dir>
    $ python

::

    >>> import climaf.api
    >>> .... 


A number of examples show in directory ``<install_dir>/examples`` and are also dowloadable using the links below; you will copy and paste the code lines to the Python shell using your favorite method. Each code line is documented by a comment which tries to bring all necessary information for letting your CliMAF expertise grow steadily. 

Some of the examples can be run anywhere, as they use the data sample installed with CliMAF :

  - :download:`plotmap.py <../examples/plotmap.py>`      : basic and advanced plotting (using ncview and ncl)
  - :download:`export.py <../examples/export.py>`        : how to 'export' results out of CliMAF
  - :download:`derived.py <../examples/derived.py>`      : how to define a new geophysical variable and use it in CliMAF
  - :download:`increm.py <../examples/increm.py>`        : compute any derived variable incrementally (i.e. using new inputs as they become available)
  - :download:`latlonbox.py <../examples/latlonbox.py>`    : define a dataset on a lat-lon box; also extract another box
  - :download:`regrid.py <../examples/regrid.py>`    : regrid some data or object to a named grid or to the grid of another object/data
  - :download:`ann_cycle.py <../examples/ann_cycle.py>`    : compute an annual cycle, using CDO

.. _examples_data:

Others can run only if they have access to some datasets on the local file system :
 
  - :download:`cmip5drs.py  <../examples/cmip5drs.py>`    : access data which are organized using the CMIP5 Data Reference Syntax
  - :download:`ocmip_ciclad.py <../examples/ocmip_ciclad.py>`: access data which are organized using the OCMIP5 conventions on Ciclad
  - :download:`obs4mips.py <../examples/obs4mips.py>`     : access OBS4MIPS data organized as at CNRM
  - :download:`obscami.py <../examples/obscami.py>`     : access observation data organized 'a la CAMI', here at CNRM
  - :download:`basic_oce.py <../examples/basic_oce.py>`     : acces ocean data on ORCA grid in CMIP5_DRS data, and perfome some basic operations


