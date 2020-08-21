#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

CliMAF cache module : store, retrieve and manage CliMAF objects from their CRS expression.

"""
# Created : S.Sénési - 2014

from __future__ import print_function, division, unicode_literals, absolute_import

import sys
import six
import os
import os.path
import re
import time
import pickle
import uuid
import hashlib
from operator import itemgetter

from env.environment import *
from climaf import version
from climaf.utils import Climaf_Cache_Error
from .classes import compare_trees, cobject, cdataset, guess_projects, allow_error_on_ds
from .cmacro import crewrite
from env.clogging import clogger

currentCache = None
cachedirs = None

def setNewUniqueCache(path, raz=True):
    """ Define PATH as the sole cache to use from now. And clear it

    """
    global currentCache
    global cachedirs
    global cacheIndexFileName

    cachedirs = [path]  # The list of cache directories
    cacheIndexFileName = cachedirs[0] + "/index"  # The place to write the index
    currentCache = cachedirs[0]
    if raz:
        craz(hideError=True)


def generateUniqueFileName(expression, format="nc", create_dirs=True):
    """
    Generate a filename path from string EXPRESSION and FILEFORMAT,
    almost unique for the expression and the cache directory

    This uses hashlib.sha224
    """
    #
    if format is None:
        return ""
    rep = hash_to_path(hashlib.sha224(expression).hexdigest(), format)
    # Create the relevant directory, so that user scripts don't have to care
    if create_dirs :
        dirn = os.path.dirname(rep)
        if not os.path.exists(dirn):
            os.makedirs(dirn)
    clogger.debug("returning %s" % rep)
    return rep


def hash_to_path(vhash, format):
    rep = os.sep.join([currentCache, vhash[0:2], vhash[2:]])
    rep = ".".join([rep, format])
    rep = os.path.expanduser(rep)
    return rep


def register(filename, crs, outfilename=None):
    """
    Adds in FILE a metadata named 'CRS_def' and with value CRS, and a
    metadata 'CLiMAF' with CliMAF version and ref URL

    If OUTFILENAME is not None, FILENAME is a temporary file and
    it is moved to OUTFILENAME 

    Silently skip non-existing files
    """
    # It appears that we have to let some time to the file system  for updating its inode tables
    def do_move(crs, filename, outfilename):
        if outfilename is None:
            clogger.info("%s registered as %s" % (crs, filename))
            return True
        else:
            cmd = 'mv -f %s %s ' % (filename, outfilename)
            if os.system(cmd) == 0:
                clogger.info("moved %s as %s " % (filename, outfilename))
                clogger.info("%s registered as %s" % (crs, outfilename))
                return True
            else:
                # clogger.critical("cannot move by" % cmd)
                raise Climaf_Cache_Error("cannot move (possibly after stamping) by %s" % cmd)

    waited = 0
    while waited < 50 and not os.path.exists(filename):
        time.sleep(0.1)
        waited += 1
    # time.sleep(0.5)
    if os.path.exists(filename):
        if stamping is False:
            clogger.debug('No stamping')
            return do_move(crs, filename, outfilename)
        else:
            if re.findall(".nc$", filename) and ncatted_software is not None:
                command = "%s -h -a CRS_def,global,o,c,\"%s\" -a CliMAF,global,o,c,\"CLImate Model Assessment " \
                          "Framework version %s (http://climaf.rtfd.org)\" %s" % (ncatted_software, crs, version,
                                                                                  filename)
            elif re.findall(".png$", filename) and convert_software is not None:
                crs2 = crs.replace(r"%", r"\%").replace(r'"', r'\"')
                command = "%s -set \"CRS_def\" \"%s\" -set \"CliMAF\" " \
                          "\"CLImate Model Assessment Framework version " \
                          "%s (http://climaf.rtfd.org)\" %s %s.png && mv -f %s.png %s" % \
                          (convert_software, crs2, version, filename, filename, filename, filename)
            elif re.findall(".pdf$", filename) and pdftk_software is not None:
                tmpfile = str(uuid.uuid4())
                command = "%s %s dump_data output %s && echo -e \"InfoBegin\nInfoKey: Keywords\nInfoValue: %s\" " \
                          ">> %s && %s %s update_info %s output %s.pdf && mv -f %s.pdf %s && rm -f %s" % \
                          (pdftk_software, filename, tmpfile, crs, tmpfile, pdftk_software, filename, tmpfile, filename,
                           filename, filename, tmpfile)
            elif re.findall(".eps$", filename) and exiv2_software is not None:
                command = '%s -M"add Xmp.dc.CliMAF CLImate Model Assessment Framework version %s ' \
                          '(http://climaf.rtfd.org)" -M"add Xmp.dc.CRS_def %s" %s' % \
                          (exiv2_software, version, crs, filename)
            else:
                command = None
            if command is None:
                if stamping is None:
                    clogger.warning("Command is None and stamping is None. No stamping done.")
                    return do_move(crs, filename, outfilename)
                elif stamping is True:
                    raise Climaf_Cache_Error("Cannot stamp by command None. "
                                             "You may set climaf.cache.stamping to False or None - see doc\n%s" %
                                             command)
            else:
                clogger.debug("trying stamping by %s" % command)
                command_return = os.system(command)
                if command_return == 0 or stamping is not True:
                    return do_move(crs, filename, outfilename)
                if command_return != 0:
                    if stamping is True:
                        raise Climaf_Cache_Error("Cannot stamp by command below. "
                                                 "You may set climaf.cache.stamping to False or None - see doc\n%s" %
                                                 command)
                    elif stamping is None:
                        clogger.critical("Cannot stamp by %s" % command)
                        return True
    else:
        clogger.error("file %s does not exist (for crs %s)" % (filename, crs))


def getCRS(filename):
    """ Returns the CRS expression found in FILENAME's meta-data"""
    import subprocess
    if re.findall(".nc$", filename):
        form = 'ncdump -h %s | grep -E "CRS_def *=" | ' + \
               'sed -r -e "s/.*:CRS_def *= *\\\"(.*)\\\" *;$/\\1/" '
    elif re.findall(".png$", filename):
        form = 'identify -verbose %s | grep -E " *CRS_def: " | sed -r -e "s/.*CRS_def: *//"'
    elif re.findall(".pdf$", filename):
        form = 'pdfinfo %s | grep "Keywords" | awk -F ":" \'{print $2}\' | sed "s/^ *//g"'
    elif re.findall(".eps$", filename):
        form = 'exiv2 -p x %s | grep "CRS_def" | awk \'{for (i=4;i<=NF;i++) {print $i " "} }\' '
    else:
        clogger.error("unknown filetype for %s" % filename)
        return None
    command = form % filename
    try:
        rep = subprocess.check_output(command, shell=True).replace('\n', '')
        if (rep == "") and ('Empty.png' not in filename):
            clogger.error("file %s is not well formed (no CRS)" % filename)
        if re.findall(".nc$", filename):
            rep = rep.replace(r"\'", r"'")
    except:
        rep = "failed"
    clogger.debug("CRS expression read in %s is %s" % (filename, rep))
    return rep


def rename(filename, crs):
    """ 
    Rename FILENAME to match CRS. Also updates crs in file 
    """
    newfile = generateUniqueFileName(crs, format="nc")
    if newfile:
        os.rename(filename, newfile)
        register(newfile, crs)
        return newfile


def hasExactObject(cobject):
    i = 0
    formats_to_test = known_formats + graphic_formats
    while i < len(formats_to_test):
        f = generateUniqueFileName(cobject.crs, format=formats_to_test[i], create_dirs=False)
        if os.path.exists(f):
            return f
        else:
            i += 1

def cdrop(obj, rm=True, force=False):
    """
    Deletes the cached file for a CliMAF object, if it exists

    Args:
     obj (cobject or string) : object to delete, or its string representation (CRS)

     force (bool) : should we delete the object even if it is 'protected'

     rm (bool) : for advanced use only; should we actually delete (rm) the file, or just forget it in CliMAF cache index

    Returns:
     None if object does not exists, False if failing to delete, True if OK

    Example ::

    >>> dg=ds(project='example', simulation='AMIPV6ALB2G', variable='tas', period='1980-1981')
    >>> f=cfile(dg)
    >>> os.system('ls -al '+f)
    >>> cdrop(dg)

    """

    if isinstance(obj, cobject):
        crs = repr(obj)
    elif isinstance(obj, six.string_types):
        crs = str(obj)
    else:
        clogger.error("%s is not a CliMAF object" % repr(obj))
        return
    clogger.info("Discarding cached value for %s (except if protected)" % crs)
    fil = generateUniqueFileName(crs, create_dirs=False)
    if rm:
            try:
                if force:
                    os.system("chmod +w " + fil)
                if not os.access(fil, os.W_OK):
                    clogger.info("Object %s is protected" % crs)
                    return
                path_file = os.path.dirname(fil)
                os.remove(fil)
                try:
                    os.rmdir(path_file)
                except OSError as ex:
                    pass
                    # clogger.warning(ex)
                return True
            except:
                clogger.warning("When trying to remove %s : file does not exist in cache" % crs)
                return False
    else:
        clogger.info("%s is not cached" % crs)
        return None


def cprotect(obj, stop=False):
    """
    Protects the cache file for a given object (or stops protection with arg 'stop=True').

    In order to erase it, argument 'force=True' must then be used with function
    :py:func:`~climaf.cache.craz` or :py:func:`~climaf.cache.cdrop`

    """
    if isinstance(obj, cobject):
        crs = repr(obj)
        if isinstance(obj, cdataset):
            crs = "select(" + crs + ")"
    elif isinstance(obj, six.string_types):
        crs = obj
    else:
        clogger.error("%s is not a CliMAF object" % repr(obj))
        return

    f= generateUniqueFileName(crs, create_dirs=False)
    if os.path.exists(f):
        if stop is False:
            clogger.info("Protecting cached value for " + crs)
            os.system("chmod -w " + f)
        else:
            clogger.info("Stopping protection on cached value for " + crs)
            os.system("chmod +w " + f)
        return
    else:
        clogger.info("%s is not (yet) cached; use cfile() to cache it" % crs)


def csync(update=False):
    pass

def craz(force=False, hideError=False):
    """
    Clear CliMAF cache : erase existing files content, reset in-memory index

    Args:
      force (bool): should we erase also all 'protected' files

      hideError (bool): if True, will not warn for non existing cache

    """
    cc = os.path.expanduser(currentCache)
    if os.path.exists(currentCache) or hideError is False:
        if force:
            os.system("chmod -R +w  " + cc)
        os.system("rm -fR " + cc + "/*")


def cdump(use_macro=True):
    clogger.error("Function cdump is deprecated")

def clist(size="", age="", access=0, pattern="", not_pattern="", usage=False, count=False,
          remove=False, CRS=False, special=False):
    clogger.error("Function clist is deprecated")

def cls(**kwargs):
    clogger.error("Function cls is deprecated")

def crm(**kwargs):
    clogger.error("Function crm is deprecated")

def cdu(**kwargs):
    clogger.error("Function cdu is deprecated")

def cwc(**kwargs):
    clogger.error("Function cwc is deprecated")

def rebuild():
    clogger.error("Function rebuild is deprecated")


