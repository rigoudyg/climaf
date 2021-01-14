#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CliMAF environment tools.
Those variables are used everywhere ; hence, they are grouped here for easing import.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import sys
import subprocess
try:
    from commands import getoutput, getstatusoutput
except ImportError:
    from subprocess import getoutput, getstatusoutput


from env.site_settings import atTGCC, atIPSL, onCiclad

# Variables

#: Dictionary of declared projects (type is cproject)
cprojects = dict()

#: Dictionary of aliases dictionaries
aliases = dict()

#: Dictionary of frequency names dictionaries
frequencies = dict()

#: Dictionary of realms names dictionaries
realms = dict()

#: Dictionary of scripts names dictionaries
cscripts = dict()

#: Dictionary of operators names dictionaries
operators = dict()

#: Dictionary of derived variables names dictionaries
derived_variables = dict()

#: Dictionary of macros names
cmacros = dict()

#: List of known formats
known_formats = ['nc', 'graph', 'txt']

#: List of graphic formats
graphic_formats = ['png', 'pdf', 'eps']

#: List of none formats
none_formats = [None, 'txt']

#: List of locations
locs = list()

#: Log directory
logdir = "."

#: Define whether we stamp the data files with their CRS.
# True means mandatory. None means : please try. False means : don't try
stamping = True


# Check commands available
def my_which(soft):
    rep = subprocess.check_output("which {}".format(soft), shell=True).decode("utf-8")
    if "\n" in rep:
        rep = rep.replace("\n", "")
    return rep


def bash_command_to_str(cmd):
    return str.replace(subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).stdout.readlines()[0], '\n', '')


if os.environ.get('CLIMAF_CHECK_DEPENDENCIES', "yes") == "yes":
    print("python => " + sys.version)
    print("---")
    print("Required softwares to run CliMAF => you are using the following versions/installations:")
    try:
        ncl_software = my_which("ncl")
        print("ncl " + getoutput(ncl_software + ' -V') + " => " + ncl_software)
    except:
        ncl_software = None
        print("Warning: ncl not found -> can't use CliMAF plotting scripts")
    try:
        cdo_software = my_which("cdo")
        tmp = str.split(getstatusoutput(cdo_software + ' -V')[1], ' ')
        print("cdo " + tmp[tmp.index('version') + 1] + " => " + cdo_software)
    except:
        cdo_software = None
        print("Error: cdo not found -> CDO is mandatory to run CliMAF")
    try:
        ncks_sofware = my_which("ncks")
        tmp = str.split(getstatusoutput(ncks_sofware + ' --version')[1], ' ')
        print("nco (ncks) " + tmp[tmp.index('version') + 1] + " => " + ncks_sofware)
    except:
        ncks_sofware = None
        print("Warning: nco not found -> can't use nco from CliMAF")
    try:
        if atTGCC or atIPSL or onCiclad:
            ncdump_software = '/prodigfs/ipslfs/dods/jservon/miniconda/envs/cesmep_env/bin/ncdump'
            ncdump_ret = getstatusoutput(ncdump_software)
            print("ncdump " + ncdump_ret[-1].split('\n')[-1].split()[3] + " => " + ncdump_software)
        else:
            ncdump_software = my_which("ncdump")
            binary_info = getstatusoutput(ncdump_software + " --version")[-1].split("\n")[-1]
            binary_info = binary_info.split("version")[-1].split("of")[0].strip()
            print("ncdump " + binary_info + " => " + ncdump_software)
    except:
        ncdump_software = None
        print("Warning: ncdump not found -> can't use ncdump from CliMAF")
    # Check that tools for stamping are available or enforce stamping to None
    print("Check stamping requirements")
    do_stamping = True
    try:
        ncatted_software = my_which("ncatted")
        print("nco (ncatted) found -> " + ncatted_software)
    except:
        ncatted_software = None
        print("nco (ncatted) not available, can not stamp netcdf files")
        do_stamping = False
    try:
        convert_software = my_which("convert")
        print("convert found -> " + convert_software)
    except:
        convert_software = None
        print("convert not available, can not stamp png files")
        do_stamping = False
    try:
        pdftk_software = my_which("pdftk")
        print("pdftk found -> " + pdftk_software)
    except:
        pdftk_software = None
        print("pdftk not available, can not stamp pdf files")
        do_stamping = False
    try:
        exiv2_software = my_which("exiv2")
        print("exiv2 found -> " + exiv2_software)
    except:
        exiv2_software = None
        print("exiv2 not available, can not stamp eps files")
        do_stamping = False
    if not do_stamping and stamping is True:
        print("At least one stamping requirement is not fulfilled, turn it to None.")
        stamping = None
    print("---")
