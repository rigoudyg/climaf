time_average : compute time average for all time steps
-------------------------------------------------------

Apply operator timavg on the object/dataset to another grid, using CDO

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-3560002.8.14

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**: none

**Optional arguments**: none

**Output** : the time-averaged object

**Climaf call example** ::
 
  >>> ds= .... #some dataset, with whatever variable
  >>> ds_tavg=time_average(ds)

**Side effects** : None

**Implementation** : CDO call with operator ``timavg``,  through script mcdo.sh

