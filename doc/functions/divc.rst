divc : division of a field by a constant using CliMAF ccdo and CDO operator divc
---------------------------------------------------------------------------------------

Division of a field by a constant c

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any ds object and a constant c (string or float)

**Mandatory argument**: 

None

**Output** : ds/c

**Climaf call example** ::
 
  >>> ds= ....  # some dataset, with whatever variable
  >>> c = 86400 # a constant
  >>> ds_div_c = divc(ds,c) # ds/c

**Side effects** : none

**Implementation** : shortcut to 'ccdo(ds,operator='divc,'+str(c))'

