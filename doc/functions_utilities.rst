-----------------------------------------
Utility functions and variables
-----------------------------------------

.. default-domain:: python


scripts_output_write_mode : should we accumulate scripts output
------------------------------------------------------------------

.. autodata:: climaf.driver.scripts_output_write_mode

Value 'a' allows to accumulate scripts outputs in file last.out.
Default value is 'w' and allows to keep only the output of last script.


cerr : display the output of last operator call 
--------------------------------------------------

.. autodata:: climaf.api.cerr

cpath : path for CliMAF installation directory
-----------------------------------------------

.. autodata:: climaf.api.cpath

clog : tune verbosity
-----------------------

.. autofunction:: env.clogging.clog 

clog_file  : tune verbosity for log file
-------------------------------------------

.. autofunction:: env.clogging.clog_file 

csync
---------------------

.. autofunction:: climaf.cache.csync


