import re

from climaf.clogging import clogger

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
    returns the list of non-dimensions variable in
    NetCDF file FILENAME
    """
    from Scientific.IO.NetCDF import NetCDFFile as ncf
    lvars=[]
    fileobj=ncf(filename)
    #import NetCDF4
    #fileobj=netCDF4.Dataset(filename)
    for filevar in fileobj.variables :
        if ((filevar not in fileobj.dimensions) and
            not re.findall("^lat",filevar) and
            not re.findall("^lon",filevar) and
            not re.findall("^time_",filevar) and
            not re.findall("_bnds$",filevar) ):
            lvars.append(filevar)
    fileobj.close()
    return(lvars)


def fileHasVar(filename,varname):
    """ 
    returns True if FILENAME has variable VARNAME
    """
    from Scientific.IO.NetCDF import NetCDFFile as ncf
    rep=False
    clogger.debug("opening "+filename)
    try :
        fileobj=ncf(filename)
    except:
        clogger.error("Issue opening file "+filename)
        return False
    for filevar in fileobj.variables :
        if filevar == varname :
            rep=True
            break
    fileobj.close()
    return(rep)

def timeLimits(filename) :
    return "185001-185212"
