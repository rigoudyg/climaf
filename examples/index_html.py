"""
Generate an html index of figures using the filenames for figures computed by CliMAF
and stored in CliMAF's cache, including :
  - some paragraph titles formatting 
  - a small table giving access to figure files through html links
"""
from climaf.api import *
from climaf.html import * 

# Some global variables for the atlas
exp='AMIPV6ALB2G'
period="1980"

# First : a function which provides a figure filename based on a few args.
def my_slice(var,season) :
    dats=ds(project='example',simulation=exp, variable=var, frequency='monthly', period=period)
    zonal_mean=ccdo(dats,operator="zonmean")
    # Force storing the zonal mean for optimization purpose
    if season != "ANN" :
        months={ "DJF":"12,1,2" , "MAM" : "3,4,5" , "JJA":"6,7,8", "SON":"9,10,11" }
        dat_season=select(zonal_mean,operator="selmon,"+months[season])
    else:
        dat_season=zonal_mean
    toplot=time_average(dat_season)
    return(cfile(plot(toplot,title=var+" "+exp+" "+period+" "+season)))

index=""
index += html_header("CliMAF ATLAS of "+exp+" for "+period) 
index += html_section("Example of Section level 3 header ",level=3)
index += html_section("Meridional profiles (level 4)", level=4, key="Slice")

# Define a table of html links ; use html_table_line() with your
# fucntion (here my_slice) and a dict which has columns titles
# as keys and values=args to the function 
#seasons_labels={'Year':'ANN', 'Winter':'DJF', 'Spring': 'MAM','Summer': 'JJA','Fall': 'SON'}
seasons_labels= {'Year':'ANN', 'Winter':'DJF',                 'Summer': 'JJA'              }
index += html_open_table(title='variable',titles=seasons_labels,spacing=5)
index += html_table_line(my_slice,'tas', seasons_labels,"tas - surface temperature")

# For iterating over lines, use html_table_lines, which loops on another,
# with one entry per table line, giving the line title 
lvars={
    "rst"  :"rst - short wave at top ",
    "ta"   : "ta - upper air temp"}
index += html_table_lines(my_slice,lvars,seasons_labels,thumbnail=60) 

# That's all folk. Just close the table, the html document, and write it to file
index += html_close_table()
index += html_trailer()
out="index_example.html"
with open(out,"w") as filout : filout.write(index)

import os,os.path ; os.system("firefox file://"+os.path.abspath(os.path.curdir)+"/"+out+"&")
