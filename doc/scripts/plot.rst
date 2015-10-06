plot : map, cross-section and profile plot of one or two fields, and vectors plot over a map
---------------------------------------------------------------------------------------------

Plot a map, a cross section (pressure-lat or pressure-lon), or a
profile (along lat, lon or pressure/z_index ) of one or two fields and
draw vectors plot over a map, using NCL, and allowing for tuning a
number of graphic attributes  

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - a dataset for main field which can be up to 4-dimensional

Additional fields (optional):

  - a dataset for auxiliary field which can be up to 4-dimensional
  - 2 datasets for the vector plot which can be up to 4-dimensional

Warnings: 

- Order of all data dimensions is supposed to be time, height, lat,
  lon. Only first time step is used. Only the first vertical dimension
  is used if the two other dimensions are not degenerated.   

- Order of inputs is supposed to be main field, auxiliary field and
  vectors datasets. For additional fields, if one or several optional
  datasets are not used, set None instead of dataset; unless it is
  about one or several last fields.   

**Mandatory arguments**: None (but ``title`` is recommended)

**Optional arguments**:

General:

  - ``title`` : string for graphic title; optional : CliMAF will provide the CRS of
    the dataset
  - ``linp`` : 

    - set it to 1 for getting a vertical axis with index-linear
      spacing, or
    - set it to -1 for getting a vertical axis with data-linear
      spacing, or
    - default: vertical axis will have a logarithmic scale
  - ``proj`` : use it to request a stereopolar projection, as e.g. :
    "NH","SH60"...
  - ``focus`` : set it to 'land' (resp. 'ocean') if you want to plot
    only on land (resp. ocean) 

Main field:

  - colormap and its interpretation :

   - ``cmap`` : name of the Ncl colormap to use; see e.g. 
     https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml#Aid_in_color_blindness ;
     default (climaf) is 'BlueDarkRed18'
   - ``vmin``, ``vmax`` , ``vdelta`` : min and max values and levels
     when applying the colormap, or 
   - ``levels`` : list of levels used when applying colormap
     e.g. lin="260 270 280 290"
  - ``scale``, ``offset`` : for scaling the input main field ( x -> x*scale +
    offset); default = 1. and 0. (no scaling)
  - ``units`` : name of the main field units; used in the caption;
    default is to use the corresponding CF metadata
  - ``mpCenterLonF`` : define the longitude of the center of the map
    projection coordinate system; see e.g. 
    https://www.ncl.ucar.edu/Document/Graphics/Resources/mp.shtml#mpCenterLonF ;
    default (climaf): (minimum longitude+maximum longitude)/2. 

Main field and/or auxiliary field:

  - ``contours`` : 

    - *If only main field:*

      - set it to 1 if you want to draw contours which follow color
	filled contours, or
      - set it to a list of levels used when drawing contours
	e.g. contours="230 240 250" 

    - *If main field and auxiliary field:* only contours of auxiliary
      field are drawing

      - set it to a list of levels used when drawing contours of
	auxiliary field e.g. contours="230 240 250", or
      - default (ncl): draw contours of auxiliary field in "AutomaticLevels"
	ncl mode; see e.g.
	http://www.ncl.ucar.edu/Document/Graphics/Resources/cn.shtml#cnLevelSelectionMode

Vectors:

  - ``rotation`` : set it to 1 if you want to rotate vectors from model
    grid to geographic grid (you need to have the angle file
    'angles.nc' in the current directory)  
  
  - ``vcRefLengthF`` : length used, in units of NDC, to render vectors
    with a magnitude equal to the reference magnitude, as specified by
    vcRefMagnitudeF; default (ncl): <dynamic>; see e.g. 
    http://www.ncl.ucar.edu/Document/Graphics/Resources/vc.shtml#vcRefLengthF

  - ``vcRefMagnitudeF`` : magnitude used as the reference magnitude
    used for the vector field plot; default (ncl): 0.0 (the maximum
    magnitude in the vector field will be used as the reference
    magnitude); see e.g. 
    http://www.ncl.ucar.edu/Document/Graphics/Resources/vc.shtml#vcRefMagnitudeF

  - ``vcMinDistanceF`` : minimum distance in NDC space that is to
    separate the data locations of neighboring vectors; see e.g. 
    http://www.ncl.ucar.edu/Document/Graphics/Resources/vc.shtml#vcMinDistanceF ;
    default (climaf): 0.017  

  - ``vcGlyphStyle`` : style of glyph used to represent the vector
    magnitude and direction; default (ncl): "LineArrow"; see e.g.
    http://www.ncl.ucar.edu/Document/Graphics/Resources/vc.shtml#vcGlyphStyle

  - ``vcLineArrowColor`` : uniform color for all lines used to draw
    vector arrows; see e.g.
    http://www.ncl.ucar.edu/Document/Graphics/Resources/vc.shtml#vcLineArrowColor ; 
    default (climaf): "white"

**Required file** If rotation is set to 1, file 'angles.nc' must be
made available to the script: use function fixed_fields() for that
(see example below). For an example of this file and the script which
creates this file: see :download:`angle_EM.nc
<../../tools/angle_EM.nc>` and :download:`angle.ncl
<../../tools/angle.ncl>`  

**Outputs** :
  - main output : a PNG figure

**Climaf call example** For more examples which are systematically
tested, see :download:`gplot.py <../../examples/gplot.py>` and
:download:`test_gplot.py <../../testing/test_gplot.py>`    
 
  - A map ::

     >>> duo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")
     >>> dvo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O") 
     >>> tos=ds(project="EM",simulation="PRE6CPLCr2alb", variable="tos", period="199807", realm="O")
     >>> # Extraction of 'tos' sub box for auxiliary field
     >>> sub_tos=llbox(tos, latmin=30, latmax=80, lonmin=-60, lonmax=0) 
     >>> # How to get required file for rotate vectors from model grid on geographic grid
     >>> fixed_fields('plot', ('angles.nc',cpath+"/../tools/angle_${project}.nc"))
    
     >>> # A Map of one field and vectors, with contours lines follow color filled contours and rotation of vectors on geographic grid
     >>> plot_map1=plot(tos, None, duo, dvo, title='1 field (contours lines follow color filled contours) + vectors', 
     ... contours=1, rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02) 
     >>> cshow(plot_map1)

     >>> # A Map of one field and vectors, with contours lines don t follow color filled contours and rotation of vectors on geographic grid
     >>> plot_map2=plot(tos, None, duo, dvo, title='1 field (user control contours) + vectors', contours='1 3 5 7 9 11 13', 
     ... proj='NH', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)

     >>> # A Map of two fields and vectors, with explicit contours levels for auxiliary field and rotation of vectors on geographic grid
     >>> plot_map3=plot(tos, sub_tos, duo, dvo, title='2 fields (user control auxiliary field contours) + vectors', contours='0 2 4 6 8 10 12 14 16',
     ... rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02) 

     >>> # A Map of two fields and vectors, with automatic contours levels for auxiliary field and rotation of vectors on geographic grid
     >>> plot_map4=plot(tos, sub_tos, duo, dvo, title='2 fields (automatic contours levels for auxiliary field) + vectors', 
     ... proj="NH", rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, vcMinDistanceF=0.01, vcLineArrowColor="yellow") 

  - A cross-section ::

     >>> january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
     >>> ta_zonal_mean=ccdo(january_ta,operator="zonmean")
     >>> # Extraction of 'january_ta' sub box for auxiliary field
     >>> cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) 
     >>> ta_zonal_mean2=ccdo(cross_field2, operator="zonmean")

     >>> # A vertical cross-section in pressure coordinates of one field without contours lines and with logarithmic scale (default)
     >>> plot_cross1=plot(ta_zonal_mean,title='1 field cross-section without contours lines')
     >>> cshow(plot_cross1)

     >>> # A cross-section of one field, which contours lines follow color filled contours
     >>> plot_cross2=plot(ta_zonal_mean, contours=1, title='1 field (contours lines follow color filled contours)')

     >>> # A cross-section of one field, which contours lines don t follow color filled contours
     >>> plot_cross3=plot(ta_zonal_mean, contours="240 245 250", title='1 field (user control contours)')

     >>> # A cross-section of two fields, with explicit contours levels for auxiliary field
     >>> plot_cross4=plot(ta_zonal_mean, ta_zonal_mean2, contours="240 245 250", title='2 fields (user control auxiliary field contours)') 

     >>> # A cross-section of two fields, with automatic contours levels for auxiliary field and a pressure-linear spacing for vertical axis 
     >>> plot_cross5=plot(ta_zonal_mean, ta_zonal_mean2, linp=-1, title='2 fields (automatic contours levels for auxiliary field)')
     
  - A profile ::

     >>> ta_profile=ccdo(ta_zonal_mean,operator="mermean")
     >>> ta_profile2=ccdo(ta_zonal_mean2,operator="mermean")

     >>> # One profile, with a logarithmic scale (default)
     >>> plot_profile1=plot(ta_profile, title='A profile')
     >>> cshow(plot_profile1)
 
     >>> # Two profiles, with a index-linear spacing for vertical axis
     >>> plot_profile2=plot(ta_profile, ta_profile2, title='Two profiles', linp=1)

**Side effects** : None

**Implementation** : Basic use of ncl: gsn_csm_pres_hgt, gsn_csm_xy,
gsn_csm_contour_map, gsn_csm_contour_map_ce, gsn_csm_contour,
gsn_csm_vector_scalar_map, gsn_csm_vector_scalar_map_ce



