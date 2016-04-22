div : division of two fields using CliMAF ccdo2 and CDO operator div
---------------------------------------------------------------------------

Division of two fields

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any pair of objects with compatible grids, ranks and sizes 

**Mandatory argument**: 

None

**Output** : ds1 / ds2

**Climaf call example** ::
 
  >>> ds1= .... #some dataset, with whatever variable
  >>> ds2= .... #some other, compatible dataset
  >>> ds1_on_ds2 = div(ds1,ds2) # ds1 / ds2

**Side effects** : none

**Implementation** : shortcut to 'ccdo2(ds1,ds2,operator='div')'

