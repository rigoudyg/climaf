curl_tau_atm : computes wind stress curl on regular grid (usually atmosphere)
---------------------------------------------------------

Computes the wind stress curl using a ferret script and making some fixes afterwards Computes the wind stress curl using a ferret script and making some fixes afterwards to make the output file suitable for CliMAF.
Ferret core code: let curltau = tauv[d=2,x=@ddc]-tauu[d=1,y=@ddc]

**Reference** : None

**Provider / contact** : Julie Deshayes / Juliette Mignot; climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - a tauu dataset
  - and a tauv dataset
  The script actually expects 'tauu' and 'tauv' variable names.

**Mandatory arguments**: same as inputs

**Optional arguments**: None

**Output** : an output netcdf file with the 'curltau' variable

**Climaf call example**::
 
  >>> ds_tauu = .... # some dataset, with whatever variable
  >>> ds_tauv = .... # some dataset, with whatever variable
  >>> curltau_ds = curl_tau_atm(ds_tauu, ds_tauv) #

**Implementation** : a ferret script

