plotmap : geographical map for a one-time-step dataset
-----------------------------------------------------------

Plot a geographical map, using NCL, and allowing for tuning a number of graphic attributes

**References** : http://www.ncl.ucar.edu

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**:
  - ``color`` : name of the Ncl colormap to use
  - ``vmin``, ``vmax`` , ``vdelta`` : min and max values and levels
    when applying the colormap 
  - ``scale, offset`` : for scaling the input field ( x -> x*scale +
    offset); yet mandatory but this will be improved soon
  - ``units`` : name of the field units; used in the caption; yet
    mandatory, but this will be improved to use CF metadata

**Optional arguments**:
  - ``crs`` : string for graphic title; optional : CliMAF will provide the CRS of
    the dataset

**Outputs** :
  - main output : a PNG figure

**Climaf call example** ::
 
  >> tas= ....some dataset like e.g. of monthly mean of a low level temperature
  >> map=plotmap(ta,color="BlueDarkRed18", min=260, max=300, delta=4, scale=1, offset=0, units="K")

**Side effects** : create temporary files in the directory provided for output fields

**Implementation** : just two calls to ``cdo`` and the use of ``ncwa`` for discarding
degenerated space dimensions (because CDO does not discard them)

**CliMAF call sequence pattern** (for reference) ::

  "ncl plotmap.ncl infile=${in} plotname=${out} cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} var=${var} title=${crs} scale=${scale} offset=${offset} units=${units}",format="png"

