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


