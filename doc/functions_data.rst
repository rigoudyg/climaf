-------------------------------------------------------------
Functions for data definition and access
-------------------------------------------------------------

.. default-domain:: python


Except for the first three paragraphs, this section is for advanced use. As a first step, you should consider using
the built-in data data definitions described at :py:mod:`~climaf.projects`. 
You may need to come back to this section for reference




ds : define a dataset object (actually a front-end for ``cdataset``)
--------------------------------------------------------------------------

.. autofunction:: climaf.classes.ds

cdataset :: define a dataset object 
--------------------------------------------------------------------------

.. autoclass:: climaf.classes.cdataset

cdef : define some default values for datasets attributes
--------------------------------------------------------------------------

.. autofunction:: climaf.classes.cdef

eds : define an ensemble of datasets
---------------------------------------------------

.. autofunction:: climaf.classes.eds

cproject : declare a new project and its non-standard attributes/facets
--------------------------------------------------------------------------

.. autoclass:: climaf.classes.cproject

cprojects : list of known projects
--------------------------------------------------------------------------

.. autodata:: climaf.classes.cdefaults

dataloc : describe data locations for a series of experiments
--------------------------------------------------------------------------

.. autoclass:: climaf.dataloc.dataloc

cdefaults: list of default values
--------------------------------------------------------------------------

.. autodata:: climaf.classes.cdefaults

derive : define a variable as computed from other variables
--------------------------------------------------------------------------

.. autofunction:: climaf.operators.derive 

calias : define a variable as computed, in a project,  from another, single, variable
----------------------------------------------------------------------------------------

.. autofunction:: climaf.classes.calias


cfreqs : declare non-standard frequency names, for a project
--------------------------------------------------------------------------

.. autofunction:: climaf.classes.cfreqs

