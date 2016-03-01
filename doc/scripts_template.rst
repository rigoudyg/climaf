:orphan:

*Notes* :

 - *This is a template for describing a CliMAF operator. Depending on your reading context, one of these links may work for downloading it*: :download:`scripts_template.rst <scripts_template.rst>` *or* http://climaf.readthedocs.org/en/latest/_downloads/scripts_template.rst 
 - *The syntax is* `ReST <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_:

  - *Underlining, tabs, '::' and double multiply signs are ReST construct that you should keep for a nice rendering*
  - *The first two lines give a title, which must be the CliMAF operator name, and a summary sentence*
  - *The Rest 'single' emphasis, namely text between single multiply signs (or showing in italics) is used here for the comments indicating how to use the template*

 - *Please read the CliMAF doc section dealing with operators for context information. This link may work :* :ref:`operators`


my_new_climaf_operator : what it does
-------------------------------------------------------

*You should here describe in one or two phrases what the new operator computes*


**References** : *any bibliographic reference or link to technical
documents*

**Provider / contact** : *one or two mail adresses, for acknowledgment
and/or for support - In order to limit spamming, use e.g. : myself at
mylab dot fr. You may use : climaf at meteo dot fr , if you do not
want to be involved in support, nor feedback*

**Inputs** (in the order of CliMAF call):
  - *describe here if the first (main) input dataset can be any
    geophysical variable case of a generic operator) or must be some
    specific variable*
  - *do the same for next inputs, if the operator do use multiple
    input datasets*

**Mandatory arguments**: 
  - ``argument1`` : *describe the semantics of <argument1>, if any*
  - *do the same for all arguments*

**Optional arguments**
    - ...

**Outputs** :
  - main output : *describe the content of main output, with further
    details than in the general description of the operator*
  - secondary outputs and their names *(if any*) :
     -  ``sec_out_nam`` : *describe the content of <sec_out_nam>*

*provide a typical example of calling this operator using CliMAF*

**Climaf call example** ::
 
  >>> ds= ....some dataset
  >>> m = my_new_climaf_operator(ds, argument1='abcd')  
  >>> secondary_ouput = m.sec_out_nam  

**Side effects** : *describe side effects if any (e.g. showing a
figure, creating temporary files); Note : side effects do not match
CliMAF's spirit*

**Implementation** : *you may provide some details on how the operator
is implemented : as a script, a binary, using such and such tools or
libraries ... This is useful for somebody considering to embark on
improving the operator*

**CliMAF call sequence pattern** (for reference) : *copy here the second
argument of the call to CliMAF function cscript which declares the 
operator to CliMAF, and which will drive the match between 
the arguments in CliMAF call and the arguments provided to the
script/binary*

