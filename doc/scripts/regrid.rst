regrid : regrid an object to the grid of another one
---------------------------------------------------------

Interpolate the object to the grid of another object, using CDO

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-5200002.12.1

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any object or dataset to interpolate 
  - the object or dataset on which grid to interpolate

**Mandatory arguments**: none

**Optional arguments**:
  - ``option`` : interpolation option (cf. CDO doc); default : 
    'remapbil' for bilinear interpolation

**Output** : the interpolated object

**Climaf call example**::
 
  >>> ds= .... # some dataset, with whatever variable
  >>> grid_ds= ....# some other dataset, used here for its grid
  >>> remapbil_ds=regrid(ds,grid_ds) # Interpolation is bilinear
  >>> remapcon2_ds=regrid(ds,grid_ds, option="remapcon2")  # Interpolation is 2nd order conservative

**Side effects** : a temporary file is created in current directory,
then erased (name : climaf_tmp_grid)

**Implementation** : standard CDO calls (griddes and remapgrid)

