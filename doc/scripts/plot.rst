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

  - a dataset for an auxiliary field which can be up to 4-dimensional
  - 2 datasets for a vector field which can be up to 4-dimensional

Warnings: 

- Order of all data dimensions is supposed to be time, height, lat,
  lon. Only first time step is used. Only the first vertical dimension
  is used if the two other dimensions are not degenerated.   

- Order of input datasets is supposed to be main field, auxiliary field and
  vectors datasets. The last ones can be omitted. If you want to omit
  the scalar field but not the verctor components, use value None for
  the scalar dataset

**Mandatory arguments**: None (but ``title`` is recommended)

**Optional arguments**:

General:

  - ``title`` : string for graphic title; optional : CliMAF will provide the CRS of
    the dataset
  - ``format`` : graphic output format, either 'png' or 'pdf';
    default: 'png'. For 'png' format, all the surrounding white extra
    space are cropped, while not for 'pdf' format. In case of 'pdf'
    format, if you want to trim white extra space, use 'cpdfcrop'
    operator which is 'pdfcrop' tool and which preserves in more
    metadata.  
  - ``resolution`` : string for image resolution, containing width and
    height of resultant image or paper separated by character 'x', as
    e.g. : "900x900" (in pixels for PNG output), "8.5x14" (in inches
    for PDF output)

    - if format is "png", resolution specifies the width and height of
      resultant image in pixels; default (ncl): 1024x1024
    - if format is "pdf", resolution specifies the width and height of
      the paper, in inches; default (ncl): 8.5x11 (<=> 612x792 in pixels)
  - ``linp`` : 

    - 1 for getting a vertical axis with index-linear spacing, or
    - -1 for getting a vertical axis with data-linear spacing, or
    - default: vertical axis will have a logarithmic scale
  - ``proj`` : use it to request a stereopolar projection, as e.g. :
    "NH","SH60"...
  - ``focus`` : set it to 'land' (resp. 'ocean') if you want to plot
    only on land (resp. ocean) 
  - ``time``, ``level`` : for selecting time or level. This arguments
    apply on all fields which have time and/or level dimension. Set it
    to: 

    - an integer if you want to select an index, 
    - or a float if you want to select closest coordinate value,
    - default: select the first time step if we have non-degenerated 
      dimensions (t,z,y,x) ; select first time or level step if
      field rank is 3.     

Main field:

  - colormap and its interpretation :

   - ``cmap`` : name of the Ncl colormap to use; see e.g. 
     https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml#Aid_in_color_blindness ;
     default (climaf) is 'BlueDarkRed18'
   - ``vmin``, ``vmax`` , ``vdelta`` : min and max values and levels
     when applying the colormap, or 
   - ``colors`` : list of levels used when applying colormap
     e.g. colors="260 270 280 290"
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

    - *If plotting only a main field:*

      - set it to 1 if you want to draw contours which follow color
	filled contours, or
      - set it to a list of levels used when drawing contours
	e.g. contours="230 240 250" 

    - *If plotting a main field and an auxiliary field:* only the contours of 
      the auxiliary field are drawn

      - set it to a list of levels used when drawing contours of
	auxiliary field e.g. contours="230 240 250", or
      - default (ncl): draw contours of auxiliary field in "AutomaticLevels"
	ncl mode; see e.g.
	http://www.ncl.ucar.edu/Document/Graphics/Resources/cn.shtml#cnLevelSelectionMode

Vectors:

  - ``rotation`` : set it to 1 if you want to rotate vectors from model
    grid to geographic grid (see note below about an angles file)
  
  - ``vcRefLengthF`` : length used, in units of Ncl's NDC , to render vectors
    with a magnitude equal to the reference magnitude, as specified by
    vcRefMagnitudeF; default (ncl): <dynamic>; see e.g. 
    http://www.ncl.ucar.edu/Document/Graphics/Resources/vc.shtml#vcRefLengthF

  - ``vcRefMagnitudeF`` : magnitude used as the reference magnitude
    used for the vector field plot; default (ncl): 0.0 (i.e. the maximum
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
 
  - Maps ::

     >>> duo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")
     >>> dvo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O") 
     >>> tos=ds(project="EM",simulation="PRE6CPLCr2alb", variable="tos", period="199807", realm="O")
     >>> # Extraction of 'tos' sub box for auxiliary field
     >>> sub_tos=llbox(tos, latmin=30, latmax=80, lonmin=-60, lonmax=0) 
     >>> # How to get required file for rotate vectors from model grid on geographic grid
     >>> fixed_fields('plot', ('angles.nc',cpath+"/../tools/angle_${project}.nc"))
    
     >>> # A Map of one field and vectors, contours lines follows color fill, rotation of vectors on geographic grid and with 'pdf' output format 
     >>> plot_map1=plot(tos, None, duo, dvo, title='1 field (contours lines follow color filled contours) + vectors', 
     ... contours=1, rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, format="pdf") 
     >>> cshow(plot_map1)
     >>> # 'cpdfcrop' operator applied on 'plot_map1' object ('cpdfcrop' <=> 'pdfcrop' by preserving metadata)
     >>> cshow(cpdfcrop(plot_map1))

     >>> # A Map of one field and vectors, user-controlled contours lines, rotation as above, and  with 'png' output format (default)
     >>> plot_map2=plot(tos, None, duo, dvo, title='1 field (user control contours) + vectors', contours='1 3 5 7 9 11 13', 
     ... proj='NH', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)

     >>> # A Map of two fields and vectors, with explicit contours levels for auxiliary field and rotation of vectors 
     >>> plot_map3=plot(tos, sub_tos, duo, dvo, title='2 fields (user control auxiliary field contours) + vectors', contours='0 2 4 6 8 10 12 14 16',
     ... rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02) 

     >>> # A Map of two fields and vectors, with automatic contours levels for auxiliary field and rotation of vectors 
     >>> plot_map4=plot(tos, sub_tos, duo, dvo, title='2 fields (automatic contours levels for auxiliary field) + vectors', 
     ... proj="NH", rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, vcMinDistanceF=0.01, vcLineArrowColor="yellow") 

     >>> # A Map of two fields and vectors, with index selection of time step and/or level step for all fields which have this dimension :
     >>> # time selection has no impact for vectors because time dimension is degenerated, so only level selection is done for vectors
     >>> thetao=ds(project="EM",simulation="PRE6CPLCr2alb", variable="thetao", period="1998", realm="O") # thetao(time_counter, deptht, y, x) 
     >>> sub_thetao=llbox(thetao, latmin=30, latmax=80, lonmin=-60, lonmax=0) 
     >>> plot_map5=plot(thetao, sub_thetao, duo, dvo, title='Selecting index 10 for level and 0 for time', rotation=1, vcRefLengthF=0.002, 
     ... vcRefMagnitudeF=0.02, level=10, time=0) 

  - A cross-section ::

     >>> january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
     >>> ta_zonal_mean=ccdo(january_ta,operator="zonmean")
     >>> # Extraction of 'january_ta' sub box for auxiliary field
     >>> cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) 
     >>> ta_zonal_mean2=ccdo(cross_field2, operator="zonmean")

     >>> # A vertical cross-section in pressure coordinates of one field without contours lines and with logarithmic scale (default)
     >>> plot_cross1=plot(ta_zonal_mean,title='1 field cross-section without contours lines')
     >>> cshow(plot_cross1)

     >>> # A cross-section of one field, which contours lines following color fill
     >>> plot_cross2=plot(ta_zonal_mean, contours=1, title='1 field (contours lines follow color filled contours)')

     >>> # A cross-section of one field, with used-controlled contours lines 
     >>> plot_cross3=plot(ta_zonal_mean, contours="240 245 250", title='1 field (user control contours)')

     >>> # A cross-section of two fields, with explicit contours levels for auxiliary field
     >>> plot_cross4=plot(ta_zonal_mean, ta_zonal_mean2, contours="240 245 250", title='2 fields (user control auxiliary field contours)') 

     >>> # A cross-section of two fields, with automatic contours levels for auxiliary field and a pressure-linear spacing for vertical axis 
     >>> plot_cross5=plot(ta_zonal_mean, ta_zonal_mean2, linp=-1, title='2 fields (automatic contours levels for auxiliary field)')
    
     >>> # A cross-section with value selection of time step for all fields which have this dimension
     >>> # time selection is done for main and auxiliary field 
     >>> january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1980") # ta(time, plev, lat, lon) 
     >>> ta_zonal_mean=ccdo(january_ta,operator="zonmean") 
     >>> cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) 
     >>> ta_zonal_mean2=ccdo(cross_field2, operator="zonmean") 
     >>> plot_cross6=plot(ta_zonal_mean, ta_zonal_mean2, title='Selecting time closed to 3000', linp=1, time=3000.) 

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



