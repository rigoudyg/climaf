# Using macros in CliMAF  - S.Senesi - 04/2015

# The basic idea is that, once you are happy with a suite of
# operations that lead to a nice result (be it a figure or a data
# object), you can very easily define a macro from it, using
# 'cmacro()'; the macros can be saved and edited, and they simplify
# the display of CliMAF cache content

from climaf.api import *

# First use and combine CliMAF operators to get some interesting
# result using some dataset(s)
january_ta=ds(project='example',simulation="AMIPV6ALB2G", variable="ta",
              frequency='monthly', period="198001")
ta_europe=llbox(january_ta,latmin=40,latmax=60,lonmin=-15,lonmax=25)
ta_ezm=ccdo(ta_europe,operator="zonmean")

# Using this result as an example, define a macro named "eu_zonal_mean",
# which arguments will be the datasets involved in this result
macro("eu_zonal_mean",ta_ezm)

# Also design a figure and define the corresponding macro
fig_ezm=plot(ta_ezm)
macro("eu_cross_section",fig_ezm)

# You can of course use a macro on other dataset(s), 
pr=ds(project='example',simulation="AMIPV6ALB2G", variable="pr",
              frequency='monthly', period="198001")
pr_ezm=eu_zonal_mean(pr)

# You can also define a macro 'from scratch', using ARG for dataset arguments/parameters
macro("my_macro", "ccdo(ARG,operator='timavg')")

# All macros are registered in dictionnary climaf.cmacros.cmacros,
# which is imported by climaf.api :
cmacros

# You can also look at how the macros do use macros (esp. eu_cross_section)
climaf.cmacro.show()

# How to remove a macro
cmacros.pop("my_macro")

# Save the macros in some location (provide a filename)
# Default is ~/.climaf.macros, and is used for
#   - automatically saving macros at end of CliMAF sessions
#   - automatically reading macros at start of CliMAF sessions
climaf.cmacro.write()

# Look at the external representation of the macros. 
print "\nContent of ~/.climaf.macros :"
import os ; os.system("cat ~/.climaf.macros")

# Using that example, you can also write macros to and load macros from 
# any file, using the macro syntax (here, we use the default location) 
climaf.cmacro.read("~/.climaf.macros")

# Trigger the computation of some results, in order to populate the cache 
cfile(fig_ezm)

# The cache is displayed using macros
print "\nCache content (using macros) :"
cdump()




