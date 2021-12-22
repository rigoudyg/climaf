#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" CliMAF datasets location handling and data access module

Handles a database of attributes for describing organization and location of datasets
"""

# Created : S.Senesi - 2014

from __future__ import print_function, division, unicode_literals, absolute_import

import six
import os.path
import re
import glob
from string import Template

import env
from env.environment import *
from climaf.utils import Climaf_Error
from climaf.period import init_period
from climaf.netcdfbasics import fileHasVar
from env.clogging import clogger
from climaf.projects.optimize import cmip6_optimize_check_paths, cmip6_optimize_wildcards
from climaf.find_files import selectGenericFiles

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
             :py:func:`~climaf.select_files.selectGenericFiles`. This is the default

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
        entries will be used (which means : the entry (or entries) with the lowest number of wildcards)

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


def selectFiles(return_wildcards=None, merge_periods_on=None, return_combinations=None, \
                with_periods = None, **kwargs):
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
    for org, _ , urls in ofu:
        if org != 'generic' :
            clogger.warning("Organisation = %s will be deprecated quite soon."%org+\
                            "Please refer to you CliMAF wizard for removing its use")
        if return_wildcards is not None and len(return_wildcards) > 0 and org != "generic":
            raise Climaf_Error("Can handle multiple facet query only for organization=generic ")
        if return_combinations is not None and len(return_combinations) > 0 and org != "generic":
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
            if project == "CMIP6" and env.environment.optimize_cmip6_wildcards and \
               cmip6_optimize_check_paths(urls) :
                kwargs_list = cmip6_optimize_wildcards(kwargs2)
                if not with_periods and return_combinations is not None :
                    # Just return the list of dicts with facet values combinations
                    return_combinations.extend(kwargs_list)
                    rep.append('dummy')
                else:
                    if return_combinations is None :
                        # Also for glob, but must get periods
                        clogger.warning("cdataset.explore doesn't anymore return choices with  "+\
                                        "optimized CMIP6 search. Use cdataset.glob() or set "+\
                                        "env.environment.optimize_cmip6_wildcards to False")
                    for kwa in kwargs_list :
                        rep.extend(selectGenericFiles(urls, return_combinations = return_combinations, **kwa))
            else:
                rep.extend(selectGenericFiles(urls, return_wildcards = return_wildcards,
                                              return_combinations = return_combinations,
                                              merge_periods_on = merge_periods_on,
                                              **kwargs2))
        else:
            raise Climaf_Error("Cannot process organization " + org + " for simulation " + simulation + " and model " +
                               model + " of project " + project)
    if not ofu:
        return None
    else:
        if len(rep) == 0:
            clogger.warning("no file found for %s, at these "
                            "data locations %s " % (repr(kwargs), repr(urls)))
            clogger.warning("i.e. at " + str([url.replace("${PERIOD}", "$PERIOD").replace("$", "").format(**kwargs)
                                              for url in urls]))
            if env.environment.optimize_cmip6_wildcards:
                clogger.warning("If you think this may be due to fresh data ingest, "
                                "you may wish to reset some of the tables used in "
                                "optimizing CMIP6 data search. See help(climaf.projects.optimize.clear_tables)")
            #if any([kwargs[k] == '' for k in kwargs):
            #    clogger.warning("Please check these empty attributes %s" % [k for k in kwargs if kwargs[k] == ''])
            return None
    # When returning strings (actually filenames), join them in a single string
    if len(rep) > 0 and isinstance((rep[0]),six.string_types) :
        # Discard duplicates (assumes that sorting is harmless for later processing)
        rep = sorted(list(set([f.strip() for f in rep])))
        # Assemble filenames in one single string
        rep = ' '.join(rep)
    return rep


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


def test2():
    return


if __name__ == "__main__":
    test2()


