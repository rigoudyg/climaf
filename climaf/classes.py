# -*- coding: iso-8859-1 -*-
""" 
 Basic types and syntax for a CLIMAF Reference Syntax interpreter and driver
 This is a first protoype, where the interpreter is Python itself


 """
# Created : S.Senesi - 2014

import re, string, copy, os.path

import dataloc
from period import init_period, cperiod
from clogging import clogger, dedent
from netcdfbasics import fileHasVar, varsOfFile, timeLimits, model_id
from decimal import Decimal

#: Dictionary of declared projects (type is cproject)
cprojects=dict()

#: Dictionary of aliases dictionaries
aliases=dict()

#: Dictionary of frequency names dictionaries
frequencies=dict()

class cproject():
    def __init__(self,name,  *args, **kwargs) :
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
        however of lower priority than the value set using :py:func:`cdef`

        A project can be declared as having non-standard variable
        names in datafiles, or variables that should undergo re-scaling; see
        :py:func:`~climaf.classes.calias`

        A project can be declared as having non-standard frequency names (this is 
        used when accessing datafiles); see :py:func:`~climaf.classes.cfreqs`)

        """
        if name in cprojects : clogger.warning("Redefining project %s"%name)
        self.project=name
        #
        self.facets=[]
        self.facet_defaults=dict()
        forced=['project','simulation', 'variable', 'period', 'domain']
        for f in forced : self.facets.append(f)
        for a in args :
            if isinstance(a,tuple) :
                facet_name,facet_default=a
                self.facet_defaults[facet_name]=facet_default
            else :
                facet_name=a
            if not facet_name in forced : self.facets.append(facet_name)
        #
        self.separator="."
        if "separator" in kwargs : self.separator=kwargs['separator']
        if "sep"       in kwargs : self.separator=kwargs['sep']
        if self.separator=="," :
            raise Climaf_Classes_Error("Character ',' is forbidden as a project separator")
        cprojects[name]=self
        self.crs=""
        # Build the pattern for the datasets CRS for this cproject
        for f in self.facets : 
            self.crs += "${%s}%s"%(f,self.separator)
        self.crs=self.crs[:-1]
        # Create an attribute hodling the list of facets which are allowed
        # for defining an ensemble, and put a first facet there
        self.attributes_for_ensemble=['simulation']
        if 'ensemble' in kwargs :
            self.attributes_for_ensemble.extend(kwargs["ensemble"])
    def __repr__(self):
        return self.crs
    def crs2ds(self,crs) :
        """ 
        Try to interpret string ``crs`` as the CRS of a dataset for
        the cproject. Return the dataset if OK
        """
        fields=crs.split(self.separator)
        if len(fields) == len(self.facets) :
            if fields[0] == self.project :
                kvp=dict()
                for i,f in enumerate(self.facets) : kvp[f]=fields[i]
                return cdataset(**kvp)

def cdef(attribute,value=None, project=None):
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
    
    if project not in cprojects :
        raise Climaf_Classes_Error("project '%s' has not yet been declared"%project)
    if attribute == 'project' : project=None
    #
    if project and not attribute in cprojects[project].facets :
        raise Climaf_Classes_Error("project '%s' doesn't use facet '%s'"%(project,attribute))
    if value is None :
        rep=cprojects[project].facet_defaults.get(attribute,None)
        if not rep :
            rep=cprojects[None].facet_defaults.get(attribute,"N/A")
        return rep
    else :
        cprojects[project].facet_defaults[attribute]=value
            

cproject(None)
cdef("domain","global")


# All Cobject instances are registered in this directory :
cobjects=dict()

class cobject():
    def __init__(self):
        # crs is the string expression defining the object 
        # in the CLIMAF Reference Syntax
        self.crs="void"
    def __str__(self):
        #return "Climaf object : "+self.crs
        return self.buildcrs()
    def __repr__(self):
        return self.buildcrs()
    def register(self):
        cobjects[self.crs]=self
        #clogger.debug("Object Created ; crs = %s"%(self.crs))
    def erase(self):
        del(cobjects[self.crs])
        clogger.debug("Object deleted ; crs = %s"%(self.crs))

def processDatasetArgs(**kwargs) :
    """
    Perfom basic checks on kwargs for functions cdataset and eds
    regarding the project where the dataset is defined
    Also complement with default values as handled by the
    project's definition and by cdef()
    """
    if 'project' in kwargs : project=kwargs['project']
    else : project= cdef("project")
    if project is None :
        raise Climaf_Classes_Error("Must provide a project (Can use cdef)")
    elif project not in cprojects :
        raise Climaf_Classes_Error(
            "Dataset's project '%s' has not "
            "been described by a call to cproject()"%project)
    attval=dict()
    attval["project"]=project
    sep=cprojects[project].separator
    #
    # Register facets values
    for facet in cprojects[project].facets :
        if facet in kwargs and kwargs[facet] : val=kwargs[facet]
        else: val=cdef(facet,project=project)
        attval[facet]=val
        if val :
            if isinstance(val,list) : listval=val
            else : listval=[val]
            for lval in listval :
                if isinstance(lval,str) and lval.find(sep) >= 0 :
                    Climaf_Classes_Error(
                        "You cannot use character '%s' when setting '%s=%s' because "
                        "it is the declared separator for project '%s'. "
                        "See help(cproject) for changing it, if needed"%(sep,facet,val,project))
            #print "initalizing facet %s with value"%(facet,val)
    # Special processing for CMIP5 fixed fields : handling redundancy in facets
    if (attval['project'] == 'CMIP5'):
        if ( attval['table']=='fx' or attval['period']=='fx' or 
             attval['simulation']=='r0i0p0' or attval['frequency']=='fx') :
            attval['table']='fx' ; attval['period']='fx' 
            attval['simulation']='r0i0p0' ; attval['frequency']='fx'
    #
    errmsg=""
    for facet in cprojects[project].facets :
        if attval[facet] is None :
            e="Project '%s' needs facet '%s'. You may use cdef() for setting a default value"\
               %(project,facet)
            errmsg+=" "+e
    if errmsg != "" : raise Climaf_Classes_Error(errmsg)
    #
    #print "kw="+`kwargs`
    for facet in attval :
        # Facet specific processing
        if facet=='period' :
            if not isinstance(attval['period'],cperiod) :
                try :
                    attval['period']=init_period(attval['period'])
                except :
                    raise Climaf_Classes_Error("Cannot interpret period for %s"%`attval['period']`)
            #else :
            #    print "%s is a cperiod"%`attval['period']`
        #elif facet=='domain' and not type(attval['domain']) is str :
        #    # May be a list
        #    attval['domain']=eval(attval['domain'])
        # Check for typing or user's logic errors
        if not facet in cprojects[project].facets :
            e="Project %s doesn't have facet %s"%(project,facet)
            errmsg+=" "+e
    if errmsg != "" : raise Climaf_Classes_Error(errmsg)
    if 'period' in attval and not isinstance(attval['period'],cperiod) :
        Climaf_Classes_Error("at end of  process.. : period is not a cperiod")
    return attval


class cdataset(cobject):
    #def __init__(self,project=None,model=None,simulation=None,period=None,
    #             rip=None,frequency=None,domain=None,variable=None,version='last') :
    def __init__(self,**kwargs) :
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
        
        
        """
        #
        attval=processDatasetArgs(**kwargs)
        #
        # TBD : Next lines for backward compatibility, but should re-engineer 
        self.project=attval["project"]
        self.simulation=attval['simulation']
        self.variable= attval['variable']
        # alias is a n-plet : filevar, scale, offset, filenameVar, missing
        self.period    =attval['period']
        self.domain    =attval['domain']
        #
        self.model    =attval.get('model',"*")
        self.frequency=attval.get('frequency',"*")
        # Normalized name is annual_cycle, but allow also for 'seasonal' for the time being
        if (self.frequency=='seasonal' or self.frequency=='annual_cycle') :
            self.period.fx=True
        freqs_dic=frequencies.get(self.project,None)
        #print freqs_dic
        if freqs_dic :
            for k in freqs_dic :
                if freqs_dic[k]==self.frequency and k=='annual_cycle' :
                    self.period.fx=True
        #
        self.kvp=attval
        self.alias=varIsAliased(self.project,self.variable)
        #
        if ("," in self.variable and self.alias) :
            filevar,scale,offset,units,filenameVar,missing=self.alias
            if (filevar != self.variable or scale != 1. or offset != 0 or missing ) :
                raise Climaf_Classes_Error("Cannot alias/scale/setmiss on group variable")
        # Build CliMAF Ref Syntax for the dataset
        self.crs=self.buildcrs()
        # 
        self.files=None
        self.register()

    def setperiod(self,period) :
        self.erase()
        self.period=period
        self.kvp['period']=period
        self.crs=self.buildcrs()
        self.register()
        
    def buildcrs(self,period=None,crsrewrite=None):
        crs_template=string.Template(cprojects[self.project].crs)
        dic=self.kvp.copy()
        if period is not None : dic['period']=period
	if type(dic['domain']) is list : dic['domain']=`dic['domain']`
        rep="ds('%s')"%crs_template.safe_substitute(dic)
        return rep

    def isLocal(self) :
        model=getattr(self,"model","*")
        return(dataloc.isLocal(project=self.project, model=model, \
                               simulation=self.simulation, frequency=self.frequency))
    def isCached(self) :
        """ TBD : analyze if a remote dataset is locally cached
        
        """
        clogger.error("TBD - remote datasets are not yet cached")
        rep=False
        return rep

    def oneVarPerFile(self):
        locs=dataloc.getlocs(project=self.project, model=self.model, simulation=self.simulation, \
                             frequency=self.frequency)
        return(all([org for org,freq,url in locs]))
    
    def periodIsFine(self):
        clogger.debug("always returns False, yet - TBD")
        return(False) 
        
    def domainIsFine(self):
        clogger.debug("a bit too simple yet (domain=='global')- TBD")
        return(self.domain == 'global') 
        
    def periodHasOneFile(self) :
        return(len(self.baseFiles().split(" ")) < 2)
        #clogger.debug("always returns False, yet - TBD")
        #return(False) 

    def hasOneMember(self) :
        clogger.debug("always returns True, yet - TBD")
        return(True) 

    def hasExactVariable(self):
        # Assume that group variable do not need aliasing
        if ("," in self.variable) : return True
        clogger.debug("always returns False, yet - TBD")
        return(False) 
    
    def missingIsOK(self):
        if (alias is None) : return True
        filevar,scale,offset,units,filenameVar,missing=self.alias
        return missing is None
    
    def baseFiles(self,force=False):
        """ Returns the list of (local) files which include the data for the dataset
        Use cached value unless called with arg force=True
        """
        if (force and self.project != 'file') or self.files is None :
            dic=self.kvp.copy()
            if self.alias : 
                filevar,scale,offset,units,filenameVar,missing=self.alias
                dic["variable"]=filevar
                if filenameVar : dic["filenameVar"]=filenameVar
            clogger.debug("Looking with dic=%s"%`dic`)
            self.files=dataloc.selectLocalFiles(**dic)
        return self.files
    def hasRawVariable(self) :
        """ Test local data files to tell if a dataset variable is actually included 
        in files (rather than being a derived, virtual variable)

        For the time being, returns False, which leads to always consider that variables
        declared as 'derived' actually are derived """
        clogger.debug("TBD: actually test variables in files, rather than assuming that variable %s is virtual for dataset %s"\
                        %(self.variable,self.crs))
        return(False)

class cens(cobject):
    def __init__(self, labels=None, *members ) :
        """
        Create a CliMAF object of class ``cens`` , i.e. an
        ensemble of objects, with a list of labels attached

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
             declaration calls for it
             (see :py:func:`~climaf.operators.cscript()`)
           - if it is a Python function : with the list of
             corresponding objects

         - if the operator is 'ensemble-dumb', CliMAF will loop
           applying it on each member, and will form a new ensemble
           with the results.

        ``labels`` must be a list of strings, which describe what is
        basically different among members. They are usually used by
        plot scripts to provide a caption allowing to identify each
        dataset/object e.g using varied colors. The labels list is
        propagated across operators application.

        Example:
        
        >>> cdef('project','example'); cdef('simulation',"AMIPV6ALB2G");
        >>> cdef('variable','tas');cdef('frequency','monthly')
        >>> #
        >>> ds1980=ds(period="1980")
        >>> ds1981=ds(period="1981")
        >>> #
        >>> cens(['1980','1981'],ds1980,ds1981)
        >>> ncview(cens)  # will launch ncview once per member
        
        """
        if not labels : 
            raise Climaf_Classes_Error("Must provide a list of labels for members")
        if isinstance(labels,cobject) :
            raise Climaf_Classes_Error("First argument must be the list of labels for members")
        if not all(map(lambda x : isinstance(x,str), labels)):
            raise Climaf_Classes_Error("All labels must be strings")
        if len(labels) != len(members) :
            raise Climaf_Classes_Error("Must provide as many labels as members")
        if not all(map(lambda x : isinstance(x,cobject), members)):
            raise Climaf_Classes_Error("All members must be CliMAF objects")
        self.members=list(members)
        self.labels=labels
        self.crs=self.buildcrs()
        self.register()

    def buildcrs(self,crsrewrite=None,period=None) :
        rep="cens("+`self.labels`+","
        for m in self.members : rep+=m.buildcrs(crsrewrite=crsrewrite)+","
        rep=rep+")"
        rep=rep.replace(",)",")")
        return rep


def eds(**kwargs):
    """
    Create a dataset ensemble using the same calling sequence as
    :py:func:`~climaf.classes.cdataset`, except that one of the facets
    is a list, for defining the nsemble members; this facet must be among
    the facets authorized for ensemble in the (single) project involved

    Example::

    >>> cdef("frequency","monthly") ;  cdef("project","CMIP5"); cdef("model","CNRM-CM5")
    >>> cdef("variable","tas"); cdef("period","1860")
    >>> ens=eds(experiment="historical", simulation=["r1i1p1","r2i1p1"])

    """
    attval=processDatasetArgs(**kwargs)
    # Check that any facet/attribute of type 'list' (for defining an
    # ensemble) is OK for the project, and that there is at most one
    nlist=0
    listattr=None
    for attr in attval :
        clogger.debug("Looking at attr %s for ensemble"%attr)
        if isinstance(attval[attr], list) and attr != "domain":
            if not attr in cprojects[attval["project"]].attributes_for_ensemble :
                raise Climaf_Classes_Error("Attribute %s cannot be used for ensemble"%attr)
            clogger.debug("Attr %s is used for an ensemble"%attr)
            nlist+=1
            listattr=attr
    if nlist != 1 :
        raise Climaf_Classes_Error("Must ask for an ensemble on exactly one attribute")
    #
    # Create an ensemble of datasets if applicable
    labels=[]; members=[]
    for member in attval[listattr] :
        attval2=attval.copy()
        attval2[listattr]=member
        members.append(cdataset(**attval2))
        labels.append(member)
    return cens(labels,*members)

def fds(filename, simulation=None, variable=None, period=None, model=None) :
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
    filename=os.path.expanduser(filename)
    if not os.path.exists(filename): 
        raise Climaf_Classes_Error("File %s does no exist"%filename)
    #
    if model is None : model=model_id(filename)
    if simulation is None : simulation=os.path.basename(filename)[0:-3]
    #
    if variable is None :
        lvars=varsOfFile(filename)
        if len(lvars)==0 : 
            raise Climaf_Classes_Error("No variable in file %s"%filename)
        variable=lvars.pop()
        for v in lvars : variable+=","+v
    else :
        lvars=variable.split(',')
        for v in lvars :
            if not fileHasVar(filename,v) :
                raise Climaf_Classes_Error("No variable %s in file %s"%(v,filename))
    #
    fperiod=timeLimits(filename)
    if period is None :
        if fperiod is None :
            raise Climaf_Classes_Error("Must provide a period for file %s "\
                                           %(filename))
        else :
            period=`fperiod`
    else :
        if fperiod and not fperiod.includes(init_period(period)) :
            raise Climaf_Classes_Error("Max period from file %s is %s"\
                                           %(filename,`fperiod`))
    #
    d=ds(project='file', model=model, simulation=simulation, 
         variable=variable, period=period, path=filename)
    d.files=filename
    return d


class ctree(cobject):
    def __init__(self, climaf_operator, script, *operands, **parameters ) :
        """ Builds the tree of a composed object, including a dict for outputs.

        """
        self.operator=climaf_operator
        self.script=script
        import copy
        self.flags=copy.copy(script.flags)
        self.operands=operands
        if "period" in parameters :
            p=parameters["period"]
            if isinstance(p,cperiod) : parameters["period"]=`p`
        self.parameters=parameters
        for o in operands :
            if o and not isinstance(o,cobject) :
                raise Climaf_Classes_Error("operand "+`o`+" is not a CliMAF object")
        self.crs=self.buildcrs()
        self.outputs=dict()
        self.register()

    def buildcrs(self, crsrewrite=None, period=None) :
        """ Builds the CRS expression representing applying OPERATOR on OPERANDS with PARAMETERS.
        Forces period downtree if provided
        A function for rewriting operand's CRS may be provided
        """
        # Operators are listed in alphabetical order; parameters too
        rep=self.operator+"("
        #
        ops=[ o for o in self.operands ]
        for op in ops :
            if op :
                opcrs = op.buildcrs(crsrewrite=crsrewrite,period=period)
                if crsrewrite : opcrs=crsrewrite(opcrs)
                rep+= opcrs + ","
        #
        clefs=self.parameters.keys()
        clefs.sort()
        for par in clefs :
            rep += par+"="+`self.parameters[par]`+","
        rep += ")"
        rep=rep.replace(",)",")")
        return rep

    def setperiod(self,period):
        """ modifies the period for all datasets of a tree"""
        self.erase()
        for op in self.operands : op.setperiod(period)
        self.crs=self.buildcrs(period=period)
        self.register()

class scriptChild(cobject):
    def __init__(self, cobject,varname) :
        """
        Builds one of the child of a script call, which represents one output

        """
        self.father=cobject
        self.varname=varname
        self.crs=self.buildcrs()
        self.file=None
        self.register()

    def setperiod(self,period):
        self.erase()
        self.crs=self.father.crs.buildcrs(period=period)
        self.crs += "."+self.varname
        self.register()

    def buildcrs(self,period=None,crsrewrite=None):
        tmp= self.father.buildcrs(period=period)
        if (crsrewrite): tmp=crsrewrite(tmp)
        return tmp+"."+self.varname

def compare_trees(tree1,tree2,func,filter_on_operator=None) :
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
    if isinstance(tree1,cdataset) and isinstance(tree2,cdataset):
        return func(tree1,tree2)
    elif isinstance(tree1,ctree) and isinstance(tree2,ctree):
        if tree1.operator == tree2.operator :
            if filter_on_operator :
                if filter_on_operator(tree1.operator): return None
            if tree1.parameters == tree2.parameters :
                return(reduce(lambda a,b : a if `a`==`b` else None, 
                   [ compare_trees(op1,op2,func,filter_on_operator) 
                     for op1,op2 in zip(tree1.operands, tree2.operands) ]))
    elif isinstance(tree1,scriptChild) and isinstance(tree2,scriptChild):
        if tree1.varname==tree2.varname :
            return compare_trees(tree1.father,tree2.father,
                                 func,filter_on_operator)


def ds(*args,**kwargs) :
    """
    Returns a dataset from its full Climate Reference Syntax string. Example ::

     >>> ds('CMIP5.historical.pr.[1980].global.monthly.CNRM-CM5.r1i1p1.mon.Amon.atmos.last')

    Also a shortcut for :py:meth:`~climaf.classes.cdataset`, 
    when used with with only keywords arguments. Example ::

     >>> cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',\
              simulation='r2i3p9', domain=[40,60,-10,20], variable='tas', period='1980-1989', version='last')

    """
    if len(args) >1 :
        raise Climaf_Classes_Error("Must provide either only a string or only keyword arguments")
    #clogger.debug("Entering , with args=%s, kwargs=%s"%(`args`,`kwargs`))
    if (len(args)==0) : return cdataset(**kwargs) # Front-end to cdataset
    crs=args[0]
    results=[]
    for cproj in cprojects : 
        try : dataset = cprojects[cproj].crs2ds(crs) 
        except Climaf_Classes_Error: dataset=None
        if (dataset) : results.append(dataset)
    if len(results) > 1 :
        e="CRS expressions %s is ambiguous among projects %s"%(crs,`cprojects.keys()`)
        clogger.error(e)
        raise Climaf_Classes_Error(e)
    elif len(results) == 0 :
        e="CRS expressions %s is not valid for any project in %s"%(crs,`cprojects.keys()`)
        raise Climaf_Classes_Error(e)
        return None
    else : 
        rep=results[0]
        if rep.project=='file' : 
            rep.files=rep.kvp["path"]
        return rep

def cfreqs(project,dic) :
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
    frequencies[project]=dic


def calias(project,variable,fileVariable=None,scale=1.,offset=0.,units=None,missing=None,filenameVar=None) :
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
    >>> calias('NEMO','so,thetao',filenameVar='grid_T_table2.2')
    
    """
    if not fileVariable : fileVariable = variable
    if not filenameVar  : filenameVar  = None
    if project not in cprojects : 
        raise Climaf_Classes_Error("project %s is not known"%project)
    if project not in aliases : aliases[project]=dict()
    if type(variable)     is not list : variable    = [variable]
    if type(filenameVar)  is not list : filenameVar = [filenameVar]
    if type(fileVariable) is not list : fileVariable= [fileVariable]
    if type(units)        is not list : units       = [units]
    for v,u,fv,fnv in zip(variable,units,fileVariable,filenameVar) :
        aliases[project][v]=(fv,scale,offset,u,fnv,missing)

def varIsAliased(project,variable) :
    """ 
    Return a n-uplet (fileVariable, scale, offset, filevarName,
    missing) defining how to compute a 'variable' which is not in
    files, for the 'project'
    """
    if project in aliases and variable in aliases[project] :
        return aliases[project][variable]

def cmissing(project,missing,*kwargs) :
    """ Declare that in 'project', a given constant must be interpreted
    as a missing value, for a given set of project's attributes values

    Such a declaration must follow all ``calias`` declarations for the
    same project
    """
    pass # TBD 



class cpage(cobject):
    def __init__(self, fig_lines=None, widths=None, heights=None, 
                  orientation="portrait", fig_trim=True, page_trim=True):
        """
        Builds a CliMAF cpage object, which represents an array of figures

        Args:
         fig_line (a list of lists of figure objects or an ensemble of
           figure objects): each sublist of 'fig_lines' represents a
           line of figures
         widths (list, optional): the list of figure widths, i.e. the
           width of each column. By default, if fig_line is:

             - a list of lists:  spacing is even
             - an ensemble:  one column is used
         heights (list, optional): the list of figure heights, i.e. the
           height of each line. By default  spacing is even
         orientation (str, optional): page's orientation, either 'portrait' 
           (default) or 'landscape'
         fig_trim (logical, optional): to turn on/off triming for all figures.
           It removes all the surrounding extra space of figures in the page,
           either True (default) or False
         page_trim (logical, optional): to turn on/off triming for the page. It
           removes all the surrounding extra space of the page, either True
           (default) or False 

        Example:

         Using no default value, to create a page with 2 columns and 3 lines::
        
          >>> fig=plot(tas_avg,title='title')
          >>> my_page=cpage([[None, fig],[fig, fig],[fig,fig]], widths=[0.2,0.8],
          ... heights=[0.33,0.33,0.33], orientation='landscape', fig_trim=False, page_trim=False)

        
        """
        if fig_lines is None :
            raise Climaf_Classes_Error("fig_lines must be provided")
       
        self.orientation=orientation
        self.fig_trim=fig_trim
        self.page_trim=page_trim

        if not isinstance(fig_lines,list) and not isinstance(fig_lines,cens) :
            raise Climaf_Classes_Error(
                "fig_lines must be an ensemble or a list "
                "of lists (each representing a line of figures)")
        if isinstance(fig_lines,list) :
            if not widths :
                widths=[]
                for line in fig_lines:
                    if len(line)!=len(fig_lines[0]):
                        raise Climaf_Classes_Error("each line in fig_lines must have same dimension")
                for column in fig_lines[0]: widths.append(round(1./len(fig_lines[0]),2))
            self.widths=widths

            if not heights :
                heights=[]
                for line in fig_lines: heights.append(round(1./len(fig_lines),2))
            self.heights=heights

            if len(fig_lines)!=len(self.heights) :
                raise Climaf_Classes_Error(
                    "fig_lines must have same size than heights")
            for line in fig_lines:
                if not isinstance(line,list) :
                    raise Climaf_Classes_Error(
                        "each element in fig_lines must be a list of figures")
                if len(line)!=len(self.widths) :
                    raise Climaf_Classes_Error(
                        "each line in fig_lines must have same dimension as "
                        "widths; pb for sublist "+`line`)
            self.fig_lines=fig_lines
        else: # case of an ensemble (cens) 
            figs=list(fig_lines.members)

            if not widths: widths=[1.]
            self.widths=widths
            if not heights :
                heights=[]
                for memb in figs: heights.append(round(1./len(figs),2))
            self.heights=heights
            
            self.fig_lines=[]
            for l in heights :
                line=[]
                for c in widths :
                    if len(figs) > 0 : line.append(figs.pop(0))
                    else : line.append(None)
                              
                self.fig_lines.append(line)
        #
        self.crs=self.buildcrs()
               
    def buildcrs(self,crsrewrite=None,period=None):
        rep="cpage(["
        for line in self.fig_lines :
            rep+="["
            for f in line :
                if f : rep+=f.buildcrs(crsrewrite=crsrewrite)+","
                else : rep+=`None`+","
            rep+=" ],"; 
        rep+="],"+`self.widths`+","+`self.heights`+",orientation='"+self.orientation+\
              "', fig_trim='%s', page_trim='%s')" %(self.fig_trim,self.page_trim)
        rep=rep.replace(",]","]")
        rep=rep.replace(", ]","]")
        
        return rep

        
def guess_projects(crs) :
    """
    Return the list of projects involved in the datasets involved in a 
    CRS expression. 
    """
    def guess_project(crs) :
        """
        Guess which is the project name for a dataset's crs, with minimum 
        assumption on the separator used in the project
        """
        separators=[r'.',r'_',r'£',r'$',r'@',r'_',r'|',r'&',r"-",r"=",r"^",
                    r";",r":",r"!",r'§',r'/',r'.',r'ø',r'+',r'°']
        counts=dict()
        for sep in separators : counts[sep]=crs.count(sep)
        # Assume that the highest count gives the right separator
        max=0
        for key in counts : 
            if counts[key] >= max : 
                max=counts[key]
                sep=key
        return(crs[1:crs.find(sep)])
    return map(guess_project,re.findall(r"ds\(([^)]*)",crs))
    
def browse_tree(cobj,func,results):
    """ Browse a CliMAF object's tree, accumulating in 'results' the 
    values returned by 'func' on each tree node or leave (if they are 
    not None)
    """
    if isinstance(cobj,cdataset) or isinstance(cobj,cdummy) :
        res=func(cobj)
        if res : partial.append(res)
    elif isinstance(cobj,ctree) :
        res=func(cobj.operator)
        if res : partial.append(res)
        for op in cobj.operands : browse_tree(op,func,partial)
    elif isinstance(cobj,scriptChild) :
        browse_tree(cobj.father,func,partial)
    elif isinstance(cobj,cpage) :
        for line in cobj.fig_lines :
            map(lambda x : browse_tree(x,func,partial), line)
    elif cobj is None : return 
    else :
        clogger.error("Cannot yet handle object :%s", `cobj`)
        return


class Climaf_Classes_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)
    def __str__(self):
        return `self.valeur`

def test():
#    clogger.basicConfig(level=clogger.DEBUG) #LV
#    clogger.basicConfig(format='"%(asctime)s [%(funcName)s: %(filename)s,%(lineno)d] %(message)s : %(levelname)s', level=clogger.DEBUG)
    cdef("project","CMIP5")
    #cdef("project","PR6")
    cdef("model","CNRM-CM5")
    cdef("experiment","historical")
    cdef("simulation","r1i1p1")
    cdef("period","197901-198012")
    cdef("domain","global")
    #
    tos=cdataset(experiment="rcp85", variable="tos", period="19790101-19790102")
    tr=ctree("operator", tos, para1="val1",para2="val2")
    #tos.pr()
    #
    #ds1=Dataset(period="1850-2012")
    #genericDataSets(ds1.crs)
    #ds2=Dataset(project="CMIP3")
    #ex="toto("+ ds1.crs + "," + ds2.crs
    #print genericDataSets(ex)
    #print firstGenericDataSet(ex)

def t2() :
    p=period("1984-1984")
    

if __name__ == "__main__":
    test()
