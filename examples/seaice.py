"""
Example of CliMAF session with SeaIce data (here organized 'a la EM')

"""
# S.Senesi - may 2015

from climaf.api import *

import os
if not atCNRM or (os.getenv("USER") != "senesi" and os.getenv("USER") != "salas") :
    print "This example does work only at CNRM for some users"
    exit(0)

# Next declaration is actually built-in
dataloc(project="EM", organization="EM", url=["dummy"])

# Next declaration is now built-in in CliMAF (and also for a number of non-ambiguous variables)
calias('EM','sic', missing=1.e+20)

# Define default value for some dataset facets
cdef("frequency","monthly") ;  
cdef("project","EM")

# Define your dataset (a number of facets take default values)
sic=ds(experiment="NG89", variable="sic", period="198310", realm="I")

# Display the basic filenames involved in the dataset (all filenames in one single string)
# CliMAF will search them at the data location which is the most specific among all declared data locations 
files=sic.baseFiles()
print files

# Let CliMAF generate a file with the exact dataset in its disk cache (this
# select period and/or variables, aggregate files...) 
my_file=cfile(sic)
print my_file

# Check file size and content
import os
os.system("ls -al "+my_file)
os.system("type ncdump && ncdump -h "+my_file)

# Stereopolar plot with explicit levels. See othe rplot arguments in on-line help
# as e.g. help(plot)
fig1=plot(sic,crs="Sic 198310 2",proj="NH70",levels="0.1 10 30 60 80 90 95 97 98 99")
cshow(fig1)

# Remap Sea Ice data to atmospheric grid. Use default option (remapbil)
tas=ds(project="EM", experiment="GSAGNS1", variable="tas", period="1975", realm="L")
sic_on_tas_grid=regrid(sic,tas)
fig2=plot(sic_on_tas_grid,crs="regridded_sic")
cshow(fig2)


# Access to daily data
sicd=ds(experiment="NG89", variable="sic", period="198303", realm="I", frequency='daily')
print sicd.baseFiles()


exit(0)
