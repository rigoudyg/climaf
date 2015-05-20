plot : map, cross-section and profile plot 
-------------------------------------------------------------

Plot a series of xy curves (along lat, lon or pressure/z_index ) for
an ensemble dataset using NCL

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - an ensemble dataset which can be up to 4-dimensional, but with
    only one non-degenerated dimension. All members are (yet) assumed
    to have the same vector size

**Mandatory arguments**: 

  - ``var`` : name of the variable to plot (must be the same for all members)

**Optional arguments**:

  - ``title`` : string for graphic title
  - ``labels`` : a string with one label per member, separated by
    character '$'
  - ``colors`` : a string with one NCL color name per member,
    separated by whitespace
  - ``thickness`` : thickness of the curves line; default to 2.
  - ``linp`` : set it to 1 for getting a vertical axis with index-linear spacing 

**Outputs** :

  - main output : a PNG figure

**Climaf call example**::
 
  >>> j0=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
  >>> j1=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")
  >>> e2=cens(['1980','1981'],j0,j1)
  >>> tas_ga=space_average(e2)
  >>> p=lines(tas_ga,title="Surface Temperature global average")

**Shortcomings**:

  - time axis units is not changed to a smart one
  - must have the same coordinates for all vectors
