"""
CliMAF module ``api`` defines functions for basic CliMAF use : a kind of Application Programm Interface for scripting in Python with CliMAF for easy climate model output processing.

It also imports a few functions from other modules, and declares a number of 'CliMAF standard operators'

Main functions are ``dataloc``, ``ds``, ``cdataset``, ``cdef``, ``cscript``, ``cfile``, ``cMA`` :
 - ``dataloc`` : set data locations for a series of experiments
 - ``cdef``    : define some default values for datasets attributes
 - ``ds``      : define a dataset object
 - ``cscript`` : define a new CliMAF operator (this also defines a new Pyhton fucntion)
 - ``cfile``   : get the file         value of a CliMAF object (compute it)
 - ``cMA``     : get the Masked Array value of a CliMAF object (compute it)


Utility functions are  ``clog``, ``cdump``, ``craz``, ``csave``:
 - ``clog``    : tune verbosity
 - ``cdump``   : tell what's in cache
 - ``craz``    : reset cache
 - ``csave``   : save cache index to disk

"""
# Created : S.Senesi - 2014


import os

#Void if logging level already set by the user :
import logging ; logging.basicConfig(level=logging.ERROR)

import climaf, climaf.cache

#: Path for the CliMAF package. From here, can write e.g. ``cpath+"../scripts"``
cpath=os.path.abspath(climaf.__path__[0]) 

climaf.cache.setNewUniqueCache("~/tmp/climaf_cache")


from climaf.classes   import cdefault as cdef,cdataset,ds #,cperiod
from climaf.driver    import ceval,varOf #,cfile,cobj 
from climaf.dataloc   import dataloc 
from climaf.operators import cscript, scripts as cscripts, derive
from climaf.cache     import creset as craz, csync as csave , cdump
import climaf.standard_operators

# Commodity functions
def cfile(object,deep=None) :
    """
    Provide the filename for a CliMAF object. Launch computation if needed.

    Args:
      object (CliMAF object) : either a datset or a 'compound' object (like the result of a CliMAF standard operator)
      deep (logical, optional) : governs the use of cached values when computing the object
      
        - if missing, or None : use cache as much as possible
        - False : make a shallow computation, i.e. do not use cached values for top level operation
        - True  : make a deep computation, i.e. do not use any cached value

    Returns: a filename in CliMAF cache; the file contains the object's value


    """
    return climaf.driver.ceval(object,format='file',deep=deep)

def cobj(*args,**kwargs) :
    """ Provides the in-memory value of a CliMAF object. Launches computation if needed

    """
    #print "args=",args
    #print "kwargs=",keyw
    return climaf.driver.ceval(*args,format='MaskedArray',**kwargs)

def  cMA(object,deep=None) :
    """
    Provide the Masked Array value for a CliMAF object. Launch computation if needed.

    Args:
      object (CliMAF object) : either a datset or a 'compound' object (like the result of a CliMAF standard operator)
      deep (logical, optional) : governs the use of cached values when computing the object

        - if missing, or None : use cache as much as possible
        - False : make a shallow computation, i.e. do not use cached values for top level operation
        - True  : make a deep computation, i.e. do not use any cached value

    Returns: a Masked Array containing the object's value

    """
    return climaf.driver.ceval(object,format='MaskedArray',deep=deep)

def cexport(*args,**kwargs) :
    """ Alias for climaf.driver.ceval. Create synonyms for arg 'format'

    """
    if "format" in kwargs :
        if (kwargs['format']=="NetCDF" or kwargs['format']=="netcdf" or kwargs['format']=="nc") :
            kwargs['format']="file" 
        if (kwargs['format']=="MA") :
            kwargs['format']="MaskedArray" 
    return climaf.driver.ceval(*args,**kwargs)

def cimport(cobject,crs) :
    logging.debug("cimport : should check syntax of arg 'crs' -TBD")
    logging.warning("cimport is not for the dummies - Playing at your own risks !")
    import numpy, numpy.ma
    if isinstance(cobject,numpy.ma.MaskedArray) :
        logging.debug("cimport : for now, use a file for importing - should revisit - TBD")
        logging.error("cimport : not yet implemented fro Masked Arrays - TBD")
    elif isinstance(cobject,str) :
        cache.register(cobject,crs)
    else :
        logging.error("cimport : argument is not a Masked Array nor a filename",cobject)
    

def clog(arg) :
    """
    Sets the verbosity level for CliMAF log messages.

    Among : logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL

    """
    logging.getLogger().setLevel(arg)


