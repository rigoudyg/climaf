.. _standard_operators:

Standard operators and functions
---------------------------------

CliMAF includes a number of 'Standard Operators' and of 'Object Functions', which implement more or less basic climate
diagnostics or utilities:

  - All do return CliMAF objects. 
  - Operators are implemented as external scripts or binaries, while 'object functions' are implemented as python
    functions.
  - operators can be used to define derived variables using function :py:func:`~climaf.operators_derive.derive`, while 'object
    functions' cannot


Other functions exists, which do not return CliMAF objects (and are not called 'object functions') - see :doc:`API`

The set of standard operators grows with scientists contributions (see :ref:`how_to_contribute_a_script`). They are
documented here, through individual documentation files in
`REStructured Text format <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ and following
:download:`this example <scripts_template.rst>` which renders :doc:`as shows here <scripts_template>`.  For each
operator, the content of the doc file is also made available in the Python on-line help (see
:ref:`how_to_list_operators`).

Documented operators and 'object functions' as of today:

 - arithmetic operations provided as 'object functions':
    - :py:func:`~climaf.functions.fadd`
    - :py:func:`~climaf.functions.fsub`
    - :py:func:`~climaf.functions.fmul`
    - :py:func:`~climaf.functions.fdiv`
    - :py:func:`~climaf.functions.apply_scale_offset`

 - arithmetic operations provided as operators:
    - :doc:`scripts/plus`
    - :doc:`scripts/minus`
    - :doc:`scripts/multiply`
    - :doc:`scripts/divide`

 - swiss knives |sk|:
    - :doc:`scripts/ccdo`
    - :doc:`scripts/ccdo2`
    - :doc:`scripts/ccdo_ens`

 - climate data operators:
    - spatial operations:
        - :doc:`scripts/llbox`
        - :doc:`scripts/space_average`
        - object function :py:func:`~climaf.functions.zonmean`
    - regridding:
        - :doc:`scripts/regrid`
        - :doc:`scripts/regridn`
    - :doc:`scripts/regridll`
        - object function :py:func:`~climaf.functions.lonlatpres_interpolation`
        - :doc:`scripts/ml2pl`
    - object functions computing a difference with regridding (typically to compute model biases):
        - :py:func:`~climaf.functions.diff_regrid`
        - :py:func:`~climaf.functions.diff_regridn`
        - :py:func:`~climaf.functions.diff_zonmean`
    - temporal operations:
        - :doc:`scripts/time_average`
        - object function :py:func:`~climaf.functions.clim_average`
        - object function :py:func:`~climaf.functions.annual_cycle`
    - statistical operators:
        - :doc:`scripts/cLinearRegression`
    - Others:
        - :doc:`scripts/slice`
        - :doc:`scripts/mask`
        - :doc:`scripts/ncpdq`

 - operators for creating figures:

     .. note:: Overview on the output format to be used for 'plot' and 'curves' operators w.r.t. figure trimming:
	       
           - If you want a **PNG** figure, **you just have to call 'plot' or 'curves'**, and argument 'trim' allows to
             remove extra white space. Note that resolution unit is in pixels
		 
           - If you want a **PDF** or **EPS** output figure, **you may need a further step** to remove extra white
             space: you have to use 'cpdfcrop' or 'cepscrop' operator (which are slow) respectively, after the figure
             plot. Note that resolution unit is in inches or using a standard paper size by name
		 
.. _note_on_figure_pages:

     .. note:: Overview on method to create **a page with several CliMAF figures**:

           - :py:func:`~climaf.classes.cpage`: this operator creates a PNG or PDF page of figures array using
             'ImageMagick', figures adjustment in the page is adapted to figures size. If you use 'cpage', you don't
             need any pre-processing because:
    
         - 1/ argument 'fig_trim' allows to trim extra white space of each figure;
         - 2/ argument 'page_trim' allows to trim extra white space for the page

           - :py:func:`~climaf.classes.cpage_pdf`: this operator creates a PDF page of figures array using 'pdfjam',
             figures adjustment in each array cell is automatically centered, you can't adjust figures differently.
             So if you use 'cpage_pdf', you may need to do pre and post-treatment because:
		 
         - 1/ there is no argument 'fig_trim' allowing you to trim extra white space when generating pdf figures, so
           you must apply 'cpdfcrop' before cpage_pdf (on all figures)
         - 2/ there is no argument 'page_trim' allowing you to trim extra white space when generating the page, so you
           must use 'cpdfcrop' on its output
    
         **So, to create an array of figures:**
	       
           - If you want an **PNG** output figure: you should use **'cpage'**. If quality is not sufficient, increase
             resolution of each figure (with argument 'resolution' of 'curves' or 'plot' operator) and also page
             resolution (with arguments 'page_width' and 'page_height' of 'cpage')

           - If you want an **PDF** output figure: you can use either 'cpage_pdf' or 'cpage':

         - **'cpage_pdf'** is highly recommended
         - if you want to have more control on figures adjustment in the page, use **'cpage'** and increase resolution
           of each figure and also of output page

.. _graphic_operators:

    - :doc:`scripts/plot`
    - :doc:`scripts/plotmap`
    - :py:func:`~climaf.plot.plot_params.plot_params`
    - :doc:`scripts/curves`
    - :doc:`scripts/ensemble_ts_plot`
    - :py:func::`~climaf.function.ts_plot`
    - :doc:`scripts/hovm`
    - :py:func:`~climaf.plot.plot_params.hovm_params`
    - :doc:`scripts/cpdfcrop`
    - :doc:`scripts/cepscrop`

 - example for two outputs:
    - :doc:`scripts/mean_and_std`

.. toctree::
   :maxdepth: 1

   cdftools

.. |sk| image:: swiss_knife_50.png

Albeit this is not a proper practice, **some more operators may exist in your CliMAF release** which would not be
documented here. Please see :ref:`how_to_list_operators` for such cases

A name-sorted list:

.. toctree::
  :glob:

  /scripts/*
