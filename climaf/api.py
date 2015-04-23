"""
CliMAF module ``api`` defines functions for basic CliMAF use : a kind of Application Programm Interface for scripting in Python with CliMAF for easy climate model output processing.

It also imports a few functions from other modules, and declares a number of 'CliMAF standard operators'

Main functions are :

- for data definition and access :

 - ``cproject``: declare a project and its non-standard attributes/facets

 - ``dataloc`` : set data locations for a series of experiments

 - ``cdef``    : define some default values for datasets attributes

 - ``ds``      : define a dataset object (actually a front-end for ``cdataset``)

 - ``derive``  : define a variable as computed from other variables

 - `` calias`` : describe how a variable is derived form another, single, one, and which
   variable name should be used in deriving data filename for this variable 

- for processing the data 

 - ``cscript`` : define a new CliMAF operator (this also defines a new Python function)

 - ``cMA``     : get the Masked Array value of a CliMAF object (compute it)

- for managing/viewing results :

 - ``cfile``   : get the file value of a CliMAF object (compute it)

 - ``cshow``   : display a result of type 'figure'

 - ``cdump``   : tell what's in cache

 - ``cdrop``   : delete the cached file for an object

 - ``craz``    : reset cache

 - ``csync``   : save cache index to disk


- utility functions :

 - ``clog``    : tune verbosity

 - ``clog_file``    : tune verbosity for log file

"""
# Created : S.Senesi - 2014


import os, os.path, shutil, logging
#
import climaf

# Declare standard projects and standard data locations
from climaf.projects import *

#####################################################################################################################
# All CliMAF functions we want to provide as top-level functions when this module is loaded as "from ... import *"
#####################################################################################################################
#
from classes   import cdef,cdataset,ds,cproject,cprojects,calias
from driver    import ceval, varOf, cfile, cshow, cMA, cimport, cexport 
from dataloc   import dataloc 
from operators import cscript, scripts as cscripts, derive, operators
from cache     import craz, csync as csave , cdump, cdrop
from clogging  import clogger, clog, clog_file
from site_settings import atCNRM, onCiclad

# CliMAF standard dynamic operators
from climaf.operators import *

#: Path for the CliMAF package. From here, can write e.g. ``cpath+"../scripts"``. The value shown in the doc is not meaningful for your own CliMAF install
cpath=os.path.abspath(climaf.__path__[0]) 

