#!/usr/bin/env python
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

from env.environment import *
from env.clogging import clogger
import env
from climaf.utils import Climaf_Error, Climaf_Classes_Error, cartesian_product_substitute
from climaf.period import init_period, sort_periods_list
from climaf.netcdfbasics import fileHasVar


def selectGenericFiles(urls, return_wildcards=None, merge_periods_on=None, return_combinations=None, **kwargs):
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
                    on retient le fichier

            - A chaque fois qu'on retient un fichier , on ajoute au dict wildcard_facets les valeurs recontrées pour les
              attributs

        - Dès qu'un pattern de la  liste url a eu des fichiers qui collent, on abandonne l'examen des patterns suivants

    - A la fin , on formatte le dictionnaire de valeurs de facettes qui est rendu

    """
    rep = list()
    #
    periods = None  # a list of periods available
    if return_wildcards is not None:
        periods_dict = return_wildcards.get("period", dict())
        for val in periods_dict:
            periods_dict[val] = set(periods_dict[val])
    else:
        periods_dict = dict()
    #
    period = kwargs['period']
    if period == "*":
        periods = []  # Init an empty list of all periods
    elif isinstance(period, six.string_types):
        period = init_period(period)
    #
    variable = kwargs['variable']
    altvar = kwargs.get('filenameVar', variable)
    #
    # a patterns for dates for globbing
    date_glob_patt = "*"
    date_keyword = "${PERIOD}"
    #
    # a pattern for dates for regexp
    digit = "[0-9]"
    year = "%s{4}" % digit
    month = "(01|02|03|04|05|06|07|08|09|10|11|12)"
    day = "([0-3][0-9])"
    hour = "(00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23)"
    minutes = "[0-5][0-9]"
    date = "%s(%s(%s(%s(%s)?)?)?)?" % (year, month, day, hour, minutes)
    rperiod = "(?P<period>(?P<start>%s)([_-](?P<end>%s))?)" % (date, date)
    date_regexp_patt = rperiod
    date_regexp_keyword = "${PERIOD}"
    #
    wildcards = dict()
    #
    save_kwargs = copy.deepcopy(kwargs)
    for one_url in urls:
        # Some keywords in kwargs can have values of type 'set', which must then be
        # expanded by cartesian product
        expanded_urls, simple_kwargs, kwargs = cartesian_product_substitute(one_url, skip_keys=["variable", ],
                                                                            **save_kwargs)
        for url in expanded_urls:
            # First discard protocol prefix in url element
            remote_prefix, basename = mysplit(url)
            #
            # Instantiate keywords in pattern with attributes values provided in kwargs
            my_template = Template(basename)
            template = my_template.safe_substitute(**simple_kwargs)
            # print("template =",template)
            #
            # Construct a pattern for also globbing dates
            temp2 = template.replace(date_keyword, date_glob_patt)
            #
            # Do globbing with plain varname
            lfiles = my_glob(remote_prefix, temp2, url, date_regexp_keyword, date_regexp_patt, kwargs)
            clogger.debug("Globbed %d files with plain varname on %s : " % (len(lfiles), temp2))
            #
            # If unsuccessful using varname, try with filenameVar
            if len(lfiles) == 0 and "filenameVar" in simple_kwargs and simple_kwargs['filenameVar']:
                # Change value of facet 'variable'
                simple_kwargs['variable'] = simple_kwargs['filenameVar']
                template = my_template.safe_substitute(**simple_kwargs)
                temp2 = template.replace(date_keyword, date_glob_patt)
                #
                # Do globbing with fileVarname
                lfiles = my_glob(remote_prefix, temp2, url, date_regexp_keyword, date_regexp_patt, kwargs)
                clogger.debug("Globbed %d files for filenamevar on %s: " % (len(lfiles), temp2))
            #
            # For registering encountered values for those facets which have a wildcard,
            # construct a regexp with a group name for all facets (but period)
            facets_regexp = build_facets_regexp(one_url, kwargs, date_regexp_keyword, date_regexp_patt)

            #
            for f in lfiles:
                #
                # Process fixed-fields case, or extract file time period 
                #
                fperiod = None
                if kwargs.get('frequency') in ["fx", "seasonnal", "annual_cycle"] or kwargs.get('period') in ['fx', ] \
                        or kwargs.get('table') in ['fx', ]:
                    store = False
                    # local data
                    if not remote_prefix and ((basename.find("${variable}") >= 0) or variable in ['*', ] or
                                              fileHasVar(f, variable) or
                                              (variable != altvar and fileHasVar(f, altvar))):
                        store = True
                    elif remote_prefix:  # remote data
                        if (basename.find("${variable}") >= 0) or variable == '*' or \
                           (variable != altvar and (f.find(altvar) >= 0)):
                            store = True
                        else:
                            raise Climaf_Error("For remote files, filename pattern (%s) should include ${varname} " +
                                               "(which is instanciated by variable name or filenameVar)" % f)
                    if store and store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards,
                                                             merge_periods_on, combinations=return_combinations):
                        clogger.debug("adding fixed field :" + remote_prefix + f)
                        rep.append(remote_prefix + f)
                    continue
                else:
                    # Extract file period period from filename
                    fperiod = extract_period(f, template, date_regexp_keyword, date_regexp_patt)
    
                #
                # For non-fixed fields, if file period matches requested period, check variable
                #
                if fperiod and (periods is not None or period.intersects(fperiod)):
                    #
                    clogger.debug('Period is OK - Considering variable filtering on %s and %s for %s' %
                                  (variable, altvar, f))
                    store = False
                    # Filter against variable
                    if url.find("${variable}") >= 0:
                        store = True
                        clogger.debug('appending %s based on variable in filename' % f)
                    elif f not in rep:
                        # local data
                        if not remote_prefix and (variable in ['*', ] or "," in variable or fileHasVar(f, variable) or
                                                  (altvar != variable and fileHasVar(f, altvar))):
                            store = True
                            clogger.debug('appending %s based on multi-var or var exists in file ' % f)
                        # remote data
                        elif remote_prefix:
                            if variable in ['*', ] or "," in variable or (variable != altvar and (f.find(altvar) >= 0)):
                                store = True
                                # Should check time period in the file if not date_regexp
                                clogger.debug('appending %s based on multi-var or altvar ' % (remote_prefix + f))
                            else:
                                mess = "For remote files, filename pattern (%s) should include" % (remote_prefix + f)
                                mess += " ${varname} (which is instanciated by variable name or filenameVar)"
                                raise Climaf_Error(mess)
                    if store:
                        if store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on,
                                                       fperiod, periods, periods_dict,
                                                       combinations=return_combinations):
                            rep.append(f)
                else:
                    if not fperiod:
                        clogger.debug('not appending %s because period is None ' % f)
                    elif not period.intersects(fperiod):
                        clogger.debug('not appending %s because period doesn t intersect %s' % (f, period))
                    else:
                        clogger.debug('not appending %s for some other reason %s' % f)
    
        # Break on first url with any matching data
        if len(rep) > 0:
            clogger.debug('url %s does match for ' % url + repr(kwargs))
            break
        
    # Post-process wildcard facets values
    post_process_wildcard_facets_values(wildcards, return_wildcards, kwargs, periods_dict)
    
    return rep


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


def build_facets_regexp(string, kwargs, date_regexp_keyword, date_regexp_patt):
    """
    STRING is a pattern which includes facet keywords, KWARGS is a dict of 
    keyword/values

    For later extracting encountered values for those facets which have a wildcard,
    we construct and return a regexp with a group name for each facet present in KWARGS 
    (but period)
    """
    _, base = mysplit(string)
    
    # Change glob syntax wildcards to regexp syntax
    base = base.replace("?", ".").replace("*", ".*")
    
    # Substitute rightmost occurrences by a group-capable pattern which name is the facet name
    alt_kwargs = kwargs.copy()
    for kw in kwargs:
        if isinstance(kwargs[kw], six.string_types):  # This excludes period attribute, which has a type
            alt_kwargs[kw] = kwargs[kw].replace("?", ".").replace("*", ".*")
            # We replace by the rightmost because matching fields in filenames
            # (so, at right) is trickier than in pathnames when using wildcards
            # (we could do that only for wildcards facets)
            base = rreplace(base, r"${%s}" % kw, r"(?P<%s>%s)" % (kw, alt_kwargs[kw]))
    # We substitute second and next occurrences by non-group-capable patterns
    facets_regexp = Template(base).safe_substitute(**alt_kwargs)
    #
    # Same for date regexp, except from the left (why ?)  
    facets_regexp = facets_regexp.replace(date_regexp_keyword, date_regexp_patt, 1)
    facets_regexp = facets_regexp.replace(date_regexp_keyword, ".*")
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


def store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on=None,
                                fperiod=None, periods=None, periods_dict=None, combinations=None):
    """Using a (groups-capable) regexp FACETS_REGEXP for finding facet
    values, analyze string F for finding the value of each keyword
    (facet name) in KWARGS, and stores (add) it in dict WILDCARDS
    (which keys are facet names and values are set of encountered
    values)

    If COMBINATIONS is not None on input, it is fed as a list of dict 
    providing key/values pairs for all cases with data

    Regarding periods, ... (TBD)

    Return False if any facet value is not allowed in project kwargs["project"]

    """
    
    #
    # first check that all facet values belong to the list of autorized
    # values possibly defined for each facet. Return False otherwise
    project = kwargs["project"]
    proj = cprojects[project]
    for kw in kwargs:
        it = re.finditer(facets_regexp, f)
        for oc in it:
            try:
                facet_value = oc.group(kw)
            except:
                continue
            valid_values = proj.cvalid(kw, None)
            if isinstance(valid_values, list) and (facet_value not in valid_values):
                clogger.info("Facet value %s for %s is not allowed (in %s)" % (facet_value, kw, f))
                return False
    #
    combination = dict()
    if fperiod is not None and periods is not None:
        clogger.debug('Adding period %s' % fperiod)
        periods.append(fperiod)
    #
    for kw in kwargs:
        it = re.finditer(facets_regexp, f)
        clogger.debug("Store_wildcard... : processing facet %s with \n%s and \n%s" % (kw, facets_regexp, f))
        for oc in it:
            try:
                facet_value = oc.group(kw)
            except:
                clogger.debug("Store_wildcard... : facet %s does not occur in %s for \n%s" % (kw, facets_regexp, f))
                continue
            clogger.debug("Store_wildcard... : facet %s = %s" % (kw, facet_value))
            combination[kw] = facet_value
            if isinstance(kwargs[kw], six.string_types) and ("*" in kwargs[kw] or "?" in kwargs[kw]):
                if facet_value is not None:
                    if kw not in wildcards:
                        wildcards[kw] = set()
                    wildcards[kw].add(facet_value)
                    clogger.debug("Discover %s =%s for file =%s" % (kw, facet_value, f))
                else:
                    clogger.error("Logic issue for kw =%s and file =%s" % (kw, f))
                #
                if fperiod is not None and periods is not None:
                    if merge_periods_on is None:
                        key = None
                    elif kw == merge_periods_on:
                        key = facet_value
                    else:
                        continue
                    if key not in periods_dict:
                        periods_dict[key] = set()
                    clogger.debug("adding period %s for key %s in %s" % (str(fperiod), key, periods_dict))
                    periods_dict[key].add(fperiod)
                else:
                    pass
    #
    # Store facets combination and possibly its period
    if combinations is not None:
        combinations.append(combination)
    return True


def my_glob(remote_prefix, pattern, url, date_regexp_keyword, date_regexp_patt, kwargs):
    if remote_prefix:
        lfiles = sorted(glob_remote_data(remote_prefix, pattern))
        clogger.debug("Remote globbing %d files for varname on %s : " % (len(lfiles), remote_prefix + pattern))
    else:  # local data
        if kwargs['project'] != 'CMIP6' or not env.environment.optimize_cmip6_wildcards:
            lfiles = sorted(glob.glob(pattern))
        else:
            lfiles = sorted(glob.glob(pattern))
            # If using cmip6_optimize_wildcards_by_subsets , should
            # rather use a globbing which tests that leaf directory
            # exists before globing
            # lfiles = sorted(leaf_glob(pattern))
        clogger.debug("Before regexp filtering : Globbing %d files for varname on %s : " % (len(lfiles), pattern))
    # Must filter with date_regexp, because * with glob for dates is too inclusive
    ret = set()
    for f in lfiles:
        if re.search(date_regexp_patt, f) or date_regexp_keyword not in url:
            ret.add(f)
    return list(ret) 
    

def extract_period(filename, template, date_regexp_keyword, date_regexp_patt):
    """Test if TEMPLATE includes a DATE_REGEXP_KEYWORD and if yes,
    replaces it with DATE_REGEXP_PATTERN, after having replaced
    globing wildcards (*,?) by regexp exquivalent wildcards (.*,.)

    The returned template can be used to extract the date values,
    provided DATE_REGEXP_PATERN is a group capable regexp

    Returns None if pattern not found

    """
    # Construct regexp for extracting dates from filename
    date_regexp = None
    template_toreg = template.replace(r"*", r".*").replace(r"?", r".").replace(r"+", r"\+")
    if template_toreg.find(date_regexp_keyword) >= 0:
        date_regexp = template_toreg.replace(date_regexp_keyword, date_regexp_patt, 1)
    if date_regexp:
        tperiod = re.sub(date_regexp, r'\g<period>', filename)
        if tperiod == filename:
            raise Climaf_Error("Cannot find a period in %s with regexp %s" % (filename, date_regexp))
        fperiod = init_period(tperiod)
        return fperiod
    else:
        clogger.info("Cannot yet filter re. time using only file content (for %s)." % filename)

        
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
                password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))
        else:
            password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))
    else:
        if host in secrets.hosts:
            username, account, password = secrets.authenticators(host)
        else:
            username = eval(input("Enter login for host '%s': " % host))
            password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))

    try:
        connect = ftp.FTP(host, username, password)
        listfiles = connect.nlst(pattern)
        connect.quit()
        return listfiles
    except ftp.all_errors as err_ftp:
        print(err_ftp)
        raise Climaf_Error("Access problem for data %s on host '%s' and user '%s'" % (url, host, username))


def post_process_wildcard_facets_values(wildcards, return_wildcards, kwargs, periods_dict):
    #  For wildcard facets, extract facet values + checks
    for facet in wildcards:
        s = wildcards[facet]
        if return_wildcards is not None:
            if facet == "period":
                # print "s =",s," periods_dict =",periods_dict
                for val in periods_dict:
                    periods_dict[val] = sort_periods_list(list(periods_dict[val]))
                clogger.info("Attribute period ='*' has values %s" % periods_dict)
                return_wildcards["period"] = periods_dict
            else:
                if len(s) == 1:
                    s = s.pop()
                    clogger.info("Attribute %s ='%s' has matching value '%s'" % (facet, kwargs[facet], s))
                    return_wildcards[facet] = s
                else:
                    rep = list(s)
                    rep.sort()
                    return_wildcards[facet] = rep
                    message = "Attribute %s ='%s' has multiple values : %s" % (facet, kwargs[facet], list(s))
                    if return_wildcards:
                        clogger.info(message)
                    else:
                        clogger.error(message)
        else:
            clogger.debug("return_wildcards is None")

