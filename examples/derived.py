""" CliMAF - example for derived variables

A derived variable is a new geophysical variable defined by explaining
how to compute it using a script and some other geophysical variable(s)

It can be used to define a CliMAF dataset

"""

# S.Senesi - sept 2014

from climaf.api import *
# Tell CliMAF how verbose it should be (levels : CRITICAL, ERROR, WARNING, INFO, DEBUG)
clog(logging.INFO) # default is WARNING

# Define data location and organization for an experiment, as concisely as possible
dataloc(experiment="AMIPV6ALB2G", organization="example", url=[cpath+"/../examples/data/AMIPV6ALB2G"])

# Set some default values
cdef("experiment","AMIPV6ALB2G")
cdef("period","1980-1981")

# Declare a script tht will be used in defining how to derive the new variable
cscript('minus','cdo sub ${in_1} ${in_2} ${out}')

# Define some dataset with a new, virtual, variable (also called
# 'derived') . We call it 'crest' (which stand for Cloud Radiative
# Effect in Shortwave at Top of atmosphere), from all-sky and
# clear-sky sortwave fluxes
creShortTop=ds(variable="crest")

# Say how you compute (or derive) 
derive('crest','minus','rst','rstcs')

# Ask for actually compute the variable as a file
my_file=cfile(creShortTop)
print my_file

if (my_file is None) : exit(1)