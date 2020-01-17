#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 Basic types and syntax for a CLIMAF Reference Syntax interpreter and driver
 This is a first protoype, where the interpreter is Python itself


"""
# Created : S.Sénési - 2014

import re
import string
import copy
import os.path

import dataloc
from period import init_period, cperiod, merge_periods, intersect_periods_list, lastyears, firstyears
from clogging import clogger, dedent
from netcdfbasics import fileHasVar, varsOfFile, timeLimits, model_id
from decimal import Decimal

#: Dictionary of declared projects (type is cproject)
cprojects = dict()

#: Dictionary of aliases dictionaries
aliases = dict()

#: Dictionary of frequency names dictionaries
frequencies = dict()

#: Dictionary of realms names dictionaries
realms = dict()


class cproject():
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
            raise Climaf_Classes_Error("Character ',' is forbidden as a project separator")
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
        raise Climaf_Classes_Error("project '%s' has not yet been declared" % project)
    if attribute == 'project':
        project = None
    #
    if project and attribute not in cprojects[project].facets:
        raise Climaf_Classes_Error("project '%s' doesn't use facet '%s'" % (project, attribute))
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


class cobject():
    def __init__(self):
        # crs is the string expression defining the object
        # in the CLIMAF Reference Syntax
        self.crs = "void"

    def __str__(self):
        # return "Climaf object : "+self.crs
        return self.buildcrs()

    def __repr__(self):
        return self.buildcrs()

    def register(self):
        pass
        # cobjects[self.crs]=self
        # clogger.debug("Object Created ; crs = %s"%(self.crs))

    def erase(self):
        pass
        # del(cobjects[self.crs])
        # clogger.debug("Object deleted ; crs = %s"%(self.crs))


class cdummy(cobject):
    def __init__(self):
        """
        cdummy class represents dummy arguments in the CRS
        """
        pass

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
                if isinstance(lval, str) and lval.find(sep) >= 0:
                    raise Climaf_Classes_Error(
                        "You cannot use character '%s' when setting '%s=%s' because "
                        "it is the declared separator for project '%s'. "
                        "See help(cproject) for changing it, if needed" % (sep, facet, val, project))
            # print "initalizing facet %s with value"%(facet,val)
    if attval['project'] == 'CMIP5':
        # Allow for a synonym for 'simulation' in CMIP5 : 'member'
        if 'member' in kwargs and kwargs['member'] not in [None, '']:
            attval['simulation'] = kwargs['member']
            clogger.info('Attribute "member" in project CMIP5 has been translated to "simulation"')
        # Special processing for CMIP5 fixed fields : handling redundancy in facets
        if (attval['table'] == 'fx' or attval['period'] == 'fx' or
                attval['simulation'] == 'r0i0p0' or attval['frequency'] == 'fx'):
            attval['table'] = 'fx'
            attval['period'] = 'fx'
            attval['simulation'] = 'r0i0p0'
            attval['frequency'] = 'fx'
    # Special processing for CMIP6  : facet 'simulation' is forbidden (must use 'realization')
    if (attval['project'] == 'CMIP6') and 'simulation' in kwargs and kwargs['simulation'] is not '':
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
    if 'period' in attval and not isinstance(attval['period'], cperiod) and attval['period'] not in ["*",]:
        Climaf_Classes_Error("at end of  process.. : period is not a cperiod")
    return attval


class cdataset(cobject):
    # def __init__(self,project=None,model=None,simulation=None,period=None,
    #             rip=None,frequency=None,domain=None,variable=None,version='last') :
    def __init__(self, **kwargs):
        """
        Create a CLIMAF dataset.

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

        - period : see :py:func:`~climaf.period.init_period`

        - domain : allowed values are either 'global' or a list for
          latlon corners ordered as in : [ latmin, latmax, lonmin,
          lonmax ]

        - variable :  name of the geophysical variable ; this should be :

           - either a variable actually included in the datafiles,

           - or a 'derived' variable (see  :py:func:`~climaf.operators.derive` ),

           - or, an aliased variable name (see :py:func:`~climaf.classes.alias` )

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
            filevar, scale, offset, units, filenameVar, missing = self.alias
            if filevar != self.variable or scale != 1. or offset != 0 or missing:
                raise Climaf_Classes_Error("Cannot alias/scale/setmiss on group variable")
        # Build CliMAF Ref Syntax for the dataset
        self.crs = self.buildcrs()
        #
        self.files = None
        self.local_copies_of_remote_files = None
        self.register()

    def setperiod(self, period):
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
        if type(dic['domain']) is list:
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
                raise Climaf_Classes_Error("Cannot proceed with errata: Cannot resolve ambiguities on %s" % repr(self))
            # CMIP6.CMIP.CNRM-CERFACS.CNRM-ESM2-1.1pctCO2.r1i1p1f2.Emon.expfe.gn.v20181018
            ref = "%s.%s.%s.%s.%s.%s.%s.%s.%s.v%s" % ("CMIP6", res.kvp['mip'],
                                                      res.kvp['institute'], res.kvp['model'], res.kvp['experiment'],
                                                      res.kvp['realization'],
                                                      res.kvp['table'], res.kvp['variable'], res.kvp['grid'],
                                                      res.kvp['version'])
            clogger.warning("Querying errata service %s using %s" % (service, browser))
            os.system("%s %s%s &" % (browser, service, ref))
            # voir le fichier api_errata_Atef.py pour faire mieux
        else:
            clogger.warning("No errata service is yet defined for project %s" % self.project)

    def isLocal(self):
        # return self.baseFiles().find(":")<0
        model = getattr(self, "model", "*")
        return (dataloc.isLocal(project=self.project, model=model, simulation=self.simulation,
                                frequency=self.frequency))

    def isCached(self):
        """ TBD : analyze if a remote dataset is locally cached

        """
        # clogger.error("TBD - remote datasets are not yet cached")
        rep = False
        return rep

    def oneVarPerFile(self):
        locs = dataloc.getlocs(project=self.project, model=self.model, simulation=self.simulation,
                               frequency=self.frequency)
        return all([org for org, freq, url in locs])

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
        if alias is None:
            return True
        _, _, _, _, _, missing = self.alias
        return missing is None

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

          >>> rst=ds(project="CMIP6", model='*', experiment="*ontrol*", realization="r1i1p1f*", table="Amon", variable="rsut", period="1980-1981")
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
          >>> mrst=ds(project="CMIP6", model='*', experiment="piControl", realization="r1i1p1f*", table="Amon", variable="rsut", period="1980-1981")
          >>> mrst.explore('choices')
          {'institute': ['CNRM-CERFACS'], 'mip': ['CMIP'], 'model': ['CNRM-ESM2-1', 'CNRM-CM6-1'], 'grid': ['gr'], 'realization': ['r1i1p1f2']}
          >>> small_ensemble=mrst.explore('ensemble')
          >>> small_ensemble
          cens({
                'CNRM-ESM2-1':ds('CMIP6%%rsut%1980-1981%global%/cnrm/cmip%CNRM-ESM2-1%CNRM-CERFACS%CMIP%Amon%piControl%r1i1p1f2%gr%latest'),
                'CNRM-CM6-1' :ds('CMIP6%%rsut%1980-1981%global%/cnrm/cmip%CNRM-CM6-1%CNRM-CERFACS%CMIP%Amon%piControl%r1i1p1f2%gr%latest')
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

          >>> # What is the overall period covered by the union of all datafiles (but not necessarily by a single model!)
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
        dic = self.kvp.copy()
        if self.alias:
            filevar, _, _, _, filenameVar, _ = self.alias
            req_var = dic["variable"]
            dic["variable"] = string.Template(filevar).safe_substitute(dic)
            if filenameVar:
                dic["filenameVar"] = filenameVar
        clogger.debug("Looking with dic=%s" % repr(dic))
        wildcards = None
        # if option != 'check_and_store' :
        wildcards = dict()
        files = dataloc.selectFiles(return_wildcards=wildcards, merge_periods_on=group_periods_on, **dic)
        # -- Use the requested variable instead of the aliased
        if self.alias:
            dic["variable"] = req_var
        # if option != 'check_and_store' :
        periods = wildcards.get('period', None)
        # else : periods=None
        if periods:
            # print "periods=",periods
            if option != 'choices':
                if group_periods_on:
                    raise Climaf_Classes_Error("Can use 'group_periods_on' only with option='choices'")
                if operation != 'intersection':
                    raise Climaf_Classes_Error("Can use operation %s only with option='choices'" % operation)
            if operation == 'intersection':
                if group_periods_on:
                    # print "periods=",periods
                    merged_periods = [merge_periods(p) for p in periods.values()]
                    inter = merged_periods.pop(0)
                    for p in merged_periods:
                        inter = intersect_periods_list(inter, p)
                else:
                    inter = merge_periods(periods[None])
                wildcards['period'] = inter
            elif operation == 'union':
                to_merge = []
                for plist in periods.values():
                    to_merge.extend(plist)
                wildcards['period'] = merge_periods(to_merge)
            elif operation is None:
                # Merge periods for each facet value separately
                if group_periods_on:
                    for key in periods:
                        periods[key] = merge_periods(periods[key])
                wildcards['period'] = periods
            else:
                raise Climaf_Classes_Error("Operation %s is not kown " % operation)
        #
        wildcard_attributes_list = [k for k in dic if type(dic[k]) is str and "*" in dic[k]]
        if option == 'resolve':
            clogger.debug("Trying to resolve on attributes %s" % wildcard_attributes_list)
            for kw in wildcards:
                val = wildcards[kw]
                if type(val) == list:
                    if len(val) > 1:
                        if kw == 'period':
                            raise Climaf_Classes_Error("Periods with holes are not handled %s" % val)
                        else:
                            raise Climaf_Classes_Error("Wildcard attribute %s is ambiguous %s" % (kw, val))
                    else:
                        val = val[0]
                        dic[kw] = val
                else:
                    if kw == 'variable':  # Should take care of aliasing to fileVar
                        matching_vars = set()
                        paliases = aliases.get(self.project, [])
                        for variable in paliases:
                            if val == paliases[variable][0]:
                                matching_vars.add(variable)
                        if len(matching_vars) == 0:
                            # No filename variable in aliases matches actual filename
                            dic[kw] = val
                        elif len(matching_vars) == 1:
                            # One variable has a filename variable whih matches the retrieved filename
                            dic[kw] = matching_vars.pop()
                        else:
                            raise Climaf_Classes_Error("Filename variable %s is matched by multiple variables %s" %
                                                       (val, repr(matching_vars)))
                    else:
                        dic[kw] = val
            #
            return ds(**dic)
        elif option == 'choices':
            clogger.debug("Listing possible values for these wildcard attributes %s" % wildcard_attributes_list)
            self.files = files
            return wildcards
        elif option == 'ensemble':
            clogger.debug("Trying to create an ensemble on attributes %s" % wildcard_attributes_list)
            is_ensemble = False
            for kw in wildcards:
                entry = wildcards[kw]
                # print "entry=",entry, 'type=',type(entry), 'ensemble_kw=',ensemble_kw
                if kw == 'period' and type(entry) is list:
                    if len(wildcards['period']) > 1:
                        raise \
                            Climaf_Classes_Error(
                                "Cannot create an ensemble with holes in period (%s)" % wildcards['period'])
                    entry = entry[0]
                if type(entry) is list:
                    is_ensemble = (len(entry) > 1)
                dic[kw] = entry
            if is_ensemble is False:
                # raise Climaf_Classes_Error("Creating an ensemble does not make sense because all wildcard "+\
                #                           "attributes have a single possible value (%s)"%wildcards)
                clogger.warning("Creating an ensemble with a single member")
            self.files = files
            return eds(first=first, **dic)
        elif option == 'check_and_store':
            for kw in wildcards:
                entry = wildcards[kw]
                if type(entry) is list and len(entry) > 1:
                    raise Climaf_Classes_Error("This dataset is ambiguous on attribute %s='%s'; please choose among :"
                                               " %s or use either 'ensure_dataset=False' (with method baseFiles or "
                                               "listfiles) or 'option=\'choices\' (with method explore)" %
                                               (kw, dic[kw], entry))
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
                self.explore()
            else:
                self.explore(option='choices')
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

    def check(self):
        """
        Check time consistency of first variable of a dataset or ensemble members:
        - check if first data time interval is consistent with dataset frequency
        - check if file data have a gap
        - check if period covered by data files actually includes the whole of dataset period

        Returns: True if period of data files included dataset period, False otherwise.

        Examples:

        >>> # Dataset with monthly frequency
        >>> tas=ds(project='example', simulation='AMIPV6ALB2G', variable='tas',period='1980-1981')
        >>> res1=tas.check()
        >>>
        >>> # Ensemble with monthly frequency
        >>> j0=ds(project='example',simulation='AMIPV6ALB2G', variable='tas', frequency='monthly', period='1980')
        >>> j1=ds(project='example',simulation='AMIPV6ALB2G', variable='tas', frequency='monthly', period='1981')
        >>> ens=cens({'1980':j0, '1981':j1})
        >>> res2=ens.check()

        >>> # Define a new project for 'em' data with 3 hours frequency in particular
        >>> cproject('em_3h','root','group','realm','frequency',separator='|')
        >>> path='/cnrm/cmip/cnrm/simulations/${group}/${realm}/Regu/${frequency}/${simulation}/${variable}_??_YYYY.nc'
        >>> dataloc(project='em_3h', organization='generic', url=path)

        >>> # Dataset with 3h frequency for 'tas' variable (instant)
        >>> tas_3h=ds(project='em_3h',variable='tas',group='AR4',realm='Atmos',frequency='3Hourly', simulation='A1B',period='2050-2100')
        >>> res3=tas_3h.check()

        >>> # Dataset with 3h frequency for 'pr' variable (time mean)
        >>> pr_3h=ds(project='em_3h',variable='pr',group='AR4',realm='Atmos',frequency='3Hourly', simulation='A1B',period='2050-2100')
        >>> res4=pr_3h.check()

        """
        from anynetcdf import ncf
        from datetime import datetime, timedelta
        from netCDF4 import num2date
        import numpy as np

        # Returns the list of files which include the data for the dataset
        # or for each member of the ensemble
        if isinstance(self, cdataset):
            if self.isLocal() or self.isCached():
                files = self.baseFiles()
            else:
                files = self.local_copies_of_remote_files
            if not files:
                clogger.error('No file found for: %s' % self)
                if not (self.isLocal() or self.isCached()):
                    clogger.warning('For remote data, you have to do at first "cfile(%s)"' % self)
                return False
        else:
            clogger.error("Cannot handle %s" % self)
            return
        #
        if files:
            filedate = []
            clogger.debug("List of selected files: %s" % files)

            var = str.split(varOf(self), ',')[0]
            # Concatenate all data files
            for filename in str.split(files, ' '):
                fileobj = ncf(filename)
                #
                if self.project in aliases and var in aliases[self.project]:
                    var = aliases[self.project][var][0]
                #
                dimname = ''
                for dim in fileobj.variables[var].dimensions:
                    if 'time' in dim:
                        dimname = dim
                if not dimname:
                    clogger.error('No time dimension for variable %s' % var)
                time_obj = fileobj.variables[dimname]
                filedate = np.concatenate((filedate, num2date(time_obj.getValue(), units=time_obj.units,
                                                              calendar=time_obj.calendar)))

            clogger.debug('Time data of selected files: %s' % filedate)

            # Check if first data time interval is consistent with dataset frequency
            if len(filedate) > 1:
                filedate_delta = (filedate[1] - filedate[0]).total_seconds()
            else:
                clogger.error('Time dimension is degenerated.')
                return

            if ((self.frequency == 'monthly' or not self.frequency)
                and (filedate_delta > 31. * 24. * 3600 or filedate_delta <= 29. * 24. * 3600.))\
                    or (self.frequency == 'yearly' and
                        (filedate_delta > 366. * 24. * 3600. or filedate_delta < 365. * 24. * 3600.))\
                    or (self.frequency == 'decadal' and
                        (filedate_delta > 3653. * 24. * 3600. or filedate_delta < 3651. * 24. * 3600.)):

                clogger.warning(
                    'First data time interval (= %.1f days) is not consistent with dataset frequency (i.e. %s)'
                    % (filedate_delta / (24. * 3600.), self.frequency))

            elif self.frequency == 'daily' and filedate_delta != 86400.:
                clogger.warning(
                    'First data time interval (= %.2f hours) is not consistent with dataset frequency (i.e. %s)'
                    % (filedate_delta / 3600., self.frequency))

            elif (self.frequency == '6h' or self.frequency == '3h' or self.frequency == '1h'
                  or self.frequency == '3Hourly' or self.frequency == '6Hourly') \
                    and filedate_delta != float(self.frequency[0]) * 3600.:
                clogger.warning('First data time interval (= %.2f hours) is different to dataset frequency (i.e. %.2f)'
                                % (filedate_delta / 3600., float(self.frequency[0])))

            # Check if file data have a gap
            i = 0
            cpt = 0
            while i < len(filedate) - 2:
                i += 1
                if (filedate[i + 1] - filedate[i]).total_seconds() != filedate_delta:
                    cpt += 1
                    if cpt < 5:
                        if self.frequency == 'monthly' or not self.frequency or \
                                self.frequency == 'yearly' or self.frequency == 'decadal':
                            clogger.error('File data have a gap between indexes %i and %i: delta = %.0f days '
                                          % (i, i + 1, (filedate[i + 1] - filedate[i]).total_seconds() / (24. * 3600.))
                                          + 'instead of %.0f days (<=> 1st data interval)'
                                          % (filedate_delta / (24. * 3600.)))
                        elif self.frequency == 'daily' or self.frequency == '6h' or \
                                self.frequency == '3h' or self.frequency == '1h' or \
                                self.frequency == '3Hourly' or self.frequency == '6Hourly':
                            clogger.error('File data have a gap between indexes %i and %i: ' % (i, i + 1) +
                                          'delta = %.0f hours instead of %.0f hours (<=> 1st data interval)'
                                          % ((filedate[i + 1] - filedate[i]).total_seconds() / 3600.,
                                             filedate_delta / 3600.))
            #
            # Compute period covered by data files
            if self.frequency == 'monthly' or not self.frequency:
                filedate[0] = filedate[0].replace(day=01)
                if filedate[-1].month > 11:
                    filedate[-1] = filedate[-1].replace(year=filedate[-1].year + 1)
                    filedate[-1] = filedate[-1].replace(month=01)
                    filedate[-1] = filedate[-1].replace(day=01)
                else:
                    filedate[-1] = filedate[-1].replace(month=filedate[-1].month + 1)
                    filedate[-1] = filedate[-1].replace(day=01)

            elif self.frequency == 'daily':
                filedate[0] = filedate[0].replace(hour=00)
                filedate[-1] = filedate[-1].replace(hour=00)
                filedate[-1] = filedate[-1] + timedelta(days=1)

            elif self.frequency == '6h' or self.frequency == '3h' or self.frequency == '1h' \
                    or self.frequency == '3Hourly' or self.frequency == '6Hourly':

                if 'cell_methods' in fileobj.variables[var].__dict__:  # time mean

                    regex = re.compile('.*time *: *mean *\(? *interval *: *([0-9]+.?[0-9]+?) ([a-zA-Z]+) *\)')
                    cell_meth_att = regex.search(fileobj.variables[var].cell_methods)
                    if cell_meth_att:
                        if cell_meth_att.group(2) == 'hours':
                            freq = float(cell_meth_att.group(1))
                        elif cell_meth_att.group(2) == 'minutes':
                            freq = float(cell_meth_att.group(1)) / 60.
                    else:  # 'cell_methods' attribute defined with the value 'time: mean'
                        freq = filedate_delta / 3600.

                    filedate[0] = filedate[0] - timedelta(minutes=(freq / 2.) * 60 +
                                                                  ((filedate[0].hour * 60 + filedate[0].minute) -
                                                                   (freq / 2.) * 60) % (freq * 60))
                    filedate[-1] = filedate[-1] - timedelta(minutes=(freq / 2.) * 60 +
                                                                    ((filedate[-1].hour * 60 + filedate[-1].minute) -
                                                                     (freq / 2.) * 60) % (freq * 60) - freq * 60)

                else:  # assume it is instant data
                    freq = filedate_delta / 3600.
                    filedate[-1] = filedate[-1] - timedelta(minutes=(freq / 2.) * 60 +
                                                                    ((filedate[-1].hour * 60 + filedate[-1].minute) -
                                                                     (freq / 2.) * 60) % (freq * 60) - 2 * freq * 60)

            elif self.frequency == 'yearly' or self.frequency == 'decadal':
                filedate[0] = filedate[0].replace(month=01)
                filedate[0] = filedate[0].replace(day=01)
                filedate[-1] = filedate[-1].replace(month=01)
                filedate[-1] = filedate[-1].replace(day=01)
                filedate[-1] = filedate[-1] + timedelta(years=1)

            elif self.frequency == 'fx' or self.frequency == 'annual_cycle':
                clogger.error('Check time consistency with a frequency equal to %s has no sense' % self.frequency)

            else:
                clogger.error('Dataset frequency is non-standard: frequency = %s. ' % self.frequency +
                              'Normalized frequency values are: decadal, yearly, monthly, ' +
                              'daily, 6h, 3h, fx and annual_cycle')
            #
            # Check period of datafiles vs dataset period
            clogger.debug('Period covered by selected files: %s' % filedate)
            file_period = cperiod(start=filedate[0], end=filedate[-1])
            #
            if file_period.includes(self.period):
                clogger.info("Time data in datafiles (i.e. %s) includes time data of " % file_period +
                             "dataset (i.e. %s) => dataset are consistent." % self.period)
                return True
            else:
                clogger.info("Time data in datafiles (i.e. %s) don't include time data of " % file_period +
                             "dataset (i.e. %s) => dataset are not consistent." % self.period)
                return False


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
        if not all(map(lambda x: isinstance(x, str), dic.keys())):
            raise Climaf_Classes_Error("Ensemble keys/labels must be strings")
        if not all(map(lambda x: isinstance(x, cobject), dic.values())):
            raise Climaf_Classes_Error("Ensemble members must be CliMAF objects")
        self.sortfunc = sortfunc
        #
        dict.update(self, dic)
        #
        keylist = self.keys()
        try:
            from natsort import natsorted
            keylist = natsorted(keylist)
        except:
            keylist.sort()
        if order:
            self.set_order(order, keylist)
        elif sortfunc:
            self.order = sortfunc(keylist)
        else:
            self.order = keylist
        #
        self.crs = self.buildcrs()
        self.register()

    def set_order(self, order, ordered_keylist=None):
        ordered_list = [o for o in order]
        ordered_list.sort()
        if ordered_keylist is None:
            ordered_keylist = [o for o in self]
            ordered_keylist.sort()
        if ordered_list != ordered_keylist:
            raise Climaf_Classes_Error(
                "Labels list (as described by order list) does not match ensemble labels list : %s   and %s" %
                (repr(ordered_list), repr(ordered_keylist)))
        self.order = order

    def __setitem__(self, k, v):
        if not isinstance(k, str):
            raise Climaf_Classes_Error("Ensemble keys/labels must be strings")
        if not isinstance(v, cobject):
            raise Climaf_Classes_Error("Ensemble members must be CliMAF objects")
        dict.__setitem__(self, k, v)
        if k not in self.order:
            self.order.append(k)
            if self.sortfunc:
                self.order = self.sortfunc(self.keys())
        self.crs = self.buildcrs()
        self.register()

    def items(self):
        return [(l, self[l]) for l in self.order]

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
            for el, val in it.items():
                self.order.append(el)
        else:
            for el, val in it:
                self.order.append(el)
        if self.sortfunc:
            self.order = self.sortfunc(self.keys())

    def buildcrs(self, crsrewrite=None, period=None):
        rep = "cens({"
        for m in self.order:
            rep += "'" + m + "'" + ":" + self[m].buildcrs(crsrewrite=crsrewrite, period=period) + ","
        rep = rep + "}"
        rep = rep.replace(",}", "}")
        rep = rep + ")"
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
                raise Climaf_Classes_Error("Attribute %s cannot be used for ensemble" % attr)
            clogger.debug("Attr %s is used for an ensemble" % attr)
            nlist += 1
            listattr.append(attr)
    if len(listattr) < 1:
        raise Climaf_Classes_Error("For building an ensemble, must have at least one attribute which is a list")
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
        listattr2 = [l for l in listattr]
        if first is not None:
            listattr2.remove(first)
            att = first
        else:
            # Use the first attributes declared as ensemble-prone for the project
            for a in cprojects[attval["project"]].attributes_for_ensemble:
                print "Checkin listattribute", a, "against", listattr2
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
                    l = [e for e in c]
                    l.append((att, v))
                    newcomb.append(l)
            comb = newcomb
        orderl = []
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

    The following restriction apply to such datasets :

    - functions :py:func:`~climaf.classes.calias` and
      :py:func:`~climaf.operators.derive` cannot be used for project
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
                raise Climaf_Classes_Error("No variable %s in file %s" % (v, filename))
    #
    fperiod = timeLimits(filename)
    if period is None:
        if fperiod is None:
            raise Climaf_Classes_Error("Must provide a period for file %s " % filename)
        else:
            period = repr(fperiod)
    else:
        if fperiod and not fperiod.includes(init_period(period)):
            raise Climaf_Classes_Error("Max period from file %s is %s" % (filename, repr(fperiod)))
    #
    d = ds(project='file', model=model, simulation=simulation,
           variable=variable, period=period, path=filename)
    d.files = filename
    return d


class ctree(cobject):
    def __init__(self, climaf_operator, script, *operands, **parameters):
        """ Builds the tree of a composed object, including a dict for outputs.

        """
        self.operator = climaf_operator
        self.script = script
        import copy
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
                raise Climaf_Classes_Error("operand " + repr(o) + " is not a CliMAF object")
        self.crs = self.buildcrs()
        self.outputs = dict()
        self.register()

    def buildcrs(self, crsrewrite=None, period=None):
        """ Builds the CRS expression representing applying OPERATOR on OPERANDS with PARAMETERS.
        Forces period downtree if provided
        A function for rewriting operand's CRS may be provided
        """
        # Operators are listed in alphabetical order; parameters too
        rep = self.operator + "("
        #
        ops = [o for o in self.operands]
        for op in ops:
            if op:
                opcrs = op.buildcrs(crsrewrite=crsrewrite, period=period)
                if crsrewrite:
                    opcrs = crsrewrite(opcrs)
                rep += opcrs + ","
        #
        clefs = self.parameters.keys()
        clefs.sort()
        for par in clefs:
            if par != 'member_label':  # and self.parameters[par] is not None:
                rep += par + "=" + repr(self.parameters[par]) + ","
        rep += ")"
        rep = rep.replace(",)", ")")
        clogger.debug("Create crs for ctree: %s" % rep)
        return rep

    def setperiod(self, period):
        """ modifies the period for all datasets of a tree"""
        self.erase()
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
        tmp = self.father.buildcrs(period=period)
        if crsrewrite:
            tmp = crsrewrite(tmp)
        return tmp + "." + self.varname


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
                clogger.debug("Parameters are not coherent: %s/%s" % (tree1.parameters, tree2.parameters))
                return None
    elif isinstance(tree1, scriptChild) and isinstance(tree2, scriptChild):
        clogger.debug("Comparison of two scriptChild...")
        if tree1.varname == tree2.varname:
            clogger.debug("... varnames are coherent: %s" % tree1.varname)
            rep = compare_trees(tree1.father, tree2.father, func, filter_on_operator)
            clogger.debug("... %s" % str(rep))
            return rep
        else:
            clogger.debug("... varnames are not coherent: %s/%s" % (tree1.varname, tree2.varname))
            return None


allow_errors_on_ds_call = True  # False


def allow_error_on_ds(allow=True):
    global allow_errors_on_ds_call
    allow_errors_on_ds_call = allow
    # print ('allow_errors_on_ds_call='+`allow_errors_on_ds_call`)


def select_projects(**kwargs):
    """
    If kwargs['project'] is a list (has multiple values), select_projects loops on the projects
    until it finds a file containing the aliased variable name.
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
            clogger.info('-- File found for project ' + project + ' and ' + repr(wkwargs))
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
            clogger.info('-- No file found for project ' + project + ' and ' + repr(wkwargs))
    return kwargs


def ds(*args, **kwargs):
    """
    Returns a dataset from its full Climate Reference Syntax string. Example ::

     >>> ds('CMIP5.historical.pr.[1980].global.monthly.CNRM-CM5.r1i1p1.mon.Amon.atmos.last')

    Also a shortcut for :py:meth:`~climaf.classes.cdataset`,
    when used with with only keywords arguments. Example ::

     >>> cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',\
              simulation='r2i3p9', domain=[40,60,-10,20], variable='tas', period='1980-1989', version='last')

    In that case, you may use e.g. period='last_50y' to get the last 50 years (or less) of data; but this
    will work only if no dataset's attribute is ambiguous. 'first_50y' also works, similarly

    You must refer to doc at : :py:meth:`~climaf.classes.cdataset`
    """
    if len(args) > 1:
        raise Climaf_Classes_Error("Must provide either only a string or only keyword arguments")
    # clogger.debug("Entering , with args=%s, kwargs=%s"%(`args`,`kwargs`))
    if len(args) == 0:
        match = None
        if 'period' in kwargs and type(kwargs['period']) is str:
            match = re.match("(?P<option>last|LAST|first|FIRST)_(?P<duration>[0-9]*)(y|Y)$", kwargs['period'])
            if match is not None:
                return resolve_first_or_last_years(copy.deepcopy(kwargs), match.group('duration'),
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
        e = "CRS expression %s is ambiguous among projects %s" % (crs, repr(cprojects.keys()))
        if allow_errors_on_ds_call:
            clogger.info(e)
        else:
            raise Climaf_Classes_Error(e)
    elif len(results) == 0:
        e = "CRS expression %s is not valid for any project in %s" % (crs, repr(cprojects.keys()))
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


def calias(project, variable, fileVariable=None, scale=1., offset=0., units=None, missing=None, filenameVar=None):
    """ Declare that in ``project``, ``variable`` is to be computed by
    reading ``filevariable``, and applying ``scale`` and ``offset``;

    Arg ``filenameVar`` allows to tell which fake variable name should be
    used when computing the filename for this variable in this project
    (for optimisation purpose);

    Can tell that a given constant must be interpreted as a missing value

    ``variable`` may be a list. In that case, ``fileVariable`` and
    ``filenameVar``, if provided, should be parallel lists

    `` variable`` can be a comma separated list of variables, in which
    case this tells how variables are grouped in files (it make sense
    to use filenameVar in that case, as this is a xway to provide the
    label which is unique to this grouping of variable; scale, offset
    and missing args must be the same for all variables in that case

    Example ::

    >>> calias('erai','tas','t2m',filenameVar='2T')
    >>> calias('erai','tas_degC','t2m',scale=1., offset=-273.15)  # scale and offset may be provided
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
    if type(variable) is not list:
        variable = [variable]
    if type(filenameVar) is not list:
        filenameVar = [filenameVar]
    if type(fileVariable) is not list:
        fileVariable = [fileVariable]
    if type(units) is not list:
        units = [units]
    for v, u, fv, fnv in zip(variable, units, fileVariable, filenameVar):
        aliases[project][v] = (fv, scale, offset, u, fnv, missing)


def varIsAliased(project, variable):
    """
    Return a n-uplet (fileVariable, scale, offset, filevarName,
    missing) defining how to compute a 'variable' which is not in
    files, for the 'project'
    """
    if project in aliases and variable in aliases[project]:
        return aliases[project][variable]


def cmissing(project, missing, *kwargs):
    """ Declare that in 'project', a given constant must be interpreted
    as a missing value, for a given set of project's attributes values

    Such a declaration must follow all ``calias`` declarations for the
    same project
    """
    pass  # TBD


class cpage(cobject):
    def __init__(self, fig_lines=None, widths=None, heights=None,
                 fig_trim=True, page_trim=True, format="png",
                 orientation=None,
                 page_width=1000., page_height=1500., title="", x=0, y=26, ybox=50, pt=24,
                 font="Times-New-Roman", gravity="North", background="white"):
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
          title (str, optional) : append a label below or above (depending optional
           argument 'gravity') figures in the page.

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
        if fig_lines is None:
            raise Climaf_Classes_Error("fig_lines must be provided")
        self.fig_trim = fig_trim
        self.page_trim = page_trim
        self.format = format
        if orientation is not None:
            if orientation == 'portrait':
                page_width = 1000.
                page_height = 1500.
            else:
                if orientation == 'landscape':
                    page_width = 1500.
                    page_height = 1000.
                else:
                    raise Climaf_Classes_Error(
                        "if set, orientation must be 'portrait' or 'landscape'")
        self.page_width = page_width
        self.page_height = page_height
        self.title = title
        self.x = x
        self.y = y
        self.ybox = ybox
        self.pt = pt
        self.font = font
        self.gravity = gravity
        self.background = background
        if self.ybox < (self.y + self.pt):
            raise Climaf_Classes_Error("Title exceeds the assigned box: ybox<y+pt")
        if not isinstance(fig_lines, list) and not isinstance(fig_lines, cens):
            raise Climaf_Classes_Error(
                "fig_lines must be a CliMAF ensemble or a list "
                "of lists (each representing a line of figures)")
        if isinstance(fig_lines, list):
            if not widths:
                widths = []
                for line in fig_lines:
                    if len(line) != len(fig_lines[0]):
                        raise Climaf_Classes_Error("each line in fig_lines must have same dimension")
                for column in fig_lines[0]:
                    widths.append(round(1. / len(fig_lines[0]), 2))
            self.widths = widths

            if not heights:
                heights = []
                for line in fig_lines:
                    heights.append(round(1. / len(fig_lines), 2))
            self.heights = heights

            if len(fig_lines) != len(self.heights):
                raise Climaf_Classes_Error(
                    "fig_lines must have same size than heights")
            for line in fig_lines:
                if not isinstance(line, list):
                    raise Climaf_Classes_Error(
                        "each element in fig_lines must be a list of figures")
                if len(line) != len(self.widths):
                    raise Climaf_Classes_Error(
                        "each line in fig_lines must have same dimension as "
                        "widths; pb for sublist " + repr(line))
            self.fig_lines = fig_lines
        else:  # case of an ensemble (cens)
            if not widths and not heights:
                self.scatter_on_page([fig_lines[label] for label in fig_lines.order])
            else:
                figs = [fig for fig in fig_lines.order]
                if not widths:
                    widths = [1.]
                self.widths = widths
                if not heights:
                    heights = []
                    for memb in figs:
                        heights.append(round(1. / len(figs), 2))
                self.heights = heights

                self.fig_lines = []
                for l in heights:
                    line = []
                    for c in widths:
                        if len(figs) > 0:
                            line.append(fig_lines[figs.pop(0)])
                        else:
                            line.append(None)

                    self.fig_lines.append(line)
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
        elif n in range(9,13):
            nx, ny = 3, 4
        elif n in range(13, 16):
            nx, ny = 3, 5
        elif n in range(16, 21):
            nx, ny = 4, 5
        elif n >= 21:
            raise Climaf_Classes_Error("Too many figures in page")
        lines = []
        for i in range(len(figs)):
            if i % nx == 0:
                line = []
                lines.append(line)
            line.append(figs[i])
        j = len(line)
        for i in range(j, nx):
            line.append(None)
        self.fig_lines = lines
        self.widths = [round(1. / nx, 2) for i in range(nx)]
        self.heights = [round(1. / ny, 2) for i in range(ny)]

    def buildcrs(self, crsrewrite=None, period=None):
        rep = "cpage(["
        for line in self.fig_lines:
            rep += "["
            for f in line:
                if f:
                    rep += f.buildcrs(crsrewrite=crsrewrite) + ","
                else:
                    rep += repr(None) + ","
            rep += " ],"

        if self.title is "":
            rep += ("]," + repr(self.widths) + "," + repr(self.heights) + ", fig_trim='%s', page_trim='%s', format='"
                    + self.format + "', page_width=%d, page_height=%d)") \
                   % (self.fig_trim, self.page_trim, self.page_width, self.page_height)

        else:
            rep += ("]," + repr(self.widths) + "," + repr(self.heights) +
                    ", fig_trim='%s', page_trim='%s', format='" + self.format +
                    "', page_width=%d, page_height=%d, title='" + self.title +
                    "', x=%d, y=%d, ybox=%d, pt=%d, font='" + self.font +
                    "', gravity='" + self.gravity + "', background='" + self.background + "')") \
                   % (self.fig_trim, self.page_trim, self.page_width, self.page_height, self.x, self.y, self.ybox,
                      self.pt)

        rep = rep.replace(",]", "]")
        rep = rep.replace(", ]", "]")

        return rep


class cpage_pdf(cobject):
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
        if fig_lines is None:
            raise Climaf_Classes_Error("fig_lines must be provided")
        if orientation is not None:
            if orientation == 'portrait':
                page_width = 1000.
                page_height = 1500.
            else:
                if orientation == 'landscape':
                    page_width = 1500.
                    page_height = 1000.
                else:
                    raise Climaf_Classes_Error(
                        "if set, orientation must be 'portrait' or 'landscape'")
        self.page_width = page_width
        self.page_height = page_height
        self.scale = scale
        self.openright = openright
        self.title = title
        self.x = x
        self.y = y
        self.titlebox = titlebox
        self.pt = pt
        self.font = font
        self.background = background
        if not isinstance(fig_lines, list) and not isinstance(fig_lines, cens):
            raise Climaf_Classes_Error(
                "fig_lines must be a CliMAF ensemble or a list "
                "of lists (each representing a line of figures)")
        if isinstance(fig_lines, list):
            if not widths:
                widths = []
                for line in fig_lines:
                    if len(line) != len(fig_lines[0]):
                        raise Climaf_Classes_Error("each line in fig_lines must have same dimension")
                for column in fig_lines[0]:
                    widths.append(round(1. / len(fig_lines[0]), 2))
            self.widths = widths

            if not heights:
                heights = []
                for line in fig_lines:
                    heights.append(round(1. / len(fig_lines), 2))
            self.heights = heights

            if len(fig_lines) != len(self.heights):
                raise Climaf_Classes_Error(
                    "fig_lines must have same size than heights")
            for line in fig_lines:
                if not isinstance(line, list):
                    raise Climaf_Classes_Error(
                        "each element in fig_lines must be a list of figures")
                if len(line) != len(self.widths):
                    raise Climaf_Classes_Error(
                        "each line in fig_lines must have same dimension as "
                        "widths; pb for sublist " + repr(line))
            self.fig_lines = fig_lines
        else:  # case of an ensemble (cens)
            figs = [fig for fig in fig_lines.order]

            if not widths:
                widths = [1.]
            self.widths = widths
            if not heights:
                heights = []
                for memb in figs:
                    heights.append(round(1. / len(figs), 2))
            self.heights = heights

            self.fig_lines = []
            for l in heights:
                line = []
                for c in widths:
                    if len(figs) > 0:
                        line.append(fig_lines[figs.pop(0)])
                    else:
                        line.append(None)

                self.fig_lines.append(line)
        #
        self.crs = self.buildcrs()

    def buildcrs(self, crsrewrite=None, period=None):
        rep = "cpage_pdf(["
        for line in self.fig_lines:
            rep += "["
            for f in line:
                if f:
                    rep += f.buildcrs(crsrewrite=crsrewrite) + ","
                else:
                    rep += repr(None) + ","
            rep += " ],"

        if self.title is "":
            rep += ("]," + repr(self.widths) + "," + repr(self.heights) +
                    "', page_width=%d, page_height=%d, scale=%.2f, openright='%s')") \
                   % (self.page_width, self.page_height, self.scale, self.openright)

        else:
            rep += ("]," + repr(self.widths) + "," + repr(self.heights) +
                    "', page_width=%d, page_height=%d, scale=%.2f, openright='%s', title='"
                    + self.title + "', x=%d, y=%d, titlebox='%s', pt='" + self.pt + "', font='"
                    + self.font + "', background='" + self.background + "')") \
                   % (self.page_width, self.page_height, self.scale, self.openright, self.x, self.y, self.titlebox)

        rep = rep.replace(",]", "]")
        rep = rep.replace(", ]", "]")

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

    return map(guess_project, re.findall(r"ds\(([^)]*)", crs))


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
            map(lambda x: browse_tree(x, func, partial), line)
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
        if type(cobject.domain) is list:
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
        clogger.debug("For now, domainOf logic for scripts output is basic (1st operand) - TBD")
        return domainOf(cobject.operands[0])
    elif isinstance(cobject, scriptChild):
        clogger.debug("For now, domainOf logic for scriptChilds is basic - TBD")
        return domainOf(cobject.father)
    elif isinstance(cobject, cens):
        clogger.debug("for now, domainOf logic for 'cens' objet is basic (1st member)- TBD")
        return domainOf(cobject.values()[0])
    elif cobject is None:
        return "none"
    else:
        clogger.error("Unkown class for argument " + repr(cobject))


def varOf(cobject): return attributeOf(cobject, "variable")


def modelOf(cobject): return attributeOf(cobject, "model")


def simulationOf(cobject): return attributeOf(cobject, "simulation")


def projectOf(cobject): return attributeOf(cobject, "project")


def realmOf(cobject): return attributeOf(cobject, "realm")


def gridOf(cobject): return attributeOf(cobject, "grid")


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
        return attributeOf(cobject.values()[0], attrib)
    elif getattr(cobject, attrib, None):
        value = getattr(cobject, attrib)
        clogger.debug("Find value for object... %s" % value)
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
    elif cobject is None:
        return ''
    else:
        raise Climaf_Classes_Error("Unknown class for argument " + repr(cobject))


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


class Climaf_Classes_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)


class Climaf_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)


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
    tos = cdataset(experiment="rcp85", variable="tos", period="19790101-19790102")
    tr = ctree("operator", tos, para1="val1", para2="val2")
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
