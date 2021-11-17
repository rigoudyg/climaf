:orphan:

-----------------------------------------
Functions for managing/viewing results
-----------------------------------------

.. default-domain:: python

There are a few functions for managing CliMAF results

cfile : get the file value of a CliMAF object 
----------------------------------------------

.. autofunction:: climaf.driver.cfile 
   
efile : create the file for an ensemble of CliMAF objects
---------------------------------------------------------- 

.. autofunction:: climaf.driver.efile 

cMA : get the Masked Array value of a CliMAF object 
------------------------------------------------------

.. autofunction:: climaf.driver.cMA

cvalue : get the scalar value of a CliMAF scalar object 
--------------------------------------------------------

.. autofunction:: climaf.driver.cvalue

cshow : dump an object or display a 'figure'
--------------------------------------------

.. autofunction:: climaf.driver.cshow

cpage : create an array of figures (output: 'png' or 'pdf' figure)
-------------------------------------------------------------------

.. autoclass:: climaf.classes.cpage

cpage_pdf : create an array of figures (output: 'pdf' figure)
-------------------------------------------------------------

.. autoclass:: climaf.classes.cpage_pdf

html : create an html index, with tables of links to figures
------------------------------------------------------------

.. automodule:: climaf.html
   :noindex:

.. autofunction:: climaf.html.header
   :noindex:

.. autofunction:: climaf.html.trailer
   :noindex:

.. autofunction:: climaf.html.section
   :noindex:

.. autofunction:: climaf.html.open_table
   :noindex:

.. autofunction:: climaf.html.close_table
   :noindex:

.. autofunction:: climaf.html.open_line
   :noindex:

.. autofunction:: climaf.html.close_line
   :noindex:

.. autofunction:: climaf.html.line
   :noindex:

.. autofunction:: climaf.html.link
   :noindex:

.. autofunction:: climaf.html.link_on_its_own_line
   :noindex:

.. autofunction:: climaf.html.cell
   :noindex:

.. autofunction:: climaf.html.fline
   :noindex:

.. autofunction:: climaf.html.flines
   :noindex:

.. autofunction:: climaf.html.vspace
   :noindex:
   

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

cprotect : protect a result's file against cdrop and craz
---------------------------------------------------------

.. autofunction:: climaf.cache.cprotect

