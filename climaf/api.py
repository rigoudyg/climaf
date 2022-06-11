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

 - ``craz``     : reset fields cache

 - ``raz_cvalues`` : reset scalar values cache

 - ``csync``    : save cache index to disk
 
 - ``ccost``    : provide compute costs for an object


- utility functions :

 - ``clog``     : tune verbosity

 - ``clog_file``: tune verbosity for log file

"""
# Created : S.Senesi - 2014

from __future__ import print_function, division, unicode_literals, absolute_import


import os
#
from env.environment import *
from env.clogging import clogger, clog, clog_file, logdir
from env.site_settings import atCNRM, onCiclad, onSpirit, atTGCC, atIDRIS, atIPSL, onSpip
#
import climaf

# Declare standard projects and standard data locations
from .projects import *

#############################################################################################
# All CliMAF functions we want to provide as top-level functions when
# this module is loaded as "from ... import *"
#############################################################################################
#
from climaf.classes import cdef, cdataset, ds, cproject, cpage, \
    cfreqs, cens, eds, fds, cpage_pdf, varOf, crealms
from climaf.cmacro import macro
from climaf.driver import ceval, cfile, cshow, cMA, cvalue, cimport, cexport, calias, efile
from climaf.dataloc import dataloc
from climaf.operators import cscript, fixed_fields
from climaf.operators_derive import derive
from climaf.cache import craz, csync, cdump, cdrop, clist, cls, crm, cdu, \
    cwc, cprotect, raz_cvalues, ccost
from climaf.plot.plot_params import plot_params, hovm_params
from climaf.plot.varlongname import varlongname
#
from climaf.derived_variables import *
from climaf.functions import *
from climaf.easyCMIP_functions import *


#: Path for the CliMAF package. From here, can write e.g. ``cpath+"../scripts"``. The value shown in the doc is not
# meaningful for your own CliMAF install
cpath = os.path.abspath(climaf.__path__[0])


def cerr():
    """ Display file 'last.out' (stdout and stderr of last operator call)

    """
    os.system('cat ' + logdir + '/last.out')
