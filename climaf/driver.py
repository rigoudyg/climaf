""" CliMAF driver

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

#Multi pour : ds.adressOF, cache.remoteRead, cstore, cache.cdrop, cache.hasIncludingTree, ceval_select, ceval_operator...

import os, re, logging, posixpath, subprocess, time
from string import Template

# Climaf modules
import climaf
import classes
import cache
import operators

# Declares an external operator used temporarily (until internal objects and operators are handled)
#operators.cscript('select' ,climaf.__path__[0]+'/scripts/mcdo.sh "" ${out} ${var} ${period} ${multins} ' )
operators.cscript('select' ,climaf.__path__[0]+'/../scripts/mcdo.sh "" ${out} ${var} ${period} ${ins} ' )

def capply (operator, *operands, **parameters):
    """ Builds the object representing applying a CliMAF operator (script or function)
    
    Returns results as a list of CliMAF objects and stores them if auto-store is on
    """
    res=None
    opds=map(str,operands)
    if operator in operators.scripts :
        logging.debug("driver.capply : applying script %s to"%operator + `opds` + `parameters`)
        res=capply_script(operator, *operands, **parameters)
    elif operator in operators.operators :
        logging.debug("driver.capply : applying operator %s to"%operator + `opds` + `parameters`)
        res=capply_operator(operator,*operands, **parameters)
    else:
        logging.error("climaf.driver.capply : %s is not a known operator nor script"%operator)
    return res

def capply_script (script_name, *operands, **parameters):
    """ Create object for application of a script to OPERANDS with keyword PARAMETERS."""

    if script_name not in operators.scripts :
        logging.error("Script %s is not know. Consider declaring it with function 'cscript'",
                      script_name)
        return None
    script=operators.scripts[script_name]
    if len(operands) != script.inputs_number() : 
        logging.error("driver.capply_script : script %s is declared with %d inputs, "+
                      "while you provided %d"%\
                      (script_name,script.inputs_number(),len(operands)))
        return None
    rep=classes.ctree(script_name, script, *operands, **parameters)
    if rep is not None :
        #
        # TBD Analyze script inputs cardinality vs actual arguments
        #for op in operands :
        #
        # Create one child for each output
        defaultVariable=operands[0].variable
        for outname in script.outputs :
            if outname is None :
                rep.variable=script.outputs[None]%defaultVariable
            else :
                son=classes.scriptChild(rep,outname)
                son.variable=script.outputs[outname]%defaultVariable
                rep.outputs[outname]=son
                setattr(rep,outname,son)
                #
                # Check that all parameters to the call are expected by the script 
                for para in parameters :
                    if re.match(r".*\{"+para+r"\}",script.command) is None :
                        logging.error("driver.capply_script : parameter %s is not expected by  script %s (which command is : %s)"%(para,script_name,script.command))
                        return None
    #
    return rep

def capply_operator (operator, *operands, **parameters):
    """ Create object for application of an internal OPERATOR to OPERANDS with keywords PARAMETERS.

    """
    logging.error("capply_operator : Not yet developped - TBD")
    return None
    

def ceval(cobject,userflags=operators.scriptFlags(False,False,False,False,False),format="MaskedArray",deep=None, derived_list=[]) :
    """ Actually evaluates a CliMAF object, either as an in-memory data structure or
    as a string of filenames (which either represent a superset or exactly includes
    the desired data)

    with arg deep=True , re-evaluates all components
    with arg deep=False, re-evaluates top level operation
    without arg deep   , use cached values as far as possible

    arg derived_list is the list of variables that have been considered as 'derived'
    (i.e. not natives) in upstream evaluations. It avoids to loop endlessly
    """
    if format != 'MaskedArray' and format != 'file' and format != 'png' :
        logging.error('Allowed formats yet are : "object", "file" and "png"')
        return None
    #
    if isinstance(cobject,classes.cdataset):
        logging.debug("ceval : Evaluating dataset " + cobject.crs)
        ds=cobject
        if ds.isLocal() or ds.isCached() :
            logging.debug("ceval : Dataset %s is local or cached "%ds )
            #  if the data is local, then
            #   if the user can select the data and aggregate time, and requested format is
            #     'file' return the filenames
            #   else : read the data, create a cache file for that, and recurse
            # Go to derived variable evaluation if appicable
            if ds.variable in operators.derived_variables and not ds.hasRawVariable() :
                if ds.variable in derived_list :
                    logging.error("driver.ceval : Loop detected while evaluating derived variable "+
                                  ds.variable + " " + `derived_list`)
                    return None
                derived=derive_variable(ds)
                logging.debug("ceval : evaluating derived variable %s as %s"%\
                                  (ds.variable,`derived`))
                derived_value=ceval(derived, format=format, deep=deep, 
                                    userflags=userflags,
                                    derived_list=derived_list.append(ds.variable))
                if derived_value : 
                    logging.debug("ceval : succeeded in evaluating derived variable %s as %s"%\
                                      (ds.variable,`derived`))
                    set_variable(derived_value, ds.variable, format=format)
                return(derived_value)
            if ((userflags.canSelectVar or ds.oneVarPerFile()) and \
                (userflags.canSelectTime or ds.periodIsFine()) and \
                (userflags.canAggregateTime or ds.periodHasOneFile()) and 
                #(userflags.doSqueezeMembers or ds.hasOneMember()) and 
                #(userflags.canOffsetScale or ds.hasExactVariable()) and 
                (format == 'file')) :
                logging.debug("ceval : Delivering file set or sets is OK for the target use")
                return(ds.selectFiles()) # a single string with all filenames,
                               #or a list of such strings in case of ensembles
            logging.debug("ceval : Must subset and/or aggregate and/or select "+
                          "var from data files and/or get data, or provide object result")
            ## extract=cread(ds)
            ## logging.debug("ceval : Done with subsetting and caching data files")
            ## cstore(extract) # extract should include the dataset def
            ## return ceval(extract,userflags,format)
            logging.debug("Fetching/selection/aggregation is done using an "+
                          "external script for now - TBD")
            #ds.setOffsetScale()
            extract=capply('select',ds)
            if extract is None :
                logging.error("ceval : cannot access dataset" + `ds`)
                return None
            return ceval(extract,userflags=userflags,format=format,deep=deep)
        else :
            # else (non-local and non-cached dataset)
            #   if the user can access the dataset by one of the dataset-specific protocols
            #   then assume it can also select on time and provide it with the address
            #   else : fetch the relevant selection of the data, and store it in cache
            logging.debug("ceval : Dataset is remote " )
            if (userflags.canOpenDap and format == 'file' ) :
                logging.debug("ceval : But user can OpenDAP " )
                return(ds.adressOf())
            else :
                logging.debug("ceval : Must remote read and cache " )
                # Assume remoteRead fetches the strict minimum 
                extract=cache.remoteRead(ds)
                if (format == 'file' ) :
                    cachefile=cstore(extract)
                    logging.debug("ceval : And provide cache file reference " )
                    return cachefile
                else :
                    logging.debug("ceval : And provide in-memory object " )
                    return(extract)
    #
    elif isinstance(cobject,classes.ctree) or isinstance(cobject,classes.scriptChild) : 
        logging.debug("ceval : Evaluating compound object : " + cobject.crs)
        if (deep is not None) : cache.cdrop(cobject.crs)
        filename=cache.hasExactObject(cobject) 
        if filename : 
            logging.info("driver.ceval : Object found in cache : %s"%cobject.crs)
            if format=='file' : return filename
            else: return cread(filename)
        it,altperiod=cache.hasIncludingObject(cobject)
        if it : 
            logging.info("driver.ceval : Including object found in cache : %s"%it.crs)
            # Just select (if necessary for the user) the portion relevant to the request
            return(ceval_select(it,cobject,userflags,format,deep))
        #
        it,comp_period=cache.hasBeginObject(cobject) 
        if it : 
            logging.info("driver.ceval : partial result found in cache for %s : %s"%\
                                  (cobject.crs,it.crs))
            begcrs=it.crs
            # Turn object for begin in complement object for end, and eval it
            it.setperiod(comp_period)
            ceval(it,userflags,format,deep)
            if (format == 'file') :
                return cache.complement(begcrs,it.crs,cobject.crs)
            else :
                logging.debug("driver.ceval : cannot yet complement except for files")
                return(None)
        #
        logging.info("driver.ceval : nothing relevant found in cache for %s"%cobject.crs)
        if deep==False : deep=None
        if isinstance(cobject,classes.ctree)  :
            # the cache doesn't have a similar tree, let us recursively eval subtrees
            # TBD  : analyze if the dataset is remote and the remote place 'offers' the operator
            if cobject.operator in operators.scripts :
                file=ceval_script(cobject,deep) # Does return a filename, or list of filenames
                if ( format == 'file' ) : return (file)
                else : return cread(file)
            elif cobject.operator in operators.operators :
                obj=ceval_operator(cobject,deep)
                if (format == 'file' ) : return(cstore(obj))
                else : return(obj)
            else : 
                logging.error("driver - ceval : operator %s is not a script nor known operator",str(cobject.operator))
                return(None)
        else :
            # isinstance(cobject,classes.scriptChild) should be True
            # Force evaluation of 'father' script
            if ceval_script(cobject.father,deep)  is not None :
                # Re-evaluate, which should succeed using cache
                return ceval(cobject,userflags,format,deep)
            else :
                logging.error("driver.ceval : generating script aborted for "+cobject.father.crs)
                return None
    elif isinstance(cobject,str) :
        logging.debug("ceval : Evaluating object from crs : %s"%cobject)
        logging.error("Evaluation from CRS is not yet implemented ( %s )"%cobject)
        return None
    else :
        logging.error("driver - ceval : argument " +`cobject`+" is not (yet) managed")
        return(None)
    # if cache.DynamicIsOn : 
    #    if hasDynamicInputs(cobject) :
    #        if hasOutdatedInputs(cobject) :
    #          return ' Already Done'
    #  else : return ' Not Dynamic'
    # else : return 'Dynamic Off'



def ceval_script (scriptCall,deep):
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
        inValue=ceval(op,userflags=script.flags,format='file',deep=deep)
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
    #       logging.error("ceval : Cannot mix ensemble sizes : size of ensemble # %d is not 1 nor equals to max ensemble size (%d) in %s"%\
    #                         (rank,max(sizes),scriptCall.crs))
    #       return(None)
    # if ( nbSizeMax != 1 ) :
    #     if ( nbSizeMax != len(sizes)) :
    #       logging.error("ceval : Cannot mix ensemble sizes : more than one operands has a size > 1, while some have size 1 in %s"%scriptCall.crs)
    #       return(None)

    # Replace input data placeholders with filenames
    subdict=dict()
    opscrs=""
    if 0 in script.inputs :
        label,multiple,serie=script.inputs[0]
        op=scriptCall.operands[0]
        infile=dict_invalues[op]
        subdict[ label ]='"'+infile+'"'
        subdict["var"]='"'+op.variable+'"'
        subdict["period"]=str(timePeriod(op))
    i=0
    for op in scriptCall.operands :
        opscrs += op.crs+" - "
        infile=dict_invalues[op]
        i+=1
        if ( i> 1 or 1 in script.inputs) :
            label,multiple,serie=script.inputs[i]
            subdict[ label ]='"'+infile+'"'
            # Provide the name of the variable in input file if script allows for
            subdict["var_%d"%i]=op.variable
            # Provide period selection if script allows for
            subdict["period_%d"%i]=timePeriod(op)
    logging.debug("driver.ceval_script - subdict for operands is "+`subdict`)
    # substituion is deffered after scriptcall parameters evaluation, which may
    # redefine e.g period
    #
    # Provide one cache filename for each output and instantiates the command accordingly
    if script.outputFormat is not None :
        # Compute a filename for each ouptut
        # Un-named main ouput
        main_output_filename=cache.generateUniqueFileName(scriptCall.crs,
                                                          format=script.outputFormat)
        subdict["out"]=main_output_filename
        subdict["out_"+scriptCall.variable]=main_output_filename
        # Named outputs
        for output in scriptCall.outputs:
            subdict["out_"+output]=cache.generateUniqueFileName(scriptCall.crs+"."+output,\
                                                         format=script.outputFormat)
    # Account for script call parameters
    for p in scriptCall.parameters : subdict[p]=scriptCall.parameters[p]
    if 'crs' not in scriptCall.parameters : subdict["crs"]=opscrs
    # Substitute all args, with special case of NCL convention for passing args
    if (script.command.split(' ')[0][-3:]=="ncl") :
        for o in subdict :
            if isinstance(subdict[o],str) and subdict[o][0] != "\"" :
                subdict[o]="\"" + subdict[o] + "\""
    template=template.safe_substitute(subdict)
    #
    # Allow script call no to use all formal arguments
    template=re.sub(r"(\w*=)?\$\{\w*\}",r"",template)
    #
    if (script.command.split(' ')[0][-3:]=="ncl") :
        template=re.sub(r'([^=\s]*=([^=\s\"]+|\"[^\"]*\"))',r"'\1'",template)
    # Launch script using command, and check termination 
    #command="PATH=$PATH:"+operators.scriptsPath+template+fileVariables
    command="echo '\n\nstdout and stderr of script call :\n\t "+template+\
             "\n\n'> scripts.out  ; "+ template+\
             " >> scripts.out 2>&1"
    tim1=time.time()
    logging.info("driver.ceval_script : Launching command:"+template)
    # Timing
    # TBD : Should use process.check_output and display stderr when exit is non-0
    if ( subprocess.call(command, shell=True) == 0):
        if script.outputFormat is not None :
            # Tagging output files with their CliMAF Reference Syntax definition
            # Un-named main ouput
            ok = cache.register(main_output_filename,scriptCall.crs)
            # Named outputs
            for output in scriptCall.outputs:
                ok = ok and cache.register(subdict["out_"+output],scriptCall.crs+"."+output)
            if ok : 
                duration=time.time() - tim1
                logging.info(("driver.ceval_script : Done in %.1g s with command:"+template) % 
                             duration)
                return main_output_filename
            else :
                logging.error("driver.ceval_script : Some output missing when executing : %s. \nSee scripts.out"%template)
        else :
            logging.debug("driver.ceval_script : script %s has no ouput"%script.name)
    else:
        logging.error("driver.ceval_script: Script call failure for %s . \nSee scripts.out"%template)
    return None


def timePeriod(cobject) :
    """ Returns a time period for a CliMAF object : if object is a dataset, returns
    its time period, otherwise returns time period of first operand
    """
    if isinstance(cobject,classes.cdataset) : return cobject.period
    elif isinstance(cobject,classes.ctree) :
        logging.debug("driver.timePeriod : for now, timePeriod logic for scripts output is basic (1st operand) - TBD")
        return timePeriod(cobject.operands[0])
    elif isinstance(cobject,classes.scriptChild) :
        logging.debug("driver.timePeriod : for now, timePeriod logic for scriptChilds is basic - TBD")
        return timePeriod(cobject.father)
    else : logging.error("driver.timePeriod : unkown class for argument "+`cobject`)
                  
def varOf(cobject) :
    """ Returns the variable for a CliMAF object : if object is a dataset, returns
    its 'variable' property, otherwise returns variable of first operand
    """
    if isinstance(cobject,classes.cdataset) : return cobject.variable
    elif isinstance(cobject,classes.ctree) :
        logging.debug("driver.varOf : for now, varOf logic is basic (1st operand) - TBD")
        return varOf(cobject.operands[0])
    else : logging.error("driver.varOf : unkown class for argument "+`cobject`)

def varOfFile(filename) :
    """ returns the name of the unique non-dimension variable in
    NetCDF file FILENAME, or None if it is not unique
    """
    varname=None
    from Scientific.IO.NetCDF import NetCDFFile as ncf
    fileobj=ncf(filename)
    #import NetCDF4
    #fileobj=netCDF4.Dataset(filename)
    for filevar in fileobj.variables :
        if filevar not in fileobj.dimensions :
            if varname is None : 
                varname=filevar
            else :
                logging.debug("driver.varOf : Got at least two variables (%s and %s) "+\
                                  "and no direction to choose  - File is %s"%\
                                  (varname,filevar,datafile))
                return(None)
    fileobj.close()
    return(varname)

                  
def ceval_select(includer,included,userflags,format,deep) :
    """ Extract object INCLUDED from (existing) object INCLUDER,
    taking into account the capability of the user process (USERFLAGS)
    and the required delivering FORMAT(file or object)
    """
    if format=='file' : 
        if userflags.canSelectTime :
            logging.debug("driver.ceval_select : TBD - should do smthg smart when user can select time")
            #includer.setperiod(included.period)
        incperiod=timePeriod(included)
        extract=capply('select',includer, period=incperiod)
        objfile=ceval(extract,format='file',deep=deep)
        crs=includer.buildcrs(`incperiod`)
        return(cache.rename(objfile,crs))
    else :
        logging.error("driver.ceval_select : can yet process only files - TBD")


def cread(datafile,varname=None):
    import re,logging
    if not datafile : return(None)
    if re.findall(".png$",datafile) :
        subprocess.Popen(["display",datafile,"&"])
    elif re.findall(".nc$",datafile) :
        logging.debug("cread : reading NetCDF file %s"%datafile)
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
        logging.error("driver.cread : cannot yet handle %s"%datafile)
        return None

def cview(datafile):
    if re.findall(".png$",datafile) :
        subprocess.Popen(["display",datafile,"&"])
    else :
        logging.error("driver.cread : cannot yet handle %s"%datafile)
        return None

def derive_variable(ds):
    """ Assuming that variable of DS is a derived variable, returns the CliMAF object
    representing the operation needed to compute it (using information in dict 
    operators.derived_variable
    """
    if not isinstance(ds,classes.cdataset):
        logging.error("derive_variable : arg ds is not a dataset")
        return(None)
    if ds.variable not in operators.derived_variables :
        logging.error("derive_variable : %s is not a derived variable")
        return(None)
    op,outname,inVarNames,params=operators.derived_variables[ds.variable]
    inVars=[]
    for varname in inVarNames :
        inVars.append(classes.cdataset(project=ds.project, model=ds.model,
                experiment=ds.experiment, rip=ds.rip,period=ds.period, 
                frequency=ds.frequency, domain=ds.domain, variable=varname)) 
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
            logging.error("driver.set_variable : Issue with changing varname to %s in %s"%(varname,obj))
            return None
        logging.debug("driver.set_variable : Varname changed to %s in %s"%(varname,obj))
        command="ncatted -a long_name,%s,o,c,%s %s"%(varname,long_name,obj)
        if ( os.system(command) != 0 ) :
            logging.error("driver.set_variable : Issue with changing long_name for var %s in %s"%
                          (varname,obj))
            return None
        return True
    elif (format=='MaskedArray') :
        logging.warning('driver.set_variable : TBD - Cannot yet set the varname for MaskedArray')
    else :
        logging.error('driver.set_variable : Cannot handle format %s'%format)
    

def CFlongname(varname) :
    """ Returns long_name of variable VARNAME after CF convention 
    """
    return("TBD_should_improve_function_climaf.driver.CFlongname") 
