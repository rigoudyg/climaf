# -*- coding: iso-8859-1 -*-
"""
CliMAF module ``html`` defines functions for building some html index
giving acces to figure files, through links bearing a label or through
thumbnails. It eases iterating over lines and columns in tables. **See
an example in** :download:`index_html.py <../examples/index_html.py>`
and :download:`its screen dump <../doc/html_index.png>`

"""

import os
from climaf import __path__ as cpath

def header(title,style_file=None) :
    """ Returns text for an html document header, with provided
    title. If a style filename is not provided, a default style sheet
    will apply
    """
    rep= """
    <?xml version="1.0" encoding="iso-8859-1"?> 
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">    
    <head>
    <title>[ """ + title + """ ]</title>
    """
    trailer="""
        </head>
        <body>
        <h1>"""+ title +"""</h1>
        <hr/> <!--- this draws a line --->
        """
    if style_file is not None :
        style=\
          """<link rel="stylesheet" href=""" +\
          style_file +\
          """ type="text/css"/>"""
    else:
        with open(cpath[0]+"/cami_style_css") as fic :
            style=\
              """<style type="text/css" media=screen>"""+\
              fic.read()+\
              """</style>"""
    return rep+style+trailer+'\n'

def trailer():
    """ Returns the text for closing an html document
    """
    return("</body>\n")

def vspace(nb=1) : 
    return nb*"<br>\n"

def section(title,level=1,key="None"):
    """ Returns text for a section header in an html document
    with given title. Style depends on level value. Arg key is not yet used
    """
    return '<h'+`level`+'><a name="'+key+'"></a>'+title+'</h4>'+'\n'

def open_table(title="",columns=[],spacing=5):
    """ 
    Returns header text for an html table. title will go as title for
    first column. columns should be a list of column titles
    """
    rep= '<TABLE CELLSPACING='+`spacing`+'>'+'\n'
    rep+=' <TR>\n <TH ALIGN=LEFT> '+title+' </TH> \n'
    for label in columns:
        rep+='<TD ALIGN=RIGHT>'+label+'</TD>\n'
    rep+='</TR> \n'
    return rep

def close_table() :
    """ Returns text for closing an html table
    """
    return("</TABLE>\n")

def open_line(title) :
    return(' <TR>\n <TH ALIGN=LEFT> <li>'+title+'</li> </TH> \n')

def close_line() :
    return(' </TR>\n')

def link(label,filename,thumbnail=None) :
    """ 
    Creates the provided label, with a link to the provided image
    filename (if not None) and possibly showing a thumbnail for the
    image (with the provided thumbnail size)
    """
    if filename :
        rep='<A HREF="'+filename+'">'
        if thumbnail is not None :
            rep+= '<IMG HEIGHT=' + `thumbnail` + \
                ' WIDTH=' + `thumbnail` + ' SRC="'+filename+'">'
        else:
            rep+=label
        rep+='</a>'
    else:
        rep=label
    return rep

def cell(label,filename=None,thumbnail=None) :
    """ 
    Create a table cell with the provided label, which bears a link to
    the provided filename and possibly shows a thumbnail for the link
    with the provided thumbnail size
    """
    return '<TD ALIGN=RIGHT>'+ \
        link(label,filename,thumbnail)+\
        '</TD>\n'

def line(dic,title="",thumbnail=None):
    """
    Create an html line with labels from dic keys and links to
    filenames from dic values. Put a line title if provided. Replace
    labels with thumbnail figures if arg thumbnail is set to a size
    (in pixels);in that case, dic can also be a list of filenames
    """
    if thumbnail :
        if isinstance(dic,dict) : 
            figures=dic.values()
        else : 
            figures=dic.keys()
        labels=figures # not actually used
    else : 
        figures=dic.values()
        labels=dic.keys()
    rep=title
    for lab,fig in zip(labels,figures): 
        rep+=cell(lab,fig,thumbnail)
    rep+=vspace()
    return rep

def flines(func,fargs, sargs, common_args=[], \
       other_fargs=[], other_sargs=[], thumbnail=None, **kwargs):
    """ 
    **See doc for** :py:func:`~climaf.html.fline` **first** 

    Creates a table by iterating calling fline over 'fargs'
    (which can be a list or a dict) with :

    - 'farg' being the running element (or key) of 'fargs' 
    - 'title' being the corresponding 'fargs' value (or 'farg' if not a dict)
    - 'common_args' being forwarded to :py:func:`~climaf.html.fline`
    - 'other_args' being the merge of other_fargs[farg] and other_sargs
    
    It forwards remaining keyword arguments (kwargs) to  :py:func:`~climaf.html.fline`

    Example : assuming that function avg returns the filename for a figure
    showing the average value of a variable over a mask, create a
    table of links for average values of two variables over two masks,
    with thumbnail of images:

    >>> t=table_lines(avg,['tas','tos'],['land','sea'],thumbnail=40)

    """
    rep=""
    for farg in fargs:
        args=[farg,sargs]+common_args
        if other_fargs : 
            args=args+other_fargs.get(farg,None)
        args=args+other_sargs
        if isinstance(fargs,list) :
            title=`farg`
        else:
            title=fargs.get(farg,`farg`)
        rep+=fline(func,*args,title=title,thumbnail=thumbnail,**kwargs)
    return(rep)


def fline(func,farg, sargs, title=None, \
         common_args=[], other_args=[], thumbnail=None, **kwargs) :
    """
    Create the html text for a line of table cells, by iterating
    calling a function, once per column, with at least two
    arguments. Cells have a label and possibly a link

    - 'func' is a python function which computes and labels 
      and/or figures; 
    - 'farg' is any object, used a 1st arg for 'func'; 
    - 'sargs' is a list or a dict, used for providing 
      the 2nd arg to each call to 'func'. 
    - 'title' is a line title (for first column); 
      if missing, 'farg' is used
    - see further below fo remaining arguments
    
    So, there will be one column/cell per item in 'sargs'; each cell
    shows a label which can be an active link.  Both the label value
    and the link value can be the result of calling 'func' arg with
    the pair of arguments ('farg' and the running element of 'sargs');
    the function can return a single value (either a label or a figure
    filename) or both

    Use cases :

     - a line showing just numeric values; we assume that 
       function average(var,mask) returns such a numeric 
       value, which is a gloabl average of a variable over a mask:

       >>> rep=fline(average, 'tas', \
       ...   [ 'global', 'sea', 'land', 'tropics'], 'tas averages')

     - a line showing the same average values, but each value is a
       link to e.g. a figure of the time series of global average
       values : same call, but just let function 'average' compute the
       average and the figure, and return a couple : average, figure
       filename

     - a line showing pre-defined labels, which here are shortcuts for
       mask names, and which carry links to same figures as above : let
       function 'average' only return the figure filename, and call :
 
       >>> rep=fline(average, 'tas', 
       ...  {'global':'GLB','sea':'SEA','land':"LND"}, 'tas averages')

    Advanced arguments :

      - common_args : a list of additionnal arguments to pass to
        'func', whatever the value of its second argument
      - other_args : a dictionnary of lists of additionnal arguments
        to pass to 'func'; only the entry which key equals running
        value of second argument is passed to 'func' (after common_args)
      - thumbnail : if 'func' returns a filename, generate a thumbnail
        image of that size (in pixels)

    """
    def foo(*args):
        if len(args)==1 :
            return args[0]
        else:
            return reduce(lambda x,y : x+y, args)
    if not func : func=foo
    #
    if not title : title=`farg`
    imposed_labels=True
    if not isinstance(sargs,dict) :
        imposed_labels=False
        if not isinstance(sargs,list) :
            print "Issue with second args :"+\
                "not a dict nor a list (got `sargs`) "
            return
        else :
            sargs=dict(zip(sargs,sargs))
    rep=open_line(title)
    for key in sargs : 
        allargs=[farg,sargs[key]]
        allargs=allargs+common_args
        if other_args :
            allargs=allargs+other_args.get(key,None)
        #print 'allargs=',allargs
        funcrep=func(*allargs,**kwargs)
        if isinstance(funcrep,tuple): 
            #print "tuple case",lab,rfig
            lab,rfig=funcrep
        else :
            if imposed_labels or os.path.exists(funcrep) :
                lab=sargs[key] ; rfig=funcrep
                #print "fig case",lab,rfig
            else:
                lab=funcrep ; rfig=None
                #print "lab case",lab,rfig
        rep+=cell(lab,rfig,thumbnail)
    rep+=close_line()
    return(rep)

#cinstantiate("index.html","inst.html")


def cinstantiate(objin,filout=None,should_exec=True) :
    """ Read file or string 'objin', extract parts of text surrounded by '£',
    evaluate them as Python assignments or expressions, replaces
    expressions with the result of evaluation, and :
     - either returns the whole, modified, file content
     - or write it to filout (if provided)

     If assign is False, assignements will not be executed
    """
    def exec_and_discard_test(m):
        expression=m.group(1)
        if should_exec :
            #print "Executing %s"%expression
            #try :
            exec expression in globals()
            #except :
            #    print "Issue executing %s"%expression
        return ""
    #
    def replace_text_with_evaluation(m):
        expression=m.group(1)
        #print "Evaluating %s"%expression
        #try:
        rep=eval(expression,globals())
        #except :
        #    print "Issue evaluating %s"%expression
        #print "rep="+`rep`
        return rep if isinstance(rep,str) or isinstance(rep,str) else `rep`
    #
    import re, os.path
    if os.path.exists(objin) :
        with open(objin) as filin :
            flux=filin.read()
    elif isinstance(objin,str) or isinstance(objin,unicode) :
        flux=objin[:]
    else:
        print("Input is not a file nor a string"+`flux`)
        return(None)
    #re.sub(r"£([^£]*)£",repl,"aa£pp=6£bb£`pp`£cc\ndd£`pp`£")
    rep=re.sub(u"£([^£]*)£",exec_and_discard_test,flux)
    rep=re.sub(u"&([^&]*)&",replace_text_with_evaluation,rep)
    if filout :
        with open(filout,'w') as ficout :
            ficout.write(rep)
    else:
        return rep

# TODO : a function which copy all images referenced by the index, and modifies
# the index accordingly (for 'saving' the image package)
