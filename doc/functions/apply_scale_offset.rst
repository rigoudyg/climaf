apply_scale_offset : Apply a scale and an offset to a CliMAF object using CliMAF ccdo
---------------------------------------------------------------------------------------

Multiply a field with a scale factor and add an offset

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any ds object, a scale and an offset (string or float)

**Mandatory argument**: 

None

**Output** : (ds*scale)+offset

**Climaf call example** ::

  >>> # Convert Kelvin to Celsius 
  >>> ds= ....   # some dataset, with whatever variable
  >>> scale = 1.0
  >>> offset = -273.15
  >>> ds_Kelvin_2_Celsius = apply_scale_offset(ds,scale,offset) # (ds*scale)+offset

**Side effects** : none

**Implementation** : shortcut to 'ccdo(ccdo(dat,operator='mulc,'+str(float(scale))),operator='addc,'+str(float(offset)))'

