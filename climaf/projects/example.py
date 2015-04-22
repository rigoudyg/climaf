"""
This module declaresDeclare project example and its data location for standard CliMAF package

Only one additionnal attribute : frequency (but data sample actually includes only frequency= 'mon'

Example of an 'example' dataset definition ::

 >>> dg=ds(project='example', experiment='AMIPV6ALB2G', variable='tas', period='1980-1981', frequency='mon')


"""

import os

from climaf import __path__ as cpath
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
cpath=os.path.abspath(cpath[0]) 

cproject("example" , "frequency" )

data_pattern_L=cpath+"/../examples/data/${experiment}/L/${experiment}SFXYYYY.nc"
data_pattern_A=cpath+"/../examples/data/${experiment}/A/${experiment}PLYYYY.nc"
dataloc(project="example",organization="generic",url=[data_pattern_A,data_pattern_L])
