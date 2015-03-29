""" 
 Basic types and syntax for a CLIMAF Reference Syntax interpreter and driver
 This is a first protoype, where the interpreter is Python itself


 """
# Created : S.Senesi - 2014

# The CliMAF software is an environment for Climate Model Assessment. It
# has been developped mainly by CNRM-GAME (Meteo-France and CNRS), and
# by IPSL, in the context of the `CONVERGENCE project
# <http://convergence.ipsl.fr/>`_, funded by The
# French 'Agence Nationale de la Recherche' under grant #
# ANR-13-MONU-0008-01
# 
# This software is governed by the CeCILL-C license under French law and
# biding by the rules of distribution of free software. The CeCILL-C
# licence is a free software license,explicitly compatible with the GNU
# GPL (see http://www.gnu.org/licenses/license-list.en.html#CeCILL)

import re, logging
import dataloc
from period import init_period,cperiod

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
        logging.debug("Object Created ; crs = %s"%(self.crs))
    def erase(self):
        del(cobjects[self.crs])
        logging.debug("Object deleted ; crs = %s"%(self.crs))

class cdataset(cobject):
    def __init__(self,project=None,model=None,experiment=None,period=None,
                 rip=None,frequency=None,domain=None,variable=None,version='last') :
        """
        Create a CLIMAF dataset. 
        
        A CLIMAF dataset is a description of what the data is and not the data itself nor a file.
        It is essentially a set of attributes

        All args (but period and version) defaults to the value set by :py:func:`~climaf.classes.cdefault`

        Args:
          project (str, optional): project attribute
          model (str, optional): model attribute
          experiment (str, optional): experiment attribute
          frequency (str, optional): frequency attribute
          rip (str, optional): rip attribute
          domain (str, optional): domain attribute
          variable (str, optional): variable attribute
          period (str): a period, syntax as explained with :py:func:`climaf.period.init_period`
          variable (str, optional): version of the data; default to 'last'
        
        
        """
        # Should check following initializations w.r.t. relevant regexps
        self.project=    cdefault("project")   if project   is None else project
        self.model=      cdefault("model")     if model     is None else model
        self.experiment= cdefault("experiment")if experiment is None else experiment
        self.rip=        cdefault("rip")       if rip       is None else rip
        self.period=     cdefault("period")    if period    is None else period
        if (isinstance(self.period,str)) : self.period=init_period(self.period)
        self.frequency=  cdefault("frequency") if frequency is None else frequency
        self.domain=     cdefault("domain")    if domain    is None else domain
        self.variable=   cdefault("variable")  if variable  is None else variable
        self.version=    version
        self.fileVarName=self.variable
        #
        self.crs=self.buildcrs()
        # Some more stuff for looking for data location and organization for this very experiment
        self.register()

    def setperiod(self,period) :
        self.erase()
        self.period=period
        self.crs=self.buildcrs()
        self.register()
        
    def buildcrs(self,period=None):
        if period is None : period=self.period
        # Note : function 'ds' (far below) must be modified when buildcrs is modified
        s= "."
	if type(self.domain) is list : sdomain=`self.domain`
	else : sdomain=self.domain
        return "ds('"+self.project+s+self.model+s+self.experiment+s+self.rip+s+`period`+s+\
                  self.frequency+s+sdomain+s+self.variable+"')"

    def isLocal(self) :
        return(dataloc.isLocal(project=self.project, model=self.model, \
                               experiment=self.experiment, frequency=self.frequency))
    def isCached(self) :
        """ TBD : analyze if a remote dataset is locally cached
        
        """
        logging.error("classes.cdataset.isCached : TBD - remote datasets are not yet cached")
        rep=False
        return rep

    def oneVarPerFile(self):
        locs=dataloc.getlocs(project=self.project, model=self.model, experiment=self.experiment, \
                             frequency=self.frequency)
        return(all([org for org,freq,url in locs]))
    
    def periodIsFine(self):
        logging.debug("classes.cdataset.periodIsFine : always returns False, yet - TBD")
        return(False) 
        
    def domainIsFine(self):
        logging.debug("classes.cdataset.domainIsFine : a bit too simple yet (domain=='global')- TBD")
        return(self.domain == 'global') 
        
    def periodHasOneFile(self) :
        logging.debug("classes.cdataset.periodHasOneFIle : always returns False, yet - TBD")
        return(False) 

    def hasOneMember(self) :
        logging.debug("classes.cdataset.hasOneMember : always returns True, yet - TBD")
        return(True) 

    def selectFiles(self):
        """ Returns the list of (local) files which include the data for the dataset
        
        Method : depending on the data organization, select the relevant files for the
        requested period and variable
        Implicitly assumes that organization is the same for all 
        
        """
        return(dataloc.selectLocalFiles(project=self.project, model=self.model, \
                 experiment=self.experiment, frequency=self.frequency,\
                 variable=self.variable, period=self.period, version=self.version))
    def hasRawVariable(self) :
        """ Test local data files to tell if a dataset variable is actually included 
        in files (rather than being a derived, virtual variable)

        For the time being, returns False, which leads to always consider that variables
        declared as 'derived' actually are derived """
        logging.debug("dataset.hasRawVariable : TBD: actually test variables in files, rather than assuming that variable %s is virtual for dataset %s"\
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
                logging.error("ctree : __init__ : operand "+`o`+" is not a CliMAF object")
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
    Returns a dataset from its full Climate Reference Syntax.

    Also a shortcut for :py:meth:`~climaf.classes.cdataset`, when used with with only keywords arguments

    """
    # Note : muts be kept phased with self.crs defined in cdataset.init(), both for
    # function name and CRS syntax
    if len(args) > 1 :
        logging.error("climaf.classes.ds : must provide 0 or 1 positional arguments, not "+len(args))
        return None
    if (len(args)==0) : return cdataset(**kwargs) # Front-end to cdataset
    crs=args[0]
    # TBD : improve flexibility for provided CRS (i.e. optional fields) by analyzing w.r.t. known values
    fields=crs.split(".")
    project=fields[0]
    model=fields[1]
    experiment=fields[2]
    rip=fields[3]
    period=init_period(fields[4]) 
    frequency=fields[5]
    domain=fields[6]
    # domain may be the string representation of a list of corner coordinates, 
    # let us try to evaluate it
    try :
        domain=eval(domain)
    except :
        pass
    variable=fields[7]
    return cdataset(project=project,model=model,experiment=experiment,rip=rip,period=period,\
             frequency=frequency,domain=domain,variable=variable)

def test():
    logging.basicConfig(level=logging.DEBUG)
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
