timeplot : simple timeplot for a single variable
---------------------------------------------------

Creates a figure for time evolution of the dataset variable
The plot is yet ugly, and will be improved soon

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
  >>> fig=timeplot(tas)
  >>> cobj(fig)           # to have the figure computed and dsiplayed in a single call
  >>> figfile=cfile(fig)  # to both launch figure compute, an get a filename for the figure

**Side effects** : none

**Implementation** : uses ``xmgrace`` 
