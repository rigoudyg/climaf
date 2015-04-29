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


Utility functions are  ``clog``, ``cdump``, ``craz``, ``csave``, ``cfilePage``:
 - ``clog``      : tune verbosity
 - ``cdump``     : tell what's in cache
 - ``craz``      : reset cache
 - ``csave``     : save cache index to disk
 - ``cfilePage`` : build a page with CliMAF figures

"""
# Created : S.Senesi - 2014


import os, os.path, shutil, logging, subprocess

import climaf, climaf.cache
from climaf.classes   import cdefault as cdef, cdataset, ds, cpage #,cperiod
from climaf.driver    import ceval, varOf #,cfile,cobj 
from climaf.dataloc   import dataloc 
from climaf.operators import cscript, scripts as cscripts, derive
from climaf.cache     import creset as craz, csync as csave, cdump, cdrop
from clogging         import clogger, clog, clog_file
import climaf.standard_operators

clog(logging.ERROR)
clog_file(logging.ERROR)
#: Path for the CliMAF package. From here, can write e.g. ``cpath+"../scripts"``. The value shown in the doc is not meaningful for your own CliMAF install
cpath=os.path.abspath(climaf.__path__[0]) 
climaf.cache.setNewUniqueCache("~/tmp/climaf_cache")
climaf.standard_operators.load_standard_operators()


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

def cfilePage(cobj) :
    """ Builds a page with CliMAF figures, computing associated crs 
        
        Arg:
        - cobj (CliMAF object): a cpage object containing :
            - the list of figure widths, i.e. the width of each column (cobj.widths_list)
            - the list of figure heights, i.e. the height of each line (cobj.heights_list)
            - a list of crs list. Each sublist of 'fig_lines' represents crs for each line (cobj.fig_lines)
            - page's orientation, either 'portrait' or 'landscape' -by default, orientation is set to 'portrait'- (cobj.orientation)

        Returns the filename in CliMAF cache, which contains the result (and None if failure)

        Example, using no default value, to create a page with 2 columns and 3 lines:

          >> fig=plotmap(tas_avg,crs='title',**map_graph_attributes(varOf(tas_avg)))
          
          cfilePage(cpage(widths_list=[0.2,0.8],heights_list=[0.33,0.33,0.33],\
          fig_lines=[[None, fig],[fig, fig],[fig,fig]],orientation='portrait'))

    """
    if not isinstance(cobj,climaf.classes.cpage):
        clogger.error("arg cobj is not a cpage object")
        return(None)

    #output figure
    out_fig="climaf_cpage.png"
    #out_fig=climaf.cache.generateUniqueFileName("chaine_crs_test_for_cpage",format="png")
    #[getCRS     : cache.py  , L. 143 ] : ERROR    : file /home/vignonl/tmp/climaf_cache/75/2.png is not well formed (no CRS)
    #out_fig=climaf.cache.generateUniqueFileName("plotmap(time_average(ds('example.*.AMIPV6ALB2G.r1i1p1.1980-1981.monthly.global.tas.*.*')), color='BlueDarkRed18', crs='titre', delta=2.0, max=30, min=-30, offset=-273.15, scale=1.0, units='C')",format="png")

    #size page and creation
    if cobj.orientation == "portrait":
        page_width=800.
        page_height=1200.
    elif cobj.orientation == "landscape":
        page_width=1200.
        page_height=800.
    
    size_page="%dx%d"%(page_width, page_height)
    comm=subprocess.Popen(["convert", "-size", size_page, "xc:white", out_fig], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    comm.wait()
    if comm.wait()!=0 : raise climaf.classes.Climaf_cpage_Error("Page creation failed")

    #margins
    x_left_margin=10. # Left shift at start and end line
    y_top_margin=10. # Initial vertical shift for first line
    x_right_margin=10. # Right shift at start and end line
    y_bot_margin=10.  # Vertical shift for last line
    xmargin=20. # Horizontal shift between figures
    ymargin=20. # Vertical shift between figures

    #page composition
    y=y_top_margin
    for line, rheight in zip(cobj.fig_lines, cobj.heights_list) :
        height=(page_height-ymargin*(len(cobj.heights_list)-1.)-y_top_margin-y_bot_margin)*rheight # Line height in pixels
        x=x_left_margin
        
        for fig, rwidth in zip(line, cobj.widths_list) :
            width=(page_width-xmargin*(len(cobj.widths_list)-1.)-x_left_margin-x_right_margin)*rwidth # Figure width in pixels
            scaling="%dx%d+%d+%d" %(width,height,x,y)
            figfile=cfile(fig) if fig else 'canvas:None' 
            comm=subprocess.Popen(["composite", "-geometry", scaling, figfile, out_fig, out_fig], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            comm.wait()
            if comm.wait()!=0 : raise climaf.classes.Climaf_cpage_Error("Composite failed for figure %s" %fig)
            x+=width+xmargin
            
        y+=height+ymargin

    return cobj
