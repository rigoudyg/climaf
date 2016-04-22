iplot : display the plot associated with a CliMAF object in an IPython Notebook
---------------------------------------------------------------------------------------

Interactive version of cshow() for display in IPython Notebooks
Similar to implot() but you provide a plot (a CliMAF object produced with plot() )
implot() takes directly a field as argument.

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : any CliMAF plot

**Mandatory argument**: 

None

**Output** : an image in an IPython Notebook

**Climaf call example** ::
 
  >>> my_plot = plot(...)
  >>> iplot(myplot)

**Side effects** : none

**Implementation** : shortcut to 'Image(filename=cfile(map))' ; uses 'from IPython.display import Image'

