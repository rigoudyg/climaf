-----------------------------
Application Program Interface
-----------------------------
.. default-domain:: python

.. automodule:: api

Function names used as section titles are those defined by ``climaf.api`` and
can be used 'as is' after executing ``from climaf.api import *``

For documented standard operators see  :ref:`standard_operators` ; for the other ones, see :ref:`how_to_list_operators`


dataloc
-------

.. autoclass:: dataloc.dataloc

cdataset
----------

.. autoclass:: classes.cdataset

ds
------

.. autofunction:: classes.ds


cdef
------

.. autofunction:: classes.cdefault

cscript
----------------------
 
.. autoclass:: climaf.operators.cscript

cfile
------

.. autofunction:: api.cfile 

cMA
------

.. autofunction:: api.cMA

clog
------

.. autofunction:: api.clog 

cdump
------

.. autofunction:: cache.cdump 

craz 
---------------------

.. autofunction:: cache.creset

csave 
---------------------

.. autofunction:: cache.csync


init_period
---------------

.. autofunction:: period.init_period

Some useful variables
------------------------
**cpath**

.. autodata:: api.cpath

**cdefaults**

.. autodata:: classes.cdefaults
