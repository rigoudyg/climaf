import sys; sys.path.append("/home/stephane/Bureau/climaf")
# How to build a an array of figures using cpage()
from climaf.api import *

# Define a dataset with one single time step
cdef("frequency","monthly")
cdef("period","198001")
tas=ds(project="example", experiment="AMIPV6ALB2G", variable="tas")

# Define a figure
fig1=plot(tas,crs="title")

# Trigger computation of fig1 as a cached file
cfile(fig1)

#########################################################################
# Define page1 as a figure array
page1=cpage(widths_list=[0.2,0.8],heights_list=[0.33,0.33,0.33],
                fig_lines=[[None, fig1],[fig1, fig1],[fig1,fig1]])
#########################################################################

# Clear cache value for page1
cdrop(page1)

# ask for display of page1
cshow(page1)

