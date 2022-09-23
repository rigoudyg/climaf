#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Optimize searching datasets files when some facets are 
shell-like wildcards (i.e. include * or ?)

For now limited to project CMIP6 and active only if
env.environment.optimize_cmip6_wildcards is True (which is the
default) . See doc for
:py:func:`~climaf.projects.optimize.cmip6_optimize_wildcards`

"""

from __future__ import print_function, division, unicode_literals, absolute_import

import glob
import json
import hashlib
import time
import os
import re
from collections import defaultdict

from env.clogging import clogger
from env.environment import cprojects
import env

dirnames = defaultdict(lambda: defaultdict(list))


def wild(c):
    return "?" in c or "*" in c


def cmip6_optimize_wildcards(kwargs):
    """Allow to optimize CMIP6 data search by analyzing CMIP6 keyword
    values in KWARGS, and replacing some patterns using * or ?
    by the list of their possible values, by querying the file system

    It is automatically activated and used when
    ``env.environment.optimize_cmip6_wildcards`` is True.

    It assumes that all CMIP6 data are organized using CMIP6 canonical
    DRS with a pattern like :
    `${root}/CMIP6/${mip}/${institute}/${model}/${experiment}/${realization}/${table}/`
    
    It uses tables which are built automatically, stored in CLiMAF
    cache, and can be refreshed by clearing it. See
    :py:func:`~climaf.projects.optimize.clear_tables`
    
    First principle is to focus on facets which are high in the DRS
    hierarchy, and so in the directories hierarchy. For such facets,
    in order to speed-up search when the facet value includes a
    wildcard, and when another facet allows to reduce significantly
    the number of values of the wildcard facet, we build a look-up
    table.
    
    This is for instance the case in CMIP6 when facet 'mip' is * and
    facet 'experiment' is known. Or when 'institute' is * and 'model'
    is known.
    
    Next principle is to the build a list of valid paths segment after
    segment, by testing which wildcard segments values among the
    possible ones actually lead to an existing path. For some cases,
    when there is no way to guess a limited list of values (as
    e.g. for 'version'), glob.glob is used

    Keyword PERIOD is not processed at that level.

    Returns a list of non-wildcard KWARGS which match actually
    existing leaf directories, and which is used in later search (see
    :py:func:`~climaf.dataloc.selectFiles`)

    """
    
    if not env.environment.optimize_cmip6_wildcards:
        return [kwargs.copy()]
    else:
        #
        root = os.sep.join([kwargs["root"], "CMIP6"])
        broot = root.encode('utf-8')
        root_tag = hashlib.sha1(broot).hexdigest()[0:8]
        #
        mip = kwargs.get('mip')
        experiment = kwargs.get('experiment')
        institute = kwargs.get('institute')
        model = kwargs.get('model')
        realization = kwargs.get('realization')
        table = kwargs.get('table')
        variable = kwargs.get('variable')
        grid = kwargs.get('grid')
        version = kwargs.get('version')

        # Mip
        ##########
        if wild(mip):
            if wild(experiment):
                raise ValueError("When requesting optimization, must provide at least mip or experiment")
            mip = possible_values("CMIP6", "experiment2mip", root, experiment, mip)[0]
            clogger.debug("Based on experiment = %s, attribute mip is set to %s" % (experiment, mip))
        #
        # Institute
        ################
        institutes = possible_values("CMIP6", "model2institute", root, model, institute)
        paths = list()
        for inst in institutes:
            paths.extend(listdirs(os.sep.join([root, mip]), inst, test_exists=wild(model)))

        # Model
        #############
        new_paths = list()
        for path in paths:
            institute = cmip6_facets(path, root, 2)[0]
            models = possible_values("CMIP6", "mip_institute_experiment2model", root,
                                     "_".join([mip, institute, experiment]), model)
            for amodel in models:
                new_paths.extend(listdirs(path, amodel, test_exists=wild(experiment)))
        paths = new_paths

        # experiment
        ################
        new_paths = list()
        for path in paths:
            model = cmip6_facets(path, root, 3)[0]
            experiments = possible_values("CMIP6", "mip_model2experiment", root, "_".join([mip, model]), experiment)
            for exp in experiments:
                new_paths.extend(listdirs(path, exp))
        paths = new_paths

        # realization
        ################
        new_paths = list()
        for path in paths:
            model, experiment = cmip6_facets(path, root, 3, 4)
            realizations = possible_values("CMIP6", "mip_model_experiment2realization",
                                           root, "_".join([mip, model, experiment]), realization)
            for real in realizations:
                new_paths.extend(listdirs(path, real))
        paths = new_paths

        # Table
        ###########
        new_paths = list()
        tables = [table, ]
        if wild(table):
            # TBD: build a list of possible tables based on variable name
            ###############################################################
            raise ValueError("For the time being, must provide table name")

            tables = ['3hr', '6hrLev', '6hrPlev', '6hrPlevPt', 'AERday', 'AERhr', 'AERmon', 'AERmonZ', 'Amon', 'CF3hr',
                      'CFday', 'CFmon', 'CFsubhr', 'day', 'E1hr', 'E3hr', 'Eday', 'EdayZ', 'Efx', 'Emon', 'EmonZ', 'fx',
                      'LImon', 'Lmon', 'Oday', 'Ofx', 'Omon', 'SIday', 'SImon']
            # clogger.debug("Attribute table = %s can have value only among %s"%tables)
        #
        for path in paths:
            for table in tables:
                new_paths.extend(listdirs(path, table))
        paths = new_paths

        # Variable
        ###########
        new_paths = list()
        for path in paths:
            variables = [variable, ]
            #     # TBD : build a list of possible variables based on table name
            #     ###############################################################
            #     raise ValueError("For the time being, must provide variable name")
            #     #clogger.debug("Attribute variable = %s can have value only among %s"%variables)
            for var in variables:
                new_paths.extend(listdirs(path, variable))
        paths = new_paths

        # Grid
        ###########
        new_paths = list()
        for path in paths:
            model, table, variable = cmip6_facets(path, root, 3, 6, 7)
            grids = possible_values("CMIP6", "model_table_variable2grid", root, "_".join([model, table, variable]),
                                    grid)
            if len(grids) == 0:
                # grids = ["gr", "gn", "gr1", "gr2"]
                grids = [grid, ]  # This better matches user's request
                clogger.info("Attribute grid has no registered set of values for %s / %s / %s" %
                             (model, variable, table))
            for gr in grids:
                new_paths.extend(listdirs(path, gr))
        paths = new_paths

        # Version : no try at registering version per model+experiment+real+table+variable+grid
        # -> use glob() to find version
        # And also : at that final stage, test that directories exist
        ################################
        new_paths = list()
        clogger.info('cmip6_optimize: before ensuring paths exists, there are %d paths' % len(paths))
        clogger.debug('Paths: %s', paths)
        for path in paths:
            new_paths.extend(listdirs(path, version, test_exists=True))
        paths = new_paths
        clogger.info('cmip6_optimize: after ensuring paths exists, there are %d paths' % len(paths))
        clogger.debug('Paths: %s', paths)

        dicts = list()
        for path in paths:
            d = cmip6_path2dict(path, root)
            d['project'] = kwargs['project']
            d['period'] = kwargs['period']
            d['root'] = kwargs['root']
            dicts.append(d)

        clogger.debug("There are %d optimized paths for data directories" % len(dicts))
        return dicts


def cmip6_path2dict(path, root):
    """Returns a dict of facet/value pairs derived from PATH after
    removing prefix ROOT and assuming that the path matches CMIP6
    DRS"""
    path = path[len(root)+1:].split(os.sep)
    rep = {key: pos for (pos, key) in enumerate(["mip", "institute", "model", "experiment", "realization", "table",
                                                "variable", "grid", "version"])}
    for k in rep:
        rep[k] = path[rep[k]]
    return rep
    

def cmip6_facets(path, root, *fields):
    """Returns a tuple of facets values for the ranks in FIELDS, derived
    from PATH after removing prefix ROOT and assuming that the path
    matches CMIP6 DRS, at least up to the max depth in FIELDS

    Example :
    >>> institute, model, experiment, realization, table, variable = cmip6_facets(path, root, 2, 3, 4, 5, 6, 7)

    """
    rep = list()
    path = path[len(root)+1:].split(os.sep)
    for field in fields:
        rep.append(path[field-1])
    return tuple(rep)


def listdirs(parent, pattern, test_exists=False):
    """List directories which may actually exists, by complementing path
    PARENT with a single level of sub-directories, which match PATTERN

    If the pattern includes no wildcard, simply complement with
    PATTERN, and test existence only if TEST_EXITS is True

    Otherwise, use glob.glob to find existing sub-directories

    """
    # clogger.debug('listdirs with %s and %s'%(parent,pattern))

    if not wild(pattern):
        path = os.sep.join([parent, pattern])
        if not test_exists or os.path.exists(path):
            return [path, ]
        else:
            return list()
    else:
        # Is it cost-effective to test that a path exists before
        # globing on (some of) its subdirs?  According to various
        # tests, it is not
        rep = glob.glob(os.sep.join([parent, pattern]))
        return rep

    
def cmip6_optimize_check_paths(paths):

    """Check that paths patterns in PATHS fit (at least some of) the
    requirements for optimizing data search
    """
    start = os.sep.join(["${root}", "CMIP6"])
    test = [not path.startswith(start) for path in paths]
    if any(test):
        for path in [paths[i] for (i, t) in enumerate(test) if t]:
            clogger.debug("Path %s does not fit requirements for optimization" % path)
        return False
    else:
        return True


def dirnames_for_one_case(case_name, glob_pattern, split_index, case_value,
                          key_index=-1, reset=False, value_pattern=None, root=None):

    """Returns the ensemble of directories which have files matching a
    given GLOB_PATTERN, which is supposed to end with a "/*" which
    corresponds to CASE_VALUE. The directory names are extracted from
    glob() return at a hierarchy level indicated by SPLIT_INDEX;
    
    Method : Uses an entry CASE_NAME in a global lookup table 
    Try to read it from file if not present.
    If it fails builds (stores, and writes) it by globbing according to the pattern
    
    If arg RESET is True, performs the globbing anyway and re-write the table
    on disk

    See examples of use in :py:func:`~climaf.projects.cmip6.cmip6_optimize_wildcards`

    """
    global dirnames
    # print("begin:",dirnames)
    
    filen = _build_filename(case_name)
    should_write = False
    #
    if reset: 
        dirnames.pop(case_name, None)
    elif case_name not in dirnames:
        # Try to load table from file
        try:
            with open(filen, "r") as f:
                dirnames[case_name] = json.load(f)
                clogger.debug("Table %s read" % filen)
        except:
            clogger.debug("Table %s not found" % filen)
    #
    if case_name not in dirnames:
        should_write = True
        # Build table by globbing
        clogger.warning("Building table %s by globbing. "
                        "\n\tThis may take a while but will be saved for further sessions. "
                        "\n\tTable will be stored in the cache as %s" % (case_name, filen))
        values = set()
        t = time.time()
        cases = glob.glob(root + glob_pattern)
        clogger.warning("Globbing duration was %g" % (time.time() - t))
        clogger.info("Globbing duration was %g for %s and returned %d enties" %
                     ((time.time() - t), glob_pattern, len(cases)))
        for case in cases:
            if not isinstance(key_index, list):
                key = case.split(os.sep)[key_index]
            else:
                key = ""
                for k in key_index:
                    key += "%s_" % (case.split(os.sep)[k])
            value = case.split(os.sep)[split_index]
            dirnames[case_name][key].append(value)
            clogger.debug('Adding value %s to entry %s of case %s ' % (value, key, case_name))
        for v in dirnames[case_name]:
            dirnames[case_name][v] = list(set(dirnames[case_name][v]))
    #
    if should_write:
        with open(filen, "w") as f:
            json.dump(dirnames[case_name], f, separators=(',', ': '), indent=3, ensure_ascii=True)
        
    #
    if not wild(case_value):
        # clogger.debug('Looking for entry %s in table %s'%(case_value,case_name))
        try:
            ret = dirnames[case_name][case_value]
        except:
            clogger.debug('No  %s in %s' % (case_value, case_name))
            ret = list()
    else:
        ret = list()
        pat = case_value.replace("?", ".").replace("*", ".*")
        for case in dirnames[case_name]:
            if re.search(pat, case):
                ret.extend(dirnames[case_name][case])
        ret = list(set(ret))

    if value_pattern not in [None, "*"]:
        rep = list()
        pat = value_pattern.replace("?", ".").replace("*", ".*")
        for r in ret:
            if re.search(pat, r):
                rep.append(r)
        ret = rep
    return ret
        

def clear_tables(pattern=None):
    """Clear all search optimization tabes that include a given pattern
    (e.g. 'CMIP6'), or all tables if no pattern is given

    In order to identify the pattern for a given table :

    - tables are stored in your CliMAF cache (which name is displayed
      at the beginning of your session)

    - table names are self explanatory;
      e.g. 'CMIP6_mip_experiment_model2realization_7367d567.json'
      stands for the table which allows to derive the list of
      realizations from the values of mip, experiment and model. The
      last part is a hash code for the root directory of the CMIP6 data

    """
    global dirnames
    for case_name in dirnames:
        if pattern is None or pattern in case_name:
            dirnames.pop(case_name)
            os.remove(_build_filename(case_name))


def _build_filename(case_name):
    return os.sep.join([env.environment.currentCache, case_name]) + ".json"


def possible_values(project, tag, root, key, value_pattern):
    """For a given PROJECT, returns the list of possible values for a
    facet (here called the value facet) given the value (KEY) of
    another facet (here called the key facet). Returns only values
    that match VALUE_PATTERN. Return [] if None found

    If VALUE_PATTERN has no wildcard, just return it as result (in a list)

    Values are searched based on additional information TAG, which
    carries two pieces of information : which is facet which value
    (KEY) is provided, and which is the facet which values are
    searched

    Current implementation is based on globing and uses TAG to derive
    three items :

    - pattern to use for globing the filesystem
    - index of the value facet in the file hierarchy matching the pattern
    - index (or indices) of the key facet(s) in the file hierarchy 
      matching the pattern

    It then calls function dirnames_for_one_case which implements the
    globbing, and which caches its results in a json file.

    """
    if not wild(value_pattern):
        return [value_pattern, ]
    else:
        #
        params = {
            "CMIP6": {
                # First entries, actually used
                "experiment2mip": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*", "*"]),
                    "split_index": -4,
                    "key_index": -1
                },
                "model2institute": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*"]),
                    "split_index": -2,
                    "key_index": -1
                },
                "mip_institute_experiment2model": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*", "*"]),
                    "split_index": -2,
                    "key_index": [-4, -3, -1]
                },
                "mip_model2experiment": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*", "*"]),
                    "split_index": -1,
                    "key_index": [-4, -2]
                },
                "mip_model_experiment2realization": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*", "*", "*"]),
                    "split_index": -1,
                    "key_index": [-5, -3, -2]
                },
                "model_table_variable2grid": {
                    "glob_pattern": os.sep.join(["", "CMIP", "*", "*", "historical", "r1i*", "*", "*", "*"]),
                    "split_index": -1,
                    "key_index": [-6, -3, -2]
                },
                # Next entries are no more used
                "mip_institute2model": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*"]),
                    "split_index": -1,
                    "key_index": [-3, -2]
                },
                "mip_experiment2model": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*", "*"]),
                    "split_index": -2,
                    "key_index": [-4, -1]
                },
                "mip2experiment": {
                    "glob_pattern": os.sep.join(["", "*", "*", "*", "*"]),
                    "split_index": -1,
                    "key_index": -4
                },
            }
        }
        broot = root.encode('utf-8')
        root_tag = hashlib.sha1(broot).hexdigest()[0:8]
        case_name = "_".join([project, tag, root_tag])
        #
        if tag in params[project]:
            paras = params[project][tag]
        else:
            paras = [params[project][a_tag] for a_tag in params[project] if a_tag in tag]
            if len(paras) > 0:
                paras = paras[0]
            else:
                paras = None
        if paras is None:
            raise ValueError("Unknown case %s" % tag)
        #
        ret = dirnames_for_one_case(case_name=case_name, case_value=key, value_pattern=value_pattern, root=root,
                                    **paras)
        clogger.debug('According to table %s , %s and %s lead to possible values %s' % (tag, key, value_pattern, ret))
        return ret

