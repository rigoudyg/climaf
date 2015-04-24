plotxsec : Cross section plot for a one-time-step dataset
-----------------------------------------------------------

Plot a cross section (pressure-lat or pressure-lon), using NCL, and allowing for tuning a number of graphic attributes

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - a dataset 
     - with no or singleton dimension either for latitude or for longitude
     - with or without time dimension (first time step will be plotted)

**Mandatory arguments**: None

**Optional arguments**:
  - ``min``, ``max`` , ``vdelta`` : min and max values and levels when applying the colormap 
  - ``color`` : name of the Ncl colormap to use; default
    is 'BlueDarkRed18'  ; see
    e.g. https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml#Aid_in_color_blindness. 
  - ``crs`` : string for graphic title; optional : CliMAF will provide the CRS of
    the dataset
  - ``scale``, ``offset`` : for scaling the input field ( x -> x*scale +
    offset); default = 1. and 0. (no scaling)
  - ``units`` : name of the field units; used in the caption; default
    is to use the corresponding CF metadata

**Outputs** :
  - main output : a PNG figure

**Climaf call example** ::
 
  >>> january_ta=ds(project='example',experiment="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
  >>> ta_zonal_mean=ccdo(january_ta,operator="zonmean")
  >>> plot=plotxsec(ta_zonal_mean)
  >>> cshow(plot)

**Side effects** : None

**Implementation** : Basic use of ncl_gsm_pres_hgt

