""" 
CliMAF driver

There is quite a lot of things to document here. Maybe at a later stage ....

"""

# Created : S.Senesi - 2014

#Multi pour : ds.adressOF, cache.remoteRead, cstore, cache.cdrop, cache.hasIncludingTree, ceval_select, ceval_operator...

import os, os.path, re, posixpath, subprocess, time
from string import Template

# Climaf modules
import climaf
import classes
import cache
import operators
from clogging import clogger, indent as cindent, dedent as cdedent
from climaf.netcdfbasics import varOfFile
from climaf.period import init_period

# Declares an external operator used temporarily (until internal objects and operators are handled)
#operators.cscript('select' ,climaf.__path__[0]+'/scripts/mcdo.sh "" ${out} ${var} ${period} ${multins} ' )

def capply (climaf_operator, *operands, **parameters):
    """ Builds the object representing applying a CliMAF operator (script or function)
    
    Returns results as a list of CliMAF objects and stores them if auto-store is on
    """
    res=None
    if operands is None or operands[0] is None :
        clogger.debug("Operands is None")
        return None
    opds=map(str,operands)
    if climaf_operator in operators.scripts :
        #clogger.debug("applying script %s to"%climaf_operator + `opds` + `parameters`)
        res=capply_script(climaf_operator, *operands, **parameters)
        op=operators.scripts[climaf_operator]
        if op.outputFormat is None : ceval(res,userflags=op.flags)
    elif climaf_operator in operators.operators :
        clogger.debug("applying operator %s to"%climaf_operator + `opds` + `parameters`)
        res=capply_operator(climaf_operator,*operands, **parameters)
    else:
        clogger.error("%s is not a known operator nor script"%climaf_operator)
    return res

def capply_script (script_name, *operands, **parameters):
    """ Create object for application of a script to OPERANDS with keyword PARAMETERS."""

    if script_name not in operators.scripts :
        clogger.error("Script %s is not know. Consider declaring it with function 'cscript'",
                      script_name)
        return None
    script=operators.scripts[script_name]
    if len(operands) != script.inputs_number() : 
        clogger.error("Operator %s is "
	    "declared with %d input streams, while you provided %d. Get doc with 'help(%s)'"%(
            script_name,script.inputs_number(),len(operands), script_name ))
        return None
    rep=classes.ctree(script_name, script, *operands, **parameters)
    if rep is not None :
        #
        # TBD Analyze script inputs cardinality vs actual arguments
        #for op in operands :
        #
        # Create one child for each output
        defaultVariable=varOf(operands[0])
        #defaultPeriod=operands[0].period
        for outname in script.outputs :
            if outname is None :
                rep.variable=script.outputs[None]%defaultVariable
            else :
                son=classes.scriptChild(rep,outname)
                son.variable=script.outputs[outname]%defaultVariable
                rep.outputs[outname]=son
                setattr(rep,outname,son)
        # Check that all parameters to the call are expected by the script 
        for para in parameters :
            if re.match(r".*\{"+para+r"\}",script.command) is None :
                if re.match(r".*\{"+para+r"_iso\}",script.command) is None :
                    err="parameter %s is not expected by  script %s (which command is : %s)"%(para,script_name,script.command)
                    clogger.error(err)
                    return None
                    #raise Climaf_Driver_Error(err)
    #
    return rep

def capply_operator (climaf_operator, *operands, **parameters):
    """ Create object for application of an internal OPERATOR to OPERANDS with keywords PARAMETERS.

    """
    clogger.error("Not yet developped - TBD")
    return None
    

def ceval(cobject,
          userflags=None,
          format="MaskedArray",deep=None, derived_list=[], recurse_list=[]) :
    """ 
    Actually evaluates a CliMAF object, either as an in-memory data structure or
    as a string of filenames (which either represent a superset or exactly includes
    the desired data)

    - with arg deep=True , re-evaluates all components
    - with arg deep=False, re-evaluates top level operation
    - without arg deep   , use cached values as far as possible

    arg derived_list is the list of variables that have been considered as 'derived'
    (i.e. not natives) in upstream evaluations. It avoids to loop endlessly
    """
    if format != 'MaskedArray' and format != 'file' and format != 'png' :
        err='Allowed formats yet are : "object", "file" and "png"'
        clogger.error(err); raise Climaf_Driver_Error(err)
    #
    if userflags is None : userflags=operators.scriptFlags()
    #
    # Next check is too crude for dealing with use of operator 'select'
    #if cobject.crs in recurse_list :
    #    clogger.critical("INTERNAL ERROR : infinite loop on object: "+cobject.crs)
    #    return None
    cindent()
    if isinstance(cobject,classes.cdataset):
        recurse_list.append(cobject.crs)
        clogger.debug("Evaluating dataset operand " + cobject.crs + "having kvp=" + `cobject.kvp`)
        ds=cobject
        if ds.isLocal() or ds.isCached() :
            clogger.debug("Dataset %s is local or cached "%ds )
            #  if the data is local, then
            #   if the user can select the data and aggregate time, and requested format is
            #     'file' return the filenames
            #   else : read the data, create a cache file for that, and recurse
            # Go to derived variable evaluation if appicable
            if ds.variable in operators.derived_variables and not ds.hasRawVariable() :
                if ds.variable in derived_list :
                    cdedent()
                    err="Loop detected while evaluating derived variable "+\
                                  ds.variable + " " + `derived_list`
                    clogger.error(err); raise Climaf_Driver_Error(err)
                derived=derive_variable(ds)
                clogger.debug("evaluating derived variable %s as %s"%\
                                  (ds.variable,`derived`))
                derived_value=ceval(derived, format=format, deep=deep, 
                                    userflags=userflags,
                                    derived_list=derived_list.append(ds.variable),
                                    recurse_list=recurse_list)
                if derived_value : 
                    clogger.debug("succeeded in evaluating derived variable %s as %s"%\
                                      (ds.variable,`derived`))
                    set_variable(derived_value, ds.variable, format=format)
                cdedent()
                return(derived_value)
            elif ((userflags.canSelectVar or ds.oneVarPerFile()) and \
                (userflags.canSelectTime or ds.periodIsFine()) and \
                (userflags.canSelectDomain or ds.domainIsFine()) and \
                (userflags.canAggregateTime or ds.periodHasOneFile()) and 
                #(userflags.doSqueezeMembers or ds.hasOneMember()) and 
                #(userflags.canOffsetScale or ds.hasExactVariable()) and 
                (format == 'file')) :
                clogger.debug("Delivering file set or sets is OK for the target use")
                cdedent()
                return(ds.baseFiles()) # a single string with all filenames,
                               #or a list of such strings in case of ensembles
            else:
                clogger.debug("Must subset and/or aggregate and/or select "+
                              "var from data files and/or get data, or provide object result")
                ## extract=cread(ds)
                ## clogger.debug(" Done with subsetting and caching data files")
                ## cstore(extract) # extract should include the dataset def
                ## return ceval(extract,userflags,format)
                clogger.debug("Fetching/selection/aggregation is done using an "+
                          "external script for now - TBD")
                #ds.setOffsetScale()
                extract=capply('select',ds)
                if extract is None :
                    clogger.errorerr="Cannot access dataset" + `ds`
                    clogger.error(err); raise Climaf_Driver_Error(err)
                    cdedent()
                rep=ceval(extract,userflags=userflags,format=format,deep=deep,recurse_list=recurse_list)
                cdedent()
                return rep
        else :
            # else (non-local and non-cached dataset)
            #   if the user can access the dataset by one of the dataset-specific protocols
            #   then assume it can also select on time and provide it with the address
            #   else : fetch the relevant selection of the data, and store it in cache
            clogger.debug("Dataset is remote " )
            if (userflags.canOpenDap and format == 'file' ) :
                clogger.debug("But user can OpenDAP " )
                cdedent()
                return(ds.adressOf())
            else :
                clogger.debug("Must remote read and cache " )
                # Assume remoteRead fetches the strict minimum 
                extract=cache.remoteRead(ds)
                if (format == 'file' ) :
                    cachefile=cstore(extract)
                    clogger.debug("And provide cache file reference " )
                    cdedent()
                    return cachefile
                else :
                    clogger.debug("And provide in-memory object " )
                    cdedent()
                    return(extract)
    #
    elif isinstance(cobject,classes.ctree) or isinstance(cobject,classes.scriptChild) : 
        #clogger.debug("Evaluating object operand %s"%`cobject`)
        recurse_list.append(cobject.crs)
        clogger.debug("Evaluating compound object : " + `cobject`)
        if (deep is not None) : cache.cdrop(cobject.crs)
        clogger.debug("Searching cache for exact object : " + `cobject`)
        filename=cache.hasExactObject(cobject)
        #filename=None
        if filename :
            clogger.info("Object found in cache: %s is at %s:  "%(cobject.crs,filename))
            if format=='file' : 
                cdedent()
                return filename
            else:
                cdedent()
                return cread(filename)
        clogger.debug("Searching cache for including object for : " + `cobject`)
        it,altperiod=cache.hasIncludingObject(cobject)
        #clogger.debug("Finished with searching cache for including object for : " + `cobject`)
        #it=None
        if it :
            clogger.info("Including object found in cache : %s"%(it.crs))
            clogger.info("Selecting "+`cobject`+" out of it")
            # Just select (if necessary for the user) the portion relevant to the request
            rep=ceval_select(it,cobject,userflags,format,deep,derived_list, recurse_list)
            cdedent()
            return rep
        #
        clogger.debug("Searching cache for begin  object for : " + `cobject`)
        it,comp_period=cache.hasBeginObject(cobject) 
        clogger.debug("Finished with searching cache for begin  object for : " + `cobject`)
        #it=None
        if it : 
            clogger.info("partial result found in cache for %s : %s"%\
                                  (cobject.crs,it.crs))
            begcrs=it.crs
            # Turn object for begin in complement object for end, and eval it
            it.setperiod(comp_period)
            ceval(it,userflags,format,deep,derived_list,recurse_list)
            if (format == 'file') :
                rep=cache.complement(begcrs,it.crs,cobject.crs)
                cdedent()
                return rep
            else :
                clogger.debug("cannot yet complement except for files")
                cdedent()
                return(None)
        #
        clogger.info("nothing relevant found in cache for %s"%cobject.crs)
        if deep==False : deep=None
        if isinstance(cobject,classes.ctree)  :
            # the cache doesn't have a similar tree, let us recursively eval subtrees
            # TBD  : analyze if the dataset is remote and the remote place 'offers' the operator
            if cobject.operator in operators.scripts :
                file=ceval_script(cobject,deep,recurse_list=recurse_list) # Does return a filename, or list of filenames
                if ( format == 'file' ) : 
                    cdedent()
                    return (file)
                else : 
                    cdedent()
                    return cread(file)
            elif cobject.operator in operators.operators :
                obj=ceval_operator(cobject,deep)
                if (format == 'file' ) : 
                    rep=cstore(obj)
                    cdedent()
                    return rep
                else : 
                    cdedent()
                    return(obj)
            else : 
                err="operator %s is not a script nor known operator",str(cobject.operator)
                clogger.error(err); raise Climaf_Driver_Error(err)
        else :
            # isinstance(cobject,classes.scriptChild) should be True
            # Force evaluation of 'father' script
            if ceval_script(cobject.father,deep,recurse_list=recurse_list)  is not None :
                # Re-evaluate, which should succeed using cache
                rep=ceval(cobject,userflags,format,deep,recurse_list=recurse_list)
                cdedent()
                return rep
            else :
                cdedent()
                err="generating script aborted for "+cobject.father.crs
                clogger.error(err); raise Climaf_Driver_Error(err)
    elif isinstance(cobject,str) :
        clogger.debug("Evaluating object from crs : %s"%cobject)
        cdedent()
        err="Evaluation from CRS is not yet implemented ( %s )"%cobject
        clogger.error(err); raise Climaf_Driver_Error(err)
    else :
        cdedent()
        err="argument " +`cobject`+" is not (yet) managed"
        clogger.error(err); raise Climaf_Driver_Error(err)



def ceval_script (scriptCall,deep,recurse_list=[]):
    """ Actually applies a CliMAF-declared script on a script_call object 
    
    Prepare operands as fiels and build command from operands and parameters list
    Assumes that scripts are described in dictionnary 'scripts'  by templates as
    documented in operators.cscript
    
    Returns a CLiMAF cache data filename
    """
    script=operators.scripts[scriptCall.operator]
    template=Template(script.command)

    # Evaluate input data 
    dict_invalues=dict()
    sizes=[]
    for op in scriptCall.operands :
        inValue=ceval(op,userflags=script.flags,format='file',deep=deep,
                      recurse_list=recurse_list)
        if inValue is None or inValue is "" : return None
        if isinstance(inValue,list) : size=len(inValue)
        else : size=1
        sizes.append(size)
        dict_invalues[op]=inValue
    # Check consistency regarding number of members , considering that input data is either a string with
    # multiple files (which together cover a time period and are
    # called a 'set' of files) or a list of such strings/sets (if the
    # input data is an ensemble); we check that either all input
    # streams have the same number of members (i.e. the lists of files
    # sets have the same size among all input data streams ) or all
    # but one are single member ensembles (i.e.  only one is a list)
    # nbSize1=0
    # nbSizeMax=0
    # rank=0
    # for s in sizes : 
    #     if (s == 1)          : nbSize1 += 1
    #     if (s == max(sizes)) : 
    #         nbSizeMax += 1
    #         maxRank=rank
    #     rank += 1
    #     if (s != 1) and (s != max(sizes)) :
    #       clogger.error("Cannot mix ensemble sizes : size of ensemble # %d is not 1 nor equals to max ensemble size (%d) in %s"%\
    #                         (rank,max(sizes),scriptCall.crs))
    #       return(None)
    # if ( nbSizeMax != 1 ) :
    #     if ( nbSizeMax != len(sizes)) :
    #       clogger.error("Cannot mix ensemble sizes : more than one operands has a size > 1, while some have size 1 in %s"%scriptCall.crs)
    #       return(None)

    # Replace input data placeholders with filenames
    subdict=dict()
    opscrs=""
    if 0 in script.inputs :
        label,multiple,serie=script.inputs[0]
        op=scriptCall.operands[0]
        infile=dict_invalues[op]
        if not all(map(os.path.exists,infile.split(" "))) :
            err="Internal error : some input file does not exist among %s:"%(infile)
            clogger.error(err)
            raise Climaf_Driver_Error(err)
        subdict[ label ]='"'+infile+'"'
        subdict["var"]='"'+varOf(op)+'"'
        per=timePeriod(op)
        if per.fx :
            subdict["period"]='""'
            subdict["period_iso"]='""'
        else:
            subdict["period"]='"'+str(per)+'"'
            subdict["period_iso"]='"'+per.iso()+'"'
        subdict["domain"]='"'+domainOf(op)+'"'
    i=0
    for op in scriptCall.operands :
        opscrs += op.crs+" - "
        infile=dict_invalues[op]
        if not all(map(os.path.exists,infile.split(" "))) :
            err="Internal error : some input file does not exist among %s:"%(infile)
            clogger.error(err)
            raise Climaf_Driver_Error(err)
        i+=1
        if ( i> 1 or 1 in script.inputs) :
            label,multiple,serie=script.inputs[i]
            subdict[ label ]='"'+infile+'"'
            # Provide the name of the variable in input file if script allows for
            subdict["var_%d"%i]='"'+varOf(op)+'"'
            # Provide period selection if script allows for
            per=timePeriod(op)
            if per.fx :
                subdict["period_%d"%i]='""'
                subdict["period_iso_%d"%i]='""'
            else :
                subdict["period_%d"%i]='"'+str(per)+'"'
                subdict["period_iso_%d"%i]='"'+per.iso()+'"'
            subdict["domain_%d"%i]='"'+domainOf(op)+'"'
    clogger.debug("subdict for operands is "+`subdict`)
    # substituion is deffered after scriptcall parameters evaluation, which may
    # redefine e.g period
    #
    # Provide one cache filename for each output and instantiates the command accordingly
    if script.outputFormat is not None :
        # Compute a filename for each ouptut
        # Un-named main output
        main_output_filename=cache.generateUniqueFileName(scriptCall.crs,
                                                          format=script.outputFormat)
        subdict["out"]=main_output_filename
        subdict["out_"+scriptCall.variable]=main_output_filename
        # Named outputs
        for output in scriptCall.outputs:
            subdict["out_"+output]=cache.generateUniqueFileName(scriptCall.crs+"."+output,\
                                                         format=script.outputFormat)
    # Account for script call parameters
    for p in scriptCall.parameters : 
        #clogger.debug("processing parameter %s=%s"%(p,scriptCall.parameters[p]))
        subdict[p]=scriptCall.parameters[p]
        if p=="period" :
            subdict["period_iso"]=init_period(scriptCall.parameters[p]).iso()
    if 'crs' not in scriptCall.parameters : subdict["crs"]=opscrs.replace("'","")

    # Substitute all args, with special case of NCL convention for passing args
    if (script.command.split(' ')[0][-3:]=="ncl") :
        for o in subdict :
            if isinstance(subdict[o],str) :
                if subdict[o][0] != "\"" :
                    subdict[o]="\"" + subdict[o] + "\""
                subdict[o].replace("'","")
    template=template.safe_substitute(subdict)
    #
    # Allow script call not to use all formal arguments
    template=re.sub(r"(\w*=)?\$\{\w*\}",r"",template)
    #
    if (script.command.split(' ')[0][-3:]=="ncl") :
        template=re.sub(r'([^=\s]*)=([^=\s\"]+|\"[^\"]*\")',r"\1='\2'",template)
    # Launch script using command, and check termination 
    #command="PATH=$PATH:"+operators.scriptsPath+template+fileVariables
    command="echo '\n\nstdout and stderr of script call :\n\t "+template+\
             "\n\n'> scripts.out  ; "+ template+\
             " >> scripts.out 2>&1"
    tim1=time.time()
    clogger.info("Launching command:"+template)
    # Timing
    # TBD : Should use process.check_output and display stderr when exit is non-0
    if ( subprocess.call(command, shell=True) == 0):
        if script.outputFormat is not None :
            # Tagging output files with their CliMAF Reference Syntax definition
            # Un-named main output
            ok = cache.register(main_output_filename,scriptCall.crs)
            # Named outputs
            for output in scriptCall.outputs:
                ok = ok and cache.register(subdict["out_"+output],scriptCall.crs+"."+output)
            if ok : 
                duration=time.time() - tim1
                clogger.info(("Done in %.1g s with command:"+template) % 
                             duration)
                return main_output_filename
            else :
                err="Some output missing when executing : %s. \nSee scripts.out"%template
                clogger.error(err)
                raise Climaf_Driver_Error(err)
        else :
            clogger.debug("script %s has no output"%script.name)
    else:
        err="See scripts.out for analyzing script call failure for : %s "%template
        clogger.error(err)
        raise Climaf_Driver_Error(err)
    return None


def timePeriod(cobject) :
    """ Returns a time period for a CliMAF object : if object is a dataset, returns
    its time period, otherwise returns time period of first operand
    """
    if isinstance(cobject,classes.cdataset) : return cobject.period
    elif isinstance(cobject,classes.ctree) :
        clogger.debug("for now, timePeriod logic for scripts output is basic (1st operand) - TBD")
        return timePeriod(cobject.operands[0])
    elif isinstance(cobject,classes.scriptChild) :
        clogger.debug("for now, timePeriod logic for scriptChilds is basic - TBD")
        return timePeriod(cobject.father)
    else : clogger.error("unkown class for argument "+`cobject`)
                  
def domainOf(cobject) :
    """ Returns a domain for a CliMAF object : if object is a dataset, returns
    its domain, otherwise returns domain of first operand
    """
    if isinstance(cobject,classes.cdataset) : 
	if type(cobject.domain) is list :
            rep=""
            for coord in cobject.domain[0:-1] : rep=r"%s%d,"%(rep,coord)
            rep="%s%d"%(rep,cobject.domain[-1])
            return(rep)
	else : 
	    if cobject.domain == "global" : return ""
	    else : return(cobject.domain)
    elif isinstance(cobject,classes.ctree) :
        clogger.debug("For now, domainOf logic for scripts output is basic (1st operand) - TBD")
        return domainOf(cobject.operands[0])
    elif isinstance(cobject,classes.scriptChild) :
        clogger.debug("For now, domainOf logic for scriptChilds is basic - TBD")
        return domainOf(cobject.father)
    else : clogger.error("Unkown class for argument "+`cobject`)
                  
def varOf(cobject) :
    """ Returns the variable for a CliMAF object : if object is a dataset, returns
    its 'variable' property, otherwise returns variable of first operand
    """
    if isinstance(cobject,classes.cdataset) : return cobject.variable
    elif getattr(cobject,"variable",None) : 
        return getattr(cobject,"variable",None) 
    elif isinstance(cobject,classes.ctree) :
        clogger.debug("for now, varOf logic is basic (1st operand) - TBD")
        return varOf(cobject.operands[0])
    else : clogger.error("Unkown class for argument "+`cobject`)

                  
def ceval_select(includer,included,userflags,format,deep,derived_list,recurse_list) :
    """ Extract object INCLUDED from (existing) object INCLUDER,
    taking into account the capability of the user process (USERFLAGS)
    and the required delivering FORMAT(file or object)
    """
    if format=='file' : 
        if userflags.canSelectTime or userflags.canSelectDomain:
            clogger.debug("TBD - should do smthg smart when user can select time or domain")
            #includer.setperiod(included.period)
        incperiod=timePeriod(included)
	clogger.debug("extract sub period %s out of %s"%(`incperiod`,includer.crs))
        extract=capply('select',includer, period=`incperiod`)
        objfile=ceval(extract,userflags,'file',deep,derived_list,recurse_list)
	if objfile :
            crs=includer.buildcrs(incperiod)
            return(cache.rename(objfile,crs))
        else :
            clogger.critical("Cannot evaluate "+`extract`)
    else :
        clogger.error("Can yet process only files - TBD")


def cread(datafile,varname=None):
    import re
    if not datafile : return(None)
    if re.findall(".png$",datafile) :
        subprocess.Popen(["display",datafile,"&"])
    elif re.findall(".nc$",datafile) :
        clogger.debug("reading NetCDF file %s"%datafile)
        if varname is None: varname=varOfFile(datafile)
        if varname is None: return(None)
        from Scientific.IO.NetCDF import NetCDFFile as ncf
        fileobj=ncf(datafile)
        #import netCDF4
        #fileobj=netCDF4.Dataset(datafile)
        # Note taken from the CDOpy developper : .data is not backwards 
        # compatible to old scipy versions, [:] is
        data=fileobj.variables[varname][:]
        fillv=fileobj.variables[varname]._FillValue
        import numpy.ma
        rep= numpy.ma.array(data,mask = data==fillv)
        fileobj.close()
        return(rep)
    else :
        clogger.error("cannot yet handle %s"%datafile)
        return None

def cview(datafile):
    if re.findall(".png$",datafile) :
        subprocess.Popen(["display",datafile,"&"])
    else :
        clogger.error("cannot yet handle %s"%datafile)
        return None

def derive_variable(ds):
    """ Assuming that variable of DS is a derived variable, returns the CliMAF object
    representing the operation needed to compute it (using information in dict 
    operators.derived_variable
    """
    if not isinstance(ds,classes.cdataset):
        err="arg is not a dataset"
        clogger.error(err) ; raise Climaf_Driver_Error(err)
    if ds.variable not in operators.derived_variables :
        err="%s is not a derived variable"%ds.variable
        clogger.error(err) ; raise Climaf_Driver_Error(err)
    op,outname,inVarNames,params=operators.derived_variables[ds.variable]
    inVars=[]
    for varname in inVarNames :
        dic=ds.kvp.copy()
        dic['variable']=varname
        inVars.append(classes.cdataset(**dic))
    father=capply(op,*inVars,**params)
    if (outname == "out"): rep=father
    else : rep=scriptChild(father,outname)
    rep.variable=ds.variable
    return rep

def set_variable(obj, varname, format) :
    """ Change to VARNAME the variable name for OBJ, which FORMAT 
    maybe 'file' or 'MaskedArray'. 
    Also set the variable long_name using CF convention (TBD)
    """
    if obj is None : return None
    long_name=CFlongname(varname)
    if (format=='file') :
        oldvarname=varOfFile(obj)
        command="ncrename -v %s,%s %s >/dev/null 2>&1"%(oldvarname,varname,obj)
        if ( os.system(command) != 0 ) :
            clogger.error("Issue with changing varname to %s in %s"%(varname,obj))
            return None
        clogger.debug("Varname changed to %s in %s"%(varname,obj))
        command="ncatted -a long_name,%s,o,c,%s %s"%(varname,long_name,obj)
        if ( os.system(command) != 0 ) :
            clogger.error("Issue with changing long_name for var %s in %s"%
                          (varname,obj))
            return None
        return True
    elif (format=='MaskedArray') :
        clogger.warning('TBD - Cannot yet set the varname for MaskedArray')
    else :
        clogger.error('Cannot handle format %s'%format)
    

def CFlongname(varname) :
    """ Returns long_name of variable VARNAME after CF convention 
    """
    return("TBD_should_improve_function_climaf.driver.CFlongname") 

class Climaf_Driver_Error(Exception):
    pass

