.. |sk| image:: swiss_knife_50.png

ccdo_ens : |sk| invoke CDO with a unary operator on an ensemble of datasets (build with eds or cens)
---------------------------------------------------------

Apply CDO on two datasets or objects, with a CDO operator as argument 

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any object or dataset 

**Mandatory argument**: 

- ``operator`` : a CDO unary operator (as e.g. ``ensavg``, ``ensmax`` ...)

**Output** : the result of CDO operator

**Climaf call example** ::
 
  >>> ens = eds(....) #an ensemble of datasets
  >>> ens_avg = ccdo_ens(ens,operator='ensavg') # 

**Side effects** : none

**Implementation** : using cscript('ccdo_ens','cdo ${operator} ${mmin} ${out}') 

**Note** : because the choice of operator is left to the user, CliMAF assumes that the output has squeezed dimension(s) over time or space (and hence will not attempt to re-use this output for extracting a sub-period or sub-domain)

