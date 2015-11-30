curves : plot multiple profiles (along p, lat, lon..) 
-------------------------------------------------------------

**WARNING : this operator will not be supported in future
versions. It will be replaced by an improved version of operator lines,
when thisis one will be able to handle more cases than time series**

Plot a series of xy curves (along lat, lon or pressure/z_index ) for
an ensemble dataset using NCL

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - an ensemble dataset which can be up to 4-dimensional, but with
    only one non-degenerated dimension. All members are (yet) assumed
    to have the same vector size. OK when dimension is
    not time

**Mandatory arguments**: 

  - None

**Optional arguments**:

  - ``title`` : string for graphic title
  - ``labels`` : a string with one label per member, separated by
    character '$'
  - ``colors`` : a string with one NCL color name per member,
    separated by whitespace
  - ``linp`` : set it to 1 for getting a vertical axis with
    index-linear spacing  

**Outputs** :

  - main output : a PNG figure

**Climaf call example**::
 
  >>> j0=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
  >>> j1=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")
  >>> ens=cens(['1980','1981'],j0,j1)
  >>> tas_ga=space_average(ens)
  >>> p=lines(tas_ga,title="Surface Temperature global average",T_axis="tweaked")
  >>> cshow(p)

  >>> d0=ds(project='CMIP5', model="CNRM-CM5", simulation="1pctCO2", variable="tas", period="1860")
  >>> d1=ds(project='CMIP5', model="CNRM-CM5", simulation="1pctCO2", variable="tas", period="1861")
  >>> d2=ds(project='CMIP5', model="CNRM-CM5", simulation="1pctCO2", variable="tas", period="1862")
  >>> d3=ds(project='CMIP5', model="CNRM-CM5", simulation="1pctCO2", variable="tas", period="1863")
  >>> d4=ds(project='CMIP5', model="CNRM-CM5", simulation="1pctCO2", variable="tas", period="1864")
  >>> ens2=cens(['1960','1961','1962','1963','1964'],d0,d1,d2,d3,d4)
  >>> moy=space_average(ens2)
  >>> p=lines(moy,title="Surface Temperature global average") # Time axis is "real"
  >>> cshow(p)







