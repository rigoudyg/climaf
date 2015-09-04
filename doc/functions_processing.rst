--------------------------------------------------------
Functions for processing data
--------------------------------------------------------

.. default-domain:: python

Standard operators
---------------------

For documented standard operators see  :ref:`standard_operators`  


Non-standard operators
-----------------------

See :ref:`how_to_list_operators`

cscript : define a new CliMAF operator 
-----------------------------------------------------------------------------------
 
Defining a new CliMAF operator also defines a new Python function,
with the same name

.. autoclass:: climaf.operators.cscript

fixed_fields : when operators need auxilliray data fields (e.g. grid, mesh, mask)
-----------------------------------------------------------------------------------

And you may need to tell how an operator will receive some fixed fields
'behind the curtain' (in addition to the datasets, which are provided
as arguments)

.. autofunction:: climaf.operators.fixed_fields


cmacro : define a macro  
-----------------------------------------

.. autofunction:: climaf.cmacros.cmacro

cens : define an ensemble of objects
---------------------------------------------------

.. autoclass:: climaf.classes.cens



