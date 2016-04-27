plot_params : python dictionary of default plotting parameters by variable and context (full_field, bias, model_model)
-----------------------------------------------------------------------------------------------------------------------

Returns a dictionary of default plotting parameters (isolines, color palettes...) by variable and context, i.e. the full field (full_field), bias (bias), or model-model difference (model_model).

This type of dictionary is typically passed to plot with "**".

plot_params loads a set of default CliMAF plotting parameters for both 'atmos' and 'ocean'. Then, it updates with sets of parameters that are specific to the centers (for instance CNRM or IPSL).

Eventually, it can take a custom dictionary as an argument; it will use it to update the dictionary.

The user can use climaf/plot/atmos_plot_params.py as an example to create a custom dictionary.

**Provider / contact** : climaf at meteo dot fr

**Input** : a variable name (string) and a context (string, choose among full_field, bias, model_model)

**Mandatory argument**: a variable name

**Output** : a python dictionary with plotting parameters to be used by plot() 

**Climaf call example** ::
 
  >>> var = 'pr'
  >>> climato_dat = time_average(ds(variable=var, project='CMIP5', ...))       # here, the annual mean climatology of a CMIP5 dataset for variable var
  >>> climato_ref = time_average(ds(variable=var, project='ref_climatos',...)) # the annual mean climatology of a reference dataset for variable var

  >>> bias = diff_regrid(climato_dat,climato_ref)         # We compute the bias map with diff_regrid()
  >>> climato_plot = plot(climato_dat, **plot_params(var,'full_field')) 
  >>> bias_plot = plot(bias, **plot_params(var,'bias'))

  >>> my_custom_params = {'pr':{'bias':{'colors':'-10 -5 -2 -0.5 -0.2 -0.1 0 0.1 0.2 0.5 1 2 5 10'}}}
  >>> bias_plot_custom_params = plot(bias, **plot_params(var,'bias',custom_plot_params=my_custom_params)

  >>> # How to import custom params stored in a my_custom_plot_param_file.py file in the working directory
  >>> from my_custom_plot_param_file import dict_plot_params as my_custom_params
  >>> bias_plot_custom_params = plot(bias, **plot_params(var,'bias',custom_plot_params=my_custom_params)


**Side effects** : none

**Implementation** :

Imports python dictionaries and merge them together in the plot_params functions; see the code and dictionary files in climaf/plot
