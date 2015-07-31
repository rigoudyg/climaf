lines : plot multiple profiles (along p, lat, lon..) 
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

  - ``realXaxis`` : an integer (0 or 1) which determines time axis
    when datasets does not cover the same time period; 

    - realXaxis=0 : time axis will be aligned to the same origin (take
      the first file as ref.) 
    - realXaxis=1 : time axis will be the union of all time periods 


**Optional arguments**:

  - ``title`` : string for graphic title
  - ``labels`` : a string with one label per member, separated by
    character '$'
  - ``colors`` : a string with one NCL color name per member,
    separated by whitespace
  - ``thickness`` : thickness of the curves line; default to 2.
  - ``linp`` : set it to 1 for getting a vertical axis with
    index-linear spacing 
  - ``fmt``: a string specifying the format of the tick labels. This
    string is parsed as follows: the '%' acts as the escape
    character. The single character after every '%' is formatted
    according to the rule: 

    - Y => 4-digit year (e.g., 2007).
    - y => 2-digit year (e.g., 07).
    - C => CAPITAL month abbreviation (e.g., JUN).
    - c => Small month abbreviation (e.g., Jun).
    - F => CAPITAL full month (e.g., JUNE).
    - f => Small full month (e.g., June).
    - N => 2-digit month (e.g., 06).
    - n => 1 or 2 digit month (e.g., 6 for June, 12 for December).
    - D => 2-digit day (e.g., 04).
    - d => 1 or 2 digit day (e.g., 4)
    - H => 2-digit hour (e.g., 09).
    - h => 1 or 2 digit hour (e.g., 9 or 11).
    - M => 2 digit minute (e.g., 08).
    - m => 1 or 2 digit minute (e.g., 07 or 56).
    - S => 2 digit second (e.g., 02).
    - s => 1 or 2 digit second (e.g., 2 or 23).

Any character at any other place in the format string is drawn as is.

NOTE: a '%' can be drawn using "%%". In case fmt is absent, a minimal
algorithm exists which tries to determine the format string depending
on the length and values of the date-time. For more details, see:
https://www.ncl.ucar.edu/Document/Functions/User_contributed/time_axis_labels.shtml

**Outputs** :

  - main output : a PNG figure

**Climaf call example**::
 
  >>> j0=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
  >>> j1=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")
  >>> ens=cens(['1980','1981'],j0,j1)
  >>> tas_ga=space_average(ens)
  >>> p=lines(tas_ga,title="Surface Temperature global average",realXaxis=1)
  >>> cshow(p)

  >>> d0=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1860")
  >>> d1=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1861")
  >>> d2=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1862")
  >>> d3=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1863")
  >>> d4=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1864")
  >>> d5=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1865")
  >>> d6=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1866")
  >>> d7=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1867")
  >>> d8=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1868")
  >>> d9=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1869")
  >>> ens2=cens(['1960','1961','1962','1963','1964','1965','1966','1967','1968','1969'],d0,d1,d2,d3,d4,d5,d6,d7,d8,d9)
  >>> moy=space_average(ens2)
  >>> p=lines(moy,title="surface temp global average",realXaxis=1)
  >>> cshow(p)







