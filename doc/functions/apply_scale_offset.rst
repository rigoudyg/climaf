apply_scale_offset : Apply a scale and an offset to a CliMAF object using CliMAF ccdo
---------------------------------------------------------------------------------------

Multiply a field with a scale factor and add an offset

 **Note** : this function should be used parcimonioulsy because the model in CliMAF 
 for dealing with scaling and offset is rather :

      - to automatically scale and offset the data to S.I. units at
        input/reading stage; this si done by declaring scaling for
        each relevant variable in a project using function
        :py:func:`~climaf.dataloc.calias`; it also allows to set the units
      - if the S.I. units are not suitable for a plot, to use plot 
        operators arguments 'scale' and 'offset' to change the values


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

