#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CliMAF module ``api`` defines functions for basic CliMAF use : a kind of Application Program Interface for scripting in
Python with CliMAF for easy climate model output processing.

It also imports a few functions from other modules, and declares a number of 'CliMAF standard operators'

Main functions are :

- for data definition and access :

 - ``cproject`` : declare a project and its non-standard attributes/facets

 - ``dataloc``  : set data locations for a series of simulations

 - ``cdef``     : define some default values for datasets attributes

 - ``ds``       : define a dataset object (actually a front-end for ``cdataset``)

 - ``eds``      : define an ensemble dataset object (actually a front-end for ``cens``)

 - ``derive``   : define a variable as computed from other variables

 - `` calias``  : describe how a variable is derived form another, single, one, and which
   variable name should be used in deriving data filename for this variable

- for processing the data

 - ``cscript``  : define a new CliMAF operator (this also defines a new Python function)

 - ``cMA``      : get the Masked Array value of a CliMAF object (compute it)

 - ``cvalue``   : get the value of a CliMAF object which actually is a scalar

 - ``cens``     : define an ensemble of objects

- for managing/viewing results :

 - ``cfile``    : get the file value of a CliMAF object (compute it)

 - ``efile``    : create a single file for an ensemble of CliMAF objects

 - ``cshow``    : display a result of type 'figure'

 - ``cpage``    : create an array of figures (output: 'png' or 'pdf' figure)

 - ``cpage_pdf``: create an array of figures (output: 'pdf' figure)

 - ``cdump``    : tell what's in cache

 - ``cdrop``    : delete the cached file for an object

 - ``cprotect`` : protect the cached file for an object from deletion

 - ``craz``     : reset cache

 - ``csync``    : save cache index to disk


- utility functions :

 - ``clog``     : tune verbosity

 - ``clog_file``: tune verbosity for log file

"""
# Created : S.Senesi - 2014


import os
import os.path
#
import climaf

# Declare standard projects and standard data locations
from projects import *

#####################################################################################################################
# All CliMAF functions we want to provide as top-level functions when this module is loaded as "from ... import *"
#####################################################################################################################
#
from classes import cdef, cdataset, ds, cproject, cprojects, aliases, cpage, cfreqs, cens, eds, fds, cpage_pdf, varOf, \
    crealms
from cmacro import macro, cmacros
from driver import ceval, cfile, cshow, cMA, cvalue, cimport, cexport, calias, efile
from dataloc import dataloc
from operators import cscript, scripts as cscripts, operators, fixed_fields, derive
from cache import craz, csync, cdump, cdrop, clist, cls, crm, cdu, cwc, cprotect
from clogging import clogger, clog, clog_file, logdir
from site_settings import atCNRM, onCiclad, atTGCC, atIDRIS, atIPSL, onSpip
from plot.plot_params import plot_params, hovm_params
from plot.varlongname import varlongname
from derived_variables import *
from functions import *
from easyCMIP_functions import *

#: Path for the CliMAF package. From here, can write e.g. ``cpath+"../scripts"``. The value shown in the doc is not
# meaningful for your own CliMAF install
cpath = os.path.abspath(climaf.__path__[0])


def cerr():
    """ Display file 'last.out' (stdout and stderr of last operator call)

    """
    os.system('cat ' + logdir + '/last.out')
