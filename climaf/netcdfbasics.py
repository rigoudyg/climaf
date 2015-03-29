from Scientific.IO.NetCDF import NetCDFFile as ncf

def varOfFile(filename) :
    """ 
    returns the name of the unique non-dimension variable in
    NetCDF file FILENAME, or None if it is not unique
    """
    varname=None
    fileobj=ncf(filename)
    #import NetCDF4
    #fileobj=netCDF4.Dataset(filename)
    for filevar in fileobj.variables :
        if filevar not in fileobj.dimensions :
            if varname is None : 
                varname=filevar
            else :
                logging.debug("driver.varOf : Got at least two variables (%s and %s) "+\
                                  "and no direction to choose  - File is %s"%\
                                  (varname,filevar,datafile))
                return(None)
    fileobj.close()
    return(varname)


def fileHasVar(filename,varname):
    """ 
    returns True if FILENAME has variable VARNAME
    """
    rep=False
    varname=None
    fileobj=ncf(filename)
    for filevar in fileobj.variables :
        if filevar == varname :
            rep=True
            break
    fileobj.close()
    return(rep)

