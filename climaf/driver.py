""" 
CliMAF driver

There is quite a lot of things to document here. Maybe at a later stage ....

"""
from __future__ import print_function

# Created : S.Senesi - 2014

import sys,os, os.path, re, posixpath, subprocess, time, shutil, copy
from string import Template

# Climaf modules
import climaf
import classes
import cache
import operators
import cmacro
from clogging import clogger, indent as cindent, dedent as cdedent
from climaf.netcdfbasics import varOfFile
from climaf.period import init_period

def capply(climaf_operator, *operands, **parameters):
    """ Builds the object representing applying a CliMAF operator (script, function or macro)
    
    Returns results as a list of CliMAF objects and stores them if auto-store is on
    """
    res=None
    if operands is None or operands[0] is None :
        raise Climaf_Driver_Error("Operands is None")
    opds=map(str,operands)
    if climaf_operator in operators.scripts :
        #clogger.debug("applying script %s to"%climaf_operator + `opds` + `parameters`)
        res=capply_script(climaf_operator, *operands, **parameters)
        # Evaluate object right now if there is no output to manage
        op=operators.scripts[climaf_operator]
        if op.outputFormat is None : ceval(res,userflags=copy.copy(op.flags))
    elif climaf_operator in cmacro.cmacros :
        if (len(parameters) > 0) :
            raise Climaf_Driver_Error("Macros cannot be called with keyword args")
        clogger.debug("applying macro %s to"%climaf_operator + `opds` )
        res=cmacro.instantiate(cmacro.cmacros[climaf_operator],*operands)
    elif climaf_operator in operators.operators :
        clogger.debug("applying operator %s to"%climaf_operator + `opds` + `parameters`)
        res=capply_operator(climaf_operator,*operands, **parameters)
    else:
        clogger.error("%s is not a known operator nor script"%climaf_operator)
    return res

def capply_script (script_name, *operands, **parameters):
    """ Create object for application of a script to OPERANDS with keyword PARAMETERS."""
    
    if script_name not in operators.scripts :
        raise Climaf_Driver_Error("Script %s is not know. Consider declaring it "
                                  "with function 'cscript'", script_name)
    script=operators.scripts[script_name]
    if len(operands) != script.inputs_number() : 
        raise Climaf_Driver_Error("Operator %s is "
                                  "declared with %d input streams, while you provided %d. Get doc with 'help(%s)'"%(
                script_name,script.inputs_number(),len(operands), script_name ))
    #
    # Check that all parameters to the call are expected by the script 
    for para in parameters :
        if re.match(r".*\{"+para+r"\}",script.command) is None :
            if re.match(r".*\{"+para+r"_iso\}",script.command) is None :
                if para != 'member_label' :
                    raise Climaf_Driver_Error("parameter '%s' is not expected by script %s"
                                          "(which command is : %s)"%(para,script_name,script.command))
    #
    # Check that only first operand can be an ensemble
    opscopy=[ o for o in operands ]
    opscopy.remove(opscopy[0])
    for op in opscopy  :
        if isinstance(op,classes.cens ):
            raise Climaf_Driver_Error("Cannot yet have an ensemble as operand except as first one")
    # 
    #print "op(0)="+`operands[0]`
    #print "script=%s , script.flags.commuteWithEnsemble="%script_name+`script.flags.commuteWithEnsemble`
    if (isinstance(operands[0],classes.cens) and script.flags.commuteWithEnsemble) :
        # Must iterate on members
        reps=[]
        for member,label in zip(operands[0].members,operands[0].labels) :
            clogger.debug("processing member "+`member`)
            params=parameters.copy()
            params["member_label"]=label
            reps.append(maketree(script_name, script, member, *opscopy, **params))
        return(classes.cens(operands[0].labels,*reps))
    else: 
        return(maketree(script_name, script, *operands, **parameters))
            
def maketree(script_name, script, *operands, **parameters):
    rep=classes.ctree(script_name, script, *operands, **parameters)
    # TBD Analyze script inputs cardinality vs actual arguments
    # Create one child for each output
    defaultVariable=varOf(operands[0])
        #defaultPeriod=operands[0].period
    for outname in script.outputs :
        if outname is None  or outname=='' :
            if "%s" in script.outputs[''] :
                rep.variable=script.outputs['']%defaultVariable
            else:
                rep.variable=script.outputs['']
        else :
            son=classes.scriptChild(rep,outname)
            if "%s" in script.outputs[outname] :
                son.variable=script.outputs[outname]%defaultVariable
            else:
                son.variable=script.outputs[outname]
            rep.outputs[outname]=son
            setattr(rep,outname,son)
    return rep

def capply_operator (climaf_operator, *operands, **parameters):
    """ 
    Create object for application of an internal OPERATOR to OPERANDS with keywords PARAMETERS.
    
    """
    clogger.error("Not yet developped - TBD")
    return None
    

def ceval(cobject, userflags=None, format="MaskedArray",
          deep=None, derived_list=[], recurse_list=[]) :
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
	raise Climaf_Driver_Error('Allowed formats yet are : "object", "file" and "png"')
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
            #if ds.variable in operators.derived_variables and not ds.hasRawVariable() :
            if operators.is_derived_variable(ds.variable,ds.project) :
                if ds.variable in derived_list :
                    raise Climaf_Driver_Error("Loop detected while evaluating"
                         "derived variable "+ ds.variable + " " + `derived_list`)
                derived=derive_variable(ds)
                clogger.debug("evaluating derived variable %s as %s"%\
                                  (ds.variable,`derived`))
                derived_value=ceval(derived, format=format, deep=deep, 
                                    userflags=userflags,
                                    derived_list=derived_list+[ds.variable],
                                    recurse_list=recurse_list)
                if derived_value : 
                    clogger.debug("succeeded in evaluating derived variable %s as %s"%\
                                      (ds.variable,`derived`))
                    set_variable(derived_value, ds.variable, format=format)
                cdedent()
                return(derived_value)
            elif ((userflags.canSelectVar   or ds.oneVarPerFile()   ) and \
                (userflags.canSelectTime    or ds.periodIsFine()    ) and \
                (userflags.canSelectDomain  or ds.domainIsFine()    ) and \
                (userflags.canAggregateTime or ds.periodHasOneFile()) and \
                (userflags.canAlias         or ds.hasExactVariable()) and \
                (userflags.canMissing       or ds.missingIsOK())      and \
                #(userflags.doSqueezeMembers or ds.hasOneMember()) and 
                (format == 'file')) :
                clogger.debug("Delivering basefiles is OK for the target use")
                cdedent()
                rep=ds.baseFiles()
                if not rep : raise Climaf_Driver_Error("No file found for %s"%`ds`)
                return(rep) # a single string with all filenames,
                               #or a list of such strings in case of ensembles
            else:
                clogger.debug("Must subset and/or aggregate and/or select "+
                              "var from data files and/or get data, or provide object result")
                ## extract=cread(ds)
                ## clogger.debug(" Done with subsetting and caching data files")
                ## cstore(extract) # extract should include the dataset def
                ## return ceval(extract,userflags,format)
                clogger.debug("Fetching/selection/aggregation is done using an external script for now - TBD")
                extract=capply('select',ds)
                if extract is None : raise Climaf_Driver_Error("Cannot access dataset" + `ds`)
                rep=ceval(extract,userflags=userflags,format=format)
                userflags.unset_selectors()
                cdedent()
                return rep
        else :
            # else (non-local and non-cached dataset)
            #   if the user can access the dataset by one of the dataset-specific protocols
            #   then assume it can also select on time and provide it with the address
            #   else : fetch the relevant selection of the data, and store it in cache
            clogger.debug("Dataset is remote " )
            if (userflags.canOpendap and format == 'file' ) :
                clogger.debug("But user can OpenDAP " )
                cdedent()
                return(ds.adressOf())
            else :
                clogger.debug("Must remote read and cache " )
                rep=ceval(capply('remote_select',ds),userflags=userflags,format=format)
                userflags.unset_selectors()
                cdedent()
                return rep
    #
    elif isinstance(cobject,classes.ctree) or isinstance(cobject,classes.scriptChild) or \
             isinstance(cobject,classes.cpage) or isinstance(cobject,classes.cens) : 
        recurse_list.append(cobject.buildcrs())
        clogger.debug("Evaluating compound object : " + `cobject`)
        #################################################################
        if (deep is not None) : cache.cdrop(cobject.crs)
        #
        clogger.debug("Searching cache for exact object : " + `cobject`)
        #################################################################
        filename=cache.hasExactObject(cobject)
        #filename=None
        if filename :
            clogger.info("Object found in cache: %s is at %s:  "%(cobject.crs,filename))
            cdedent()
            if format=='file' : return filename
            else: return cread(filename,varOf(cobject))
        if not isinstance(cobject,classes.cpage) and not isinstance(cobject,classes.cens) :
            #
            clogger.debug("Searching cache for including object for : " + `cobject`)
            ########################################################################
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
            ########################################################################
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
                else : raise Climaf_Driver_Error("cannot yet complement except for files")
            #
            clogger.info("nothing relevant found in cache for %s"%cobject.crs)
        #
        if deep==False : deep=None
        if isinstance(cobject,classes.ctree)  :
            #
            # the cache doesn't have a similar tree, let us recursively eval subtrees
            ##########################################################################
            # TBD  : analyze if the dataset is remote and the remote place 'offers' the operator
            if cobject.operator in operators.scripts :
                file=ceval_script(cobject,deep,recurse_list=recurse_list) # Does return a filename, or list of filenames
                cdedent()
                if ( format == 'file' ) : return (file)
                else : return cread(file,varOf(cobject))
            elif cobject.operator in operators.operators :
                obj=ceval_operator(cobject,deep)
                cdedent()
                if (format == 'file' ) : 
                    rep=cstore(obj) ; return rep
                else : return(obj)
            else : 
                raise Climaf_Driver_Error("operator %s is not a script nor known operator",str(cobject.operator))
        elif isinstance(cobject,classes.scriptChild) :
            # Force evaluation of 'father' script
            if ceval_script(cobject.father,deep,recurse_list=recurse_list)  is not None :
                # Re-evaluate, which should succeed using cache
                rep=ceval(cobject,userflags,format,deep,recurse_list=recurse_list)
                cdedent()
                return rep
            else :
                raise Climaf_Driver_Error("generating script aborted for "+cobject.father.crs)
        elif isinstance(cobject,classes.cpage) :
            file=cfilePage(cobject, deep, recurse_list=recurse_list)
            cdedent()
            if ( format == 'file' ) : return (file)
            else : return cread(file)
        elif isinstance(cobject,classes.cens) :
            rep=[]
            for member in cobject.members :
                rep.append(ceval(member,copy.copy(userflags),format,deep,recurse_list=recurse_list))
            if (format=="file") : return(reduce(lambda x,y : x+" "+y, rep))
            else : return rep
        else :
            raise Climaf_Driver_Error("Internal logic error")
    elif isinstance(cobject,str) :
        clogger.debug("Evaluating object from crs : %s"%cobject)
        raise Climaf_Driver_Error("Evaluation from CRS is not yet implemented ( %s )"%cobject)
    else :
        raise Climaf_Driver_Error("argument such as " +`cobject`+" are not (yet) managed")



def ceval_script (scriptCall,deep,recurse_list=[]):
    """ Actually applies a CliMAF-declared script on a script_call object 
    
    Prepare operands as fiels and build command from operands and parameters list
    Assumes that scripts are described in dictionary 'scripts'  by templates as
    documented in operators.cscript
    
    Returns a CLiMAF cache data filename
    """
    script=operators.scripts[scriptCall.operator]
    template=Template(script.command)

    # Evaluate input data 
    dict_invalues=dict()
    sizes=[]
    for op in scriptCall.operands :
        inValue=ceval(op,userflags=scriptCall.flags,format='file',deep=deep,
                      recurse_list=recurse_list)
        if inValue is None or inValue is "" :
            raise Climaf_Driver_Error("When evaluating %s : value for %s is None"\
                                      %(scriptCall.script,`op`))
        if isinstance(inValue,list) : size=len(inValue)
        else : size=1
        sizes.append(size)
        dict_invalues[op]=inValue
    #
    # Replace input data placeholders with filenames
    subdict=dict()
    opscrs=""
    if 0 in script.inputs :
        label,multiple,serie=script.inputs[0]
        op=scriptCall.operands[0]
        infile=dict_invalues[op]
        if not all(map(os.path.exists,infile.split(" "))) :
            raise Climaf_Driver_Error("Internal error : some input file does not exist among %s:"%(infile))
        subdict[ label ]=infile
        #if scriptCall.flags.canSelectVar :
        subdict["var"]=varOf(op)
        if isinstance(op,classes.cdataset) and op.alias:
            filevar,scale,offset,units,filenameVar,missing=op.alias
            if scriptCall.flags.canAlias and "," not in varOf(op) :
                #if script=="select" and ((varOf(op) != filevar) or scale != 1.0 or offset != 0.) :
                subdict["alias"]="%s,%s,%.4g,%.4g"%(varOf(op),filevar,scale,offset)
                subdict["var"]=filevar
            if units : subdict["units"]=units 
            if scriptCall.flags.canMissing and missing :
                subdict["missing"]=missing
        if isinstance(op,classes.cens) :
            if not multiple :
                raise Climaf_Driver_Error(
                    "Script %s 's input #%s cannot accept ensemble %s"\
                        %(scriptCall.script,0,`op`))
            #subdict["labels"]=r'"'+reduce(lambda x,y : "'"+x+"' '"+y+"'", op.labels)+r'"'
            subdict["labels"]=reduce(lambda x,y : x+"$"+y, op.labels)
        per=timePeriod(op)
        if not per.fx and str(per) != "" and scriptCall.flags.canSelectTime:
            subdict["period"]=str(per)
            subdict["period_iso"]=per.iso()
        if scriptCall.flags.canSelectDomain :
            subdict["domain"]=domainOf(op)
    i=0
    for op in scriptCall.operands :
        opscrs += op.crs+" - "
        infile=dict_invalues[op]
        if not all(map(os.path.exists,infile.split(" "))) :
            raise Climaf_Driver_Error("Internal error : some input file does not exist among %s:"%(infile))
        i+=1
        if ( i> 1 or 1 in script.inputs) :
            label,multiple,serie=script.inputs[i]
            subdict[ label ]=infile
            # Provide the name of the variable in input file if script allows for
            subdict["var_%d"%i]=varOf(op)
            if isinstance(op,classes.cdataset) and op.alias :
                filevar,scale,offset,units,filenameVar,missing =op.alias
                if ((varOf(op) != filevar) or (scale != 1.0) or (offset != 0.)) and \
                       "," not in varOf(op):
                    subdict["alias_%d"%i]="%s %s %f %f"%(varOf(op),filevar,scale,offset)
                    subdict["var_%d"%i]=filevar
		if units : subdict["units_%d"%i]=units 
		if missing : subdict["missing_%d"%i]=missing
            # Provide period selection if script allows for
            per=timePeriod(op)
            if not per.fx and per != "":
                subdict["period_%d"%i]=str(per)
                subdict["period_iso_%d"%i]=per.iso()
            subdict["domain_%d"%i]=domainOf(op)
    clogger.debug("subdict for operands is "+`subdict`)
    # substitution is deffered after scriptcall parameters evaluation, which may
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
    subdict["crs"]=opscrs.replace("'","")
    #
    # Combine CRS and possibly member_label to provide/complement title 
    if 'title' not in subdict :
        if 'member_label' in subdict :
            subdict["title"]=subdict['member_label']
        else:
            subdict["title"]=subdict["crs"]
    else: 
        if 'member_label' in subdict :
            subdict["title"]=subdict["title"]+" "+subdict['member_label']
            subdict.pop('member_label')
    #
    # Substitute all args
    template=template.safe_substitute(subdict)
    #
    # Allowing for some formal parameters to be missing in the actual call:
    #
    # Discard remaining substrings looking like :
    #  some_word='"${some_keyword}"'     , or:
    #  '"${some_keyword}"'
    template=re.sub(r'(\w*=)?(\'\")?\$\{\w*\}(\"\')?',r"",template)
    #
    # Discard remaining substrings looking like :
    #  some_word=${some_keyword}          , or
    #  ${some_keyword}
    template=re.sub(r"(\w*=)?\$\{\w*\}",r"",template)
    #
    # Link the fixed fields needed by the script/operator
    if script.fixedfields is not None :
        subdict_ff=dict()
        subdict_ff["model"]=modelOf(scriptCall.operands[0])
        subdict_ff["simulation"]=simulationOf(scriptCall.operands[0])
        subdict_ff["project"]=projectOf(scriptCall.operands[0])
        l=script.fixedfields #return paths: (linkname, targetname)
        files_exist=dict()
        for ll,lt in l:
            #Replace input data placeholders with filenames for fixed fields
            template_ff_target=Template(lt).substitute(subdict_ff)
            # symlink
            files_exist[ll]=False
            if os.path.isfile(ll):      
                files_exist[ll]=True
            else:
                os.system("ln -s "+template_ff_target+" "+ll)   
            
    # Launch script using command, and check termination 
    #command="PATH=$PATH:"+operators.scriptsPath+template+fileVariables
    #command="echo '\n\nstdout and stderr of script call :\n\t "+template+\
    #         "\n\n'> scripts.out  ; "+ template+ " >> scripts.out 2>&1"

    tim1=time.time()
    clogger.info("Launching command:"+template)
    #
    command=subprocess.Popen(template, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    repcom=command.wait()
    #
    logfile=open('last.out', 'w')
    logfile.write("\n\nstdout and stderr of script call :\n\t "+template+"\n\n")
    command_std=""
    for line in command.stdout:
        command_std+=line
        logfile.write(line)
    logfile.close()
    
    # Clean fixed fields symbolic links
    if script.fixedfields is not None :
        l=script.fixedfields  #return paths: (linkname, targetname)
        for ll,lt in l:
            if files_exist[ll] == False:
                os.system("rm -f "+ll)  

    if ( repcom == 0 ):
        if script.outputFormat is not None :
            # Tagging output files with their CliMAF Reference Syntax definition
            # Un-named main output
            ok = cache.register(main_output_filename,scriptCall.crs)
            # Named outputs
            for output in scriptCall.outputs:
                ok = ok and cache.register(subdict["out_"+output],\
                                           scriptCall.crs+"."+output)
                #if ok :
                #    set_variable(subdict["out_"+output], output, 'file')
            if ok : 
                duration=time.time() - tim1
                print("Done in %.1f s with script computation for %s "%\
                          (duration,`scriptCall`),file=sys.stderr)
                clogger.debug("Done in %.1f s with script computation for "
                              "%s (command was :%s )"%\
                                  (duration,`scriptCall`,template))
                return main_output_filename
            else :                
                raise Climaf_Driver_Error("Some output missing when executing "
                                          ": %s. \n See last.out"%template)
        else :
            clogger.debug("script %s has no output"%script.name)
            return None
    else:
        clogger.debug("Full script output:\n"+command_std)
        comm2=subprocess.Popen(["tail", "-n", "10", "last.out"], stdout=subprocess.PIPE)
        clogger.error("Last lines of script output:\n"+comm2.stdout.read())
        raise Climaf_Driver_Error("Script failure for : %s. More details either in file "
                                  "./last.out or by re-runing with clog(\"debug\")" %template)
        #raise Climaf_Driver_Error("See above (or scripts.out <=> clog('debug')) for analyzing "
        #                          "script call failure for : %s "%template)



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
    elif isinstance(cobject,classes.cens) :
        clogger.debug("for now, timePeriod logic for 'cens' objet is basic (1st member)- TBD")
        return timePeriod(cobject.members[0])
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
    elif isinstance(cobject,classes.cens) :
        clogger.debug("for now, domainOf logic for 'cens' objet is basic (1st member)- TBD")
        return domainOf(cobject.members[0])
    else : clogger.error("Unkown class for argument "+`cobject`)
                  

def varOf(cobject) : return attributeOf(cobject,"variable")
def modelOf(cobject) : return attributeOf(cobject,"model")
def simulationOf(cobject) : return attributeOf(cobject,"simulation")
def projectOf(cobject) : return attributeOf(cobject,"project")

def attributeOf(cobject,attrib) :
    """ Returns the attribute for a CliMAF object : if object is a dataset, returns
    its attribute property, otherwise returns attribute of first operand
    """
    if isinstance(cobject,classes.cdataset) : return getattr(cobject,attrib) 
    elif isinstance(cobject,classes.cens) : return attributeOf(cobject.members[0],attrib)
    elif getattr(cobject,attrib,None) : return getattr(cobject,attrib) 
    elif isinstance(cobject,classes.ctree) :
        clogger.debug("for now, varOf logic is basic (1st operand) - TBD")
        return attributeOf(cobject.operands[0],attrib)
    elif isinstance(cobject,cmacro.cdummy) :
        return "dummy"
    else : raise Climaf_Driver_Error("Unknown class for argument "+`cobject`)

                  
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
            crs=includer.buildcrs(period=incperiod)
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
        if varname is None: raise Climaf_Driver_Error("")
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
        raise Climaf_Driver_Error("arg is not a dataset")
    if not operators.is_derived_variable(ds.variable,ds.project) :
        raise Climaf_Driver_Error("%s is not a derived variable"%ds.variable)
    op,outname,inVarNames,params=operators.derived_variable(ds.variable,ds.project)
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
        if not oldvarname : 
            raise Climaf_Driver_Error("Cannot set variable name for a multi-variable dataset")
        if (oldvarname != varname) :
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
    
# Commodity functions
#########################

def cfile(object,target=None,ln=None,hard=None,deep=None) :
    """
    Provide the filename for a CliMAF object, or copy this file to target. Launch computation if needed. 

    Args:
    
      object (CliMAF object) : either a dataset or a 'compound' object (e.g. the result of a CliMAF operator)

      target (str, optional) : name of the destination file in case you really need another
       filename; CliMAF will then anyway also store the result in its cache,  either as a copy
       (default), or a sym- or a hard-link (see below); 

      ln (logical, optional) : if True, CliMAF cache file is created as a symlink to the target;
       this allows to cross filesystem boundaries, while still saving disk space (wrt to a copy);
       CliMAF will manage the broken link cases (at the expense of a new computation)

      hard (logical, optional) : if True, CliMAF cache file is created as a hard link to the target;
       this allows to save disk space, but does not allow to cross filesystem boundaries

      deep (logical, optional) : governs the use of cached values when computing the object:
      
        - if missing, or None : use cache as much as possible (speed up the computation)

        - False : make a shallow computation, i.e. do not use cached values for the 
          top level operation

        - True  : make a deep computation, i.e. do not use any cached value

    Returns:

       - if target is provided, returns this filename (or linkname) if computation is 
         successful ('target' contains the result), and None otherwise;
       
       - if target is not provided, returns the filename in CliMAF cache, which contains
         the result (and None if failure)
       

    """
    clogger.debug("cfile called on "+str(object))  
    result=climaf.driver.ceval(object,format='file',deep=deep)
    if target is None : return result
    else :
        target=os.path.abspath(os.path.expanduser(target))
        if (isinstance(object,climaf.classes.cens)) :
            raise Climaf_Driver_Error("Cannot yet copy or link result files for an ensemble")
        if result is not None :
            if ln or hard :
                if ln and hard : Climaf_Driver_Error("flags ln and hard are mutually exclusive")
                elif ln :
                    if not os.path.samefile(result,target):
                        shutil.move(result,target)
                        if os.path.exists(result) : os.remove(result)
                        os.symlink(target,result)
                else:
                    # Must create hard link
                    # If result is a link, follow links for finding source of hard link
                    source=os.readlink(result)
                    if (source == target):
                        # This is a case where the file had already been symlinked to the same target name
                        shutil.move(source,result)
                        os.link(result,target)
                    else :
                        if os.path.exists(target) : os.remove(target)
                        os.link(source,target)
            else :
                shutil.copyfile(result,target)
        return target

def cshow(obj) :
    """ 
    Provide the in-memory value of a CliMAF object. 
    For a figure object, this will lead to display it
    ( launch computation if needed. )
    """
    clogger.debug("cshow called on "+str(obj)) 
    return climaf.driver.ceval(obj,format='MaskedArray')

def  cMA(obj,deep=None) :
    """
    Provide the Masked Array value for a CliMAF object. Launch computation if needed.

    Args:
      obj (CliMAF object) : either a datset or a 'compound' object (like the result of a CliMAF standard operator)
      deep (logical, optional) : governs the use of cached values when computing the object

        - if missing, or None : use cache as much as possible
        - False : make a shallow computation, i.e. do not use cached values for top level operation
        - True  : make a deep computation, i.e. do not use any cached value

    Returns:
      a Masked Array containing the object's value

    """
    clogger.debug("cMA called with arguments"+str(obj)) 
    return climaf.driver.ceval(obj,format='MaskedArray',deep=deep)

def cexport(*args,**kwargs) :
    """ Alias for climaf.driver.ceval. Create synonyms for arg 'format'

    """
    clogger.debug("cexport called with arguments"+str(args))  
    if "format" in kwargs :
        if (kwargs['format']=="NetCDF" or kwargs['format']=="netcdf" or kwargs['format']=="nc") :
            kwargs['format']="file" 
        if (kwargs['format']=="MA") :
            kwargs['format']="MaskedArray" 
    return climaf.driver.ceval(*args,**kwargs)

def cimport(cobject,crs) :
    clogger.debug("cimport called with argument",cobject)  
    clogger.debug("should check syntax of arg 'crs' -TBD")
    clogger.warning("cimport is not for the dummies - Playing at your own risks !")
    import numpy, numpy.ma
    if isinstance(cobject,numpy.ma.MaskedArray) :
        clogger.debug("for now, use a file for importing - should revisit - TBD")
        clogger.error("not yet implemented fro Masked Arrays - TBD")
    elif isinstance(cobject,str) :
        cache.register(cobject,crs)
    else :
        clogger.error("argument is not a Masked Array nor a filename",cobject)
    

def cfilePage(cobj, deep, recurse_list=None) :
    """
    Builds a page with CliMAF figures, computing associated crs

    Args:
     cobj (cpage object)
     
    Returns : the filename in CliMAF cache, which contains the result (and None if failure)

    """
    if not isinstance(cobj,classes.cpage):
        raise Climaf_Driver_Error("cobj is not a cpage object")
    clogger.debug("Computing figure array for cpage %s"%(cobj.crs))
    #
    # page size and creation
    if cobj.orientation == "portrait":
        page_width=800. ; page_height=1200.
    elif cobj.orientation == "landscape":
        page_width=1200. ; page_height=800.
    page_size="%dx%d"%(page_width, page_height)
    args=["convert", "-size", page_size, "xc:white"]
    #
    # margins
    x_left_margin=10. # Left shift at start and end of line
    y_top_margin=10. # Initial vertical shift for first line
    x_right_margin=10. # Right shift at start and end of line
    y_bot_margin=10. # Vertical shift for last line
    xmargin=20. # Horizontal shift between figures
    ymargin=20. # Vertical shift between figures
    #
    usable_height=page_height-ymargin*(len(cobj.heights)-1.)-y_top_margin -y_bot_margin
    usable_width =page_width -xmargin*(len(cobj.widths)-1.) -x_left_margin-x_right_margin
    #
    # page composition
    y=y_top_margin
    for line, rheight in zip(cobj.fig_lines, cobj.heights) :
        # Line height in pixels
        height=usable_height*rheight 
        x=x_left_margin
        for fig, rwidth in zip(line, cobj.widths) :
            # Figure width in pixels
            width=usable_width*rwidth 
            scaling="%dx%d+%d+%d" %(width,height,x,y)
            if fig : 
                figfile=ceval(fig,format="file", deep=deep, recurse_list=recurse_list)
            else : figfile='xc:None'
            clogger.debug("Compositing figure %s",fig.crs if fig else 'None')
            args.extend([figfile , "-geometry", scaling, "-composite" ])
            x+=width+xmargin
        y+=height+ymargin
    out_fig=cache.generateUniqueFileName(cobj.buildcrs(), format="png")
    args.append(out_fig)
    clogger.debug("Compositing figures : %s"%`args`)
    comm=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if comm.wait()!=0 :
        raise Climaf_Driver_Error("Compositing failed : %s" %comm.stderr.read())
    if cache.register(out_fig,cobj.crs) :
        clogger.debug("Registering file %s for cpage %s"%(out_fig,cobj.crs))
        return out_fig

def calias(project,variable,**kwargs):
              
    if not "," in variable: # mono-variable
        classes.calias(project=project,variable=variable,**kwargs) 
        
    else : #multi-variable
        classes.calias(project=project,variable=variable,**kwargs) 
        list_variable=variable.split(",")
        
        for v in list_variable:
            operators.derive(project,v,'ccdo',variable,operator='selname,%s'%v)
            classes.calias(project=project,variable=v,**kwargs) 


def CFlongname(varname) :
    """ Returns long_name of variable VARNAME after CF convention 
    """
    return("TBD_should_improve_function_climaf.driver.CFlongname") 

class Climaf_Driver_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        cdedent(100)
    def __str__(self):
        return `self.valeur`

