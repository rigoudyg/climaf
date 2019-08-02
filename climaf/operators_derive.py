#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CliMAF derive operators tools.
"""
from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.clogging import clogger
from climaf.environment import get_variable, change_variable
from climaf.utils import Climaf_Operator_Error


def is_derived_variable(variable, project):
    """ True if the variable is a derived variable, either in provided project
    or in wildcard project '*'
    """
    derived_variables = get_variable("derived_variables")
    rep = (project in derived_variables and variable in derived_variables[project] or
           "*" in derived_variables and variable in derived_variables["*"])
    clogger.debug("Checking if variable %s is derived for project %s : %s" % (variable, project, rep))
    return rep


def derived_variable(variable, project):
    """ Returns the entry defining a derived variable in requested project or in wildcard project '*'
    """
    derived_variables = get_variable("derived_variables")
    if project in derived_variables and variable in derived_variables[project]:
        rep = derived_variables[project][variable]
    elif "*" in derived_variables and variable in derived_variables["*"]:
        rep = derived_variables['*'][variable]
    else:
        rep = None
    clogger.debug("Derived variable %s for project %s is %s" % (variable, project, rep))
    return rep


def derive(project, derivedVar, Operator, *invars, **params):
    """
    Define that 'derivedVar' is a derived variable in 'project', computed by
    applying 'Operator' to input streams which are datasets whose
    variable names take the values in ``*invars`` and the parameter/arguments
    of Operator take the values in ``**params``

    'project' may be the wildcard : '*'

    Example, assuming that operator 'minus' has been defined as ::

    >>> cscript('minus','cdo sub ${in_1} ${in_2} ${out}')

    which means that ``minus`` uses CDO for substracting the two datasets;
    you may define, for a given project 'CMIP5', a new variable e.g.
    for cloud radiative effect at the surface, named 'rscre',
    using the difference of values of all-sky and clear-sky net
    radiation at the surface by::

    >>> derive('CMIP5', 'rscre','minus','rs','rscs')

    You may then use this variable name at any location you
    would use any other variable name

    Note : you may use wildcard '*' for the project

    Another example is rescaling or renaming some variable;
    here, let us define how variable 'ta'
    can be derived from ERAI variable 't' :

    >>> derive('erai', 'ta','rescale', 't', scale=1., offset=0.)

    **However, this is not the most efficient way to do that**.
    See :py:func:`~climaf.classes.calias()`

    Expert use : argument 'derivedVar' may be a dictionary, which
    keys are derived variable names and values are scripts outputs
    names; example ::

    >>> cscript('vertical_interp', 'vinterp.sh ${in} surface_pressure=${in_2} ${out_l500} ${out_l850} method=${opt}')
    >>> derive('*', {'z500' : 'l500' , 'z850' : 'l850'},'vertical_interp', 'zg', 'ps', opt='log')

    """
    # Action : register the information in a dedicated dict which keys
    # are single derived variable names, and which will be used at the
    # object evaluation step
    # Also : some consistency checks w.r.t. script definition
    scripts = get_variable("scripts")
    if Operator in scripts:
        if not isinstance(derivedVar, dict):
            derivedVar = dict(out=derivedVar)
        for outname in derivedVar:
            if (outname != 'out' and
                    (not getattr(Operator, "outvarnames", None)
                     or outname not in Operator.outvarnames)):
                raise Climaf_Operator_Error("%s is not a named  output for operator %s; type help(%s)" %
                                            (outname, Operator, Operator))
            s = scripts[Operator]
            if s.inputs_number() != len(invars):
                clogger.error("number of input variables for operator %s is %d, which is inconsistent with "
                              "script declaration : %s" % (s.name, len(invars), s.command))
                return
            # TBD : check parameters number  ( need to build
            # its list in cscript.init() )
            derived_variables = get_variable("derived_variables")
            if project not in derived_variables:
                derived_variables[project] = dict()
            clogger.debug("Add derive variable %s obtained with operator %s, output variable %s, input variables %s "
                          "and parameters %s" % (derivedVar[outname], str(Operator), derivedVar[outname],
                                                 str(list(invars)), str(params)))
            derived_variables[project][derivedVar[outname]] = (Operator, derivedVar[outname], list(invars), params)
            change_variable("derived_variables", derived_variables)
    elif Operator in get_variable("operators"):
        clogger.warning("Cannot yet handle derived variables based on internal operators")
    else:
        clogger.error("second argument (%s) must be a script or operator, already declared" % repr(Operator))
