.. |sk| image:: swiss_knife_50.png

ccdo2 : |sk| invoke CDO with a bianry operator (i.e. on two datasets)
------------------------------------------------------------------------

Apply CDO on two datasets or objects, with a CDO operator as argument 

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any object or dataset 

**Mandatory argument**: 

- ``operator`` : a CDO unary operator (as e.g. ``div``, ``mul`` ...)

**Output** : the result of CDO operator

**Climaf call example** ::
 
  >>> ds1= .... #some dataset, with whatever variable
  >>> ds2= .... #some dataset, with whatever variable
  >>> ds1_ds2=ccdo2(ds1,ds2,operator='mul') # 

**Side effects** : none

**Implementation** : using cscript('ccdo2','cdo ${operator} ${in_1} ${in_2} ${out}') 

**Note** : because the choice of operator is left to the user, CliMAF assumes that the output has squeezed dimension(s) over time or space (and hence will not attempt to re-use this output for extracting a sub-period or sub-domain)

