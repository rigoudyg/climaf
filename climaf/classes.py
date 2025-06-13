#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Basic types and syntax for a CLIMAF Reference Syntax interpreter and driver
 This is a first protoype, where the interpreter is Python itself


"""
# Created : S.Sénési - 2014

from __future__ import print_function, division, unicode_literals, absolute_import

import re
import string
import copy
import os.path
from collections import defaultdict
from functools import reduce, partial
import six
import warnings
import json
import shutil
import glob
import xarray as xr
from datetime import timedelta

from env.environment import *
from climaf.utils import Climaf_Classes_Error, remove_keys_with_same_values
from climaf.dataloc import isLocal, getlocs, selectFiles, dataloc
from climaf.period import init_period, cperiod, merge_periods, intersect_periods_list,\
    lastyears, firstyears, group_periods, freq_to_minutes, build_date_regexp_pattern
from env.clogging import clogger
from climaf.netcdfbasics import fileHasVar, varsOfFile, attrOfFile, timeLimits, model_id, infer_freq

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Should function ds() try to resolve for period=*
auto_resolve = False


def derive_cproject(name, parent_name, new_project_facets=list()):
    """
    Create a new project named 'name' from the project 'parent_name' adding the facets listed in 'new_project_facets'
    if specified. Also derive the location list from the parent project.

    :param name: name of the new project
    :param parent_name: name of the source project
    :param new_project_facets: the list of the facets to add to the new project (could be already present in parent).
    :return: the new project
    """
    if name in cprojects or any([elt.project == name for elt in locs]):
        raise Climaf_Classes_Error(
            "Could not derive a project from an existing one if it already exists: %s." % name)
    else:
        cprojects[parent_name].derive(name, new_project_facets)
        [elt.derive(name) for elt in locs if elt.project == parent_name]


class cproject(object):
    def __init__(self, name, *args, **kwargs):
        """
        Declare a project and its facets/attributes in CliMAF (see below)

        Args:
          name (string) : project name;
           do not use the chosen separator in it (see below)
          args (strings) : attribute names;
           they are free; do not use the chosen separator in it (see below); **CliMAF
           anyway will add attributes :
           project, simulation, variable, period, and domain**
          kwargs (dict) :
           can only be used with keywords :

            - ``sep`` or ``separator`` for indicating the symbol separating
              facets in the dataset syntax. Defaults to ".".
            - ``ensemble`` for declaring a list of attribute
              names which are allowed for defining an ensemble in
              this project ('simulation' is automatically allowed)
            - ``use_frequency`` to declare that the frequency can not be derived from time bounds of the file.
              In this case the facet ``frequency`` is mandatory for the project and a default value must be defined.

        Returns : a cproject object, which string representation is
        the pattern later used in CliMAF Refreence Syntax for
        representing datasets in this project

        A 'cproject' is the definition of a set of attributes, or
        facets, which values will completely define a 'dataset' as
        managed by CliMAF. Its name is one of the possible keys
        for describing data locations (see
        :py:class:`~climaf.dataloc.dataloc`)

        For instance, cproject CMIP5, after its Data Reference Syntax,
        has attributes :
        model, simulation (used for rip), experiment, variable, frequency, realm, table, version


        **A number of projects are built-in**. See :py:mod:`~climaf.projects`

        A dataset in a cproject declared as ::

        >>> cproject('MINE','myfreq','myfacet',sep='_')

        will return ::

          ${project}_${simulation}_${variable}_${period}_${domain}_${myfreq}_${myfacet}

        and will have datasets represented as  e.g.::

          'MINE_hist_tas_[1980-1999]_global_decadal_gabu'

        while an example for built-in cproject CMIP5 will be::

          'CMIP5.historical.pr.[1980].global.monthly.CNRM-CM5.r1i1p1.mon.Amon.atmos.last'

        The attributes list should include all facets which are useful
        for distinguishing datasets from each other, and for computing
        datafile pathnames in the 'generic' organization (see
        :py:class:`~climaf.dataloc.dataloc`)

        A default value for a given facet can be specified, by providing a tuple
        (facet_name,default_value) instead of the facet name. This default value is
        however of lower priority than the value set using :py:func:`~climaf.classes.cdef`

        A project can be declared as having non-standard variable
        names in datafiles, or variables that should undergo re-scaling; see
        :py:func:`~climaf.classes.calias`

        A project can be declared as having non-standard frequency names (this is
        used when accessing datafiles); see :py:func:`~climaf.classes.cfreqs`)

        """
        if name in cprojects:
            clogger.warning("Redefining project %s" % name)
        self.project = name
        #
        self.facets = []
        self.facet_defaults = dict()
        self.facet_authorized_values = dict()
        forced = ['project', 'simulation', 'variable', 'period', 'domain']
        for f in forced:
            self.facets.append(f)
        for a in args:
            if isinstance(a, tuple):
                facet_name, facet_default = a
                self.facet_defaults[facet_name] = facet_default
            else:
                facet_name = a
            if facet_name not in forced:
                self.facets.append(facet_name)
        #
        self.separator = "."
        if "separator" in kwargs:
            self.separator = kwargs['separator']
        if "sep" in kwargs:
            self.separator = kwargs['sep']
        if self.separator == ",":
            raise Climaf_Classes_Error(
                "Character ',' is forbidden as a project separator")
        cprojects[name] = self
        self.crs = ""
        # Build the pattern for the datasets CRS for this cproject
        for f in self.facets:
            self.crs += "${%s}%s" % (f, self.separator)
        self.crs = self.crs[:-1]
        # Create an attribute hodling the list of facets which are allowed
        # for defining an ensemble, and put a first facet there
        self.attributes_for_ensemble = ['simulation']
        if 'ensemble' in kwargs:
            self.attributes_for_ensemble.extend(kwargs["ensemble"])
        self.use_frequency = kwargs.get("use_frequency", False)
        
        # A dict for translating CliMAF facet names to project facet names
        # for use by intake
        self.translate_facet = kwargs.get("translate_facet", dict())

        # A pattern for extracting the period from the filename
        # This is used for project which data is indexed using intake,
        # and only until intake fields 'period_start' and 'period_end'
        # are fixed at IPSL
        self.period_pattern = kwargs.get("period_pattern", "*_${PERIOD}.nc")

        # resolve_ambiguities is a method which chooses among facet values when
        # they are ambiguous. It receives args : dic (the facets dic),
        # facet (the ambiguous facet) and lvalues (the list of possibel values)
        # (historical behaviour is to raise an error on ambiguities)
        self.resolve_ambiguities = None

    def derive(self, new_name, new_facets=list()):
        """
        Derive a new project from this one with name 'new_name' and possibly new facets listed in 'new_facets'
        :param new_name: name of the newly created project
        :param new_facets: list of the new facets
        :return: the new project
        """
        args = list()
        for a in self.facets:
            if a in self.facet_defaults:
                args.append((a, self.facet_defaults[a]))
            else:
                args.append(a)
        args.extend(new_facets)
        kwargs = dict()
        kwargs["separator"] = self.separator
        if len(self.attributes_for_ensemble) > 1:
            kwargs["ensemble"] = self.attributes_for_ensemble[1:]
        return cproject(new_name, *args, **kwargs)

    def __repr__(self):
        return self.crs

    def crs2ds(self, crs):
        """
        Try to interpret string ``crs`` as the CRS of a dataset for
        the cproject. Return the dataset if OK
        """
        fields = crs.split(self.separator)
        if len(fields) == len(self.facets):
            if fields[0] == self.project:
                kvp = dict()
                for i, f in enumerate(self.facets):
                    kvp[f] = fields[i]
                return cdataset(**kvp)

    def build_cvalid_from_tree_of_files(self, project_name=None):
        if project_name is None:
            project_name = self.project
        # Find out the directory paths to be checked (other keys can be considered by hand)
        project_locs = [os.path.dirname(loc) for loc in locs if loc.project in [
            project_name, ]]
        # Do not consider root
        project_locs = [loc.replace(
            "${root}", self.facet_defaults["root"]) for loc in project_locs]
        facets_regexp = re.compile(r"\$\{(?P<facet>[^\{^\}]+)\}")
        list_facets = list()
        for loc in project_locs:
            list_facets.append([m.groupdict()["facet"]
                               for m in facets_regexp.finditer(loc)])
        dict_facets = defaultdict(list)
        for (loc, facets) in zip(project_locs, list_facets):
            loc_list = [loc, ]
            tmp_loc_list = list()
            for facet in facets:
                facet_reg = r"\$\{%s\}" % facet
                facet_regexp = re.compile(facet_reg)
                for tmp_loc in loc_list:
                    match = facet_regexp.match(tmp_loc)
                    if match is not None:
                        begin_tmp_loc = tmp_loc[:tmp_loc.find(
                            os.sep, match.end())]
                        begin_tmp_loc = begin_tmp_loc.replace(facet_reg, "*")
                        list_values = glob.glob(begin_tmp_loc)
                        list_values = [val.replace(tmp_loc[:match.start()], "")[:len(tmp_loc) - match.end()]
                                       for val in list_values]
                        dict_facets[facet].extend(list_values)
                        tmp_loc_list.extend(
                            [tmp_loc.replace(facet_reg, val) for val in list_values])
                    else:
                        tmp_loc_list.append(tmp_loc)
                loc_list, tmp_loc_list = tmp_loc_list, list()
        for key in dict_facets:
            dict_facets[key] = sorted(list(set(dict_facets[key])))
        return dict_facets

    def build_cvalid_conf_file_name(self, project_name=None, choice="both"):
        """
        Build cvalid conf file name from project name.
        :param project_name: name of the default project to be used
        :param choice: where to look for the conf file, either "user" (in $HOME/.climaf), "default" (in climaf/projects)
                       or "both"
        :return: a list of possible conf file names
        """
        if project_name is None:
            project_name = self.project
        cvalid_user_conf_file = os.sep.join(
            [os.environ["HOME"], ".climaf", "cvalid_{}.json".format(project_name)])
        cvalid_default_conf_file = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "project",
                                                "cvalid_{}.json".format(project_name)])
        if choice in ["both", ]:
            return [cvalid_user_conf_file, cvalid_default_conf_file]
        elif choice in ["user", ]:
            return [cvalid_user_conf_file, ]
        elif choice in ["default", ]:
            return [cvalid_default_conf_file, ]
        else:
            raise ValueError("Unknown value for choice: %s" % choice)

    def initialize_cvalid_values(self, project_name=None):
        """
        Initialize cvalid values for the current project with values defined in a json file, either in the CliMAF'
        project directory or in the climaf conf directory.
        :param project_name: name of the project to build the conf file name
        """
        cvalid_conf_files = self.build_cvalid_conf_file_name(
            project_name=project_name, choice="both")
        cvalid_conf_files = [f for f in cvalid_conf_files if os.path.isfile(f)]
        if len(cvalid_conf_files) > 0:
            cvalid_conf_file = cvalid_conf_files[0]
            content = json.load(cvalid_conf_file)
            for key in content:
                self.cvalid(key, content[key])

    def initialize_user_cvalid_values(self, project_name=None, from_tree_of_files=False, force=False):
        """
        Initialize the user's configuration file for project project_name.
        If the configuration file already exists, do nothing except if force=True.
        If from_tree_of_file=True, read the tree of files to find out the possible values (not implemented yet).
        :param project_name: name of the default project
        :param from_tree_of_files: boolean, should the tree of file be read?
        :param force: boolean, should an existing user conf file be bypassed?
        """
        cvalid_user_conf_file = self.build_cvalid_conf_file_name(
            project_name=project_name, choice="user")[0]
        cvalid_default_conf_file = self.build_cvalid_conf_file_name(
            project_name=project_name, choice="default")[0]
        if os.path.isfile(cvalid_user_conf_file):
            if force:
                clogger.warning("User's cvalid configuration file %s already exists and force=True, replace it" %
                                cvalid_user_conf_file)
                os.remove(cvalid_user_conf_file)
                if from_tree_of_files:
                    content = self.build_cvalid_from_tree_of_files(
                        project_name)
                    json.dump(content, cvalid_user_conf_file)
                elif os.path.isfile(cvalid_default_conf_file):
                    if not os.path.isdir(os.path.dirname(cvalid_user_conf_file)):
                        os.makedirs(os.path.dirname(cvalid_user_conf_file))
                    shutil.copyfile(cvalid_default_conf_file,
                                    cvalid_user_conf_file)
                else:
                    clogger.error(
                        "Default cvalid configuration file %s does not exist" % cvalid_default_conf_file)
            else:
                clogger.warning("User's cvalid configuration file %s already exists and force=False, do nothing." %
                                cvalid_user_conf_file)
        elif cvalid_default_conf_file:
            if not os.path.isdir(os.path.dirname(cvalid_user_conf_file)):
                os.makedirs(os.path.dirname(cvalid_user_conf_file))
            shutil.copyfile(cvalid_default_conf_file, cvalid_user_conf_file)
        else:
            clogger.error(
                "Default cvalid configuration file %s does not exist" % cvalid_default_conf_file)

    def cvalid(self, attribute, value=None):
        """Set or get the list of valid values for a CliMAF dataset attribute
        or facet (such as e.g. 'model', 'simulation' ...). Useful
        e.g. for constraining those data files which match a dataset
        definition

        Example::

        >>> cvalid('grid' , [ "gr", "gn", "gr1", "gr2" ])

        """
        #
        if attribute not in self.facets:
            raise Climaf_Classes_Error(
                "project '%s' doesn't use facet '%s'" % (self.project, attribute))
        if value is None:
            return self.facet_authorized_values.get(attribute, None)
        else:
            self.facet_authorized_values[attribute] = value


def cdef(attribute, value=None, project=None):
    """
    Set or get the default value for a CliMAF dataset attribute
    or facet (such as e.g. 'model', 'simulation' ...), for use by
    next calls to :py:class:`~climaf.classes.cdataset()` or to
    :py:func:`~climaf.classes.ds`

    Argument 'project' allows to restrict the use/query of the default
    value to the context of the given 'project'. On can also set the
    (global) default value for attribute 'project'

    There is no actual check that 'attribute' is a valid keyword for
    a call to ``ds`` or ``cdataset``

    Example::

    >>> cdef('project','OCMPI5')
    >>> cdef('frequency','monthly',project='OCMPI5')
    """
    if project not in cprojects:
        raise Climaf_Classes_Error(
            "project '%s' has not yet been declared" % project)
    if attribute == 'project':
        project = None
    #
    if project and attribute not in cprojects[project].facets:
        raise Climaf_Classes_Error(
            "project '%s' doesn't use facet '%s'" % (project, attribute))
    if value is None:
        rep = cprojects[project].facet_defaults.get(attribute, None)
        if not rep:
            rep = cprojects[None].facet_defaults.get(attribute, "")
        return rep
    else:
        cprojects[project].facet_defaults[attribute] = value


cproject(None)
cdef("domain", "global")

# All Cobject instances are registered in this directory :
cobjects = dict()


class cobject(object):
    def __init__(self):
        # crs is the string expression defining the object
        # in the CLIMAF Reference Syntax
        self.crs = "void"

    def __str__(self):
        # return "Climaf object : "+self.crs
        return self.crs

    def __repr__(self):
        return self.crs

    def register(self):
        pass
        # cobjects[self.crs]=self
        # clogger.debug("Object Created ; crs = %s"%(self.crs))

    def erase(self):
        pass
        # del(cobjects[self.crs])
        # clogger.debug("Object deleted ; crs = %s"%(self.crs))

    def buildcrs(self):
        raise NotImplementedError

    def __eq__(self, other):
        """
        Check the equality of two CliMAF objects.
        :param other: CliMAF object to be compared
        :return: boolean indicating whether the CliMAF objects are the same or not
        """
        return isinstance(other, type(self)) and self.crs == other.crs


class cdummy(cobject):
    def __init__(self):
        """
        cdummy class represents dummy arguments in the CRS
        """
        self.crs = self.buildcrs()

    def buildcrs(self, period=None, crsrewrite=None):
        return 'ARG'


def processDatasetArgs(**kwargs):
    """
    Perfom basic checks on kwargs for functions cdataset and eds
    regarding the project where the dataset is defined
    Also complement with default values as handled by the
    project's definition and by cdef()
    """
    if 'project' in kwargs:
        project = kwargs['project']
    else:
        project = cdef("project")
    if project is None:
        raise Climaf_Classes_Error("Must provide a project (Can use cdef)")
    elif project not in cprojects:
        raise Climaf_Classes_Error(
            "Dataset's project '%s' has not "
            "been described by a call to cproject()" % project)
    attval = dict()
    attval["project"] = project
    sep = cprojects[project].separator
    #
    # Register facets values
    for facet in cprojects[project].facets:
        if facet in kwargs and kwargs[facet]:
            val = kwargs[facet]
        else:
            val = cdef(facet, project=project)
        attval[facet] = val
        if val:
            if isinstance(val, list):
                listval = val
            else:
                listval = [val]
            for lval in listval:
                if isinstance(lval, six.string_types) and lval.find(sep) >= 0:
                    raise Climaf_Classes_Error(
                        "You cannot use character '%s' when setting '%s=%s' because "
                        "it is the declared separator for project '%s'. "
                        "See help(cproject) for changing it, if needed" % (sep, facet, val, project))
            # print "initalizing facet %s with value"%(facet,val)
    if attval['project'] == 'CMIP5':
        # Allow for a synonym for 'simulation' in CMIP5 : 'member'
        if 'member' in kwargs and kwargs['member'] not in [None, '']:
            attval['simulation'] = kwargs['member']
            clogger.info(
                'Attribute "member" in project CMIP5 has been translated to "simulation"')
        # Special processing for CMIP5 fixed fields : handling redundancy in facets
        if (attval['table'] == 'fx' or attval['period'] == 'fx' or
                attval['simulation'] == 'r0i0p0' or attval['frequency'] == 'fx'):
            attval['table'] = 'fx'
            attval['period'] = 'fx'
            attval['simulation'] = 'r0i0p0'
            attval['frequency'] = 'fx'
    # Special processing for CMIP6  : facet 'simulation' is forbidden (must use 'realization')
    if (attval['project'] == 'CMIP6') and 'simulation' in kwargs and len(kwargs['simulation']) > 0:
        raise Climaf_Classes_Error("You cannot use attribute 'simulation' in CMIP6; please use 'realization'. "
                                   "This if for kwargs=%s" % repr(kwargs))

    errmsg = ""
    for facet in cprojects[project].facets:
        if attval[facet] is None:
            e = "Project '%s' needs facet '%s'. You may use cdef() for setting a default value" \
                % (project, facet)
            errmsg += " " + e
    if errmsg != "":
        raise Climaf_Classes_Error(errmsg)
    #
    # print "kw="+`kwargs`
    for facet in attval:
        # print "checking facet %s"%facet
        # Facet specific processing
        if facet == 'period':
            if attval["period"] == "fx":
                attval["period"] = cperiod(attval["period"])
            elif not isinstance(attval['period'], cperiod) and attval['period'] != "*":
                attval['period'] = init_period(attval['period'])
        # Check for typing or user's logic errors
        if facet not in cprojects[project].facets:
            e = "Project %s doesn't have facet %s" % (project, facet)
            errmsg += " " + e
    if errmsg != "":
        raise Climaf_Classes_Error(errmsg)
    if 'period' in attval and not isinstance(attval['period'], cperiod) and attval['period'] not in ["*", ]:
        Climaf_Classes_Error("at end of  process.. : period is not a cperiod")
    return attval


class cdataset(cobject):
    # def __init__(self,project=None,model=None,simulation=None,period=None,
    #             rip=None,frequency=None,domain=None,variable=None,version='last') :
    def __init__(self, **kwargs):
        """Create a CLIMAF dataset.

        A CLIMAF dataset is a description of what the data (rather than
        the data itself or a file).  It is basically a set of pairs
        attribute-value. The list of attributes actually used to
        describe a dataset is defined by the project it refers
        to.

        To display the attributes you may use for a given project, type e.g.:

        >>> cprojects["CMIP5"]

        For further details on projects , see
        :py:class:`~climaf.classes.cproject`

        None of the project's attributes are mandatory arguments, because
        all attributes defaults to the value set by
        :py:func:`~climaf.classes.cdef` (which also applies if
        providing a None value for an attribute)

        Some attributes have a special format or processing :

        - period : see :py:func:`~climaf.period.init_period`. See also
          function :py:func:`climaf.classes.ds` for added
          flexibility in defining periods as last of first set of years
          among available data

        - domain : allowed values are either 'global' or a list for
          latlon corners ordered as in : [ latmin, latmax, lonmin,
          lonmax ]

        - variable :  name of the geophysical variable ; this should be :

           - either a variable actually included in the datafiles,

           - or a 'derived' variable (see  :py:func:`~climaf.operators_derive.derive` ),

           - or, an aliased variable name (see :py:func:`~climaf.classes.alias` )

        - check : this is actually not a dataset attribute but an
          optionnal argument that can trigger a check of the datafiles
          associated with th dataset; allowed values are : 

            - 'light' : checks that the period indicated by dates in data 
              filenames includes dataset's period (see :py:func:`~climaf.classes.cdataset.light_check)` 

            - 'period' : checks that the period covered by data in files 
              includes dataset's period (see :py:func:`~climaf.classes.cdataset.check)`

            - 'full' : in addition to case 'period', also checks for gaps in 
               data, and for frequency (see :py:func:`~climaf.classes.cdataset.check)`

           An error is raised if the check fails.

        - in project CMIP5 , for triplets (frequency, simulation, period, table )  :
          if any is 'fx' (or 'r0i0p0 for simulation), the others are forced to
          'fx' (resp. 'r0i0p0') too.

        Example, using no default value, and adressing some CMIP5 data ::

          >>>  cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',
          >>>           simulation='r2i3p9', domain=[40,60,-10,20], variable='tas', period='1980-1989', version='last')

        You may use wildcard ('*') in attribute values, and use  :py:meth:`~climaf.classes.cdataset.explore`
        for having CliMAF doing something sensible matching such attributes with available data

        """
        #
        attval = processDatasetArgs(**kwargs)
        #
        # TBD : Next lines for backward compatibility, but should re-engineer
        self.project = attval["project"]
        self.simulation = attval['simulation']
        self.variable = attval['variable']
        # alias is a n-plet : filevar, scale, offset, filenameVar, missing
        self.period = attval['period']
        self.domain = attval['domain']
        #
        self.model = attval.get('model', "*")
        self.frequency = attval.get('frequency', "*")
        # Normalized name is annual_cycle, but allow also for 'seasonal' for the time being
        if self.frequency in ['seasonal', 'annual_cycle']:
            self.period.fx = True
        freqs_dic = frequencies.get(self.project, None)
        # print freqs_dic
        if freqs_dic:
            for k in freqs_dic:
                if freqs_dic[k] == self.frequency and k == 'annual_cycle':
                    self.period.fx = True
        #
        self.kvp = attval
        self.alias = varIsAliased(self.project, self.variable)
        #
        if "," in self.variable and self.alias:
            filevar, scale, offset, units, filenameVar, missing, conditions = self.alias
            if filevar != self.variable or scale != 1. or offset != 0 or missing:
                raise Climaf_Classes_Error(
                    "Cannot alias/scale/setmiss on group variable")
        # Build CliMAF Ref Syntax for the dataset
        self.crs = self.buildcrs()
        #
        self.files = None
        self.local_copies_of_remote_files = None
        self.register()
        if "check" in kwargs:
            if kwargs["check"] == "light":
                if not self.light_check():
                    raise Climaf_Classes_Error(
                        "Period light check failed for %s" % self)
            elif kwargs["check"] == "period":
                if not self.check(period=True, gap=False, frequency=False):
                    raise Climaf_Classes_Error(
                        "Period check failed for %s" % self)
            elif kwargs["check"] == "full":
                if not self.check(period=True, gap=True, frequency=True):
                    raise Climaf_Classes_Error(
                        "Period/gap/frequency check failed for %s" % self)
            else:
                raise Climaf_Classes_Error(
                    "Provided value for check is invalid %s" % kwargs["check"])

    def __eq__(self, other):
        res = super(cdataset, self).__eq__(other)
        if res:
            self_kvp = copy.deepcopy(self.kvp)
            self_kvp["model"] = self.model
            self_kvp["frequency"] = self.frequency
            self_kvp["alias"] = self.alias
            other_kvp = copy.deepcopy(other.kvp)
            other_kvp["model"] = other.model
            other_kvp["frequency"] = other.frequency
            other_kvp["alias"] = other.alias
            res = res and all([self_kvp[p] == other_kvp[p] for p in self_kvp])
        return res

    def setperiod(self, period):
        if isinstance(period, six.string_types):
            period = init_period(period)
        self.erase()
        self.period = period
        self.kvp['period'] = period
        self.crs = self.buildcrs()
        self.register()

    def buildcrs(self, period=None, crsrewrite=None):
        crs_template = string.Template(cprojects[self.project].crs)
        dic = self.kvp.copy()
        if period is not None:
            dic['period'] = period
        if isinstance(dic['domain'], list):
            dic['domain'] = repr(dic['domain'])
        rep = "ds('%s')" % crs_template.safe_substitute(dic)
        return rep

    def errata(self):
        if self.project == "CMIP6":
            service = "https://errata.es-doc.org/1/resolve/simple-pid?datasets="
            browser = "firefox"
            try:
                res = self.explore('resolve')
            except:
                raise Climaf_Classes_Error(
                    "Cannot proceed with errata: Cannot resolve ambiguities on %s" % repr(self))
            # CMIP6.CMIP.CNRM-CERFACS.CNRM-ESM2-1.1pctCO2.r1i1p1f2.Emon.expfe.gn.v20181018
            ref = ".".join(["CMIP6", res.kvp["mip"], res.kvp["institute"], res.kvp["model"], res.kvp["experiment"],
                            res.kvp["realization"], res.kvp["table"], res.kvp["variable"], res.kvp["grid"],
                            "v" + res.kvp["version"]])
            clogger.warning("Querying errata service %s using %s" %
                            (service, browser))
            os.system("%s %s%s &" % (browser, service, ref))
            # voir le fichier api_errata_Atef.py pour faire mieux
        else:
            clogger.warning(
                "No errata service is yet defined for project %s" % self.project)

    def isLocal(self):
        # return self.baseFiles().find(":")<0
        model = getattr(self, "model", "*")
        return isLocal(project=self.project, model=model, simulation=self.simulation, frequency=self.frequency,
                       realm=self.kvp.get("realm", "*"), table=self.kvp.get("table", "*"))

    def isCached(self):
        """ TBD : analyze if a remote dataset is locally cached

        """
        # clogger.error("TBD - remote datasets are not yet cached")
        rep = False
        return rep

    def oneVarPerFile(self):
        llocs = getlocs(project=self.project, model=self.model, simulation=self.simulation, frequency=self.frequency,
                        realm=self.kvp.get("realm", "*"), table=self.kvp.get("table", "*"))
        return all([org for org, freq, url in llocs])

    def periodIsFine(self):
        clogger.debug("always returns False, yet - TBD")
        return False

    def domainIsFine(self):
        clogger.debug("a bit too simple yet (domain=='global')- TBD")
        return self.domain == 'global'

    def periodHasOneFile(self):
        return len(self.baseFiles().split(" ")) < 2
        # clogger.debug("always returns False, yet - TBD")
        # return(False)

    def hasOneMember(self):
        clogger.debug("always returns True, yet - TBD")
        return True

    def hasExactVariable(self):
        # Assume that group variable do not need aliasing
        if "," in self.variable:
            return True
        clogger.debug("always returns False, yet - TBD")
        return False

    def missingIsOK(self):
        if self.alias is None:
            return True
        else:
            _, _, _, _, _, missing, _ = self.alias
            return missing is None

    def matches_conditions(self, conditions):
        """
        Return True if, for all keys in dict conditions, the kvp
        value of object for same key is among condition's values (which can be a list)
        Example :
          with conditions={ "model":"CanESM5" , "version": ["20180103", "20190112"] }
          the method will return True for both versions of that model
        """
        if conditions is None:
            return True
        for key in conditions:
            values = conditions[key]
            if not isinstance(values, list):
                values = [values, ]
            if self.kvp[key] not in values:
                return False
        return True

    def prefered_value(self, kw, values_list):
        """ If the project described by dataset's project has a prefered
        value among VALUES_LIST for facet KW, returns it, else None"""
        if "project" in self.kvp:
            project = self.kvp["project"]
            chooser = cprojects[project].resolve_ambiguities
            if chooser:
                clogger.debug("Trying to solve ambiguity for "+repr(kw))
                return chooser(self.kvp, kw, values_list)
            else:
                clogger.error("No way to resolve ambiguity on %s among %s for project %s"\
                              %(kw,values_list,project))

    def check_if_dict_ambiguous(self, input_dict):
        ambiguous_dict = dict()
        non_ambigous_dict = dict()
        for (kw, val) in input_dict.items():
            if isinstance(val, list):
                if len(val) > 1:
                    prefered = self.prefered_value(kw, val)
                    if prefered:
                        non_ambigous_dict[kw] = prefered
                    else:
                        ambiguous_dict[kw] = val
                else:
                    non_ambigous_dict[kw] = val[0]
            elif kw in ['variable', ]:  # Should take care of aliasing to fileVar
                matching_vars = set()
                paliases = aliases.get(self.project, [])
                for variable in paliases:
                    if val == paliases[variable][0]:
                        matching_vars.add(variable)
                if len(matching_vars) == 0:
                    # No filename variable in aliases matches actual filename
                    non_ambigous_dict[kw] = val
                elif len(matching_vars) == 1:
                    # One variable has a filename variable which matches the retrieved filename
                    non_ambigous_dict[kw] = matching_vars[0]
                else:
                    ambiguous_dict[kw] = (val, matching_vars)
            else:
                non_ambigous_dict[kw] = val
        return non_ambigous_dict, ambiguous_dict

    def glob(self, what=None, ensure_period=True, merge_periods=True,
             split=None, use_frequency=False):
        """Datafile exploration for a dataset which possibly has
        wildcards (* and ?) in attributes/facets.

        Returns info regarding matching datafile or directories:

          - if WHAT = 'files' , returns a string of all data filenames

          - otherwise, returns a list of facet/value dictionnaries for
            matching data (or a pair of lists, see SPLIT below)

        If ENSURE_PERIOD is True, returns only results where the
        requested data period is fully covered by the set of data
        files. Each returned period is then the same as the requested
        period

        Otherwise, if MERGE_PERIODS is True, each returned period is
        actually a list of the intersections of the requested period
        and (merged) available data periods.

        Otherwise, individual data file periods are returned.

        if SPLIT is not None, a pair is returned instead of the dicts list :

           - first element is a dict with facets which values are the
             same among all cases

           - second element is the dicts list as above, but in which
             facets with common values are discarded

        Example :

        >>> tos_data = ds(project='CMIP6', mip='CMIP', variable='tos', period='*',
               table='Omon', institute='CNRM-CERFACS', model='CNRM*', realization='r1i1p1f2' )

        >>> common_values, varied_values = tos_data.glob(merge_periods=True, split=True)

        >>> common_values
        {'variable': 'tos', 'period': [1850-2014], 'root': '/bdd',
         'institute': 'CNRM-CERFACS', 'mip': 'CMIP', 'table': 'Omon',
         'experiment': 'historical', 'realization': 'r1i1p1f2', 'version': 'latest',
         'project': 'CMIP6'}

        >>> varied_values
        [{'model': 'CNRM-ESM2-1'  , 'grid': 'gn' },
         {'model': 'CNRM-ESM2-1'  , 'grid': 'gr1'},
         {'model': 'CNRM-CM6-1'   , 'grid': 'gn' },
         {'model': 'CNRM-CM6-1'   , 'grid': 'gr1'},
         {'model': 'CNRM-CM6-1-HR', 'grid': 'gn' } ]

        """
        dic = self.kvp.copy()
        if 'project' not in dic:
            raise Climaf_Classes_Error(
                "Facet 'project' is missing in dataset's facet")
        project = dic['project']
        if "*" in project or "?" in project:
            raise Climaf_Classes_Error("A wildcard in facet project (%s) " % project +
                                       "would stress the file system too much")
        if self.alias:
            filevar, _, _, _, filenameVar, _, conditions = self.alias
            req_var = dic["variable"]
            dic["variable"] = string.Template(filevar).safe_substitute(dic)
            if filenameVar:
                dic["filenameVar"] = filenameVar
        clogger.debug("glob() with dic=%s" % repr(dic))
        cases = list()
        files = selectFiles(with_periods=(merge_periods is True or what in ['files', ]),
                            return_combinations=cases, use_frequency=use_frequency, **dic)
        # Add facet project in each case
        for case in cases:
            case['project'] = project
        #
        if what in ['files', ]:
            return files
        else:
            if ensure_period is True:
                merge_periods = True
            if merge_periods is True:
                cases = group_periods(cases)
                # Keep only the intersection of requested period and data periods
                period = dic['period']
                if period != "*":
                    for case in cases:
                        case['period'] = [p.intersects(
                            period) for p in case['period']]
                if ensure_period is True:
                    # Build the list of cases which period exactly matches
                    tempo = list()
                    for case in cases:
                        if len(case['period']) == 1:
                            # This also fits case period==*
                            case['period'] = case['period'][0]
                        tempo.append(case)
                    cases = tempo
            if split is not None:
                dicts = remove_keys_with_same_values(cases)
                return dicts, cases
            else:
                return cases

    def explore(self, option='check_and_store', group_periods_on=None, operation='intersection', first=None):
        """
        Versatile datafile exploration for a dataset which possibly has wildcards (* and ? ) in
        attributes.

        ``option`` can be :

          - 'choices' for returning a dict which keys are wildcard attributes and entries
            are values list
          - 'resolve' for returning a NEW DATASET with instanciated attributes (if uniquely)
          - 'ensemble' for returning AN ENSEMBLE based on multiple possible values of one
            or more attributes (tell which one is first in labels by using arg 'first')
          - 'check_and_store' (or missing) for just identifying and storing dataset files list
            (while ensuring non-ambiguity check for wildcard attributes)

        This feature works only for projects which organization is of type 'generic'

        **See further below, after the first examples, what can done with wildcard on 'period'**

        Toy example ::

          >>> rst=ds(project="example", simulation="*", variable="rst", period="1980-1981")
          >>> rst
          ds('example|*|rst|1980-1981|global|monthly')

          >>> rst.explore('choices')
          {'simulation': ['AMIPV6ALB2G']}

          >>> instanciated_dataset=rst.explore('resolve')
          >>> instanciated_dataset
          ds('example|AMIPV6ALB2G|rst|1980-1981|global|monthly')

          >>> my_ensemble=rst.explore('ensemble')
          error    : "Creating an ensemble does not make sense because all wildcard attributes have a single possible
                      value ({'simulation': ['AMIPV6ALB2G']})"

        Real life example for options ``choices`` and ``ensemble`` ::

          >>> rst=ds(project="CMIP6", model='*', experiment="*ontrol*", realization="r1i1p1f*", table="Amon",
          ...        variable="rsut", period="1980-1981")
          >>> clog('info')
          >>> rst.explore('choices')
          info     : Attribute institute has matching value CNRM-CERFACS
          info     : Attribute experiment has multiple values : set(['piClim-control', 'piControl'])
          info     : Attribute grid has matching value gr
          info     : Attribute realization has matching value r1i1p1f2
          info     : Attribute mip has multiple values : set(['CMIP', 'RFMIP'])
          info     : Attribute model has multiple values : set(['CNRM-ESM2-1', 'CNRM-CM6-1'])
          {'institute': ['CNRM-CERFACS'], 'experiment': ['piClim-control', 'piControl'], 'grid': ['gr'],
          'realization': ['r1i1p1f2'], 'mip': ['CMIP', 'RFMIP'], 'model': ['CNRM-ESM2-1', 'CNRM-CM6-1']}

          >>> # Let us further select by setting experiment=piControl
          >>> mrst=ds(project="CMIP6", model='*', experiment="piControl", realization="r1i1p1f*", table="Amon",
          ...         variable="rsut", period="1980-1981")
          >>> mrst.explore('choices')
          {'institute': ['CNRM-CERFACS'], 'mip': ['CMIP'], 'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'], 'grid': ['gr'],
           'realization': ['r1i1p1f2']}
          >>> small_ensemble=mrst.explore('ensemble')
          >>> small_ensemble
          cens({
                'CNRM-ESM2-1':ds('CMIP6%%rsut%1980-1981%global%/cnrm/cmip%CNRM-ESM2-1%CNRM-CERFACS%CMIP%Amon%piControl%'
                                 'r1i1p1f2%gr%latest'),
                'CNRM-CM6-1' :ds('CMIP6%%rsut%1980-1981%global%/cnrm/cmip%CNRM-CM6-1%CNRM-CERFACS%CMIP%Amon%piControl%'
                                 'r1i1p1f2%gr%latest')
               })

        When option='choices' and period= '*', the period of all matching files will be either :

          - aggregated among all instances of all attributes with wildcards (default)
          - or, if argument ``group_periods_on`` provides an attribute name, aggregated after
            being sorted on that attribute and merged

        The aggregation is governed by argument ``operation``, which can be either :

          - 'intersection' : which is the most useful case, and hence is the default
          - 'union' : which has not much sense except to know which periods are definitely
            not covered by any data
          - None : no aggregation occurs, and you get a dict of the merged periods, which
            keys are the value of the grouping attribute

        Attribute 'period' cannot use a * without being  == * ;


        Examples without grouping periods over any attribute ::

          >>> # Let us use a kind of dataset which data files are temporally splitted,
          >>> # and allow for various models, and use a wildcard for period
          >>> so=ds(project="CMIP6", model='CNRM*', experiment="piControl", realization="r1i1p1f2",
          ... table="Omon", variable="so", period="*")

          >>> # What is the overall period covered by the union of all datafiles
          >>> # (but not necessarily by a single model!)
          >>> so.explore('choices', operation='union')
          { 'period': [1850-2349], 'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'] .....}

          >>> # What is the intersection of periods covered by each datafile
          >>> so.explore('choices')
          { 'period': [None], 'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'] .....}

          >>> # What is the list of periods covered by datafiles
          >>> so.explore('choices', operation=None)
          { 'period': {None: [1850-1899, 1900-1949, 1950-1999, 2000-2049, 2050-2099,
                              2100-2149, 2150-2199, 2200-2249, 2250-2299, 2300-2349]},
             'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'] .....}

        Examples using periods grouping over an attribute ::

          >>> # What is the intersection of available periods after grouping them on the various values of 'model'
          >>> so.explore('choices',group_periods_on='model')
          { 'period': [1850-2349], 'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'], ....}

          >>> # Same, but explicit the default value
          >>> so.explore('choices',group_periods_on='model',operation='intersection')
          { 'period': [1850-2349], 'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'], ....}

          >>> # What are the aggregated periods for each value of 'model'
          >>> so.explore('choices',group_periods_on='model',operation=None)
          { 'period':
              {'CNRM-ESM2-1': [1850-2349],
               'CNRM-CM6-1' : [1850-2349] },
            'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'], ...}

        """
        use_frequency = cprojects[self.project].use_frequency
        if use_frequency:
            if "frequency" in self.kvp:
                use_frequency = self.kvp["frequency"]
            else:
                use_frequency = cdef("frequency", project=self.project)
                if not use_frequency:
                    use_frequency = False
        dic = self.kvp.copy()
        if self.alias:
            filevar, _, _, _, filenameVar, _, conditions = self.alias
            req_var = dic["variable"]
            dic["variable"] = string.Template(filevar).safe_substitute(dic)
            if filenameVar:
                dic["filenameVar"] = filenameVar
        clogger.debug("Looking with dic=%s" % repr(dic))
        # if option != 'check_and_store' :
        wildcards = dict()
        files = selectFiles(return_wildcards=wildcards, merge_periods_on=group_periods_on,
                            use_frequency=use_frequency, **dic)
        # -- Use the requested variable instead of the aliased
        if self.alias:
            dic["variable"] = req_var
        # if option != 'check_and_store' :
        periods = wildcards.get('period', None)
        # else : periods=None
        if periods:
            # print "periods=",periods
            if option not in ['choices', ]:
                if group_periods_on:
                    raise Climaf_Classes_Error(
                        "Can use 'group_periods_on' only with option='choices'")
                if operation != 'intersection':
                    raise Climaf_Classes_Error(
                        "Can use operation %s only with option='choices'" % operation)
            if operation in ['intersection', ]:
                if group_periods_on:
                    # print "periods=",periods
                    merged_periods = [merge_periods(
                        p) for p in list(periods.values())]
                    inter = merged_periods.pop(0)
                    for p in merged_periods:
                        inter = intersect_periods_list(inter, p)
                else:
                    inter = merge_periods(periods[None])
                wildcards['period'] = inter
            elif operation in ['union', ]:
                to_merge = []
                for plist in list(periods.values()):
                    to_merge.extend(plist)
                wildcards['period'] = merge_periods(to_merge)
            elif operation is None:
                # Merge periods for each facet value separately
                if group_periods_on:
                    for key in periods:
                        periods[key] = merge_periods(periods[key])
                wildcards['period'] = periods
            else:
                raise Climaf_Classes_Error(
                    "Operation %s is not known " % operation)
        #
        wildcard_attributes_list = [k for k in dic if isinstance(
            dic[k], six.string_types) and "*" in dic[k]]
        if option in ['resolve', ]:
            clogger.debug("Trying to resolve on attributes %s" %
                          wildcard_attributes_list)
            non_ambiguous_dict, ambiguous_dict = self.check_if_dict_ambiguous(
                wildcards)
            if len(ambiguous_dict) != 0:
                error_msg = list()
                for kw in sorted(list(ambiguous_dict)):
                    if kw in ["variable", ]:
                        error_msg.append("Filename variable %s is matched by multiple variables %s" %
                                         (ambiguous_dict[kw][0], repr(ambiguous_dict[kw][1])))
                    elif kw in ["period", ]:
                        error_msg.append(
                            "Periods with holes are not handled: %s" % str(ambiguous_dict[kw]))
                    else:
                        error_msg.append("Wildcard attribute %s is ambiguous %s for dataset %s" %
                                         (kw, str(ambiguous_dict[kw]), self))
                raise Climaf_Classes_Error(" ".join(error_msg))
            else:
                dic.update(**non_ambiguous_dict)
                self.files = files
                rep = ds(**dic)
                rep.files = files
                return rep 
        elif option in ['choices', ]:
            clogger.debug(
                "Listing possible values for these wildcard attributes %s" % wildcard_attributes_list)
            self.files = files
            return wildcards
        elif option in ['ensemble', ]:
            clogger.debug("Trying to create an ensemble on attributes %s" %
                          wildcard_attributes_list)
            is_ensemble = False
            for kw in wildcards:
                entry = wildcards[kw]
                # print "entry=",entry, 'type=',type(entry), 'ensemble_kw=',ensemble_kw
                if kw in ['period', ] and isinstance(entry, list):
                    if len(wildcards['period']) > 1:
                        raise Climaf_Classes_Error("Cannot create an ensemble with holes in period (%s)" %
                                                   wildcards['period'])
                    entry = entry[0]
                if isinstance(entry, list):
                    is_ensemble = (len(entry) > 1)
                dic[kw] = entry
            if is_ensemble is False:
                # raise Climaf_Classes_Error("Creating an ensemble does not make sense because all wildcard "+\
                #                           "attributes have a single possible value (%s)"%wildcards)
                clogger.warning("Creating an ensemble with a single member")
            self.files = files
            return eds(first=first, **dic)
        elif option in ['check_and_store', ]:
            for kw in wildcards:
                entry = wildcards[kw]
                if isinstance(entry, list) and len(entry) > 1:
                    raise Climaf_Classes_Error("This dataset is ambiguous on attribute %s='%s'; please choose among :"
                                               " %s or use either 'ensure_dataset=False' (with method baseFiles or "
                                               "listfiles) or 'option=\'choices\' (with method explore). "
                                               "Context is %s" % (kw, dic[kw], entry, self.kvp))
            self.files = files
        else:
            raise Climaf_Classes_Error("Unknown option %s" % option)
                        

    def baseFiles(self, force=False, ensure_dataset=True):
        """ Returns the list of (local or remote) files which include the data
        for the dataset

        Use cached value (i.e. attribute 'files') unless called with arg force=True

        If ensure_dataset is True, forbid ambiguous datasets
        """
        if (force and self.project != 'file') or self.files is None:
            if ensure_dataset:
                clogger.debug(
                    "baseFile calls explore method with default option")
                self.explore()
            else:
                clogger.debug("baseFiles calls explore with option 'choices'")
                cases = self.explore(option='choices')
                clogger.debug("baseFiles : explore result is %s" % cases)
                list_keys = [k for k in cases if type(
                    cases[k]) is list and k != 'period']
                if len(list_keys) > 0:
                    clogger.error(
                        "The dataset is ambiguous on %s; its CRS is %s" % (cases, self))
                    return None
        return self.files

    def listfiles(self, force=False, ensure_dataset=True):
        """ Returns the list of (local or remote) files which include the data
        for the dataset

        Use cached value unless called with arg force=True

        If ensure_dataset is True, forbid ambiguous datasets
        """
        return self.baseFiles(force=force, ensure_dataset=ensure_dataset)

    def hasRawVariable(self):
        """ Test local data files to tell if a dataset variable is actually included
        in files (rather than being a derived, virtual variable)

        For the time being, returns False, which leads to always consider that variables
        declared as 'derived' actually are derived """
        clogger.debug("TBD: actually test variables in files, rather than assuming that variable %s is virtual for "
                      "dataset %s" % (self.variable, self.crs))
        return False

    def light_check(self):
        """Check that dataset's period is covered by the period deduced from
        the filenames of its datafiles. Filenames with non-date digits
        (e.g. initialization year) may generate interpretation
        problems

        Return True if the period is covered

        Nervertheless, data in files may show gaps; use
        dataset.check(gap=True) if you need a deeper check

        """
        #
        pattern = build_date_regexp_pattern()
        files = self.baseFiles()
        if files is None:
            clogger.warning("No data file for dataset %s" % self)
            return None
        files = files.split()
        periods = []
        for fil in files:
            matches = re.findall(pattern, fil)
            if len(matches) != 1:
                clogger.error(
                    f"No (or too much) date(s) found in filename {file}")
                return None
            else:
                # First element is a tuple, which first element matches the period
                periods.append(init_period(matches[0][0]))
        clogger.debug("File periods are :" + str(periods))
        data_period = merge_periods(periods)
        clogger.debug("Merged periods : " + str(data_period))
        return any([p.includes(self.period) for p in data_period])

    def check(self, frequency=False, gap=False, period=True):
        """
        Check time consistency of first variable of a dataset or ensemble members:

        - if frequency is True : check if datafile frequency is consistent
          with facet frequency
        - if gap is True : check if file data have a gap
        - if period is True : check if period covered by data actually includes the
          whole of dataset period (regardless of possible gaps)

        Default case is to check only period

        Returns: True if every check is OK, False if one fails, None if any cannot be analyzed

        For gap and period check, monthly data are processed quite empirically
        """
        #
        if not (frequency or period or gap):
            clogger.error(
                "You must activate at least one of the diags : frequency, gap or period")
            return(None)
        #
        if self.frequency == 'fx' or self.frequency == 'annual_cycle':
            clogger.info("No check for fixed data for %s", self)
            return True
        #
        files = self.baseFiles()
        if not files:
            clogger.error("The dataset has no data file !")
            return None
        files = files.split()
        clogger.debug("List of selected files: %s" % files)
        #
        rep = True
        dsets = [xr.open_dataset(f, use_cftime=True) for f in files]
        all_dsets = xr.combine_by_coords(dsets, combine_attrs='override')
        #
        if "time" not in all_dsets:
            clogger.warning("Cannot yet check a dataset which time dimension" +
                            "is not named 'time' (%s)" % self)
            return None
        #
        monthly = False # JS
        if self.frequency in ["monthly", "mon"]:
            monthly = True
        else:
            field = dsets[0][self.variable]
            if hasattr(field, 'frequency') and field.frequency in ["monthly", "mon"] :
                monthly = True
        #
        times = all_dsets.time
        clogger.debug('Time data of selected files: %s' % times)
        cell_methods = getattr(dsets[0][varOf(self)], "cell_methods", None)
        #time_average = (re.findall('.*time *: *mean', cell_methods)[0] != '')
        # Some HadISST data have cell_methods = 'time: lat: lon: mean', which 
        # does not comply with the CF convention. We have to account for it.
        time_average = (re.findall(' *time: *([a-zA-Z0-9]*: *)*?mean', cell_methods) != [])
        #
        data_freq = infer_freq(times, monthly)
        clogger.debug("Frequency is "+data_freq)
        if data_freq is None:
            if (frequency and self.frequency != "*") or (gap and not monthly):
                clogger.error(
                    "Time interval detected by infer_freq() is None ")
                return None
        #
        if frequency:
            # Check if data time interval is consistent with dataset frequency
            table = {"monthly": "MS", "daily": "D", "day": "D", "6h": "6H", "3h": "3H",
                     "1h": "1H", "6Hourly": "6H", "3Hourly": "3H"}
            if self.frequency not in table:
                clogger.error(
                    "Frequency check cannot handle dataset's frequency %s" % self.frequency)
                return None
            if data_freq != table[self.frequency]:
                message = 'Datafile time interval %s is not consistent with dataset\' frequency %s'
                clogger.warning(message % (data_freq, self.frequency))
                rep = False
        #
        if gap:
            time_values = times.values.flatten()
            # Check if file data have a gap
            clogger.debug("Checking for gap")
            if monthly:
                clogger.warning(
                    "For monthly data, gap check is quite empirical")
                # clogger.error("Check cannot yet check gap monthly data due to" +
                #              " a shortcoming in incrementing for monthly data")
                # return None
                cpt = 0
                for ptim, tim in zip(time_values[:-1], time_values[1:]):
                    delta = tim - ptim
                    if delta < timedelta(days=29) or \
                       delta > timedelta(days=31):
                        rep = False
                        cpt += 1
                        if cpt > 3:
                            break
                        clogger.error("File data time issue between " +
                                      "%s and %s, interval inconsistent with monthly data" %
                                      (ptim, tim))
            else:
                cpt = 0
                delta = freq_to_minutes(data_freq)
                for ptim, tim in zip(time_values[:-1], time_values[1:]):
                    if ptim + timedelta(minutes=delta) != tim:
                        rep = False
                        cpt += 1
                        if cpt > 3:
                            break
                        clogger.error("File data time issue between %s and %s, interval inconsistent with %s" %
                                      (ptim, tim, delta))
        #
        if period:
            # Compare period covered by data files with dataset's period
            clogger.debug("Checking for period")
            if monthly:
                use_freq = "monthly"
            else:
                use_freq = True
            file_period = timeLimits(times, use_frequency=use_freq, cell_methods=cell_methods,
                                     strict_on_time_dim_name=False)
            clogger.debug(
                'Period covered by selected files is: %s' % file_period)
            consist = ""
            if not file_period.includes(self.period):
                consist = "not "
                rep = False
            clogger.info("Data file(s) time period (%s) does %sinclude dataset time period (%s)" %
                         (file_period, consist, self.period) + "=> time periods are %sconsistent." % consist)
        return rep


class cens(cobject, dict):
    def __init__(self, dic={}, order=None, sortfunc=None):
        """Function cens creates a CliMAF object of class ``cens`` ,
        i.e. a dict of objects, which keys are member labels, and
        which members are ordered, using method ``set_order``

        In some cases, ensembles of datasets from the same project
        can also be built easily using :py:func:`~climaf.classes.eds()`

        When applying an operator to an ensemble, CliMAF will know,
        from operator's declaration (see
        :py:func:`~climaf.operators.cscript()`), whether the operator
        'wishes' to get the ensemble or, on the reverse, is not
        'ensemble-capable' :

         - if the operator is ensemble-capable it will deliver it :

           - if it is a script : with a string composed  by
             concatenating the corresponding input files; it will
             also provide the labels list to the script if its
             declaration calls for it with keyword ${labels}
             (see :py:func:`~climaf.operators.cscript()`)
           - if it is a Python function : with the dict of
             corresponding objects

         - if the operator is 'ensemble-dumb', CliMAF will loop
           applying it on each member, and will form a new ensemble
           with the results.

        The dict keys must be label strings, which describe what is
        basically different among members. They are usually used by
        plot scripts to provide a caption allowing to identify each
        dataset/object e.g using various colors.

        Examples (see also :download:`../examples/ensemble.py`) :

        >>> cdef('project','example'); cdef('simulation',"AMIPV6ALB2G")
        >>> cdef('variable','tas');cdef('frequency','monthly')
        >>> #
        >>> ds1980=ds(period="1980")
        >>> ds1981=ds(period="1981")
        >>> #
        >>> myens=cens({'1980':ds1980 , '1981':ds1981 })
        >>> ncview(myens)  # will launch ncview once per member
        >>>
        >>> myens=cens({'1980':ds1980 , '1981':ds1981 }, order=['1981','1980'])
        >>> myens.set_order(['1981','1980'])
        >>>
        >>> # Add a member
        >>> myens['abcd']=ds(period="1982")

        Limitations : Even if an ensemble is a dict, some dict methods
        are not properly implemented (popitem, fromkeys) and function
        iteritems does not use member order

        You can write an ensemble to a file using function
        :py:func:`~climaf.cache.efile`

        """
        if not all(map(lambda x: isinstance(x, six.string_types), list(dic))):
            raise Climaf_Classes_Error("Ensemble keys/labels must be strings")
        if not all(map(lambda x: isinstance(x, cobject), list(dic.values()))):
            raise Climaf_Classes_Error(
                "Ensemble members must be CliMAF objects")
        self.sortfunc = sortfunc
        #
        dict.update(self, dic)
        #
        keylist = list(self)
        try:
            from natsort.natsort import natsorted
            keylist = natsorted(keylist)
        except:
            keylist.sort()
        if order:
            self.set_order(order, None)
        elif sortfunc:
            self.order = sortfunc(keylist)
        else:
            self.order = keylist
        #
        self.crs = self.buildcrs()
        self.register()

    def __eq__(self, other):
        res = super(cens, self).__eq__(other)
        if res:
            res = res and self.order == other.order and all(
                [self.__dict__[m] == other.__dict[m] for m in self.order])
        return res

    def set_order(self, order, ordered_keylist=None):
        ordered_list = [o for o in order]
        ordered_list.sort()
        if ordered_keylist is None:
            ordered_keylist = list(self)
            ordered_keylist.sort()
        if sorted(ordered_list) != sorted(ordered_keylist):
            raise Climaf_Classes_Error(
                "Order list does not match dict keys list : %s   and %s" %
                (repr(ordered_list), repr(ordered_keylist)))
        self.order = order

    def __setitem__(self, k, v):
        if not isinstance(k, six.string_types):
            raise Climaf_Classes_Error("Ensemble keys/labels must be strings")
        if not isinstance(v, cobject):
            raise Climaf_Classes_Error(
                "Ensemble members must be CliMAF objects")
        dict.__setitem__(self, k, v)
        if k not in self.order:
            self.order.append(k)
            if self.sortfunc:
                self.order = self.sortfunc(list(self))
        self.crs = self.buildcrs()
        self.register()

    def items(self):
        return [(elt, self[elt]) for elt in self.order]

    def copy(self):
        e = cens(self,
                 order=[m for m in self.order],
                 sortfunc=self.sortfunc)
        return e

    def pop(self, key, default=None):
        if key in self:
            self.order.remove(key)
            return dict.pop(self, key, default)
        else:
            return default

    def clear(self):
        dict.clear(self)
        self.order = []

    def update(self, it):
        dict.update(self, it)
        if isinstance(it, dict):
            for el, val in list(it.items()):
                self.order.append(el)
        else:
            for el, val in it:
                self.order.append(el)
        if self.sortfunc:
            self.order = self.sortfunc(list(self))

    def buildcrs(self, crsrewrite=None, period=None):
        if crsrewrite is None and period is None:
            # A useful optimization, for multi-model studies
            rep = "cens({%s})" % ",".join(
                ["'%s':%s" % (m, self[m].crs) for m in self.order])
        else:
            rep = "cens({%s})" % ",".join(["'%s':%s" % (m, self[m].buildcrs(crsrewrite=crsrewrite, period=period))
                                           for m in self.order])
        return rep

    def check(self):
        """
        Check time consistency of first variable for each member of the ensemble :
        - check if first data time interval is consistent with dataset frequency
        - check if file data have a gap
        - check if period covered by data files actually includes the whole of dataset period

        Returns: True if period of data files included dataset period, False otherwise.

        Example:

        >>> # Ensemble with monthly frequency
        >>> j0=ds(project='example',simulation='AMIPV6ALB2G', variable='tas', frequency='monthly', period='1980')
        >>> j1=ds(project='example',simulation='AMIPV6ALB2G', variable='tas', frequency='monthly', period='1981')
        >>> ens=cens({'1980':j0, '1981':j1})
        >>> res=ens.check()

        """

        # Call 'check' method of 'cdataset' for each member of the ensemble
        rep = True
        for memb in self:
            # clogger.info('Member: %s'%memb)
            rep = self[memb].check() and rep
        return rep


def eds(first=None, **kwargs):
    """
    Create a dataset ensemble using the same calling sequence as
    :py:func:`~climaf.classes.cdataset`, except that some facets
    are lists, which defines the ensemble members; these facets must be among
    the facets authorized for ensemble in the (single) project involved

    Example::

    >>> cdef("frequency","monthly") ;  cdef("project","CMIP5"); cdef("model","CNRM-CM5")
    >>> cdef("variable","tas"); cdef("period","1860")
    >>> ens=eds(experiment="historical", simulation=["r1i1p1","r2i1p1"])

    Argument 'first' is used when multiple attributes are of list type, and tells which
    of these attributes appears first in member labels

    """
    attval = processDatasetArgs(**kwargs)
    # Check that any facet/attribute of type 'list' (for defining an
    # ensemble) is OK for the project, and that there is at most one
    nlist = 0
    listattr = []
    for attr in attval:
        clogger.debug("Looking at attr %s for ensemble" % attr)
        if isinstance(attval[attr], list) and attr != "domain":
            if attr not in cprojects[attval["project"]].attributes_for_ensemble:
                raise Climaf_Classes_Error(
                    "Attribute %s cannot be used for ensemble" % attr)
            clogger.debug("Attr %s is used for an ensemble" % attr)
            nlist += 1
            listattr.append(attr)
    if len(listattr) < 1:
        raise Climaf_Classes_Error(
            "For building an ensemble, must have at least one attribute which is a list")
    # Create an ensemble of datasets if applicable
    d = dict()
    if len(listattr) == 1:
        # Simple case : only one attribute has multiple values (-> members)
        attr = listattr[0]
        for member in attval[attr]:
            attval2 = attval.copy()
            attval2[attr] = member
            d[member] = cdataset(**attval2)
        return cens(d, order=attval[attr])
    else:
        # Must construct the cartesian product of all list-type attributes
        listattr2 = [att for att in listattr]
        if first is not None:
            listattr2.remove(first)
            att = first
        else:
            # Use the first attributes declared as ensemble-prone for the project
            for a in cprojects[attval["project"]].attributes_for_ensemble:
                print("Checkin listattribute", a, "against", listattr2)
                if a in listattr2:
                    listattr2.remove(a)
                    att = a
                    break
        comb = [[(att, val)] for val in attval[att]]
        while len(listattr2) > 0:
            att = listattr2.pop(0)
            newcomb = []
            for c in comb:
                for v in attval[att]:
                    lst = [e for e in c]
                    lst.append((att, v))
                    newcomb.append(lst)
            comb = newcomb
        orderl = list()
        for c in comb:
            attval2 = attval.copy()
            label = ""
            for att, val in c:
                attval2[att] = val
                label += val + "_"
            label = label[:-1]
            orderl.append(label)
            d[label] = cdataset(**attval2)
        return cens(d, order=orderl)


def fds(filename, simulation=None, variable=None, period=None, model=None):
    """
    fds stands for FileDataSet; it allows to create a dataset simply
    by providing a filename and optionally a simulation name , a
    variable name, a period and a model name.

    For dataset attributes which are not provided, these defaults apply :

    - simulation : the filename basename (without suffix '.nc')
    - variable : the set of variables in the data file
    - period : the period actually covered by the data file (if it has time_bnds)
    - model : the 'model_id' attribute if it exists, otherwise : 'no_model'
    - project  : 'file' (with separator = '|')
    - frequency : the value of global attribute fequency in datafile, if it exists

    The following restriction apply to such datasets :

    - functions :py:func:`~climaf.classes.calias` and
      :py:func:`~climaf.operators_derive.derive` cannot be used for project
      'file'

    Results are unforeseen if all variables do not have the same time axis

    Examples : See :download:`data_file.py <../examples/data_file.py>`

    """
    filename = os.path.expanduser(filename)
    if not os.path.exists(filename):
        raise Climaf_Classes_Error("File %s does no exist" % filename)
    #
    if model is None:
        model = model_id(filename)
    if simulation is None:
        simulation = os.path.basename(filename)[0:-3]
    #
    if variable is None:
        lvars = varsOfFile(filename)
        if len(lvars) == 0:
            raise Climaf_Classes_Error("No variable in file %s" % filename)
        variable = lvars.pop()
        for v in lvars:
            variable += "," + v
    else:
        lvars = variable.split(',')
        for v in lvars:
            if not fileHasVar(filename, v):
                raise Climaf_Classes_Error(
                    "No variable %s in file %s" % (v, filename))
    #
    try:
        fperiod = timeLimits(filename)
    except:
        fperiod = None
    if period is None:
        if fperiod is None:
            period = "fx"
            # raise Climaf_Classes_Error("Must provide a period for file %s " % filename)
        else:
            period = repr(fperiod)
    elif period != 'fx':
        if fperiod and not fperiod.includes(init_period(period)):
            raise Climaf_Classes_Error(
                "Max period from file %s is %s" % (filename, repr(fperiod)))
    #
    d = ds(project='file', model=model, simulation=simulation,
           variable=variable, period=period, path=filename)
    d.files = filename

    d.frequency = attrOfFile(filename, "frequency", "*")
    if period == 'fx':
        d.frequency = 'fx'

    return d


class ctree(cobject):
    def __init__(self, climaf_operator, script, *operands, **parameters):
        """ Builds the tree of a composed object, including a dict for outputs.

        """
        if len(operands) == 0:
            raise Climaf_Classes_Error(
                "Cannot apply an operator to no operand")
        self.operator = climaf_operator
        self.script = script
        import copy
        if script is None:
            self.flags = False
        else:
            self.flags = copy.copy(script.flags)
        self.operands = operands
        if "period" in parameters:
            p = parameters["period"]
            if isinstance(p, cperiod):
                parameters["period"] = repr(p)
        if "variable" in parameters:
            self.variable = parameters["variable"]
        else:
            self.variable = None
        self.parameters = parameters
        for o in operands:
            if o and not isinstance(o, cobject):
                raise Climaf_Classes_Error(
                    "operand " + repr(o) + " is not a CliMAF object")
        self.crs = self.buildcrs()
        self.outputs = dict()
        self.register()

    def buildcrs(self, crsrewrite=None, period=None):
        """ Builds the CRS expression representing applying OPERATOR on
        OPERANDS with PARAMETERS.
        Forces period downtree if provided
        A function for rewriting operand's CRS may be provided

        Special case : if operator is 'select' and sole operand is a dataset and there
        is no parameters, then return dataset's crs. This is the way to avoid
        repetitive data selection, when a data selection has been explictly cached
        """
        first_op = self.operands[0]
        if self.operator in ['select', ] and len(self.operands) == 1 and isinstance(first_op, cdataset) and \
                len(list(self.parameters)) == 0 and first_op.alias is None:
            if crsrewrite is None and period is None:
                return first_op.crs
            else:
                return first_op.buildcrs(crsrewrite=crsrewrite, period=period)
        #
        # General case
        # Operators are listed in alphabetical order; parameters too
        rep = list()
        #
        for op in [o for o in self.operands if o]:
            if crsrewrite is None and period is None and "crs" in dir(op):
                opcrs = op.crs
            else:
                opcrs = op.buildcrs(crsrewrite=crsrewrite, period=period)
            if crsrewrite:
                opcrs = crsrewrite(opcrs)
            rep.append(opcrs)
        #
        for par in [p for p in sorted(list(self.parameters)) if p not in ["member_label", ]]:
            value = self.parameters[par]
            if isinstance(value, six.string_types):
                value = str(value)
            rep.append("{}={}".format(par, repr(value)))
        rep = "%s(%s)" % (self.operator, ",".join(rep))
        # clogger.debug("Create crs for ctree: %s" % rep)
        return rep

    def setperiod(self, period):
        """ modifies the period for all datasets of a tree"""
        self.erase()
        if isinstance(period, six.string_types):
            period = init_period(period)
        for op in self.operands:
            op.setperiod(period)
        self.crs = self.buildcrs(period=period)
        self.register()


class scriptChild(cobject):
    def __init__(self, cobject, varname):
        """
        Builds one of the child of a script call, which represents one output

        """
        self.father = cobject
        self.varname = varname
        self.variable = varname
        self.crs = self.buildcrs()
        self.file = None
        self.register()

    def setperiod(self, period):
        self.erase()
        self.crs = self.buildcrs(period=period)
        self.register()

    def buildcrs(self, period=None, crsrewrite=None):
        if period is None:
            tmp = self.father.crs
        else:
            tmp = self.father.buildcrs(period=period)
        if crsrewrite:
            tmp = crsrewrite(tmp)
        return ".".join([tmp, self.varname])


def compare_trees(tree1, tree2, func, filter_on_operator=None):
    """
    Recursively compares TREE1 and TREE2.

    For the nodes : compares operator and parameters; ensures
    that FILTER_ON_OPERATOR(operator) is not true

    For the leaves (datasets) : ensure that string representations of
    applying function FUNC to the pair of datasets returns the same
    value for all datasets pairs in the (parallel) trees

    Returns that common value : func(leave1,leave2)) or None

    FUNC cannot return None as a valid value
    """
    if isinstance(tree1, cdataset) and isinstance(tree2, cdataset):
        rep = func(tree1, tree2)
        clogger.debug("Comparison of two datasets...")
        clogger.debug("... %s" % str(rep))
        return rep
    elif isinstance(tree1, ctree) and isinstance(tree2, ctree):
        clogger.debug("Comparison of two trees...")
        if tree1.operator == tree2.operator:
            if filter_on_operator:
                if filter_on_operator(tree1.operator):
                    clogger.debug("Operator filtered: %s" % tree1.operator)
                    return None
            if tree1.parameters == tree2.parameters:
                clogger.debug("Parameters are coherent: %s" % tree1.parameters)
                rep = (reduce(lambda a, b: a if repr(a) == repr(b) else None,
                              [compare_trees(op1, op2, func, filter_on_operator)
                              for op1, op2 in zip(tree1.operands, tree2.operands)]))
                clogger.debug("... %s" % str(rep))
                return rep
            else:
                clogger.debug("Parameters are not coherent: %s/%s" %
                              (tree1.parameters, tree2.parameters))
                return None
    elif isinstance(tree1, scriptChild) and isinstance(tree2, scriptChild):
        clogger.debug("Comparison of two scriptChild...")
        if tree1.varname == tree2.varname:
            clogger.debug("... varnames are coherent: %s" % tree1.varname)
            rep = compare_trees(tree1.father, tree2.father,
                                func, filter_on_operator)
            clogger.debug("... %s" % str(rep))
            return rep
        else:
            clogger.debug("... varnames are not coherent: %s/%s" %
                          (tree1.varname, tree2.varname))
            return None


allow_errors_on_ds_call = True  # False


def allow_error_on_ds(allow=True):
    global allow_errors_on_ds_call
    allow_errors_on_ds_call = allow
    # print ('allow_errors_on_ds_call='+`allow_errors_on_ds_call`)


def select_projects(**kwargs):
    """
    If kwargs['project'] is a list (has multiple values), select_projects loops
    on the projects until it finds a file containing the aliased variable name.
    """
    if 'project' not in kwargs:
        return kwargs
    else:
        p_list = kwargs['project']
    if not isinstance(p_list, list):
        # p_list = [p_list]
        return kwargs
    for project in p_list:
        wkwargs = kwargs.copy()
        wkwargs.update(dict(project=project))
        dat = cdataset(**wkwargs)
        files = dat.baseFiles()
        if files:
            clogger.info('-- File found for project ' +
                         project + ' and ' + repr(wkwargs))
            try:
                tmpVarInFile = varIsAliased(project, wkwargs['variable'])[0]
            except:
                tmpVarInFile = wkwargs['variable']
            if fileHasVar(files.split(" ")[0], tmpVarInFile):
                clogger.info('-- Variable ' + tmpVarInFile + ' (aliased to variable ' +
                             wkwargs['variable'] + ') found in ' + files.split(" ")[0])
                return wkwargs
            else:
                clogger.info('-- Variable ' + tmpVarInFile +
                             ' (aliased to variable ' + wkwargs['variable'] + ') was not found in ' + files.split(" ")[
                                 0])
                # clogger.info('--> Try with another project than '+project+' or another variable name')
        else:
            clogger.info('-- No file found for project ' +
                         project + ' and ' + repr(wkwargs))
    return kwargs


def ds(*args, **kwargs):
    """Returns a dataset from its full Climate Reference Syntax
    string. Example ::

     >>> ds('CMIP5.historical.pr.[1980].global.monthly.CNRM-CM5.r1i1p1.mon.Amon.atmos.last')

    Also a shortcut for :py:meth:`~climaf.classes.cdataset`,
    when used with with only keywords arguments. Example ::

     >>> ds(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',\
              simulation='r2i3p9', domain=[40,60,-10,20], variable='tas', period='1980-1989', version='last')

    In that latter case, you may use e.g. period='last_50y' to get the
    last 50 years (or less) of data; but this will work only if no
    dataset's attribute is ambiguous. 'first_50y' also works,
    similarly; and also period='*'.

    You must refer to doc at : :py:meth:`~climaf.classes.cdataset`

    """
    if len(args) > 1:
        raise Climaf_Classes_Error(
            "Must provide either only a string or only keyword arguments")
    # clogger.debug("Entering , with args=%s, kwargs=%s"%(`args`,`kwargs`))
    if len(args) == 0:
        if 'period' in kwargs and isinstance(kwargs['period'], six.string_types):
            if kwargs['period'] == '*' and auto_resolve:
                clogger.info('Trying to solve for period for %s' % kwargs)
                if resolve_star_period(kwargs):
                    # Case where there is a '*' only for period. kwargs has been modified
                    clogger.info('Solved period = %s' % kwargs['period'])
                    return cdataset(**select_projects(**kwargs))
            else:
                match = re.match(
                    "(?P<option>last|LAST|first|FIRST)_(?P<duration>[0-9]*)([yY])$", kwargs['period'])
                if match is not None:
                    return resolve_first_or_last_years(copy.deepcopy(kwargs),
                                                       match.group('duration'),
                                                       option=match.group('option').lower())
        return cdataset(**select_projects(**kwargs))

    crs = args[0]
    results = []
    for cproj in cprojects:
        try:
            dataset = cprojects[cproj].crs2ds(crs)
        except Climaf_Classes_Error:
            dataset = None
        if dataset:
            results.append(dataset)
    if len(results) > 1:
        e = "CRS expression %s is ambiguous among projects %s" % (
            crs, repr(list(cprojects)))
        if allow_errors_on_ds_call:
            clogger.info(e)
        else:
            raise Climaf_Classes_Error(e)
    elif len(results) == 0:
        e = "CRS expression %s is not valid for any project in %s" % (
            crs, repr(list(cprojects)))
        if allow_errors_on_ds_call:
            clogger.debug(e)
        else:
            raise Climaf_Classes_Error(e)
    else:
        rep = results[0]
        if rep.project == 'file':
            rep.files = rep.kvp["path"]
        return rep


def cfreqs(project, dic):
    """
    Allow to declare a dictionary specific to ``project`` for matching
    ``normalized`` frequency values to project-specific frequency values

    Normalized frequency values are :
      decadal, yearly, monthly, daily, 6h, 3h, fx and annual_cycle

    When defining a dataset, any reference to a non-standard
    frequency will be left unchanged both in the datset's CRS and
    when trying to access corresponding datafiles

    Examples::

    >>> cfreqs('CMIP5',{'monthly':'mon' , 'daily':'day' })
    """
    #
    frequencies[project] = dic


def crealms(project, dic):
    """
    Allow to declare a dictionary specific to ``project`` for matching
    ``normalized`` realm names to project-specific realm names

    Normalized realm names are :
      atmos, ocean, land, seaice

    When defining a dataset, any reference to a non-standard
    realm will be left unchanged both in the datset's CRS and
    when trying to access corresponding datafiles

    Examples::

    >>> crealms('CMIP5',{'atmos':'ATM' , 'ocean':'OCE' })
    """
    #
    realms[project] = dic


def calias(project, variable, fileVariable=None, scale=1., offset=0.,
           units=None, missing=None, filenameVar=None, conditions=None):
    """ Declare that in ``project``, ``variable`` is to be computed by
    reading ``filevariable``, and applying ``scale`` and ``offset``;
    (see first example erai below)

    Arg ``conditions`` allows to restrict the effect, based on the value
    of some facets. It is a dictionary of applicable values or
    values'list, which keys are the facets  (see example CMIP6 below)

    Arg ``filenameVar`` allows to tell which fake variable name should be
    used when computing the filename for this variable in this project
    (for optimisation purpose); (see seconf example erai below)

    Can tell that a given constant must be interpreted as a missing value
    (see 4th example, EM, below)

    ``variable`` may be a list. In that case, ``fileVariable`` and
    ``filenameVar``, if provided, should be parallel lists

    `` variable`` can be a comma separated list of variables, in which
    case this tells how variables are grouped in files (it make sense
    to use filenameVar in that case, as this is a way to provide the
    label which is unique to this grouping of variable; scale, offset
    and missing args must be the same for all variables in that case

    Example ::

    >>> # scale and offset may be provided
    >>> calias('erai','tas_degC','t2m',scale=1., offset=-273.15)
    >>> calias('CMIP6','evspsbl',scale=-1., conditions={ 'model':'CanESM5' , 'version': ['20180103', '20190112'] })
    >>> calias('erai','tas','t2m',filenameVar='2T')
    >>> calias('EM',[ 'sic', 'sit', 'sim', 'snd', 'ialb', 'tsice'], missing=1.e+20)
    >>> calias('data_CNRM','so,thetao',filenameVar='grid_T_table2.2')

    NB: A wrapper with same name of this function is defined in
    :py:func:`climaf.driver.calias` and it is the one which is
    exported by module climaf.api. It allows to use a list of
    variable.

    """
    if not fileVariable:
        fileVariable = variable
    if not filenameVar:
        filenameVar = None
    if project not in cprojects:
        raise Climaf_Classes_Error("project %s is not known" % project)
    if project not in aliases:
        aliases[project] = dict()
    if not isinstance(variable, list):
        variable = [variable]
    if not isinstance(filenameVar, list):
        filenameVar = [filenameVar]
    if not isinstance(fileVariable, list):
        fileVariable = [fileVariable]
    if not isinstance(units, list):
        units = [units]
    if conditions is not None:
        for kw in conditions:
            if kw not in cprojects[project].facets:
                raise Climaf_Classes_Error(
                    "Keyword \"%s\" is not allowed for project %s" % (kw, project))
    for v, u, fv, fnv in zip(variable, units, fileVariable, filenameVar):
        aliases[project][v] = (fv, scale, offset, u, fnv, missing, conditions)


def varIsAliased(project, variable):
    """
    Return a n-uplet (fileVariable, scale, offset, filevarName,
    missing,conditions) defining how to compute a 'variable' which
    is not in files, for the 'project'
    """
    if project in aliases and variable in aliases[project]:
        return aliases[project][variable]


def cmissing(project, missing, *kwargs):
    """ Declare that in 'project', a given constant must be interpreted
    as a missing value, for a given set of project's attributes values

    Such a declaration must follow all ``calias`` declarations for the
    same project
    """
    pass
    # raise NotImplementedError()


class cpage_all(cobject):
    def __init__(self, fig_lines=None, orientation=None, page_width=1000., page_height=1500., title="", x=0, y=2):
        """
        Common tools for classes cpage and cpage_pdf.
        """
        if fig_lines is None:
            raise Climaf_Classes_Error("fig_lines must be provided")
        if orientation is not None:
            if orientation in ['portrait', ]:
                page_width = 1000.
                page_height = 1500.
            elif orientation in ['landscape', ]:
                page_width = 1500.
                page_height = 1000.
            else:
                raise Climaf_Classes_Error("if set, orientation must be 'portrait' or 'landscape' (not %s)" %
                                           orientation)
        self.page_width = page_width
        self.page_height = page_height
        self.title = title
        self.x = x
        self.y = y

    def check_figs_list(self, fig_lines, widths, heights):
        if not widths:
            widths = [round(1. / len(fig_lines[0]), 2)] * len(fig_lines[0])
        self.widths = widths

        if not heights:
            heights = [round(1. / len(fig_lines), 2)] * len(fig_lines)
        self.heights = heights

        if not all(isinstance(fig_line, list) for fig_line in fig_lines):
            raise Climaf_Classes_Error(
                "each element in fig_lines must be a list of figures")
        if not all([len(fig_lines[i]) == len(self.widths) for i in range(1, len(fig_lines))]):
            raise Climaf_Classes_Error("each line in fig_lines must have same dimension as widths %d" %
                                       len(self.widths))
        if len(fig_lines) != len(self.heights):
            raise Climaf_Classes_Error(
                "fig_lines must have same size than heights")
        self.fig_lines = fig_lines

    def check_figs_cens(self, fig_lines, widths, heights):
        figs = [fig_lines[fig] for fig in fig_lines.order]
        if not widths:
            widths = [1., ]
        self.widths = widths
        if not heights:
            heights = [round(1. / len(figs), 2)] * len(figs)
        self.heights = heights

        if len(figs) < len(heights) * len(widths):
            figs.extend([None] * (len(heights) * len(widths) - len(figs) + 1))
        self.fig_lines = [
            figs[x: x + len(widths)] for x in range(0, len(heights) * len(widths), len(widths))]

    def buildcrs(self, crsrewrite=None, period=None):
        rep = list()
        for line in self.fig_lines:
            if crsrewrite is not None:
                rep.append("[%s]" % ",".join([f.buildcrs(crsrewrite=crsrewrite) if f is not None else repr(f)
                                              for f in line]))
            else:
                rep.append("[%s]" % ",".join(
                    [f.crs if f is not None else repr(f) for f in line]))
        return rep


class cpage(cpage_all):
    def __init__(self, fig_lines=None, widths=None, heights=None,
                 fig_trim=True, page_trim=True, format="png",
                 orientation=None,
                 page_width=1000., page_height=1500., title="", x=0, y=26, ybox=50, pt=24,
                 font="Times-New-Roman", gravity="North", background="white",
                 insert="", insert_width=200):
        """
        Builds a CliMAF cpage object, which represents an array of figures (output:
        'png' or 'pdf' figure)

        Args:

          fig_lines (a list of lists of figure objects or an ensemble of figure objects):
           each sublist of 'fig_lines' represents a line of figures
          widths (list, optional): the list of figure widths, i.e. the width of each
           column. By default, if fig_lines is:

             - a list of lists: spacing is even
             - an ensemble: one column is used
          heights (list, optional): the list of figure heights, i.e. the
           height of each line. By default spacing is even
          fig_trim (logical, optional): to turn on/off triming for all figures.
           It removes all the surrounding extra space of figures in the page,
           either True (default) or False
          page_trim (logical, optional): to turn on/off triming for the page. It
           removes all the surrounding extra space of the page, either True
           (default) or False
          format (str, optional) : graphic output format, either 'png' (default)
           or 'pdf'(not recommended)
          page_width (float, optional) : width resolution of resultant image;
           CLiMAF default: 1000.
          page_height (float, optional) : height resolution of resultant image;
           CLiMAF default: 1500.
          orientation (str,optional): if set, it supersedes page_width and
           page_height with values 1000*1500 (for portrait) or 1500*1000 (for landscape)
          title (str, optional) : append a label below or above (depending on optional
           argument 'gravity') figures in the page.
          insert(str,optional) : the filename for an image to insert (centered at the
           bottom)
          insert_width(int,optional) : the width at which the inserted image will be
           scaled (in pixels)

        If title is activated:

            - x, y (int, optional): annotate the page with text.
              x is the offset towards the right from the upper left corner
              of the page, while y is the offset upward or the bottom
              according to the optional argument 'gravity' (i.e. 'South' or 'North'
              respectively); CLiMAF default: x=0, y=26. For more details, see:
              http://www.imagemagick.org/script/command-line-options.php?#annotate ;
              where x and y correspond respectively to tx and ty
              in ``-annotate {+-}tx{+-}ty text``
            - ybox (int, optional): width of the assigned box for title;
              CLiMAF default: 50. For more details, see:
              http://www.imagemagick.org/script/command-line-options.php?#splice
            - pt (int, optional): font size of the title; CLiMAF default: 24
            - font (str, optional): set the font to use when creating title; CLiMAF
              default: 'Times-New-Roman'. To print a complete list of fonts, use:
              'convert -list font'
            - gravity (str, optional): the choosen direction specifies where to position
              title; CLiMAF default: 'North'. For more details, see:
              http://www.imagemagick.org/script/command-line-options.php?#gravity
            - background (str, optional): background color of the assigned box for
              title; default: 'white'. To print a complete list of color names, use:
              'convert -list color'

        Example:

         Using no default value, to create a page with 2 columns and 3 lines::

          >>> tas_ds=ds(project='example',simulation='AMIPV6ALB2G', variable='tas', period='1980-1981')
          >>> tas_avg=time_average(tas_ds)
          >>> fig=plot(tas_avg,title='title')
          >>> my_page=cpage([[None, fig],[fig, fig],[fig,fig]], widths=[0.2,0.8],
          ... heights=[0.33,0.33,0.33], fig_trim=False, page_trim=False,
          ... format='pdf', title='Page title', x=10, y=20, ybox=45,
          ... pt=20, font='Utopia', gravity='South', background='grey90',
          ... page_width=1600., page_height=2400.)
        """
        super(cpage, self).__init__(fig_lines=fig_lines, orientation=orientation, page_width=page_width,
                                    page_height=page_height, title=title, x=x, y=y)
        self.fig_trim = fig_trim
        self.page_trim = page_trim
        self.format = format
        self.ybox = ybox
        self.pt = pt
        self.font = font
        self.gravity = gravity
        self.background = background
        self.insert = insert
        self.insert_width = insert_width
        if self.ybox < (self.y + self.pt):
            raise Climaf_Classes_Error(
                "Title exceeds the assigned box: ybox<y+pt")
        if not isinstance(fig_lines, (list, cens)):
            raise Climaf_Classes_Error("fig_lines must be a CliMAF ensemble or a list "
                                       "of lists (each representing a line of figures)")
        elif isinstance(fig_lines, list):
            self.check_figs_list(fig_lines=fig_lines,
                                 widths=widths, heights=heights)
        # case of an ensemble (cens) if heights and widths are not provided
        elif not widths and not heights:
            self.scatter_on_page([fig_lines[label]
                                 for label in fig_lines.order])
        else:  # case of an ensemble (cens) with heights or widths provided
            self.check_figs_cens(fig_lines=fig_lines,
                                 widths=widths, heights=heights)
        #
        self.crs = self.buildcrs()

    def scatter_on_page(self, figs):
        """ Try to optimize nb of columns and lines, based on figs
        list length
        """
        n = len(figs)
        if n in range(1, 4):
            nx, ny = 1, n
        elif n == 4:
            nx, ny = 2, 2
        elif n in range(5, 7):
            nx, ny = 2, 3
        elif n in range(7, 9):
            nx, ny = 2, 4
        elif n in range(9, 13):
            nx, ny = 3, 4
        elif n in range(13, 16):
            nx, ny = 3, 5
        elif n in range(16, 21):
            nx, ny = 4, 5
        elif n in range(21, 25):
            nx, ny = 4, 6
        elif n in range(25, 36):
            nx, ny = 5, 7
        elif n in range(36, 49):
            nx, ny = 6, 8
        else:
            raise Climaf_Classes_Error("Too many figures in page")
        figs.extend([None] * (nx * ny - len(figs) + 1))
        lines = [figs[x: x + nx] for x in range(0, nx * ny, nx)]
        self.fig_lines = lines
        self.widths = [round(1. / nx, 2)] * nx
        self.heights = [round(1. / ny, 2)] * ny

    def buildcrs(self, crsrewrite=None, period=None):
        rep = super(cpage, self).buildcrs(crsrewrite=crsrewrite, period=period)
        param = "%s,%s, fig_trim='%s', page_trim='%s', format='%s', page_width=%d, page_height=%d" % \
            (repr(self.widths), repr(self.heights), self.fig_trim, self.page_trim, self.format, self.page_width,
             self.page_height)
        if isinstance(self.title, six.string_types) and len(self.title) != 0:
            param = "%s, title='%s', x=%d, y=%d, ybox=%d, pt=%d, font='%s', gravity='%s', backgroud='%s', " \
                "insert='%s', insert_width=%d" % (param, self.title, self.x, self.y, self.ybox, self.pt, self.font,
                                                  self.gravity, self.background, self.insert, self.insert_width)
        rep = "cpage([%s],%s)" % (",".join(rep), param)

        return rep


class cpage_pdf(cpage_all):
    def __init__(self, fig_lines=None, widths=None, heights=None,
                 orientation=None, page_width=1000., page_height=1500.,
                 scale=1., openright=False,
                 title="", x=0, y=2, titlebox=False, pt="Huge",
                 font="\\familydefault", background="white"):
        """
        Builds a CliMAF cpage_pdf object, which represents an array of figures (output:
        'pdf' figure). Figures are automatically centered in the page using 'pdfjam' tool; see
        http://www2.warwick.ac.uk/fac/sci/statistics/staff/academic-research/firth/software/pdfjam

        Args:
          fig_lines (a list of lists of figure objects or an ensemble of figure objects):
           each sublist of 'fig_lines' represents a line of figures
          widths (list, optional): the list of figure widths, i.e. the width of each
           column. By default, if fig_lines is:

             - a list of lists: spacing is even
             - an ensemble: one column is used
          heights (list, optional): the list of figure heights, i.e. the
           height of each line. By default spacing is even
          page_width (float, optional): width resolution of resultant image;
           CLiMAF default: 1000.
          page_height (float, optional): height resolution of resultant image;
           CLiMAF default: 1500.
          orientation (str,optional): if set, it supersedes page_width and
           page_height with values 1000*1500 (for portrait) or 1500*1000 (for landscape)
          scale (float, optional): to scale all input pages; default:1.
          openright (logical, optional): this option puts an empty figure before the
           first figure; default: False. For more details, see:
           http://ftp.oleane.net/pub/CTAN/macros/latex/contrib/pdfpages/pdfpages.pdf
          title (str, optional): append a label in the page.

        If title is activated, it is by default horizontally centered:

            - x (int, optional): title horizontal shift (in cm).
            - y (int, optional): vertical shift from the top of the page (in cm);
              only positive (down) values have an effect, default=2 cm
            - titlebox (logical, optional): set it to True to frame the text in a box,
              frame color is 'black'
            - pt (str, optional): title font size; CLiMAF default: 'Huge'
              (corresponding to 24 pt). You can set or not a backslash before this
              argument.
            - font (str, optional): font
              abbreviation among available LaTex fonts; default: '\\\\\\\\familydefault'.
            - background (str, optional): frame fill background color; among LaTex
              'fcolorbox' colors; default: 'white'.

        Left and right margins are set to 2cm.

        Example:

         Using no default value, to create a PDF page with 2 columns and 3 lines::

          >>> tas_ds=ds(project='example',simulation='AMIPV6ALB2G', variable='tas', period='1980-1981')
          >>> tas_avg=time_average(tas_ds)
          >>> fig=plot(tas_avg,title='title',format='pdf')
          >>> crop_fig=cpdfcrop(fig)
          >>> my_pdfpage=cpage_pdf([[crop_fig,crop_fig],[crop_fig, crop_fig],[crop_fig,crop_fig]],
          ... widths=[0.2,0.8], heights=[0.33,0.33,0.33], page_width=800., page_height=1200.,
          ... scale=0.95, openright=True, title='Page title', x=-5, y=10, titlebox=True,
          ... pt='huge', font='ptm', background='yellow') # Font name is 'Times'
        """
        super(cpage_pdf, self).__init__(fig_lines=fig_lines, orientation=orientation, page_width=page_width,
                                        page_height=page_height, title=title, x=x, y=y)
        self.scale = scale
        self.openright = openright
        self.titlebox = titlebox
        self.pt = pt
        self.font = font
        self.background = background
        if not isinstance(fig_lines, (list, cens)):
            raise Climaf_Classes_Error("fig_lines must be a CliMAF ensemble or a list "
                                       "of lists (each representing a line of figures)")
        elif isinstance(fig_lines, list):
            self.check_figs_list(fig_lines=fig_lines,
                                 widths=widths, heights=heights)
        else:  # case of an ensemble (cens)
            self.check_figs_cens(fig_lines=fig_lines,
                                 widths=widths, heights=heights)
        #
        self.crs = self.buildcrs()

    def buildcrs(self, crsrewrite=None, period=None):
        rep = super(cpage_pdf, self).buildcrs(
            crsrewrite=crsrewrite, period=period)
        param = "%s,%s, page_width=%d, page_height=%d, scale=%.2f, openright='%s'" % \
            (repr(self.widths), repr(self.heights), self.page_width,
             self.page_height, self.scale, self.openright)
        if isinstance(self.title, six.string_types) and len(self.title) != 0:
            param = "%s, title='%s', x=%d, y=%d, titlebox='%s', pt='%s', font='%s', backgroud='%s'" % \
                (param, self.title, self.x, self.y, self.titlebox,
                 self.pt, self.font, self.background)
        rep = "cpage_pdf([%s],%s)" % (",".join(rep), param)

        return rep


def guess_projects(crs):
    """
    Return the list of projects involved in the datasets involved in a
    CRS expression.
    """

    def guess_project(crs):
        """
        Guess which is the project name for a dataset's crs, with minimum
        assumption on the separator used in the project
        """
        separators = [r'.', r'_', r'£', r'$', r'@', r'_', r'|', r'&', r"-", r"=", r"^",
                      r";", r":", r"!", r'§', r'/', r'.', r'ø', r'+', r'°']
        counts = dict()
        for sep in separators:
            counts[sep] = crs.count(sep)
        # Assume that the highest count gives the right separator
        max = 0
        for key in counts:
            if counts[key] >= max:
                max = counts[key]
                sep = key
        return crs[1:crs.find(sep)]

    return list(map(guess_project, re.findall(r"ds\(([^)]*)", crs)))


def browse_tree(cobj, func, results):
    """ Browse a CliMAF object's tree, accumulating in 'results' the
    values returned by 'func' on each tree node or leave (if they are
    not None)
    """
    if isinstance(cobj, cdataset) or isinstance(cobj, cdummy):
        res = func(cobj)
        if res:
            partial.append(res)
    elif isinstance(cobj, ctree):
        res = func(cobj.operator)
        if res:
            partial.append(res)
        for op in cobj.operands:
            browse_tree(op, func, partial)
    elif isinstance(cobj, scriptChild):
        browse_tree(cobj.father, func, partial)
    elif isinstance(cobj, cpage):
        for line in cobj.fig_lines:
            list(map(lambda x: browse_tree(x, func, partial), line))
    elif cobj is None:
        return
    else:
        clogger.error("Cannot yet handle object :%s", repr(cobj))
        return


def domainOf(cobject):
    """ Returns a domain for a CliMAF object : if object is a dataset, returns
    its domain, otherwise returns domain of first operand
    """
    if isinstance(cobject, cdataset):
        if isinstance(cobject.domain, list):
            rep = ""
            for coord in cobject.domain[0:-1]:
                rep = r"%s%d," % (rep, coord)
            rep = "%s%d" % (rep, cobject.domain[-1])
            return rep
        else:
            if cobject.domain == "global":
                return ""
            else:
                return cobject.domain
    elif isinstance(cobject, ctree):
        clogger.debug(
            "For now, domainOf logic for scripts output is basic (1st operand) - TBD")
        return domainOf(cobject.operands[0])
    elif isinstance(cobject, scriptChild):
        clogger.debug(
            "For now, domainOf logic for scriptChilds is basic - TBD")
        return domainOf(cobject.father)
    elif isinstance(cobject, cens):
        clogger.debug(
            "for now, domainOf logic for 'cens' objet is basic (1st member)- TBD")
        return domainOf(list(cobject.values())[0])
    elif cobject is None:
        return "none"
    else:
        if cobject != "":
            clogger.error("Unkown class for argument " + repr(cobject))


def varOf(cobject):
    return attributeOf(cobject, "variable")


def modelOf(cobject):
    return attributeOf(cobject, "model")


def simulationOf(cobject):
    return attributeOf(cobject, "simulation")


def experimentOf(cobject):
    return attributeOf(cobject, "experiment")


def realizationOf(cobject):
    return attributeOf(cobject, "realization")


def projectOf(cobject):
    return attributeOf(cobject, "project")


def realmOf(cobject):
    return attributeOf(cobject, "realm")


def gridOf(cobject):
    return attributeOf(cobject, "grid")


def attributeOf(cobject, attrib):
    """ Returns the attribute for a CliMAF object : if object is a dataset, returns
    its attribute property, otherwise returns attribute of first operand
    """
    if isinstance(cobject, cdataset):
        val = getattr(cobject, attrib, None)
        if val is not None:
            return val
        else:
            return cobject.kvp.get(attrib)
    elif isinstance(cobject, cens):
        return attributeOf(list(cobject.values())[0], attrib)
    elif getattr(cobject, attrib, None):
        value = getattr(cobject, attrib)
        clogger.debug("Find value for object's %s... %s" % (attrib, value))
        return value
    elif isinstance(cobject, ctree):
        clogger.debug("for now, varOf logic is basic (1st operand) - TBD")
        # TODO: Check which operands in the correct one
        value = getattr(cobject, attrib, None)
        if value is None:
            value = attributeOf(cobject.operands[0], attrib)
            clogger.debug("Find value for current first operand... %s" % value)
            return value
        else:
            clogger.debug("Find value for current object... %s" % value)
            return value
    elif isinstance(cobject, cdummy):
        return "dummy"
    elif isinstance(cobject, cpage) or isinstance(cobject, cpage_pdf):
        return None
    elif cobject is None or cobject == '':
        return ''
    else:
        raise Climaf_Classes_Error(
            "Unknown class for argument " + repr(cobject))


def timePeriod(cobject):
    """ Returns a time period for a CliMAF object : if object is a dataset, returns
    its time period, otherwise analyze complex case and reurns something sensible
    """
    if isinstance(cobject, cdataset):
        return cobject.period
    elif isinstance(cobject, ctree):
        clogger.debug("timePeriod : processing %s,operands=%s" %
                      (cobject.script, repr(cobject.operands)))
        if cobject.script.flags.doCatTime and len(cobject.operands) > 1:
            clogger.debug(
                "Building composite period for results of %s" % cobject.operator)
            periods = [timePeriod(op) for op in cobject.operands]
            merged_period = merge_periods(periods)
            if len(merged_period) > 1:
                raise Climaf_Driver_Error("Issue when time assembling with %s, periods are not consecutive : %s" %
                                          (cobject.operator, merged_period))
            return merged_period[0]
        else:
            clogger.debug(
                "timePeriod logic for script is 'choose 1st operand' %s" % cobject.script)
            return timePeriod(cobject.operands[0])
    elif isinstance(cobject, scriptChild):
        clogger.debug(
            "for now, timePeriod logic for scriptChilds is basic - TBD")
        return timePeriod(cobject.father)
    elif isinstance(cobject, cens):
        clogger.debug(
            "for now, timePeriod logic for 'cens' objet is basic (1st member)- TBD")
        return timePeriod(list(cobject.values())[0])
    else:
        return None  # clogger.error("unkown class for argument "+`cobject`)


def resolve_star_period(kwargs):

    # If dict 'kwargs' has only kw 'period' with value '*', resolve
    # corresponding dataset on period, and sets kwargs['period']
    # accordingly (if dataset has only one corresponding period)

    if 'period' in kwargs and kwargs['period'] == '*' and \
       not any(["*" in kwargs[k] or "?" in kwargs[k] for k in kwargs if k != 'period']):
        explorer = cdataset(** select_projects(** kwargs))
        attributes = explorer.explore(option='choices')
        if 'period' in attributes:
            periods = attributes['period']
            if len(periods) == 1:
                kwargs['period'] = str(periods[0])
                return True
    return False


def resolve_first_or_last_years(kwargs, duration, option="last"):
    # Returns a dataset after translation of period like 'last_50y'
    kwargs['period'] = '*'
    explorer = ds(**kwargs)
    attributes = explorer.explore(option='choices')
    if 'period' in attributes:
        periods = attributes['period']
        if option == 'last':
            period = periods[-1]
            kwargs['period'] = lastyears(period, int(duration))
        if option == 'first':
            period = periods[0]
            kwargs['period'] = firstyears(period, int(duration))
    else:
        kwargs['period'] = '*'
    explorer = ds(**kwargs)
    return explorer.explore('resolve')


def test():
    #    clogger.basicConfig(level=clogger.DEBUG)
    #    clogger.basicConfig(format='"%(asctime)s [%(funcName)s: %(filename)s,%(lineno)d] %(message)s : %(levelname)s',
    #                        level=clogger.DEBUG)
    cdef("project", "CMIP5")
    # cdef("project","PR6")
    cdef("model", "CNRM-CM5")
    cdef("experiment", "historical")
    cdef("simulation", "r1i1p1")
    cdef("period", "197901-198012")
    cdef("domain", "global")
    #
    tos = cdataset(experiment="rcp85", variable="tos",
                   period="19790101-19790102")
    tr = ctree("operator", tos, para1="val1", para2="val2")
    print(tr)
    # tos.pr()
    #
    # ds1=Dataset(period="1850-2012")
    # genericDataSets(ds1.crs)
    # ds2=Dataset(project="CMIP3")
    # ex="toto("+ ds1.crs + "," + ds2.crs
    # print genericDataSets(ex)
    # print firstGenericDataSet(ex)


def t2():
    p = period("1984-1984")


if __name__ == "__main__":
    test()
