plot : map, cross-section and profile plot 
-------------------------------------------------------------

Plot a map, a cross section (pressure-lat or pressure-lon), or a
profile (along lat, lon or pressure/z_index ) using NCL, and allowing for 
tuning a number of graphic attributes

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - a dataset which can be up to 4-dimensional. Order of dimensions is
    supposed to be time, height, lat, lon. Only first time step is
    used. Only the first vertical dimension is used if the two other
    dimensions are not degenerated .

**Mandatory arguments**: None (but ``crs`` is recommended)

**Optional arguments**:
  - ``crs`` : string for graphic title; optional : CliMAF will provide the CRS of
    the dataset
  - colormap and its interpretation :

   - ``color`` : name of the Ncl colormap to use; default
     is 'BlueDarkRed18'  ; see
     e.g. https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml#Aid_in_color_blindness. 
   - ``min``, ``max`` , ``vdelta`` : min and max values and levels when applying the colormap 
   - ``levels`` : list of levels used when applyng colomap e.g. lin="260,270,280,290"

  - ``scale``, ``offset`` : for scaling the input field ( x -> x*scale +
    offset); default = 1. and 0. (no scaling)
  - ``units`` : name of the field units; used in the caption; default
    is to use the corresponding CF metadata
  - ``linp`` : set it to 1 for getting a vertical axis with index-linear spacing 
  - ``proj`` : use it to request a stereopolar projection, as e.g. : "NH","SH60"...

**Outputs** :
  - main output : a PNG figure

**Climaf call example** 
 
  - A map ::

   >>> surface_ta=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="198001")
   >>> plot_map=plot(surface_ta,crs='A Map')
   >>> cshow(plot_map)

  - A cross-section ::

   >>> january_ta=ds(project='example',experiment="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
   >>> ta_zonal_mean=ccdo(january_ta,operator="zonmean")
   >>> plot_cross=plot(ta_zonal_mean,crs='A cross-section')
   >>> cshow(plot_cross)

  - A profile ::

   >>> ta_profile=ccdo(ta_zonal_mean,operator="mermean")
   >>> plot_profile=plot(ta_profile,crs='A profile',linp=1)
   >>> cshow(plot_profile)

**Side effects** : None

**Implementation** : Basic use of ncl_gsm_pres_hgt, gsn_csm_xy, gsn_csm_contour_map_ce

