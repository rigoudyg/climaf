plotmap : geographical map for a one-time-step dataset
-----------------------------------------------------------

Plot a geographical map, using NCL, and allowing for tuning a number of graphic attributes

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**:
  - ``color`` : name of the Ncl colormap to use; see e.g. https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml#Aid_in_color_blindness
  - ``vmin``, ``vmax`` , ``vdelta`` : min and max values and levels
    when applying the colormap 

**Optional arguments**:
  - ``crs`` : string for graphic title; optional : CliMAF will provide the CRS of
    the dataset
  - ``scale``, ``offset`` : for scaling the input field ( x -> x*scale +
    offset); default = 1. and 0. (no scaling)
  - ``units`` : name of the field units; used in the caption; default
    is to use the corresponding CF metadata

**Outputs** :
  - main output : a PNG figure

**Climaf call example** ::
 
  >> tas= ....some dataset like e.g. of monthly mean of a low level temperature
  >> map=plotmap(ta,color="BlueDarkRed18", vmin=260, vmax=300, delta=4")

**Side effects** : create temporary files in the directory provided for output fields

**Implementation** : just two calls to ``cdo`` and the use of ``ncwa`` for discarding
degenerated space dimensions (because CDO does not discard them)

**CliMAF call sequence pattern** (for reference) ::

  "ncl plotmap.ncl infile=${in} plotname=${out} cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} var=${var} title=${crs} scale=${scale} offset=${offset} units=${units}",format="png"

