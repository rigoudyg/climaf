diff_regridn : regrids dat1 and dat2 on a common cdogrid and returns the difference (using regridn and minus)
---------------------------------------------------------------------------------------

Regrids dat1 on dat2 on a common grid and returns the difference between dat1 and dat2
The default cdogrid is 'n90'

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : two CliMAF objects with the same number of time steps

**Mandatory argument**: 

None

**Output** : difference between dat1 and dat2

**Climaf call example** ::
 
  >>> dat1= ....   # some dataset, with whatever variable
  >>> dat2= ....   # some dataset, with the same variable as dat1
  >>> diff_dat1_dat2 = diff_regridn(dat1,dat2) # -> uses cdogrid='n90'
  >>> diff_dat1_dat2 = diff_regridn(dat1,dat2,cdogrid='r180x90') # -> Returns the difference on 2° grid


**Side effects** : none

**Implementation** : shortcut to 'minus ( regridn( data1, cdogrid=cdogrid), regridn( data2, cdogrid=cdogrid ))'

