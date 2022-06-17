-----------------------------------------------------------------
Calling ESMValTools diagnostic scripts
-----------------------------------------------------------------


`ESMValTool <https://docs.esmvaltool.org/>`_ is a software package for evaluating Earth Sytem Models ; it includes a large number of ``recipes`` which are configuration files for its runs (see a `recipe example
<https://github.com/ESMValGroup/ESMValTool/blob/main/esmvaltool/recipes/examples/recipe_python.yml>`_); such ``recipes`` include a data preparation and preprocessing step, followed by the call of one or more diagnostic scripts.

CliMAF can feed those diagnostic scripts and launch it. The following applies :

Script declaration
------------------
The ESMValTool diagnostic script must be declared using function :py:func:`~climaf.ESMValTool_diags.evt_script` (and using the same name as in ESMValTool recipes); it allows to create a python function for calling the script, herafter called the ``nickname`` function.

Script inputs 
-------------
- when using this feature, it is the user's responsibility to understand which data pre-processing is needed upstream of the diagnostic script and to reproduce that pre-processing using CliMAF, in order to feed the diagnostic consistently. The recipe describes that pre-processing;

- according to ESMValTool's principles, each script input of type ``field`` must be an ensemble of fields, composed of fields representing the same geophysical variable

- these ensembles must be provided as arguments to the ``nickname`` function in the same order than used in ESMValTool recipe's list of variables; 

- any script parameter that can be set in a ``recipe`` can also be set through CliMAF as a keyword argument to the ``nickname`` function call

- other parameters that ESMValTool users set in the config-user.yml file and that ESMValTool passes to the script can also be set through CliMAF at the stage of the ``nickname`` function call. This applies for instance to parameters :
   - ``output_dir`` (defaults to ./evtscript_output/),
   - ``output_type`` (png) ,
   - ``write_netcdf`` (True)
   - ``write_plots`` (True)
   - ``profile_diagnostic`` (False),
   - ``auxiliary_data_dir`` (empty)

- the log level passed to the script is the current CliMAF log level, but can be superseded using parameter ``log_level``
  

Scripts outputs
---------------
- diagnostic script outputs are organized similarly to ESMValtool's : a subdirectory of ``output_dir`` is created for each call, which name includes a date/time stamp and is part of the value returned by the ``nickname`` function call (see below); it includes subdirectories ``preproc``,  ``work``, ``run`` and ``plots``; these sub-directories have a simpler organization than in ESMValTool (less hierarchy levels) because they represent outputs for a simpler run : only the diagnostic script (rather than a full recipe with its pre-processing)

- subdir ``preproc`` includes, like in ESMValTool, one sub-directory per input variable (i.e per input ensemble); each one includes symbolic links to the input data files, which are located in CliMAF cache; the symbolic link name is built using the key (in the ensemble dictionnary), the variable name and the start and end year for the data period; these symbolic names are those used as provenance information by ESMValTool and cannot host the kind of provenance information that CliMAF could provide;

- there is yet no way for CliMAF to handle ESMValTool diagnostic script's output data as CliMAF objects, because ESMValTool doesn't include any rule for **symbolic naming** of these outputs. So, calling an ESMValTool script is more or less a dead-end in the data processing flow.

- ESMValTool generates ``provenance`` information using diagnostic script's outputs, and builds an html index of graphic type outputs, named ``index.html``, in the output dir. The provenance information dictionnary is included in the ``nickname`` function call returned values.


Values returned upon diagnostic script call
-------------------------------------------
Upon invocation, the ``nickname`` function returns a pair of values :

- the name for the script's top-level outputs directory 
  
- the dictionnary of provenance information (see ESMValTool documentation)


ESMValTool scripts wrapper
--------------------------

An helper script is needed in order to set the relevant environment for calling ESMValTool scripts before calling it. Such a wrapper script must be tuned for each ESMValTool install one wants to use, and to the specifics of the platform for handling software envroinments. Variable :py:func:`~climaf.ESMValTool_diags.wrapper` should be set to the path for such a wrapper script. If it is not set, CliMAF will try to use hard-coded values depending on the current platform. At the time of writing, hard-coded values are limited to the case of Ciclad,  and the corresponding wrapper is available in CliMAF distribution :download:`as scripts/ESMValTool_python_diags_wrapper_for_ciclad.sh <../scripts/ESMValTool_python_diags_wrapper_for_ciclad.sh>`. However, this script may have to be updated for an alternate ESMValTool install location.

Example
--------

The example below is also available for :download:`download here <../examples/ESMValTool_cvdp.py>`

.. code-block:: bash

    # An example of declaring and calling an ESMValTool script from CliMAF
    
    from climaf.api import *
    from climaf.ESMValTool_diags import evt_script
    
    # If your platform is not Ciclad, you must tell which is the wrapper for ESMValTool scripts
    climaf.ESMValTool_diags.wrapper = \
        "/home/ssenesi/climaf_installs/climaf_running/scripts/"+\
        "ESMValTool_python_diags_wrapper_for_ciclad.sh"
    
    # Create a CliMAF function for calling the ESMValTool diagnostic script
    # (use the same syntax as the ESMVaTool recipe for designating the script)
    evt_script("call_cvdp", "cvdp/cvdp_wrapper")
    
    # Prepare input datasets for the diag. 
    base      = dict(project="CMIP6", experiment="historical",
                     realization='r1i1p1f2',  table="Amon", period="1850-1855", )
    models    = [ "CNRM-CM6-1", "CNRM-ESM2-1"]
    
    variables = [ "ts", "tas", "pr", "psl" ]
    
    ensembles = []
    for variable in variables:
        ensemble = cens(
            {
                model :  ds(model=model, variable=variable, **base)
                for model in models
            })
        ensembles.append(ensemble)
    
    # Note : here, for other diagnostic scripts, you may have to reproduce
    # the preprocessing steps that ESMValTool recipes implement upstream
    # of the diagnostic script. For CVDP, there is actually no such
    # preprocessing
        
    # Call the diag. You may provide parameters that are known to ESMValTool
    # or to the diagnostic script
    wdir, prov = call_cvdp(*ensembles, output_dir="./out", write_netcdf=False)
    
    # First returned value is the diag's working directory
    print(wdir)
    
    # Second one is a dictionnary of provenance information which
    # describes all outputs (either graphics or NetCDF files) by various
    # attributes, one of which being a 'caption'
    one_output, its_attributes=prov.popitem()
    print(one_output, its_attributes['caption'])
    
    # But there is no further established framework in ESMValTool for a
    # diagnostic to 'publish' a list of identifiers for its outputs



Public functions and variables involved
---------------------------------------

.. autofunction:: climaf.ESMValTool_diags.evt_script

.. autodata:: climaf.ESMValTool_diags.wrapper

Private functions and variables involved
----------------------------------------

.. autofunction:: climaf.driver.ceval_evt

.. autofunction:: climaf.ESMValTool_diags.call_evt_script

