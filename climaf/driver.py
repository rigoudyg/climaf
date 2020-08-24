#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CliMAF driver

There is quite a lot of things to document here. Maybe at a later stage ....

"""
from __future__ import print_function, division, unicode_literals, absolute_import

# Created : S.Senesi - 2014

import sys
import os
import os.path
import re
import posixpath
import subprocess
import time
import shutil
import copy
from string import Template
import tempfile
from datetime import datetime
from functools import reduce
from six import string_types

try:
    from commands import getoutput, getstatusoutput
except ImportError:
    from subprocess import getoutput, getstatusoutput


# Climaf modules
import climaf
from climaf.operators_scripts import scriptFlags
from climaf.operators_derive import is_derived_variable, derived_variable, derive
from climaf import classes
from climaf import cache
from climaf.cmacro import instantiate
from env.clogging import clogger, indent as cindent, dedent as cdedent
from climaf.netcdfbasics import varOfFile
from climaf.period import init_period, cperiod, merge_periods
from climaf import xdg_bin
from climaf.classes import allow_errors_on_ds_call
from env.environment import *


# When evaluating an object, default behaviour is to search cache for including or begin objects
# but this could be expensive
dig_hard_into_cache = True


def capply(climaf_operator, *operands, **parameters):
    """
    Builds the object representing applying a CliMAF operator (script, function or macro) by calling the dedicated
    function.
    :param climaf_operator: a CliMAF operator (either a declared script, macro or operator)
    :param operands: operands to be passed to the climaf operator
    :param parameters: parameters to be passed to the climaf operator (not available for macros)
    :return: a list of CliMAF objects (stored if auto-store is on)
    """
    res = None
    if operands is None or operands[0] is None and not classes.allow_errors_on_ds_call:
        raise Climaf_Driver_Error("Operands is None for operator %s" % climaf_operator)
    opds = list(map(str, operands))
    if climaf_operator in cscripts:
        # clogger.debug("applying script %s to"%climaf_operator + `opds` + `parameters`)
        res = capply_script(climaf_operator, *operands, **parameters)
        # Evaluate object right now if there is no output to manage
        op = cscripts[climaf_operator]
        if op.outputFormat in none_formats:
            ceval(res, userflags=copy.copy(op.flags))
    elif climaf_operator in cmacros:
        if len(parameters) > 0:
            raise Climaf_Driver_Error("Macros cannot be called with keyword args")
        clogger.debug("applying macro %s to" % climaf_operator + repr(opds))
        res = instantiate(cmacros[climaf_operator], *operands)
    elif climaf_operator in operators:
        clogger.debug("applying operator %s to" % climaf_operator + repr(opds) + repr(parameters))
        res = capply_operator(climaf_operator, *operands, **parameters)
    else:
        clogger.error("%s is not a known operator nor script" % climaf_operator)
    return res


def capply_operator(climaf_operator, *operands, **parameters):
    """
    Create object for application of an internal OPERATOR to OPERANDS with keywords PARAMETERS.
    TODO: To be implemented
    """
    clogger.error("Not yet developped - TBD")
    raise NotImplementedError("Could not yet apply an operator.")
    return None


def capply_script(script_name, *operands, **parameters):
    """
    Create object for application of a script to OPERANDS with keyword PARAMETERS.
    :param script_name: name of the script to be applied
    :param operands: operands to be passed to the script
    :param parameters: parameters to be passed to the script
    :return: an object that represents the application of the script
    """
    if script_name not in cscripts:
        raise Climaf_Driver_Error("Script %s is not know. Consider declaring it with function 'cscript'", script_name)
    script = cscripts[script_name]
    # if len(operands) != script.inputs_number() :
    #     raise Climaf_Driver_Error("Operator %s is "
    #                               "declared with %d input streams, while you provided %d. Get doc with 'help(%s)'"%(
    #             script_name,script.inputs_number(),len(operands), script_name ))
    #
    # Check that all parameters to the call are expected by the script
    command = script.command
    for para in parameters:
        if not(r"{%s}" % para in command) and not(r"{%s_iso}" % para in command) and para != 'member_label' \
                and not para.startswith("add_"):
                    raise Climaf_Driver_Error("parameter '%s' is not expected by script %s (which command is : %s)" %
                                              (para, script_name, command))
    #
    # Check that only first operand can be an ensemble
    opscopy = list(operands)
    first = opscopy[0]
    if len(opscopy) > 1:
        opscopy = opscopy[1:]
    else:
        opscopy = list()
    if True in [isinstance(op, classes.cens) for op in opscopy]:
        raise Climaf_Driver_Error("Cannot yet have an ensemble as operand except as first one")
    #
    # If first operand is an ensemble, and the script is not ensemble-capable,
    # result is the ensemble of applying the script ot each member of first operand
    # Otherwise, just call maketree
    if isinstance(first, classes.cens) and script.flags.commuteWithEnsemble:
        # Must iterate on members
        reps = []
        order = first.order
        for label in order:
            member = first[label]
            clogger.debug("processing member %s : " % label + repr(member))
            params = parameters.copy()
            params["member_label"] = label
            reps.append(maketree(script_name, script, member, *opscopy, **params))
        return classes.cens(dict(list(zip(order, reps))), order)
    else:
        return maketree(script_name, script, *operands, **parameters)


def maketree(script_name, script, *operands, **parameters):
    # maketree takes care of
    #  - creating a ctree object representing the application of the scripts to its operands
    #  - checking that the time period of result makes sense
    #  - computing the variable name for all outputs, using dict script.outputs
    #  - for each secondary outputs, creating an attribute of the ctree named as this output
    add_dict = dict()
    for p in [p for p in parameters if p.startswith("add_")]:
        add_dict[p] = parameters.pop(p)
    if "add_variable" in add_dict:
        defaultVariable = add_dict["add_variable"]
        parameters["add_variable"] = defaultVariable
    else:
        defaultVariable = classes.varOf(operands[0])
    rep = classes.ctree(script_name, script, *operands, **parameters)
    # TBD Analyze script inputs cardinality vs actual arguments
    # Create one child for each output
    # defaultPeriod=operands[0].period
    for outname in script.outputs:
        if outname is None or outname == '':
            # This is the main output
            if "%s" in script.outputs['']:
                rep.variable = script.outputs[''] % defaultVariable
            else:
                rep.variable = script.outputs['']
            template = Template(rep.variable)
            rep.variable = template.substitute(parameters)
        else:
            # This is a secondary output
            son = classes.scriptChild(rep, outname)
            if "%s" in script.outputs[outname]:
                son.variable = script.outputs[outname] % defaultVariable
            else:
                son.variable = script.outputs[outname]
            template = Template(son.variable)
            son.variable = template.substitute(parameters)
            rep.outputs[outname] = son
            setattr(rep, outname, son)
    # Check that time period of output makes sense
    p = timePeriod(rep)
    #
    return rep


def capply_operator(climaf_operator, *operands, **parameters):
    """
    Create object for application of an internal OPERATOR to OPERANDS with keywords PARAMETERS.

    """
    clogger.error("Not yet developped - TBD")
    return None


def ceval_for_cdataset(cobject, userflags=None, format="MaskedArray", deep=None, derived_list=list(),
                       recurse_list=list()):
    """
    Evaluate a CliMAF object of kind climaf.classes.cdataset
    :param cobject:
    :param userflags:
    :param format:
    :param deep:
    :param derived_list:
    :param recurse_list:
    :return:
    """
    recurse_list.append(cobject.crs)
    clogger.debug("Evaluating dataset operand " + cobject.crs + "having kvp=" + repr(cobject.kvp))
    ds = cobject
    cache_value = cache.hasExactObject(ds)
    if cache_value is not None:
        clogger.debug("Dataset %s exists in cache" % ds)
        cdedent()
        return cache_value
    if ds.isLocal() or ds.isCached():
        clogger.debug("Dataset %s is local or cached " % ds)
        #  if the data is local, then
        #   if the caller operator can select the data and aggregate time, and requested format is
        #     'file' return the filenames
        #   else : read the data, create a cache file for that, and recurse
        #
        # First go to derived variable evaluation if applicable
        if is_derived_variable(ds.variable, ds.project):
            if ds.variable in derived_list:
                raise Climaf_Driver_Error("Loop detected while evaluating"
                                          "derived variable " + ds.variable + " " + repr(derived_list))
            # Create the object representing applying the operation needed to derive the var
            # and return it
            derived = derive_variable(ds)
            clogger.debug("evaluating derived variable %s as %s" % (ds.variable, repr(derived)))
            derived_value = ceval(derived, format=format, deep=deep,
                                  userflags=userflags,
                                  derived_list=derived_list + [ds.variable],
                                  recurse_list=recurse_list)
            if derived_value:
                clogger.debug("succeeded in evaluating derived variable %s as %s" % (ds.variable, repr(derived)))
                set_variable(derived_value, ds.variable, format=format)
            cdedent()
            return derived_value
        elif noselect(userflags, ds, format):
            # The caller is assumed to be able to select the needed sub-period or variable
            # and to select the variable
            clogger.debug("Delivering file set or sets is OK for the target use")
            cdedent()
            rep = ds.baseFiles()
            if not rep:
                raise Climaf_Driver_Error("No file found for %s" % repr(ds))
            return rep  # a single string with all filenames,
            # or a list of such strings in case of ensembles
        else:
            clogger.debug("Must subset and/or aggregate and/or select " +
                          "var from data files and/or get data, or provide object result")
            if format == 'file' or format == "MaskedArray":
                if ds.hasOneMember():
                    clogger.debug("Fetching/selection/aggregation is done using an external script for now - TBD")
                    extract = capply('select', ds)
                else:
                    clogger.debug("On multi-member datafiles , fetching/selection/aggregation " +
                                  "is done using select_member - TBD")
                    extract = capply('select_member', ds)
                if extract is None:
                    raise Climaf_Driver_Error("Cannot access dataset" + repr(ds))
                rep = ceval(extract, userflags=userflags, format=format)
            else:
                raise Climaf_Driver_Error("Untractable output format %s" % format)
            userflags.unset_selectors()
            cdedent()
            return rep
    else:
        # Non-local and non-cached dataset
        #   if the user can access the dataset by one of the dataset-specific protocols
        #   then assume it can also select on time; -> just provide it with the address
        #   else : fetch the relevant selection of the data, and store it in cache
        clogger.debug("Dataset is remote ")
        if userflags.canOpendap and format == 'file':
            clogger.debug("But user can OpenDAP ")
            cdedent()
            return ds.adressOf()
        else:
            if noselect(userflags, ds, format):
                # ce cas-ci n'a jamais été activé !
                clogger.debug("Delivering file set or sets is OK for the target use")
                cdedent()
                rep = ds.baseFiles()
                if not rep:
                    raise Climaf_Driver_Error("No file found for %s" % repr(ds))
                return rep
            else:
                # This matches reaching data using e.g. ftp
                clogger.debug("Must remote read and cache ")
                rep = ceval(capply('remote_select', ds), userflags=userflags, format=format)
                ds.files = rep
                userflags.unset_selectors()
                cdedent()
                return rep


def ceval_for_ctree(cobject, userflags=None, format="MaskedArray", deep=None, derived_list=list(),
                    recurse_list=list()):
    """

    :param cobject:
    :param userflags:
    :param format:
    :param deep:
    :param derived_list:
    :param recurse_list:
    :return:
    """
    recurse_list.append(cobject.crs)
    clogger.debug("Evaluating compound object : " + repr(cobject))
    #################################################################
    if deep is not None:
        cache.cdrop(cobject.crs)
    #
    clogger.debug("Searching cache for exact object : " + repr(cobject))
    #################################################################
    filename = cache.hasExactObject(cobject)
    # filename=None
    if filename:
        clogger.info("Object found in cache: %s is at %s:  " % (cobject.crs, filename))
        cdedent()
        if format == 'file':
            return filename
        else:
            return cread(filename, classes.varOf(cobject))
    if dig_hard_into_cache:
        clogger.debug("Searching cache for including object for : " + repr(cobject))
        ########################################################################
        it, altperiod = cache.hasIncludingObject(cobject)
        # clogger.debug("Finished with searching cache for including object for : " + `cobject`)
        # it=None
        if it:
            clogger.info("Including object found in cache : %s" % it.crs)
            if format == 'file':
                clogger.info("Selecting " + repr(cobject) + " out of it")
                # Just select (if necessary for the user) the portion relevant to the request
                rep = ceval_select(it, cobject, userflags, format, deep, derived_list, recurse_list)
                cdedent()
                return rep
            else:
                clogger.debug("Because out format %s is not (yet, TBD) supported by ceval_select, cannot use "
                              "including object found for : " % format + repr(cobject))
            #
        clogger.debug("Searching cache for begin  object for : " + repr(cobject))
        ########################################################################
        it, comp_period = cache.hasBeginObject(cobject)
        clogger.debug("Finished with searching cache for begin  object for : " + repr(cobject))
        # it=None
        if it:
            clogger.info("partial result found in cache for %s : %s" % (cobject.crs, it.crs))
            clogger.debug("comp_period=" + repr(comp_period))
            begcrs = it.crs
            # Build complement object for end, and eval it
            comp = copy.deepcopy(it)
            comp.setperiod(comp_period)
            evalcomp = ceval(comp, userflags, format, deep, derived_list, recurse_list)
            set_variable(evalcomp, cobject.variable, format=format)
            rep = cache.complement(begcrs, comp.crs, cobject.crs)
            cdedent()
            if format == 'file':
                return rep
            else:
                return ceval(cobject)
        #
    clogger.info("nothing relevant found in cache for %s" % cobject.crs)
    #
    #  Only deep=True can propagate downward !
    if deep:
        down_deep= True
    else :
        down_deep= None
    #
    # the cache doesn't have a similar tree, let us recursively eval subtrees
    ##########################################################################
    # TBD  : analyze if the dataset is remote and the remote place 'offers' the operator
    if cobject.operator in cscripts:
        clogger.debug("Script %s found" % cobject.operator)
        file = ceval_script(cobject, down_deep,
                            recurse_list=recurse_list)  # Does return a filename, or list of filenames
        cdedent()
        if format == 'file':
            return file
        else:
            return cread(file, classes.varOf(cobject))
    elif cobject.operator in operators:
        clogger.debug("Operator %s found" % cobject.operator)
        # TODO: Implement ceval_operator
        obj = ceval_operator(cobject, deep)
        cdedent()
        if format == 'file':
            # TODO: Implement cstore
            rep = cstore(obj)
            return rep
        else:
            return obj
    else:
        raise Climaf_Driver_Error("operator %s is not a script nor known operator %s" % str(cobject.operator))


def ceval_for_scriptChild(cobject, userflags=None, format="MaskedArray", deep=None, derived_list=list(),
                          recurse_list=list()):
    """

    :param cobject:
    :param userflags:
    :param format:
    :param deep:
    :param derived_list:
    :param recurse_list:
    :return:
    """
    recurse_list.append(cobject.crs)
    clogger.debug("Evaluating compound object : " + repr(cobject))
    #################################################################
    if deep is not None:
        cache.cdrop(cobject.crs)
    #
    clogger.debug("Searching cache for exact object : " + repr(cobject))
    #################################################################
    filename = cache.hasExactObject(cobject)
    # filename=None
    if filename:
        clogger.info("Object found in cache: %s is at %s:  " % (cobject.crs, filename))
        cdedent()
        if format == 'file':
            return filename
        else:
            return cread(filename, classes.varOf(cobject))
    if dig_hard_into_cache:
        clogger.debug("Searching cache for including object for : " + repr(cobject))
        ########################################################################
        it, altperiod = cache.hasIncludingObject(cobject)
        # clogger.debug("Finished with searching cache for including object for : " + `cobject`)
        # it=None
        if it:
            clogger.info("Including object found in cache : %s" % it.crs)
            if format == 'file':
                clogger.info("Selecting " + repr(cobject) + " out of it")
                # Just select (if necessary for the user) the portion relevant to the request
                rep = ceval_select(it, cobject, userflags, format, deep, derived_list, recurse_list)
                cdedent()
                return rep
            else:
                clogger.debug("Because out format %s is not (yet, TBD) supported by ceval_select, cannot use "
                              "including object found for : " % format + repr(cobject))
            #
        clogger.debug("Searching cache for begin  object for : " + repr(cobject))
        ########################################################################
        it, comp_period = cache.hasBeginObject(cobject)
        clogger.debug("Finished with searching cache for begin  object for : " + repr(cobject))
        # it=None
        if it:
            clogger.info("partial result found in cache for %s : %s" % (cobject.crs, it.crs))
            clogger.debug("comp_period=" + repr(comp_period))
            begcrs = it.crs
            # Build complement object for end, and eval it
            comp = copy.deepcopy(it)
            comp.setperiod(comp_period)
            evalcomp = ceval(comp, userflags, format, deep, derived_list, recurse_list)
            set_variable(evalcomp, cobject.variable, format=format)
            rep = cache.complement(begcrs, comp.crs, cobject.crs)
            cdedent()
            if format == 'file':
                return rep
            else:
                return ceval(cobject)
        #
    clogger.info("nothing relevant found in cache for %s" % cobject.crs)
    #
    #  Only deep=True can propagate downward !
    if deep :
        down_deep= True
    else :
        down_deep= None
    # Force evaluation of 'father' script
    if ceval_script(cobject.father, down_deep, recurse_list=recurse_list) is not None:
        # Re-evaluate, which should succeed using cache
        rep = ceval(cobject, userflags, format, None, recurse_list=recurse_list)
        cdedent()
        return rep
    else:
        raise Climaf_Driver_Error("generating script aborted for " + cobject.father.crs)


def ceval_for_cpage(cobject, userflags=None, format="MaskedArray", deep=None, derived_list=list(),
                    recurse_list=list()):
    """

    :param cobject:
    :param userflags:
    :param format:
    :param deep:
    :param derived_list:
    :param recurse_list:
    :return:
    """
    recurse_list.append(cobject.crs)
    clogger.debug("Evaluating compound object : " + repr(cobject))
    #################################################################
    if deep is not None:
        cache.cdrop(cobject.crs)
    #
    clogger.debug("Searching cache for exact object : " + repr(cobject))
    #################################################################
    filename = cache.hasExactObject(cobject)
    # filename=None
    if filename:
        clogger.info("Object found in cache: %s is at %s:  " % (cobject.crs, filename))
        cdedent()
        if format == 'file':
            return filename
        else:
            return cread(filename, classes.varOf(cobject))
    #
    #  Only deep=True can propagate downward !
    if deep:
        down_deep= True
    else :
        down_deep= None
    file = cfilePage(cobject, down_deep, recurse_list=recurse_list)
    cdedent()
    if format == 'file':
        return file
    else:
        return cread(file)  # !! Does it make sense ?


def ceval_for_cpage_pdf(cobject, userflags=None, format="MaskedArray", deep=None, derived_list=list(),
                        recurse_list=list()):
    """

    :param cobject:
    :param userflags:
    :param format:
    :param deep:
    :param derived_list:
    :param recurse_list:
    :return:
    """
    recurse_list.append(cobject.crs)
    clogger.debug("Evaluating compound object : " + repr(cobject))
    #################################################################
    if deep is not None:
        cache.cdrop(cobject.crs)
    #
    clogger.debug("Searching cache for exact object : " + repr(cobject))
    #################################################################
    filename = cache.hasExactObject(cobject)
    # filename=None
    if filename:
        clogger.info("Object found in cache: %s is at %s:  " % (cobject.crs, filename))
        cdedent()
        if format == 'file':
            return filename
        else:
            return cread(filename, classes.varOf(cobject))
    #
    #  Only deep=True can propagate downward !
    if deep:
        down_deep= True
    else :
        down_deep= None
    #
    file = cfilePage_pdf(cobject, down_deep, recurse_list=recurse_list)
    cdedent()
    if format == 'file':
        return file
    else:
        return cread(file)  # !! Does it make sense ?


def ceval_for_cens(cobject, userflags=None, format="MaskedArray", deep=None, derived_list=list(),
                   recurse_list=list()):
    """

    :param cobject:
    :param userflags:
    :param format:
    :param deep:
    :param derived_list:
    :param recurse_list:
    :return:
    """
    recurse_list.append(cobject.crs)
    clogger.debug("Evaluating compound object : " + repr(cobject))
    #################################################################
    if deep is not None:
        cache.cdrop(cobject.crs)
    #
    clogger.debug("Searching cache for exact object : " + repr(cobject))
    #################################################################
    filename = cache.hasExactObject(cobject)
    # filename=None
    if filename:
        clogger.info("Object found in cache: %s is at %s:  " % (cobject.crs, filename))
        cdedent()
        if format == 'file':
            return filename
        else:
            return cread(filename, classes.varOf(cobject))
    d = dict()
    for member in cobject.order:
        # print ("evaluating member %s"%member)
        d[member] = ceval(cobject[member], copy.copy(userflags), format, deep, recurse_list=recurse_list)
    cdedent()
    if format == "file":
        return reduce(lambda x, y: x + " " + y, [d[m] for m in cobject.order])
    else:
        return d


def ceval_for_string(cobject, userflags=None, format="MaskedArray", deep=None, derived_list=list(),
                     recurse_list=list()):
    """
    Evaluate a CliMAF object of kind string.
    TODO: Implement this function
    :param cobject:
    :param userflags:
    :param format:
    :param deep:
    :param derived_list:
    :param recurse_list:
    :return:
    """
    clogger.debug("Evaluating object from crs : %s" % cobject)
    raise NotImplementedError("Evaluation from CRS is not yet implemented ( %s )" % cobject)


def ceval(cobject, userflags=None, format="MaskedArray",
          deep=None, derived_list=[], recurse_list=[]):
    """
    Actually evaluates a CliMAF object, either as an in-memory data structure or
    as a string of filenames (which either represent a superset or exactly includes
    the desired data)

    - with arg deep=True , re-evaluates all components
    - with arg deep=False, re-evaluates top level operation
    - without arg deep   , use cached values as far as possible

    arg derived_list is the list of variables that have been considered as 'derived'
    (i.e. not natives) in upstream evaluations. It avoids to loop endlessly
    """
    if format not in ["MaskedArray", "file", "txt"]:
        raise Climaf_Driver_Error("Allowed formats yet are : 'object', 'nc', 'txt', %s" % ', '.join(
            [repr(x) for x in graphic_formats]))
    #
    if userflags is None:
        userflags = scriptFlags()
    #
    # Next check is too crude for dealing with use of operator 'select'
    # if cobject.crs in recurse_list :
    #    clogger.critical("INTERNAL ERROR : infinite loop on object: "+cobject.crs)
    #    return None
    cindent()
    if isinstance(cobject, classes.cdataset):
        return ceval_for_cdataset(cobject=cobject, userflags=userflags, format=format, deep=deep,
                                  derived_list=derived_list, recurse_list=recurse_list)
    #
    elif isinstance(cobject, classes.ctree):
        return ceval_for_ctree(cobject=cobject, userflags=userflags, format=format, deep=deep,
                               derived_list=derived_list, recurse_list=recurse_list)
    elif isinstance(cobject, classes.scriptChild):
        return ceval_for_scriptChild(cobject=cobject, userflags=userflags, format=format, deep=deep,
                                     derived_list=derived_list, recurse_list=recurse_list)
    elif isinstance(cobject, classes.cpage):
        return ceval_for_cpage(cobject=cobject, userflags=userflags, format=format, deep=deep,
                               derived_list=derived_list, recurse_list=recurse_list)
    elif isinstance(cobject, classes.cpage_pdf):
        return ceval_for_cpage_pdf(cobject=cobject, userflags=userflags, format=format, deep=deep,
                                   derived_list=derived_list, recurse_list=recurse_list)
    elif isinstance(cobject, classes.cens):
        return ceval_for_cens(cobject=cobject, userflags=userflags, format=format, deep=deep,
                              derived_list=derived_list, recurse_list=recurse_list)
    elif isinstance(cobject, str):
        return ceval_for_string(cobject=cobject, userflags=userflags, format=format, deep=deep,
                                derived_list=derived_list, recurse_list=recurse_list)
    else:
        raise Climaf_Driver_Error("argument " + repr(cobject) + " is not (yet) managed")


def ceval_script(scriptCall, deep, recurse_list=[]):
    """ Actually applies a CliMAF-declared script on a script_call object

    Prepare operands as fiels and build command from operands and parameters list
    Assumes that scripts are described in dictionary 'scripts'  by templates as
    documented in operators.cscript

    Returns a CLiMAF cache data filename
    """
    script = cscripts[scriptCall.operator]
    template = Template(script.command)
    # Evaluate input data
    invalues = []
    sizes = []
    for op in scriptCall.operands:
        if op:
            if scriptCall.operator != 'remote_select' and \
                    isinstance(op, classes.cdataset) and \
                    not (op.isLocal() or op.isCached()):
                inValue = ceval(op, format='file', deep=deep)
            else:
                inValue = ceval(op, userflags=scriptCall.flags, format='file', deep=deep,
                                recurse_list=recurse_list)
            clogger.debug("evaluating %s operand %s as %s" % (scriptCall.operator, op, inValue))
            if inValue is None or inValue is "":
                raise Climaf_Driver_Error("When evaluating %s : value for %s is None" % (scriptCall.script, repr(op)))
            if isinstance(inValue, list):
                size = len(inValue)
            else:
                size = 1
        else:
            inValue = ''
            size = 0
        sizes.append(size)
        invalues.append(inValue)
    # print("len(invalues)=%d"%len(invalues))
    #
    # Replace input data placeholders with filenames
    subdict = dict()
    opscrs = ""
    if 0 in script.inputs:
        label, multiple, serie = script.inputs[0]
        op = scriptCall.operands[0]
        # print("processing 0, op=%s"%`op`)
        infile = invalues[0]
        if (scriptCall.operator != 'remote_select') and \
                not all(map(os.path.exists, infile.split(" "))):
            raise Climaf_Driver_Error("Internal error : for script %s and 1st operand %s, some input file does not exist among %s:" % \
                                      (scriptCall.operator,op,infile))
        subdict[label] = infile
        # if scriptCall.flags.canSelectVar :
        subdict["var"] = classes.varOf(op)
        subdict["Var"] = classes.varOf(op)
        if isinstance(op, classes.cdataset) and op.alias:
            filevar, scale, offset, units, filenameVar, missing, conditions = op.alias
            if op.matches_conditions(conditions):
                if scriptCall.flags.canAlias and "," not in classes.varOf(op):
                    # if script=="select" and ((classes.varOf(op) != filevar) or scale != 1.0 or offset != 0.) :
                    subdict["var"] = Template(filevar).safe_substitute(op.kvp)
                    subdict["alias"] = "%s,%s,%.4g,%.4g" % (classes.varOf(op), subdict["var"], scale, offset)
                if units:
                    subdict["units"] = units
                if scriptCall.flags.canMissing and missing:
                    subdict["missing"] = missing
        if isinstance(op, classes.cens):
            if not multiple:
                raise Climaf_Driver_Error(
                    "Script %s 's input #%s cannot accept ensemble %s" % (scriptCall.script, 0, repr(op)))
            # subdict["labels"]=r'"'+reduce(lambda x,y : "'"+x+"' '"+y+"'", op.labels)+r'"'
            subdict["labels"] = reduce(lambda x, y: x + "$" + y, op.order)
        if op:
            per = timePeriod(op)
            if per and not per.fx and str(per) != "" and scriptCall.flags.canSelectTime:
                subdict["period"] = str(per)
                subdict["period_iso"] = per.iso()
        if scriptCall.flags.canSelectDomain:
            subdict["domain"] = classes.domainOf(op)
    else:
        subdict["var"] = classes.varOf(scriptCall)
        subdict["Var"] = classes.varOf(scriptCall)
    i = 0
    for op in scriptCall.operands:
        if op:
            opscrs += op.crs + " - "
        # print("processing %s, i=%d"%(`op`,i))
        infile = invalues[i]
        if (scriptCall.operator != 'remote_select') and infile is not '' and \
                not all(map(os.path.exists, infile.split(" "))):
            raise Climaf_Driver_Error("Internal error : some input file does not exist among %s:" % infile)
        i += 1
        if i > 1 or 1 in script.inputs:
            label, multiple, serie = script.inputs[i]
            subdict[label] = infile
            # Provide the name of the variable in input file if script allows for
            if isinstance(op, classes.cobject):
                subdict["var_%d" % i] = classes.varOf(op)
            if isinstance(op, classes.cdataset) and op.alias:
                filevar, scale, offset, units, filenameVar, missing, conditions = op.alias
                if op.matches_conditions(conditions):
                    if ((classes.varOf(op) != filevar) or (scale != 1.0) or (offset != 0.)) and \
                            "," not in classes.varOf(op):
                        subdict["var_%d" % i] = Template(filevar).safe_substitute(op.kvp)
                        subdict["alias_%d" % i] = "%s %s %f %f" % (classes.varOf(op),
                                                                   subdict["var_%d" % i], scale, offset)
                    if units:
                        subdict["units_%d" % i] = units
                    if missing:
                        subdict["missing_%d" % i] = missing
            # Provide period selection if script allows for
            if op:
                per = timePeriod(op)
                if not per.fx and per != "":
                    subdict["period_%d" % i] = str(per)
                    subdict["period_iso_%d" % i] = per.iso()
            subdict["domain_%d" % i] = classes.domainOf(op)
    clogger.debug("subdict for operands is " + repr(subdict))
    # substitution is deffered after scriptcall parameters evaluation, which may
    # redefine e.g period
    #
    # Provide one cache filename for each output and instantiates the command accordingly
    if script.outputFormat not in none_formats:
        if script.outputFormat == "graph":
            if 'format' in scriptCall.parameters:
                if scriptCall.parameters['format'] in graphic_formats:
                    output_fmt = scriptCall.parameters['format']
                else:
                    raise Climaf_Driver_Error('Allowed graphic formats yet are : %s' % ', '.join(
                        [repr(x) for x in graphic_formats]))
            else:  # default graphic format
                output_fmt = "png"
        else:
            output_fmt = script.outputFormat
        # Compute a filename for each ouptut
        # Un-named main output
        # main_output_filename=tempfile.NamedTemporaryFile(suffix="."+output_fmt).name
        # #cache.generateUniqueFileName(scriptCall.crs, format=output_fmt)
        tmpfile, tmpfile_fmt = os.path.splitext(cache.generateUniqueFileName(scriptCall.crs, format=output_fmt))
        main_output_filename = "%s_%i%s" % (tmpfile, os.getpid(), tmpfile_fmt)

        subdict["out"] = main_output_filename
        subdict["out_" + classes.varOf(scriptCall)] = main_output_filename

        subdict["out_final"] = cache.generateUniqueFileName(scriptCall.crs, format=output_fmt)
        subdict["out_final_" + classes.varOf(scriptCall)] = cache.generateUniqueFileName(scriptCall.crs,
                                                                                         format=output_fmt)

        # Named outputs
        for output in scriptCall.outputs:
            # subdict["out_"+output]=tempfile.NamedTemporaryFile(suffix="."+output_fmt).name
            tmpfile, tmpfile_fmt = os.path.splitext(
                cache.generateUniqueFileName(scriptCall.crs + "." + output, format=output_fmt))
            subdict["out_" + output] = "%s_%i%s" % (tmpfile, os.getpid(), tmpfile_fmt)
            subdict["out_final_" + output] = cache.generateUniqueFileName(scriptCall.crs + "." + output,
                                                                          format=output_fmt)

    # Account for script call parameters
    for p in scriptCall.parameters:
        # clogger.debug("processing parameter %s=%s"%(p,scriptCall.parameters[p]))
        subdict[p] = scriptCall.parameters[p]
        if p == "period":
            subdict["period_iso"] = init_period(scriptCall.parameters[p]).iso()
    subdict["crs"] = opscrs.replace("'", "")
    #
    # Discard selection parameters if selection already occurred for first operand
    # TBD : manage the cases where other operands didn't undergo selection
    if cache.hasExactObject(scriptCall.operands[0]) :
        # for key in ["period","period_iso","var","domain","missing","alias","units"]:
        for key in ["period", "period_iso", "var", "domain", "missing", "alias"]:
            if key in subdict :
                subdict.pop(key)
    #
    # print("subdict="+`subdict`)
    # Combine CRS and possibly member_label to provide/complement title
    if 'title' not in subdict:
        if 'member_label' in subdict:
            subdict["title"] = subdict['member_label']
    #        else:
    #            subdict["title"]=subdict["crs"]
    else:
        # print("Got a member label : %s"%subdict['member_label'])
        if 'member_label' in subdict:
            subdict["title"] = subdict["title"] + " " + subdict['member_label']
            subdict.pop('member_label')
    #
    # Substitute all args
    template = template.safe_substitute(subdict)
    #
    # Allowing for some formal parameters to be missing in the actual call:
    #
    # Discard remaining substrings looking like :
    #  some_word='"${some_keyword}"' , or simply : '"${some_keyword}"'
    template = re.sub(r'(\w*=)?(\'\")?\$\{\w*\}(\"\')?', r"", template)
    #
    # Discard remaining substrings looking like :
    #  some_word=${some_keyword}  or  simply : ${some_keyword}
    template = re.sub(r"(\w*=)?\$\{\w*\}", r"", template)
    #
    # Link the fixed fields needed by the script/operator
    if script.fixedfields is not None:
        # subdict_ff=dict()
        subdict_ff = scriptCall.parameters.copy()
        subdict_ff["model"] = classes.modelOf(scriptCall.operands[0])
        subdict_ff["simulation"] = classes.simulationOf(scriptCall.operands[0])
        subdict_ff["project"] = classes.projectOf(scriptCall.operands[0])
        subdict_ff["realm"] = classes.realmOf(scriptCall.operands[0])
        subdict_ff["grid"] = classes.gridOf(scriptCall.operands[0])
        scr_fixed_fields = script.fixedfields  # return paths: (linkname, targetname)
        files_exist = dict()
        for ll, lt in scr_fixed_fields:
            # Replace input data placeholders with filenames for fixed fields
            template_ff_target = Template(lt).substitute(subdict_ff)
            # symlink if needed
            files_exist[ll] = False
            if os.path.islink(ll):
                if os.path.realpath(ll) != template_ff_target:
                    os.remove(ll)
                    os.symlink(template_ff_target, ll)
            elif os.path.isfile(ll):
                files_exist[ll] = True
            else:
                os.symlink(template_ff_target, ll)
    #
    tim1 = time.time()
    clogger.info("Launching command:" + template)
    #
    with open(logdir + '/last.out', 'w') as logfile:
        logfile.write("\n\nstdout and stderr of script call :\n\t " + template + "\n\n")
        try:
            subprocess.check_call(template, stdout=logfile, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError:
            raise Climaf_Driver_Error("Something went wrong when computing %s. See file ./last.out for details" %
                                      scriptCall.crs)

    #
    # For remote files, we supply ds.local_copies_of_remote_files
    # for local filenames in order to can use ds.check()
    if scriptCall.operator == 'remote_select':
        local_filename = []
        for el in scriptCall.operands[0].baseFiles().split(" "):
            local_filename.append(climaf.dataloc.remote_to_local_filename(el))
        scriptCall.operands[0].local_copies_of_remote_files = ' '.join(local_filename)
    #
    # Clean fixed fields symbolic links (linkname, targetname)
    if script.fixedfields:
        for ll, lt in script.fixedfields:
            if not files_exist[ll]:
                os.system("rm -f " + ll)
    # Handle outputs
    if script.outputFormat in ["txt", ]:
        with open(logdir + "/last.out", 'r') as f:
            for line in f.readlines():
                sys.stdout.write(line)
    if script.outputFormat in none_formats:
        return None
    # Tagging output files with their CliMAF Reference Syntax definition
    # 1 - Un-named main output
    ok = cache.register(main_output_filename, scriptCall.crs, subdict["out_final"])
    # 2 - Named outputs
    for output in scriptCall.outputs:
        ok = ok and cache.register(subdict["out_" + output], scriptCall.crs + "." + output,
                                   subdict["out_final_" + output])
    if ok:
        duration = time.time() - tim1
        # print(...file=sys.stderr)
        clogger.info("Done in %.1f s with script computation for "
                     "%s (command was :%s )" % (duration, repr(scriptCall), template))
        return subdict["out_final"]  # main_output_filename
    else:
        raise Climaf_Driver_Error("Some output missing when executing "
                                  ": %s. \n See %s/last.out" % (template, logdir))


def timePeriod(cobject):
    """ Returns a time period for a CliMAF object : if object is a dataset, returns
    its time period, otherwise returns time period of first operand
    """
    if isinstance(cobject, classes.cdataset):
        return cobject.period
    elif isinstance(cobject, classes.ctree):
        clogger.debug("timePeriod : processing %s,operands=%s" % (cobject.script, repr(cobject.operands)))
        if cobject.script.flags.doCatTime and len(cobject.operands) > 1:
            clogger.debug("Building composite period for results of %s" % cobject.operator)
            periods = [timePeriod(op) for op in cobject.operands]
            merged_period = merge_periods(periods)
            if len(merged_period) > 1:
                raise Climaf_Driver_Error("Issue when time assembling with %s, periods are not consecutive : %s" %
                                          (cobject.operator, merged_period))
            return merged_period[0]
        else:
            clogger.debug("timePeriod logic for script is 'choose 1st operand' %s" % cobject.script)
            return timePeriod(cobject.operands[0])
    elif isinstance(cobject, classes.scriptChild):
        clogger.debug("for now, timePeriod logic for scriptChilds is basic - TBD")
        return timePeriod(cobject.father)
    elif isinstance(cobject, classes.cens):
        clogger.debug("for now, timePeriod logic for 'cens' objet is basic (1st member)- TBD")
        return timePeriod(list(cobject.values())[0])
    else:
        return None  # clogger.error("unkown class for argument "+`cobject`)


def ceval_select(includer, included, userflags, format, deep, derived_list, recurse_list):
    """ Extract object INCLUDED from (existing) object INCLUDER,
    taking into account the capability of the user process (USERFLAGS)
    and the required delivering FORMAT(file or object)
    """
    if format == 'file':
        if userflags.canSelectTime or userflags.canSelectDomain:
            clogger.debug("TBD - should do smthg smart when user can select time or domain")
            # includer.setperiod(included.period)
        incperiod = timePeriod(included)
        clogger.debug("extract sub period %s out of %s" % (repr(incperiod), includer.crs))
        clogger.debug("Variable considered in includer: %s" % includer.variable)
        clogger.debug("Variable considered in included: %s" % included.variable)
        extract = capply('select', includer, period=repr(incperiod))
        clogger.debug("Variable considered in extract: %s" % extract.variable)
        clogger.debug("Extract crs found: %s" % extract)
        objfile = ceval(extract, userflags, 'file', deep, derived_list, recurse_list)
        if objfile:
            crs = includer.buildcrs(period=incperiod)
            return cache.rename(objfile, crs)
        else:
            clogger.critical("Cannot evaluate " + repr(extract))
            exit()
    else:
        clogger.error("Can yet process only files - TBD")


def cread(datafile, varname=None, period=None):
    import re
    if not datafile:
        return None
    if re.findall(".png$", datafile) or \
            ((re.findall(".pdf$", datafile) or re.findall(".eps$", datafile)) and (not xdg_bin)):
        subprocess.Popen(["display", datafile, "&"])
    elif (re.findall(".pdf$", datafile) or re.findall(".eps$", datafile)) and xdg_bin:
        subprocess.Popen(["xdg-open", datafile])
    elif re.findall(".nc$", datafile):
        clogger.debug("reading NetCDF file %s" % datafile)
        if varname is None:
            varname = varOfFile(datafile)
        if varname is None:
            raise Climaf_Driver_Error("")
        if period is not None:
            clogger.warning("Cannot yet select on period (%s) using CMa for files %s - TBD" % (period, files))
        from .anynetcdf import ncf
        fileobj = ncf(datafile)
        # Note taken from the CDOpy developper : .data is not backwards
        # compatible to old scipy versions, [:] is
        data = fileobj.variables[varname][:]
        import numpy.ma
        if '_FillValue' in dir(fileobj.variables[varname]):
            fillv = fileobj.variables[varname]._FillValue
            rep = numpy.ma.array(data, mask=data == fillv)
        else:
            rep = numpy.ma.array(data)
        fileobj.close()
        return rep
    else:
        clogger.error("cannot yet handle %s" % datafile)
        return None


def cview(datafile):
    if re.findall(".png$", datafile) or \
            ((re.findall(".pdf$", datafile) or re.findall(".eps$", datafile)) and (not xdg_bin)):
        subprocess.Popen(["display", datafile, "&"])
    elif (re.findall(".pdf$", datafile) or re.findall(".eps$", datafile)) and xdg_bin:
        subprocess.Popen(["xdg-open", datafile])
    else:
        clogger.error("cannot yet handle %s" % datafile)
        return None


def derive_variable(ds):
    """ Assuming that variable of DS is a derived variable, returns the CliMAF object
    representing the operation needed to compute it (using information in dict
    operators_derive.derived_variable
    """
    if not isinstance(ds, classes.cdataset):
        raise Climaf_Driver_Error("arg is not a dataset")
    if not is_derived_variable(ds.variable, ds.project):
        raise Climaf_Driver_Error("%s is not a derived variable" % ds.variable)
    op, outname, inVarNames, params = derived_variable(ds.variable, ds.project)
    inVars = []
    first=True
    for varname in inVarNames:
        dic = copy.deepcopy(ds.kvp)
        dic['variable'] = varname
        # If the dataset has a version attribute, it should be inherited only
        # by the first input variable, an be set to "latest" for the next ones
        # (it would be tricky to do something smarter TBD)
        if not first and "version" in dic :
            dic['version'] = "latest"
        first=False
        inVars.append(classes.cdataset(**dic))
    params["add_variable"] = ds.variable
    # TODO: force the output variable to be well defined
    father = capply(op, *inVars, **params)
    clogger.debug("Father object is: %s" % repr(father))
    if outname == "out" or outname == ds.variable:
        rep = father
    else:
        rep = classes.scriptChild(father, outname)
    clogger.debug("DEBUG variable>>> %s" % rep.variable)
    # TODO: check the type of the outputs
    rep.variable = ds.variable
    clogger.debug("DEBUG variable>>> %s" % rep.variable)
    return rep


def set_variable(obj, varname, format):
    """ Change to VARNAME the variable name for OBJ, which FORMAT
    maybe 'file' or 'MaskedArray'.
    Also set the variable long_name using CF convention (TBD)
    """
    if obj is None:
        return None
    long_name = CFlongname(varname)
    if format == 'file':
        oldvarname = varOfFile(obj)
        if not oldvarname:
            raise Climaf_Driver_Error("Cannot set variable name for a multi-variable dataset: %s " % oldvarname)
        if oldvarname != varname:
            command = "ncrename -v %s,%s %s >/dev/null 2>&1" % (oldvarname, varname, obj)
            if os.system(command) != 0:
                clogger.error("Issue with changing varname to %s in %s" % (varname, obj))
                return None
            clogger.debug("Varname changed to %s in %s" % (varname, obj))
            command = "ncatted -a long_name,%s,o,c,%s %s" % (varname, long_name, obj)
            if os.system(command) != 0:
                clogger.error("Issue with changing long_name for var %s in %s" %
                              (varname, obj))
                return None
            return True
    elif format == 'MaskedArray':
        clogger.warning('TBD - Cannot yet set the varname for MaskedArray')
    else:
        clogger.error('Cannot handle format %s' % format)


def noselect(userflags, ds, format):
    """ Check the capability of the user process (USERFLAGS)
    and a set of attribute values of dataset (DS)

    Return True if the user can select the data and aggregate time,
    and requested FORMAT is 'file', and False otherwise
    """

    can_select = False

    if ((userflags.canSelectVar or ds.oneVarPerFile()) and
            (userflags.canSelectTime or ds.periodIsFine()) and
            (userflags.canSelectDomain or ds.domainIsFine()) and
            (userflags.canAggregateTime or ds.periodHasOneFile()) and
            (userflags.canAlias or ds.hasExactVariable()) and
            (userflags.canMissing or ds.missingIsOK()) and
            (ds.hasOneMember()) and
            (format == 'file')):
        can_select = True

    return can_select


# Commodity functions
#########################

def cfile(object, target=None, ln=None, hard=None, deep=None):
    """
    Provide the filename for a CliMAF object, or copy this file to target. Launch computation if needed.

    Args:

      object (CliMAF object) : either a dataset or a 'compound' object (e.g. the result of a CliMAF operator)

      target (str, optional) : name of the destination file in case you really need another
       filename; CliMAF will then anyway also store the result in its cache,  either as a copy
       (default), or a sym- or a hard-link (see below);

      ln (logical, optional) : if True, CliMAF cache file is created as a symlink to the target;
       this allows to cross filesystem boundaries, while still saving disk space (wrt to a copy);
       CliMAF will manage the broken link cases (at the expense of a new computation)

      hard (logical, optional) : if True, CliMAF cache file is created as a hard link to the target;
       this allows to save disk space, but does not allow to cross filesystem boundaries

      deep (logical, optional) : governs the use of cached values when computing the object:

        - if missing, or None : use cache as much as possible (speed up the computation)

        - False : make a shallow computation, i.e. do not use cached values for the
          top level operation

        - True  : make a deep computation, i.e. do not use any cached value

    Returns:

       - if target is provided, returns this filename (or linkname) if computation is
         successful ('target' contains the result), and None otherwise;

       - if target is not provided, returns the filename in CliMAF cache, which contains
         the result (and None if failure)


    """
    clogger.debug("cfile called on " + str(object))
    start_time = datetime.now()
    clogger.debug("Starting cfile at: " + start_time.strftime("%Y-%m-%d %H:%M:%S"))
    #
    # -- Evaluate the CliMAF object
    result = ceval(object, format='file', deep=deep)
    #
    end_time = datetime.now()
    duration = end_time - start_time
    clogger.debug("cfile completed at: " + end_time.strftime("%Y-%m-%d %H:%M:%S") + " : total duration = " +
                  str(duration.total_seconds()) + ' seconds')
    if target is None:
        return result
    else:
        target = os.path.abspath(os.path.expanduser(target))
        target_dir = os.path.dirname(target)
        if isinstance(object, climaf.classes.cens):
            raise Climaf_Driver_Error("Cannot yet copy or link result files for an ensemble")
        if result is not None:
            if ln or hard:
                if ln and hard:
                    Climaf_Driver_Error("flags ln and hard are mutually exclusive")
                elif ln:
                    if os.path.exists(target):
                        if not os.path.samefile(result, target):
                            os.remove(target)
                            shutil.move(result, target)
                            os.symlink(target, result)
                    else:
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                        shutil.move(result, target)
                        os.symlink(target, result)
                else:
                    # Must create hard link
                    # If result is a link, follow links for finding source of hard link
                    if os.path.islink(result):
                        source = os.readlink(result)
                    else:
                        source = result
                    if source == target:
                        # This is a case where the file had already been symlinked to the same target name
                        shutil.move(source, result)
                        os.link(result, target)
                    else:
                        if os.path.exists(target):
                            os.remove(target)
                        os.link(source, target)
            else:
                if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                shutil.copyfile(result, target)
        if not os.path.exists(target):
            raise Climaf_Driver_Error("Issue during the creation of the target file %s" % target)
        else:
            return target


def cshow(obj):
    """
    Provide the in-memory value of a CliMAF object.
    For a figure object, this will lead to display it
    ( launch computation if needed. )
    """
    clogger.debug("cshow called on " + str(obj))
    return climaf.driver.ceval(obj, format='MaskedArray')


def cMA(obj, deep=None):
    """
    Provide the Masked Array value for a CliMAF object. Launch computation if needed.

    Args:
      obj (CliMAF object) : either a datset or a 'compound' object (like the result of a CliMAF standard operator)
      deep (logical, optional) : governs the use of cached values when computing the object

        - if missing, or None : use cache as much as possible
        - False : make a shallow computation, i.e. do not use cached values for top level operation
        - True  : make a deep computation, i.e. do not use any cached value

    Returns:
      a Masked Array containing the object's value

    """
    clogger.debug("cMA called with arguments" + str(obj))
    return climaf.driver.ceval(obj, format='MaskedArray', deep=deep)


def cvalue(obj, index=0,deep=None):
    """
    Return the value of the array for an object, after MV flattening, at a given index

    Example:

     >>> data=ds(project='mine',variable='tas', ...)
     >>> data1=time_average(data)
     >>> data2=space_average(data1)
     >>> v=cvalue(data2)

    Does use the file representation of the object
    """
    return cMA(obj,deep=deep).data.flat[index]


def cexport(*args, **kwargs):
    """ Alias for climaf.driver.ceval. Create synonyms for arg 'format'

    """
    clogger.debug("cexport called with arguments" + str(args))
    if "format" in kwargs:
        if (kwargs['format'] == "NetCDF" or kwargs['format'] == "netcdf" or kwargs['format'] == "nc"
                or kwargs['format'] == "png" or kwargs['format'] == "pdf" or kwargs['format'] == "eps"):
            kwargs['format'] = "file"
        if kwargs['format'] == "MA":
            kwargs['format'] = "MaskedArray"
    return climaf.driver.ceval(*args, **kwargs)


def cimport(cobject, crs):
    clogger.debug("cimport called with argument", cobject)
    clogger.debug("should check syntax of arg 'crs' -TBD")
    clogger.warning("cimport is not for the dummies - Playing at your own risks !")
    import numpy
    import numpy.ma
    if isinstance(cobject, numpy.ma.MaskedArray):
        clogger.debug("for now, use a file for importing - should revisit - TBD")
        clogger.error("not yet implemented fro Masked Arrays - TBD")
    elif isinstance(cobject, string_types):
        cache.register(cobject, crs)
    else:
        clogger.error("argument is not a Masked Array nor a filename", cobject)


def get_fig_sizes(figfile):
    args_figsize = ["identify", figfile]
    # On some sites, getoutput first lines have warning messages
    # Furthermore, in case of missing file, last line could be an error -> only consider lines beginning with figfile
    output_figsize = getoutput(" ".join(args_figsize)).split("\n")
    output_figsize = [l for l in output_figsize if l.startswith(figfile)][-1]
    # comm_figsize = subprocess.Popen(args_figsize, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # output_figsize = comm_figsize.stdout.read()
    figsize = str(output_figsize).split(" ").pop(2)
    (fig_width, fig_height) = figsize.split("x")
    return int(fig_width), int(fig_height)


def cfilePage(cobj, deep, recurse_list=None):
    """
    Builds a page with CliMAF figures, computing associated crs

    Args:
     cobj (cpage object)

    Returns : the filename in CliMAF cache, which contains the result (and None if failure)

    """
    if not isinstance(cobj, classes.cpage):
        raise Climaf_Driver_Error("cobj is not a cpage object")
    clogger.debug("Computing figure array for cpage %s" % cobj.crs)
    #
    # page size and creation
    page_size = "%dx%d" % (cobj.page_width, cobj.page_height)
    args = ["convert", "-size", page_size, "xc:white"]
    #
    # margins
    x_left_margin = 30.  # Left shift at start and end of line
    y_top_margin = 30.  # Initial vertical shift for first line
    x_right_margin = 30.  # Right shift at start and end of line
    y_bot_margin = 30.  # Vertical shift for last line
    xmargin = 30.  # Horizontal shift between figures
    ymargin = 30.  # Vertical shift between figures
    #
    usable_height = cobj.page_height - ymargin * (len(cobj.heights) - 1.) - y_top_margin - y_bot_margin
    if cobj.title is not "":
        usable_height -= cobj.ybox
    if cobj.insert is not "":
        ins_base_width, ins_base_height = get_fig_sizes(cobj.insert)
        insert_height = int((float(ins_base_height) * cobj.insert_width) / float(ins_base_width))
        usable_height -= insert_height
    #
    usable_width = cobj.page_width - xmargin * (len(cobj.widths) - 1.) - x_left_margin - x_right_margin
    #
    # page composition
    y = y_top_margin
    for line, rheight in zip(cobj.fig_lines, cobj.heights):
        # Line height in pixels
        height = usable_height * rheight
        x = x_left_margin
        max_old = 0.
        for fig, rwidth in zip(line, cobj.widths):
            # Figure width in pixels
            width = usable_width * rwidth
            scaling = "%dx%d+%d+%d" % (width, height, x, y)
            if fig:
                figfile = ceval(fig, format="file", deep=deep, recurse_list=recurse_list)
            else:
                figfile = 'xc:None'
            clogger.debug("Compositing figure %s", fig.crs if fig else 'None')

            args.extend([figfile, "-geometry", scaling, "-composite"])

            # Real size of figure in pixels: [fig_width x fig_height]
            try:
                fig_width, fig_height = get_fig_sizes(figfile)
            except:
                raise Climaf_Driver_Error("Issue with figure "+str(fig))
            # Scaling and max height
            if float(fig_width) != 1. and float(fig_height) != 1.:
                if ((float(fig_width) / float(fig_height)) * float(height)) < width:
                    new_fig_width = (float(fig_width) / float(fig_height)) * float(height)
                    new_fig_height = height
                else:
                    new_fig_height = (float(fig_height) / float(fig_width)) * float(width)
                    new_fig_width = width
            else:  # for figure = 'None'
                new_fig_height = fig_height
                new_fig_width = fig_width

            max_fig_height = max(float(new_fig_height), max_old)
            max_old = float(new_fig_height)

            if False and cobj.fig_trim and (float(fig_width) / float(fig_height) < width / height):
                width_adj = float(fig_width) * (height / float(fig_height))
                x += width_adj + xmargin
            else:
                x += width + xmargin

        if cobj.fig_trim and (float(fig_width) / float(fig_height) > width / height):
            height_adj = max_fig_height
            y += height_adj + ymargin
        else:
            y += height + ymargin

    if cobj.insert != "":
        args.extend([cobj.insert, "-geometry", "x%d+%d+%d" %
                     (insert_height, (cobj.page_width - cobj.insert_width) / 2, y), "-composite"])

    out_fig = cache.generateUniqueFileName(cobj.crs, format=cobj.format)
    if cobj.page_trim:
        args.append("-trim")
    if cobj.title != "":
        splice = "0x%d" % cobj.ybox
        annotate = "+%d+%d" % (cobj.x, cobj.y)
        args.extend(["-gravity", cobj.gravity, "-background", cobj.background, "-splice", splice, "-font", cobj.font,
                     "-pointsize", "%d" % cobj.pt, "-annotate", annotate, '"%s"' % cobj.title])

    args.append(out_fig)
    clogger.debug("Compositing figures : %s" % repr(args))

    try:
        with open("tmp.err", "w") as fic:
            out = subprocess.check_output(" ".join(args), shell=True, stderr=fic)
    except subprocess.CalledProcessError:
        with open("tmp.err") as fic:
            err = fic.read()
        raise Climaf_Driver_Error("Compositing failed : %s" % err)
    finally:
        os.remove("tmp.err")

    if cache.register(out_fig, cobj.crs):
        clogger.debug("Registering file %s for cpage %s" % (out_fig, cobj.crs))
        return out_fig


def cfilePage_pdf(cobj, deep, recurse_list=None):
    """
    Builds a PDF page with CliMAF figures using pdfjam, computing associated crs

    Args:
     cobj (cpage_pdf object)

    Returns : the filename in CliMAF cache, which contains the result (and None if failure)

    """
    if not isinstance(cobj, classes.cpage_pdf):
        raise Climaf_Driver_Error("cobj is not a cpage_pdf object")
    clogger.debug("Computing figure array for cpage %s" % cobj.crs)
    #
    # margins
    xmargin = 30.  # Horizontal shift between figures
    ymargin = 30.  # Vertical shift between figures
    #
    # page size and creation
    page_size = '"{%dpx,%dpx}"' % (cobj.page_width, cobj.page_height)
    fig_nb = '"%dx%d"' % (len(cobj.fig_lines[0]), len(cobj.fig_lines))
    fig_delta = '"%d %d"' % (xmargin, ymargin)
    preamb = '"\\pagestyle{empty} \\usepackage{hyperref} \\usepackage{graphicx} \\usepackage{geometry} ' \
             '\\geometry{vmargin=%dcm,hmargin=2cm}"' % cobj.y

    args = ["pdfjam", "--keepinfo", "--preamble", preamb, "--papersize", page_size, "--delta", fig_delta, "--nup",
            fig_nb]  # "%s"%preamb
    #
    # page composition
    for line in cobj.fig_lines:
        for fig in line:
            if fig:
                figfile = ceval(fig, format="file", deep=deep, recurse_list=recurse_list)
                clogger.debug("Compositing figure %s", fig.crs)
            else:
                raise Climaf_Driver_Error("Each figure must exist ('None' figure is not accepted)")
            args.extend([figfile])
    #
    # more optional options
    if cobj.openright is True:
        args.extend(["--openright", "True"])

    if cobj.scale != 1.:
        args.extend(["--scale", "%.2f" % cobj.scale])

    if cobj.title != "":
        if "\\" in cobj.pt:
            pt = cobj.pt.split("\\")[-1]
        else:
            pt = cobj.pt

        if cobj.titlebox:
            latex_command = r'"\begin{center} \hspace{%dcm} \setlength{\fboxrule}{0.5pt} ' \
                            r'\setlength{\fboxsep}{2mm} \fcolorbox{black}{%s}{\%s{\fontfamily{%s}\selectfont %s}}'\
                            r' \end{center}"' % (cobj.x, cobj.background, pt, cobj.font, cobj.title)
        else:
            latex_command = r'"\begin{center} \hspace{%dcm} \%s{\fontfamily{%s}\selectfont %s} \end{center}"' \
                            % (cobj.x, pt, cobj.font, cobj.title)
        args.extend(["--pagecommand", latex_command])

    #
    # launch process and registering output in cache
    out_fig = cache.generateUniqueFileName(cobj.crs, format='pdf')

    args.extend(["--outfile", out_fig])

    clogger.debug("Compositing figures : %s" % repr(args))
    try:
        with open("tmp.err", "w") as fic:
            out = subprocess.check_output(" ".join(args), shell=True, stderr=fic)
    except subprocess.CalledProcessError:
        with open("tmp.err") as fic:
            err = fic.read()
        raise Climaf_Driver_Error("Compositing failed : %s" % err)
    finally:
        os.remove("tmp.err")

    if cache.register(out_fig, cobj.crs):
        clogger.debug("Registering file %s for cpage %s" % (out_fig, cobj.crs))
    return out_fig


def calias(project, variable, fileVariable=None, **kwargs):
    """
    See :py:func:`climaf.classes.calias`

    Declare that in ``project``, ``variable`` is to be computed by
    reading ``filevariable``;
    It allows to use a list of variables, given as a string where
    the name of variables are separated by commas
    """
    if "," not in variable:  # mono-variable
        classes.calias(project=project, variable=variable, fileVariable=fileVariable, **kwargs)

    else:  # multi-variable
        classes.calias(project=project, variable=variable, fileVariable=fileVariable, **kwargs)
        list_variable = variable.split(",")

        for v in list_variable:
            derive(project, v, 'ccdo', variable, operator='selname,%s' % v)
            classes.calias(project=project, variable=v, fileVariable=None, **kwargs)


def CFlongname(varname):
    """ Returns long_name of variable VARNAME after CF convention
    """
    return "TBD_should_improve_function_climaf.driver.CFlongname"


def efile(obj, filename, force=False):
    """
    Create a single file for an ensemble of CliMAF objects (launch computation if needed).

    This is a convenience function. Such files are not handled in CliMAF cache

    Args:

        obj (CliMAF object) : an ensemble of CliMAF objects ('cens' objet)

        filename (str) : output filename. It will include a field for each
         ensemble's member, with a variable name suffixed by the member
         label (e.g. : tas_CNRM-CM, tas_IPSL-CM... ) (more formally :
         'var(obj.order[n])'_'obj.ens[order[n]]')

        force (logical, optional) : if True, CliMAF will overwrite the file
         'filename' if it already exists

    """
    if isinstance(obj, classes.cens):

        if os.path.isfile(filename):
            if force:
                os.system("rm -rf %s" % filename)
                clogger.warning("File '%s' already existed and has been overwritten" % filename)
            else:
                raise Climaf_Driver_Error("File '%s' already exists: use 'force=True' to overwrite it" % filename)

        for lab in obj.order:
            memb = obj[lab]
            ffile = cfile(memb)

            f = tempfile.NamedTemporaryFile(suffix=".nc")
            command = "ncrename -O -v %s,%s_%s %s %s" % (classes.varOf(memb), classes.varOf(memb), lab, ffile, f.name)
            if os.system(command) != 0:
                raise Climaf_Driver_Error("ncrename failed : %s" % command)

            command2 = "ncks -A %s %s" % (f.name, filename)
            if os.system(command2) != 0:
                raise Climaf_Driver_Error(
                    "Issue when merging %s and %s (using command: %s)" % (f.name, filename, command2))
            f.close()

    else:
        clogger.warning("objet is not a 'cens' objet")


class Climaf_Driver_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        cdedent(100)

    def __str__(self):
        return repr(self.valeur)
