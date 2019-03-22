#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Package projects declares a number of 'projects', and the data location
for these projects , at CNRM or on Ciclad, when they exists. All its modules are
automatically loaded when importing climaf.api or launching by
``climaf``

The concept of a 'project' in CliMAF is explained with function
:py:func:`~climaf.classes.cproject()`. It allows to declare non-standard
variable names, scaling parameters ....

Please note that, for some combinations of observation 'projects' and
variables (i.e. 'snm' in erai, 'pr' in gpcp and cruts3), CliMAF provides a
flux variable, while the original data provides a monthly
accumulation. In that case, the conversion to rates assumes a fixed
month lenght of 30.3 days (for ensuring mnimal bias at year scale)

For listing the declared projects and their specifics, if you are under
the Python prompt, type e.g. ::

  >>> dir(climaf.projects)
  >>> help(climaf.projects.cmip5)

For knowing the specifics of variables for a given project (as e.g. re-scaling), type ::

  >>> aliases["erai"]

and interpret a result such as::

  'erai': {'clt': ('tcc', 1.0, 0.0, None, 'TCC', None),
           'das': ('d2m', 1.0, 0.0, None, '2D', None),
  ....

by : in project 'erai', standard variable 'clt' is read from data variable 'tcc' with scaling=1, offest=0, and no change
in units name; while 'TCC' is the variable name used in computing datafilename; and there is no special missing value in
addition to the one duly declared in the datafile

"""

__all__ = ["example", "cami", "cmip3", "cmip5", "ocmip5", "obs4mips", "em", "erai", "erai_land", "gpcc", "gpcp",
           "ceres", "cruts3", "file", "ref_climatos_and_ts", "igcm_out", "emn36", "nemo", "igcm_cmip6", "cmip6", "eobs",
           "cordex"]
