.. _standard_operators:


Standard Operators
-------------------------------

CliMAF includes a number of 'Standard Operators', which implement more or less basic climate diagnostics or utilities. This set increases
with scientists contributions (see :ref:`how_to_contribute_a_script`). They are documented here, through
individual documentation files in `REStructured Text format <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
and following :download:`this example <scripts_template.rst>` which renders :doc:`as shows here <scripts_template>`. 
For each operator, the content of the doc file is also made available in the Python on-line help (see :ref:`how_to_list_operators`).

Documented operators as of today : 

 - basic functions:
    - :doc:`scripts/llbox`
    - :doc:`scripts/regrid`
    - :doc:`scripts/regridn`
    - :doc:`scripts/time_average`
    - :doc:`scripts/space_average`

 - graphics
    - :doc:`scripts/plot`
    - :doc:`scripts/lines`
    - :doc:`scripts/timeplot`
    - :doc:`scripts/ncview`

 - swiss knife |sk| :
    - :doc:`scripts/ccdo`

 - example for two outputs :
    - :doc:`scripts/mean_and_std`

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
      - :doc:`scripts/ccdfmxlheatc`

    - operators dealing with transport:

      - :doc:`scripts/ccdftransport`
      - :doc:`scripts/ccdfvT`

    - operators based on cdfstd:

      - :doc:`scripts/ccdfstd`
      - :doc:`scripts/ccdfstdmoy`
   
    - :doc:`scripts/ccdfsections`
    

.. |sk| image:: swiss_knife_50.png

Albeit this is not a proper practice, **some more operators may exist in your CliMAF release** which would not be documented here. Please see :ref:`how_to_list_operators` for such cases

A name-sorted list :

.. toctree::
  :glob:

  /scripts/*
