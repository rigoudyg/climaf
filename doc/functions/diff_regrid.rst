diff_regrid : regrids dat1 on dat2 and returns the difference (using regrid)
-----------------------------------------------------------------------------

Regrids dat1 on dat2 and returns the difference between dat1 and dat2

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : two CliMAF objects with the same number of time steps

**Mandatory argument**: 

None

**Output** : difference between dat1 and dat2

**Climaf call example** ::
 
  >>> dat1= ....   # some dataset, with whatever variable
  >>> dat2= ....   # some dataset, with the same variable as dat1
  >>> diff_dat1_dat2 = diff_regrid(dat1,dat2)

**Side effects** : none

**Implementation** : shortcut to 'sub(regrid(dat1,dat2), dat2)'

