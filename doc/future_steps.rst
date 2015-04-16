Future steps and wish list
---------------------------

The next developments will adress, probably in that order :

- handling geographical domains which are lists of locations

- adding graphic operators : 

  - verastile (and nice) curve plot, 

  - cross-sections [ in z, p, log(p)], 

  - Hoevmuller diagram, 

  - Taylor diagram

- adding graphic functions for composing pages with individual graphs, and for building html index

- cache management functions : 

  - add a grading scheme on cache results : a value is set by the user, and used as a criterion to protect some data when cleaning the cache

  - list / count / delete files in cache based on various criteria (modification date, access date, size, facets, grade)

  - use a hierarchy of cache locations, some being shared among various users

- interfacing the Drakkar's community CDFtools

- managing masks (e.g. for ocean, tropics, lakes, oceanic basins ...)

- managing dataset ensembles

- an alias feature (allow to declare that a variable can be decude by some offset and scaling from another one); however, the 'derived variable' feature, albeit sub-optimal, already allows for that; see :py:func:`~climaf.operators.derive`

- chunking : automatically splitting e.g. the time dimension when processing a dataset if memory issues call for





The wish list, is the list of features wich priority is lesser; you may complement it by sending suggestions to ``climaf at meteo dot fr`` :

- develop a fast remapping operator (provided there is some evidence that CDO's reampping was sub-optimal)

- add to every result file some metadata reagrding the basic data files used at the origin of all processing : creation date, version number if applicable

- a built-in arithmetics on datasets

- manage operators which provide multi-variable NetCDF files