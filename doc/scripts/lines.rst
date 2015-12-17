lines : plot multiple profiles (along p, lat, lon..) 
-------------------------------------------------------------

Plot a series of xy curves (along lat, lon or pressure/z_index ) for
an ensemble dataset using NCL

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - an ensemble dataset which can be up to 4-dimensional, but with
    only one non-degenerated dimension. All members are (yet) assumed
    to have the same vector size. 

**Mandatory arguments**: 

  - None

**Optional arguments**:

  - ``title`` : string for graphic title
  - ``labels`` : a string with one label per member, separated by
    character '$'
  - ``colors`` : a string with one NCL color name per member,
    separated by whitespace
  - ``thickness`` : thickness of the curves line; default to 2.
  - ``X_axis`` : a string ("real" or "aligned") which determines X
    axis when datasets does not cover the same range; default to
    "real".   

   - X_axis="real"    : X axis will be the union of all X axis
   - X_axis="aligned" : X axis will be aligned to the same origin
     (take the first file as ref.)  
      
  - ``linp`` : set it to 1 for getting a vertical axis with
    index-linear spacing  
  - ``fmt``: a string specifying the format of the tick labels. This
    string is parsed as follows: the '%' acts as the escape
    character. The single character after every '%' is formatted
    according to the rule described here:

    https://www.ncl.ucar.edu/Document/Functions/User_contributed/time_axis_labels.shtml

    In case fmt is absent, a minimal algorithm exists which tries to
    determine the format string depending on the length and values of
    the date-time. 

**Outputs** :

  - main output : a PNG figure

**Climaf call example**::
 
  >>> j0=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
  >>> j1=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")
  >>> ens=cens(['1980','1981'],j0,j1)
  >>> tas_ga=space_average(ens)
  >>> p=lines(tas_ga,title="Surface Temperature global average",X_axis="aligned")
  >>> cshow(p)

  >>> d0=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1860")
  >>> d1=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1861")
  >>> d2=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1862")
  >>> d3=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1863")
  >>> d4=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1864")
  >>> ens2=cens(['1960','1961','1962','1963','1964'],d0,d1,d2,d3,d4)
  >>> moy=space_average(ens2)
  >>> p=lines(moy,title="Surface Temperature global average") # Time axis is "real"
  >>> cshow(p)







