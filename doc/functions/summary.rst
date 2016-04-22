summary : returns the path and filename of a dataset linked with a ds() object with the pairs keywords/values
---------------------------------------------------------------------------------------

summary() returns the path and filename of a dataset associated with a ds() object with the pairs keywords/values.
It is very useful to explore the existing datasets behind a data request with ds().

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html

**Provider / contact** : climaf at meteo dot fr

**Input** : the output of ds() request

**Mandatory argument**: 

None

**Output** : 

**Climaf call example** ::
 
  >>> dat= ds(....)   # some dataset, with whatever variable
  >>> summary(dat) #

**Side effects** : if summary returns a list of files, the user has to specify more precisely the request so that the ds() object points only to one dataset (that might cover multiple files in time).

