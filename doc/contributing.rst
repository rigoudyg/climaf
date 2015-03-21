.. _contributing_changes:

------------------------------------------------
Contributing changes for integration in CliMAF
------------------------------------------------

This section is still a draft :

- When contributing to the documentation or for a standrad operator (by providing a script), please prepare your changes according to :ref:`how_to_contribute_a_script` and :ref:`how_to_improve_doc`

- When writing Python code for CliMAF core, docstrings should stick to `Google-style docstring coding standard <http://sphinx-doc.org/ext/example_google.html#example-google>`_ ; you may also consider  `other Google-style coding standards <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_

- You may propose your changes to climaf@meteo.fr :

  - By providing a tar file of a modified climaf installation directory. You may include unchanged files in the tar file, but please discard useless new files. You may wish to exclude the (quite big) data samples and other useless material using exclude patterns in the tar command, as in::

      tar cf climaf.tar --exclude=AMIPV6*nc --exclude=tas*nc --exclude=.git --exclude=_build climaf

  - If you use the git source code versioning system :
     - If you have access to CNRM's Lustre and have your CliMAF git repository there : by comitting your changes to this repository and sending the repository location and the commit number  
     - If you can consider using GitHub : by creating your own CliMAF repository there and ... (please wait, must check something...)
