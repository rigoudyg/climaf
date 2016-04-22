addc : add a constant to a field using CliMAF ccdo and CDO operator addc
---------------------------------------------------------------------------------------

Add a constant to a field

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any ds object and a constant c (string or float)

**Mandatory argument**: 

None

**Output** : ds+c

**Climaf call example** ::
 
  >>> ds= ....   # some dataset, with whatever variable
  >>> c = 273.15 # a constant
  >>> ds_plus_c = addc(ds,c) # ds+c

**Side effects** : none

**Implementation** : shortcut to 'ccdo(ds,operator='addc,'+str(c))'

