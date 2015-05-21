"""

Package projects declares a number of 'projects', and the data location
for this projects , at CNRM or on Ciclad, when they exists. It is
automatically loaded when importing climaf.api or launching by
``climaf``

The concept of a 'project' in CliMAF is explained with function
:py:func:`~climaf.classes.cproject()`. It allows to declare non-standard
variable names, scaling parameters ....


For knowing declared projects, if you are under the Python prompt, type e.g. ::

  >>> dir(climaf.projects)
  >>> help(climaf.projects.cmip5)


"""

__all__=[ "example", "cami", "cmip5", "ocmip5" , "obs4mips" , "em" , "erai", "erai-land", "gpcc", "gpcp", "ceres", "cruts3"]
