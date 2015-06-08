# Example of ensemble definition and handling in CliMAF
# S.Senesi - 05/2015

from climaf.api import *

# Basic example : superimpose zonal profiles of tas for various periods of same experiment
############################################################################################

# Define some objects. here, they are datasets for the same experiment but distinct periods
j0=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
j1=ds(project='example',experiment="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")

# Create an ensemble out of various objects. The list of labels must stand first
e2=cens(['1980','1981'],j0,j1)

# You can operate on ensemble with operators that are not ensemble-capable
# Then, CliMAF will simply loop operators on members, and forward the label list
# Here, let us compute global average on the ensemble
tas_ga=space_average(e2)

# Ensemble-capable scripts are those which declares their main input using keyord ${mmin}
# They receive the labels if they were declared with keyword ${labels}
# 'lines' is such a script, devoted to plot xy curves
p=lines(tas_ga,title="Surface Temperature global average")
cshow(p)


# Advanced example : create panel plot of various members, add a member, and compute anomalies
###############################################################################################

# Define some default values for using CMIP5 data for various realizations
cdef("frequency","monthly") ;  cdef("project","CMIP5");
cdef("model","CNRM-CM5") ; cdef("variable","tas"); 

# Create an ensemble of datasets , more easily, with 'eds'; labels are automatic
ens=eds(experiment="historical", period="1860", rip=["r1i1p1","r2i1p1"])

# The member labels are added to the 'title' value when looping a
# non-ensemble-capable script on ensemble members :
multiplot=plot(ens, title='tas')

# Display all plots separately
cshow(multiplot)

# Assemble all plots in a page and display it
page=cpage([1],[0.5,0.5],multiplot)
cshow(page)

# Add a member to an ensemble
member=ds(experiment="historical", period="1860", rip="r3i1p1")
ens.members.append(member)
ens.labels.append("r3i1p1")

# Compute ensemble mean thanks to CDO
cscript("ensavg","cdo ensavg ${mmin} ${out}")
average=ensavg(ens)

# A standard operator :
#cscript("minus","cdo sub ${in_1} ${in_2} ${out}")

# Compute anomalies wrt to ensemble mean
anomalies=minus(ens,average)
cshow(cpage([0.5,0.5],[0.5,0.5],plot(anomalies,title='tas')))
