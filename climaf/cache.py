""" CliMAF cache module : stores and retrieves CliMAF objects from their CRS expression.

"""
# Created : S.Senesi - 2014

import sys, os, os.path, re, time, glob
from climaf.classes import compare_trees

from clogging import clogger
import subprocess
import climaf

cpath=os.path.abspath(climaf.__path__[0])

directoryNameLength=2
DynamicIsOn=False
currentCache=None
cachedirs=None
crs2filename=dict()

def setNewUniqueCache(path) :
    """ Define PATH as the sole cache to use from now. And clear it 

    """
    global currentCache
    global cachedirs
    global cacheIndexFileName
    
    cachedirs=[ path ] # The list of cache directories
    crs2filename=dict()  # The index associating filenames to CRS expressions
    cacheIndexFileName = cachedirs[0]+"/index"  # The place to write the index
    currentCache=cachedirs[0]
    creset(hideError=True)

#def generateUniqueFileName(expression, operator=climaf.classes.firstGenericDataSet):
def generateUniqueFileName(expression, operator=None, format="nc"):
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
    import hashlib
    #
    if format==None : return ""
    prefix=""
    if operator is not None :
        prefix2=operator(expression)
        if prefix2 is not None : prefix=prefix2+"/"
    full=hashlib.sha224(expression).hexdigest()
    number=4
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
        readCRS=getCRS(existing)
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
    """ Search for first occurrence of PATH as a path in all directories listed in CACHEDIRS"""
    for cdir in cachedirs :
        candidate=os.path.expanduser(cdir+"/"+path)        
        if os.path.exists(candidate): return candidate

def register(filename,crs):
    """ Adds in FILE a metadata named CRS_def and with value CRS. Records this FILE in dict crs2filename

    Silently skip non-existing files
    """
    # First read index from file if it is yet empty
    if len(crs2filename.keys()) == 0 : cload()
    # It appears that we have to allow the file system some time for updating its inode tables
    waited=0
    while waited < 10 and not os.path.exists(filename) :
        time.sleep(0.5)
        waited += 1
    time.sleep(0.5)
    if os.path.exists(filename) :
        #while time.time() < os.path.getmtime(filename) + 0.2 : time.sleep(0.2)
        if re.findall(".nc$",filename) : 
            command="ncatted -h -a CRS_def,global,o,c,\"%s\" %s"%(crs,filename)
        if re.findall(".png$",filename) :
            command="convert -set \"CRS_def\" \"%s\" %s %s.png && mv -f %s.png %s"%\
                (crs,filename,filename,filename,filename)
        clogger.debug("trying stamping by %s"%command)
        if ( os.system(command) == 0 ) :
            crs2filename[crs]=filename
            clogger.info("%s registered as %s"%(crs,filename))
            return True
        else : 
            clogger.critical("cannot stamp by %s"%command)
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
    else :
        clogger.critical("unknown filetype for %s"%filename)
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
        for c in l : del(crs2filename[c]) 
        os.rename(filename,newfile)
        register(newfile,crs)
        return(newfile)
    
def hasMatchingObject(cobject,ds_func) : 

    """ if the cache holds a file which represents an object with the
    same nodes as COBJECT and which leaves/datasets, when paired with
    those of COBJECT and applying ds_func, returns an identical not
    None value for all pairs, then returns its filename, its CRS and
    this value (for the first one in dict crs2filename

    Can be applied for finding same object with included or including
    time-period
    """
    # First read index from file if it is yet empty
    if len(crs2filename.keys()) == 0 : cload()
    def op_squeezes_time(operator):
        import operators
        return operators.scripts[operator].flags.doSqueezeTime 
    #
    for crs in crs2filename :
        co=eval(crs, sys.modules['__main__'].__dict__)
        altperiod=compare_trees(co,cobject, ds_func,op_squeezes_time)
        if altperiod : return co,altperiod
    return None,None

def hasIncludingObject(cobject) :
    def ds_period_difference(includer,included):
        if includer.buildcrs("") == included.buildcrs("") :
            return includer.period.includes(included.period)
    clogger.debug("search for including object for "+`cobject`)
    return hasMatchingObject(cobject,ds_period_difference)

def hasBeginObject(cobject) :
    def ds_period_begins(begin,longer):
        if longer.buildcrs("") == begin.buildcrs("") :
            return longer.period.start_with(begin.period)
    return hasMatchingObject(cobject,ds_period_begins)

def hasExactObject(cobject) :
    # First read index from file if it is yet empty
    if len(crs2filename.keys()) == 0 : cload()
    if cobject.crs in crs2filename :
        return (crs2filename[cobject.crs])

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

def cdrop(crs, rm=True) :
    """ Deletes a cached file for a given CliMAF Reference Syntax expression, if it exists

    Returns None if it does not exists, False if delete is unsuccessful, True if OK    """
    if crs in crs2filename :
        clogger.info("discarding cached value for "+crs)
        try :
            if rm : os.remove(crs2filename[crs])
            crs2filename.pop(crs)
            return True
        except:
            return False
    else :
        clogger.error("%s is not cached"%crs)
        return None

def csync() :
    """
    Writes in-memory cache dictionnary to disk ; should be called before exit

    """
    import pickle
    cacheIndexFile=file(os.path.expanduser(cacheIndexFileName), "w")
    pickle.dump(crs2filename,cacheIndexFile)  
    cacheIndexFile.close()

def cload() :
    import pickle
    global crs2filename #pb sans cette declaration
    if len(crs2filename) != 0 :
        clogger.critical("attempt to reset file index - would lead to inconsistency !")
        return 
    try :
        cacheIndexFile=file(os.path.expanduser(cacheIndexFileName), "r")
        crs2filename=pickle.load(cacheIndexFile)
        cacheIndexFile.close()
    except:
        clogger.debug("no index file yet")

def creset(hideError=False) :
    """
    Clear CliMAF cache : erase existing files content, reset in-memory index

    Args:
      hideError (bool): if True, will not warn for non existing cache

    """
    cc=os.path.expanduser(currentCache)
    if (os.path.exists(currentCache) or hideError is False) :
        os.system("rm -fR "+cc+"/*")
        os.system("ls  "+cc)
    #for f in crs2filename : os.remove(crs2filename[f])
    #if os.path.exists(cacheIndexFileName) : os.remove(cacheIndexFileName)
    crs2filename=dict()

def cdump():
    """
    Dumps the in-memory content of CliMAF cache index
    
    """
    for crs in crs2filename :
        #print "%s : %s"%(crs2filename[crs][-30:],crs)
        print "%s : %s"%(crs2filename[crs],crs)

def list_cache():
    """
    Return the list of files in cache directories
    
    """
    files_in_cache=[]
    find_return=""
    for dir_cache in cachedirs :
        rep=os.path.expanduser(dir_cache)
        find_return+=os.popen("find %s -type f \( -name '*.png' -o -name '*.nc' \) -print" %rep).read()
    files_in_cache=find_return.split('\n')
    files_in_cache.pop(-1)
    return(files_in_cache)

def clist(size="", age="", access=0, pattern="", not_pattern="", usage=False, CRS= False, count=False, remove=False, special=False):
    """
    TBD 
    List the content of CliMAF cache according to some selection criteria
    
    """

    #check if cache index is up to date, if it is not the function 'rebuild' is called
    files_in_cache=list_cache()
    files_in_cache.sort()
    index_keys=crs2filename.values()
    index_keys.sort()
    if files_in_cache != index_keys:
        clogger.info("Rebuild of index crs2filename")
        rebuild()  

    #cache directories
    rep=os.path.expanduser(cachedirs[0]) #TBD: le cache ne contient qu un rep pr le moment => voir pour boucler sur tous les caches

    #command for research on size/age/access
    command=""
    opt_find=""
    if size :
        if re.search('[kMG]', size) is None : #unite par defaut = bloc de 512 octets (option b)
            opt_find+="-size +%sc "%size  #octets
        else:
            opt_find+="-size +%s "%size
    if age : #age=+/-nbre_jours
        opt_find+="-ctime %s "%age
    if access !=0 :
        opt_find+="-atime +%s"%str(int(access))
                
    var_find=False
    if size or age or access != 0 :
        var_find=True
        command="find %s -type f \( -name '*.png' -o -name '*.nc' \) %s -print" %(rep, opt_find)
        clogger.debug(command)
        
    #construction of the new dictionnary after research on size/age/access
    new_dict=dict()
    if var_find is True:
        find_return=""
        list_search_files_after_find=[]

        find_return=os.popen(command).read()
        list_search_files_after_find=find_return.split('\n')
        list_search_files_after_find.pop(-1)
        clogger.debug("List of search files: "+`list_search_files_after_find`)

        for filen in list_search_files_after_find :
            for crs in crs2filename:
                if crs2filename[crs]==filen:
                    new_dict[crs]=filen
                    
        if len(new_dict) != 0 and new_dict != crs2filename :
            clogger.debug("Dictionnary after find for size/age/access: "+`new_dict`)
        elif new_dict == crs2filename:
            clogger.debug("Dictionnary unchanged after find for size/age/access")
        elif len(new_dict) == 0 :
            clogger.debug("No files found after find for size/age/access => no result")
    else:
        new_dict=crs2filename.copy()

    #size new dictionnary
    len_new_dict=len(new_dict)

    #research on pattern
    find_pattern=False
    if pattern :
        if len_new_dict != 0: 
            list_crs_to_rm=[]
            for crs in new_dict :
                if re.search(pattern, crs) or re.search(pattern, new_dict[crs]):
                    clogger.debug("String found in %s: %s"%(crs,new_dict[crs]))
                    find_pattern=True
                else:
                    list_crs_to_rm.append(crs)
            for crs in list_crs_to_rm :
                del new_dict[crs]
    
            if find_pattern is True :
                clogger.debug("Dictionnary after search for pattern: "+`new_dict`)
            elif find_pattern is False and len_new_dict!=0 :
                clogger.debug("No string found for pattern => no result")
       
    #update size new dictionnary
    len_new_dict=len(new_dict)
    
    #TBD si la var find_not_pattern est utile par la suite
    #research on not_pattern      
    find_not_pattern=False  
    if not_pattern:
        if len_new_dict != 0: 
            list_crs_to_rm=[]
            for crs in new_dict :
                if re.search(not_pattern, crs) is None and re.search(not_pattern, new_dict[crs]) is None:
                    clogger.debug("String not found in %s: %s"%(crs, new_dict[crs]))
                    find_not_pattern=True
                else:
                    list_crs_to_rm.append(crs)
            for crs in list_crs_to_rm :
                del new_dict[crs]
        
            if find_not_pattern is True :
                clogger.debug("Dictionnary after search for not_pattern: "+`new_dict`)
            elif find_not_pattern is False and len_new_dict!=0 :
                clogger.debug("All strings contain not_pattern => no result")
            
    #update size new dictionnary
    len_new_dict=len(new_dict)

    #request on new dictionnary through usage, count and remove
    work_dic=new_dict.copy() if (var_find is True or pattern is not "" or not_pattern is not "") else crs2filename.copy()
        
    if usage is True and len_new_dict != 0 :
        tmp=""
        for crs in work_dic :
            tmp+=work_dic[crs]+" "
        res=os.popen("du -sc %s | awk '{print $1}' | tail -n1"%tmp).read() #result in Ko
        tot_volume=float(res)

        unit=["K","M","G","T"]
        i=0
        while tot_volume >= 1024. and i < 4:
            tot_volume/=1024.
            i+=1
        
        if count is True : #count total volume of found files
            print "%4.1f%s : total" %(tot_volume, unit[i])

        else: #count volume of each found files and total volume
            for crs in work_dic :
                res=os.popen("du -sh %s | awk '{print $1}'"%work_dic[crs]).read().replace('\n','')
                print "%5s : %s" %(res, crs)
            print "%4.1f%s : total" %(tot_volume, unit[i])
            
    elif count is True and len_new_dict != 0 :
        print "Files found:", len(work_dic)
        if CRS is True:
            for crs in work_dic :
                print crs
        
    elif remove is True and len_new_dict != 0 :
        print "Removed files:"
        list_tmp_crs=[]
        list_tmp_crs=new_dict.keys() if (var_find is True or pattern is not "" or not_pattern is not "") else crs2filename.keys() 
        for crs in list_tmp_crs:
            cdrop(crs, rm=True)
                
    else: #usage, count et remove are False
        if var_find is True or pattern is not "" or not_pattern is not "" :
            if len(new_dict) != 0 : 
                if new_dict != crs2filename :
                    print "Final content of CliMAF cache"
                if new_dict == crs2filename :
                    print "Final content of CliMAF cache : similar to initial"
                for crs in new_dict :
                    print crs
            elif len(new_dict) == 0  :
                print "Result for research: empty"    
        else:
            print "Content of CliMAF cache"
            for crs in crs2filename :
                print crs

    work_dic.clear()

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
    TBD
    
    """
    clist(**kwargs)

def crm(**kwargs):
    """
    TBD 
    
    """
    kwargs['remove']=True
    kwargs['usage']=False
    kwargs['count']=False
    clist(**kwargs)

def cdu(**kwargs):
    """
    TBD 
    
    """
    kwargs['usage']=True 
    kwargs['remove']=False
    clist(**kwargs)

def cwc(**kwargs):
    """
    TBD
    
    """
    kwargs['count']=True
    kwargs['remove']=False
    return clist(**kwargs)

def rebuild():
    """
    Rebuild the in-memory content of CliMAF cache index
    
    """
    files_in_cache=list_cache()
    crs2filename.clear()
    for files in files_in_cache:
        crs2filename[getCRS(files)]=files

    return(crs2filename)
    

if __name__ == "__main__":
    cachedirs=[ "~/tmp/climaf_cache" ]
    e=getCRS("~/tmp/climaf_cache/test_expressionOf")
    searchFile("test_expressionOf") 
    stringToPath("aerzed",4)    
    print generateUniqueFileName("azertyuiop")


# Todo :

# a function for restoring the index from directory content, in case it has not been written on disk at the end of a session, or it is broken n some other way
