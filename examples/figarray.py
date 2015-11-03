# How to build a an array of figures using cpage()
from climaf.api import *

# Define a dataset with one single time step
cdef("frequency","monthly")
cdef("period","198001")
tas=ds(project="example", simulation="AMIPV6ALB2G", variable="tas")

# Define a figure
fig1=plot(tas,title="title")

# Trigger computation of fig1 as a cached file
cfile(fig1)

###########################################################################
# Define page1 as a figure array by trimming all the surrounding extra
# space of figures (fig_trim=True by default) and also of the page
# (page_trim=True by default)
page1=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]],
            widths=[0.2,0.8],heights=[0.33,0.33,0.33])
###########################################################################
# ask for display of page1
cshow(page1)

###########################################################################
# Define page2 as a figure array without specify widths and heights;
# widths and heights will then be computed in a homogeneous way to fill the
# page, i.e. for this example: widths=[0.5,0.5]; heights=[0.33,0.33,0.33]
page2=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]])
###########################################################################
cshow(page2)

###########################################################################
# Define page3 as a figure array by not trimming all the surrounding extra
# space of the page (page_trim=False) but of figures (fig_trim=True by default) 
page3=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]],
            page_trim=False)
###########################################################################
cshow(page3)

###########################################################################
# Define an ensemble with one single month of data per member
tas81=ds(project="example", simulation="AMIPV6ALB2G", variable="tas",period="198101",frequency="monthly")
ens=cens(['1980','1981'],tas,tas81)

# Define an ensemble of figures
fig_ens=plot(ens,title="title")

# Trigger computation of fig_ens as a cached file
#cfile(fig_ens)
cshow(fig_ens) # will launch cshow once per member

###########################################################################
# Define page4 as a figure array without specifying widths and heights;
# widths and heights will then be computed in an even way to fill the
# page with one column, i.e. for this example: widths=[1.]; heights=[0.5,0.5]
page4=cpage(fig_ens)
###########################################################################
cshow(page4)

###########################################################################
# Define page5 as a figure array by only specifying heights (in the case of an
# ensemble : widths=[1.] by default) and by not trimming all the surrounding extra
# space of the page (page_trim=False) but of figures (fig_trim=True by default) 
page5=cpage(fig_ens, heights=[0.8,0.2], page_trim=False)
###########################################################################
cshow(page5)
