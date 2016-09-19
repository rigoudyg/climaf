hovm : plot Hovmöller diagrams on a given or global domain (SST/climate boxes, ... )
-------------------------------------------------------------------------------------

Plot Hovmöller diagrams  on a given or global domain using NCL, and
allowing for tuning a number of graphic attributes. Some SST/climate
boxes are available to be passed to this operator (see below in
:ref:`Optional arguments <climate_boxes>`). 

The various cases are:

- Time vs. Lon (or reverse) : if exists, mean
  or section at a given point on Lat, and section at a given point on
  height, or    
- Time vs. Lat (or reverse) : if exists, mean
  or section at a given point on Lon, and section at a given point on
  height, or   
- Time vs. Height (or reverse) : if exists,
  mean or section at a given point on Lat/Lon. 

Remark: If data grid is curvilinear, you have to do a projection on a
rectilinear grid before using ``hovm``, otherwise the mean on Lat or
Lon axis will be rough/wrong.  

**References** : https://www.ncl.ucar.edu/Applications/time_lon.shtml

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - a dataset can be up to 4-dimensional

Warning: Order of all data dimensions is supposed to be time, height, lat, lon. 

**Mandatory arguments** :
 
  - ``mean_axis``: set it to "Lat" or "Lon" if you want a mean on one
    of these axis or set it to "Point" if you want a section on one or
    more points (passed with ``xpoint``, ``ypoint``, ``zpoint``; see
    further below).  
    
    Remark : If rank of field is 2, ``mean_axis`` becomes an optional
    argument because this script will plot supplied coordinates. 

  - ``xpoint``, ``ypoint``, ``zpoint``: points for longitude, latitude
    and height respectively where section(s) will be made. These
    arguments apply on all fields (from 3D to 4D) which have
    corresponding dimension, so many arguments as upper number of
    dimensions for two is needed (number of remaining dimensions after
    an average on the latitude or the longitude axis if there was
    one). Set it to,   

    - an integer if you want to select an index (first index is 0),
    - or a float if you want to select closest coordinate value.

    Remark: If ``mean_axis`` is set to "Point", one or more of these
    arguments is mandatory depend on field dimension. On the other
    hand, if ``mean_axis`` is set to "Lat" or "Lon", these arguments
    are not necessary mandatory depend on field dimension.

**Optional arguments** :

  - ``mean_axis``: mandatory argument which can be optional (see
    above)

  - ``xpoint``, ``ypoint``, ``zpoint``: arguments which can be
    optional (see above) 

.. _climate_boxes:

  - ``latS``, ``latN``, ``lonW``, ``lonE``: domain for plot and for
    averaged axis (if ``mean_axis`` is set to "Lat" or "Lon");
    default: all domain (float or string). 
    You can pass SST/climate boxes, available via function
    :py:func:`~climaf.plot.plot_params.hovm_params`. This function
    returns a python dictionary with domain (i.e. ``latS``, ``latN``,
    ``lonW``, ``lonE``) to be passed to ``hovm`` operator with '**'
    (see example :ref:`Climaf call example <climate_boxes_example>`).

  - ``title``: string for graphic title; default: period + domain
    definition

    Remarks: the ~ character has a special meaning in NCL strings. It
    represents a function code. See function codes example page
    http://www.ncl.ucar.edu/Applications/fcodes.shtml for (more)
    examples of function codes. Particularly: 

    - The ~C~ will put a carriage return to the title. By default it
      is left justified. If you need it centered, you will have to add
      spaces.
    - Use a ~Z#~ to resize text in mid-stream. The # refers to the
      percent of normal. 
  
  - ``color``: name of the Ncl colormap to use; see
    e.g. http://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml;
    default (climaf) is 'amwg256'.  
    
  - ``reverse``: set it to True to reverse colormap; default: False.

  - ``scale``, ``offset``: for scaling the input field (x -> x*scale +
    offset); default = 1. and 0. (no scaling) 

  - ``units``: name of the field units; used in the caption; default
    is to use the corresponding CF metadata 

  - ``invXY``: set it to True to invert X axis and Y axis; default: False

  - ``fmt``: a string specifying the format of the tick labels for
    time axis. This string is parsed as follows: the '%' acts as the
    escape character. The single character after every '%' is
    formatted according to the rule described here: 

    https://www.ncl.ucar.edu/Document/Functions/User_contributed/time_axis_labels.shtml

    In case fmt is absent, a minimal algorithm exists which tries to
    determine the format string depending on the time range length. 

  - ``options``: strings for setting NCL graphic resources
    directly. These resources are separated by "|", as e.g. : '
    options="tiMainString=lv|tiXAxisString=longitude" '. These
    resources have higher priority than CliMAF default ones, which are
    : 

    - tiMainString = period + domain definition
    - gsnLeftString = var
    - gsnRightString = (units) if data has "units" attribute else
      "(None)"  
    - gsnCenterString = points where section(s) was(were) done, if any 
    - txFontHeightF = 0.015
    - cnLineLabelFontHeightF = 0.015  
    - cnInfoLabelFontHeightF = 0.01
    - cnFillOn = True
    - cnLinesOn = False
    - cnLineLabelsOn = False          
    - cnMaxLevelCount = 25
    - cnRasterSmoothingOn = True
    - cnFillOpacityF = 0.6 
    - lbLabelFont = "helvetica"
    - gsn[X or Y]AxisIrregular2Log = True   ; set x or y-axis (depend
      on ``invXY`` value) to log scale if the second dimension is a
      z-axis [height]   
    - For time dimension on y-axis or x-axis depend on ``invXY``
      value: 

      - ti[Y or X]AxisString = "Time"
      - tm[Y or X]MajorGrid = True 
      - tm[Y or X]MajorGridThicknessF = 0.5 
      - tm[Y or X]MinorGridThicknessF= 0.25 
    - For second dimension on x-axis or y-axis depend on ``invXY``
      value: 

      - ti[X or Y]AxisString = second dimension name
      - tm[X or Y]MajorGrid = True 
      - tm[X or Y]MajorGridThicknessF = 0.5 
      - tm[X or Y]MinorGrid = True 
      - tm[X or Y]MinorGridThicknessF = 0.25
      - tm[XB or YL]LabelFontHeightF = 0.018 
      - tm[YL or XB]LabelFontHeightF = 0.02
      - tm[XB or YL]TickSpacingF = floattointeger(Xfeatures(2)) where
	Xfeatures = nice_mnmxintvl(min(XArray), max(XArray), 4, False)
	and XArray is the array of values of second dimension
    - To set some "nice" contour levels for field to plot: if
      mnmxint(0).ge.0 where mnmxint = nice_mnmxintvl(min(fld(:,:)),
      max(fld(:,:)), 21, False),  

      - cnLevelSelectionMode = "ManualLevels"
      - cnMinLevelValF  = mnmxint(0) 
      - cnMaxLevelValF  = mnmxint(1)
      - cnLevelSpacingF = mnmxint(2)/2.      

    For more details, see: https://www.ncl.ucar.edu/

  - ``format``: graphic output format, either 'png', 'pdf' or 'eps';
    default: 'png'. For 'png' format, all the surrounding extra white
    space are cropped with optional argument ``trim`` (but not for
    'pdf' or 'eps' format). In case of 'pdf' or 'eps' format, if you
    want to trim extra white space, use 'cpdfcrop' (which is 'pdfcrop'
    tool) or 'cepscrop' operator respectively. 

  - ``trim``: set it to True if you want to crop all the surrounding
    extra white space for 'png' format; default: True. 

  - ``resolution``: string for output image resolution

    - if format is "png", resolution specifies the width and height of
      resultant image in pixels as e.g. 800x1200; default (ncl):
      1024x1024
    - if format is "pdf" or "eps", resolution specifies either the
      width and height of the paper, as above but in inches unit, or a
      standard paper size by name, as e.g. 'A4'. Ncl uses a resolution
      of 72 dots per inch (dpi); default (ncl): 8.5x11 or "letter"
      (<=> 612x792 pixels)

**Outputs** :
  - main output : a PNG or PDF or EPS figure

**Climaf call example** :: For more examples which are systematically
tested, see :download:`hovm.py <../../examples/hovm.py>`  

  >>> # 4D field: ta(time, plev, lat, lon)
  >>> ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1980")

  >>> # Mean on latitude axis: you must set only one point (xpoint, ypoint or zpoint) because rank=4 and a mean on latitude is done 
  >>> # Plot a Hovmöller diagram on all domain, at level index 3, and using %c for 'fmt' (i.e. small month abbreviation e.g., Jun): 
  >>> diag_xt=hovm(ta, title='Temperature', mean_axis='Lat', zpoint=3,fmt="%c") # => plot (x,t), or mean_axis="Lon" and zpoint=3 => plot (y,t)
  >>> cshow(diag_xt)
  >>> # Diagram on domain [-10,0,-90,-80] at longitude close to 360 and where X and Y are inverted:
  >>> diag_tz=hovm(ta, title='Temperature', mean_axis='Lat', xpoint=360., fmt="%c", latS=-10, latN= 0, lonW=-90, lonE=-80, 
  >>> ... invXY=True) # => plot (t,z) or mean_axis="Lon" and ypoint=3 => plot (t,z)

.. _climate_boxes_example:

  >>> # No mean: section at different points => you must set two points (xpoint, ypoint or zpoint) because rank=4
  >>> # Diagram on 'NINO1-2' box with 'CBR_wet' colorpalette and 'options' for tuning NCL graphic resources:
  >>> diag_section=hovm(ta, title='Temperature', mean_axis='Point', xpoint=2, zpoint=1500., 
  >>> color="CBR_wet", options="tiXAxisString=latitude|cnLinesOn=True",
  >>> **hovm_params('NINO1-2')) # => plot (y,t), or ypoint/zpoint => plot (x,t), or xpoint/ypoint => plot (z,t)

  >>> # 3D field: pr(time, lat, lon)
  >>> cdef("project","erai")
  >>> cdef("frequency","monthly")
  >>> cdef("period","1979-2008")
  >>> dataerai=ds( simulation="erai", variable="pr", grid="T127" )
  >>> # Mean on latitude axis: you must not set points because rank=3 and a mean on latitude is done
  >>> # If you use xpoint/ypoint/zpoint, selected points are not considered. 
  >>> ploterai=hovm(dataerai, mean_axis="Lat", color="CBR_wet", **hovm_params('NINO1-2'))

**Side effects** : None

**Implementation** : Basic use of ncl: gsn_csm_hov
