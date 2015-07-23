-----------------------------------------
Functions for managing/viewing results
-----------------------------------------

.. default-domain:: python

There are a few functions for managing CliMAF results

cfile : get the file value of a CliMAF object 
----------------------------------------------

.. autofunction:: climaf.driver.cfile 

cMA : get the Masked Array value of a CliMAF object 
------------------------------------------------------

.. autofunction:: climaf.driver.cMA

cshow : dump an object or display a 'figure'
--------------------------------------------

.. autofunction:: climaf.driver.cshow

cpage : create an array of figures
--------------------------------------------

.. autoclass:: climaf.classes.cpage


html : create an html index, with tables of links to figures
------------------------------------------------------------

.. automodule:: climaf.html

.. autofunction:: climaf.html.html_header

.. autofunction:: climaf.html.html_section

.. autofunction:: climaf.html.html_open_table

.. autofunction:: climaf.html.html_table_line

.. autofunction:: climaf.html.html_table_lines

.. autofunction:: climaf.html.html_close_table

.. autofunction:: climaf.html.html_trailer


clist : tell what's in cache, and much more
-------------------------------------------

.. autofunction:: climaf.cache.clist

cls : tell what's in cache
---------------------------------

.. autofunction:: climaf.cache.cls

crm : remove some files from cache
-------------------------------------

.. autofunction:: climaf.cache.crm

cdu : disk cache usage
---------------------------------

.. autofunction:: climaf.cache.cdu

cwc : count some files in cache
---------------------------------

.. autofunction:: climaf.cache.cwc

craz : reset cache
---------------------

.. autofunction:: climaf.cache.craz

cdrop : erase a result's file
--------------------------------

.. autofunction:: climaf.cache.cdrop



