CliMAF : a Climate Model Assessment Framework
---------------------------------------------

CliMAF doc is available at `Readthedocs
<http://climaf.readthedocs.org/>`_ , which includes `installation instructions <http://climaf.readthedocs.org/en/latest/installing.html>`_

The aim of CliMAF is to allow for an actual, **easy, collaborative development of climate model outputs assessment suites by climate scientists with varied IT background**, and to ultimately share such suites for the benefit of the Climate Science. 

It is basically a scriptable way to process NetCDF `CF compliant
<http://cfconventions.org/>`_ climate model outputs 

----

.. _Organization:

**Repository organization** 

- ``doc``      : used to **build** documentation; please **read** doc at  `CliMAF doc site <http://climaf.readthedocs.org/>`_
- ``examples`` : a collection of Python scripts and IPython Notebooks illustrating most of the ways to use CliMAF (also includes a limited input data set)
- ``scripts``  : the core set of diagnostic/processing modules
- ``dev``      : a place where you may wish to store other processing  modules, which should finally end up in sister diectory ``scripts`` 
- ``climaf``   : python code for CliMAF core functions : driver, cache ...
- ``testing``  : guess from text above


