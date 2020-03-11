#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Climaf is documented at ReadTheDocs : http://climaf.readthedocs.org/

"""
from __future__ import print_function

import time
import os

# Created : S.Sénési - 2014

__all__ = ["cache", "classes", "dataloc", "driver", "netcdfbasics",
           "operators", "period", "standard_operators", "cmacro", "html", "functions", "plot",
           "projects", "derived_variables"]

version = "1.2.13"


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
    import env.clogging as clogging
    import env.site_settings as site_settings
    import cache
    import standard_operators
    import cmacro
    import operators
    import subprocess
    import commands


    def my_which(soft):
        p = subprocess.Popen(["which", soft], stdout=subprocess.PIPE)
        return str.replace(p.stdout.readlines()[0], '\n', '')


    def bash_command_to_str(cmd):
        return str.replace(subprocess.Popen(str.split(cmd, ' '), stdout=subprocess.PIPE).stdout.readlines()[0], '\n',
                           '')


    tim("imports")
    print("CliMAF version = " + version, file=sys.stderr)
    print("CliMAF install => " + "/".join(__file__.split("/")[:-2]))
    if os.environ.get('CLIMAF_CHECK_DEPENDENCIES', "yes") == "yes" :
        print("python => " + my_which('python'))
        print("---")
        print("Required softwares to run CliMAF => you are using the following versions/installations:")
        try:
            print("ncl " + commands.getoutput(my_which('ncl') + ' -V') + " => " + my_which('ncl'))
        except:
            print("Warning: ncl not found -> can't use CliMAF plotting scripts")
        try:
            tmp = str.split(commands.getstatusoutput(my_which('cdo') + ' -V')[1], ' ')
            print("cdo " + tmp[tmp.index('version') + 1] + " => " + my_which('cdo'))
        except:
            print("Error: cdo not found -> CDO is mandatory to run CliMAF")
        try:
            tmp = str.split(commands.getstatusoutput(my_which('ncks') + ' --version')[1], ' ')
            print("nco (ncks) " + tmp[tmp.index('version') + 1] + " => " + my_which('ncks'))
        except:
            print("Warning: nco not found -> can't use nco from CliMAF")
        try:
            if site_settings.atTGCC or site_settings.atIPSL or site_settings.onCiclad:
                ncdump_ret = commands.getstatusoutput('/prodigfs/ipslfs/dods/jservon/miniconda/envs/cesmep_env/bin/ncdump')
                print("ncdump " + ncdump_ret[-1].split('\n')[-1].split()[3] + " => " + my_which('ncdump'))
            else:
                binary_info = commands.getstatusoutput(my_which("ncdump") + " --version")[-1].split("\n")[-1]
                binary_info = binary_info.split("version")[-1].split("of")[0].strip()
                print("ncdump " + binary_info + " => " + my_which('ncdump'))
        except:
            print("Warning: ncdump not found -> can't use ncdump from CliMAF")
        # Check that tools for stamping are available or enforce stamping to None
        print("Check stamping requirements")
        do_stamping = True
        try:
            print("nco (ncatted) found -> " + my_which("ncatted"))
        except:
            print("nco (ncatted) not available, can not stamp netcdf files")
            do_stamping = False
        try:
            print("convert found -> " + my_which("convert"))
        except:
            print("convert not available, can not stamp png files")
            do_stamping = False
        try:
            print("pdftk found -> " + my_which("pdftk"))
        except:
            print("pdftk not available, can not stamp pdf files")
            do_stamping = False
        try:
            print("exiv2 found -> " + my_which("exiv2"))
        except:
            print("exiv2 not available, can not stamp eps files")
            do_stamping = False
        if not do_stamping and cache.stamping is True:
            print("At least one stamping requirement is not fulfilled, turn it to None.")
            cache.stamping = None
        print("---")
    #
    # Check that the variable TMPDIR, if defined, points to an existing directory
    if "TMPDIR" in os.environ and not os.path.isdir(os.environ["TMPDIR"]):
        # raise OSError("TMPDIR points to a non existing directory! Change the value of the variable to go on.")
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
    macroFilename = os.environ.get("CLIMAF_MACROS", "~/.climaf.macros")
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
