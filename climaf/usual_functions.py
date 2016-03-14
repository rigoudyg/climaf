from climaf.api import *
from climaf.operators import *

# -- Fonctions de plot interractives
from IPython.display import Image

def iplot(map):
    return Image(filename=cfile(map))


# -- Calcul de moyenne sur la verticale dans l'ocean

# -> Identifie les niveaux verticaux du fichier compris entre zmin et zmax
def getLevs(dat,zmin,zmax,convertPressureUnit=None):
    from anynetcdf import ncf
    filename=dat.baseFiles()
    fileobj=ncf(filename)
    min_lev = zmin
    max_lev = zmax
    my_levs=None
    levname=None
    for varname in fileobj.variables:
        if varname in ['level','levels','lev','levs','depth','deptht','DEPTH','DEPTHT','plev']:
            levname=varname
    for lev in fileobj.variables[levname].getValue():
        #print lev
        if min_lev <= lev <= max_lev:
            if convertPressureUnit:
               if convertPressureUnit=='hPaToPa':
                  lev = lev*100
               if convertPressureUnit=='PaTohPa':
                  lev = lev/100
            if my_levs:
                my_levs=my_levs+','+str(int(lev))
            else:
                my_levs=str(int(lev))
    return my_levs




def vertical_average(dat,zmin,zmax):    
    levs = getLevs(dat,zmin,zmax)
    print ' --> Compute average on the following vertical levels : '+levs
    tmp = ccdo(dat, operator="'vertmean -sellevel,'+levs'")
    return tmp


import numpy as np
##
#load_standard_operators()
# 
# Bidouille ...
#
def implot(map,**kwargs):
    return Image(filename=cfile(plot(map,**kwargs)))
   
def diff_regrid(data1, data2):
    return minus(regrid(data1,data2), data2)

def diff_regridn (data1, data2, cdogrid='n90'):
    return minus ( regridn( data1, cdogrid=cdogrid), regridn( data2, cdogrid=cdogrid ))

def diff_n90 (data1, data2):
    return diff_regridn ( data1, data2, cdogrid='n90' )

def icpage(fig_lines, heights=None, widths=None, **kwargs):
    if not heights :
        n_lin=len(fig_lines)
        heights = [1.0 / n_lin for i in range(n_lin)]

    if not widths:
        n_col=len(fig_lines[0])
        widths  = [1.0 / n_col for i in range(n_col)]

    return iplot(cpage(fig_lines=fig_lines, heights=heights, widths=widths, **kwargs))

def icpage2(fig_lines, **kwargs):
    n_lin=len(fig_lines)
    n_col=len(fig_lines[0])
    heights = [1.0 / n_lin for i in range(n_lin)]
    widths  = [1.0 / n_col for i in range(n_col)]
    return iplot(cpage(fig_lines=fig_lines, heights=heights, widths=widths, **kwargs))


def page_new(n_lin=1, n_col=1):   
    heights = [1.0 / n_lin for i in range(n_lin)]
    widths  = [1.0 / n_col for i in range(n_col)]
    view    = [[None for i in range(n_col)] for j in range(n_lin)]
    return {'heights':heights, 'widths':widths, 'view':view, 'n_lin':n_lin, 'n_col':n_col}

            

def tableau(n_lin=1, n_col=1):
    view    = [[ None for i in range(n_col)] for j in range(n_lin)]
    return view



def annual_cycle(dat):
    return ccdo(dat, operator="ymonavg")

def seasonal_average(dat,season):
    # -- Classic atmospheric seasons
    if season=='DJF': selmonths ='1,2,12'
    if season=='MAM': selmonths ='3,4,5'
    if season=='JJA': selmonths ='6,7,8'
    if season=='SON': selmonths ='9,10,11'
    # -- Classic oceanic seasons
    if season=='JFM': selmonths ='1,2,3'
    if season=='JAS': selmonths ='7,8,9'
    if season=='JJAS': selmonths ='6,7,8,9'
    # -- Classic ice
    if season=='March': selmonths ='3'
    if season=='September': selmonths ='9'
    #
    # -- Compute the annual cycle
    scyc = annual_cycle(dat)
    #
    # -- Then compute the seasonal average
    if season in ['March','September']:
       avg = ccdo(scyc,operator='selmon,'+selmonths)
    else:
       avg = time_average(ccdo(scyc,operator='selmon,'+selmonths))
    #
    return avg

def climato(dat):
    return time_average(dat)


def summary(dat):
    if 'baseFiles' not in dir(dat):
       print '-- Ensemble members:'
       for m in dat.members:
           for f in str.split(m.baseFiles(),' '): print f
           print 'Keys - values:'
           print m.kvp
           print '--'
    else:
	if not dat.baseFiles():
		print '-- No file found for:'
    	else:
		for f in str.split(dat.baseFiles(),' '): print f
    	return dat.kvp


def projects():
    print '-- Available projects:'
    for key in cprojects.keys():
        print '-- Project:',key
        print 'Facets =>',cprojects[key]


