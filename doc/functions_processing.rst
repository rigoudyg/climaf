--------------------------------------------------------
Functions for processing data
--------------------------------------------------------

.. default-domain:: python

Standard operators
---------------------

For documented standard operators see  :ref:`standard_operators`  

Functions returning CliMAF objects 
---------------------------------------
For functions which looks like CLiMAF operators, see : :doc:`functions_objects`


Non-standard operators
-----------------------

See :ref:`how_to_list_operators`


--------------------------------------------------------------------------------------------------------
Functions for creating new processing functions, or tuning their behaviour
--------------------------------------------------------------------------------------------------------


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

.. autofunction:: climaf.cmacro.macro


