--------------------------------------------
Functions dor data definition and access
--------------------------------------------

cproject : declare a project and its non-standard attributes/facets
-----------------------------------------------------------------------

.. autoclass:: climaf.classes.cproject

cprojects : list of known projects
------------------------------------

.. autodata:: climaf.classes.cdefaults

dataloc : describe data locations for a series of experiments
------------------------------------------------------------------

.. autoclass:: climaf.dataloc.dataloc

ds : define a dataset object (actually a front-end for ``cdataset``)
-------------------------------------------------------------------------

.. autofunction:: climaf.classes.ds

cdataset
----------

.. autoclass:: climaf.classes.cdataset

cdef : define some default values for datasets attributes
------------------------------------------------------------

.. autofunction:: climaf.classes.cdef

cdefaults: list of default values
------------------------------------------

.. autodata:: climaf.classes.cdefaults

derive : define a variable as computed from other variables
--------------------------------------------------------------

.. autofunction:: climaf.operators.derive 


