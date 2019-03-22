#!/usr/bin/python
# -*- coding: utf-8 -*-
# -- Import the dictionnaries of plot params:
from climaf.site_settings import *

# --> Import the default CliMAF sets of plot params
# --> for atmosphere
import atmos_plot_params
# --> for ocean
import ocean_plot_params
# --> for land
import land_plot_params

centerspecs = False
# --> Import the sets of plot parameters that are specific to the centers (CNRM or IPSL)
if atCNRM:
    import atmos_plot_params_CNRM as atmos_plot_params_centerspecs
    import ocean_plot_params_CNRM as ocean_plot_params_centerspecs
    import land_plot_params_CNRM as land_plot_params_centerspecs

    centerspecs = True
if atIPSL:
    import atmos_plot_params_IPSL as atmos_plot_params_centerspecs
    import ocean_plot_params_IPSL as ocean_plot_params_centerspecs
    import land_plot_params_IPSL as land_plot_params_centerspecs

    centerspecs = True


def plot_params(variable, context, custom_plot_params=None):
    """Returns a dictionary of default plotting parameters (isolines,
    color palettes...) by variable and context, i.e. the full field
    (full_field), bias (bias), or model-model difference
    (model_model).

    This type of dictionary is typically passed to plot with "**".

    plot_params first loads a set of default CliMAF plotting parameters for
    both 'atmos' and 'ocean'.

    Then, it updates with sets of parameters
    that are specific to the centers (for instance CNRM or IPSL).

    Finally, it can take a custom dictionary as an argument; it
    will use it to update the dictionary (i.e. override matching entries).
    Such a dictionnary would be build such as the example
    at :download:`../climaf/plot/atmos_plot_params.py`

    Args:
      variable (string) : variable name;
        The name of the geophysical variable to plot
      context (string) : among 'full_field', 'bias', 'model_model';
        The kind of plot
      custom_plot_params : a user dictionnary that will override CliMAF default values

    Returns : a python dictionary with plotting parameters to be
    used by plot()

    Call example ::

    >>> var = 'pr'
    >>> climato_dat = time_average(ds(variable=var, project='CMIP5', ...))
    # here, the annual mean climatology of a CMIP5 dataset for variable var
    >>> climato_ref = time_average(ds(variable=var, project='ref_climatos',...))
    # the annual mean climatology of a reference dataset for variable var

    >>> bias = diff_regrid(climato_dat,climato_ref)         # We compute the bias map with diff_regrid()
    >>> niceplot_params=plot_params(var,'full_field')
    >>> climato_plot = plot(climato_dat, **nice_plot_params)
    >>> bias_plot = plot(bias, **plot_params(var,'bias'))

    >>> my_custom_params = {'pr':{'bias':{'colors':'-10 -5 -2 -0.5 -0.2 -0.1 0 0.1 0.2 0.5 1 2 5 10'}}}
    >>> bias_plot_custom_params = plot(bias, **plot_params(var,'bias',custom_plot_params=my_custom_params)

    >>> # How to import custom params stored in a my_custom_plot_param_file.py file in the working directory
    >>> from my_custom_plot_param_file import dict_plot_params as my_custom_params
    >>> bias_plot_custom_params = plot(bias, **plot_params(var,'bias',custom_plot_params=my_custom_params)


    """

    defaults = {
        'contours': 1,
        'color': 'temp_19lev',
    }

    per_variable = {}
    # --> Adding the default plot params
    per_variable.update(atmos_plot_params.dict_plot_params)
    per_variable.update(ocean_plot_params.dict_plot_params)
    per_variable.update(land_plot_params.dict_plot_params)
    if centerspecs:
        # --> Then, add the plot params specific to the centers
        per_variable.update(atmos_plot_params_centerspecs.dict_plot_params)
        per_variable.update(ocean_plot_params_centerspecs.dict_plot_params)
        per_variable.update(land_plot_params_centerspecs.dict_plot_params)
    # --> If needed, adding a custom dictionnary of plot params
    if custom_plot_params:
        per_variable.update(custom_plot_params)
    #
    rep = defaults.copy()
    # -- If the variable name is in the list of variables:
    if variable in per_variable:
        var_entry = per_variable[variable]
        for cont in ['default', context]:
            if cont in var_entry:
                rep.update(var_entry[cont])
    else:
        print 'Message from plot_params: ' + variable + ' is not in the list of defined plot parameters'
        # -- if not, we try to split
        tmp_variable = str.split(variable, '_')[0]
        if tmp_variable in per_variable:
            print 'We will use the plot parameters of ' + tmp_variable
            var_entry = per_variable[tmp_variable]
            for cont in ['default', context]:
                if cont in var_entry:
                    rep.update(var_entry[cont])
        else:
            print 'Message from plot_params: ' + variable + ' is not in the list of defined plot parameters'
            print 'We will use the default plot parameters.'
    return rep


def hovm_params(SSTbox_name):
    """Returns a dictionary with domain definition of SST/climate
    specified box for plotting Hovmoller diagrams

    This type of dictionary is typically passed to 'hovm' operator with "**".

    Arg:
      SSTbox_name (string) : SST/climate box name.
      The available boxes are: 'NINO3-4', 'NINO1-2', 'NINO3', 'NINO4', 'GRL',
      'NATL', 'SAT' and 'TPA'.

    Returns : a python dictionary with domain parameters ('latS',
    'latN', 'lonW', 'lonE') to be used by hovm()

    Call example ::

    >>> tas=ds(project='example', simulation='AMIPV6ALB2G', variable='tas', frequency='monthly', period='1980')
    >>> # We plot a Hovmoller diagram (t,y) at longitude close to 10 for 'NINO1-2' domain
    >>> hov_diag=hovm(tas, mean_axis='Point', xpoint=10., title='Temperature', **hovm_params('NINO1-2'))
    >>> cfile(hov_diag)

    """

    SST_boxes = {
        'NINO3-4': {'latS': ' -5.', 'latN': '5.', 'lonW': '-170.', 'lonE': '-120.'},
        'NINO1-2': {'latS': '-10.', 'latN': '0.', 'lonW': '-90.', 'lonE': '-80.'},
        'NINO3': {'latS': '-5.', 'latN': '5.', 'lonW': '-150.', 'lonE': '-90.'},
        'NINO4': {'latS': '-5.', 'latN': '5.', 'lonW': '-160.', 'lonE': '-150.'},
        'GRL': {'latS': '40.', 'latN': '60.', 'lonW': '-60.', 'lonE': '-30.'},
        'NATL': {'latS': '20.', 'latN': '85.', 'lonW': '-90.', 'lonE': '30.'},
        'SAT': {'latS': '6.', 'latN': '18.', 'lonW': '-30.', 'lonE': '10.'},
        'TPA': {'latS': '20.', 'latN': '85.', 'lonW': '-90.', 'lonE': '30.'},
    }

    if SSTbox_name in SST_boxes:
        return (SST_boxes[SSTbox_name])
