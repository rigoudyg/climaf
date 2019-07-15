#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Climaf is documented at ReadTheDocs : http://climaf.readthedocs.org/

"""
from __future__ import print_function

import time
import os

# Created : S.Sénési - 2014

__all__ = ["site_settings", "cache", "classes", "clogging", "dataloc", "driver", "netcdfbasics",
           "operators", "period", "standard_operators", "cmacro", "html", "functions", "plot",
           "projects", "derived_variables"]

version = "pre_1.2.12"


def tim(string=None):
    """
    Utility function : print duration since last call
    Init it by a call without arg
    """
    if not string or not getattr(tim, 'last'):
        tim.last = time.time()
    else:
        delta = time.time() - tim.last
        tim.last = time.time()
        # if ("dotiming" in vars() and dotiming) :
        if False:
            print("Duration %.1f for step %s" % (delta, string), file=sys.stderr)


xdg_bin = False
if os.system("type xdg-open >/dev/null 2>&1") == 0:
    xdg_bin = True

already_inited = False
onrtd = os.environ.get('READTHEDOCS', None) == 'True'

if not already_inited and not onrtd:
    import sys
    from climaf.driver import logdir

    #
    already_inited = True
    #
    tim()
    import atexit

    tim("atexit")
    #
    import clogging
    import site_settings
    import cache
    import standard_operators
    import cmacro
    import operators
    import subprocess
    import commands
    
    def my_which(soft):
        p = subprocess.Popen(["which",soft], stdout=subprocess.PIPE)
        return str.replace(p.stdout.readlines()[0],'\n','')
    def bash_command_to_str(cmd):
        return str.replace(subprocess.Popen(str.split(cmd,' '), stdout=subprocess.PIPE).stdout.readlines()[0],'\n','')

    tim("imports")
    print("CliMAF version = " + version, file=sys.stderr)
    print("CliMAF install => " + "/".join(__file__.split("/")[:-2]))
    print("python => "+my_which('python'))
    print("---")
    print("Required softwares to run CliMAF => you are using the following versions/installations:")
    try:
       print("ncl "+commands.getoutput(my_which('ncl')+' -V')+" => "+my_which('ncl'))
    except:
       print("Warning: ncl not found -> can't use CliMAF plotting scripts")
    try:
       tmp = str.split(commands.getstatusoutput(my_which('cdo')+' -V')[1],' ')
       print("cdo "+tmp[tmp.index('version')+1]+" => "+my_which('cdo'))
    except:
       print("Error: cdo not found -> CDO is mandatory to run CliMAF")
       my_which('cdo')
    try:
       tmp = str.split(commands.getstatusoutput(my_which('ncks')+' --version')[1], ' ')
       print("nco (ncks) "+tmp[tmp.index('version')+1]+" => "+my_which('ncks'))
    except:
       print("Warning: nco not found -> can't use nco from CliMAF")
    try:
       print("ncdump "+commands.getstatusoutput('/prodigfs/ipslfs/dods/jservon/miniconda/envs/cesmep_env/bin/ncdump')[-1].split('\n')[-1].split()[3]+" => "+my_which('ncdump'))
    except:
       print("Warning: ncdump not found -> can't use ncdump from CliMAF")
    print("---")

    logdir = os.path.expanduser(os.getenv("CLIMAF_LOG_DIR", "."))
    #
    # Set default logging levels
    clogging.logdir = os.path.expanduser(os.getenv("CLIMAF_LOG_DIR", "."))
    clogging.clog(os.getenv("CLIMAF_LOG_LEVEL", "warning"))
    clogging.clog_file(os.getenv("CLIMAF_LOGFILE_LEVEL", "info"))
    tim("loggings")
    #
    # Decide for cache location
    if site_settings.onCiclad:
        default_cache = "/data/" + os.getenv("USER") + "/climaf_cache"
    else:
        default_cache = "~/tmp/climaf_cache"
    cachedir = os.getenv("CLIMAF_CACHE", default_cache)
    cache.setNewUniqueCache(cachedir, raz=False)
    print("Cache directory set to : " + cachedir + " (use $CLIMAF_CACHE if set) ", file=sys.stderr)
    tim("set cache")
    # Decide for cache location for remote data
    remote_cachedir = os.getenv("CLIMAF_REMOTE_CACHE", cachedir + "/remote_data")
    print("Cache directory for remote data set to : " + remote_cachedir + " (use $CLIMAF_REMOTE_CACHE if set) ",
          file=sys.stderr)
    #
    # Init dynamic CliMAF operators, and import projects and some funcs in main
    tim("execs_projects")
    exec "from climaf.classes   import ds, eds, cens, fds" in sys.modules['__main__'].__dict__
    tim("execs_classes")
    exec "from climaf.operators import cscript" in sys.modules['__main__'].__dict__
    tim("execs_cscript")
    standard_operators.load_standard_operators()
    tim("load_ops")
    exec "from climaf.projects  import *" in sys.modules['__main__'].__dict__
    #
    # Read and execute user config file
    conf_file = os.path.expanduser("~/.climaf")
    if os.path.isfile(conf_file):
        execfile(conf_file, sys.modules['__main__'].__dict__)
    tim(".climaf")
    #
    # Init and load macros
    macroFilename = "~/.climaf.macros"
    cmacro.read(macroFilename)
    print("Available macros read from %s are : %s" % (macroFilename, repr(cmacro.cmacros.keys())),
          file=sys.stderr)
    tim("macros")
    #
    # Load cache index
    cache.cload()
    tim("cload")
    #
    atexit.register(cmacro.write, macroFilename)
    atexit.register(cache.csync)
    tim("atexit")
    if cache.stamping:
        # Check if exiv2 is installed
        #
        if (os.system("type exiv2 >/dev/null 2>&1") != 0) and 'eps' in operators.graphic_formats:
            operators.graphic_formats.remove('eps')
            print("exiv2 is not installed so you can not use 'eps' output format")
