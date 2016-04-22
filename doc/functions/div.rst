div : division of two fields using CliMAF ccdo2 and CDO operator div
---------------------------------------------------------------------------

Division of two CliMAF object, or division of the CliMAF object given as first argument and a constant as second argument (string, float or integer)

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any pair of objects with compatible grids, ranks and sizes ; if you want to divide by a constant, provide a string, float or integer as second argument.

**Mandatory argument**: 

None

**Output** : ds1 / ds2

**Climaf call example** ::
 
  >>> ds1= .... #some dataset, with whatever variable
  >>> ds2= .... #some other, compatible dataset
  >>> ds1_div_by_ds2 = div(ds1,ds2) # ds1 / ds2

  >>> ds1= .... #some dataset, with whatever variable
  >>> c = '-1'  #a constant
  >>> ds1_div_by_c = div(ds1,c) # ds1 / c


**Side effects** : none

**Implementation** : shortcut to 'ccdo2(ds1,ds2,operator='div')' and ccdo(dat,operator='divc,'+c)

