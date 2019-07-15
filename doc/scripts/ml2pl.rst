ml2pl : interpolates a field from model levels to pressure levels
------------------------------------------------------------------

Returns a field on pressure levels.

Only available on Ciclad at IPSL (for the moment).

**Provider / contact** : Lionel Guez (LMD) for climaf at meteo dot fr

**Input** : a variable (CliMAF dataset) you want to interpolate and a pressure field (CliMAF dataset) with the same dimensions

The user can set a custom set of pressure levels by providing them with fixed_fields via a txt file (see press_levels.txt in scripts/ for an example) 

**Mandatory argument**: 

None

**Output** : the difference

**Climaf call example** ::
 
  >>> ds_ua= .... #some dataset, with whatever variable
  >>> ds_pres= .... #some other, compatible dataset
  >>> ua_on_preslev=ml2pl(ds_ua,ds_pres)

**Side effects** : only available on Ciclad

**Implementation** : using the binary /data/guez/build/Ml2pl/ml2pl

