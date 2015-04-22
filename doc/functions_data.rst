-------------------------------------------------------------
A package and some functions for data definition and access
-------------------------------------------------------------

package ``projects`` : pre-defined projects and datasets
===========================================================================

.. automodule:: climaf.projects

- CMIP5

  .. automodule:: climaf.projects.cmip5

- OCMIP5

  .. automodule:: climaf.projects.ocmip5

- EM

  .. automodule:: climaf.projects.em

- example

  .. automodule:: climaf.projects.example

- ERAI

  .. automodule:: climaf.projects.erai

- OBS4MIPS

  .. automodule:: climaf.projects.obs4mips

- CAMI

  .. automodule:: climaf.projects.cami

ds : define a dataset object (actually a front-end for ``cdataset``)
===========================================================================

.. autofunction:: climaf.classes.ds

cdataset
===========================================================================

.. autoclass:: climaf.classes.cdataset

cdef : define some default values for datasets attributes
===========================================================================

.. autofunction:: climaf.classes.cdef

cprojects : list of known projects
===========================================================================

.. autodata:: climaf.classes.cdefaults

cproject : declare a new project and its non-standard attributes/facets
===========================================================================

.. autoclass:: climaf.classes.cproject

dataloc : describe data locations for a series of experiments
===========================================================================

.. autoclass:: climaf.dataloc.dataloc

cdefaults: list of default values
===========================================================================

.. autodata:: climaf.classes.cdefaults

derive : define a variable as computed from other variables
===========================================================================

.. autofunction:: climaf.operators.derive 

calias : define a variable as computed from another, single, variable
===========================================================================

.. autofunction:: climaf.classes.calias


