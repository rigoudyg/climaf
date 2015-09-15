"""
Generate an html index of figures using the filenames for figures computed by CliMAF
and stored in CliMAF's cache, including :
  - some paragraph titles formatting 
  - a small table giving access to figure files through html links
"""
from climaf.api import *
from climaf.html import header,trailer,section,\
    open_table,close_table,fline,flines,link,vspace,line

# Some global variables 
exp='AMIPV6ALB2G'
period="1980"

index=""
index += header("CliMAF ATLAS of "+exp+" for "+period) 
index += section("Example of Section level 3 header ",level=3)
index += section("Meridional profiles (level 4)", level=4, key="Slice")

# Basics
##########
# Create a line of links to figures, providing labels and figures filenames
index+=line({"lab1":"fig1.ps", "lab2":"fig2.ps"},title="the title   ")

# A function which provides a figure filename based on two args .
def my_slice(var,season) :
    from climaf.operators import ccdo,time_average, plot, select
    dats=ds(project='example',simulation=exp, variable=var, \
	frequency='monthly', period=period)
    zonal_mean=ccdo(dats,operator="zonmean")
    # Force storing the zonal mean for optimization purpose
    if season != "ANN" :
        months={ "DJF":"12,1,2" , "MAM" : "3,4,5" , "JJA":"6,7,8", \
	    "SON":"9,10,11" }
        dat_season=select(zonal_mean,operator="selmon,"+months[season])
    else:
        dat_season=zonal_mean
    toplot=time_average(dat_season)
    return(cfile(plot(toplot,title=var+" "+exp+" "+period+" "+season)))

# Create a link to a figure returned by function 'my_slice'
index += link("A simple link ", my_slice('tas','ANN'))

# Advanced : create lines or tables of links, through automated iteration of a function call
#########################################################################################

index+=vspace(3)
# Define a line (i.e. a series of columns) of html links ; use
# climaf.html.fline() with args: 
#  - the function (here 'my_slice') called for each column  
#  - a common value for first arg to my_slice, 
#  - and a list of values for second arg (one for each column)
index += open_table()
index += fline(my_slice,'tas',['ANN', 'DJF','JJA'], title="Surface temperature")
index += close_table()

index+=vspace(3)
# For creating a table , with a line showing column titles, and iterating 
# over lines changing values of first arg to the function, use function
# 'flines', which loops on a list of second args, or a dict with
# similar keys and which values are line titles

seasons= {'Year':'ANN', 'Winter':'DJF'}
index += open_table(title='variable/season', columns=seasons.keys(), spacing=5)
lvars={
    "rst"  : "short wave at top ",
    "ta"   : " upper air temp"}
index += flines(my_slice,lvars,seasons.values(),thumbnail=60) 

index += close_table()
index += trailer()
out="index_example.html"
with open(out,"w") as filout : filout.write(index)

import os,os.path ; os.system("firefox file://"+os.path.abspath(os.path.curdir)+"/"+out+"&")
