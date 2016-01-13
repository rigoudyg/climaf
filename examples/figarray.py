# How to build a an array of figures using cpage()
from climaf.api import *

# Define a dataset with one single time step
cdef("frequency","monthly")
cdef("period","198001")
tas=ds(project="example", simulation="AMIPV6ALB2G", variable="tas")

# Define a figure
fig1=plot(tas,title="title",resolution="1600*2400")

# Trigger computation of fig1 as a cached file
cfile(fig1)

###########################################################################
# Define page1 as a figure array by trimming all the surrounding extra
# space of figures (fig_trim=True by default) and also of the page
# (page_trim=True by default), and control image resolution
page1=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]],
            widths=[0.2,0.8],heights=[0.33,0.33,0.33],
            page_width=800, page_height=1200)
###########################################################################
# ask for display of page1
cshow(page1)

###########################################################################
# Same as page1 by adding a title and tuning some parameters for the title
###########################################################################
page2=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]],
            widths=[0.2,0.8],heights=[0.33,0.33,0.33],title="Page title",
            background="grey90",x=-300,y=26,pt=20,
            font='Utopia',ybox=60)
cshow(page2)
 
###########################################################################
# Same as page1 with a title but without tuning parameters for the title
###########################################################################
page3=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]],
            widths=[0.2,0.8],heights=[0.33,0.33,0.33],title="Page title")
cshow(page3)

###########################################################################
# Define page4 as a figure array without specify widths and heights;
# widths and heights will then be computed in a homogeneous way to fill the
# page, i.e. for this example: widths=[0.5,0.5]; heights=[0.33,0.33,0.33]
page4=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]])
###########################################################################
cshow(page4)

###########################################################################
# Define page5 as a figure array by not trimming all the surrounding extra
# space of the page (page_trim=False) but of figures (fig_trim=True by default) 
page5=cpage([[None, fig1],[fig1, fig1],[fig1,fig1]],
            page_trim=False)
###########################################################################
cshow(page5)

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
# Define page6 as a figure array without specifying widths and heights;
# widths and heights will then be computed in an even way to fill the
# page with one column, i.e. for this example: widths=[1.]; heights=[0.5,0.5]
page6=cpage(fig_ens)
###########################################################################
cshow(page6)

###########################################################################
# Define page7 as a figure array by only specifying heights (in the case of an
# ensemble : widths=[1.] by default) and by not trimming all the surrounding extra
# space of the page (page_trim=False) but of figures (fig_trim=True by default) 
page7=cpage(fig_ens, heights=[0.8,0.2], page_trim=False)
###########################################################################
cshow(page7)
