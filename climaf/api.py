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
from climaf import version
from climaf.classes   import cdef,cdataset,ds,cproject,cprojects,calias
from climaf.driver    import ceval,varOf 
from climaf.dataloc   import dataloc 
from climaf.operators import cscript, scripts as cscripts, derive, operators
from climaf.cache     import craz, csync as csave , cdump, cdrop
from clogging         import clogger, clog, clog_file
import climaf.standard_operators 

#########################
# CliMAF init phase
#########################

Climaf_version="0.5.1"

#: Path for the CliMAF package. From here, can write e.g. ``cpath+"../scripts"``. The value shown in the doc is not meaningful for your own CliMAF install
cpath=os.path.abspath(climaf.__path__[0]) 

# Set default logging levels
clog(os.getenv("CLIMAF_LOG_LEVEL","error"))
clog_file(os.getenv("CLIMAF_LOGFILE_LEVEL","info"))

from climaf.site_settings import onCiclad, atCNRM
from climaf.projects      import *
climaf.standard_operators.load_standard_operators()
#print "ops="+`climaf.operators.scripts.keys()`

print "climaf.version="+climaf.version

# Read user config file
conf_file=os.path.expanduser("~/.climaf")

if os.path.isfile(conf_file) :
    #execfile(conf_file, {"Climaf_version":Climaf_version })
    with open(conf_file) as fobj:
       startup_file = fobj.read()
       exec(startup_file)

# Decide for cache location
if onCiclad : default_cache="/data/"+os.getenv("USER")+"/climaf_cache"
else: default_cache="~/tmp/climaf_cache"
climaf.cache.setNewUniqueCache(os.getenv("CLIMAF_CACHE",default_cache))


#########################
# Commodity functions
#########################

def cfile(object,target=None,ln=None,deep=None) :
    """
    Provide the filename for a CliMAF object, or copy this file to target. Launch computation if needed. 

    Args:
      object (CliMAF object) : either a dataset or a 'compound' object (e.g. the result of a CliMAF operator)
      target (str, optional) : name of the destination file or link; CliMAF will anyway store the result
       in its cache; 

      ln (logical, optional) : if True, target is created as a symlink to the CLiMAF cache file

      deep (logical, optional) : governs the use of cached values when computing the object:
      
        - if missing, or None : use cache as much as possible (speed up the computation)

        - False : make a shallow computation, i.e. do not use cached values for the 
          top level operation

        - True  : make a deep computation, i.e. do not use any cached value

    Returns: 

      - if 'target' is provided : returns this filename (or linkname) if computation is 
        successful ('target' contains the result), and None otherwise; 

      - else : returns the filename in CliMAF cache, which contains the result (and None if failure)


    """
    clogger.debug("cfile called on "+str(object))  
    result=climaf.driver.ceval(object,format='file',deep=deep)
    if target is None : return result
    else :
        if result is not None :
            if ln :
                os.remove(os.path.expanduser(target))
                os.symlink(result,os.path.expanduser(target))
            else :
                shutil.copyfile(result,os.path.expanduser(target))
        return target

def cshow(obj) :
    """ 
    Provide the in-memory value of a CliMAF object. 
    For a figure object, this will lead to display it
    ( launch computation if needed. )
    """
    clogger.debug("cshow called on "+str(obj)) 
    return climaf.driver.ceval(obj,format='MaskedArray')

def  cMA(obj,deep=None) :
    """
    Provide the Masked Array value for a CliMAF object. Launch computation if needed.

    Args:
      obj (CliMAF object) : either a datset or a 'compound' object (like the result of a CliMAF standard operator)
      deep (logical, optional) : governs the use of cached values when computing the object

        - if missing, or None : use cache as much as possible
        - False : make a shallow computation, i.e. do not use cached values for top level operation
        - True  : make a deep computation, i.e. do not use any cached value

    Returns: a Masked Array containing the object's value

    """
    clogger.debug("cMA called with arguments"+str(obj)) 
    return climaf.driver.ceval(obj,format='MaskedArray',deep=deep)

def cexport(*args,**kwargs) :
    """ Alias for climaf.driver.ceval. Create synonyms for arg 'format'

    """
    clogger.debug("cexport called with arguments"+str(args))  
    if "format" in kwargs :
        if (kwargs['format']=="NetCDF" or kwargs['format']=="netcdf" or kwargs['format']=="nc") :
            kwargs['format']="file" 
        if (kwargs['format']=="MA") :
            kwargs['format']="MaskedArray" 
    return climaf.driver.ceval(*args,**kwargs)

def cimport(cobject,crs) :
    clogger.debug("cimport called with argument",cobject)  
    clogger.debug("should check syntax of arg 'crs' -TBD")
    clogger.warning("cimport is not for the dummies - Playing at your own risks !")
    import numpy, numpy.ma
    if isinstance(cobject,numpy.ma.MaskedArray) :
        clogger.debug("for now, use a file for importing - should revisit - TBD")
        clogger.error("not yet implemented fro Masked Arrays - TBD")
    elif isinstance(cobject,str) :
        cache.register(cobject,crs)
    else :
        clogger.error("argument is not a Masked Array nor a filename",cobject)
    


