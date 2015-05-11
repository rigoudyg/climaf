""" 
 Basic types and syntax for a CLIMAF Reference Syntax interpreter and driver
 This is a first protoype, where the interpreter is Python itself


 """
# Created : S.Senesi - 2014

import re, string

import dataloc
from period import init_period, cperiod
from clogging import clogger, dedent

#: Dictionnary of declared projects (type is cproject)
cprojects=dict()

#: Dictionnary of aliases dictionaries
aliases=dict()

#: Dictionnary of frequency names dictionaries
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
           project, experiment, variable, period, and domain**
          kwargs (dict) :
           can only be used with keyword ``sep`` or 
           ``separator`` for indicating the symbol separating
           facets in the dataset syntax. Defaults to ".". 

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
        experiment, model, rip, variable, frequency, realm, table, version


        **A number of projects are built-in**. See
          :py:mod:`~climaf.projects`
        
        A dataset in a cproject declared as ::

        >>> cproject("MINE","myfreq","myfacet",sep="_")

        will return ::

          ${project}_${experiment}_${variable}_${period}_${domain}_${myfreq}_${myfacet}

        and will have datasets represented as  e.g.::

          'MINE_hist_tas_[1980-1999]_global_decadal_gabu'

        while an example for built-in cproject CMIP5 will be::

          'CMIP5.historical.pr.[1980].global.monthly.CNRM-CM5.r1i1p1.mon.Amon.atmos.last'

        The attributes list should include all facets which are useful
        for distinguishing datasets from each other, and for computing
        datafile pathnames in the 'generic' organization (see
        :py:class:`~climaf.dataloc.dataloc`)

        A project can be declared as having non-standard variable
        names, or variabels that should undergo re-scaling (see
        :py:func:`~climaf.classes.calias`)

        A project can be declared as having non-standard frequency names (this is 
        used when accessing datafiles). see :py:func:`~climaf.classes.cfreqs`)

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
        if "sep"       in kwargs : self.separator=kwargs['sep']
        cprojects[name]=self
        self.crs=""
        # Build the pattern for the datasets CRS for this cproject
        for f in self.facets : 
            self.crs += "${%s}%s"%(f,self.separator)
        self.crs=self.crs[:-1]
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


#: Dictionnary storing user-default values for dataset attributes, used when defining a new dataset 
cdefaults=dict()

def cdef(attribute,value=None):
    """
    Set or get the default value for a CliMAF dataset attribute (as e.g. 'model', 'project' ...),
    for use by next calls to :py:class:`~climaf.classes.cdataset()` or to :py:func:`~climaf.classes.ds`

    Theres is no actual check that 'attribute' is a valid keyword for a call to ``ds`` or ``cdateset``

    Example::

    >>> cdefault('project','OCMPI5')
    >>> cdefault('frequency','monthly')

    """
    if value is None :
        if attribute in cdefaults.keys() :
            return cdefaults[attribute]
        else:
            return None
    else :
        cdefaults[attribute]=value

cdef("project","P")
cdef("model","M")
cdef("experiment","E")
cdef("rip","r1i1p1")
cdef("frequency","monthly")
cdef("domain","global")
cdef("table","*")
cdef("realm","*")
cdef("version","last")


# All CObject instances are registered in this directory :
cobjects=dict()

class cobject():
    def __init__(self):
        # crs is the string expression defining the object in the CLIMAF Reference Syntax
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

class cdataset(cobject):
    #def __init__(self,project=None,model=None,experiment=None,period=None,
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

        None of the attributes are mandatory, because all attributes
        defaults to the value set by
        :py:func:`~climaf.classes.cdefault`

        Some attributes have a special format or processing : 
        
        - period : see :py:func:`~climaf.period.init_period`

        - domain : allowed values are either 'global' or a list for
          latlon corners ordered as in : [ latmin, latmax, lonmin,
          lonmax ]
            
        - variable :  name of the geophysical variable ; this should be :

           - either a variable actually included in the datafiles,

           - or a 'derived' variable (see  :py:func:`~climaf.operators.derive` ),
             
           - or, an aliased variable name (see :py:func:`~climaf.classes.alias` )

        - in project CMIP5 , for triplets (frequency, rip, period, table )  : 
          if any is 'fx' (or 'r0i0p0 for rip), the others are forced to
          'fx' (resp. 'r0i0p0') too.

        Example, using no default value, and adressing some CMIP5 data ::

          >>  cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',\
              rip='r2i3p9', domain=[40,60,-10,20], variable='tas', period='1980-1989', version='last')
        
        
        """
        #
        self.crs=""
        if 'project' in kwargs : self.project=kwargs['project']
        else : self.project= cdef("project")   
        if self.project is None :
            raise Climaf_Classes_Error("Must provide a project (Can use cdef)")
        elif self.project not in cprojects :
            raise Climaf_Classes_Error("Dataset's project %s has not been described by a call to cproject()"%self.project)
        # Register facets values
        attval=dict()
        for facet in cprojects[self.project].facets :
            if facet in kwargs : val=kwargs[facet]
            else: val=cdef(facet)
            attval[facet]=val
        #
        # Special processing for CMIP5 fixed fields : handling redundancy in facets
        if (attval['project'] == 'CMIP5'):
            if ( attval['table']=='fx' or attval['period']=='fx' or 
                 attval['rip']=='r0i0p0' or attval['frequency']=='fx') :
                 attval['table']='fx' ; attval['period']='fx' 
                 attval['rip']='r0i0p0' ; attval['frequency']='fx'
        #
        errmsg=""
        for facet in cprojects[self.project].facets :
            if attval[facet] is None :
                e="Project %s needs facet %s. "%(self.project,facet)
                clogger.error(e)
                errmsg+=" "+e
        if errmsg != "" : raise Climaf_Classes_Error(errmsg)
        #
        for facet in kwargs :
            #clogger.debug("facet=%s, period=%s,kw=%s"%(facet,attval['period'],`kwargs`))
            # Facet specific processing
            if facet=='period' :
                if not isinstance(attval['period'],cperiod) :
                    try :
                        attval['period']=init_period(attval['period'])
                    except : raise Climaf_Classes_Error
            elif facet=='domain' and type(attval['domain']) is str and attval['domain'] != 'global' :
                # May be a list
                attval['domain']=eval(attval['domain'])
            # Check for typing or user's logic errors
            if not facet in cprojects[self.project].facets :
                e="Project %s doesn't have facet %s"%(self.project,facet)
                clogger.error(e)
                errmsg+=" "+e
        #print "Done with init_period in cdataset, period="+`attval["period"]`
        #
        if errmsg != "" : raise Climaf_Classes_Error(errmsg)
        # TBD : Next lines for backward compatibility, but should re-engineer 
        self.project   =attval['project']
        self.experiment=attval['experiment']
        self.variable= attval['variable']
        # alias is a n-plet : filevar, scale, offset, filenameVar, missing
        self.alias=varIsAliased(self.project,self.variable) 
        if type(attval['period']) is str :
            self.period    =init_period(attval['period'])
        else:
            self.period    =attval['period']
        self.domain    =attval['domain']
        #
        self.model    =attval.get('model',"*")
        self.frequency=attval.get('frequency',"*")
        #
        self.kvp=attval
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
        return(len(self.baseFiles().split(" ")) < 2)
        #clogger.debug("always returns False, yet - TBD")
        #return(False) 

    def hasOneMember(self) :
        clogger.debug("always returns True, yet - TBD")
        return(True) 

    def hasExactVariable(self):
        clogger.debug("always returns False, yet - TBD")
        return(False) 
    
    def missingIsOK(self):
        return self.alias.missing is None
    
    def baseFiles(self,force=False):
        """ Returns the list of (local) files which include the data for the dataset
        Use cached value unless called with arg force=True
        """
        if force or self.files is None :
            dic=self.kvp.copy()
            if self.alias : 
                filevar,scale,offset,units,filenameVar,missing=self.alias
                dic["variable"]=filevar
                dic["filenameVar"]=filenameVar
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
    def __init__(self, *members, **kwargs ) :
        """ 
        Create an ensemble from a series of objects, plus a list of labels
        """
        if kwargs.keys() != [ "labels" ] :
            raise Climaf_Classes_Error("Only kwargs 'label' is allowed")
        labels=kwargs["labels"]
        if not labels : 
            raise Climaf_Classes_Error("Must provide a list of labels for members")
        if len(labels) != len(members) :
            raise Climaf_Classes_Error("Must provide as many labels as members")
        self.members=members
        self.labels=labels
        self.crs=self.buildcrs()
        self.register()

    def buildcrs(self) :
        rep="cens("
        for m in self.members : rep+=`m`+","
        rep+="labels="+`self.labels`+")"
        return rep

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
                raise Climaf_Classes_Error("operand "+`o`+" is not a CliMAF object")
        self.crs=self.buildcrs()
        self.outputs=dict()
        self.alias=None
        self.register()

    def buildcrs(self, period=None, crsrewrite=None) :
        """ Builds the CRS expression representing applying OPERATOR on OPERANDS with PARAMETERS.
        Forces period downtree if provided
        A function for rewriting operand's CRS may be provided
        """
        # Operators are listed in alphabetical order; parameters too
        rep=self.operator+"("
        #
        ops=[ o for o in self.operands ]
        for op in ops :
            opcrs = op.buildcrs(period,crsrewrite)
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
        self.crs=self.buildcrs(period)
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
        self.alias=None
        self.register()

    def setperiod(self,period):
        self.erase()
        self.crs=self.father.crs.buildcrs(period)
        self.crs += "."+self.varname
        self.register()

    def buildcrs(self,period=None,crsrewrite=None):
        tmp= self.father.buildcrs(period)
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
    Returns a dataset from its full Climate Reference Syntax string. Example ::

     >>> ds('CMIP5.historical.pr.[1980].global.monthly.CNRM-CM5.r1i1p1.mon.Amon.atmos.last')

    Also a shortcut for :py:meth:`~climaf.classes.cdataset`, when used with with only 
    keywords arguments. Example ::

     >>> cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',\
              rip='r2i3p9', domain=[40,60,-10,20], variable='tas', period='1980-1989', version='last')

    """
    # Note : muts be kept phased with self.crs defined in cdataset.init(), both for
    # function name and CRS syntax
    if len(args) >1 :
        e="must provide either 0 or 1 positional arguments, not "+len(args)
        clogger.error(e)
        raise Climaf_Classes_Error(e)
    #clogger.debug("Entering , with args=%s, kwargs=%s"%(`args`,`kwargs`))
    if (len(args)==0) : return cdataset(**kwargs) # Front-end to cdataset
    crs=args[0]
    results=[]
    for cproj in cprojects : 
        try : dataset = cprojects[cproj].crs2ds(crs) 
        except Climaf_Classes_Error: dataset=None
        if (dataset) : results.append(dataset)
    if len(results) > 1 :
        e="CRS expressions %s is ambiguous projects %s"%(crs,`cprojects.keys()`)
        clogger.error(e)
        raise Climaf_Classes_Error(e)
    elif len(results) == 0 :
        e="CRS expressions %s is not valid for any project in %s"%(crs,`cprojects.keys()`)
        clogger.error(e)
        raise Climaf_Classes_Error(e)
        return None
    else : return results[0]

def cfreqs(project,dic) :
    """ 
    Allow to declare a dictionary specific to ``project`` for matching
    ``normalized`` frequency values to project-specific frequency values

    Normalized frequency values are : decadal, yearly, monthly, daily, 6h, 3h, fx

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

    Also allows to tell which variable name should be used when computing the
    filename for this variable in this project (for optimisation
    purpose);

    And that a given constant must be interpreted as a missing value

    ``variable`` may be a list. In that case, ``fileVariable`` and
    ``filenameVar``, if provided, should be parallel lists

    Example ::
    
    >>> calias('erai','tas','t2m',filenameVar='2T')
    >>> calias('erai','tas_degC','t2m',scale=1., offset=-273.15)  # scale and offset may be provided
    >>> calias('EM',[ 'sic', 'sit', 'sim', 'snd', 'ialb', 'tsice'], missing=1.e+20)
    
    """
    if not fileVariable : fileVariable =variable
    if not filenameVar  : filenameVar =fileVariable
    if project not in cprojects : 
        raise Climaf_Classes_Error("project %s is not known"%project)
    if project not in aliases : aliases[project]=dict()
    if type(variable)     is not list : variable    =[variable]
    if type(filenameVar)  is not list : filenameVar =[filenameVar]
    if type(fileVariable) is not list : fileVariable=[fileVariable]
    if type(units)        is not list : units    =[units]
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
    def __init__(self, widths_list=[], heights_list=[], 
                 fig_lines=None, orientation="portrait"):
        """
        Builds a CliMAF cpage object, which represents an array of figures

        Args:
         widths_list (list): the list of figure widths, i.e. the width 
           of each column
         heights_list (list): the list of figure heights, i.e. the height 
           of each line
         fig_line (a list of lists of figure objects): each sublist 
          of 'fig_lines' represents a line of figures
         orientation (str, optional): page's orientation, either 'portrait' 
          (default) or 'landscape'

        Example:

         Using no default value, to create a page with 2 columns and 3 lines::
        
          >>> fig=plotmap(tas_avg,crs='title')
          >>> my_page=cpage(widths_list=[0.2,0.8],heights_list=[0.33,0.33,0.33], fig_lines=[[None, fig],[fig, fig],[fig,fig]],orientation='landscape'))

        
        """
        self.widths_list=widths_list
        self.heights_list=heights_list
        self.fig_lines=fig_lines
        self.orientation=orientation
        if not self.widths_list :
            raise Climaf_cpage_Error("widths_list must be provided")
        if not self.heights_list :
            raise Climaf_cpage_Error("heights_list must be provided")
        if self.fig_lines is None :
            raise Climaf_cpage_Error("fig_lines must be provided")
        if not isinstance(self.fig_lines,list) :
            raise Climaf_cpage_Error("fig_lines must be a list of lists (each representing a line of figures)")
        if len(self.fig_lines)!=len(self.heights_list) :
            raise Climaf_cpage_Error("fig_lines must have same size than heights_list")
        for line in self.fig_lines:
            if not isinstance(line,list) :
                raise Climaf_cpage_Error("each element in fig_lines must be a list of figures")
            if len(line)!=len(self.widths_list) :
                raise Climaf_Classes_Error("each line in fig_lines must have same dimension as "
                                           "widths_list; pb for sublist "+`line`)
        self.crs=self.buildcrs()
        
    def buildcrs(self,crsrewrite=None):
        rep="cpage("+`self.widths_list`+","+`self.heights_list`+",["
        for line in self.fig_lines :
            rep+="["
            for f in line :
                if f : rep+=f.buildcrs(crsrewrite=crsrewrite)+","
                else : rep+=`None`+","
            rep+=" ],"; 
        rep+="], orientation='"+self.orientation+"')"
        rep=rep.replace(",]","]")
        rep=rep.replace(", ]","]")
        return rep

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
    cdef("rip","r1i1p1")
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
