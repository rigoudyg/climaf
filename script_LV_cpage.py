from climaf.api import *
clog(logging.INFO)
clog_file(logging.INFO)

dataloc(experiment="AMIPV6ALB2G", organization="example",url=[cpath+"/../examples/data/AMIPV6ALB2G"])
cdef("frequency","monthly")
cdef("period","1980-1981")

tas_ds=ds(experiment="AMIPV6ALB2G", variable="tas")
tas_ds.baseFiles()
cfile(tas_ds)

cscript('time_average' ,cpath+'/../scripts/time_average.sh ${out} ${in}' )
tas_avg=time_average(tas_ds)
cfile(tas_avg)

def map_graph_attributes(var) :
    rep=dict()
    rep["offset"]=0.
    rep["scale"]=1.
    rep["color"]="BlueDarkRed18"
    if var=='tas' :
        rep["offset"]=-273.15 ;  rep["scale"]=1.0 ; rep["units"]="C"
        rep["min"]=-20  ; rep["max"]=20 ; rep["delta"]=2.
    return rep

fig1=plotmap(tas_avg,crs="title",**map_graph_attributes(varOf(tas_avg)))

#cfilePage
cfilePage(cpage(widths_list=[0.2,0.8],heights_list=[0.33,0.33,0.33],fig_lines=[[None, fig1],[fig1, fig1],[fig1,fig1]],orientation="portrait"))

cfilePage(cpage(widths_list=[0.5,0.5],heights_list=[0.5,0.5],fig_lines=[[None, fig1],[fig1, fig1]],orientation="landscape"))

cfilePage(cpage(widths_list=[0.2,0.4,0.4],heights_list=[0.5,0.5],fig_lines=[[None, fig1, fig1],[fig1,fig1,fig1]],orientation="landscape"))
