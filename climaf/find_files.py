#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Find files that match patterns which include facet keywords and period handling.

"""

# Created :       S.Senesi - 2014
# Re-engineered : S.Senesi - 2021

from __future__ import print_function, division, unicode_literals, absolute_import

import os
import six
import os.path
import re
import glob
from string import Template
import ftplib as ftp
import getpass
import netrc
import copy
import time

from env.environment import *
from env.clogging import clogger
import env
from climaf.utils import Climaf_Error, Climaf_Classes_Error, cartesian_product_substitute
from climaf.period import init_period, sort_periods_list, cperiod, build_date_regexp_pattern
from climaf.netcdfbasics import fileHasVar, timeLimits
from climaf.projects.intake_search import intake_find

#: Regular expression for matching periods and catching their components
date_regexp_pattern = build_date_regexp_pattern()


def selectGenericFiles(urls, kwargs, return_combinations=None, use_frequency=False,
                       return_wildcards=None, merge_periods_on=None):
    """
    Allow to describe a ``generic`` file organization : the list of files returned
    by this function is composed of files which :

     - match the patterns in ``url`` once these patterns are instantiated by
        the values in kwargs, and

     - contain the ``variable`` provided in kwargs

     - match the `period`` provided in kwargs

    kwargs can have entries which are list, and are then interpreted as :

    - a first element which is a pattern (i.e. which include * or ?)

    - more elements which are the possible values, as diagnosed by some logic upstream

    In the pattern strings, no keyword is mandatory. However, for remote files,
    filename pattern must include ${varname}, which is instanciated by variable
    name or ``filenameVar`` (given via :py:func:`~climaf.classes.calias()`); this is
    for the sake of efficiency (please complain if inadequate)

    Example :

    >>> selectGenericFiles(project ='my_projet',model ='my_model', simulation ='lastexp', variable ='tas',
    ...                    period ='1980', urls =['~/DATA/${project}/${model}/*${variable}*${PERIOD}*.nc)']

    /home/stephane/DATA/my_project/my_model/somefilewith_tas_Y1980.nc

    In the pattern strings, the keywords that can be used in addition to the argument
    names (e.g. ${model}) are:

    - ${variable} : use it if the files are split by variable and
        filenames do include the variable name, as this speed up the search

    - ${PERIOD} : use it for indicating the period covered by each file, if this
        is applicable in the file naming; this period can appear in filenames as
        YYYY, YYYYMM, YYYYMMDD, YYYYMMDDHHMM, either once only, or twice with
        separator ='-' or '_'

    - wildcards '?' and '*' for matching respectively one and any number of characters


    Résumé en francais :

    - On construit une expression régulière pour matcher les périodes

    - On boucle sur les patterns de la liste url :

        - Instancier le pattern par les valeurs des facettes fournies, et par  ".*" pour $PERIOD

        - on fait glob.glob

        - on affine : on ne retient que les valeurs qui matchent avec la regexp de périodes (sous
          réserve que le pattern contienne $PERIOD) si on n'a rien, on essaie aussi
          avec filenameVar; d'où une liste de fichiers lfiles

        - on cherche a connaitre les valeurs rencontrées pour chaque facette : on construit
          une expression régulière (avec groupes) qui capture les valeurs de facettes
          (y/c PERIOD) et une autre pour capturer la date seulement (est-ce bien encore
          nécessaire ???)

        - Boucle sur les fichiers de lfiles:

            - si le pattern n'indique pas qu'on peut extraire la date,

                - si la frequence indique un champ fixe, on retient le fichier;

                - sinon , on le retient aussi sans filtrer sur la période

            - si oui,

                - on extrait la periode

                - si elle convient (divers cas ...)

                - si on a pu filtrer sur la variable,
                  ou que variable ="*" ou variable multiple,
                  ou que le fichier contient la bonne variable, eventuellement après renommage
                  alors on retient le fichier

            - A chaque fois qu'on retient un fichier, on ajoute au dict wildcard_facets les
              valeurs recontrées pour les attributs

        - Dès qu'un pattern de la liste url a eu des fichiers qui collent,
          on abandonne l'examen des patterns suivants

    - A la fin , on formate le dictionnaire de valeurs de facettes qui est rendu

    """
    rep = list()
    #
    period = kwargs['period']
    if period != '*' and isinstance(period, six.string_types):
        period = init_period(period)
    #
    periods = None  # Possibly a list of available periods
    if period == "*":  # Need to manage the list of periods
        periods = []  # Init an empty list
    #
    if return_wildcards is not None:
        # Need to manage a dict of periods lists (or sets), which keys = TBD
        # This dict is possibly fed across iterated calls
        periods_dict = return_wildcards.get("period", dict())
        #
        # Change periods dict values type from list to set
        for val in periods_dict:
            periods_dict[val] = set(periods_dict[val])
    else:
        periods_dict = dict()
    #
    wildcards = dict()
    #
    project = kwargs['project']
    #
    if urls is None:
        # Use intake catalog for searching cases
        for values in intake_find(kwargs.copy()):
            path = values.pop('path')
            if check_period_and_store(path, period, values, kwargs, wildcards, merge_periods_on,
                                      return_combinations, periods, periods_dict):
                rep.append(path)
    else:
        # Use glob.glob
        variable = kwargs['variable']
        # account for case where the variable is hosted in another variable's file
        # if 'host_variable' in kwargs:
        #     variable = kwargs.get('host_variable',variable)
        #     kwargs['variable'] = variable
        #     clogger.info("Using host variable %s",variable)
        altvar = kwargs.get('filenameVar', variable)
        save_kwargs = copy.deepcopy(kwargs)
        #
        for one_url in urls:
            clogger.debug("Now processing url " + one_url)
            # Some keywords in kwargs can have values of type 'set', which must then
            # be expanded by cartesian product. This occurs with e.g. cmip6_optimize
            expanded_urls, simple_kwargs, kwargs = cartesian_product_substitute(
                one_url, skip_keys=["variable", ], **save_kwargs)
            for url in expanded_urls:
                # First discard protocol prefix in url element
                remote_prefix, basename = mysplit(url)
                #
                full_template = Template(basename)

                # Use brute force : globbing
                lfiles = find_by_globbing(url, full_template,
                                          simple_kwargs.copy(), kwargs['project'])
                clogger.debug("Found %d files with raw variable name"%len(lfiles))
                
                # Construct a regexp with a group name for each facets but period
                facets_regexp = build_facets_regexp(one_url, kwargs)

                if len(lfiles) == 0 and altvar != variable:
                    clogger.info(
                        "No file found with regular variable name %s, trying with filenameVar %s" %
                        (variable, altvar))
                    lfiles = find_by_globbing(url, full_template, simple_kwargs.copy(),
                        kwargs['project'],alt_variable=altvar)
                    clogger.debug("Found %d files with alt variable name %s"%\
                                  (len(lfiles),altvar))
                    alt_kwargs = kwargs.copy()
                    alt_kwargs['variable'] = altvar
                    facets_regexp = build_facets_regexp(one_url, alt_kwargs)
                elif len(lfiles) == 0:
                    clogger.debug("No alternate variable name is available for %s"
                                  % variable)

                #

                for f in lfiles:
                    if f in rep:
                        continue
                    if check_for_variable(f, url, variable, altvar):
                        # Extract facet values from filename
                        a_match = re.search(facets_regexp, f)
                        if a_match:
                            values = a_match.groupdict()
                            #
                            if check_period_and_store(f, period, values,
                                                      kwargs, wildcards, merge_periods_on,
                                                      return_combinations, periods, periods_dict):
                                rep.append(remote_prefix + f)
                            # else:
                            #    clogger.info("Not appending for" +repr(values))
                        # else:
                        #     clogger.info("No match for "+ f + " and " + facets_regexp)

            # Break on first url with any matching data
            if len(rep) > 0:
                clogger.debug('url %s does match for ' %
                              url + repr(kwargs))
                break

    # Post-process wildcard facets values
    if return_wildcards is not None:
        post_process_wildcard_facets_values(
            wildcards, return_wildcards, kwargs, periods_dict)
        # Change periods dict values type from set to list
        for key in return_wildcards.get('period', []):
            return_wildcards['period'][key] = list(
                return_wildcards['period'][key])
        clogger.info("Attribute period ='*' has values %s" % periods_dict)

    return rep


def fixed_frequency(kwargs):
    return kwargs.get('frequency') in ["fx", "seasonal", "annual_cycle"] or \
        kwargs.get('period') in [cperiod("fx"), ] or \
        kwargs.get('table') in ['fx', ]


def check_for_variable(f, url, variable, altvar):
    #
    OK = False
    remote_prefix, _ = mysplit(url)

    if (url.find("${variable}") >= 0) or variable == '*':
        return True
    if remote_prefix == "":   # Local data
        if (fileHasVar(f, variable) or
                (altvar != variable and fileHasVar(f, altvar))):
            return True
        else:
            clogger.debug("File %s doesn't include variable %s nor %s"%(f,variable,altvar))
    else:  # remote data
        if (variable != altvar and (f.find(altvar) >= 0)) or \
           "," in variable:
            return True
    return False


def check_period_and_store(f, period, values, kwargs, wildcards, merge_periods_on,
                           combinations, periods, periods_dict):
    clogger.debug('Checking ' + f)

    if fixed_frequency(kwargs):
        return store_wildcard_facet_values(f, values, kwargs, wildcards, merge_periods_on, combinations)
    else:
        fperiod = values.get('period', values.get('clim_period'))
        if fperiod and isinstance(fperiod, six.string_types):
            fperiod = init_period(fperiod)
        #
        if fperiod and (periods is not None or period.intersects(fperiod)):
            clogger.debug('Period is OK')
            return store_wildcard_facet_values(f, values, kwargs, wildcards, merge_periods_on,
                                               combinations, fperiod, periods, periods_dict)
        else:
            if not fperiod:
                clogger.debug('not appending %s because period is None ' % f)
            elif not period.intersects(fperiod):
                clogger.debug(
                    'not appending %s because period %s doesn t intersect %s' % (f, fperiod, period))
            else:
                clogger.debug('not appending %s for some other reason %s' % f)
            return False


def mysplit(url):
    """ Splits the url in a prefix (before all ':') and basename
    Remove double // in basename
    """
    remote_prefix = ""
    if re.findall(".*:.*", url):
        remote_prefix = ':'.join(url.split(":")[0:-1]) + ':'
    basename = url.split(":")[-1]  # This discard the remote_prefix if any
    basename = basename.replace("//", "/")
    return remote_prefix, basename


def build_facets_regexp(string, kwargs):
    """STRING is a pattern which includes facet keywords (r"${%s}"),
    KWARGS is a dict of keyword/values

    For later extracting encountered values for those facets which
    have a wildcard, we construct and return a regexp with a group
    name for each facet present in KWARGS (but period)

    """
    _, base = mysplit(string)

    # Change glob syntax wildcards to regexp syntax
    base = base.replace("?", ".").replace("*", ".*")
    # Toward a canonical form...
    base = base.replace("//","/")

    alt_kwargs = kwargs.copy()
    for kw in kwargs:
        # Substitute leftmost occurrences by a group-capable pattern which name is
        # the facet name, and other occurences by a pattern ensuring same value
        #
        # Next condition excludes period attribute, which has a type
        if isinstance(kwargs[kw], six.string_types):
            alt_kwargs[kw] = kwargs[kw].replace("?", ".").replace("*", ".*")
            base = base.replace(r"${%s}" % kw,
                            r"(?P<%s>%s)" % (kw, alt_kwargs[kw]), 1)
            base = base.replace(r"${%s}" % kw, r"(?P=%s)" % kw)
    facets_regexp = base.replace(date_keyword, date_regexp_pattern, 1)
    facets_regexp = facets_regexp.replace(date_keyword, r"(?P=period)")
    #
    return facets_regexp


def rreplace(thestring, replaced, replacement):
    # Does replace only the rightmost occurrence of REPLACED in
    # THESTRING by REPLACEMENT
    deb = thestring.rfind(replaced)
    if deb >= 0:
        end = deb + len(replaced)
        return thestring[0:deb] + replacement + thestring[end:]
    else:
        return thestring


def store_wildcard_facet_values(f, values, kwargs, wildcards, merge_periods_on=None,
                                combinations=None, fperiod=None, periods=None, periods_dict=None):
    """
    Using facet values in dict VALUES, find the value for each 
    facet name in KWARGS, and stores (add) it in dict WILDCARDS
    (which keys are facet names and values are set of encountered
    values)

    If COMBINATIONS is not None on input, it should be a list, and
    dict VALUES is appended

    Regarding periods, ... (TBD)

    Return False if any facet value is not allowed in project kwargs["project"]
    """

    #
    # first check that all facet values belong to the list of authorized
    # values possibly defined for each facet. Return False otherwise
    project = kwargs["project"]
    proj = cprojects[project]
    for kw in kwargs:
        if kw in ['filenameVar', 'host_variable']:
            valid_values = None
        else:
            valid_values = proj.cvalid(kw, None)
        if kw in values:
            facet_value = values[kw]
            if isinstance(valid_values, list) and (facet_value not in valid_values):
                if project in env.environment.bypass_valid_check_for_project:
                    func = clogger.warning
                else:
                    func = clogger.error
                func("Facet value %s for %s is not allowed (in %s)" %
                     (facet_value, kw, f))
                return False
    #
    process_period = fperiod is not None and periods is not None
    #
    if process_period:
        clogger.debug('Adding period %s' % fperiod)
        periods.append(fperiod)
    #
    for kw in kwargs:
        clogger.debug(
            "Store_wildcard... : processing facet %s with \n%s" % (kw, f))
        if kw not in values:
            clogger.debug("Store_wildcard... : facet %s does not occur for \n%s" % (
                kw, f))
            continue
        facet_value = values[kw]
        clogger.debug("Store_wildcard... : facet %s = %s" % (kw, facet_value))

        # Store facet value in wildcards if key has a wildcard
        if isinstance(kwargs[kw], six.string_types) and \
           ("*" in kwargs[kw] or "?" in kwargs[kw]):
            if kw not in wildcards:
                wildcards[kw] = set()
            wildcards[kw].add(facet_value)
            clogger.debug("Discover %s =%s for file =%s" %
                          (kw, facet_value, f))
            #
            # Store fperiod in periods_dict if key is relevant vs merge_periods_on
            if process_period:
                if merge_periods_on is None:
                    key = None
                elif kw == merge_periods_on:
                    key = facet_value
                else:
                    continue
                if key not in periods_dict:
                    periods_dict[key] = set()
                clogger.debug("adding period %s for key %s in %s" %
                              (str(fperiod), key, periods_dict))
                periods_dict[key].add(fperiod)
    #
    # Store facets combination
    if combinations is not None:
        combinations.append(values)
    return True


def find_by_globbing(url, base_template, simple_kwargs, project, alt_variable=None):

    if alt_variable is not None:
        simple_kwargs['variable'] = alt_variable
    template = base_template.safe_substitute(**simple_kwargs)
    #
    # Do globbing
    clogger.info("Globbing on %s " % template)
    tim1 = time.time()
    lfiles = my_glob(template, url, project)
    clogger.info("Globbed %d files in %d s on %s " %
                 (len(lfiles), time.time() - tim1, template))
    return lfiles


def my_glob(template, url, project):

    # Construct a pattern for also globbing dates
    pattern = template.replace(date_keyword, "*")

    remote_prefix, _ = mysplit(url)
    if remote_prefix:
        lfiles = sorted(glob_remote_data(remote_prefix, pattern))
        clogger.debug("Remote globbing %d files for varname on %s : " %
                      (len(lfiles), remote_prefix + pattern))
    else:  # local data
        if project != 'CMIP6' or not env.environment.optimize_cmip6_wildcards:
            lfiles = sorted(glob.glob(pattern))
        else:
            # If using cmip6_optimize_wildcards_by_subsets , should
            # rather use a globbing which tests that leaf directory
            # exists before globing
            # lfiles = sorted(leaf_glob(pattern))
            lfiles = sorted(glob.glob(pattern))
        clogger.debug("Before regexp filtering : Globbing %d files for varname on %s : " % (
            len(lfiles), pattern))

    if date_keyword not in url:
        ret = set(lfiles)
    else:
        # Must filter with date_regexp, because * with glob for dates is too inclusive
        #
        date_regexp_patt_glob = "(?P<new_period>.*)"
        temp = template.replace(".", "\.").replace("?", ".").replace("*", ".*")
        pattern2 = temp.replace(date_keyword, date_regexp_patt_glob)
        pattern_to_search = re.compile(pattern2)
        patterns_to_fill = re.compile("^" + date_regexp_pattern + "$")
        #
        ret = set()
        for f in lfiles:
            the_match = pattern_to_search.match(f)
            if not the_match:
                raise ValueError("Should not pass here")
            else:
                the_match = the_match.groupdict()["new_period"]
                if patterns_to_fill.match(the_match):
                    ret.add(f)
                # else:
                #     print("No match, ",the_match, patterns_to_fill)
    return list(ret)


def glob_remote_data(url, pattern):
    """
    Returns a list of path names that match pattern, for remote data
    located at url
    """

    if len(url.split(":")) == 3:
        k = 1
    else:
        k = 0

    if re.findall("@", url.split(":")[k]):
        username = url.split(":")[k].split("@")[0]
        host = url.split(":")[k].split("@")[-1]
    else:
        username = ''
        host = url.split(":")[k]

    secrets = netrc.netrc()

    if username:
        if host in secrets.hosts:
            login, account, password = secrets.authenticators(host)
            if login != username:
                password = getpass.getpass(
                    "Password for host '%s' and user '%s': " % (host, username))
        else:
            password = getpass.getpass(
                "Password for host '%s' and user '%s': " % (host, username))
    else:
        if host in secrets.hosts:
            username, account, password = secrets.authenticators(host)
        else:
            username = eval(input("Enter login for host '%s': " % host))
            password = getpass.getpass(
                "Password for host '%s' and user '%s': " % (host, username))

    try:
        connect = ftp.FTP(host, username, password)
        listfiles = connect.nlst(pattern)
        connect.quit()
        return listfiles
    except ftp.all_errors as err_ftp:
        print(err_ftp)
        raise Climaf_Error(
            "Access problem for data %s on host '%s' and user '%s'" % (url, host, username))


def post_process_wildcard_facets_values(wildcards, return_wildcards, kwargs, periods_dict):
    #  For wildcard facets, extract facet values + checks
    for facet in wildcards:
        s = wildcards[facet]
        if facet == "period":
            # print "s =",s," periods_dict =",periods_dict
            for val in periods_dict:
                periods_dict[val] = sort_periods_list(
                    list(periods_dict[val]))
            clogger.info("Attribute period ='*' has values %s" %
                         periods_dict)
            return_wildcards["period"] = periods_dict
        else:
            if len(s) == 1:
                s = s.pop()
                clogger.info("Attribute %s ='%s' has matching value '%s'" % (
                    facet, kwargs[facet], s))
                return_wildcards[facet] = s
            else:
                rep = list(s)
                rep.sort()
                return_wildcards[facet] = rep
                message = "Attribute %s ='%s' has multiple values : %s" % (
                    facet, kwargs[facet], list(s))
                if return_wildcards:
                    clogger.info(message)
                else:
                    clogger.error(message)
