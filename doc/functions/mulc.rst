mulc : multiplication of a field by a constant using CliMAF ccdo and CDO operator mulc
---------------------------------------------------------------------------------------

Multiplication of a field by a constant c

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any object with a constant (string or float)

**Mandatory argument**: 

None

**Output** : ds * c

**Climaf call example** ::
 
  >>> ds= ....  # some dataset, with whatever variable
  >>> c = 86400 # a constant
  >>> ds_c = mulc(ds,c) # ds*c

**Side effects** : none

**Implementation** : shortcut to 'ccdo(ds,operator='mulc,'+str(c))'

