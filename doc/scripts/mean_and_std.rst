mean_and_std : field mean and standard deviation
-------------------------------------------------

Computes field mean value and field standard deviation using CDO
operators fldmean and fldstd,  and discarding lat/lon coordinates from
CDO output

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-3040002.8.5


**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**:


**Optional arguments**:
  - ``var`` : name of the input variable ; used to provide a
    meaningful name for output ``std``, namely ``std($varin)``.
    CliMAF will take care of providing this argument automatically if needed.

**Outputs** :
  - main output : field mean
  - secondary outputs and their names :
     -  ``std`` : field standard deviation

**Climaf call example** ::
 
  >>> ds= ....some dataset, with whatever variable
  >>> m=mean_and_std(ds)  # m receives the field mean
  >>> dev=m.std           # dev receives operator output named "std", namely the field standard deviation

**Side effects** : create temporary files in the directory provided for output fields

**Implementation** : just two calls to ``cdo`` and the use of ``ncwa`` for discarding
degenerated space dimensions (because CDO does not discard them)


**CliMAF call sequence pattern** (for reference) :: 

  "mean_and_std.sh ${in} ${var} ${out} ${out_sdev}"

