.. _howto:

--------
HowTo...
--------

..go quick through most CliMAF features 
------------------------------------------

Read the :download:`Grand Tour <../examples/ATourOfCliMAF.html>`

..install CliMAF
-----------------------

See :doc:`installing`


..run CliMAF, run an example
-------------------------------

See :ref:`examples`

.. _my_data:

..describe where my data is
---------------------------

If your data is organized after one of the specific organization scheme known
to CliMAF (i.e. for now ``CMPI5_DRS`` or ``EM``) , you just have to tell CliMAF about the root directories for your data. This could be as simple as::

  >>> dataloc(project="GEOMIP", organization="CMIP5_DRS", url=['/tmp/data','~/data/CMIP5'])

If this is not the case, you will most probably be happy with the 'generic' type of organization, which allows to describe the file hierarchy for your data using templates with keyowrds, such as in::

  >>> dataloc(project="MY_PROJECT", organization="generic", url=["/home/stephane/data/MY_PROJECT/${model}/${variable}_1m_YYYYMM_YYYYMM_${model}.nc"]

See examples in the section on data access at :ref:`examples` ; see function :py:class:`~climaf.dataloc.dataloc` for reference.


.. _how_to_online_help:

..get on-line help 
-------------------

From the Python shell, all relevant CliMAF functions and variables are auto-documented using Python features. Hence, you can :

- list these functions and variables by::

  >>> dir(climaf.api)

- get the general help on functions::

  >>> help(climaf.api)

- get help on a given function (say ``cscript``) by::

  >>> help(cscript)

- get help on a CliMAF operator (say ``regrid``) by::

  >>> help(regrid)


.. _how_to_list_operators:

..know which CliMAF operators are available and what they do
------------------------------------------------------------

While the set of basic CliMAF operators should be quite stable at some stage, it may evolve significantly in the initial development stage; and it actually varies among CliMAF versions; it can also be extended with your own operators (see :ref:`how_to_own_script`). 

Thus, in addition to the operators described in section :ref:`standard_operators` of the current version of the documentation, you can also look at the Python dictionary which serves as an index to the actual list of operators for your version; just type:: 

  >>> cscripts 

You may then ask for on-line help for any of the scripts , as e.g. :: 

  >>> help(plotmap)


You may know how the operator interfaces with Climaf by ::

 >>> cscripts['plotmap'].command


..tune CliMAF verbosity level
------------------------------

CliMAF uses the Python logging package :py:mod:`logging` for informing
about work done, at varied verbosity levels. There are two logging
streams : one going to screen (or stderr), the other going to file
``climaf.log`` . See function :py:func:`~climaf.clogging.clog` for
setting the severity level for the former and function
:py:func:`~climaf.clogging.clog_file` for the latter 

Note : at CliMAF startup, the severity level is set to the value of environment
variable $CLIMAF_LOG (resp. $CLIMAF_FILE_LOG)



.. _how_to_report_an_issue:

..report an issue
------------------

For the time being, you may report an issue on `the CliMAF issue page on GitHub <https://github.com/senesis/climaf/issues>`_ . Just click on the green button "New issue" (you may have to create a login on GitHub for that )


.. _how_to_own_script:

..declare my favorite script or binary as a CliMAF operator for my own use
--------------------------------------------------------------------------

Using any script in CliMAF is very easy, and you can do so for your own use only. The basics of creating a new CliMAF operator based on a script or binary are explained at :ref:`operators`. A **simple example** shows at :ref:`basic_script_example`. The detailed syntax is explained at :ref:`script_syntax`..The script can be located anywhere on the filesystem (you can quote an absolute path in the calling sequence pattern when declaring it ); at first, your script should echo each executed command, for debugging purpose;  and you may have a look at his output in file ``./scripts.out`` (in the working directory)

.. _how_to_contribute_a_script:

..contribute a diagnostic module
---------------------------------------------------

If you are willing to share as an `Open Source sofwtare <http://en.wikipedia.org/wiki/Open-source_software>`_ any diagnostic tool that can be integrated in CliMAF as a so-called 'CliMAF standard operator', you should first go through :ref:`how_to_own_script` for the basics of integrating it, and for testing the integration. At that stage, the actual binary or script will not be hosted in CliMAF installation directory. The next steps will be to :

#. think about a name for the corresponding CliMAF standard operator : it should not collide with existing operators (see :doc:`operators`), and should be both short and explicit; let us call it ``my_op`` for now; if the diagnostic module has more than one (main) output, also think twice about the names for the secondary outputs (`details here <script_syntax>`_) as they will also join the 'CliMAF Reference Syntax' 
#. if you are working with a version of CliMAF that has been installed by somebody else, you should now install your own; see :doc:`installing`
#. if your module is a script, add its code in directory ``<climaf_install_dir>/climaf/scripts``; the script filename is up to you, but should more or less ressemble or recall the name of the CliMAF operator choosen above
#. if your module is a binary which needs some compilation, prepare a makefile for that, which ideally should be tested both with Intel and Gnu compilers (... TBD : think deeper on a tractable way to integrate binaries...)
#. check twice the Climaf function call that will allow to declare the operator in CliMAF, and adapt it to the new script location, as e.g. ::

    >>> cscript ("my_op", cpath+"/scripts/"+"<calling sequence pattern>") 

   and edit file ``<climaf_install_dir>/climaf/standard_operators.py`` to add this call
#. restart a CliMAF session and check that your test script for this module (where the ``cscript`` declaration of the module should now be discarded)  still works after these changes
#. prepare a text providing a description of the diagnostic; this text
   is intended to become part of CliMAF standard documentation; it
   should preferably be in `REStructured Text format
   <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_,
   and follow  :download:`this template <scripts_template.rst>` which
   will render :doc:`e.g. as shows here <scripts_template>` , or for a
   real example  :doc:`like this <scripts/plotmap>` , but this is not
   a firm pre-requisite. Save this text as
   ``<climaf_install_dir>/doc/operators/my_op.rst``. The text may
   describe your diagnostic at length, and should provide all
   necessary bibliographic references for a sound sharing. It will
   automatically be included in the CliMAF operator Python on-line
   help (available as ``help(my_op)``). It will be accessible from CliMAF
   doc if you add a reference in file ``doc/std_operators.rst``
#. submit your changes as described at :ref:`contributing_changes`

.. _how_to_improve_doc:

..contribute to improve CliMAF documentation
--------------------------------------------
CliMAF documentation is built using `Sphinx <http://sphinx-doc.org/>`_ and can easily be modified and improved, provided you are not afraid by looking at text files formated using the `REStructured Text syntax <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ (and Sphinx is installed on your computer, which is often the case; check with ``which sphinx-build``). All doc files stand in directory ``<climaf_install_dir>/doc``, with quite easy-to-understand filenames. You can modify any file and test the result by typing::

  $ cd <climaf_install_dir>/doc
  $ make -h html

and loading the resulting file ``<climaf_install_dir>/doc/_build/html/index.html`` in your browser.

Note : part of the doc (e.g. section :ref:`api` ) is built from the Python docstrings (strings
at the beginning of classes, modules, functions, .....). 

- This needs a Python module either ``sphinx.ext.napoleon`` or
  ``sphinxcontrib.napoleon``. If the doc build fails complaining about
  one of this package, you can just comment it out in file doc/conf.py.

- When wanting to improve the doc for one of the Python functions or
  classes: the full python object path let you know where to find the
  corresponding file and docstring, in directory
  <climaf_install_dir>/climaf

Once happy with the result, please contribute your work for a merge in next CliMAF release as described at :ref:`contributing_changes`


..define a new data organization scheme
---------------------------------------

Please see the 'generic' data organization in :ref:`my_data` . if this
does not fit, please email to ``climaf at meteo dot fr``



