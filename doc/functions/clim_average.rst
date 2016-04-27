clim_average : climatology of a dataset on the specified season, month or for the annual mean
------------------------------------------------------------------------------------------------

    Computes climatological averages on the annual cycle of a dataset, on the months 
    specified with 'season', either:

    - the annual mean climatology (season => 'ann','annual','time_average','clim','climatology','annual_average','anm')

    - seasonal climatologies (e.g. season = 'DJF' or 'djf' to compute the seasonal climatology 
      over December-January-February; available seasons: DJF, MAM, JJA, SON, JFM, JAS, JJAS

    - individual monthly climatologies (e.g. season = 'january', 'jan', '1' or 1 to get 
      the climatological January)

    - annual maximum or minimum (typically makes sense with the mixed layer depth)

    Note that you can use upper case or lower case characters to specify the months or seasons.
    
    clim_average computes the annual cycle for you.


**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any CliMAF field

**Mandatory argument**: a character string for a season, month or annual mean, or float for a given month

**Output** : a CliMAF object corresponding to the climatology of dat on the specified season, month or for the annual mean

**Climaf call example** ::
 
  >>> dat= ....   # some dataset, with whatever variable
  >>> climds_JFM = clim_average(dat,'JFM')         # The climatology of dat over January-February-March
  >>> climds_ANM = clim_average(dat,'annual_mean') # The annual mean climatology
  >>> climds_September = clim_average(dat,'September') # The annual mean climatology of September
  >>> climds_September = clim_average(dat,9) # Same as previous example, with a float

**Side effects** : none

**Implementation** :

uses annual_cycle to compute the annual cycle

time_average(ccdo(scyc,operator='selmon,'+selmonths)) for the seasonal averages

ccdo(scyc,operator='selmon,'+selmonth) for the monthly climatologies

ccdo(scyc,operator='timmax') and ccdo(scyc,operator='timmin') for the annual minimum and maximum

