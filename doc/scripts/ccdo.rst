ccdo : invoke CDO with a unary operator
---------------------------------------------------------

Apply CDO on a single dataset or object, with a CDO operator as argument 

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any object or dataset 

**Mandatory argument**: ``operator`` : a CDO unary operator (as e.g. fldavg, timavg ...)

**Output** : the result of CDO operator

**Climaf call example** ::
 
  >>> ds= .... #some dataset, with whatever variable
  >>> annual_cycle=ccdo(ds,operator='ymonavg') # 

**Side effects** : none

**Implementation** : using script mcdo.sh, which can also select a variable, a time period, a latlon box ...; 

** Note** : because the choice of operatr is left to the user, CliMAF assumes that the output has squeezed dimension(s) over time or space (and hence will not attempt to re-use this output for extracting a sub-period or sub-domain)

