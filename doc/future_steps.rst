Future steps and wish list
---------------------------

The next developments will adress, possibly in that order :

- adding graphic operators or features : 

  - vectors on scalar fields
  - Hoevmoeller diagram
  - Taylor diagram

- interfacing the Drakkar community CDFtools
- managing masks (e.g. for ocean, tropics, lakes, oceanic basins ...)
- handling geographical domains which are lists of locations
- chunking : automatically splitting e.g. the time dimension when processing a dataset (provided memory issues actually call for that)
- further cache management functions : 
  - add a grading scheme on cache results : a value is set by the user, and used as a criterion to protect some data when cleaning the cache
  - use a hierarchy of cache locations, some being shared among various users
- figure pages sharing a single, common palette


The wish list, is the list of features wich priority is lesser; you may complement it by sending suggestions to ``climaf at meteo dot fr`` :

- use CliMAF as a data browser 
- develop a fast remapping operator (provided there is some evidence that CDO reampping was sub-optimal)
- add to every result file some metadata regarding the basic data files used at the origin of all processing : creation date, version number if applicable
- a built-in arithmetics on datasets
- manage operators which provide multi-variable NetCDF files
