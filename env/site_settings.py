#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standard site settings for working with CliMAF.

"""

from __future__ import print_function, division, unicode_literals, absolute_import

import os
import sys
import platform

from .clogging import clogger


atCNRM = False
atCerfacs = False
atIPSL = False
onCiclad = False
onSpirit = False
atTGCC = False
onAda = False
onErgon = False
atIDRIS = False
onJeanZay = False
onSpip = False

HostName = os.uname()[1].strip().lower()
Home = os.getenv('HOME')

# print 'Hostname:', HostName

if os.path.exists('/ccc') and not os.path.exists('/data'):
    atTGCC = True
    atIPSL = True
if os.path.exists('/cnrm'):
    atCNRM = True
if 'ciclad' in HostName or 'loholt' in HostName or 'ipsl.polytechnique.fr' in HostName or 'climserv' in HostName:
    onCiclad = True
    atIPSL = True
if 'spirit' in HostName:
    onSpirit = True
    atIPSL = True
if 'ada' in HostName:
    onAda = True
    atIDRIS = True
    atIPSL = True
if 'ergon' in HostName:
    onErgon = True
    atIDRIS = True
    atIPSL = True
if 'jean-zay' in HostName:
    onJeanZay = True
    atIDRIS = True
    atIPSL = True
if 'Spip' in HostName or 'lsce3005' in HostName or 'lsce3072' in HostName or os.path.exists(Home + '/.spip'):
    onSpip = True
    atIPSL = True
    print('Spip trouve')
    VolumesDir = os.getenv('VolumesDir')
if os.path.exists('/data/scratch/globc'):
    atCerfacs = True


def _found_python_version_to_use(list_dirs, python_version):
    if python_version in list_dirs:
        return True, python_version
    elif "." in python_version:
        python_version = ".".join(python_version.split(".")[:-1])
        return _found_python_version_to_use(list_dirs, python_version)
    else:
        return False, list_dirs


if atCNRM:
    additional_packages = os.sep.join(["", "cnrm", "est", "COMMON", "climaf", "add_packages", "lib"])
    if os.path.isdir(additional_packages):
        rep = os.listdir(additional_packages)
        rep = [r for r in rep if "python" in r]
        python_version = platform.python_version()
        found, python_version_to_add = _found_python_version_to_use(rep, python_version)
        if found:
            sys.path.append(os.sep.join([additional_packages, python_version_to_add, "site-packages"]))
        else:
            for r in rep:
                sys.path.append(os.sep.join([additional_packages, r, "site-packages"]))
    else:
        print("Warning: additional packages not found, could cause issues.")
    # Remove some environment variables which cause issues with cdo
    for env_var in ["MAGPLUS_DEBUG", "MAGPLUS_INFO"]:
        if env_var in os.environ:
            clogger.warning(f"Unset {env_var} which causes issues with cdo")
            del os.environ[env_var]
