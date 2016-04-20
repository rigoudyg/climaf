regridll : regrid an object to a lat-lon box of a CDO regular grid 
-------------------------------------------------------------------

Interpolate the object to another grid, using CDO

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-5200002.12.1

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**:
  - ``cdogrid`` : target grid name, according to CDO standard ; e.g. r360x180
    (see https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-150001.3.2)
  - ``latmin,latmax,lonmin,lonmax`` : for defining the latitude longitude box

**Optional arguments**:
  - ``option`` : interpolation option (cf. CDO doc); default : 
    'remapbil' for bilinear interpolation

**Output** : the interpolated object

**Climaf call example** ::
 
  >>> ds= .... #some dataset, with whatever variable
  >>> llbox_ds=regridll(ds,cdogrid="r180x90",latmin=-10.,latmax=10,lonmin=-180,lonmax=180)  

**Side effects** : None

**Implementation** : standard CDO calls (remapgrid)

