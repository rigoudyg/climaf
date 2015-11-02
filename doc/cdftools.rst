CdfTools
-----------

.. _cdftools: 

 - CDFTools operators; we wrap some operators using similar names; you
   need to have a version of Cdftools 3.0 which is fixed for a few
   issues and which is configured to use CMIP5 standard variable names
   (except for transport variables). Please ask climaf at meteo dot fr
   for getting the changes. CliMAF will test at startup if binary
   'cdfmean' is in your PATH

    - operators based on cdfmean:

      - :doc:`scripts/ccdfmean`
      - :doc:`scripts/ccdfmean_profile`
      - :doc:`scripts/ccdfvar`
      - :doc:`scripts/ccdfvar_profile`
	
    - operators dealing with heat content:
	  
      - :doc:`scripts/ccdfheatc`
      - :doc:`scripts/ccdfheatcm`
      - :doc:`scripts/ccdfmxlheatc`
      - :doc:`scripts/ccdfmxlheatcm`

    - operators dealing with transport:

      - :doc:`scripts/ccdftransport`
      - :doc:`scripts/ccdfvT`

    - operators based on cdfstd:

      - :doc:`scripts/ccdfstd`
      - :doc:`scripts/ccdfstdmoy`
   
    - :doc:`scripts/ccdfsections`
    - :doc:`scripts/ccdfsectionsm`

