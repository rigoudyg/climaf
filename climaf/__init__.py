"""
Climaf is documented at ReadTheDocs : http://climaf.readthedocs.org/

"""
from __future__ import print_function

# Created : S.Senesi - 2014

__all__=[ "site_settings", "cache", "classes", "clogging", "dataloc", "driver", "netcdfbasics",
          "operators", "period", "standard_operators", "cmacro", "html", "functions", "plot",
          "projects", "derived_variables" ]

version="1.2.9"

import time,os, os.path

def tim(string=None):
    """
    Utility function : print duration since last call
    Init it by a call without arg
    """
    if not string  or not getattr(tim,'last') :
        tim.last=time.time()
    else :
        delta=time.time()-tim.last
        tim.last=time.time()
        #if ("dotiming" in vars() and dotiming) :
        if False : print("Duration %.1f for step %s"%(delta,string),file=sys.stderr)

xdg_bin=False
if (os.system("type xdg-open >/dev/null 2>&1")== 0) :
    xdg_bin=True

already_inited=False
onrtd = os.environ.get('READTHEDOCS', None) == 'True'


if not already_inited  and not onrtd : 
    import sys
    from climaf.driver import logdir
    #
    already_inited=True
    #
    tim()
    import atexit
    tim("atexit")
    #
    import clogging, site_settings, cache, standard_operators, cmacro, operators
    tim("imports")
    print("Climaf version = "+version,file=sys.stderr)
    logdir=os.path.expanduser(os.getenv("CLIMAF_LOG_DIR","."))
    #
    # Set default logging levels
    clogging.logdir=os.path.expanduser(os.getenv("CLIMAF_LOG_DIR","."))
    clogging.clog(os.getenv("CLIMAF_LOG_LEVEL","warning"))
    clogging.clog_file(os.getenv("CLIMAF_LOGFILE_LEVEL","info"))
    tim("loggings")
    #    
    # Decide for cache location
    if site_settings.onCiclad :
        default_cache="/data/"+os.getenv("USER")+"/climaf_cache"
    else: default_cache="~/tmp/climaf_cache"
    cachedir=os.getenv("CLIMAF_CACHE",default_cache)
    cache.setNewUniqueCache(cachedir,raz=False)
    print ("Cache directory set to : "+cachedir+" (use $CLIMAF_CACHE if set) ",file=sys.stderr)
    tim("set cache")
    # Decide for cache location for remote data
    remote_cachedir=os.getenv("CLIMAF_REMOTE_CACHE",cachedir+"/remote_data")
    print ("Cache directory for remote data set to : "+remote_cachedir+" (use $CLIMAF_REMOTE_CACHE if set) ",file=sys.stderr)
    #
    # Init dynamic CliMAF operators, and import projects and some funcs in main
    tim("execs_projects")
    exec("from climaf.classes   import ds, eds, cens, fds") in sys.modules['__main__'].__dict__
    tim("execs_classes")
    exec("from climaf.operators import cscript") in sys.modules['__main__'].__dict__
    tim("execs_cscript")
    standard_operators.load_standard_operators()
    tim("load_ops")
    exec("from climaf.projects  import *") in sys.modules['__main__'].__dict__
    #
    # Read and execute user config file
    conf_file=os.path.expanduser("~/.climaf")
    if os.path.isfile(conf_file) :
        execfile(conf_file,sys.modules['__main__'].__dict__)
    tim(".climaf")
    #
    # Init and load macros
    macroFilename="~/.climaf.macros"
    cmacro.read(macroFilename)
    print("Available macros read from %s are : %s"%(macroFilename,`cmacro.cmacros.keys()`),
          file=sys.stderr)
    tim("macros")
    #
    # Load cache index
    cache.cload()
    tim("cload")
    #
    atexit.register(cmacro.write,macroFilename)
    atexit.register(cache.csync)
    tim("atexit")
    if cache.stamping :
        # Check if exiv2 is installed
        #
        if (os.system("type exiv2 >/dev/null 2>&1") != 0) and 'eps' in operators.graphic_formats:
            operators.graphic_formats.remove('eps')
            print("exiv2 is not installed so you can not use 'eps' output format")


