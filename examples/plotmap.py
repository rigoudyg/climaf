from climaf.api import *
clog(logging.ERROR)

# Define a dataset
#######################
cdef("frequency","monthly")
dataloc(experiment="AMIPV6ALB2G", organization="EM",url=[cpath+"/../examples/data/AMIPV6ALB2G"])
dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980-1981")

# Compute its basic climatology using an external script
#########################################################
cscript('time_average' ,cpath+'/../scripts/mcdo.sh timavg ${out} ${var} ${period} ${ins}' )
clog(logging.INFO)
ta=time_average(dg)

# A simple plotting using Ncview, without file output
#####################################################
cscript('ncview' ,'ncview ${in}' , format=None)
cobj(ncview(ta))

# A more sophisticated plot
############################
cscript('plotmap',"ncl "+ cpath +"/../scripts/plotmap.ncl infile=${in} plotname=${out} cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} var=${var} title=${crs} scale=${scale} offset=${offset} units=${units}",format="png")
map=plotmap(ta,color="BlueDarkRed18", min=260, max=300, delta=4, scale=1, offset=0, units="K")

# Ensure figure is computed, ans get its cache filename in CliMAF disk cache
figfile=cfile(map)

# getting a figure object will cache it if not already cached, and will also display it
cobj(map)

# A more comprehensive way of configuring plots
###################################################
def map_graph_attributes(var) :
    rep=dict()
    rep["offset"]=0.
    rep["scale"]=1.
    rep["color"]="BlueDarkRed18"
    if var=='tas' :
        rep["offset"]=-273.15 ;  rep["scale"]=1.0 ; rep["units"]="C"
        rep["min"]=-15  ; rep["max"]=25 ; rep["delta"]=2.
    return rep
    
map2=plotmap(ta,crs="aaa",**map_graph_attributes(varOf(ta)))
ceval(map2)

