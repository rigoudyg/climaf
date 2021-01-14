#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals, absolute_import


from __future__ import print_function

__doc__ = """
Example for decalring to CliMAF a script which has tywo outputs 

We use a data sample distributed with CliMAF

"""

# S.Senesi - nov 2018

# Load Climaf functions

from climaf.api import *

# Access example data (which are pre-defined in CliMAF)
rst = ds(project="example", simulation="AMIPV6ALB2G", variable="rst", period="1980")

# Assume that we have a shell script 'my_2_outputs_script.sh' with that (crazy) content
# !/bin/bash
# entree=$1
# sortie=$2
# autre_sortie=$3
# cp $entree $sortie
# cp $entree $autre_sortie

# Declare this script :
cscript('myscript', cpath + '/../examples/my_2_outputs_script.sh ${in} ${out} ${out_secondary}')

# EXPLANATIONS :
#  - HERE, we use 'cpath' for saying 'CliMAF python source dir'
#  - we tell CliMAF that the script assumes he will receive 3 args which are filenames :
#         * 1st filename stands for the input file provided to the script. It will match
#           with the first object provided when calling my_script
#         * 2nd filename stands for the file where the script should write its main output;
#           It matches the CliMAF object which is returned when calling my_script :

object_for_main_output = myscript(rst)

#         * 3rd filename stands for the file where the script should write the 'other' output;
#           It can be accessed under CliMAF as a 'field' of the main output object, which field
#           name is 'secondary' :

other_output = object_for_main_output.secondary

# Let us have a look at the Climaf definition of this object :
print(other_output)
# >>> myscript(ds('example|AMIPV6ALB2G|rst|1980|global|monthly')).secondary

# Let the operations be actually done
print(cfile(other_output))
# >>> /home/senesi/tmp/climaf_cache/e2eb2/1047e/3c007/0633e/056b0/96f66/634c1/c90b0/0f0e8/bdd84/71a31/1.nc

# Check that, for CliMAF, this is actually a different content than 'object_for_main_output'
print(cfile(object_for_main_output))
# >>> /home/senesi/tmp/climaf_cache/700ea/6519a/d069c/5b5db/a75e5/1eaa7/a6f59/3df7f/73e80/d309a/64216/d.nc
