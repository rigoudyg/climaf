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
    - :doc:`scripts/minus`
    - :doc:`scripts/ncdump`
    - :doc:`scripts/cpdfcrop`

 - graphics
    - :doc:`scripts/plot`
    - :doc:`scripts/curves`
    - :doc:`scripts/ncview`

 - swiss knife |sk| :
    - :doc:`scripts/ccdo`

 - example for two outputs :
    - :doc:`scripts/mean_and_std`

.. toctree::
   :maxdepth: 1

   cdftools

.. |sk| image:: swiss_knife_50.png

Albeit this is not a proper practice, **some more operators may exist in your CliMAF release** which would not be documented here. Please see :ref:`how_to_list_operators` for such cases

A name-sorted list :

.. toctree::
  :glob:

  /scripts/*
