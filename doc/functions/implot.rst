implot : interactive version of 'plot' for display in an IPython Notebook
---------------------------------------------------------------------------------------

Interactive version of plot() for display in IPython Notebooks
implot() takes directly a field as argument.

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : the attributes of a call to plot()

**Mandatory argument**: 

None

**Output** : an image in an IPython Notebook

**Climaf call example** ::
 
  >>> dat = ds(...)
  >>> implot(climato(dat))

**Side effects** : none

**Implementation** : shortcut to 'Image(filename=cfile(plot(field,**kwargs)))' ; uses 'from IPython.display import Image'

