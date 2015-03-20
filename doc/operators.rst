.. _standard_operators:


Standard Operators
-------------------------------

CliMAF includes a number of 'Standard Operators', which implement more or less basic climate diagnostics or utilities. This set increases
with scientists contributions (see :ref:`how_to_contribute_a_script`). They are documented here, through
individual documentation files in `REStructured Text format <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
and following :download:`this example <scripts_template.rst>` which renders :doc:`as shows here <scripts_template>`. 
For each operator, the content of the doc file is also made available in the Python on-line help (see :ref:`how_to_list_operators`).

Documented operators as of today : 

 - graphics
    - :doc:`scripts/plotmap`
    - :doc:`scripts/timeplot`
    - :doc:`scripts/ncview`

 - simple operations :
    - :doc:`scripts/mean_and_std`

Albeit this is not a proper practice, **some more operators may exist in your CliMAF release** which would not be documented here. Please see :ref:`how_to_list_operators` for such cases

A sorted list of operators :

.. toctree::
  :glob:

  /scripts/*
