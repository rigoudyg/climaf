sub: substraction between two CliMAF objects or between a CliMAF object and a constant 
-------------------------------------------------------------------------------------------

Substraction of two CliMAF object, or subtraction of the CliMAF object given as first argument and a constant as second argument (string, float or integer)

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any pair of objects with compatible grids, ranks and sizes ; if you want to subtract a constant, provide a string, float or integer as second argument.

**Mandatory argument**: 

None

**Output** : ds1 - ds2

**Climaf call example** ::
 
  >>> ds1= .... #some dataset, with whatever variable
  >>> ds2= .... #some other, compatible dataset
  >>> ds1_minus_ds2 = sub(ds1,ds2) # ds1 - ds2 ; equivalent to minus(ds1,ds2)

  >>> ds1= .... #some dataset, with whatever variable
  >>> c = '-1'  #a constant
  >>> ds1_minus_c = sub(ds1,c) # ds1 - c


**Side effects** : none

**Implementation** : shortcut to 'minus(dat1,dat1)' and ccdo(dat,operator='subc,'+c)

