""" CliMAF handling of external scripts and binaries , and of internal operators (Python funcs)

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

import logging, os, re, sys, subprocess
import driver

# Next definition can be splitted in a set managed by an administrator, and
# other sets managed and fed by users. But it should be enforced that no redefinition
# occurs for some really basic operators (should it ?)
internals=[]
scripts=dict()
operators=dict()
derived_variables=dict()

class scriptFlags():
    def __init__(self,canOpendap, canSelectVar, canSelectTime, canAggregateTime, doSqueezeTime):
        self.canOpendap=canOpendap
        self.canSelectVar=canSelectVar
        self.canSelectTime=canSelectTime
        self.canAggregateTime=canAggregateTime
        self.doSqueezeTime=doSqueezeTime

class cscript():
    def __init__(self,name, command, canOpendap=False, format="nc", doSqueezTime=False, **params):

        """
        Declares a CliMAF script.

        A CliMAF script is composed of a name and a calling sequence with templates for args, as in :
        
        \"my_script single_input=${in} -x ${any_param_name} -main_output=${out} ${out_other} ${out_third}\"
        \"my_script ${in_1} -x ${any_param_name} -otherinput ${in_2} ${out} ${out_other} ${out_third}\"
        
        where :

        - ${in_<i>} are placeholders for input file where <i> agree with
        input streams operands arguments ordering.  You may use ${in}
        for first operand. Use 'ins' instead of 'in' if the script can
        handle multiple files for a given input stream (it will then
        get a string of filenames, with whitespace separator)

        - ${var} is a placeholder for telling the script which file
        variable to process; use it only if the script can select
        a variable in multi-variable files;
        * the script should accept an empty string for variable name,
        because, for efficiency purposes, CliMAF will always indicate 
        that way if the input file is already filtered for the variable
        * if there are mutiple inputs, correspondig variable names will
        automatically be provided as '--climaf_var_$i var_$i'

        - ${out_xxx} are placeholders for outputs of the script, xxx
        being their output labels. The first placeholder may lack any
        _xxx if the output label is the name of the first input's
        variable. If the script does not produce any ouput to manage,
        use 'format=None'. By default, the variable name for an output
        labeled 'abc' is 'abc'. But you may declare how to compute the
        variable name for each output, from first input variable name,
        by providing a format string, using arguments ending by '_var'
        as in : output1_var='std_dev(%s)' for the output labelled
        output1 (i.e. declared as ${out_output1})
        
        - ${period} is a placeholder for telling the script which time
        period to process; use it only if the script is able to do time
        slicing; if not used, CliMAF will perform time-slicing
        upstream; if used, CliMAF will provide the period as a string
        YYYYMMDD-YYYYMMDD (to be undestrstood as [YYYYMMDD-YYYYMMDD[ )
        
        - other placeholders stand for scalar or string arguments and
        agree with argument names used when invoking the script from
        CliMAF
        
        - pattern ${crs} will by default be replaced by a string representing the
        object in CliMAF Reference Syntax
        
        - all outputs must be of the same format, declared by arg
        'format'; handled values : nc, png and None

        """
        # Check that script name do not clash with an existing symbol 
        if name in dir() and name not in scripts :
            logging.error("operators/cscript : trying to redefine %s, which exists outside CliMAF"%name)
            return None
        if name in scripts : logging.warning("Redefining CliMAF script %s"%name)
        #
        # Check now that script is executable
        scriptcommand=command.split(' ')[0]
        try :
            executable=subprocess.check_output('which '+scriptcommand, \
                                                   shell=True)
        except :  
            logging.error("operators.cscript : defining %s : command %s is not executable"%\
                              (name,scriptcommand))
                # raise ClimafException
            return None
        executable=executable.replace('\n','')
        #
        # Analyze inputs field keywords and populate dict attribute 'inputs' with some properties
        self.inputs=dict()
        it=re.finditer(r"\${(?P<keyw>(?P<mult>mm)?in(?P<serie>s)?(_(?P<n>([\d]+)))?)}",command)
        for oc in it : 
            if (oc.group("n") is not None) : rank=int(oc.group("n"))
            else : rank=0
            if rank in self.inputs :
                logging.error("When defining %s : duplicate declaration for input #%d"%(name,rank))
                return(None)
            multiple=(oc.group("mult") is not None)
            serie=(oc.group("serie") is not None)
            self.inputs[rank]=(oc.group("keyw"),multiple,serie)
        if len(self.inputs)==0 : 
            logging.error(("When defining %s : command %s must include at least one of "+
                          "${in} ${ins} ${min} or ${in_..} for specifying how CliMAF will provide the input filename(s)")%\
                              (name,command))
            return None
        #print self.inputs
        for i in range(len(self.inputs)) :
            if i+1 not in self.inputs and not ( i == 0 and 0  in self.inputs) :
                logging.error("When defining %s : error in input sequence for rank %d"%(name,i+1))
                return(None)
        #
        # Check that command includes an argument allowing for providing at least one output filename
        if command.find("${out") < 0 :
            if format is not None :
                logging.error("(operators.cscript : defining %s : command %d must include "+
                              "'${out_xxx}' for specifying how CliMAF will provide the output(s) filename(s))"%\
                                  (name,command))
                return None
            else: 
                logging.warning("operators.cscript : defining script %s as output-less"%name)
        #
        # Search in call arguments for keywords matching "<output_name>_var" which may provide
        # format string for 'computing' outputs variable name from input variable name
        outvarnames=dict() ; pattern=r"^(.*)_var$"
        for p in params : 
            if re.match(pattern,p):
                outvarnames[re.findall(pattern,p)[0]]=params[p]
        logging.debug("operators.script : outvarnames = "+`outvarnames`)
        #
        # Analyze outputs names , associated variable names (or format strings), and store 
        # it in attribute dict 'outputs' 
        self.outputs=dict()
        it=re.finditer(r"\${out(_(?P<outname>[\w-]*))?}",command)
        for occ in it :
            outname=occ.group("outname") 
            if outname is not None :
                if (outname in outvarnames) : 
                    self.outputs[outname]=outvarnames[outname]
                else :
                    self.outputs[outname]=outname
            else:
                self.outputs[None]="%s"
        logging.debug("operators.script : outputs = "+`self.outputs`)
        #
        canSelectVar=False
        if command.find("${var}") > 0 : canSelectVar=True
        canAggregateTime=False
        if command.find("${ins}") > 0     or command.find("${ins_1}") > 0    :
            canAggregateTime=True
        canSelectTime=False
        if command.find("${period}") > 0  or command.find("${period_1}") > 0 :
            canSelectTime=True
        self.name=name
        self.command=command
        #
        self.flags=scriptFlags(canOpendap, canSelectVar, canSelectTime, \
                                   canAggregateTime, doSqueezTime )
        self.outputFormat=format
        scripts[name]=self

        # Init doc string for the operator
        doc="CliMAF wrapper for command : %s"%self.command
        # try to get a better doc string from colocated doc/directory
        docfilename=os.path.dirname(__file__)+"/../doc/scripts/"+name+".rst"
        #print "docfilen= "+docfilename
        try:
            docfile=open(docfilename)
            doc=docfile.read()
            docfile.close()
        except:
            pass
        #
        # creates a function named as requested, which will invoke
        # capply with that name and same arguments
        exec 'def %s(*args,**dic) :\n  """%s""" \n  return climaf.driver.capply("%s",*args,**dic)\n '%\
            (name,doc,name) \
            in sys.modules['__main__'].__dict__
        logging.debug("CliMAF script %s has been declared"%name)

    def inputs_number(self):
        """ returns the number of distinct arguments of a script which are inputs 
        
        """
        l=re.findall(r"\$\{(mm)?ins?(_\d*)?\}",self.command)
        ls=[]; old=None
        for e in l :
            if e != old : ls.append(e)
            old=e
        return(len(ls))

class coperator():
    def __init__(self,op, command, canOpendap=False, canSelectVar=False, canSelectTime=False, canAggregateTime=False ):
        logging.error("operators.coperator : not yet developped")


def derive(derivedVar, scriptOp, *invars, **params) :
    """ Define that 'derivedVar' is a derived variable, computed by
    applying 'scriptOp' to input streams which are datasets whose 
    variable names tae the values in '*invars' and the parameter/arguments 
    of scriptOp tae the values in '**params'

    Example , assuming that script 'minus' has been defined as :
        cscript('minus','cdo sub ${in_1} ${in_2} ${out}')
    you may define cloud radiative effect at the surface ('rscre')
    using the difference of values of all-sky and clear-sky net
    radiation at the surface by 
       derived('rscre','minus','rs','rscs')

    argument 'derivedVar' may be a dictionnary, with keys=derived variable
    names and values=scripts outputs names; example :
       cscript('vertical_interp', 'vinterp.sh ${in} surface_pressure=${in_2} 
                                   ${out_l500} ${out_l850} method=${opt}')
       derived({z500 : 'l500' , z850 : 'l850'},'vertical_interp', 'zg', 'ps', opt='log'}
    
    """
    # Action : register the information in a dedicated dict which keys
    # are single derived variable names, and which will be used at the
    # object evaluation step
    # Also : some consistency checks w.r.t. script definition
    if scriptOp in scripts :
        if not isinstance(derivedVar,dict) : derivedVar=dict(out=derivedVar)
        for outname in derivedVar :
            if outname != 'out' and outname not in scriptOp.outvarnames :
                logging.error("operators.derive : %s is not a named  ouput for script %s"%(outname,scriptOp))
                return
            s=scripts[scriptOp]
            if s.inputs_number() != len(invars) :
                logging.error("operators.derive : number of input variables for operator %s is %d, which is inconsistent with script declaration : %s"%(s.name,len(invars),s.command))
                return
            # TBD : check parameters number  ( need to build its list in cscript.init() )
            derived_variables[derivedVar[outname]]=(scriptOp, outname, list(invars), params)
    elif scriptOp in operators :
        logging.warning("operators.derive : cannot yet handle derived variables based on internal operators")
    else : 
        logging.error("operators.derive : second argument must be a script or operator, already declared")



if __name__ == "__main__":
    def ceval(script_name,*args,**dic) :
        print script_name, " has been called with args=",args, " and dic=",dic
        print "Command would be:",
    cscript('test_script' ,'echo $*')
    test_script(arg1=1,arg2='two')

#scripts['eof']='eof "${in}" ${out_eof} ${out_cp}'
#scripts['regress']='regress ${in_1} ${in_2} ${out_regress} ${out_correl}'
#scripts['spatial_average']="cdo fldavg ${datain} ${dataout} ${box} ${dataout2}"
#scripts['eof']="eof ${datain} ${out1} ${dataout2}"

