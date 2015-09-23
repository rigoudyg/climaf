import re

from climaf.clogging import clogger, dedent
from climaf.period import cperiod

class Climaf_Netcdf_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)
    def __str__(self):
        return `self.valeur`

try :
    from scipy.io.netcdf import netcdf_file as ncf
except ImportError:
    try :
        from NetCDF4 import Dataset as ncf
    except ImportError:
        raise Climaf_Netcdf_Error("Netcdf handling is yet available only with modules scipy.io.netcdf or NetCDF4")


def varOfFile(filename) :
    lvars=varsOfFile(filename)
    if len(lvars) > 1 :
        clogger.debug("Got multiple variables (%s) and "
                      "no direction to choose  - File is %s" %\
                          (`lvars`,filename))
        return(None)
    if(lvars)==1 : return lvars[0]

def varsOfFile(filename) :
    """ 
    returns the list of non-dimensions variable in NetCDF file FILENAME
    """
    lvars=[]
    with ncf(filename, 'r') as fileobj:
        for filevar in fileobj.variables :
            if ((filevar not in fileobj.dimensions) and
                not re.findall("^lat",filevar) and
                not re.findall("^lon",filevar) and
                not re.findall("^time_",filevar) and
                not re.findall("_bnds$",filevar) ):
                lvars.append(filevar)
        return(lvars)


def fileHasVar(filename,varname):
    """ 
    returns True if FILENAME has variable VARNAME
    """
    rep=False
    clogger.debug("opening "+filename)
    with ncf(filename, 'r') as fileobj:
        for filevar in fileobj.variables :
            if filevar == varname :
                rep=True
                break
        return(rep)

def model_id(filename):
    """ 

    """
    rep='no_model'
    clogger.debug("opening "+filename)
    with ncf(filename, 'r') as f:
        if 'model_id' in dir(f) : rep=f.model_id
    return(rep)
    
def timeLimits(filename) :
    #
    try :
        import netcdftime
    except :
        raise Climaf_Netcdf_Error("Netcdf time handling is yet available only with module netcdftime")
    #
    with ncf(filename) as f:
        if 'time_bnds' in f.variables :
            tim=f.variables['time_bnds']
            start=tim[0,0] ; end=tim[-1,1] 
            ct=netcdftime.utime(tim.units, calendar=tim.calendar)
            return cperiod(ct.num2date(start),ct.num2date(end))
        else:
            return None
            #raise Climaf_Netcdf_Error("No time bounds in file %s, and no guess method yet developped (TBD)"%filename)
        
