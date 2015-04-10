""" 
 Basic types and syntax for a CLIMAF Reference Syntax interpreter and driver
 This is a first protoype, where the interpreter is Python itself


 """
# Created : S.Senesi - 2014

import re, string

import dataloc
from period import init_period, cperiod
from clogging import clogger

#: Dictionnary storing user-default values for dataset attributes, used when defining a new dataset 
cdefaults=dict()

def cdefault(attribute,value=None):
    """
    Set or get the default value for a CliMAF dataset attributes (as e.g. 'model', 'project' ...),
    for use by next calls to :py:class:`~climaf.classes.cdataset` or to :py:func:`~climaf.classes.ds`

    Theres is no actual check that 'attribute' is a valid keyword for a call to ``ds`` or ``cdateset``

    """
    if value is None :
        if attribute in cdefaults.keys() :
            return cdefaults[attribute]
        else:
            return None
    else :
        cdefaults[attribute]=value

cdefault("project","*")
cdefault("model","*")
#cdefault("experiment","*")
#cdefault("period","197901-198012")
cdefault("rip","r1i1p1")
cdefault("frequency","monthly")
cdefault("domain","global")
cdefault("table","*")
cdefault("realm","*")
cdefault("version","last")
#cdefault("variable","tas")


# Basic handling of CliMAF Ref Syntax objects
##########################################################################################

# All CObject instances are registered in this directory :
cobjects=dict()

class cobject():
    def __init__(self):
        # crs is the string expression defining the object in the CLIMAF Reference Syntax
        self.crs="void"
        # every object has a variable name for the main/unique file variable  
        self.fileVarName="void"
    def pr(self):
        print(self.crs)
    def __str__(self):
        #return "Climaf object : "+self.crs
        return self.crs
    def __repr__(self):
        return self.crs
    def register(self):
        cobjects[self.crs]=self
        clogger.debug("Object Created ; crs = %s"%(self.crs))
    def erase(self):
        del(cobjects[self.crs])
        clogger.debug("Object deleted ; crs = %s"%(self.crs))

class cdataset(cobject):
    #def __init__(self,project=None,model=None,experiment=None,period=None,
    #             rip=None,frequency=None,domain=None,variable=None,version='last') :
    def __init__(self,**kwargs) :
        """
        Create a CLIMAF dataset. 
        
        A CLIMAF dataset is a description of what the data is and not the data itself nor a file.
        It is essentially a set of pairs attributes-values. The list of attributes actually used 
        to describe a dataset is defined by the 'project' it refers to. However, all projects 
        include attributes experiment, period and variable

        All attributes defaults to the value set by :py:func:`~climaf.classes.cdefault`

        For the time being, the attributes used in the string description of a dataset 
        (its CRS) are the whole list of CMIP5_DRS attributes, with wildcards 
        values when attribute is not applicable; this scheme should be relaxed sooner or
        later. e.g., in a home-made 'project', the 'model' attribute could be superfluous 

        Args:
          project (str, optional): project attribute; should match one of the data locations declared
           with :py:func:`~climaf.dataloc.dataloc` (even if it is only a wildcard one)

          model (str, optional): model attribute; should match one of the data locations declared
           with :py:func:`~climaf.dataloc.dataloc` (even if it is only a wildcard one)

          experiment (str, optional): experiment attribute ; should match one of the data locations declared
           with :py:func:`~climaf.dataloc.dataloc` (even if it is only a wildcard one)

          frequency (str, optional): frequency attribute ; should match one of the data locations declared
           with :py:func:`~climaf.dataloc.dataloc` (even if it is only a wildcard one)

          rip (str, optional): rip attribute; after CMIP5 syntax (e.g. : r1i1p1 )

          domain (str, optional): domain attribute; allowed values are either 'global' or a list for latlon
            corners ordered as in : [ latmin, latmax, lonmin, lonmax ]
            
          variable (str, optional): name of geophysical variable ; this should be :

           - either a variable actually included in the datafiles, or
           - a 'derived' variable (see  :py:func:`~climaf.operators.derive` ), or
           - later on (to be developped), an aliased variable name

          period (str): a period, syntax as explained with :py:func:`~climaf.period.init_period`

          version (str, optional): version of the data; file access functions hanlde nicely values
            'last' and '*'

        Example, using no default value, and adressing some CMIP5 data ::

          >>  dataloc(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',\
              rip='r2i3p9', domain=[40,60,-10,20], variable='tas', period='1980-1989', version='last')
        
        
        """
        #
        self.crs=""
        if 'project' in kwargs : self.project=kwargs['project']
        else : self.project= cdefault("project")   
        if self.project is None :
            clogger.error("Must provide a project (Can use cdef)")
            return 
        elif self.project not in cprojects :
            clogger.error("Dataset's project %s has not been described by a call to cproject()"%self.project)
            return
        # Register facets values
        err=False
        self.kvp=dict()
        for facet in cprojects[self.project].facets :
            if facet in kwargs : val=kwargs[facet]
            else: val=cdefault(facet)
            if val is None :
                clogger.error("Project %s needs facet %s"%(self.project,facet))
                err=True
            self.kvp[facet]=val
            #self.__set__(facet,val)
        #
        # Check for typing or user's logic errors
        for facet in kwargs :
            if not facet in cprojects[self.project].facets :
                clogger.error("Project %s doesn't have facet %s"%(self.project,facet))
                err=True
        #
        if err : return None
        if ('period' in self.kvp) : self.kvp['period']=init_period(self.kvp['period'])
        # TBD : Next lines for backward compatibility, but should re-engineer 
        self.project   =self.kvp['project']
        self.experiment=self.kvp['experiment']
        self.variable= self.kvp['variable']
        self.period    =self.kvp['period']
        self.domain    =self.kvp['domain']
        #
        self.model    =self.kvp.get('model',"*")
        self.frequency=self.kvp.get('frequency',"*")
        #
        # Build CliMAF Ref Syntax for the dataset
        self.crs=self.buildcrs()
        # 
        self.register()

    def setperiod(self,period) :
        self.erase()
        self.period=period
        self.crs=self.buildcrs()
        self.register()
        
    def buildcrs(self,period=None):
        # Note : function 'ds' (far below) must be modified when buildcrs is modified
        crs_template=string.Template(cprojects[self.project].crs)
        dic=self.kvp
        if period is not None : dic['period']=period
	if type(dic['domain']) is list : dic['domain']=`dic('domain')`
        rep="ds('%s')"%crs_template.safe_substitute(dic)
        return rep

    def isLocal(self) :
        model=getattr(self,"model","*")
        return(dataloc.isLocal(project=self.project, model=model, \
                               experiment=self.experiment, frequency=self.frequency))
    def isCached(self) :
        """ TBD : analyze if a remote dataset is locally cached
        
        """
        clogger.error("TBD - remote datasets are not yet cached")
        rep=False
        return rep

    def oneVarPerFile(self):
        locs=dataloc.getlocs(project=self.project, model=self.model, experiment=self.experiment, \
                             frequency=self.frequency)
        return(all([org for org,freq,url in locs]))
    
    def periodIsFine(self):
        clogger.debug("always returns False, yet - TBD")
        return(False) 
        
    def domainIsFine(self):
        clogger.debug("a bit too simple yet (domain=='global')- TBD")
        return(self.domain == 'global') 
        
    def periodHasOneFile(self) :
        clogger.debug("always returns False, yet - TBD")
        return(False) 

    def hasOneMember(self) :
        clogger.debug("always returns True, yet - TBD")
        return(True) 

    def baseFiles(self):
        """ Returns the list of (local) files which include the data for the dataset
        """
        return(dataloc.selectLocalFiles(**self.kvp))
    def hasRawVariable(self) :
        """ Test local data files to tell if a dataset variable is actually included 
        in files (rather than being a derived, virtual variable)

        For the time being, returns False, which leads to always consider that variables
        declared as 'derived' actually are derived """
        clogger.debug("TBD: actually test variables in files, rather than assuming that variable %s is virtual for dataset %s"\
                        %(self.variable,self.crs))
        return(False)

class ctree(cobject):
    def __init__(self, climaf_operator, script, *operands, **parameters ) :
        """ Builds the tree of a composed object, including a dict for outputs.

        """
        self.operator=climaf_operator
        self.script=script
        self.operands=operands
        if "period" in parameters :
            p=parameters["period"]
            if isinstance(p,cperiod) : parameters["period"]=`p`
        self.parameters=parameters
        for o in operands :
            if not isinstance(o,cobject) :
                clogger.error(" __init__ : operand "+`o`+" is not a CliMAF object")
                return None
        self.crs=self.buildcrs()
        self.outputs=dict()
        self.register()

    def buildcrs(self, period=None) :
        """ Builds the CRS expression representing applying OPERATOR on OPERANDS with PARAMETERS.
        Forces period downtree if provided
        """
        # Operators are listed in alphabetical order; parameters too
        rep=self.operator+"("
        ops=[ o for o in self.operands ]
        #ops.sort()
        for op in ops : rep += op.buildcrs(period)+", "
        clefs=self.parameters.keys()
        clefs.sort()
        for par in clefs : rep += par+"="+`self.parameters[par]`+", "
        rep += ")"
        rep=rep.replace(", )",")")
        return rep

    def setperiod(self,period):
        """ modifies the period for all datasets of a tree"""
        self.erase()
        for op in self.operands : op.setperiod(period)
        self.crs=self.buildcrs(period)
        self.register()

class scriptChild(cobject):
    def __init__(self, cobject,varname) :
        """ Builds one of the child of a script call, which represents one output

        """
        self.father=cobject
        self.varname=varname
        self.crs=self.buildcrs()
        self.file=None
        self.register()

    def setperiod(self,period):
        self.erase()
        self.crs=self.father.crs.buildcrs(period)+"."+self.varname
        self.register()

    def buildcrs(self,period=None):
        return self.father.buildcrs(period)+"."+self.varname

def compare_trees(tree1,tree2,func,filter_on_operator=None) :
    """
    Recursively compares TREE1 and TREE2.
    
    For the nodes : compares operator and parameters; ensures 
    that FILTER_ON_OPERATOR(operator) is not true 
    
    For the leaves (datasets) : ensure that string representations of
    applying function FUNC to the pair of datasets returns the same
    value for all datasets pairs in the (parallel) trees
    
    Returns that common value : func(leave1,leave2)) or None
    
    FUNC cannot not return None as a valid value
    """
    if isinstance(tree1,cdataset) and isinstance(tree2,cdataset):
        return func(tree1,tree2)
    elif isinstance(tree1,ctree) and isinstance(tree2,ctree):
        if tree1.operator == tree2.operator :
            if filter_on_operator :
                if filter_on_operator(tree1.operator): return None
            if tree1.parameters == tree2.parameters :
                return(reduce(lambda(a,b) : a if `a`==`b` else None, 
                   [ compare_trees(op1,op2,func,filter_on_operator) 
                     for op1,op2 in zip(tree1.operands, tree2.operands) ]))
    elif isinstance(tree1,scriptChild) and isinstance(tree2,scriptChild):
        if tree1.name==tree2.name :
            return compare_trees(tree1.father,tree2.father,func,filter_on_operator)


    #

# def genericDataSets(expression, pattern=None) :
#     """ Identifies the basic datasets in EXPRESSION and returns them
#     as generic Datasets (i.e. without period nor domain information).
#     """
    
#     # TBC : take care of exceptions, and remove period and domain info, and upgrade to non-basic datasets

def ds(*args,**kwargs) :
    """
    Returns a dataset from its full Climate Reference Syntax string.

    Also a shortcut for :py:meth:`~climaf.classes.cdataset`, when used with with only keywords arguments

    """
    # Note : muts be kept phased with self.crs defined in cdataset.init(), both for
    # function name and CRS syntax
    if len(args) >1 :
        clogger.error("must provide either 0 or 1 positional arguments, not "+len(args))
        return None
    if (len(args)==0) : return cdataset(**kwargs) # Front-end to cdataset
    crs=args[0]
    results=[]
    for cproj in cprojects : 
        dataset = cproj.crs2ds(crs) 
        if (dataset) : result.append(dataset)
    if len(results) > 1 :
        clooger.error("CRS expressions %s is ambiguous"%crs)
        return None
    elif len(results) == 0 :
        clooger.error("CRS expressions %s is not valid for any project in %s"%(crs,`cprojects`))
        return None
    else : return results[0]

#: List of declared projects (type is cproject)
cprojects=dict()

class cproject():
    def __init__(self,name,  *args, **kwargs) :
        """
        A 'cproject' is the definition of a set of attributes, or facets, which 
        values completely define a 'dataset' as managed by CliMAF.

        For instance, cproject CMIP5 , after his Data Reference Syntax, has attributes : 
        experiment, model, rip, variable, frequency, realm, table, version

        The args provide the attribute names.

        CliMAF anyway enforces attributes : project, experiment, variable, period, domain

        The attributes list, as composed of those ienforced by CliMAF
        and those provided by args, defines the Reference Syntax for
        datasets in the cproject; for instance, a datset in a cproject
        declared as ::

        >>> cproject("MINE","myfreq","myfacet")

        will hase dataset syntax based on the pattern:

        project.experiment.variable.period.domain.myfreq

        such as::

        MINE_hist_[1980-1999]_global_decadal

        while an example for cproject CMIP5 could be::

        CMIP5.historical.[1980].global.monthly

        The attributes list should include all facets which are useful
        for distinguishing datastes for each other , and for computing
        datafile pathnames in the 'generic' organization (see
        :ref:class:`~climaf.dataloc.dataloc`)

        """
        if name in cprojects : clogger.warning("Redefining project %s"%name)
        self.project=name
        #
        self.facets=[]
        forced=['project','experiment', 'variable', 'period', 'domain']
        for f in forced : self.facets.append(f)
        for a in args : 
            if not a in forced : self.facets.append(a)
        #
        self.separator="."
        if "separator" in kwargs : self.separator=kwargs['separator']
        cprojects[name]=self
        self.crs=""
        # Build the pattern for the datasets CRS for this cproject
        for f in self.facets : 
            self.crs += "${%s}%s"%(f,self.separator)
        self.crs=self.crs[:-1]
    def __repr__(self):
        return self.crs
    def crs2ds(crs) :
        """ 
        Try to interpret a string as the CRS of a dataset for the current cproject
        Return the dataset if OK
        """
        fields=crs.split(self.separator)
        if len(fields) == len(self.facets) :
            if fields[0] == self.project :
                kvp=dict()
                for i,f in enumerate(self.facets) : kvp[f]=fields[i]
                try :
                    kvp['period']=init_period(kvp['period'])
                    # domain may be the string representation of a list of corner coordinates, 
                    # let us try to evaluate it
                    kvp['domain']=eval(kvp['domain'])
                except:
                    return
                return cdataset(kvp)


def test():
#    clogger.basicConfig(level=clogger.DEBUG) #LV
#    clogger.basicConfig(format='"%(asctime)s [%(funcName)s: %(filename)s,%(lineno)d] %(message)s : %(levelname)s', level=clogger.DEBUG)
    cdefault("project","CMIP5")
    #cdefault("project","PR6")
    cdefault("model","CNRM-CM5")
    cdefault("experiment","historical")
    cdefault("rip","r1i1p1")
    cdefault("period","197901-198012")
    cdefault("domain","global")
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
