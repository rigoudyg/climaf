# -- Import the dictionnaries of plot params:
from climaf.site_settings import *

# --> Import the default CliMAF sets of plot params 
# --> for atmosphere
import atmos_plot_params
# --> for ocean
import ocean_plot_params

# --> Import the sets of plot parameters that are specific to the centers (CNRM or IPSL)
if atCNRM:
   import atmos_plot_params_CNRM as atmos_plot_params_centerspecs
   import ocean_plot_params_CNRM as ocean_plot_params_centerspecs
if atIPSL:
   import atmos_plot_params_IPSL as atmos_plot_params_centerspecs
   import ocean_plot_params_IPSL as ocean_plot_params_centerspecs

def plot_params(variable,context, custom_plot_params=None) :
    """
    Return plot parameters as a dict(), according to LMDZ habits , for a given
    variable and a context (among full_field, bias, model_model)
    
    The user can pass his own custom dictionnary of plot parameters with custom_plot_params.

    """

    defaults = { 
        'contours' : 1 ,
        'color'    :'temp_19lev',
    }

    per_variable = {}
    # --> Adding the default plot params
    per_variable.update(atmos_plot_params.dict_plot_params)
    per_variable.update(ocean_plot_params.dict_plot_params)
    # --> Then, add the plot params specific to the centers
    per_variable.update(atmos_plot_params_centerspecs.dict_plot_params)
    per_variable.update(ocean_plot_params_centerspecs.dict_plot_params)
    # --> If needed, adding a custom dictionnary of plot params
    if custom_plot_params:
       per_variable.update(custom_plot_params)
    #
    rep=defaults.copy()
    if variable in per_variable : 
        var_entry=per_variable[variable]
        for cont in [ 'default', context ] :
            if cont in var_entry : rep.update(var_entry[cont])
    return rep
        
