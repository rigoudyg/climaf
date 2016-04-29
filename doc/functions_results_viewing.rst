
functions for inspecting data
====================================================================================================

summary : describe files associated with a dataset
---------------------------------------------------
 - :doc:`functions/summary`

ncdump : dump file header
------------------------------
 - :doc:`scripts/ncdump`

cshow : dump an object 
------------------------------------------------

.. autofunction:: climaf.driver.cshow
   :noindex:


functions to create images, and to display datasets and images
====================================================================================================

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


plot_params : get plot parameters for a variable and a context
----------------------------------------------------------------

.. autofunction:: climaf.plot.plot_params.plot_params

cshow : display a figure using 'display'
---------------------------------------------

.. autofunction:: climaf.driver.cshow
   :noindex:

functions for assembling figures in pages 
====================================================================================================

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
====================================================================================================

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

.. autofunction:: climaf.html.cell
   :noindex:

.. autofunction:: climaf.html.fline
   :noindex:

.. autofunction:: climaf.html.flines
   :noindex:

.. autofunction:: climaf.html.vspace
   :noindex:
   
