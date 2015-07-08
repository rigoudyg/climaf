# -*- coding: iso-8859-1 -*-
"""
CliMAF module ``hmtl`` defines functions for building some html index
giving acces to figure files, through links bearing a label or through
thumbnails, and organized in tables. It eases iterating over lines and
columns in tables. **See an example in** :download:`index_html.py
<../examples/index_html.py>` and :download:`its screen dump
<../doc/html_index.png>`

"""

from climaf import __path__ as cpath

def html_header(title,style_file=None) :
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
        with open(cpath[0]+"/style.css") as fic :
            style=\
              """<style type="text/css" media=screen>"""+\
              fic.read()+\
              """</style>"""
    return rep+style+trailer+'\n'

def html_section(title,level=1,key="None"):
    """ Returns text for a section header in an html document
    with given title. Style depends on level value. Arg key is not yet used
    """
    return '<h'+`level`+'><a name="'+key+'"></a>'+title+'</h4>'+'\n'

def html_open_table(title="",titles=None,spacing=5):
    """ Returns header text for an html table. If titles is not None,
    it should be a dict which keys will be used as column titles. In
    that case, if title is provided, it is used as title for the first
    column.
    """
    rep= '<TABLE CELLSPACING='+`spacing`+'>'+'\n'
    if titles is not None :
        rep+=' <TR>\n <TH ALIGN=LEFT> '+title+' </TH> \n'
        dic=titles.keys()
        print dic
        for label in dic :
            rep+='<TD ALIGN=RIGHT>'+label+'</TD>\n'
        rep+='</TR> \n'
        return rep

def html_close_table() :
    """ Returns text for closing an html table
    """
    return("</TABLE>\n")

def html_table_lines(func,dic,*args,**thumb) :
    """ Returns text for multiple lines of a table, by iterating
    calls to :py:func:`~climaf.html.html_table_lines` . dic is a
    dictionary which keys are provided as first argument of the
    calls, and values as last argument. Dictionary argument thumb is
    forwarded too.
    """
    rep=""
    for var in dic:
        a=args+(dic[var],)
        rep+=html_table_line(func,var,*a,**thumb)
    return(rep)

def html_table_line(func,*args,**thumb) :
    """
    Create the html text for a line of table cells , which
    each includes an HREF link to an image file, and a label or thumbnail
    bearing this link. Last arg is a title for first column. But
    last argument, is a dictionary which keys are
    the labels and which values are tuples of arguments (or single
    values) to pass to the function for computing the filename. 
    Other arguments (except last and but last) are also passed to
    the function, in front of the dict values ones.
    The dict argument can also be a list.

    Example : assume function 'foo' takes 3 arguments and just
    concatenate them (assuming they are strings). A call to :
    
    >>> html_table_line(foo,'/root',{ 'labelA': ('/dirA','A.nc'), 'labelB':('/dirB','B.png') }, 'title' )

    will produce :
      <TH ALIGN=LEFT> <li>title</li> </TH> 
      <TD ALIGN=RIGHT><A HREF='/root/dirA/A.nc'>labelA</a> </TD>
      <TD ALIGN=RIGHT><A HREF='/root/dirB/B.png'>labelB</a> </TD>
      
    If func is None, a function like 'foo' above is used If last
    argument is a list, it is turned into a dictionary with value=key
    Values are not necessary tuples Dict argument thumb may include
    key 'thumbnail', in which case thumbnails will be generated (with
    the size being dict value)

    Examples:

    >>> html_table_line(None,'/root',[ '/labA', '/labB'])

    will produce :
    
      - <TD ALIGN=RIGHT><A HREF='/root/labA'>labA</a> </TD>
      - <TD ALIGN=RIGHT><A HREF='/root/labB'>labB</a> </TD>
    
    """
    def foo(*args):
        if len(args)==1 :
            return args[0]
        else:
            return reduce(lambda x,y : x+y, args)
    if not func : func=foo
    largs=list(args)
    title=largs.pop()
    rep=' <TR>\n <TH ALIGN=LEFT> <li>'+title+'</li> </TH> \n'
    dic=largs.pop()
    if not isinstance(dic,dict) :
        if not isinstance(dic,list) :
            print "Issue with dictionary : got `dic` "
            return
        else :
            dic=dict(zip(dic,dic))
    for k in dic :
        if not isinstance(dic[k],list) and not isinstance(dic[k],tuple) :
            dic[k]=[dic[k]]
    for label in dic :
        #print "largs="+`largs`
        allargs=largs[:]
        #print "dic[label]="+`dic[label]`
        allargs.extend(dic[label])
        #print "allargs="+`allargs`
        #print `func`
        #print "f="+func(*allargs)
        fig=func(*allargs)
        rep+='<TD ALIGN=RIGHT><A HREF="'+fig+'">'
        if 'thumbnail' not in thumb : rep+=label
        else: rep+= '<IMG HEIGHT=' + `thumb['thumbnail']` + ' WIDTH=' + `thumb['thumbnail']` + ' SRC="'+fig+'">'
        rep+='</a> </TD>\n'
    rep+='</TR> \n'
    return(rep)

def html_trailer():
    """ Returns the text for closing an html document
    """
    return("</body>\n")

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
