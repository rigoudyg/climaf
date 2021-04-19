#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

import re

from env.clogging import clogger, dedent
from climaf.period import cperiod
from env.environment import *
from climaf.anynetcdf import ncf


class Climaf_Netcdf_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)


def varOfFile(filename):
    lvars = varsOfFile(filename)
    if len(lvars) > 1:
        clogger.debug("Got multiple variables (%s) and no direction to choose  - File is %s" % (repr(lvars), filename))
        return None
    if len(lvars) == 1:
        return lvars[0]


def varsOfFile(filename):
    """
    Returns the list of non-dimensions variable in NetCDF file FILENAME
    """
    lvars = []
    fileobj = ncf(filename, 'r')
    vars = fileobj.variables
    if isinstance(vars, dict):
        svars = list(vars)
    for filevar in svars:
        if ((filevar not in fileobj.dimensions) and
                # other variables linked to dimensions
                not re.findall("^lat", filevar) and
                not re.findall("^lon", filevar) and
                not re.findall("^LAT", filevar) and
                not re.findall("^LON", filevar) and
                not re.findall("nav_lat", filevar) and
                not re.findall("nav_lon", filevar) and
                not re.findall("^time_", filevar) and
                not re.findall("crs", filevar) and
                not re.findall("_bnds$", filevar)):
            lvars.append(filevar)
    # case of scalar coordinates
    if isinstance(vars, dict):
        for var in vars.keys():
            if var in lvars and (hasattr(vars[var], "axis") or hasattr(vars[var], "bounds")):
                lvars.remove(var)

    fileobj.close()
    return lvars


def fileHasVar(filename, varname):
    """
    returns True if FILENAME has variable VARNAME
    """
    rep = False
    clogger.debug("opening " + filename + " for checkin if has variable " + varname)
    fileobj = ncf(filename)
    vars = fileobj.variables
    if isinstance(vars, dict):
        vars = list(vars)
    for filevar in vars:
        if filevar == varname:
            rep = True
            break
    fileobj.close()
    return rep


def fileHasDim(filename, dimname):
    """
    returns True if FILENAME has dimension dimname
    """
    rep = False
    clogger.debug("opening " + filename + " for checkin if has dimension " + dimname)
    fileobj = ncf(filename)
    dims = fileobj.dimensions
    vars = fileobj.variables
    if isinstance(dims, dict):
        dims = list(dims)
    if isinstance(vars, dict):
        vars = list(vars)
    dims = dims + vars
    for filedim in dims:
        if filedim == dimname:
            rep = True
            break
    fileobj.close()
    return rep


def dimsOfFile(filename):
    """
    returns the list of dimensions of the netcdf file filename
    """
    clogger.debug("opening " + filename + " for checking the dimensions")
    fileobj = ncf(filename)
    dims = fileobj.dimensions
    if isinstance(dims, dict):
        dims = list(dims)
    fileobj.close()
    return dims


def model_id(filename):
    """

    """
    rep = 'no_model'
    clogger.debug("opening " + filename)
    f = ncf(filename, 'r')
    if 'model_id' in dir(f):
        rep = f.model_id
    f.close()
    return rep


def timeLimits(filename):
    #
    try:
        import netcdftime
    except ImportError:
        try:
            from NetCDF4 import netcdftime
        except ImportError:
            raise Climaf_Netcdf_Error("Netcdf time handling is yet available only with module netcdftime")
    #
    rep = None
    f = ncf(filename)
    if 'time_bnds' in f.variables:
        tim = f.variables['time_bnds']
        if 'units' in dir(tim) and 'calendar' in dir(tim):
            start = tim[0, 0]
            end = tim[-1, 1]
            ct = netcdftime.utime(tim.units, calendar=tim.calendar)
            return cperiod(ct.num2date(start), ct.num2date(end))
    f.close()
    return rep
    # raise Climaf_Netcdf_Error("No time bounds in file %s, and no guess method yet developped (TBD)"%filename)
