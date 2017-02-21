"""

CliMAF cache module : store, retrieve and manage CliMAF objects from their CRS expression.



"""
# Created : S.Senesi - 2014

import sys, os, os.path, re, time, glob
import pickle
import uuid
import hashlib
from operator import itemgetter  

from climaf import version
from classes import compare_trees, cobject, cdataset, cprojects, guess_projects, allow_error_on_ds
from cmacro  import crewrite
from clogging import clogger, dedent
import operators

currentCache=None
cachedirs=None
#: The length for truncating the hash value of CRS expressions when forming cache filenames
fileNameLength=60
#: Define whether we try to have safe naming of cache objects using adaptative filename length
safe=False
#: The length of subdir names when segmenting cache filenames
directoryNameLength=5
#: Define whether we stamps the data files with their CRS
stamping=True
#: The index associating filenames to CRS expressions
crs2filename=dict()
#: The dictionary associating CRS expressions to their evaluation 
crs2eval=dict()

#: A dict containing cache index entries (as listed in index file), which 
# were up to now not interpretable, given the set of defined projects
crs_not_yet_evaluable=dict()

def setNewUniqueCache(path,raz=True) :
    """ Define PATH as the sole cache to use from now. And clear it 

    """
    global currentCache
    global cachedirs
    global cacheIndexFileName
    
    cachedirs=[ path ] # The list of cache directories
    cacheIndexFileName = cachedirs[0]+"/index"  # The place to write the index
    currentCache=cachedirs[0]
    if (raz) : craz(hideError=True)

def generateUniqueFileName(expression, operator=None, format="nc"):
    if safe and stamping :
        return generateUniqueFileName_safe(expression, operator=operator, format=format)
    else :
        return generateUniqueFileName_unsafe(expression, format=format)
    
def generateUniqueFileName_unsafe(expression, format="nc"):
    """
    Generate a filename path from string EXPRESSION and FILEFORMAT,
    almost unique for the expression and the cache directory

    This uses hashlib.sha224, which are truncated to fileNameLength. 

    Generated names drive a structure where each directory name 
    has dirNameLength characters
    """
    #
    if format==None : return ""
    prefix=""
    full=hashlib.sha224(expression).hexdigest()
    rep=currentCache+"/"+prefix+stringToPath(full[0 : fileNameLength - 1 ], directoryNameLength )+"."+format
    rep=os.path.expanduser(rep)
    # Create the relevant directory, so that user scripts don't have to care
    dirn=os.path.dirname(rep)
    if not os.path.exists(dirn) : os.makedirs(dirn)
    clogger.debug("returning %s"%rep)
    return(rep)

def generateUniqueFileName_safe(expression, operator=None, format="nc"):
    """ Generate a filename path from string EXPRESSION and FILEFORMAT, unique for the
    expression and the set of cache directories currently listed in cache.cachedirs 
    OPERATOR may be a function that provides a prefix, using EXPRESSION

    This uses hashlib.sha224, which are truncated to 3 (or more) characters. 
    More characters are used if a shorter name is already in use for another
    expression in one of the known cache directories 

    Generated names drive a structure where each directory name 1 or 2
    characters and file names have no more characters

    Exits if uniqueness is unachievable (quite unexpectable !) """
    #
    if format==None : return ""
    prefix=""
    if operator is not None :
        prefix2=operator(expression)
        if prefix2 is not None : prefix=prefix2+"/"
    full=hashlib.sha224(expression).hexdigest()
    number=fileNameLength
    guess=full[0 : number - 1 ]
    existing=searchFile(prefix+stringToPath(guess, directoryNameLength )+"."+format)
    if existing : 
        readCRS=getCRS(existing)
        # Update index if needed
        if readCRS not in crs2filename :
            clogger.warning("existing data %s in file %s was not yet registered in cache index"%\
                                (readCRS,existing))
            crs2filename[readCRS]=existing
    while ( ( existing is not None ) and ( readCRS != expression )) :
        clogger.debug("must skip %s which CRS is %s"%\
                      (existing, getCRS(existing) ))
        number += 2
        if (number >= len(full) ) :
            clogger.critical("Critical issue in cache : "+len(full)+" digits is not enough for "+expression)
            exit
        guess=full[0 : number - 1 ]
        existing=searchFile(prefix+stringToPath(guess, directoryNameLength )+"."+format)
        if existing : readCRS=getCRS(existing)
    rep=currentCache+"/"+prefix+stringToPath(full[0 : number - 1 ], directoryNameLength )+"."+format
    rep=os.path.expanduser(rep)
    # Create the relevant directory, so that user scripts don't have to care
    dirn=os.path.dirname(rep)
    if not os.path.exists(dirn) : os.makedirs(dirn)
    clogger.debug("returning %s"%rep)
    return(rep)

def stringToPath(name, length) :
    """ Breaks NAME to a path with LENGTH characters-long directory names , for avoiding crowded directories"""
    l=len(name)
    rep=""
    i=0
    while (i + length < l) : 
        rep = rep+name[i:i+length]+"/"
        i   += length
    rep += name[i:l]
    return rep

def searchFile(path):
    """ Search for first occurrence of PATH as a path in all 
    directories listed in CACHEDIRS
    """
    for cdir in cachedirs :
        candidate=os.path.expanduser(cdir+"/"+path)        
        if os.path.lexists(candidate):
            # If this is a broken link, delete it ~ silently and return None
            if not os.path.exists(candidate):
                clogger.debug("Broken link for %s was deleted"%candidate)
                os.remove(candidate)
                return None
            return candidate

def register(filename,crs,outfilename=None):
    """ 
    Adds in FILE a metadata named 'CRS_def' and with value CRS, and a
    metadata 'CLiMAF' with CliMAF version and ref URL

    Records this FILE in dict crs2filename

    If OUTFILENAME is not None, FILENAME is a temporary file and
    it's OUTFILENAME which is recorded in dict crs2filename

    Silently skip non-existing files
    """
    # First read index from file if it is yet empty - No : done at startup
    # if len(crs2filename.keys()) == 0 : cload()
    # It appears that we have to let some time to the file system  for updating its inode tables
    if not stamping :
        clogger.debug('No stamping')
        crs2filename[crs]=filename
        return True 
    waited=0
    while waited < 20 and not os.path.exists(filename) :
        time.sleep(0.1)
        waited += 1
    #time.sleep(0.5)
    if os.path.exists(filename) :
        #while time.time() < os.path.getmtime(filename) + 0.2 : time.sleep(0.2)
        if re.findall(".nc$",filename) : 
            command="ncatted -h -a CRS_def,global,o,c,\"%s\" -a CliMAF,global,o,c,\"CLImate Model Assessment Framework version %s (http://climaf.rtfd.org)\" %s"%\
                (crs,version,filename)
        if re.findall(".png$",filename) :
            crs2=crs.replace("%","\%")
            command="convert -set \"CRS_def\" \"%s\" -set \"CliMAF\" \"CLImate Model Assessment Framework version %s (http://climaf.rtfd.org)\" %s %s.png && mv -f %s.png %s"%\
                (crs2,version,filename,filename,filename,filename)
        if re.findall(".pdf$",filename) :
            tmpfile = str(uuid.uuid4())
            command="pdftk %s dump_data output %s && echo -e \"InfoBegin\nInfoKey: Keywords\nInfoValue: %s\" >> %s && pdftk %s update_info %s output %s.pdf && mv -f %s.pdf %s && rm -f %s"%\
                (filename,tmpfile,crs,tmpfile,filename,tmpfile,filename,filename,filename,tmpfile)
        if re.findall(".eps$",filename) :
            command='exiv2 -M"add Xmp.dc.CliMAF CLImate Model Assessment Framework version %s (http://climaf.rtfd.org)" -M"add Xmp.dc.CRS_def %s" %s'%\
                (version,crs,filename)
        clogger.debug("trying stamping by %s"%command)
        if ( os.system(command) == 0 ) :     
            if outfilename:
                cmd = 'mv -f %s %s '%(filename,outfilename)
                if ( os.system(cmd) == 0 ):
                    clogger.info("move %s as %s "%(filename,outfilename))
                    clogger.info("%s registered as %s"%(crs,outfilename))
                    crs2filename[crs]=outfilename
                    return True
                else:
                    clogger.critical("cannot move by"%cmd)
                    exit()
                    return None
            else:
                clogger.info("%s registered as %s"%(crs,filename))
                crs2filename[crs]=filename
                return True
        else : 
            clogger.critical("cannot stamp by %s"%command)
            exit()
            return None
    else :
        clogger.error("file %s does not exist (for crs %s)"%(filename,crs))

    
def getCRS(filename) :
    """ Returns the CRS expression found in FILENAME's meta-data"""
    import subprocess
    if re.findall(".nc$",filename) : 
        form='ncdump -h %s | grep -E "CRS_def *=" | '+\
            'sed -r -e "s/.*:CRS_def *= *\\\"(.*)\\\" *;$/\\1/" '
    elif re.findall(".png$",filename) :
        form='identify -verbose %s | grep -E " *CRS_def: " | sed -r -e "s/.*CRS_def: *//"'
    elif re.findall(".pdf$",filename) :
        form='pdfinfo %s | grep "Keywords" | awk -F ":" \'{print $2}\' | sed "s/^ *//g"'
    elif re.findall(".eps$",filename) :
        form='exiv2 -p x %s | grep "CRS_def" | awk \'{for (i=4;i<=NF;i++) {print $i " "} }\' '
    else :
        clogger.error("unknown filetype for %s"%filename)
        return None
    command=form%filename
    try:
        rep=subprocess.check_output(command, shell=True).replace('\n','')
        if (rep == "" ) : 
            clogger.error("file %s is not well formed (no CRS)"%filename)
        if re.findall(".nc$",filename) : rep=rep.replace(r"\'",r"'")
    except:
        rep="failed"
    clogger.debug("CRS expression read in %s is %s"%(filename,rep))
    return rep

def rename(filename,crs) :
    """ Rename FILENAME to match CRS. Also updates crs in file and
    crs2filename """
    newfile=generateUniqueFileName(crs, format="nc")
    if newfile :
        l=[ c for c in crs2filename if crs2filename[c] == filename ]
        for c in l : crs2filename.pop(c) 
        os.rename(filename,newfile)
        register(newfile,crs)
        return(newfile)
    
def hasMatchingObject(cobject,ds_func) : 
    """
    If the cache holds a file which represents an object with the
    same nodes as COBJECT and which leaves/datasets, when paired with
    those of COBJECT and applying ds_func, returns an identical (and not
    None) value for all pairs, then returns its filename, its CRS and
    this value (for the first one in dict crs2filename)

    Can be applied for finding same object with included or including
    time-period
    """
    # First read index from file if it is yet empty - No : done at startup
    # if len(crs2filename.keys()) == 0 : cload()
    def op_squeezes_time(operator):
        return not operators.scripts[operator].flags.commuteWithTimeConcatenation 
    #
    global crs2eval
    key_to_rm=list()
    for crs in crs2filename :
        co=crs2eval.get(crs,None)
        if co is None:
            try: 
                co=eval(crs, sys.modules['__main__'].__dict__)
                if co: crs2eval[crs]=co
            except:
                pass # usually case of a CRS which project is not currently defined
        if co :
            altperiod=compare_trees(co,cobject, ds_func,op_squeezes_time)
            if altperiod :
                if os.path.exists(crs2filename[crs]) :
                    return co,altperiod
                else :
                    clogger.debug("Removing %s from cache index, because file is missing",crs)
                    key_to_rm.append(crs)
    for el in key_to_rm: crs2filename.pop(el)
    return None,None

def hasIncludingObject(cobject) :
    def ds_period_difference(includer,included):
        if includer.buildcrs(period="") == included.buildcrs(period="") :
            return includer.period.includes(included.period)
    clogger.debug("search for including object for "+`cobject`)
    return hasMatchingObject(cobject,ds_period_difference)

def hasBeginObject(cobject) :
    def ds_period_begins(begin,longer):
        if longer.buildcrs(period="") == begin.buildcrs(period="") :
            return longer.period.start_with(begin.period)
    return hasMatchingObject(cobject,ds_period_begins)

def hasExactObject(cobject) :
    # First read index from file if it is yet empty
    # NO! : done at startup - if len(crs2filename.keys()) == 0 : cload()
    f=crs2filename.get(cobject.crs,None)
    if f:
        if os.path.exists(f) :
            return f
        else :
            clogger.debug("Dropping cobject.crs from cache index, because file si missing")
            crs2filename.pop(cobject.crs)
    
def complement(crsb, crse, crs) :
    """ Extends time period of file object of CRSB (B for 'begin')
    with file object of CRSE (E for 'end') for creating file object of
    CRS. Assumes that everything is OK with args compatibility and
    file contents
    """
    fileb=crs2filename[crsb]
    filee=crs2filename[crse]
    filet=generateUniqueFileName(crs)
    command="ncrcat -O %s %s %s"%(fileb,filee,filet)
    if ( os.system(command) != 0 ) :
        clogger.error("Issue when merging %s and %s in %s (using command:%s)"%\
                          (crsb,crse,crs,command))
        return None
    else :
        cdrop(crsb) ; cdrop(crse)
        register(filet,crs)
        return filet

def cdrop(obj, rm=True) :
    """
    Deletes the cached file for a CliMAF object, if it exists

    Args:
     obj (cobject or string) : object to delete, or its string representation (CRS)

     rm (bool) : for advanced use only; should we actually delete (rm) the file, or just forget it in CliMAF cache index
    
    Returns:
     None if object does not exists, False if failing to delete, True if OK

    Example ::

    >>> dg=ds(project='example', simulation='AMIPV6ALB2G', variable='tas', period='1980-1981')
    >>> f=cfile(dg)
    >>> os.system('ls -al '+f)
    >>> cdrop(dg)
    
    """
    global crs2filename

    if (isinstance(obj,cobject) ):
        crs=`obj`
        if (isinstance(obj, cdataset) ) : crs="select("+crs+")"
    elif type(obj) is str : crs=obj
    else :
        clogger.error("%s is not a CliMAF object"%`obj`)
        return
    if crs in crs2filename :
        clogger.info("discarding cached value for "+crs)
        fil=crs2filename.pop(crs)
        if rm :
            try :
                path_file=os.path.dirname(fil)
                os.remove(fil)
                try:
                    os.rmdir(path_file)
                except OSError as ex:
                    clogger.warning(ex)
                
                return True
            except:
                clogger.warning("When trying to remove %s : file does not exist in cache"%crs)
                return False
    else :
        clogger.info("%s is not cached"%crs)
        return None

def csync(update=False) :
    """
    Merges current in-memory cache index and current on-file cache index 
    for updating both

    If arg `update` is True, additionnaly ensures consistency between files
    set and index content, either :

    - if cache.stamping is true, by reading CRS in all files
    - else, by removing files which are not in the index; this may erase 
      result files which have been computed by another running 
      instance of CliMAF
    """
    #
    import pickle
    global cacheIndexFileName

    # Merge index on file and index in memory
    file_index=cload(True)
    crs2filename.update(file_index)

    # check if cache index is up to date; if not
    # enforce consistency
    if update :
        clogger.info("Listing crs from files present in cache")
        files_in_cache=list_cache()
        files_in_cache.sort()
        files_in_index=crs2filename.values()
        files_in_index.sort()
        if files_in_index != files_in_cache:
            if stamping :
                clogger.info("Rebuilding cache index from file content")
                rebuild()
            else :
                clogger.info('Removing cache files which content is not known')
                for fil in files_in_cache :
                    if fil not in files_in_index :
                        os.system("rm %"%fil)
                    #else :
                    # Should also remove empty files, as soon as
                    # file creation will be atomic enough 
    # Save to disk
    try: 
        cacheIndexFile=file(os.path.expanduser(cacheIndexFileName), "w")
        pickle.dump(crs2filename,cacheIndexFile)  
        cacheIndexFile.close()
    except:
        clogger.info("No cache index file yet")

def cload(alt=None) :
    global crs2filename 
    global crs_not_yet_evaluable
    rep=dict()
 
    if len(crs2filename) != 0 and not alt:
        Climaf_Cache_Error(
            "attempt to reset file index - would lead to inconsistency !")
    try :
        cacheIndexFile=file(os.path.expanduser(cacheIndexFileName), "r")
        if alt :
            rep=pickle.load(cacheIndexFile)
        else:
            crs2filename=pickle.load(cacheIndexFile)
        cacheIndexFile.close()
    except:
        pass
        #clogger.debug("no index file yet")
    #
    must_check_index_entries=False
    if (must_check_index_entries) :
        # We may have some crs inherited from past sessions and for which
        # some operator may have become non-standard, or some projects are yet 
        # undeclared
        crs_not_yet_evaluable=dict()
        allow_error_on_ds()
        for crs in crs2filename.copy() :
            try :
                #print "evaluating crs="+crs
                eval(crs, sys.modules['__main__'].__dict__)
            except:
                print ("Inconsistent cache object is skipped : %s"%crs)
                #clogger.debug("Inconsistent cache object is skipped : %s"%crs)
                p=guess_projects(crs)
                if p not in crs_not_yet_evaluable : crs_not_yet_evaluable[p]=dict()
                crs_not_yet_evaluable[p][crs]=crs2filename[crs]
                crs2filename.pop(crs)
                # Analyze projects of inconsistent cache objects
                projects= crs_not_yet_evaluable.keys()
                if projects :
                    clogger.info( 
                        "The cache has %d objects for non-declared projects %s.\n"
                        "For using it, consider including relevant project(s) "
                        "declaration(s) in ~/.climaf and restarting CliMAF.\n"
                        "You can also declare these projects right now and call 'csync(True)'\n"
                        "Or you can erase corresponding data by 'crm(pattern=...project name...)'"% \
                        (len(crs_not_yet_evaluable),`list(projects)`))
        allow_error_on_ds(False)
    if alt :
        return rep
        

def cload_for_project(project):
    """
    Append to the cache index dict those left index entries for 'project' which evaluate successfully
    """
    d=crs_not_yet_evaluable[project]
    for crs in d.copy() :
        try :
            #print "evaluating crs="+crs
            eval(crs, sys.modules['__main__'].__dict__)
            crs2filename[crs]=d[crs]
            d.pop(crs)
        except:
            clogger.error("CRS expression %s is not valid for project %s"%(crs,project))
         
def craz(hideError=False) :
    """
    Clear CliMAF cache : erase existing files content, reset in-memory index

    Args:
      hideError (bool): if True, will not warn for non existing cache

    """
    global crs2filename
    cc=os.path.expanduser(currentCache)
    if (os.path.exists(currentCache) or hideError is False) :
        os.system("rm -fR "+cc+"/*")
        os.system("ls  "+cc)
    #for f in crs2filename : os.remove(crs2filename[f])
    #if os.path.exists(cacheIndexFileName) : os.remove(cacheIndexFileName)
    crs2filename=dict()

def cdump(use_macro=True):
    """
    List the in-memory content of CliMAF cache index. Interpret it
    using macros except if arg use_macro is False
    
    """
    for crs in crs2filename :
        if not use_macro :
            # No interpretation by macros
            #print "%s : %s"%(crs2filename[crs][-30:],crs)
            print "%s : %s"%(crs2filename[crs],crs)
        else:
            # Must update for new macros
            print "%s : %s"%(crs2filename[crs],crewrite(crs))

def list_cache():
    """
    Return the list of files in cache directories, using `find`
    
    """
    files_in_cache=[]
    find_return=""
    for dir_cache in cachedirs :
        rep=os.path.expanduser(dir_cache)
        find_return+=os.popen("find %s -type f \( -name '*.png' -o -name '*.nc' -o -name '*.pdf' -o -name '*.eps' \) -print" %rep).read()
    files_in_cache=find_return.split('\n')
    files_in_cache.pop(-1)
    return(files_in_cache)

def clist(size="", age="", access=0, pattern="", not_pattern="", usage=False, count=False,
          remove=False, CRS=False, special=False):
    """
    Internal function used by its front-ends : :py:func:`~climaf.cache.cls`, :py:func:`~climaf.cache.crm`,
    :py:func:`~climaf.cache.cdu`, :py:func:`~climaf.cache.cwc`

    List the content of CliMAF cache according to some search criteria
    and operate possibly an action (usage, count or remove) on this list.

    Please consider the cost and benefit of first updating CliMAF cache index (by scanning
    files on disk) using :py:func:`csync()`
    
    Args:
     size (string, optional): n[ckMG]     
      Search files using more than n units of disk space, rounding up.
      The following suffixes can be used:

        - "c"    for bytes (default)
        - "k"    for Kilobytes (units of         1,024 bytes)
        - "M"    for Megabytes (units of     1,048,576 bytes)
        - "G"    for Gigabytes (units of 1,073,741,824 bytes)

     age (string, optional): Number of 24h periods. Search files which
      status was last changed n*24 hours ago.
      Any fractional part is ignored, so to match age='+1', a file has
      to have been changed at least two days ago.
      Numeric arguments can be specified as:
      
        - `+n`   for greater than n
        - `-n`   for less than n,
        - `n`    for exactly n.

     access (int, optional): n 
      Search files which were last accessed more than n*24 hours ago. Any
      fractional part is ignored, so to match access='1', a file has to
      have been accessed at least two days ago.

     pattern (string, optional): Scan through crs and filenames looking for
      the first location where the regular expression pattern produces a match. 

     not_pattern (string, optional): Scan through crs and filenames looking
      for the location where the regular expression not_pattern does not
      produce a match. 
        
     usage (bool, optional): Estimate found files space usage, for each
      found file and total size. If count is True, estimate only found
      files total space usage.

     count (bool, optional): Return the number of found files. If CRS is True,
      also return crs of found files.
        
     remove (bool, optional): Remove the found files. This argument is exclusive.
        
     CRS (bool, optional): if True, print also CRS expression. Useful only
      if count is True.


    Return:
      The dictionary corresponding to the request and associated action ( or dictionary
      of CliMAF cache index if no argument is provided)

     Example to search files using more than 3M of disk space, which status
      was last changed more than 15 days ago and containing the pattern
      '1980-1981' either in crs or filename. For found files, we want to
      estimate only found files total space usage::
     
      >>> clist(size='3M', age='+15', pattern= '1980-1981', usage=True, count=True)

    """

    #cache directories
    rep=os.path.expanduser(cachedirs[0]) #TBD: le cache ne contient qu un rep pr le moment => voir pour boucler sur tous les caches

    #command for research on size/age/access
    command=""
    opt_find=""
    if size :
        if re.search('[kMG]', size) is None :  
            opt_find+="-size +%sc "%size  
        else:
            opt_find+="-size +%s "%size
    if age :
        opt_find+="-ctime %s "%age
    if access !=0 :
        opt_find+="-atime +%s"%str(int(access))
                
    var_find=False
    if size or age or access != 0 :
        var_find=True
        command="find %s -type f \( -name '*.png' -o -name '*.nc' -o -name '*.pdf' -o -name '*.eps' \) %s -print" %(rep, opt_find) 
        clogger.debug("Find command is :"+command)

        #construction of the new dictionary after research on size/age/access
        new_dict=dict()
        find_return=""
        list_search_files_after_find=[]

        find_return=os.popen(command).read()
        list_search_files_after_find=find_return.split('\n')
        list_search_files_after_find.pop(-1)
        clogger.debug("List of search files: "+`list_search_files_after_find`)

        # Search CRS for each found file
        for filen in list_search_files_after_find :
            for crs in crs2filename:
                if crs2filename[crs]==filen:
                    new_dict[crs]=filen
                    
        if len(new_dict) != 0 :
            if new_dict != crs2filename :
                clogger.debug("Dictionary after find for size/age/access: "+`new_dict`)
            else : 
                clogger.debug("Size/age/access criteria do not lead to any filtering")
        else :
            clogger.debug("No file meet the size/age/access criteria")
    else:
        new_dict=crs2filename.copy()

    #size of new dictionary
    len_new_dict=len(new_dict)

    #filter on pattern
    find_pattern=False
    if pattern :
        list_crs_to_rm=[]
        for crs in new_dict :
            if re.search(pattern, crewrite(crs)) or re.search(pattern, new_dict[crs]):
                clogger.debug("Pattern found in %s: %s"%(crs,new_dict[crs]))
                find_pattern=True
            else:
                # Do not remove now from new_dict, because we loop on it
                list_crs_to_rm.append(crs)
        for crs in list_crs_to_rm :
            del new_dict[crs]
    
        if find_pattern :
            clogger.debug("Dictionary after search for pattern: "+`new_dict`)
        elif len_new_dict!=0 :
            clogger.debug("No string found for pattern => no result")
       
    #update size new dictionary
    len_new_dict=len(new_dict)
    
    #research on not_pattern  
    find_not_pattern=False  
    if not_pattern:
        list_crs_to_rm=[]
        for crs in new_dict :
            if re.search(not_pattern, crewrite(crs)) is None and \
               re.search(not_pattern, new_dict[crs]) is None :
                clogger.debug("Pattern not found in %s: %s"%(crs, new_dict[crs]))
                find_not_pattern=True
            else:
                list_crs_to_rm.append(crs)
        for crs in list_crs_to_rm :
            del new_dict[crs]
        
        if find_not_pattern :
            clogger.debug("Dictionary after search for not_pattern: "+`new_dict`)
        elif  len_new_dict!=0 :
            clogger.debug("All strings contain not_pattern => no result")
            
    #update size new dictionary
    len_new_dict=len(new_dict)

    #request on new dictionary through usage, count and remove
    work_dic=new_dict if (var_find or pattern is not "" or not_pattern is not "") else crs2filename
    
    if usage is True and len_new_dict != 0 :
        #construction of a dictionary containing crs and disk-usage associated
        dic_usage=dict()
        tmp=""
        for crs in work_dic :
            tmp+=work_dic[crs]+" "
        res=os.popen("du -sc %s"%tmp).read()
        
        regex=re.compile('([0-9]+)\t')
        list_size=re.findall(regex,res)
        regex2=re.compile('([0-9]+\t)')
        str_path=regex2.sub('',res)
        list_fig=str_path.split('\n')
        list_fig.pop(-1)
    
        for fig,size in zip(list_fig,list_size): 
            if fig!="total":
                for crs in work_dic:
                    if fig==work_dic[crs]:
                        dic_usage[crs]=size 
            else:
                dic_usage[fig]=size

        #sort of usage dictionary and units conversion
        du_list_sort=dic_usage.items()
        du_list_sort.sort(key=itemgetter(1),reverse=False)
        
        unit=["K","M","G","T"]
        for n,pair in enumerate(du_list_sort):
            i=0
            flt=float(pair[1])
            while flt >= 1024. and i < 4:
                flt/=1024.
                i+=1
            du_list_sort[n]=(du_list_sort[n][0],"%6.1f%s"%(flt,unit[i]))
            
        if count is True : # Display total volume of found files
            for fig, size in du_list_sort:
                if fig=="total":              
                    print "%7s : %s" %(size,fig)  
            
        else: #retrieve disk-usage of each found file and total volume
            for fig,size in du_list_sort:
                print "%7s : %s" %(size,fig)
        
    elif count is True and len_new_dict != 0 :
        print "Number of files found:", len(work_dic)
        if CRS is True:
            for crs in work_dic : print crs
        
    elif remove is True and len_new_dict != 0 :
        print "Removed files:"
        list_tmp_crs=[]
        list_tmp_crs=new_dict.keys() if (var_find or pattern is not "" or not_pattern is not "") else crs2filename.keys() 
        for crs in list_tmp_crs:
            cdrop(crs, rm=True)
        return(map(crewrite,list_tmp_crs))
                
    else: #usage, count and remove are False
        if var_find or pattern is not "" or not_pattern is not "" :
            if len(new_dict) != 0 : 
                if new_dict != crs2filename :
                    print "Filtered objects :"
                else :
                    print "Filtered objects = cache content"
                return (map(crewrite,new_dict.keys()))
            #else : print "No matching file "    
        else:
            print "Content of CliMAF cache"
            return (map(crewrite,crs2filename.keys()))

    #TBD
    if special is True :
        global dic_special
        dic_special=dict()
        if var_find is True or pattern is not "" or not_pattern is not "" :
            dic_special=new_dict.copy()
        else: 
            dic_special=crs2filename.copy()
        print "List of marked figures as 'special'", dic_special.values()
        return(dic_special) #TBD: declarer comme var globale et enlever son effacement dans creset

    new_dict.clear()

def cls(**kwargs):
    """
    List CliMAF cache objects. Synonym to clist(). See :py:func:`~climaf.cache.clist`
   
    """
    return clist(**kwargs)

def crm(**kwargs):
    """
    Remove the cache files found by 'clist()' when using same arguments.
    See :py:func:`~climaf.cache.clist`

    Example to remove files using more than 3M of disk space, which status
    was last changed more than 15 days ago and containing the pattern
    '1980-1981' either in crs or filename::
     
     >>> crm(size='3M', age='+15', pattern='1980-1981')

    """
    kwargs['remove']=True
    kwargs['usage']=False
    kwargs['count']=False
    return clist(**kwargs)

def cdu(**kwargs):
    """
    Report disk usage, for files matching some criteria, as specified
    for :py:func:`~climaf.cache.clist`. With count=True, report only total disk usage.

    Example to search files using more than 3M of disk space, which status
    was last changed more than 15 days ago and containing the pattern '1980-1981'
    either in crs or filename. For found files, we want to
    estimate only found files total space usage::
     
      >>> cdu(size='3M', age='+15', pattern= '1980-1981', count=True)
    
    """
    kwargs['usage']=True 
    kwargs['remove']=False
    return clist(**kwargs)

def cwc(**kwargs):
    """
    Report number of cache files matching some criteria, as specified
    for :py:func:`~climaf.cache.clist`. If CRS is True, also return CRS expression
    of found files.

    Example to return the number and crs associated of files using more
    than 3M of disk space, which status was last changed more than 15
    days ago and containing the pattern '1980-1981' either in crs or
    filename::
     
     >>> cwc(size='3M', age='+15', pattern= '1980-1981', CRS=True)

    """
    kwargs['count']=True
    kwargs['remove']=False
    kwargs['usage']=False 
    return clist(**kwargs)

def rebuild():
    """
    Rebuild the in-memory content of CliMAF cache index
    
    """
    global crs2filename

    if not stamping :
        clogger.warning("Cannot rebuild cache index, because we are not in 'stamping' mode")
        return None
    files_in_cache=list_cache()
    crs2filename.clear()
    for files in files_in_cache:
        filecrs=getCRS(files)
        if filecrs:
            crs2filename[filecrs]=files
        else:
            os.system('rm -f '+files)
            clogger.warning("File %s is removed"%files)
    return(crs2filename)
    

class Climaf_Cache_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)
    def __str__(self):
        return `self.valeur`
