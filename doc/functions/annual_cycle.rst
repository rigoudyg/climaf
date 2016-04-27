annual_cycle : returns the monthly climatological annual cycle of a dataset using CDO ymonavg
------------------------------------------------------------------------------------------------

Computes the annual cycle as the 12 climatological months of dat

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any CliMAF object

**Mandatory argument**: 

None

**Output** : a CliMAF object that is the monthly climatological annual cycle of dat

**Climaf call example** ::
 
  >>> dat= ....   # some dataset, with whatever variable
  >>> annual_cycle_dat = annual_cycle(dat) #

**Side effects** : none

**Implementation** : shortcut to 'ccdo(dat, operator="ymonavg")'

