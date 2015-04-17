from climaf.clogging import clogger

def varOfFile(filename) :
    """ 
    returns the name of the unique non-dimension variable in
    NetCDF file FILENAME, or None if it is not unique
    """
    from Scientific.IO.NetCDF import NetCDFFile as ncf
    varname=None
    fileobj=ncf(filename)
    #import NetCDF4
    #fileobj=netCDF4.Dataset(filename)
    for filevar in fileobj.variables :
        if filevar not in fileobj.dimensions :
            if varname is None : 
                varname=filevar
            else :
                clogger.debug("Got at least two variables (%s and %s) "+\
                                  "and no direction to choose  - File is %s"%\
                                  (varname,filevar,filename))
                return(None)
    fileobj.close()
    return(varname)


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

