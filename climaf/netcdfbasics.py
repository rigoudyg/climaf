#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

import datetime
import re
import warnings
import xarray as xr
import six
from datetime import timedelta

from climaf.utils import Climaf_Error
from env.environment import *
from env.clogging import clogger, dedent
from climaf.period import cperiod, freq_to_minutes, init_period, build_date_regexp_pattern

warnings.filterwarnings("ignore", category=DeprecationWarning)


def varOfFile(filename):
    lvars = varsOfFile(filename)
    if len(lvars) > 1:
        # Special case of IPSL-CM outputs
        for area in ["area", "cell_area", "aire"]:
            if area in lvars:
                lvars.remove(area)
        for var in lvars.copy():
            if re.findall("_b(ou)?nds$", var):
                lvars.remove(var)
    if len(lvars) > 1:
        clogger.error(
            "Got multiple variables (%s) and no direction to choose  - File is %s" % (repr(lvars), filename))
        return None
    if len(lvars) == 1:
        return lvars[0]


def varsOfFile(filename, all=False):
    """
    Returns the list of variable names in NetCDF file FILENAME. If ALL is False
    only variable which are not dimensions nor scalar coordinates are returned
    """
    lvars = list()
    with xr.open_dataset(filename, decode_times=False) as ds:
        lvars = set(list(ds.variables.keys()))
        if all is False:
            # remove dimensions
            lvars = lvars - set(list(ds.dims))
            # Remove scalar coordinates
            lvars = [elt for elt in lvars if not (
                hasattr(ds[elt], "axis") or hasattr(ds[elt], "bounds"))]
            # Remove variables which are related to dimensions (e.g. dim bounds....)
            lvars = [elt for elt in lvars
                     if not re.findall("(^lat|^lon|^LAT|^LON|nav_lat|nav_lon|^time|crs|_bnds$)", elt)]
        else:
            lvars = lvars & set(list(ds.dim))
    return sorted(list(lvars))


def fileHasVar(filename, varname):
    """
    returns True if FILENAME has variable VARNAME
    """
    rep = False
    clogger.debug("opening " + filename +
                  " for checkin if has variable " + varname)
    with xr.open_dataset(filename, decode_times=False) as ds:
        return varname in ds


def fileHasDim(filename, dimname):
    """
    returns True if FILENAME has dimension dimname
    """
    return dimname in dimsOfFile(filename)


def dimsOfFile(filename):
    """
    returns the list of dimensions of the netcdf file filename
    """
    clogger.debug("opening " + filename + " for checking the dimensions")
    with xr.open_dataset(filename, decode_times=False) as ds:
        return ds.dims


def model_id(filename):
    """

    """
    return attrOfFile(filename, 'model_id', 'no_model')


def timeLimits(filename_or_timedim, use_frequency=False, strict_on_time_dim_name=True,
               cell_methods=None, time_average=None):
    """Returns a cperiod object representing the time period covered by a datafile or 
    by a cftime Index (including the time averaging periods at both end if applicable)

    For the case of a datafile : if there is a time bounds variable in file, it is 
    used. Otherwise, if USE_FREQUENCY is True or a string, method below is applied

    For the case of a cftime Index argument, its first and last time
    values are used, except is USE_FREQUENCY is True or a string; in that last 
    case, method below applies

    When no time bounds are available, or when arg is a cftime Index
    and USE_FREQUENCY is True or a string, the method applied is :
      -  if TIME_AVERAGE is False, we assume that values are instant values
      -  otherwise, arg CELL_METHODS is scrutinized to detect a 'time.*:mean' 
         occurrence and decide if we have instant values. 
           * If no, 
           * If yes, the frequency 
         between time values is computed, and used to compute bounds by adding 
         half a period at both ends (for the case of month, we assume that full 
         months are averaged and adjust to month start/end )

    """
    tdim = None
    if isinstance(filename_or_timedim, six.string_types):
        with xr.open_dataset(filename_or_timedim, use_cftime=True) as ds:
            for var in ds.variables:
                if re.findall("^time.*b(ou)?nds$", var):
                    tdim = ds.variables[var]
                    break
        if tdim is not None:
            start = tdim[0, 0]  # This is a DataArray
            end = tdim[-1, 1]
        else:
            clogger.warning(
                f"No time bounds variable in {filename_or_timedim}")
            if not use_frequency:
                return None
    else:
        if not use_frequency:
            # Assume that the provided cfTime index represents time bounds
            tdim = filename_or_timedim
    #
    if tdim is not None:
        start = start.values.flatten()[0]  # this is a nectdf time object
        end = end.values.flatten()[0]
        return cperiod(start, end)
    #
    else:
        if not isinstance(filename_or_timedim, six.string_types):
            timedim = filename_or_timedim
            start = timedim.values.flatten()[0]
            end = timedim.values.flatten()[-1]
        else:
            with xr.open_dataset(filename_or_timedim, use_cftime=True) as ds:
                time_error_message = "No time dimension found in %s, dims are %s" % \
                                     (filename_or_timedim, [str(d) for d in ds.dims])
                if "time" in ds.variables:
                    timedim = "time"
                elif strict_on_time_dim_name:
                    clogger.warning(time_error_message)
                    return None
                else:
                    timedim = [dim for dim in ds.dims if re.findall("^time.*", str(dim))]
                    found = len(timedim) > 0
                    if found:
                        timedim = timedim[0]
                if found:
                    start = ds[timedim][0].values.flatten()[0]
                    end = ds[timedim][-1].values.flatten()[0]
                    timedim = ds[timedim]
                else:
                    clogger.error(time_error_message)
                    return None
        #
        if cell_methods is not None and time_average is None:
            # time_average = (re.findall( '.*time *: *mean', cell_methods)[0] != '')
            # Some HadISST data have cell_methods = 'time: lat: lon: mean', which
            # does not comply with the CF convention. We have to account for it.
            time_average = (re.findall(' *time: *([a-zA-Z0-9]*: *)*?mean', cell_methods) != [])

        # Diagnose delta, the time interval between data samples
        if time_average is False:
            delta = 0
        else:
            if not use_frequency:
                raise Climaf_Error("No time bounds variable in file or no time dimension provided, " +
                                   "and use_frequency is False (%s)" % filename_or_timedim)
            try:
                data_freq = xr.infer_freq(timedim)
            except:
                data_freq = use_frequency
            if not data_freq:
                data_freq = use_frequency
            if data_freq == "monthly":
                data_freq = "MS"
            if not data_freq:
                raise Climaf_Error("Xarray cannot infer frequency using time dimension %s" %
                                   timedim.name + os.linesep + str(timedim))
            clogger.debug("In timeLimits: calling freq_to_minutes with data_freq=%s", data_freq)
            delta = freq_to_minutes(data_freq) / 2
            if delta is None:
                clogger.error("Frequency %s not yet managed" % data_freq)
                return None
            if data_freq[-2:] == "MS" and start.day in [14, 15, 16] and end.day in [14, 15, 16]:
                delta = "special_month"
        #
        start = timedim[0].values.flatten()[0]
        if isinstance(start, float):
            start = convert_date_string_to_datetime(str(int(start)))
        end = timedim[-1].values.flatten()[0]
        if isinstance(end, float):
            end = convert_date_string_to_datetime(str(int(end)))
        if delta == "special_month":
            start = start - timedelta(days=start.day - 1, hours=12)
            end = end + timedelta(days=end.daysinmonth -
                                  end.day + 1, hours=-12)
        else:
            start = start - timedelta(minutes=delta)
            end = end + timedelta(minutes=delta)
        return cperiod(start, end)


def convert_date_string_to_datetime(a_date):
    date_formats = ["%Y", "%Y%m", "%Y%m%d",
                    "%Y%m%d%H", "%Y%m%d%H%M", "%Y%m%d%H%M%S"]
    length = len(a_date)
    if length in [4, 6, 8, 10, 12, 14]:
        # The index of the date format is 0 for 4-digits date, 1 for 6-digits date...
        pattern = date_formats[(length - 4) // 2]
    else:
        clogger.error(
            "The entry date has a length of %d, can not handle it" % len(a_date))
        raise ValueError(
            "The entry date has a length of %d, can not handle it" % len(a_date))
    return datetime.datetime.strptime(a_date, pattern)


def isVerticalLevel(varname):
    return varname.lower() in ['level', 'levels', 'lev', 'levs', 'depth', 'deptht', 'presnivs', 'olevel'] \
        or 'plev' in varname.lower()


def verticalLevelName(filename):
    with xr.open_dataset(filename, decode_times=False) as ds:
        varname = [var for var in ds.variables if isVerticalLevel(var)]
        if len(varname) > 0:
            return varname[0]
        else:
            raise Climaf_Error(
                "No vertical level dimension identified in %s" % filename)


def verticalLevelUnits(filename):
    lev = verticalLevelName(filename)
    if lev:
        with xr.open_dataset(filename, decode_times=False) as ds:
            return ds[lev].units


def verticalLevelValues(filename):
    lev = verticalLevelName(filename)
    if lev:
        with xr.open_dataset(filename, decode_times=False) as ds:
            return list(ds[lev].values)


def attrOfFile(filename, attribute, default=None):
    with xr.open_dataset(filename, decode_times=False) as ds:
        return getattr(ds, attribute, default)


def attrOfDataset(filename, variable, attribute, default=None):
    with xr.open_dataset(filename, decode_times=False) as ds:
        return getattr(ds[variable], attribute, default)


def infer_freq(times, monthly):
    """A wrapper for xarray.infer_freq, for alleviating its shortcoming in
    infering frequency monthly. If MONTHLY is True, an adhoc,
    approximate algorithm is used for checking if TIMES represent
    monthly data. Otherwise, xarray.infer_freq is used """
    #
    if not monthly:
        return xr.infer_freq(times)
    time_values = times.values.flatten()
    OK = 1
    for cpt in range(0, 4):
        ptim = time_values[cpt]
        tim = time_values[cpt + 1]
        delta = tim - ptim
        if delta < timedelta(days=29) or delta > timedelta(days=31):
            OK = 0
    if OK == 1:
        return "MS"
    else:
        return None


def extract_period(filename, template, use_frequency=False):
    """Extract the period from FILENAME (or from the file itself),
    using TEMPLATE, which is a pattern possibly using keyword
    "${PERIOD}"

    First replaces globing wildcards (*,?) by regexp equivalent
    wildcards (.*,.) in TEMPLATE

    Next, if TEMPLATE includes the period keyword "${PERIOD}",
    replaces it with a regexp for matching pairs of dates

    If test is OK, the changed template is used to extract the date values,
    from FILENAME 

    Otherwise, use timeLimits to extract period by
    reading datafile's time dimension

    """
    # Construct regexp for extracting dates from filename
    template_toreg = template.replace(
        r"*", r".*").replace(r"?", r".").replace(r"+", r"\+")
    period_keyword = "${PERIOD}"
    #
    if template_toreg.find(period_keyword) >= 0:
        date_regexp = template_toreg.replace(
            period_keyword, build_date_regexp_pattern(), 1)
    else:
        date_regexp = None
    #
    if date_regexp:
        tperiod = re.sub(date_regexp, r'\g<period>', filename)
        clogger.debug("")
        clogger.debug("Extracting period using regexp %s in filename %s" % (
            date_regexp, filename))
        if tperiod == filename:
            clogger.error("Cannot find a period in %s with regexp %s" % (filename, date_regexp) +
                          " \n template=%s, kw=%s" % (template, period_keyword))
            return None
        else:
            clogger.debug("Found period=" + tperiod)
            fperiod = init_period(tperiod)
            return fperiod
    else:
        try:
            fperiod = timeLimits(filename, use_frequency=use_frequency)
            return fperiod
        except:
            clogger.info(
                "Cannot yet filter re. time using only file content or xarray (for %s)." % filename)
