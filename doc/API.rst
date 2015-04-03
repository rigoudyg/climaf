.. _api:

-----------------------------
Application Program Interface
-----------------------------
.. default-domain:: python

.. automodule:: climaf.api

**Function names used as section titles are those defined by** ``climaf.api`` **and
can be used 'as is' after executing**::

>>> from climaf.api import *

For documented standard operators see  :ref:`standard_operators` ; for the other ones, see :ref:`how_to_list_operators`


dataloc
-------

.. autoclass:: climaf.dataloc.dataloc

cdataset
----------

.. autoclass:: climaf.classes.cdataset

ds
------

.. autofunction:: climaf.classes.ds


cdef
------

.. autofunction:: climaf.classes.cdefault

cscript
----------------------
 
.. autoclass:: climaf.operators.cscript

cfile
------

.. autofunction:: climaf.api.cfile 

cshow
------

.. autofunction:: climaf.api.cshow

cMA
------

.. autofunction:: climaf.api.cMA

clog
------

.. autofunction:: climaf.clogging.clog 

clog_file
----------

.. autofunction:: climaf.clogging.clog_file 

cdump
------

.. autofunction:: climaf.cache.cdump 

craz 
---------------------

.. autofunction:: climaf.cache.creset

csave 
---------------------

.. autofunction:: climaf.cache.csync


init_period
----------------------

This function should not be called directly ; it is presented here
mainly for documenting the syntax of the strings describing a period
of time


.. autofunction:: climaf.period.init_period

selectLocalFiles 
----------------------------

This function should not be called directly ; it is presented here mainly for documenting the list of
organizations it can handle for function  :py:class:`~climaf.dataloc.dataloc`

.. autofunction:: climaf.dataloc.selectLocalFiles


selectGenericFiles 
----------------------------

This function should not be called directly ; it is presented here mainly for documented  the syntax of
argument ``url`` of function :py:class:`~climaf.dataloc.dataloc` when
``organization`` is set to ``generic``

.. autofunction:: climaf.dataloc.selectGenericFiles


Some useful variables
------------------------
**cpath**

.. autodata:: climaf.api.cpath

**cdefaults**

.. autodata:: climaf.classes.cdefaults
