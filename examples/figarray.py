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
# Define page1 as a figure array
page1=cpage(widths=[0.2,0.8],heights=[0.33,0.33,0.33],
                fig_lines=[[None, fig1],[fig1, fig1],[fig1,fig1]])
###########################################################################

# Clear cache value for page1
cdrop(page1)

# ask for display of page1
cshow(page1)

###########################################################################
# Define page2 as a figure array without specify widths and heights;
# widths and heights will then be computed in a homogeneous way to fill the
# page, i.e. for this example: widths=[0.5,0.5]; heights=[0.33,0.33,0.33]
page2=cpage(fig_lines=[[None, fig1],[fig1, fig1],[fig1,fig1]])
###########################################################################

cdrop(page2)
cshow(page2)

###########################################################################
# Define page3 as a figure array by trimming all the surrounding extra
# space of figures (fig_trim="on") and also of the page (page_trim="on") 
page3=cpage(fig_lines=[[None, fig1],[fig1, fig1],[fig1,fig1]],
            fig_trim="on",page_trim="on")
###########################################################################

cdrop(page3)
cshow(page3)

###########################################################################
# Define an ensemble with one single time step per member
tas81=ds(project="example", simulation="AMIPV6ALB2G", variable="tas",period="198101",frequency="monthly")
ens=cens(['1980','1981'],tas,tas81)

# Define an ensemble of figures
fig_ens=plot(ens,title="title")

# Trigger computation of fig_ens as a cached file
cfile(fig_ens)
cshow(fig_ens) # will launch cshow once per member

###########################################################################
# Define page4 as a figure array without specify widths and heights;
# widths and heights will then be computed in a homogeneous way to fill the
# page, i.e. for this example: widths=[1.]; heights=[0.5,0.5]
page4=cpage(fig_lines=fig_ens)
###########################################################################

cdrop(page4)
cshow(page4)

###########################################################################
# Define page5 as a figure array by only specifying heights (in the case of
# an ensemble : widths=[1.] by default) and by trimming all the surrounding
# extra space of figures (fig_trim="on") and also of the page (page_trim="on") 
page5=cpage(fig_lines=fig_ens, heights=[0.8,0.2],fig_trim="on", page_trim='on')
###########################################################################

cdrop(page5)
cshow(page5)
