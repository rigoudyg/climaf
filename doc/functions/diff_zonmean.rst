diff_zonmean : computes the zonal mean of dat1 and dat2 and returns the difference
---------------------------------------------------------------------------------------

Returns the zonal mean bias of dat1 against dat2
The function first computes the zonal means of dat1 and dat2.
Then, it interpolates the zonal mean field of dat1 on the zonal mean field of dat2 with the function zonmean_interpolation.
It finally returns the bias field.


**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : two CliMAF datasets with at least the latitude dimension, and the same number of time steps

**Mandatory argument**: 

None

**Output** : the zonal mean difference between dat1 and dat2 -> latitude/time (for a lon/lat/time dataset) or latitude/pressure/time (for a lon/lat/pressure/time dataset)

**Climaf call example** ::
 
  >>> ds1= ....   # some dataset, with whatever variable
  >>> ds2= ....   # some dataset, with the same variable as ds1
  >>> diff_zonmean_ds1_ds2 = diff_zonmean(ds1,ds2) # Zonal mean difference between ds1 and ds2

**Side effects** : none

**Implementation** : uses ccdo(...,operator='zonmean'),
ccdo2(...,operator='zonmean') and zonmean_interpolation  

