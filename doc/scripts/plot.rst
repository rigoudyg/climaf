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
          
Warning: Order of data dimensions is supposed to be time, height, lat,
lon. Only first time step is used. Only the first vertical dimension
is used if the two other dimensions are not degenerated.  

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

Additional fields:

  - ``aux`` : a dataset for auxiliary field which can be up to
    4-dimensional
  - ``u, v`` : 2 datasets for the vector plot which can be up to
    4-dimensional

Warning: Order of data dimensions is supposed to be time, height, lat,
lon. Only first time step is used. Only the first vertical dimension
is used if the two other dimensions are not degenerated.  

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
creates this file: see :download:`angle_ORCA1.nc
<../../tools/angle_ORCA1.nc>` and :download:`angle.ncl
<../../tools/angle.ncl>`  

**Outputs** :
  - main output : a PNG figure

**Climaf call example** For more examples, see :download:`gplot.py <../../examples/gplot.py>`    
 
  - A map ::

     >>> duo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")
     >>> dvo=ds(project="EM",simulation="PRE6CPLCr2alb", variable="vo", period="199807", realm="O") 
     >>> tos=ds(project="EM",simulation="PRE6CPLCr2alb", variable="tos", period="199807", realm="O")
     >>> sub_tos=llbox(tos, latmin=30, latmax=80, lonmin=-60, lonmax=0) # extraction of 'tos' sub box for auxiliary field
     >>> # How to get required file for rotate vectors from model grid on geographic grid
     >>> fixed_fields('plot', ('angles.nc','/data/climaf/${project}/${model}/angle_ORCA1.nc'))
    
     >>> plot_map=plot(tos, u=duo, v=dvo, title='A Map which contours lines follow color filled contours', contours=1, 
     ... rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02) # rotation of vectors on geographic grid
     >>> cshow(plot_map)

     >>> plot_map2=plot(tos, u=duo, v=dvo, title='A Map which contours lines don t follow color filled contours', contours='1 3 5 7 9 11 13', 
     ... proj='NH', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02) # rotation of vectors on geographic grid
     >>> cshow(plot_map2)

     >>> plot_map3=plot(tos, aux=sub_tos, u=duo, v=dvo, title='SST: 2 fields + vectors', contours='0 2 4 6 8 10 12 14 16',
     ... rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02) # contours lines of auxiliary field are explicit levels,
     ... # rotation of vectors on geographic grid
     >>> cshow(plot_map3)

     >>> plot_map4=plot_2fields(tos, aux=sub_tos, u=duo, v=dvo, title='SST: 2 fields + vectors, proj=NH', rotation=1, vcRefLengthF=0.002,
     ... vcRefMagnitudeF=0.02, vcMinDistanceF=0.01, vcLineArrowColor="yellow", proj="NH") # contours lines of auxiliary field are automatic levels,
     ... # rotation of vectors on geographic grid
     >>> cshow(plot_map4)

  - A cross-section ::

     >>> january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
     >>> ta_zonal_mean=ccdo(january_ta,operator="zonmean")
     >>> cross_field2=llbox(january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150) # extraction of 'january_ta' sub box for auxiliary field
     >>> ta_zonal_mean2=ccdo(cross_field2, operator="zonmean")

     >>> plot_cross=plot(ta_zonal_mean,title='A cross-section without contours lines') # by default, vertical cross-sections 
     ... # in pressure coordinates will have a logarithmic scale
     >>> cshow(plot_cross)

     >>> plot_cross2=plot(ta_zonal_mean, contours=1, title='A cross-section which contours lines follow color filled contours')
     >>> cshow(plot_cross2)

     >>> plot_cross3=plot(ta_zonal_mean, contours="240 245 250", title='A cross-section which contours lines don t follow color filled contours')
     >>> cshow(plot_cross3)

     >>> plot_cross4=plot(ta_zonal_mean, aux=ta_zonal_mean2, contours="240 245 250", 
     ... title='A cross-section which contours lines of auxiliary field are explicit levels') # 2 fields, logarithmic scale
     >>> cshow(plot_cross4)

     >>> plot_cross5=plot(ta_zonal_mean, aux=ta_zonal_mean2, linp=-1, title='A cross-section which contours lines of auxiliary field are automatic levels')
     ... # vertical axis will have a pressure-linear spacing
     >>> cshow(plot_cross5)

  - A profile ::

     >>> ta_profile=ccdo(ta_zonal_mean,operator="mermean")
     >>> ta_profile2=ccdo(ta_zonal_mean2,operator="mermean")

     >>> plot_profile1=plot(ta_profile, title='A profile') # by default, vertical profiles 
     ... #in pressure coordinates will have a logarithmic scale
     >>> cshow(plot_profile1)

     >>> plot_profile2=plot(ta_profile, aux=ta_profile2, title='Two profiles', linp=1) # 2 fields, 
     ... # vertical axis will have a index-linear spacing
     >>> cshow(plot_profile2)

**Side effects** : None

**Implementation** : Basic use of ncl: gsn_csm_pres_hgt, gsn_csm_xy,
gsn_csm_contour_map, gsn_csm_contour_map_ce, gsn_csm_contour,
gsn_csm_vector_scalar_map, gsn_csm_vector_scalar_map_ce



