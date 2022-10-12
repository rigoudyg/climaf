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

cvalue : get the scalar value of a CliMAF object (at a given index)
-------------------------------------------------------------------

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

.. automodule:: climaf.chtml
   :noindex:

.. autofunction:: climaf.chtml.header
   :noindex:

.. autofunction:: climaf.chtml.trailer
   :noindex:

.. autofunction:: climaf.chtml.section
   :noindex:

.. autofunction:: climaf.chtml.open_table
   :noindex:

.. autofunction:: climaf.chtml.close_table
   :noindex:

.. autofunction:: climaf.chtml.open_line
   :noindex:

.. autofunction:: climaf.chtml.close_line
   :noindex:

.. autofunction:: climaf.chtml.line
   :noindex:

.. autofunction:: climaf.chtml.link
   :noindex:

.. autofunction:: climaf.chtml.link_on_its_own_line
   :noindex:

.. autofunction:: climaf.chtml.cell
   :noindex:

.. autofunction:: climaf.chtml.fline
   :noindex:

.. autofunction:: climaf.chtml.flines
   :noindex:

.. autofunction:: climaf.chtml.vspace
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

ccost : provide compute cost for an object
-------------------------------------------

.. autofunction:: climaf.cache.ccost
