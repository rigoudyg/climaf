#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Driver and utilities for launching an ESMValTool diagnostic. 

Originally developped with ESMValTool version 2.2.0
"""
from __future__ import print_function, division, unicode_literals, absolute_import

# We assume that the dataset period has complete years (because (some) EVT diags do assume it too)
# Created : S.Senesi - 2021
    
import sys
import os
import yaml
import subprocess
import time
import datetime
import logging
#
from env.environment import *
from env.clogging import clogger, dedent as cdedent
from env.site_settings import atIPSL
#
import climaf
from climaf.utils import Climaf_Error, Climaf_Driver_Error
from climaf.anynetcdf import ncf
from climaf.classes import timePeriod, cens, varOf, projectOf, experimentOf, realizationOf

#: Path for the wrapper script for setting ESMValTool's diag scripts environment and launching them
wrapper = None

def evt_script(climaf_name, script):
    """Create a function named CLIMAF_NAME for launching an ESMValTool's
    diagnostic script SCRIPT (which follows EMSValTool naming
    convention)

    The created function will actually invoke :py:func:`~climaf.driver.ceval_evt` with
    argument SCRIPT and own arguments.

    """
    
    doc = "CliMAF wrapper for EVT script : %s" % script
    defs = 'def %s(*args,**dic) :\n  """%s"""\n  '% (climaf_name, doc) + \
           'return climaf.driver.ceval_evt("%s","%s",*args,**dic)\n' \
            %(climaf_name, script)
    exec(defs, globals())  #
    exec(defs, locals())  #
    exec("from climaf.ESMValTool_diags import %s" % climaf_name, sys.modules['__main__'].__dict__)
    clogger.debug("ESMValTool script %s has been declared as function %s" % (script, climaf_name))
        
        
def call_evt_script(climaf_name, script, ensembles, *operands, **parameters) :
    """
    Driver for calling an ESMValTool diagnostic script (DS). 

    This function is NOT supposed to be called directly except by CliMAF driver, see doc.

    Arguments :

    - climaf_name : name of the python function associated to the DS

    - script : name of the DS, according to ESMValTool convention

    - ensembles : list of datasets ensemble objects to provide to the
      DS (one member per variable)

    - operands : values of the ensemble objects (i.e. filenames)

    - parameters : additional key/value pairs to provide to the DS

    This drivers creates a directory dedicated to running that DS, and all 
    necessary interface files. It checks that execution was successfull.

    Returns a pair : DS working directory, dictionnary of provenance information

    """
    
    # Initalize most settings 
    settings = {
        'recipe'             : 'CliMAF',
        'script'             : script,
        'version'            : version,
        
        # User may wish to change next attributes for each call
        'auxiliary_data_dir' : None,
        'log_level'          : _translate_loglevel(clogger.getEffectiveLevel()),
        'output_file_type'   : 'png',
        'profile_diagnostic' : False,
        'write_netcdf'       : True,
        'write_plots'        : True,
        'quick_plot'         : {},
        }
    
    # Account for dynamical, un-controlled, script call parameters to update settings
    settings.update(parameters)

    # Create a working directory according to ESMValTool habits
    # (e.g. cvdp_20210523_044731)
    output_dir=settings.get('output_dir','./evtscript_output/')
    tmpdir = output_dir+"/%s_%s"%(climaf_name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    tmpdir = os.path.abspath(tmpdir)+"/"
    os.makedirs(tmpdir)
    
    # Create sub-directories according to ESMValTol habits
    for adir in ['work_dir','run_dir','preproc_dir']:
        settings[adir] = tmpdir + adir.replace('_dir','') 
        if not os.path.exists(settings[adir]):
            os.mkdir(settings[adir])
    # Plot dir doesn't stick to the rule ('plot' -> 'plots')
    settings['plot_dir'] = tmpdir + 'plots'    
    if not os.path.exists(settings['plot_dir']):
        os.mkdir(settings['plot_dir'])

    # Create medata files (one per variable/ensemble, gouped in dict
    # metadatas with key = variable, value = metadata file):
    metadatas = dict()
    for ensemble, value in zip(operands, ensembles) :
        _create_metadata_file(script, ensemble, value, settings['preproc_dir'], metadatas)

    # on pourrait faire un controle sur le fait qu'il y a bien un
    # ensemble par variable déclarée, mais pas sûr que déclarer les
    # variables soit pratiqué dans EVT

    settings['input_files'] = [ metadatas[variable] for variable in metadatas ]

    # Write settings.yaml using dict settings
    settings_filename = settings['run_dir'] + "/settings.yml"
    with open(settings_filename, 'w') as file:
        yaml.safe_dump(settings, file)

    if wrapper is None :
        _init_wrapper()

    # Launch the diagnsotic script using a wrapper
    command = [ wrapper, script, settings_filename ]
    clogger.info("Launching command : " + repr(command))
    tim1 = time.time()
    process = subprocess.Popen(
        command,
        bufsize=2**20,  # Use a large buffer to prevent NCL crash
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=settings['run_dir'],
        env=dict(os.environ),
    )
    logname = settings['run_dir'] + '/log.txt'
    returncode = None
    with open(logname, 'ab') as log:
        while returncode is None:
            returncode = process.poll()
            log.write(process.stdout.read())
            # wait, but not long because the stdout buffer may fill up:
            # https://docs.python.org/3.6/library/subprocess.html#subprocess.Popen.stdout
            time.sleep(0.001)
                
    if returncode == 0:
        clogger.debug("Script %s (%s) completed successfully", climaf_name, script)
    else:
        raise Climaf_Error(
            "Diagnostic script {} ({}) failed with return code {}. See the log "
            "in {}".format(climaf_name, script, returncode, logname))
    #
    duration = time.time() - tim1
    clogger.info("Done in %.1f s with %s computation "
                 "(command was :%s )" % (duration, script, command))

    # Returned value is a pair : working directory, dict of provenance information
    try :
        with open(settings['run_dir']+"/diagnostic_provenance.yml","r") as prov :
            prov_dict=yaml.safe_load(prov)
    except :
        raise Climaf_Error("Script %s (%s) didn't produce provenance information",
                           climaf_name, script)
        prov_dict = {}

    return tmpdir,prov_dict
 
                                

def _create_metadata_file(script, ensemble, value, preproc_dir, metadatas) :
    """Create an ESMVamTool diagnostic script interface file of type 'medata file' 

    This yaml file describes each input file of an objects' ENSEMBLE
    provided to a SCRIPT. Input files are those listed in VALUE, as a
    white-space separated list of filenames, and are CliMAF cache
    files (or basic data files). They are provided ot the script as
    symbolic links in directory PREPROC_DIR, and with names built with
    ensemble key, variable name and file period

    A number of descriptors are soughtread from datafiles

    Arg METADATAS is a dict that allows to return the metadata
    filename, the key being the ensemble variable

    """
    if not isinstance(ensemble, cens):
        raise Climaf_Error("EVT scripts like %s only accepts ensembles , which is not the case for %s:"\
                                  % (script,ensemble))
    files=value.split(" ")
    if value != '' and not all(map(os.path.exists, files)):
        raise Climaf_Driver_Error("Internal error : some input file does not exist among %s:" % infile)

    variable = varOf(ensemble[ensemble.order[0]])
    data_dir = preproc_dir + "/" + variable
    os.makedirs(data_dir)
    #
    i=0
    metadata = dict()
    for member in ensemble.order :
        if variable != varOf(ensemble[member]) :
            raise Climaf_Driver_Error("A member has wrong variable (%s rather than %s)"\
                                  % (varOf(ensemble[member]),variable))
        d=dict()
        d['alias']                = member
        d['dataset']              = member
        # recipe_dataset_index : ? numero d'ordre dans la liste des datasets de la recipe ?
        d['recipe_dataset_index'] = i + 1
        d['project']              = projectOf(ensemble[member])
        d['exp']                  = experimentOf(ensemble[member])
        # We assume that the dataset period has complete years
        d['start_year']           = int(timePeriod(ensemble[member]).pr().split("-")[0])
        d['end_year']             = int(timePeriod(ensemble[member]).pr().split("-")[1])
        d['short_name']           = varOf(ensemble[member])
        d['variable_group']       = varOf(ensemble[member])
        d['ensemble']             = realizationOf(ensemble[member])
        d['diagnostic']           = script
        d['preprocessor']         = 'default'

        # Create a symbolic link in preproc dir for the input file
        afile = files[i]
        i += 1
        link_name = data_dir + "/" + member + "_" + variable + \
                    "_%d"%d['start_year'] + "-" + "%d"%d['end_year'] + ".nc"
        if os.path.exists(link_name):
            os.remove(link_name)
        os.symlink(afile,link_name)
        d['filename']             = link_name

        # Add informations read in file
        freq, inst, lname, table, realm, stdname, units = _read_attr_from_file(afile,variable)
        d['frequency']           = freq
        d['institute']           = inst.split()
        d['long_name']           = lname
        d['mip']                 = table 
        d['modeling_realm']      = realm.split()
        d['standard_name']       = stdname
        d['units']               = units
        metadata[d['filename']]  = d
        
    # Write metadata file
    metadata_filename =  data_dir + "/metadata.yml"
    with open(metadata_filename, 'w') as file:
        yaml.safe_dump(metadata, file)

    metadatas[variable] = metadata_filename 


def _read_attr_from_file(afile,variable) :
    with ncf(afile,'r') as fileobject:
        try :
            freq = fileobject.frequency
        except :
            freq = "N/A"
        try :
            inst = fileobject.institution_id
        except :
            inst = "N/A"
        try :
            table = fileobject.table_id
        except :
            table = "N/A"
        try :
            realm = fileobject.realm
        except :
            realm = "N/A"
            
        var = fileobject.variables[variable]
        try :
            lname = var.long_name
        except :
            lname = "N/A"
        try :
            stdname = var.standard_name
        except :
            stdname = "N/A"
        try :
            units = var.units
        except :
            units = "N/A"
    return (freq, inst, lname, table, realm, stdname, units)


def _translate_loglevel(level) :
    """
    Returns a string corresponding to the logging LEVEL, understandable by ESMVamTool
    """
    
    if level == logging.INFO :
        return "info"
    elif level == logging.DEBUG :
        return "debug"
    elif level == logging.WARNING :
        return "warning"
    elif level == logging.ERROR :
        return "error"
    elif level == logging.CRITICAL :
        return "critical"
    else :
        return level
    
def _init_wrapper():
    """
    Find a wrapper script for ESMValTool diags for the current platform. Its task 
    is to set the environment for executing such diags, and to launch it. See an 
    example of such wrapper in 
    :download:`$CLIMAF/scripts/ESMValTool_python_diags_wrapper_for_ciclad.sh<../scripts/EVT_python_diags_wrapper_for_ciclad.sh>`
    """
    if atIPSL :
        scripts_dir = __file__ + "/../../scripts" 
        wrapper= scripts_dir / "EVT_python_diags_wrapper_for_ciclad.sh"
    else:
        raise Climaf_Error(
            "Cannot find a relevant wrapper for ESMValTool diagnostic scripts "
            "for current platform (in directory {})".format(scripts_dir))

