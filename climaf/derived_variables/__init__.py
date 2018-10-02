
__all__=[ "atmosphere_derived_variables", "ocean_derived_variables" ]

from climaf.site_settings import atIPSL
# -- Load only the ipsl derived variables if we are at IPSL
if atIPSL:
   import ipsl_derived_variables
