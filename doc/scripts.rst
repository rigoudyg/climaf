.. _operators:

-----------------------------------------------------------------
Operators : using external scripts, binaries and python functions
-----------------------------------------------------------------

Principles 
----------

A main driver in CliMAF design is that it allows to define what is
called a 'CliMAF operator' by interfacing with any user-developed
diagnostic, be it an external script, an external binary of a Python
function (hereafter called a 'diagnostic'), and to combine it with other
processing stages. CliMAF provides some services to the diagnostics,
which allows to focus their development on the science.

The present section explains the basics of such an interfacing. The way to use operators is up-to-now described mainly by the :ref:`examples` section

The main principles for a diagnostic are that :

- it may implement either a simple or a complex function ; while simple
  functions are more re-usable, complex ones may be more cost-effective

- the script (or function) calling sequence is registered with CliMAF
  before use, using a dedicated syntax, which allows to map CliMAF
  managed objects to script (or function) arguments (see below)

- all type of diagnostics interface with string-like arguments on the
  command-line (or function call) for providing diagnostic computation
  parameters; this apply to all arguments except main input and
  output datasets

- for main input and output datasets :

   -  Regarding script-type diagnostics

    - they interface with CliMAF using :

     - NetCDF files or OpenDAP dataset URLs (see below) for data input
     - NetCDF files for data output

    - input and output dataset filenames are provided by CliMAF as script
      arguments (at the location required by the script)
    - NetCDF files must be `CF-compliant <http://cfconventions.org/>`_

   -  Regarding Python function-type diagnostics : they interface with CliMAF using
      MaskedArrays (to be confirmed : Masked Variables may apply)

- a diagnostic should not mix computation and graphics, because
    - computing only the graphics usually represents a very small
      computing cost in comparison to the actual data processing 
    - the result of the latter is cached by CliMAF
    - piping both parts (compute and graphics) is easy in CliMAF
    - most graphics can be dealt with using a few generic graphic scripts

Services provided to scripts and functions
------------------------------------------

CliMAF can provide a number of services in data pre-processing,
upstream of the script, which could help in simplifying the script
design : fetching data through OpenDAP, slicing the data in time and
space, aggregating NetCDF files in time, re-mapping data to a regular lat-lon grid

Because CliMAF does manage a cache of such pre-processed data, it should
be cost-effective to let it handle these operations


**Data location**

 On input, CliMAF deals with knowing where the data is, and will provide its path
 or URL; the script doesn't need to care about that, as it receives
 data paths/URLs; scripts declared as non-OpenDAP-capable will
 receives only file paths.

 For script outputs, CliMAF will provide the script with filename(s) in an existing directory, with write permission


**Time slicing / aggregating**

 Scripts may be able, or unable, to read one variable in mutiple files, where each
 file represents only a part of the time period to process; CliMAF
 manages both cases ; it can :

     - either aggregate files in a single file covering exactly the
       time period to work on
     - or it can provide the script with a list of those filenames
       which are sufficient to cover the time period to process, plus
       a specification of the time period as a string argument; this
       case is more cost-effective, for very long datasets which can
       hardly fit in a single file


**Selecting a variable to process**

 Primary datafiles may be multi-variable datafiles; one the other hand
 some scripts may wish to be released with variable selection; to
 accomodate both cases, every script can:

    - either 'declare' to CliMAF that it can select a variable in a
      multi-variable NetCDF file ; this is the most cost-effective 

    - or let CliMAF do the variable selection upstream; in that case,
      the script must be able to identify which is the NetCDF variable
      it should work on (i.e. letting apart coordinate variables)


**Aliasing and re-scaling**

 Some primary datafiles may be inconsistent with expected standards (as
 the CF convention) regarding the name of geophysical variables and/or
 their scaling. Generic services will soon be provided to the scripts
 in order to deal with such cases.


**Chunking over time or space**

 Data chunking is a technique for dealing with very large datasets
 which generates memory size issues : for instance, a space average is
 computed by looping on time periods which are small enough to fit in
 memory. CliMAF does not yet provide automated chunking


Constraints on scripts
----------------------

- each script may use multiple input data streams, and may output
  multiple data streams; but each input filename or URL is used for reading one
  geophysical variable only, each output file contains only one
  geophysical variable

- if the script has to output some scalars, it will use multiple output streams and code the scalars as one
  NectCDF file per scalar

- the script must not return a zero exit code when it is not able to do its job


.. _basic_script_example:

Example for interfacing a diagnostic script with CliMAF
-------------------------------------------------------

-   Declaring operator ``my_cdo`` based on an off-the-shelf
    script/binary (``cdo``)::

     cscript('mycdo','cdo ${operator} ${in} ${out}')

-   Use the defined operator in CliMAF : define a dataset ``tas_ds``
    and apply ``my_cdo`` on it, providing it with value ``tim_avg`` for
    argument ``operator``::

     tas_ds = ds(experiment="AMIPV6”, variable="tas", period=”1980-1981”)
     tas_avg = mycdo(tas_ds,operator='timavg')

-   The script/binary is actually called e.g. when requesting a file with
    the content of object ``tas_avg``, as in::

     filen = cfile(tas_avg)

    which returns the filename :

    */home/my/tmp/climaf_cache/4e/4.nc*

    ..while the actual system call launched behind the curtain by CliMAF would look like ::

     $ cdo tim_avg /home/my/data/AMIP/AMIP_tas.nc /home/my/tmp/climaf_cache/4e/4.nc



.. _script_syntax:

Syntax for interfacing a script
------------------------------- 

A diagnostic script is declared to CliMAF using function **cscript** with
two arguments : 

  - one for the name of the 'diagnostic operator' to define (which is also
    the name of the python function that will be used in CliMAF for
    applying the script), and

  - a second one providing **a script calling sequence pattern    string** , 

such as in:: 

  cscript ( < operator_name > , < calling_sequence_pattern > )

The script calling sequence pattern string should use the following syntax:

-  formal arguments appear as : ``${argument}`` (see example above :
   ``${in}``,  ``${out}``, ``${operator}`` )

-  except for reserved keywords, arguments in the pattern will be
   replaced by the values for corresponding keywords used when invoking
   the diagnostic operator (see the `example`__ above : argument ``operator``
   is replaced by value ``timavg`` - which is a keyword known to
   the external binary called, CDO  )

__ basic_script_example_

-  reserved argument keywords are :

   -  **in, in_<digit>, ins, ins_<digit>** : they will be replaced by
      CliMAF managed filenames for input data, as deduced from dataset 
      description or upstream computation; they can be remote URLs (if the
      script can use OpenDAP, which is declared by a third argument to
      'cscript'), local 'raw' data files, or CliMAF cache filenames

     -  **in** stands for the URL of the first dataset invoked in diagnostic
        operator call

     -  **in_<digit>** stands for the next ones, in the same order

     -  **ins** and **ins_<digit>** stand for the case where the script can
        select input from multiple input files or URLs (e.g. when the
        whole period to process spans over multiple files); in that case,
        a single string (surrounded with double quotes) will carry
        multiple URLs

   -  **var, var_<digit>** : when a script can select a variable in a
      multi-variable input stream, this is declared by adding this
      keyword in the calling sequence; CliMAF will replace it by the
      actual variable name to process; 'var' stands for first input
      stream, 'var_<digit>' for the next ones; in the example above,
      we assume that external binary CDO is not tasked with selecting
      the variable, and that CliMAF must feed CDO with a datafile
      where it has already performed the selection 
      

   - **period, period_<digit>** : when a script can select a time
     period in the content of a file or stream, it should declare it
     by putting this keyword in the pattern, which will be replaced at
     call time by the period written as <date1>-<date2>, where date is
     YYYYMMDDHHMM or shorter depending on the corresponding dataset's
     frequency value; 'period' stands for the first input_stream,
     'period_<n>' for the next ones, in the order of actual call; in
     the example above, this keyword is not used, which means that
     CliMAF has to select the period upstream of feeding CDO with the
     data

   - **out, out_<word>** : CliMAF provide file names for output files. Main
     output file must be created by the script with the name provided
     at the location or argument ${out}; using arguments like
     'out_<word>' tells CliMAF that the script provide some secondary
     output, which will be symbolically known in CliMAF syntax as an
     attribute of the main object; in the example above, we just
     apply the convention used by CDO, which expects that you provide
     an output filename as last argument on the command line

   - **crs** : will be replaced by the CliMAF Reference Syntax expression
     describing the first input stream; can be useful for plot title
     or legend



-  for scripts able to aggregate multiple input data files, each
   argument providing an input data URL must be interpreted by the
   script as a string which can actually provide a list of filenames or
   URLs

-  (TBC) every NetCDF meta-data in input data must be reproduced in
   output data, except those which becomes irrelevant

More script interfacing examples  
-------------------------------------------------

While a basic script interfacing example show in
:ref:`basic_script_example`, module :download:`standard_operators.py <../climaf/standard_operators.py>` includes the actual, commented declarations of all standard operators defined in current CLiMAF version.


Syntax for interfacing a Python function
-----------------------------------------

TBD

Documenting an operator
-------------------------

Please follow :doc:`e.g. the documentation template <scripts_template>`
