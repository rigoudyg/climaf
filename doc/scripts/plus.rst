plus : Addition of two fields using CDO operator add
----------------------------------------------------------

Addition of two fields

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any pair of objects with compatible grids, ranks and sizes 

**Mandatory argument**: 

None

**Output** : the addition

**Climaf call example** ::
 
  >>> ds1= .... #some dataset, with whatever variable
  >>> ds2= .... #some other, compatible dataset
  >>> ds1_plus_ds2 = plus(ds1,ds2) # ds1 + ds2

**Side effects** : none

**Implementation** : using 'cdo add'

