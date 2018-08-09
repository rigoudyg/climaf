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

cdataset : define a dataset object 
--------------------------------------------------------------------------

.. autoclass:: climaf.classes.cdataset

:py:meth:`cdataset.check: check time consistency of a dataset <climaf.classes.cdataset.check>`
====================================================================================================

.. automethod:: climaf.classes.cdataset.check

:py:meth:`cdataset.listfiles: returns the list of (local) files of a dataset <climaf.classes.cdataset.listfiles>`
===================================================================================================================

.. automethod:: climaf.classes.cdataset.listfiles

cdef : define some default values for datasets attributes
--------------------------------------------------------------------------

.. autofunction:: climaf.classes.cdef

eds : define an ensemble of datasets
---------------------------------------------------

.. autofunction:: climaf.classes.eds

cens : define an ensemble of objects
---------------------------------------------------

.. autoclass:: climaf.classes.cens

fds : define a dataset from a data file 
---------------------------------------------------

.. autofunction:: climaf.classes.fds


cproject : declare a new project and its non-standard attributes/facets
--------------------------------------------------------------------------

.. autoclass:: climaf.classes.cproject

cprojects : dictionary of known projects
--------------------------------------------------------------------------

.. autodata:: climaf.classes.cprojects

dataloc : describe data locations for a series of simulations
--------------------------------------------------------------------------

.. autoclass:: climaf.dataloc.dataloc

cdefault: set or get a default value for some data attribute/facet
--------------------------------------------------------------------------

.. autofunction:: climaf.classes.cdef

derive : define a variable as computed from other variables
--------------------------------------------------------------------------

.. autofunction:: climaf.operators.derive 

calias : define a variable as computed, in a project,  from another, single, variable
----------------------------------------------------------------------------------------

.. autofunction:: climaf.classes.calias
.. autofunction:: climaf.driver.calias


cfreqs : declare non-standard frequency names, for a project
--------------------------------------------------------------------------

.. autofunction:: climaf.classes.cfreqs


crealms : declare non-standard realm names, for a project
--------------------------------------------------------------------------

.. autofunction:: climaf.classes.crealms

