#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Climaf is documented at ReadTheDocs : http://climaf.readthedocs.org/

"""
from __future__ import print_function, division, unicode_literals, absolute_import

import time
import os

# Created : S.Sénési - 2014

__all__ = ["cache", "classes", "dataloc", "driver", "netcdfbasics",
           "operators", "period", "standard_operators", "cmacro", "html", "functions", "plot",
           "projects", "derived_variables"]

import env.environment

version = "2.0.0"


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

    #
    already_inited = True
    #
    tim()
    import atexit

    tim("atexit")
    #
    print("CliMAF version = " + version, file=sys.stderr)
    print("CliMAF install => " + "/".join(__file__.split("/")[:-2]))
    from env.environment import *

    tim("softwares")
    #
    import env.clogging as clogging
    import env.site_settings as site_settings
    from . import cache
    from . import standard_operators
    from . import cmacro
    from . import operators

    tim("imports")
    #
    # Check that the variable TMPDIR, if defined, points to an existing directory
    if "TMPDIR" in os.environ and not os.path.isdir(os.environ["TMPDIR"]):
        # raise OSError("TMPDIR points to a non existing directory! Change the value of the variable to go on.")
        if os.path.exists(os.environ["TMPDIR"]):
            os.remove(os.environ["TMPDIR"])
        os.makedirs(os.environ["TMPDIR"])

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
    exec("from climaf.classes   import ds, eds, cens, fds", sys.modules['__main__'].__dict__)
    tim("execs_classes")
    exec("from climaf.operators import cscript", sys.modules['__main__'].__dict__)
    tim("execs_cscript")
    standard_operators.load_standard_operators()
    tim("load_ops")
    from . import projects
    exec("from climaf.projects  import %s" % ",".join(projects.__all__), sys.modules['__main__'].__dict__)
    #
    # Read and execute user config file
    conf_file = os.path.expanduser("~/.climaf")
    if os.path.isfile(conf_file):
        exec(compile(open(conf_file).read(), conf_file, "exec"), sys.modules['__main__'].__dict__)
    tim(".climaf")
    #
    # Init and load macros
    macroFilename = os.environ.get("CLIMAF_MACROS", "~/.climaf.macros")
    cmacro.read(macroFilename)
    print("Available macros read from %s are : %s" % (macroFilename, repr(list(cmacros))),
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
        # graphic_formats = environment.get_variable("climaf_graphic_formats")
        if (os.system("type exiv2 >/dev/null 2>&1") != 0) and 'eps' in graphic_formats:
            graphic_formats.remove('eps')
            print("exiv2 is not installed so you can not use 'eps' output format")
