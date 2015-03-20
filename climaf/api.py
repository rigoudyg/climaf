"""
CliMAF module ``api`` defines functions for basic CliMAF use : a kind of Application Programm Interface for scripting in Python with CliMAF for easy climate model output processing. It also declares a number of standard 'Operators'

Main functions are ``dataloc``, ``cscript``, ``cfile``, ``CMA``, ``cexport``


"""
# Created : S.Senesi - 2014

# The CliMAF software is an environment for Climate Model Assessment. It
# has been developped mainly by CNRM-GAME (Meteo-France and CNRS), and
# by IPSL, in the context of the `CONVERGENCE project
# <http://convergence.ipsl.fr/>`_, funded by The
# French 'Agence Nationale de la Recherche' under grant 
# ANR-13-MONU-0008-01
# 
# This software is governed by the CeCILL-C license under French law and
# biding by the rules of distribution of free software. The CeCILL-C
# licence is a free software license,explicitly compatible with the GNU
# GPL (see http://www.gnu.org/licenses/license-list.en.html#CeCILL)

#Void if logging level already set by the user :
import logging ; logging.basicConfig(level=logging.ERROR)

import climaf, climaf.cache
climafPath=climaf.__path__[0] # Used for test data and test scripts
cpath=climafPath
climaf.cache.setNewUniqueCache("~/tmp/climaf_cache")


from climaf.classes   import cdefault as cdef,cdataset,ds #,cperiod
from climaf.driver    import ceval,varOf #,cfile,cobj 
from climaf.dataloc   import dataloc 
from climaf.operators import cscript, scripts as cscripts, derive
from climaf.cache     import creset as craz, csync as csave , cdump
import climaf.standard_operators

# Commodity functions
def cfile(*args,**kwargs) :
    """ Provides the filename for a CliMAF object. Launches computation if needed

    """
    return climaf.driver.ceval(*args,format='file',**kwargs)

def cobj(*args,**kwargs) :
    """ Provides the in-memory value of a CliMAF object. Launches computation if needed

    """
    #print "args=",args
    #print "kwargs=",keyw
    return climaf.driver.ceval(*args,format='MaskedArray',**kwargs)

def cMA(*args,**kwargs) :
    """ Provides the Masked Array value of a CliMAF object. Launches computation if needed

    """
    return climaf.driver.ceval(*args,format='MaskedArray',**kwargs)

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
    logging.getLogger().setLevel(arg)


