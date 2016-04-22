climato : returns the annual mean climatology of a field using CliMAF time_average
---------------------------------------------------------------------------------------

Computes the annual mean climatology of dat

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any CliMAF field

**Mandatory argument**: 

None

**Output** : annual mean climatology of the dataset

**Climaf call example** ::
 
  >>> dat= ....   # some dataset, with whatever variable
  >>> climds = climato(dat) #
  >>> cshow(plot(climato(dat)))

**Side effects** : none

**Implementation** : user-friendly shortcut to CliMAF operator time_average(dat)

