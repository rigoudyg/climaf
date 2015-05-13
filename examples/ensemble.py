# Example of ensemble definition and handling in CliMAF
# S.Senesi - 05/2015

from climaf.api import *

# Define some objects. here, they are datasets for the same experiment but distinct periods
j0=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
j1=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")

################################################################
# Create an ensemble out of it. The list of labels must be first
e2=cens(['1980','1981'],j0,j1)
################################################################

# You can operate on ensemble with operators that are not ensemble-capable
# CliMAF will simply loop operators on members, and forward the label list
m=ccdo(e2,operator='zonmean')
mg=ccdo(m,operator='mermean')
mgt=time_average(mg)
cfile(mgt)

# Ensemble-capable scripts are thos who decalres their main input using keyord ${mmin}
# They receive the labels if they declare keyword ${labels}
cscript('plotm','/cnrm/aster/data3/aster/senesi/dev/climaf/scripts/mult.sh ${labels} ${mmin}')
p=plotm(mgt)


# Define some default values for dataset attributes 
cdef("frequency","monthly") ;  cdef("project","CMIP5"); cdef("model","CNRM-CM5")
cdef("variable","tas"); cdef("period","1860")

################################################################
# Create an ensemble of datasets , more easily, with 'eds'
################################################################
ens=eds(experiment="historical", rip=["r1i1p1","r2i1p1"])

# It can be used in the same way as an output of fucntion cens()

