zonmean : returns the zonal mean of 2D or 3D field using CliMAF ccdo and CDO operator zonmean
---------------------------------------------------------------------------------------

Return the zonal mean of a CliMAF object

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : a CliMAF object

**Mandatory argument**: 

None

**Output** : the zonal mean -> latitude/time (for a lon/lat/time dataset) or latitude/pressure/time (for a lon/lat/pressure/time dataset)

**Climaf call example** ::
 
  >>> ds= ....   # some dataset, with whatever variable
  >>> ds_zonmean = zonmean(ds) # Zonal mean of ds()

**Side effects** : none

**Implementation** : shortcut to 'Shortcut to the command ccdo(dat,operator='zonmean')'

