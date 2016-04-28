minus : difference of two fields using CDO operator sub
----------------------------------------------------------

Difference of two fields

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any pair of objects with compatible grids, ranks and sizes 

**Mandatory argument**: 

None

**Output** : the difference

**Climaf call example** ::
 
  >>> ds1= .... #some dataset, with whatever variable
  >>> ds2= .... #some other, compatible dataset
  >>> diff=minus(ds1,ds2) # ds1 - ds2

**Side effects** : none

**Implementation** : using 'cdo sub'
