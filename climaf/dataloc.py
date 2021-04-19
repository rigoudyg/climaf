#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" CliMAF datasets location handling and data access module

Handles a database of attributes for describing organization and location of datasets
"""

# Created : S.Senesi - 2014

from __future__ import print_function, division, unicode_literals, absolute_import

import os
import six
import os.path
import re
import glob
import subprocess
from string import Template
import ftplib as ftp
import getpass
import netrc
from functools import partial

from env.environment import *
from climaf.utils import Climaf_Error, Climaf_Classes_Error, Climaf_Data_Error
from climaf.period import init_period, sort_periods_list
from climaf.netcdfbasics import fileHasVar
from env.clogging import clogger


class dataloc(object):
    def __init__(self, project="*", organization='generic', url=None, model="*", simulation="*",
                 realm="*", table="*", frequency="*"):
        """
        Create an entry in the data locations dictionary for an ensemble of datasets.

        Args:
          project (str,optional): project name
          model (str,optional): model name
          simulation (str,optional): simulation name
          frequency (str,optional): frequency
          organization (str): name of the organization type, among those handled by
             :py:func:`~climaf.dataloc.selectFiles`
          url (list of strings): list of URLS for the data root directories, local or remote

        Each entry in the dictionary allows to store :

         - a list of path or URLS (local or remote), which are root paths for
           finding some sets of datafiles which share a file organization scheme.

           - For remote data:

             url is supposed to be in the format 'protocol:user@host:path', but
             'protocol' and 'user' are optional. So, url can also be 'user@host:path'
             or 'protocol:host:path' or 'host:path'. ftp is default protocol (and
             the only one which is yet managed, AMOF).

             If 'user' is given:

             - if 'host' is in $HOME/.netrc file, CliMAF check if corresponding
               'login == 'user'. If it is, CliMAF get associated
               password; otherwise it will prompt the user for entering password;
             - if 'host' is not present in $HOME/.netrc file, CliMAF will prompt
               the user for entering password.

             If 'user' is not given:

             - if 'host' is in $HOME/.netrc file, CliMAF get corresponding 'login'
               as 'user' and also get associated password;
             - if 'host' is not present in $HOME/.netrc file, CliMAF prompt the
               user for entering 'user' and 'password'.

             Remark: The .netrc file contains login and password used by the
             auto-login process. It generally resides in the user's home directory
             ($HOME/.netrc). So, it is highly recommended to supply this information
             in .netrc file not to have to enter password in every request.

             Warning: python netrc module does not handle multiple entries for a
             single host. So, if netrc file has two entries for the same host, the
             netrc module only returns the last entry.

             We define two kinds of host: hosts with evolving files, e.g.
             'beaufix'; and the others.

             For any file returned by function :py:meth:`~climaf.classes.cdataset.listfiles`
             which is found in cache:

             - in case of hosts with dynamic files, the file is transferred only
               if its date on server is more recent than that found in cache;
             - for other hosts, the file found in cache is used

         - the name for the corresponding data files organization scheme. The current set of known
           schemes is :

           - CMIP5_DRS : any datafile organized after the CMIP5 data reference syntax, such as on IPSL's Ciclad and
                         CNRM's Lustre
           - EM : CNRM-CM post-processed outputs as organized using EM (please use a list of anyone string for arg urls)
           - generic : a data organization described by the user, using patterns such as described for
             :py:func:`~climaf.dataloc.selectGenericFiles`. This is the default

           Please ask the CliMAF dev team for implementing further organizations.
           It is quite quick for data which are on the filesystem. Organizations
           considered for future implementations are :

           - NetCDF model outputs as available during an ECLIS or ligIGCM simulation
           - ESGF

         - the set of attribute values which simulation's data are
           stored at that URLS and with that organization

           For remote files, filename pattern must include ${varname}, which is instanciated
           by variable name or filenameVar (given via :py:func:`~climaf.classes.calias()`),
           for the sake of efficiency. Please complain if this is inadequate


        For the sake of brievity, each attribute can have the '*'
        wildcard value; when using the dictionary, the most specific
        entries will be used (whic means : the entry (or entries) with the lowest number of wildcards)

        Example :

         - Declaring that all IPSLCM-Z-HR data for project PRE_CMIP6 are stored under a single root path and folllows
           organization named CMIP6_DRS::

            >>> dataloc(project='PRE_CMIP6', model='IPSLCM-Z-HR', organization='CMIP6_DRS', url=['/prodigfs/esg/'])

         - and declaring an exception for one simulation (here, both location and organization are supposed to be
           different)::

            >>> dataloc(project='PRE_CMIP6', model='IPSLCM-Z-HR', simulation='my_exp', organization='EM',
            ...         url=['~/tmp/my_exp_data'])

         - and declaring a project to access remote data (on multiple servers)::

            >>> cproject('MY_REMOTE_DATA', ('frequency', 'monthly'), separator='|')
            >>> dataloc(project='MY_REMOTE_DATA', organization='generic',
            ...         url=['beaufix:/home/gmgec/mrgu/vignonl/*/${simulation}SFX${PERIOD}.nc',
            ...              'ftp:vignonl@hendrix:/home/vignonl/${model}/${variable}_1m_${PERIOD}_${model}.nc']),
            >>> calias('MY_REMOTE_DATA','tas','tas',filenameVar='2T')
            >>> tas = ds(project='MY_REMOTE_DATA', simulation='AMIPV6ALB2G', variable='tas', frequency='monthly',
            ...          period='198101')

         Please refer to the :ref:`example section <examples>` of the documentation for an example with each
         organization scheme


        """
        self.project = project
        self.model = model
        self.simulation = simulation
        self.frequency = frequency
        self.organization = organization
        self.realm = realm
        self.table = table
        if organization not in ['EM', 'CMIP5_DRS', 'generic']:
            raise Climaf_Error("Cannot process organization " + organization)
        if isinstance(url, list):
            self.urls = url
        else:
            if re.findall("^esgf://.*", url):
                self.organization = "ESGF"
            self.urls = [url]
        self.urls = list(map(os.path.expanduser, self.urls))
        alt = []
        for u in self.urls:
            # if u[0] != '$' : alt.append(os.path.abspath(u)) #lv
            if u[0] != '$' and ':' not in u:
                alt.append(os.path.abspath(u))
            else:
                alt.append(u)
        # Change all datedeb-datend patterns to ${PERIOD} for upward compatibility
        alt2 = []
        for u in alt:
            for pat in ["YYYYMMDDHHMM", "YYYYMMDDHH", "YYYYMMDD", "YYYYMM", "YYYY", "${period}"]:
                u = u.replace(pat + "-" + pat, "${PERIOD}")
                u = u.replace(pat + "_" + pat, "${PERIOD}")
                u = u.replace(pat, "${PERIOD}")
            alt2.append(u)
        #
        self.urls = alt2
        # Register new dataloc only if not already registered
        if not (any([loc == self for loc in locs])):
            locs.append(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.model + self.project + self.simulation + self.frequency + self.realm + self.table + \
               self.organization + repr(self.urls)

    def pr(self):
        print("For model " + self.model + " of project " + self.project +
              " for simulation " + self.simulation + " and freq " + self.frequency +
              " locations are : " + repr(self.urls) + " and org is :" + self.organization +
              " and table is :" + self.table + " and realm is :" + self.realm)


def getlocs(project="*", model="*", simulation="*", frequency="*", realm="*", table="*"):
    """ Returns the list of org,freq,url triples which may match the
    list of given attributes values (allowing for wildcards '*') and which have
    the lowest number of wildcards (*) in attributes

    """
    rep = []
    for loc in locs:
        list_loc = [(loc.project, project), (loc.model, model), (loc.simulation, simulation),
                    (loc.frequency, frequency), (loc.realm, realm), (loc.table, table)]
        if all([f[0] in ["*", f[1]] or f[1] == "*" for f in list_loc]):
            stars = [f[0] == "*" or f[1] == "*" for f in list_loc].count(True)
            rep.append((loc.organization, loc.frequency, loc.urls, stars))
    # Must mimimize the number of '*' ? (allows wildcards in dir names, avoid too generic cases)
    # When multiple answers with wildcards, return the ones with the lowest number
    filtered = []
    mini = 100
    for org, freq, url, stars in rep:
        if stars < mini:
            mini = stars
    for org, freq, url, stars in rep:
        if stars == mini:
            filtered.append((org, freq, url))
    # Should we further filter ?
    return filtered


def isLocal(project, model, simulation, frequency, realm="*", table="*"):
    if project == 'file':
        return True
    ofu = getlocs(project=project, model=model, simulation=simulation, frequency=frequency, realm=realm, table=table)
    if len(ofu) == 0:
        return False
    rep = True
    for org, freq, llocs in ofu:
        for loc in llocs:
            if re.findall(".*:.*", loc):
                rep = False
    return rep


def selectFiles(return_wildcards=None, merge_periods_on=None, **kwargs):
    """
    Returns the shortest list of (local or remote) files which include
    the data for the list of (facet,value) pairs provided

    Method :

    - use datalocations indexed by :py:func:`~climaf.dataloc.dataloc` to
      identify data organization and data store urls for these (facet,value)
      pairs

    - check that data organization is as known one, i.e. is one of 'generic',
      CMIP5_DRS' or 'EM'

    - derive relevant filenames search function such as as :
      py:func:`~climaf.dataloc.selectCmip5DrsFiles` from data
      organization scheme

    - pass urls and relevant facet values to this filenames search function

    """
    rep = []
    project = kwargs['project']
    simulation = kwargs['simulation']
    model = kwargs.get("model", "*")
    frequency = kwargs.get("frequency", "*")
    realm = kwargs.get("realm", "*")
    table = kwargs.get("table", "*")

    ofu = getlocs(project=project, model=model, simulation=simulation, frequency=frequency, realm=realm, table=table)
    clogger.debug("locs=" + repr(ofu))
    if len(ofu) == 0:
        clogger.warning("no datalocation found for %s %s %s %s  %s %s " % (project, model, simulation, frequency, realm,
                                                                           table))
    for org, freq, urls in ofu:
        if return_wildcards is not None and len(return_wildcards) > 0 and org != "generic":
            raise Climaf_Error("Can handle multiple facet query only for organization=generic ")
        kwargs2 = kwargs.copy()
        # Convert normalized frequency to project-specific frequency if applicable
        if "frequency" in kwargs and project in frequencies:
            normfreq = kwargs2['frequency']
            if normfreq in frequencies[project]:
                kwargs2['frequency'] = frequencies[project][normfreq]
        # JS # Convert normalized realm to project-specific realm if applicable
        if "realm" in kwargs and project in realms:
            normrealm = kwargs2['realm']
            if normrealm in realms[project]:
                kwargs2['realm'] = realms[project][normrealm]
        #
        # Call organization-specific routine
        if org == "EM":
            rep.extend(selectEmFiles(**kwargs2))
        elif org == "CMIP5_DRS":
            rep.extend(selectCmip5DrsFiles(urls, **kwargs2))
        elif org == "generic":
            rep.extend(selectGenericFiles(urls, return_wildcards=return_wildcards,
                                          merge_periods_on=merge_periods_on, **kwargs2))
        else:
            raise Climaf_Error("Cannot process organization " + org + " for simulation " + simulation + " and model " +
                               model + " of project " + project)
    if not ofu:
        return None
    else:
        if len(rep) == 0:
            clogger.warning("no file found for %s, at these "
                            "data locations %s " % (repr(kwargs), repr(urls)))
            if any([kwargs[k] == '' for k in kwargs]):
                clogger.warning("Please check these empty attributes %s" % [k for k in kwargs if kwargs[k] == ''])
            return None
    # Discard duplicates (assumes that sorting is harmless for later processing)
    rep = sorted(list(set([f.strip() for f in rep])))
    # Assemble filenames in one single string
    return ' '.join(rep)


def selectGenericFiles(urls, return_wildcards=None, merge_periods_on=None, **kwargs):
    """
    Allow to describe a ``generic`` file organization : the list of files returned
    by this function is composed of files which :

     - match the patterns in ``url`` once these patterns are instantiated by
        the values in kwargs, and

     - contain the ``variable`` provided in kwargs

     - match the `period`` provided in kwargs

    In the pattern strings, no keyword is mandatory. However, for remote files,
    filename pattern must include ${varname}, which is instanciated by variable
    name or ``filenameVar`` (given via :py:func:`~climaf.classes.calias()`); this is
    for the sake of efficiency (please complain if inadequate)

    Example :

    >>> selectGenericFiles(project='my_projet',model='my_model', simulation='lastexp', variable='tas', period='1980',
    ...                    urls=['~/DATA/${project}/${model}/*${variable}*${PERIOD}*.nc)']

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
                    ou que variable="*" ou variable multiple,
                    ou que le fichier contient la bonne variable, eventuellement après renommage
                    on retient le fichier

            - A chaque fois qu'on retient un fichier , on ajoute au dict wildcard_facets les valeurs recontrées pour les
              attributs

        - Dès qu'un pattern de la  liste url a eu des fichiers qui collent, on abandonne l'examen des patterns suivants

    - A la fin , on formatte le dictionnaire de valeurs de facettes qui est rendu

    """

    def store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on=None,
                                    fperiod=None, periods=None, periods_dict=None):
        """
        Using a (groups-capable) regexp FACETS_REGEXP for finding facet values, analyze
        string F for finding the value of each keyword (facet name) in KWARGS, and stores
        it in dict WILDCARDS, which keys are facet names and values are set of encountered
        values
        Regarding periods, ... (TBD)
        """
        if fperiod is not None and periods is not None:
            clogger.debug('Adding period %s' % fperiod)
            periods.append(fperiod)
        project = kwargs["project"]
        #
        # first check that all facet values belong to the list of autorized
        # values possibly defined for each facet. Return False otherwise
        for kw in kwargs:
            it = re.finditer(facets_regexp, f)
            for oc in it:
                try:
                    facet_value = oc.group(kw)
                except:
                    continue
                valid_values = cvalid(kw, None, project)
                if isinstance(valid_values, list) and (facet_value not in valid_values):
                    clogger.debug("Facet value %s for %s is not allowed" % (facet_value, kw))
                    return False
        #
        for kw in kwargs:
            it = re.finditer(facets_regexp, f)
            for oc in it:
                try:
                    facet_value = oc.group(kw)
                except:
                    continue
                if isinstance(kwargs[kw], six.string_types) and ("*" in kwargs[kw] or "?" in kwargs[kw]):
                    if facet_value is not None:
                        if kw not in wildcards:
                            wildcards[kw] = set()
                        wildcards[kw].add(facet_value)
                        clogger.debug("Discover %s=%s for file=%s" % (kw, facet_value, f))
                    else:
                        clogger.debug("Logic issue for kw=%s and file=%s" % (kw, f))
                    #
                    if fperiod is not None and periods is not None:
                        if merge_periods_on is None:
                            key = None
                        elif kw == merge_periods_on:
                            key = facet_value
                        else:
                            # print "Skipping for kw=%s,sort=%s"%(kw,merge_periods_on)
                            continue
                        if key not in periods_dict:
                            periods_dict[key] = set()
                        clogger.debug("adding period %s for key %s in %s" % (str(fperiod), key, periods_dict))
                        periods_dict[key].add(fperiod)
                    else:
                        pass
                        # print "no Adding period for %s=%s for %s"%(kw,facet_value,f)
        # print "end of store, periods_dict=",periods_dict, "wild=",wildcards
        return True

    rep = []
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
    # (we store it in a dict only for an for historcial reason)
    #
    digit = "[0-9]"
    date_glob_patt = {"${PERIOD}": "*"}
    date_keywords = ["${PERIOD}"]
    #
    # a pattern for dates for regexp
    # (we store it in a dict only for an for historcial reason)
    #
    annee = "%s{4}" % digit
    mois = "(01|02|03|04|05|06|07|08|09|10|11|12)"
    jour = "([0-3][0-9])"
    heure = "(00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23)"
    minutes = "[0-5][0-9]"
    date = "%s(%s(%s(%s(%s)?)?)?)?" % (annee, mois, jour, heure, minutes)
    rperiod = "(?P<period>(?P<start>%s)([_-](?P<end>%s))?)" % (date, date)
    date_regexp_patt = {"${PERIOD}": rperiod}
    # an ordered list of dates regexp keywords
    date_regexp_keywords = ["${PERIOD}"]
    #
    #
    for url in urls:
        # First discard protocol prefix in url element
        remote_prefix = ""
        if re.findall(".*:.*", url):
            remote_prefix = ':'.join(url.split(":")[0:-1]) + ':'
        basename = url.split(":")[-1]  # This discard the remote_prefix if any
        basename = basename.replace("//", "/")
        #
        # Instantiate keywords in pattern with attributes values provided in kwargs
        my_template = Template(basename)
        template = my_template.safe_substitute(**kwargs)
        #
        # Construct a pattern for globbing dates
        temp2 = template
        for k in date_keywords:
            temp2 = temp2.replace(k, date_glob_patt[k])
        #
        # Do globbing with plain varname
        if remote_prefix:
            lfiles = sorted(glob_remote_data(remote_prefix, temp2))
            clogger.debug("Remote globbing %d files for varname on %s : " % (len(lfiles), remote_prefix + temp2))
        else:  # local data
            lfiles = sorted(glob.glob(temp2))
            clogger.debug("Before regexp filtering : Globbing %d files for varname on %s : " % (len(lfiles), temp2))
            # Must filter with regexp, because * with glob for dates is too inclusive
            alt = []
            for f in lfiles:
                for k in date_keywords:
                    if re.search(date_regexp_patt[k], f) and f not in alt:
                        alt.append(f)
                        continue
                # But must also consider the case where there is no date pattern in file pattern
                if not any([k in url for k in date_regexp_patt]) and f not in alt:
                    alt.append(f)
            lfiles = list(set(alt))  # JS: set(alt) to avoid double files
            clogger.debug("Globbing %d files for varname on %s : " % (len(lfiles), temp2))
        #
        # If unsuccessful using varname, try with filenameVar
        if len(lfiles) == 0 and "filenameVar" in kwargs and kwargs['filenameVar']:
            # Change value of facet 'variable'
            kwargs['variable'] = kwargs['filenameVar']
            template = my_template.safe_substitute(**kwargs)
            temp2 = template
            for k in date_keywords:
                temp2 = temp2.replace(k, date_glob_patt[k])
            #
            # Do globbing with fileVarname
            if remote_prefix:  #
                lfiles = sorted(glob_remote_data(remote_prefix, temp2))
                clogger.debug("Remote globbing %d files for filenamevar on %s: " % (len(lfiles), remote_prefix + temp2))
            else:  # local data
                lfiles = sorted(glob.glob(temp2))
                # Must filter with regexp, because * with glob is too inclusive
                alt = []
                for f in lfiles:
                    for k in date_keywords:
                        if re.search(date_regexp_patt[k], f) and f not in alt:
                            alt.append(f)
                            continue
                    # But must also consider the case where there is no date pattern in file pattern
                    if not any([k in url for k in date_regexp_patt]) and f not in alt:
                        alt.append(f)
                lfiles = alt
                clogger.debug("Globbing %d files for filenamevar on %s: " % (len(lfiles), temp2))
        #
        # For discovering values for those facets which are a wildcard,
        # construct a regexp with a group name for all facets (but period)
        alt_basename = basename.replace("?", ".").replace("*", ".*")
        alt_kwargs = kwargs.copy()

        def rreplace(thestring, replaced, replacement):
            # Does replace only the rightmost occurrence of REPLACED in
            # THESTRING by REPLACEMENT
            # We choose the rightmost because matching fields in filenames
            # (so, at right) is trickier than in pathnames when using wildcards
            deb = thestring.rfind(replaced)
            if deb >= 0:
                end = deb + len(replaced)
                return thestring[0:deb] + replacement + thestring[end:]
            else:
                return thestring
        for kw in kwargs:
            if isinstance(kwargs[kw], six.string_types):  # This excludes period attribute, which has a type
                alt_kwargs[kw] = kwargs[kw].replace("?", ".").replace("*", ".*")
                alt_basename = rreplace(alt_basename, r"${%s}" % kw, r"(?P<%s>%s)" % (kw, alt_kwargs[kw]))
        facets_regexp = Template(alt_basename).safe_substitute(**alt_kwargs)
        #
        for k in date_regexp_keywords:
            facets_regexp = facets_regexp.replace(k, date_regexp_patt[k], 1)
            facets_regexp = facets_regexp.replace(k, ".*")
        #
        wildcards = dict()
        # print "facets_regexp=",facets_regexp
        #
        # Construct regexp for extracting dates from filename
        date_regexp = None
        template_toreg = template.replace(r"*", r".*").replace(r"?", r".").replace(r"+", r"\+")
        # print "template before searching dates : "+template_toreg
        for key in date_regexp_keywords:
            # print "searchin "+key+" in "+template
            start = template_toreg.find(key)
            if start >= 0:
                date_regexp = template_toreg.replace(key, date_regexp_patt[key], 1)
                # print "found ",key," dateregexp ->",date_regexp
                hasEnd = False
                start = date_regexp.find(key)
                # start=date_regexp.find(key)
                if start >= 0:
                    hasEnd = True
                    date_regexp = date_regexp.replace(key, date_regexp_patt[key], 1)
                    # date_regexp=date_regexp.replace(key,date_regexp_patt[key],1)
                break
        # print "date_regexp before searching dates : "+date_regexp
        #
        for f in lfiles:
            # print "processing file "+f
            #
            # Extract file time period
            #
            fperiod = None
            if date_regexp:
                if "P<period>" in date_regexp:
                    # print "date_rexgep=",date_regexp
                    # print "f=",f
                    # print "period=",re.sub(date_regexp,r'\g<period>',f)
                    tperiod = re.sub(date_regexp, r'\g<period>', f)
                    if tperiod == f:
                        raise Climaf_Error("Cannot find a period in %s with regexp %s" % (f, date_regexp))
                    fperiod = init_period(tperiod)
                else:
                    date_regexp0 = date_regexp
                    # print "date_regexp for extracting dates : "+date_regexp0, "file="+f
                    start = re.sub(date_regexp0, r'\1', f)
                    if start == f:
                        raise Climaf_Data_Error("Start period not found in %s using regexp %s" % (f, date_regexp0))  # ?
                    if hasEnd:
                        end = re.sub(date_regexp0, r'\2', f)
                        fperiod = init_period("%s-%s" % (start, end))
                    else:
                        fperiod = init_period(start)
                # print "period for file %s is %s"%(f,fperiod)
                #
                # Filter file time period against required period
            else:
                if ('frequency' in kwargs and ((kwargs['frequency'] == "fx") or
                                               kwargs['frequency'] == "seasonnal" or kwargs[
                                                   'frequency'] == "annual_cycle")):
                    # local data
                    if not remote_prefix and \
                            ((basename.find("${variable}") >= 0) or variable == '*' or
                             fileHasVar(f, variable) or (variable != altvar and fileHasVar(f, altvar))):
                        if store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on):
                            clogger.debug("adding fixed field :" + f)
                            rep.append(f)
                    # remote data
                    elif remote_prefix:
                        if (basename.find("${variable}") >= 0) or variable == '*' or \
                                (variable != altvar and (f.find(altvar) >= 0)):
                            if store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on):
                                clogger.debug("adding fixed field :" + remote_prefix + f)
                                rep.append(remote_prefix + f)
                        else:
                            raise Climaf_Error("For remote files, filename pattern (%s) should include ${varname} " +
                                               "(which is instanciated by variable name or filenameVar)" % f)
                else:
                    clogger.info("Cannot yet filter files re. time using only file content.")
                    # if store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on) :
                    #    rep.append(f)

            #
            # If file period matches requested period, check similarly for variable
            #
            # print "fperiod=",fperiod
            # print "periods=",periods
            # print "inter=",period.intersects(fperiod)
            # print "date_regexp=",date_regexp
            if (fperiod and (periods is not None or period.intersects(fperiod))) \
                    or not date_regexp:
                #
                clogger.debug(
                    'Period is OK - Considering variable filtering on %s and %s for %s' % (variable, altvar, f))
                # Filter against variable
                if url.find("${variable}") >= 0:
                    if store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on,
                                                   fperiod, periods, periods_dict):
                        clogger.debug('appending %s based on variable in filename' % f)
                        rep.append(remote_prefix + f)
                    continue
                if f not in rep:
                    # local data
                    if not remote_prefix and \
                            (variable == '*' or "," in variable or fileHasVar(f, variable) or
                             (altvar != variable and fileHasVar(f, altvar))):
                        if store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on,
                                                       fperiod, periods, periods_dict):
                            # Should check time period in the file if not date_regexp
                            clogger.debug('appending %s based on multi-var or var exists in file ' % f)
                            rep.append(f)
                        continue
                    # remote data
                    elif remote_prefix:
                        if variable == '*' or "," in variable or \
                                (variable != altvar and (f.find(altvar) >= 0)):
                            if store_wildcard_facet_values(f, facets_regexp, kwargs, wildcards, merge_periods_on,
                                                           fperiod, periods, periods_dict):
                                # Should check time period in the file if not date_regexp
                                clogger.debug('appending %s based on multi-var or altvar ' % (remote_prefix + f))
                                rep.append(remote_prefix + f)
                            continue
                        else:
                            mess = "For remote files, filename pattern (%s) should include" % (remote_prefix + f)
                            mess += " ${varname} (which is instanciated by variable name or filenameVar)"
                            raise Climaf_Error(mess)
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

    #  For wildcard facets, discover facet values + checks
    for facet in wildcards:
        s = wildcards[facet]
        if return_wildcards is not None:
            if facet == "period":
                # print "s=",s," periods_dict=",periods_dict
                for val in periods_dict:
                    periods_dict[val] = sort_periods_list(list(periods_dict[val]))
                clogger.info("Attribute period='*' has values %s" % periods_dict)
                return_wildcards["period"] = periods_dict
            else:
                if len(s) == 1:
                    s = s.pop()
                    clogger.info("Attribute %s='%s' has matching value '%s'" % (facet, kwargs[facet], s))
                    return_wildcards[facet] = s
                else:
                    rep = list(s)
                    rep.sort()
                    return_wildcards[facet] = rep
                    message = "Attribute %s='%s' has multiple values : %s" % (facet, kwargs[facet], list(s))
                    if return_wildcards:
                        clogger.info(message)
                    else:
                        clogger.error(message)
        else:
            clogger.debug("return_wildcards is None")
    return rep


def ftpmatch(connect, url):
    """
    Returns a list of files matching url with wildcars "*"  "?" on a remote machine
    """

    def parse_list_line(line, subdirs=[], files=[]):
        parts = line.split(None, 8)
        if line.startswith("d"):
            return subdirs.append(parts[-1])
        elif line.startswith("-"):
            return files.append(parts[-1])
        else:
            return

    if url.find('*') < 0 and url.find('?') < 0:
        lpath_match = [url]
    else:
        lurl = url.split("/")
        for n, elt in enumerate(lurl):
            if elt.find('*') >= 0 or elt.find('?') >= 0:
                break

        prefixpath = os.path.join('/', *lurl[:n]).rstrip("/")
        patt = lurl[n].replace("*", ".*").replace("?", r".")

        lpath_match = []
        # Filename stage
        if len(lurl) == (n + 1):
            all_files = []
            cb = partial(parse_list_line, files=all_files)
            connect.dir(prefixpath, cb)
            for lfile in all_files:
                if re.match(patt, lfile) is not None:
                    lpath_match += [os.path.join(prefixpath, lfile)]
        # directory stage
        else:
            all_subdirs = []
            cb = partial(parse_list_line, subdirs=all_subdirs)
            connect.dir(prefixpath, cb)
            for sdir in all_subdirs:
                if re.match(patt, sdir) is not None:
                    lpath_match += ftpmatch(connect, os.path.join(prefixpath, sdir, *lurl[n + 1:]))
    return lpath_match


# def glob_remote_data(remote, pattern):
#     """
#     Returns a list of path names that match pattern, for remote data
#     located atremote
#     """
#
#     if len(remote.split(":")) == 3:
#         k = 1
#     else:
#         k = 0
#     k = 0
#
#     if re.findall("@", remote.split(":")[k]):
#         username = remote.split(":")[k].split("@")[0]
#         host = remote.split(":")[k].split("@")[-1]
#     else:
#         username = ''
#         host = remote.split(":")[k]
#
#     secrets = netrc.netrc()
#
#     if username:
#         if host in secrets.hosts:
#             login, account, password = secrets.authenticators(host)
#             if login != username:
#                 password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))
#         else:
#             password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))
#     else:
#         if host in secrets.hosts:
#             username, account, password = secrets.authenticators(host)
#         else:
#             username = eval(input("Enter login for host '%s': " % host))
#             password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))
#
#     try:
#         connect = ftp.FTP(host, username, password)
#         listfiles = ftpmatch(connect, pattern)
#         connect.quit()
#         return listfiles
#     except ftp.all_errors as err_ftp:
#         print(err_ftp)
#         raise Climaf_Error("Access problem for data %s on host '%s' and user '%s'" % (pattern, host, username))


# def remote_to_local_filename(url):
#     """
#     url: an url of remote data
#
#     Return local filename of remote file
#     """
#     from climaf import remote_cachedir
#
#     if len(url.split(":")) == 3:
#         k = 1
#     else:
#         k = 0
#
#     return rep


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


def remote_to_local_filename(url):
    """
    url: an url of remote data

    Return local filename of remote file
    """
    from climaf import remote_cachedir

    if len(url.split(":")) == 3:
        k = 1
    else:
        k = 0

    if re.findall("@", url.split(":")[k]):
        hostname = url.split(":")[k].split("@")[-1]
    else:
        hostname = url.split(":")[k]

    local_filename = os.path.expanduser(remote_cachedir) + '/' + hostname + os.path.abspath(url.split(":")[-1])
    return local_filename


def selectEmFiles(**kwargs):
    # Pour A et L : mon, day1, day2, 6hLev, 6hPlev, 3h
    simulation = kwargs['simulation']
    frequency = kwargs['frequency']
    variable = kwargs['variable']
    period = kwargs['period']
    realm = kwargs['realm']
    #
    freqs = {"mon": "", "3h": "_3h"}
    f = frequency
    if f in freqs:
        f = freqs[f]
    rep = []
    # Must look for all realms, here identified by a single letter
    if realm == "*":
        lrealm = ["A", "L", "O", "I"]
    else:
        lrealm = [realm]
    for realm in lrealm:
        clogger.debug("Looking for realm " + realm)
        # Use EM data for finding data dir
        freq_for_em = f
        if realm == 'I':
            freq_for_em = ""  # This is a special case ...
        command = ["grep", "^export EM_DIRECTORY_" + realm + freq_for_em + "=",
                   os.path.expanduser(os.getenv("EM_HOME")) + "/expe_" + simulation]
        try:
            ex = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            clogger.error("Issue getting archive_location for " + simulation + " for realm " + realm + " with: " +
                          repr(command))
            break
        if ex.wait() == 0:
            dir = ex.stdout.read().split("=")[1].replace('"', "").replace("\n", "")
            clogger.debug("Looking at dir " + dir)
            if os.path.exists(dir):
                lfiles = os.listdir(dir)
                for fil in lfiles:
                    # clogger.debug("Looking at file "+fil)
                    fileperiod = periodOfEmFile(fil, realm, f)
                    if fileperiod and period.intersects(fileperiod):
                        if fileHasVar(dir + "/" + fil, variable):
                            rep.append(dir + "/" + fil)
                    # clogger.debug("Done with Looking at file "+fil)
            else:
                clogger.error("Directory %s does not exist for simulation %s, realm %s "
                              "and frequency %s" % (dir, simulation, realm, f))
        else:
            clogger.info("No archive location found for " + simulation + " for realm " + realm + " with: " +
                         repr(command))
    return rep


def periodOfEmFile(filename, realm, freq):
    """
    Return the period covered by a file handled by EM, based on filename
    rules for EM. returns None if file frequency does not fit freq
    """
    if realm == 'A' or realm == 'L':
        if freq == 'mon' or freq == '':
            year = re.sub(r'^.*([0-9]{4}).nc', r'\1', filename)
            if year.isdigit():
                speriod = "%s01-%s12" % (year, year)
                return init_period(speriod)
        else:
            raise Climaf_Error("can yet handle only monthly frequency for realms A and L - TBD")
    elif realm == 'O' or realm == 'I':
        if freq == 'monthly' or freq == 'mon' or freq == '':
            altfreq = 'm'
        elif freq[0:2] == 'da':
            altfreq = 'd'
        else:
            raise Climaf_Error("Can yet handle only monthly and daily frequency for realms O and I - TBD")
        patt = r'^.*_1' + altfreq + r'_([0-9]{8})_*([0-9]{8}).*nc'
        beg = re.sub(patt, r'\1', filename)
        end = re.sub(patt, r'\2', filename)
        # clogger.debug("beg=%s,end=%s,fn=%s"%(beg,end,filename))
        if end == filename or beg == filename:
            return None
        return init_period("%s-%s" % (beg, end))
    else:
        raise Climaf_Error("unexpected realm " + realm)


def selectExampleFiles(urls, **kwargs):
    rep = []
    if kwargs['frequency'] == "monthly":
        for url in urls:
            for realm in ["A", "L"]:
                # dir=l+"/"+realm+"/Origin/Monthly/"+simulation
                dir = url + "/" + realm
                clogger.debug("Looking at dir " + dir)
                if os.path.exists(dir):
                    lfiles = os.listdir(dir)
                    for f in lfiles:
                        clogger.debug("Looking at file " + f)
                        fileperiod = periodOfEmFile(f, realm, 'mon')
                        if fileperiod and fileperiod.intersects(kwargs['period']):
                            if fileHasVar(dir + "/" + f, kwargs['variable']):
                                rep.append(dir + "/" + f)
                            # else: print "No var ",variable," in file", dir+"/"+f
    return rep


def selectCmip5DrsFiles(urls, **kwargs):
    # example for path : CMIP5/[output1/]CNRM-CERFACS/CNRM-CM5/1pctCO2/mon/atmos/
    #      Amon/r1i1p1/v20110701/clivi/clivi_Amon_CNRM-CM5_1pctCO2_r1i1p1_185001-189912.nc
    #
    # second path segment can be any string (allows for : output,output1, merge...),
    # but if 'merge' exists, it is used alone
    # This segment ca also be empty
    #
    # If version is 'last', tries provide version from directory 'last' if available,
    # otherwise those of last dir
    project = kwargs['project']
    model = kwargs['model']
    simulation = kwargs['simulation']
    frequency = kwargs['frequency']
    variable = kwargs['variable']
    realm = kwargs['realm']
    table = kwargs['table']
    period = kwargs['period']
    experiment = kwargs['experiment']
    version = kwargs['version']
    #
    rep = []
    frequency2drs = dict({'monthly': 'mon'})
    freqd = frequency
    if frequency in frequency2drs:
        freqd = frequency2drs[frequency]
    # TBD : analyze ambiguity of variable among realms+tables
    for url in urls:
        totry = ['merge/', 'output/', 'output?/', 'main/', '']
        for p in totry:
            pattern1 = url + "/" + project + "/" + p + "*/" + model  # one * for modelling center
            joker_version = "*"
            patternv = os.sep.join([pattern1, experiment, freqd, realm, table, simulation, joker_version, variable])
            if len(glob.glob(patternv)) > 0:
                break
        patternv = os.sep.join([pattern1, experiment, freqd, realm, table, simulation])
        # Get version directories list
        ldirs = glob.glob(patternv)
        clogger.debug("Globbing with " + patternv + " gives:" + repr(ldirs))
        for repert in ldirs:
            lversions = os.listdir(repert)
            lversions.sort()
            # print "lversions="+`lversions`+ "while version="+version
            cversion = version  # initial guess of the version to use
            if version == "last":
                if len(lversions) == 1:
                    cversion = lversions[0]
                elif len(lversions) > 1:
                    if "last" in lversions:
                        cversion = "last"
                    else:
                        cversion = lversions[-1]  # Assume that order provided by sort() is OK
            # print "using version "+cversion+" for requested version: "+version
            lfiles = glob.glob(os.sep.join([repert, cversion, variable, "*.nc"]))
            # print "listing "+repert+"/"+cversion+"/"+variable+"/*.nc"
            # print 'lfiles='+`lfiles`
            for f in lfiles:
                if freqd != 'fx':
                    # clogger.debug("checking period for "+ f)
                    if freqd == 'day':
                        regex = r'^.*([0-9]{8}-[0-9]{8}).nc$'
                    elif freqd == 'mon':
                        # regex=r'^.*([0-9]{4}[0-9]{2}-[0-9]{4}[0-9]{2}).nc$'
                        regex = r'^.*([0-9]{6}-[0-9]{6}).nc$'
                    elif freqd == 'yr':
                        regex = r'^.*([0-9]{4}-[0-9]{4}).nc$'
                    fileperiod = init_period(re.sub(regex, r'\1', f))
                    if fileperiod and period.intersects(fileperiod):
                        rep.append(f)
                else:
                    clogger.debug("adding fixed field " + f)
                    rep.append(f)

    return rep


def test2():
    return


if __name__ == "__main__":
    test2()


def cvalid(attribute, value=None, project=None):
    """
    Set or get the list of valid values for a CliMAF dataset attribute
    or facet (such as e.g. 'model', 'simulation' ...). Useful for constraining
    those data files which match a dataset definition

    Argument 'project' allows to restrict the use/query
    to the context of the given 'project'.

    Example::

    >>> cvalid('grid' , [ "gr", "gn", "gr1", "gr2" ] , project="CMIP6")
    """
    if project not in cprojects:
        raise Climaf_Classes_Error("project '%s' has not yet been declared" % project)
    if attribute == 'project':
        project = None
    #
    if project and attribute not in cprojects[project].facets:
        raise Climaf_Classes_Error("project '%s' doesn't use facet '%s'" % (project, attribute))
    if value is None:
        rep = cprojects[project].facet_authorized_values.get(attribute, None)
        if not rep:
            rep = cprojects[None].facet_authorized_values.get(attribute, "")
        return rep
    else:
        cprojects[project].facet_authorized_values[attribute] = value
