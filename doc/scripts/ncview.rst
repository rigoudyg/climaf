ncview : launch ncview on dataset 
---------------------------------------

Launch ncview in the background for displaying the dataset

**References** : 

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - any dataset (but only one)

**Mandatory arguments**:
  - none

**Optional arguments**:
  - none

**Outputs** :
  - none

**Climaf call example** ::
 
  >>> tas= .... #some dataset like e.g. of monthly mean of a low level temperature
  >>> cobj(ncview(tas))

**Side effects** : ncview is launched, displaying the file correspondign to the dataset

**Implementation** : just a call to ``ncview`` 

