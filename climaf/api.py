"""
CliMAF module ``api`` defines functions for basic CliMAF use : a kind of Application Programm Interface for scripting in Python with CliMAF for easy climate model output processing.

It also imports a few functions from other modules, and declares a number of 'CliMAF standard operators'

Main functions are ``dataloc``, ``ds``, ``cdataset``, ``cdef``, ``cscript``, ``cfile``, ``cMA`` :
 - ``dataloc`` : set data locations for a series of experiments
 - ``cdef``    : define some default values for datasets attributes
 - ``ds``      : define a dataset object
 - ``cscript`` : define a new CliMAF operator (this also defines a new Pyhton fucntion)
 - ``cfile``   : get the file         value of a CliMAF object (compute it)
 - ``cMA``     : get the Masked Array value of a CliMAF object (compute it)


Utility functions are  ``clog``, ``cdump``, ``craz``, ``csave``:
 - ``clog``    : tune verbosity
 - ``cdump``   : tell what's in cache
 - ``craz``    : reset cache
 - ``csave``   : save cache index to disk

"""
# Created : S.Senesi - 2014


import os, os.path, shutil, logging

import climaf, climaf.cache
from climaf.classes   import cdefault as cdef,cdataset,ds #,cperiod
from climaf.driver    import ceval,varOf #,cfile,cobj 
from climaf.dataloc   import dataloc 
from climaf.operators import cscript, scripts as cscripts, derive
from climaf.cache     import creset as craz, csync as csave , cdump, cdrop
from clogging         import clogger, clog, clog_file
import climaf.standard_operators

clog(logging.ERROR)
clog_file(logging.ERROR)
#: Path for the CliMAF package. From here, can write e.g. ``cpath+"../scripts"``. The value shown in the doc is not meaningful for your own CliMAF install
cpath=os.path.abspath(climaf.__path__[0]) 
climaf.cache.setNewUniqueCache("~/tmp/climaf_cache")
climaf.standard_operators.load_standard_operators()

from driver import cpage #LV
import subprocess

# Commodity functions
def cfile(object,target=None,ln=None,deep=None) :
    """
    Provide the filename for a CliMAF object, or copy this file to target. Launch computation if needed. 

    Args:
      object (CliMAF object) : either a dataset or a 'compound' object (e.g. the result of a CliMAF operator)
      target (str, optional) : name of the destination file or link; CliMAF will anyway store the result
       in its cache; 
      ln (logical, optional) : if True, target is created as a symlink to the CLiMAF cache file
      deep (logical, optional) : governs the use of cached values when computing the object
      
        - if missing, or None : use cache as much as possible (speed up the computation)
        - False : make a shallow computation, i.e. do not use cached values for the 
          top level operation
        - True  : make a deep computation, i.e. do not use any cached value

    Returns: 
      - if 'target' is provided : returns this filename if computation is successful ('target' contains the result), and None otherwise; 
      - else : returns the filename in CliMAF cache, which contains the result (and None if failure)


    """
    clogger.debug("cfile called on"+str(object))  
    result=climaf.driver.ceval(object,format='file',deep=deep)
    if target is None : return result
    else :
        if result is not None :
            if ln :
                os.remove(os.path.expanduser(target))
                os.symlink(result,os.path.expanduser(target))
            else :
                shutil.copyfile(result,os.path.expanduser(target))
        return target

def cshow(obj) :
    """ 
    Provide the in-memory value of a CliMAF object. 
    For a figure object, this will lead to display it
    ( launch computation if needed. )
    """
    clogger.debug("cshow called on"+str(obj)) #LV
    return climaf.driver.ceval(obj,format='MaskedArray')

def  cMA(obj,deep=None) :
    """
    Provide the Masked Array value for a CliMAF object. Launch computation if needed.

    Args:
      obj (CliMAF object) : either a datset or a 'compound' object (like the result of a CliMAF standard operator)
      deep (logical, optional) : governs the use of cached values when computing the object

        - if missing, or None : use cache as much as possible
        - False : make a shallow computation, i.e. do not use cached values for top level operation
        - True  : make a deep computation, i.e. do not use any cached value

    Returns: a Masked Array containing the object's value

    """
    clogger.debug("cMA called with arguments"+str(obj)) 
    return climaf.driver.ceval(obj,format='MaskedArray',deep=deep)

def cexport(*args,**kwargs) :
    """ Alias for climaf.driver.ceval. Create synonyms for arg 'format'

    """
    clogger.debug("cexport called with arguments"+str(args))  #LV
    if "format" in kwargs :
        if (kwargs['format']=="NetCDF" or kwargs['format']=="netcdf" or kwargs['format']=="nc") :
            kwargs['format']="file" 
        if (kwargs['format']=="MA") :
            kwargs['format']="MaskedArray" 
    return climaf.driver.ceval(*args,**kwargs)

def cimport(cobject,crs) :
    clogger.debug("cimport called with argument",cobject)  
    clogger.debug("should check syntax of arg 'crs' -TBD")
    clogger.warning("cimport is not for the dummies - Playing at your own risks !")
    import numpy, numpy.ma
    if isinstance(cobject,numpy.ma.MaskedArray) :
        clogger.debug("for now, use a file for importing - should revisit - TBD")
        clogger.error("not yet implemented fro Masked Arrays - TBD")
    elif isinstance(cobject,str) :
        cache.register(cobject,crs)
    else :
        clogger.error("argument is not a Masked Array nor a filename",cobject)
    
#LV
def cfilePage(*args, **kwargs) :
    obj_cpage=cpage(*args, **kwargs)

    #test coherence des arguments
    if len(obj_cpage.figll)!=2 :
        clogger.error("cpage.figll must have 2 dimensions")
        return(None)
    for i in range(len(obj_cpage.figll)):
        if len(obj_cpage.figll[i])!=3 :
            clogger.error("cpage.figll must have 3 dimensions in each sublist, pb for sublist %d" % (i+1))
            return(None)
        
    #calcul des figures avec cfile => figfilesll : liste de liste des figures calculees
    figfilesll=[]
    for liste in obj_cpage.figll :
        #print liste
        listfig=[]
        for fig in liste :
            #print "figure", fig
            if fig is not None:
                fic=cfile(fig)
                listfig.append(fic)
            else:
                listfig.append('canvas:None') # mot cle 'canvas:None' en cas de "blanc"
        figfilesll.append(listfig)
    print "liste de liste des figs calculees", figfilesll

    #modif 8/04/15
    #tab_fig=[]
    #for i in range(len(figfilesll)):
    #    for j in range(len(figfilesll[i])):
    #        tab_fig.append(figfilesll[i][j])  
    #print "tab de fig", tab_fig
    #fin modif 8/04/15

    #mise en page
    largeur_page=800.
    hauteur_page=1200.
    c1=largeur_page*obj_cpage.taille_x[0]  #160
    c2=largeur_page*obj_cpage.taille_x[1]-40. #600
    l1=hauteur_page*obj_cpage.taille_y[0] #396 
    l2=hauteur_page*obj_cpage.taille_y[1]#396 
    l3=hauteur_page*obj_cpage.taille_y[2]#396 
   
    #modif 8/04
    #construction d un tableau correspondant aux echelles pour chaque figure
    #num coherente des figures avec INPUT et rajout des marges
    #scale_fig=("%dx%d+10+0" %(c1,l1), "%dx%d+10+400" %(c1,l2), "%dx%d+10+800" %(c1,l3),"%dx%d+180+50" %(c2,l1), "%dx%d+180+450" %(c2,l2), "%dx%d+180+850" %(c2,l3))
    #print scale_fig
    #fin modif 8/04

    #construction d une liste de listes correspondant aux echelles pour chaque figure
    #numerotation coherente des figures avec INPUT et rajout des marges
    scale_fig_l=[]
    scale_fig_l.append(["%dx%d+10+0" %(c1,l1), "%dx%d+10+400" %(c1,l2), "%dx%d+10+800" %(c1,l3)])
    scale_fig_l.append(["%dx%d+180+50" %(c2,l1), "%dx%d+180+450" %(c2,l2), "%dx%d+180+850" %(c2,l3)])
    #print scale_fig_l
            
    #construction de la page
    size_page="%dx%d"%(largeur_page, hauteur_page)
    comm=subprocess.Popen(["convert", "-size", size_page, "xc:white", "climaf_cpage.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    comm.wait()

    #modif 8/04
    #for i in range(len(tab_fig)):
    #    print i, scale_fig[i], tab_fig[i]
    #    comm=subprocess.Popen(["composite", "-geometry", scale_fig[i], tab_fig[i], "climaf_cpage.png", "climaf_cpage.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #    comm.wait()
    #modif 8/04
    
    for i in range(len(figfilesll)):
        for j in range(len(figfilesll[i])):
            print i, j, scale_fig_l[i][j], figfilesll[i][j]
            comm=subprocess.Popen(["composite", "-geometry", scale_fig_l[i][j], figfilesll[i][j], "climaf_cpage.png", "climaf_cpage.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            comm.wait()

    return figfilesll,obj_cpage

#convert -size 800x1200 xc:white composite.png
#composite -geometry 600x396+180+50 a_trim.png composite.png composite.png 
#composite -geometry 160x396+10+400 fig_test.png composite.png composite.png
#composite -geometry 160x396+10+800 fig_test.png composite.png composite.png
#composite -geometry 600x396+180+450 a_trim.png composite.png composite.png 
#composite -geometry 600x396+180+850 a_trim.png composite.png composite.png 

#convert -size 800x1200 xc:white a_trim.png -geometry 600x396+180+50 -composite fig_test.png -geometry 160x396+10+400 -composite fig_test.png -geometry 160x396+10+800 -composite a_trim.png -geometry 600x396+180+450 -composite a_trim.png -geometry 600x396+180+850 -composite composite_onecomm.png
