from climaf.api import *
clog(logging.INFO)
clog_file(logging.INFO)
dataloc(experiment="AMIPV6ALB2G", organization="example",url=[cpath+"/../examples/data/AMIPV6ALB2G"])

cdef("frequency","monthly")
cdef("period","1980-1981")

tas_ds=ds(experiment="AMIPV6ALB2G", variable="tas")
tas_ds

tas_ds.baseFiles()
#craz() # Clear CliMAF file cache for enforcing actual computation
cfile(tas_ds)
#cfile(ds(experiment="AMIPV6ALB2G", variable="tas"))
cfile(tas_ds)

#cscript('time_average' ,cpath+'/../scripts/mcdo.sh timavg ${out} ${var} ${period} ${ins}' ) #a l origine
#cscript('time_average' ,cpath+'/../scripts/mcdo_basics.sh ${out} ${var} ${period} ${in}' ) #option2 du script plus simplifie ou var et period ne sont pas des arguments optionnels (script plus simple, appel plus lourd)
#cscript('time_average' ,cpath+'/../scripts/mcdo_basics.sh ${out} "" "" ${in}' ) #var et period sont des arguments optionnels (script plus complique, appel simplifie)
cscript('time_average' ,cpath+'/../scripts/time_average.sh ${out} ${in}' )

#load ../scripts/time_average.sh

time_average
#help(time_average)

tas_avg=time_average(tas_ds)
tas_avg
#craz()
cfile(tas_ds)
cfile(tas_avg)

#tas_avg_MA=cexport(tas_avg,format="MaskedArray")
tas_avg_MA=cMA(tas_avg)
type(tas_avg_MA)
tas_avg_MA.shape

#cfile(tas_avg)
#cfile(time_average(ds('CMIP5.CNRM-CM5.AMIPV6ALB2G.r1i1p1.19800101-19820101.monthly.global.tas')))

cscript('my_ncview' ,'ncview ${in}' , format=None)

vfig=my_ncview(tas_avg)
vfig

cshow(vfig)

cscript('plotmap',\
        "ncl "+ cpath +"/../scripts/plotmap.ncl infile=${in} plotname=${out} \
                    cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} var=${var} \
                    title=${crs} scale=${scale} offset=${offset} units=${units}; convert ${out} -trim ${out}",format="png")
map=plotmap(tas_avg,color="BlueDarkRed18", min=260, max=300, delta=4, scale=1, offset=0, units="K")
map

cfile(map)

#cexport(map)
cshow(map)

def map_graph_attributes(var) :
    rep=dict()
    rep["offset"]=0.
    rep["scale"]=1.
    rep["color"]="BlueDarkRed18"
    if var=='tas' :
        rep["offset"]=-273.15 ;  rep["scale"]=1.0 ; rep["units"]="C"
        rep["min"]=-20  ; rep["max"]=20 ; rep["delta"]=2.
    return rep

map2=plotmap(tas_avg,crs="titre",**map_graph_attributes(varOf(tas_avg)))
print(map2)

fig1=map2
fig2=map
fig3=map2
fig4=map2
fig5=map2

figfile=cfile(map2) ; print(figfile)
from IPython.display import Image
#import os
#os.system('convert /home/vignonl/tmp/climaf_cache/22/b.png -trim /home/vignonl/tmp/climaf_cache/22/b.png')
Image(filename=figfile)

creShortTop=ds(experiment="AMIPV6ALB2G",variable="crest")

cscript('minus','cdo sub ${in_1} ${in_2} ${out}')

derive('crest','minus','rst','rstcs')

#cexport(my_ncview(creShortTop))
cshow(my_ncview(creShortTop))

#reload(climaf.driver)
#clist()

fig1=plotmap(tas_avg,crs="title",**map_graph_attributes(varOf(tas_avg)))
cfilePage([0.2,0.8],[0.33,0.33,0.33],figll=[[None, fig1, fig1],[fig1,fig1,fig1]],orientation="portrait") 
