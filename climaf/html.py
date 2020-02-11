#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
CliMAF module ``html`` defines functions for building some html index
giving acces to figure files, through links bearing a label or through
thumbnails. It eases iterating over lines and columns in tables.


**See a code example in** :download:`index_html.py <../examples/index_html.py>`
or :download:`a screen dump for a similar code <../doc/html_index.png>`  here |indexh|

.. |indexh| image:: ../doc/html_index.png
  :scale: 20%


"""

import os
import re
import glob
from climaf import __path__ as cpath
from climaf.cache import getCRS
from climaf import cachedir
from climaf.driver import cfile
import pickle
import shutil
from collections import OrderedDict
from clogging import clogger, dedent


def header(title, style_file=None):
    """ Returns text for an html document header, with provided
    title. If a style filename is not provided, a default style
    sheet will apply
    """
    rep = """
    <?xml version="1.0" encoding="iso-8859-1"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
    <head>
    <title>[ """ + title + """ ]</title>
    """
    trailer = """
    </head>
    <body>
    <h1>""" + title + """</h1>
    <hr/> <!--- this draws a line --->
    """
    if style_file is not None:
        with open(style_file) as fic:
            style = \
                """<style type="text/css" media=screen>""" + \
                fic.read() + \
                """</style>"""
    else:
        with open(cpath[0] + "/cami_style_css") as fic:
            style = \
                """<style type="text/css" media=screen>""" + \
                fic.read() + \
                """</style>"""
    return rep + style + trailer + '\n'


def trailer():
    """ Returns the text for closing an html document
    """
    return "</body>\n"


def vspace(nb=1):
    return nb * "<br>\n"


def section(title, level=1, key="None"):
    """ Returns text for a section header in an html document
    with given title. Style depends on level value. Arg key is not yet used
    """
    return '<h' + repr(level) + '><a name="' + key + '"></a>' + title + '</h4>' + '\n'


def open_table(title="", columns=[], spacing=5):
    """
    Returns header text for an html table. title will go as title for
    first column. columns should be a list of column titles
    """
    rep = '<TABLE CELLSPACING=' + repr(spacing) + '>' + '\n'
    rep += ' <TR>\n <TH ALIGN=LEFT> ' + title + ' </TH> \n'
    for label in columns:
        rep += '<TD ALIGN=RIGHT>' + label + '</TD>\n'
    rep += '</TR> \n'
    return rep


def close_table():
    """ Returns text for closing an html table
    """
    return "</TABLE>\n"


def open_line(title=""):
    return ' <TR>\n <TH ALIGN=LEFT> <li>' + title + '</li> </TH> \n'


def close_line():
    return ' </TR>\n'


def link(label, filename, thumbnail=None, hover=True):
    """
    Creates the provided label, with a link to the provided image
    filename (if not None) and possibly showing a thumbnail for the
    image (with the provided thumbnail size) and possibly displaying
    this image when mouse is over it (with the provided hover size).

    - 'thumbnail' can be an integer or a string with width or height
      (in these cases, width=height), or a string with width and height
      separated by character 'x' or '*'. The size is in pixels; default :
      None (no thumbnail)
    - 'hover' can be a logical, or a string with width or height (in this
      case, width=height), or a string with width and height separated by
      character 'x' or '*'. The size is in pixels; default is True, which
      tanslates according to value of thumbnail :

      - if thumbnail is not None, hover width and height are respectively
        set as 3 times that of thumbnail width and height
      - if thumbnail is None, size is '200*200'
    """
    if filename:
        regex = re.compile('(?P<width>[0-9]+)[x*](?P<height>[0-9]+)')
        if thumbnail is not None:
            thumbnail_width = None
            thumbnail_height = None
            if isinstance(thumbnail, basestring):
                thumbnail_regex_match = regex.match(thumbnail)
                if thumbnail_regex_match:
                    thumbnail_width = thumbnail_regex_match.groupdict()["width"]
                    thumbnail_height = thumbnail_regex_match.groupdict()["height"]
            else:
                thumbnail_width = thumbnail
                thumbnail_height = thumbnail
            if thumbnail_width is not None and not isinstance(thumbnail_width, int):
                thumbnail_width = int(thumbnail_width)
            if thumbnail_height is not None and not isinstance(thumbnail_height, int):
                thumbnail_height = int(thumbnail_height)

            if hover:
                if isinstance(hover, basestring):
                    hover_regex_match = regex.match(hover)
                    if hover_regex_match:
                        hover_width = hover_regex_match.groupdict()["width"]
                        hover_height = hover_regex_match.groupdict()["height"]
                    else:
                        try:
                            int(hover)
                        except:
                            raise Climaf_Html_Error("If hover is a not empty string, it must "
                                                    "contain width and/or height, separated by 'x' or '*'")

                        hover_width = hover
                        hover_height = hover
                else:
                    hover_width = 3 * int(thumbnail_width)
                    hover_height = 3 * int(thumbnail_height)

                if hover_height is not None and not isinstance(hover_height, int):
                    hover_height = int(hover_height)
                if hover_width is not None and not isinstance(hover_width, int):
                    hover_width = int(hover_width)

                rep = '<A class="info" HREF="' + filename + '"><IMG HEIGHT=' + repr(thumbnail_height) + \
                      ' WIDTH=' + repr(thumbnail_width) + ' SRC="' + filename + '"><span><IMG HEIGHT=' + \
                      repr(hover_height) + ' WIDTH=' + repr(hover_width) + ' SRC="' + \
                      filename + '"/></span></a>'

            else:
                rep = '<A HREF="' + filename + '"><IMG HEIGHT=' + repr(thumbnail_height) + \
                      ' WIDTH=' + repr(thumbnail_width) + ' SRC="' + filename + '"></a>'

        else:

            if hover:
                if isinstance(hover, basestring):
                    hover_regex_match = regex.match(hover)
                    if hover_regex_match:
                        hover_width = hover_regex_match.groupdict()["width"]
                        hover_height = hover_regex_match.groupdict()["height"]
                    else:
                        try:
                            int(hover)
                        except:
                            raise Climaf_Html_Error("If hover is a not empty string, it must "
                                                    "contain width and/or height, separaed by 'x' or '*'")

                        hover_width = hover
                        hover_height = hover
                else:
                    hover_width = 200
                    hover_height = 200

                if hover_height is not None and not isinstance(hover_height, int):
                    hover_height = int(hover_height)
                if hover_width is not None and not isinstance(hover_width, int):
                    hover_width = int(hover_width)

                rep = '<A class="info" HREF="' + filename + '">' + label + '<span><IMG HEIGHT=' + \
                      repr(hover_height) + ' WIDTH=' + repr(hover_width) + ' SRC="' + \
                      filename + '"/></span></a>'
            else:
                rep = '<A HREF="' + filename + '">' + label + '</a>'

    else:
        rep = label

    return rep


def link_on_its_own_line(label, filename, thumbnail=None, hover=True):
    """ Does the same as :py:func:`~climaf.html.link` ,but for a link which is
    sole on its own line
    """
    return open_line() + link(label, filename, thumbnail=thumbnail, hover=hover) + close_line()


def cell(label, filename=None, thumbnail=None, hover=True, dirname=None, altdir=None):
    """
    Create a table cell with the provided label, which bears a link to
    the provided filename and possibly shows a thumbnail for the link
    with the provided thumbnail size (in pixels) and possibly display
    it when you mouse over it (with the provided hover size in pixels).

    If 'dirname' is not None, creates  a hard link in directory dirname
    to file filename. This allow to generate a portable atlas in this
    directory. Hard links are named after pattern
    climaf_atlas<digit>.<extension>

    'dirname' can be a relative or absolute path, as long as
    filename and dirname paths are coherent

    If 'altdir' is not None (and 'dirname is None), the HREF links
    images in index have the prefix of their absolute path changed from
    $CLIMAF_CACHE to 'altdir' (use case : when the Http server only knows
    another filesystem). Example:

    - CLIMAF_CACHE=/prodigfs/ipslfs/dods/fabric/coding_sprint_NEMO/stephane
    - URL https://vesg.ipsl.upmc.fr **/thredds/fileServer/IPSLFS/fabric/coding_sprint_NEMO/stephane/** .../fig.png

    """
    if dirname:
        os.system('mkdir -p ' + dirname)
        if filename:
            tmpfilename, filextension = os.path.splitext(os.path.basename(filename))

            regex = re.compile('([a-z]+)\_([a-z]+)([0-9]+)')
            # !!! # -- Make a new nb that is unique to avoid the issues with images
            #          in the cache of the browser
            from datetime import datetime
            nbs = []
            from random import randrange
            nb = randrange(1, 10000000000)
            while nb in nbs:
                nb = randrange(1, 10000000000)
            nbs.append(nb)
            os.link(filename, dirname + "/climaf_atlas" + str(nb) + filextension)
            # -- Create/append the index file in the output directory that will provide
            # -- the CRS with the new png file (climaf_atlas...png)
            index_atlas = dirname + "/index_atlas"
            index_dict = {getCRS(filename): "climaf_atlas" + str(nb) + filextension}
            CRS_of_file = getCRS(filename)
            #
            if not os.path.isfile(index_atlas):
                # -- Create the dictionary
                tt = index_dict
            else:
                # -- Read the content of the index
                atlas_index_r = file(os.path.expanduser(index_atlas), "r")
                tt = pickle.load(atlas_index_r)
                atlas_index_r.close()
                # -- Append the file
                tt.update(index_dict)
            # -- Save the file
            atlas_index_w = file(os.path.expanduser(index_atlas), "w")
            pickle.dump(tt, atlas_index_w)
            atlas_index_w.close()

            return '<TD ALIGN=RIGHT>' + \
                   link(label, "climaf_atlas" + str(nb) + filextension, thumbnail, hover) + \
                   '</TD>\n'
        else:  # lv
            return '<TD ALIGN=RIGHT>' + \
                   link(label, filename, thumbnail, hover) + \
                   '</TD>\n'

    else:
        fn = filename
        if altdir and fn:  # lv
            from climaf import cachedir
            fn = filename.replace(cachedir, altdir)
        return '<TD ALIGN=RIGHT>' + \
               link(label, fn, thumbnail, hover) + \
               '</TD>\n'


def line(list_of_pairs, title="", thumbnail=None, hover=True, dirname=None, altdir=None):
    """
    Create an html line with labels and links from first args
    list_of_pairs (and when this is not a pair, only put the label).
    Put a line title if provided. Replace
    labels with thumbnail figures if arg thumbnail is set to a size
    (in pixels) and display figures when you mouse over it if arg
    hover is set to True or to a size (in pixels); in that case, dic
    can also be a list of filenames. If 'dirname' is not None, creates
    hardlinks to the filenames, in directory dirname, and named
    as 'climaf_atlas'([0-9]+).ext (where 'ext' is 'png', 'pdf' or 'eps').
    This allows to generate a portable atlas in dirname
    """
    labels = []
    figures = []

    for e in list_of_pairs:
        if isinstance(e, tuple):
            label = e[0]
            labels.append(label)
            figures.append(e[1])
        else:
            label = e
            labels.append(e)
            figures.append(None)
    rep = open_line() + title
    for lab, fig in zip(labels, figures):
        rep += cell(lab, fig, thumbnail, hover, dirname, altdir)
    return rep + close_line()


def flines(func, fargs, sargs, common_args=[],
           other_fargs=[], other_sargs=[], thumbnail=None, hover=True, dirname=None, **kwargs):
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
    with thumbnail of images and displaying images when you mouse over it with
    'hover' argument:

    >>> t=table_lines(avg,['tas','tos'],['land','sea'],thumbnail=40,hover='60x80')

    """
    rep = ""
    for farg in fargs:
        args = [farg, sargs] + common_args
        if other_fargs:
            args = args + other_fargs.get(farg, None)
        args = args + other_sargs
        if isinstance(fargs, list):
            title = repr(farg)
        else:
            title = fargs.get(farg, repr(farg))
        rep += fline(func, *args, title=title, thumbnail=thumbnail, hover=hover, dirname=dirname, **kwargs)
    return rep


def fline(func, farg, sargs, title=None,
          common_args=[], other_args=[], thumbnail=None, hover=True, dirname=None, **kwargs):
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
       ...  {'global':'GLB','sea':'SEA','land':'LND'}, 'tas averages')

    Advanced arguments :

      - common_args : a list of additionnal arguments to pass to
        'func', whatever the value of its second argument
      - other_args : a dictionnary of lists of additionnal arguments
        to pass to 'func'; only the entry which key equals running
        value of second argument is passed to 'func' (after common_args)
      - thumbnail : if 'func' returns a filename, generate a thumbnail
        image of that size (in pixels)
      - hover : if 'func' returns a filename, display image of that size
        (in pixels) when you mouse over it. If hover is True:

        - hover width and height are respectively set as 3 times that of
          thumbnail width and height if thumbnail is not None
        - hover is set to '200*200' if thumbnail is None
      - dirname : if 'func' returns a filename, creates a directory (if
        doesn't exist) wich contains filename as a hard link to the
        target dirname/'climaf_atlas'([0-9]+).ext ('ext' is 'png', 'pdf'
        or 'eps')
    """

    def foo(*args):
        if len(args) == 1:
            return args[0]
        else:
            return reduce(lambda x, y: x + y, args)

    if not func:
        func = foo
    #
    if not title:
        title = repr(farg)
    imposed_labels = True
    if not isinstance(sargs, dict):
        imposed_labels = False
        if not isinstance(sargs, list):
            print "Issue with second args :" + \
                  "not a dict nor a list (got `sargs`) "
            return
        else:
            sargs = OrderedDict(zip(sargs, sargs))
    rep = open_line(title)
    for key in sargs:
        allargs = [farg, sargs[key]]
        allargs = allargs + common_args
        if other_args:
            allargs = allargs + other_args.get(key, None)
        # print 'allargs=',allargs
        funcrep = func(*allargs, **kwargs)
        if isinstance(funcrep, tuple):
            # print "tuple case",lab,rfig
            lab, rfig = funcrep
        else:
            if imposed_labels or os.path.exists(funcrep):
                lab = sargs[key]
                rfig = funcrep
                # print "fig case",lab,rfig
            else:
                lab = funcrep
                rfig = None
                # print "lab case",lab,rfig
        rep += cell(lab, rfig, thumbnail, hover, dirname)
    rep += close_line()
    return rep
# cinstantiate("index.html","inst.html")


def cinstantiate(objin, filout=None, should_exec=True):
    """ Read file or string 'objin', extract parts of text surrounded by 'Â£',
    evaluate them as Python assignments or expressions, replaces
    expressions with the result of evaluation, and :
     - either returns the whole, modified, file content
     - or write it to filout (if provided)

     If assign is False, assignements will not be executed
    """

    def exec_and_discard_test(m):
        expression = m.group(1)
        if should_exec:
            # print "Executing %s"%expression
            # try :
            exec expression in globals()
            # except :
            #    print "Issue executing %s"%expression
        return ""

    #
    def replace_text_with_evaluation(m):
        expression = m.group(1)
        # print "Evaluating %s"%expression
        # try:
        rep = eval(expression, globals())
        # except :
        #    print "Issue evaluating %s"%expression
        # print "rep="+`rep`
        return rep if isinstance(rep, str) or isinstance(rep, str) else repr(rep)

    #
    import re
    import os.path
    if os.path.exists(objin):
        with open(objin) as filin:
            flux = filin.read()
    elif isinstance(objin, str) or isinstance(objin, unicode):
        flux = objin[:]
    else:
        print("Input is not a file nor a string" + repr(flux))
        return None
    # re.sub(r"Â£([^Â£]*)Â£",repl,"aaÂ£pp=6Â£bbÂ£`pp`Â£cc\nddÂ£`pp`Â£")
    rep = re.sub(u"Â£([^Â£]*)Â£", exec_and_discard_test, flux)
    rep = re.sub(u"&([^&]*)&", replace_text_with_evaluation, rep)
    if filout:
        with open(filout, 'w') as ficout:
            ficout.write(rep)
    else:
        return rep


# TODO: a function which copy all images referenced by the index, and modifies the index accordingly (for 'saving' the image package)
def compareCompanion():
    """ Includes the compareCompanion Javascript functionality
        developed by Patrick Brockmann (patrick.brockmann@lsce.ipsl.fr)
        The compareCompanion gives the possibility to put a selection
        of figures in a basket and create a new html page with this selection.
        In this new page the figures can be switched and the number of columns
        displaid is controlled with a slider (in the lower right corner)
    """
    return (
        ' <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.2.0/require.min.js">'
        '</script>\n <script type="text/javascript" '
        'src="https://cdn.rawgit.com/PBrockmann/compareCompanion/master/compareCompanion.js"></script> \n')


def start_line(title):
    tmpindex = open_table()
    tmpindex += open_line(title) + close_line() + close_table()
    tmpindex += open_table()
    tmpindex += open_line()
    return tmpindex


def safe_mode_cfile_plot(myplot,do_cfile=True,safe_mode=True):
    # Need to create cachedir if it does not exist yet
    if not os.path.isdir(cachedir):
        os.makedirs(cachedir)
    blank_cell = cachedir + '/Empty.png'
    if not os.path.isfile(blank_cell):
        shutil.copy(cpath[0] + '/plot/Empty.png', cachedir)

    if not do_cfile:
       return myplot
       #
    else:
       # -- We try to 'cfile' the plot
       if not safe_mode:
          print '-- plot function is not in safe mode --'
          return cfile(myplot)
       else:
          try:
             plot_filename = cfile(myplot)
             print '--> Successfully plotted ',myplot
             return plot_filename
          except:
             # -- In case it didn't work, we try to see if it comes from the availability of the data
             print '!! Plotting failed ',myplot
             print "set clog('debug') and safe_mode=False to identify where the plotting failed"
             return blank_cell


class Climaf_Html_Error(Exception):
    from clogging import clogger, dedent

    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)
