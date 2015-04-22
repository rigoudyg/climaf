from climaf.api import *

# Define a dataset, using a built-in pre-defined datafile location
##################################################################
cdef("project","example")
cdef("frequency","monthly")
dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980-1981")
cfile(dg)

# Compute its basic climatology using an external script
#########################################################
cscript('time_average' ,cpath+'/../scripts/mcdo.sh timavg ${out} ${var} ${period_iso} ${domain} "" ${ins}' )
ta=time_average(dg)

# A simple plotting using standard operator ncview
##################################################
# For reference, here is the declaration of oeprator 'ncview' :
# cscript('ncview' ,'ncview ${in}' , format=None)

ncview(ta)

# A more sophisticated plot, using standard operator plotmap
############################################################
# For reference, here is the declaration of plotmap :
# cscript('plotmap',"ncl "+ cpath +"/../scripts/plotmap.ncl infile=${in} plotname=${out} cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} var=${var} title=${crs} scale=${scale} offset=${offset} units=${units}",format="png")

map=plotmap(ta,color="BlueDarkRed18", min=260, max=300, delta=4)

# Ensure figure is computed, and get its cache filename in CliMAF disk cache
figfile=cfile(map)

# Displaying a figure object will compute and cache it if not already done
cshow(map)

# A more comprehensive way of configuring plots
###################################################
def map_graph_attributes(var) :
    """ 
    Return a dictionnary with graphic attributes :
    - relevant to the geophysical variable in argument
    - with keys adequte dor operator 'plotmap'
    """
    rep=dict()
    rep["min"]=0  ; rep["max"]=100 ; rep["delta"]=10.
    #
    if var=='tas' :
        rep["offset"]=-273.15 ;  rep["units"]="C"
        rep["min"]=-15  ; rep["max"]=25 ; rep["delta"]=2.
    #
    return rep
    
map2=plotmap(ta,crs="Surface temperature (tas)",**map_graph_attributes(varOf(ta)))
cshow(map2)


if (cfile(map2)  is None) : exit(1)
