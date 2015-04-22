"""

This module declares project EM , which data organization is built-in

EM (Experiment Manager) is a tool used at CNRM for moving exeperiments post-processed data
from the HPSS to the local filesystem, and to organize it in a file hierarchy governed by a few
configuration files

Experiment names are assumed to be unique in the namespace defined by the user's configuration
file, which may include shared experiments

Example for defining an EM dataset::

 >>> tas=ds(project='EM', experiment='GSAGNS1', variable='tas', period='1975', frequency='monthly', realm='L')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias

cproject('EM' , 'frequency', 'realm' )
dataloc(project='EM', organization='EM', url=['dummy'])

