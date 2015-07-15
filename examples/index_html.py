"""
Generate an html index of figures using the filenames for figures computed by CliMAF
and stored in CliMAF's cache, including :
  - some paragraph titles formatting 
  - a small table giving access to figure files through html links
"""

from climaf.api import *
from climaf.html import * #html_header, html_section, html_open_table, html_table_line, html_table_lines, html_close_table, html_trailer

# Some global variables for the atlas
simulation='AMIPV6ALB2G'
period="1980"

# First : a function which provides a figure filename based on a few args.
# Here it provides it for a zonal mean of seasonal average for a given simulation,
# variable and period. Computation will occur only for data not already in CliMAF cache

def my_slice(var,exp,period,season) :
    dats=ds(project='example',simulation=exp, variable=var, frequency='monthly', period=period)
    zonal_mean=ccdo(dats,operator="zonmean")
    if season != "ANN" :
        months={ "DJF":"12,1,2" , "MAM" : "3,4,5" , "JJA":"6,7,8", "SON":"9,10,11" }
        dat_season=select(zonal_mean,operator="selmon,"+months[season])
    else:
        dat_season=zonal_mean
    toplot=time_average(dat_season)
    return(cfile(plot(toplot,title=var+" "+exp+" "+period+" "+season)))


# Let us accumulate in a string (index) the content of an html representation
# of a table of links (or thumbnails) to figure files

index=""
index += html_header("CliMAF ATLAS of "+simulation+" for "+period) 
index += html_section("Example of Section level 1 header ",level=1)
index += html_section("Example of Section level 2 header ",level=2)
index += html_section("Example of Section level 3 header ",level=3)
index += html_section("Meridional profiles (level 4)", level=4, key="Slice")

# Define a table of html links . Begin with an optional dict providing labels 
# for column titles (and for links, possibly - see below)

seasons_labels={'Year':'ANN', 'Winter':'DJF', 'Spring': 'MAM','Summer': 'JJA','Fall': 'SON'}
index += html_open_table(title='variable',titles=seasons_labels,spacing=5)

#  Function html_table_line allows to create html lines in a table easily.
#   - First arg is a function to loop on, and which returns the figure
#       filenames. Loop is over columns in the table
#   - Next args are args common to all calls to the function.
#   - But last arg is a dictionnary, on which the loop occurs, which keys are
#       the labels bearing the links, and values are tuples of args also
#       provided to the function;
#   - Last arg is a title (for the first, leftmost column).
#  There will be one html link (and one table column) per label in the dictionary

index += html_table_line(my_slice,'tas',simulation, period, seasons_labels,"tas - surface temperature")

# Function hmtl_table_lines also accepts keyword argument thumbnail, for getting a thumbnail
# rather than a label for the link - See below


# For iterating over lines, let us use html_table_lines
###########################################################

# Define a dictionnary with one entry per table line, giving the line title
vars={
    "rst"  :"rst - short wave at top ",
    "hfls" :"hfls - heat flux .. " ,
    "ta"   : "ta - upper air temp"}

# Function html_table_lines loops calling function html_table_line (without plural)
# over the dictionnary presented as fist arg, passing it dict keys as first arg 
# and dict values as last arg (in line with the call example above)
# Here, additionnaly, we ask for thumbnail images
index += html_table_lines(my_slice,vars,simulation,period,seasons_labels,thumbnail=60) 

# That's all folk. Just close the table, the html document, and write it to file
index += html_close_table()
index += html_trailer()
out="index_example.html"
with open(out,"w") as filout : filout.write(index)

import os,os.path ; os.system("firefox file://"+os.path.abspath(os.path.curdir)+"/"+out+"&")
