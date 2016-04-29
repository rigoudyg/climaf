divide : division between two CliMAF objects 
------------------------------------------------------------------------

Division of two CliMAF object.

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any pair of objects with compatible grids, ranks and sizes.

**Mandatory argument**: 

None

**Output** : ds1 / ds2

**Climaf call example** ::
 
  >>> ds1= .... #some dataset, with whatever variable
  >>> ds2= .... #some other, compatible dataset
  >>> ds1_by_ds2 = divide(ds1,ds2) # ds1 / ds2

**Side effects** : none

**Implementation** : 'cdo div ${in_1} ${in_2} ${out}' 

