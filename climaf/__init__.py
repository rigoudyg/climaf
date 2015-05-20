"""
Climaf is documented at ReadTheDocs : http://climaf.readthedocs.org/

"""

# Created : S.Senesi - 2014

__all__=[ "site_settings", "cache" , "classes", "clogging", "dataloc", "driver", "netcdfbasics",
          "operators", "period", "standard_operators" , "projects" ,"cmacro"]
import posixpath, os, sys

version="0.6.1"

already_inited=False

if not already_inited  : 
    already_inited=True
    #
    import atexit
    #
    import clogging, site_settings , cache, standard_operators, cmacro
    print "Climaf version = "+version
    #
    # Set default logging levels
    clogging.clog(os.getenv("CLIMAF_LOG_LEVEL","warning"))
    clogging.clog_file(os.getenv("CLIMAF_LOGFILE_LEVEL","info"))
    #    
    # Decide for cache location
    if site_settings.onCiclad :
        default_cache="/data/"+os.getenv("USER")+"/climaf_cache"
    else: default_cache="~/tmp/climaf_cache"
    cache.setNewUniqueCache(os.getenv("CLIMAF_CACHE",default_cache))
    print "You may tune CliMAF cache location by setting $CLIMAF_CACHE before launch"
    #
    # Init dynamic CliMAF operators, and import projects and some funcs in main
    exec "from climaf.projects  import *" in sys.modules['__main__'].__dict__
    exec "from climaf.classes   import ds, eds, cens" in sys.modules['__main__'].__dict__
    exec "from climaf.operators import cscript" in sys.modules['__main__'].__dict__
    standard_operators.load_standard_operators()
    #
    # Read and execute user config file
    conf_file=os.path.expanduser("~/.climaf")
    if os.path.isfile(conf_file) :
        execfile(conf_file,sys.modules['__main__'].__dict__)
    #
    # Init and load macros
    cmacro.read()
    #
    # Load cache index
    cache.cload()
    #
    atexit.register(cmacro.write)
    atexit.register(cache.csync)


