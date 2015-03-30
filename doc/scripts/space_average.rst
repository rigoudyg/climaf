space_average : compute space average 
-------------------------------------------------------

Apply CDO operator fldavg on the object/dataset to another grid

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-3040002.8.5

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**: none

**Optional arguments**: none

**Output** : the space-averaged object

**Climaf call example** ::
 
  >>> ds= .... #some dataset, with whatever variable
  >>> ds_tavg=space_average(ds)

**Side effects** : None

**Implementation** : CDO call with operator ``fldavg``,  through script mcdo.sh

