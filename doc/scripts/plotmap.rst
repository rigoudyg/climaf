plotmap: plot a map showing up to 5 fields with varied rendering
-----------------------------------------------------------------------------------------------------------------------------------

Plot a map showing any combination of various fields : one color-shaded, one by isolines, one vector field, and/or up to two pattern-shaded (hatched). It allows to tune various graphic attributes.

``Plotmap`` intends to replace operator ``plot``, albeit only for maps. Hence, its interface is quite compatible. Il also includes a novel interface.

It is implemented using module ``scripts/plotmap.py``, based on `Matplotlib <https://matplotlib.org/>`_ , `Cartopy <https://scitools.org.uk/cartopy/>`_ , and `GeoCat Viz >https://geocat-viz.readthedocs.io>`_

A :download:`dedicated notebook (Getting started with plotmap) <../../examples/Getting-started-with-plotmap.html>` allows to get started with its use. :download:`Another notebook (plotmapdemo) <../../examples/plotmapdemo.html>` includes more examples for each functionnality.


.. topic:: Table of contents:

  - :ref:`Inputs <inputs>`
  - :ref:`Optional arguments <optional_arguments>`

    - :ref:`General arguments<general_opt_args>`
    - :ref:`Advanced general arguments<general_adv_args>`
    - :ref:`Optional arguments common to all fields <all_field_args>`
    - Field specific arguments 
	
      - :ref:`Colored  field <main_field_opt_args>`
      - :ref:`Colored field and/or contoured field  <main_and_aux_field_opt_args>`  
      - :ref:`Contoured field <aux_field_opt_args>`
      - :ref:`Vectors <vectors_opt_args>`
      - :ref:`Pattern-shaded fields <shade_opt_args>`
      
  - :ref:`Output <plotmap_outputs>`
  - :ref:`Interface differences with plot <differences_with_plot>`
  - :ref:`Implementation <implementation>`

 
.. _references:

**References**: 

.. _provider:

**Provider / contact**: climaf at meteo dot fr

.. _inputs:

**Inputs** (in the order of CliMAF call): 

  - a dataset for a color-shaded field 
  - a dataset for a contoured field (shown by isolines)
  - 2 datasets for the components of a vector field 
  - 1 or 2 datasets for scalar fields shown as pattern-shaded (or hatched)

Each input field is optional and can be replaced by an empty string (or simply neglected if there is no further input field to provide). Examples ::

     >>> colored = ds(....)
     >>> plotmap(colored, title='title')
     
     >>> contoured = ds(....)
     >>> plotmap('', contoured, title='title')
      
     >>> patterned = ds(....)
     >>> plotmap(colored, contoured, '', '', patterned, title='title')  
      
     >>> patterned2 = ds(....)
     >>> plotmap('', '', '', '', patterned, patterned2, title='title')
     

.. _optional_arguments:

**Optional arguments** 

.. _general_opt_args:

**General and basic arguments**:

  - ``title``: string for graphic title; default: no title
  - ``title_options`` : for tuning title and subtitle : a dict of additional arguments/values for the call to `GeoCat-viz function set_titles_and_labels <https://geocat-viz.readthedocs.io/en/latest/user_api/generated/geocat.viz.util.set_titles_and_labels.html>`_; e.g. ``title_options = dict(lefttitlefontsize=18)``
  - ``units`` : string for upper right corner; default is to use the CF metadata of the first provided field, if available
      
.. _proj:

  - ``proj``: which geographic projection for the map. You can use :

         - a label known to Cartopy, such as ``PlateCarree`` or ``Lambert``; see
	   `Cartopy's list <https://scitools.org.uk/cartopy/docs/latest/reference/crs.html#list-of-projections>`_. You may then wish to set ``proj_options`` (see below)
         - "NH"/"SH" for northern/southern hemisphere polar stereographic (can be followed by the limiting
	   latitude of the map (e.g. "NH40" for a limiting latitude of 40 degrees)
	 - a string using the symbolic name of one of the input fields/dataset, among ``'colored'``, ``'contoured'``, ``'vectors'``, ``'shaded'``, ``'shade2'``; the geographic projection of that field will then be used for the map; there are also shortcuts : ``'clr', 'cnt', 'vec', 'shd', 'shd2'``
	 - the path for a NetCDF file which includes metadata describing the projection according to the `CF-convention <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#appendix-grid-mappings>`_; in that case, a value is not necessary for ``proj_options`` 
         - default value is ``'PlateCarree'`` (`described here <https://scitools.org.uk/cartopy/docs/latest/reference/projections.html#platecarree>`_)

  - ``proj_options``: a dict of arguments for the definition of the projection class, if needed, such as ``{ 'central_longitude' : 0}``. See relevant entry in `Cartopy's projections list <https://scitools.org.uk/cartopy/docs/latest/reference/crs.html#list-of-projections>`_. Default is to set ``central_longitude`` to 180 when ``proj`` has a default value 


  - ``focus``: set it to 'land' (resp. 'ocean') if you want to plot only on land (resp. ocean)
    
  - ``format``: graphic output format, either 'show', 'png', 'pdf' or 'eps'; default: 'png'. Value 'show' means that matplotlib will open a window showing the plot, rather than creating an output file; this does not work when invoked from a notebook; also, you have to close the window for going on with CliMAF
  - ``trim``: set it to False if you do not want to crop all the surrounding extra white space.
  - ``dpi``: integer for ouput image resolution, in dots per inch
  - ``resolution``: string for output image sizes

    - if format is "png", this specifies the width and height of resultant image in pixels as e.g. 800x1200;
      default: 1250x1250
    - if format is "pdf" or "eps", the units is inches (default resolution is 100 dots per inch - dpi);
      default : 8.5x11
  - ``date``, ``time``, ``level``: for selecting date, time and/or level. These arguments apply on all fields which have time and/or level dimension (while another syntax allows to disctinct selection among the various input fields - see :ref:`field-specific arguments<all_field_args>`). Set it to:

    - for ``time`` and ``level``:

      - an integer if you want to select an index (first index is 0), 
      - or a float if you want to select closest coordinate value. Warning: For ``time``, if the value has more than six digits, there is big rounding errors. 
 
    - for ``date``:

      - a string in the format 'YYYY', 'YYYYMM', 'YYYY-MM', 'YYYYMMDD', 'YYYY-MM-DD' or 'YYYYMMDDHH' e.g.: ``date=1981-01-31`` .

    - default: select first index for all dimensions but horizontal ones
    
    Remark: ``time`` and ``date`` arguments are incompatible;
	
  - ``xpolyline``, ``ypolyline``: for adding a polyline to the plot; set ``xpolyline`` and ``ypolyline`` to a list of
    the same length containing the longitude and latitude coordinates of the polyline, respectively. Lists are
    either Pyhton lists or strings with values separated by blanks.  e.g.:
    ``xpolyline = "-90.0 -45.0 -45.0 -90.0 -90.0"``, ``ypolyline = [ 30.0, 30.0, 0.0, 0.0, 30.0]``.
    Polylines are internally implemented using :ref:`plt_methods <plt_methods>` with method ``plot``
  - ``polyline_options``: a dict of arguments for function `matplotlib.pyplot.plot <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot>`_, which applies to the
    polyline. Example : ``dict(color='green', marker='o')``

.. _general_adv_args:

**General advanced arguments** : a number of advanced arguments allow to fine tune the calls to the geocat-viz, cartopy or matplotlib routines that build the plot  :

  - ``axis_methods``: allows to call methods of the `cartopy GeoAxes class <https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.mpl.geoaxes.GeoAxes.html#cartopy.mpl.geoaxes.GeoAxes>`_. Syntax is a dict which keys are method names and values are arguments/values dicts. e.g. ``axis_methods={'add_feature': {'feature': 'LAND', 'facecolor': 'black', 'zorder': 1}}``.

    Signaled methods are : annotate, add_feature, gridlines, coastlines, set_xticks, set_yticks. 

    In the case of method ``add_feature``, the feature name will be interpreted as a `cartopy.feature <https://scitools.org.uk/cartopy/docs/latest/reference/feature.html>`_;

    Method ``clabel`` (in matplotlib.axes.Axes) allows to label contours (see `axes.clabel doc <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.clabel.html#matplotlib.axes.Axes.clabel>`_); it uses a first argument (the contours set) which is automatically provided by plotmap

    Also, using ``zorder=1`` allows to have the feature before the colored or contoured plot.

.. _plt_methods:

  - ``plt_methods`` : allows to call methods of `matplolib.pyplot <https://matplotlib.org/stable/api/pyplot_summary.html>`_, with the same syntax as for ``axis_methods``. e.g. ``plt_methods={ 'text': {'x':-120, 'y': 45, 's': 'mytext', 'horizontalalignment': 'left'}}``

    Method ``clabel`` (in matplotlib.pyplot) allows to label contours (see `pyplot.clabel doc <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.clabel.html#matplotlib.pyplot.clabel>`_); it uses a first argument (the contours set) which is automatically provided by plotmap

    
  - ``gv_methods`` : allows to call `GeoCat-viz methods <https://geocat-viz.readthedocs.io/en/latest/user_api/index.html>`_ . e.g. : ``gv_methods={'add_major_minor_ticks': { 'labelsize':'small', 'x_minor_per_major':2 } }``

  - ``figure_options`` : allows to provide additional arguments to the figure `creation routine matplotlib.pyplot.figure <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html>`_

  - ``savefig_options``: allows to provide additional arguments to the figure `write routine matplotlib.pyplot.savefig <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html>`_

    
.. _all_field_args:

**Optional arguments common to all fields** :

A number of arguments are available for all fields. Their name is built with a prefix for the field type, and a suffix for the argument type, e.g. ``colored_map_min`` is the argument name for the ``min`` for the colored map field.

There are shortcuts for prefixes and for argument types, e.g. ``clr`` for ``colored_map`` and ``n`` for ``min`` which allows for the argument shortcut ``clrn`` for  ``colored_map_min``

Prefixes are : ``colored_map`` (``clr``), ``contours_map`` (``cnt``), ``vectors_map`` (``vec``), ``shaded_map`` (``shd``) and ``shade2_map`` (``shd2``)

The argument type suffixes are (with shortcut in parenthesis) :

  - ``transform (t)``, ``transform_options (to)`` : which are the geographic projection and its details for the provided field data; if missing, plotmap will try to get it from data file metadata and will use ``PlateCarree`` as a default; for syntax details see :ref:`arguments proj and proj_options<proj>`; you may aso use keyword ``no_remap`` in order to ensure that no data re-mapping will take place (but you have then to ensure that the data uses the map geographic projection set by ``proj``)
    
  - ``min (n)``, ``max (x)`` : minimum and maximum values to show; doesn't apply to vectors
    
  - ``scale  (s)``, ``offset (o)`` :  for scaling the field (x -> x*scale + offset); ``offset`` doesn't apply to vectors
    
  - ``selection_options (so)``: for driving the selection of data at given dimension values; you can actually invoke any method associated to the xarray DataArray, such a ``sel`` or ``isel``, and provide it with arguments in a dict such as ``{'sel' : {'time': '1850-02'}}``; default selection is driven by args ``level``, ``date`` and ``time`` (see above)


.. _main_field_opt_args:

**Colored field (first field)**:

That field is (by default) drawned by `Cartopy's contourf function <https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.mpl.geoaxes.GeoAxes.html#cartopy.mpl.geoaxes.GeoAxes.contourf>`_, which basically calls `Maplotlib's contourf() <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contourf.html#matplotlib.axes.Axes.contourf>`_

  - colormap and its interpretation :

   - ``color`` ( or ``cmap``, or ``colored_map_cmap``) : either :

       - name of a `Ncl colormap <https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml#Aid_in_color_blindness>`_ 
       - the name of a `matplotlib colormap <https://matplotlib.org/stable/users/explain/colors/colormaps.html#sphx-glr-users-explain-colors-colormaps-py>`_
       - a list of `matplotlib color names or values <https://matplotlib.org/stable/users/explain/colors/colors.html#sphx-glr-users-explain-colors-colors-py>`_  defining a custom color map. e.g. ``color =  [ 'b', 'white' , 'black' , 'RoyalBlue' , 'LightSkyBlue' , 'PowderBlue' , (0.1, 0.2, 0.5) ]``. For compatibility with ``plot``, a string with color names separated by commas is also valid.
       - default is Ncl's 'BlueDarkRed18'.
	 
   - and either :

     - ``min``, ``max``, ``delta``: min and max values and levels when applying the colormap (prefix ``colored_map_`` for min and max is implicit)
     - or ``levels`` (synonyms:``colors``, ``colored_map_levels``, ``clrl``): list of levels used when applying colormap e.g. ``colors="260 270 280 290"`` or ``colors=[260, 270, 280, 290]``
     - default is ``contourf()`` default

  - ``scale``, ``offset``: for scaling the colored map field (x -> x*scale + offset); default is no scaling
  - ``print_time`` : set it to True in order to add data time in the upper left caption
  - ``vcb``: a logical value for setting the colorbar vertical; default to True
  - ``colorbar_options`` : a dict for arguments/values for routine `colorbar <https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.colorbar>_`, which allows to finely tune colorbar rendering
  - ``colored_map_engine`` (or ``clre``) : the Cartopy routine used for creating the colored map, defaut is ``'contourf'``, and you may choose ``'pcolormesh'``, which do not interpolate across grid cells, and which may be more robust for some cases (e.g. Nemo tri-polar grid)
  - ``colored_map_engine_options`` (or ``clreo``) : additional arguments for the colred map engine routine
  - ``colored_map_transform, colored_map_transform_options, colored_map_selection_options, colored_map_min, colored_map_max, colored_map_scale, colored_map_offset`` : see :ref:`the common arguments<all_field_args>`

    
.. _main_and_aux_field_opt_args:

**Colored field and/or contoured field**:

  - ``contours``:

    - *If providing only a colored field:*

      - set it to 1 if you want to draw contours which follow color filled contours, or
      - set it to a list of levels used for drawing contours of the colored field at other levels; e.g. ``contours=[230, 240, 250]``

    - *If providing both a colored field and a contoured field* only the contours of the latter are drawn :
      
      - set it to a list of levels used when drawing contours of the contoured (second) field e.g. ``contours=[230, 240, 250]``; this is then a synonym for ``contours_map_levels``
      - default : see matplotib.pyplot.contour

.. _aux_field_opt_args:

**Contoured field (second arg)**:

That field is (by default) drawned by `Cartopy's contour function`_, which basically calls `Maplotlib's contour() <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contour.html#matplotlib.axes.Axes.contour>`_

  - ``contours (contours_map_levels, cntl)`` : see just above
  - ``contours_map_colors (cntc)`` : value is passed as argument ``color`` to `Cartopy's contour function <https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.mpl.geoaxes.GeoAxes.html#cartopy.mpl.geoaxes.GeoAxes.contour>`_ . Default value is ``'black'``.
  - ``contours_map_transform (cntt), contours_map_transform_options (cntto), contours_map_selection_options (cntso), contours_map_min (cntn), contours_map_max (cntx), contours_map_scale (cnts), contours_map_offset (cnto)`` : see :ref:`the common arguments<all_field_args>`
  - for labeling contours, use argument :ref:`plt_methods <plt_methods>` and method `clabel <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.clabel.html#matplotlib.pyplot.clabel>`_


.. _vectors_opt_args:

**Vectors field (3rd and 4th args)**:

  - ``vectors_map_type (vecty)``: choose type of vector representation : by arrow (``'quiver'``, default) or by barbs (``'barbs'``), or by streamlines (``'streamplot'``)
  - ``vectors_map_gridsizes (vecg)`` : allow to tune the number of arrows or barbs either along the x-axis by providing one integer value, or along both axes by providing a tuple of integers; in the first case, the value along y-axis is computed using the map aspect ratio
  - ``vectors_map_options (veco)`` : can host additional arguments for the vectors rendering routine; refer to the documentation of the chosen function : `quiver for arrows <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html#matplotlib.pyplot.quiver>`_, `barbs <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.barbs.html#matplotlib.pyplot.barbs>`_ or `streamplot <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.streamplot.html#matplotlib.pyplot.streamplot>`_. Example : ``veco={'color':'blue', 'headwidth':2.5, 'headlength':4}``
  - ``vectors_map_transform (vect), vectors_map_transform_options (vecto), vectors_map_selection_options (vecso), vectors_map_scale (vecs)`` : see :ref:`the common arguments<all_field_args>`

.. _shade_opt_args:

**Pattern-shaded (or hatched) fields (5th and/or 6th argument)**:

Arguments are the same for both fields, except that ``shaded`` should be changed to ``shade2`` for the next field.

  - ``shaded_map_levels (shdl)`` : list of levels between which shading/hatching occurs, e.g. ``[210, 240, 270, 285, 300]``
  - ``shaded_map_hatches (shdh)`` : hatching patterns list, which is reused circularly if needed  (see `hatch style reference <https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html>`_
  - ``shaded_map_transform (shdt), shaded_map_transform_options (shdto), shaded_map_min (shdn), shaded_map_max (shdx), shaded_map_scale (shds), shaded_map_offset (shdo)`` : : see :ref:`the common arguments<all_field_args>`
    

.. _plotmap_outputs:

**Outputs** :
  - main output: a PNG or PDF or EPS figure, except if ``show`` is True


.. _differences_with_plot:

**Interface differences with plot** :

Here are the main differences for some arguments which are common with ``plot`` :

  - positionnal arguments (which represent datasets) : they are not exactly the same : pattern-shaded datasets/fields are located after vector component fields, and so clearly separated from contoured dataset/field
  - xpolyline and ypolyline lists of coordinates : when using the string syntax, separator is blank, not comma + blank
  - vector datasets/fields: rotation is not yet supported
    
.. _implementation:

**Implementation**:  Underlying script plotmap.py uses matplotlib, cartopy and geocat-viz libraries. 
    
  
