Functions for inspecting data
===============================================================================

summary : describe files associated with a dataset
---------------------------------------------------
.. autofunction:: climaf.functions.summary

ncdump : dump file header
------------------------------
 - :doc:`scripts/ncdump`

cshow : dump an object 
------------------------------------------------

.. autofunction:: climaf.driver.cshow
   :noindex:


Functions to create images, and to display datasets and images
================================================================================

Warning
------------
**SEE ALSO** :ref:`the graphic operators <graphic_operators>`  and
especially :doc:`scripts/plot`

ncview: display a dataset 
-----------------------------
 - :doc:`scripts/ncview`

iplot : Interactive version of cshow() for display in IPython Notebooks
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.iplot


implot : Interactive version of plot() for display in IPython Notebooks
------------------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.implot


ts_plot : Shortcut for ensemble_ts_plot
-------------------------------------------------------------------------------------

.. autofunction:: climaf.functions.ts_plot


plot_params : get plot parameters for a variable and a context
----------------------------------------------------------------

.. autofunction:: climaf.plot.plot_params.plot_params


hovm_params : provide some SST/climate boxes for plotting Hovmoller diagrams 
-----------------------------------------------------------------------------

.. autofunction:: climaf.plot.plot_params.hovm_params


cshow : display a figure using 'display'
---------------------------------------------

.. autofunction:: climaf.driver.cshow
   :noindex:

Functions for assembling figures in pages 
==============================================================

For choosing between next two fuctnions, see the :ref:`Note on figure pages <note_on_figure_pages>`

cpage : create an array of figures (output: 'png' or 'pdf' figure)
-------------------------------------------------------------------

.. autoclass:: climaf.classes.cpage
   :noindex:

cpage_pdf : create an array of figures (output: 'pdf' figure)
-------------------------------------------------------------

.. autoclass:: climaf.classes.cpage_pdf
   :noindex:


html : package for creating an html index, with tables of links to figures
--------------------------------------------------------------------------

.. automodule:: climaf.html

.. autofunction:: climaf.html.header

.. autofunction:: climaf.html.trailer

.. autofunction:: climaf.html.section

.. autofunction:: climaf.html.open_table

.. autofunction:: climaf.html.close_table

.. autofunction:: climaf.html.open_line

.. autofunction:: climaf.html.close_line

.. autofunction:: climaf.html.line

.. autofunction:: climaf.html.link

.. autofunction:: climaf.html.link_on_its_own_line

.. autofunction:: climaf.html.cell

.. autofunction:: climaf.html.fline

.. autofunction:: climaf.html.flines

.. autofunction:: climaf.html.vspace

