regridn : regrid an object to a named grid
---------------------------------------------------

Interpolate the object to another grid, using CDO

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-5200002.12.1

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**:
  - ``cdogrid`` : target grid name, according to CDO standard 
    (see https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-150001.3.2)

**Optional arguments**:
  - ``option`` : interpolation option (cf. CDO doc); default : 
    'remapcon2' for 2nd order conservative

**Output** : the interpolated object

**Climaf call example** ::
 
  >>> ds= ....some dataset, with whatever variable
  >>> remapcon2_ds=regridn(ds,cdogrid="r180x90")  # Target Grid is 2°x2° - interpolation is 2nd order conservative
  >>> remapbil_ds=regridn(ds,cdogrid="n127", option="remapbil") # Target Grid is Gaussian - interpolation is bilinear

**Side effects** : None

**Implementation** : standard CDO calls (remapgrid)

