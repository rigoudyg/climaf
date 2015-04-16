""" CliMAF cache module : stores and retrieves CliMAF objects from their CRS expression.

"""
# Created : S.Senesi - 2014

import sys, os, os.path, re, time
from climaf.classes import compare_trees

from clogging import clogger
import subprocess
import climaf

cpath=os.path.abspath(climaf.__path__[0])

directoryNameLength=2
DynamicIsOn=False
currentCache=None
cachedirs=None

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
    global crs2filename
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
    global crs2filename
    global dic_special
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

def cls(size=0, age=0, access=0, filtre="", notfilter="", usage=False, filename= False, count=False, remove=False, special=False):
    """
    A completer List 
    
    """
    crs_list=[]
    crs2filename_list=[]
    print crs2filename
    for crs in crs2filename :
        print crs
        crs_list.append(crs)
        crs2filename_list.append(crs2filename[crs])

    print crs2filename_list
    print "fin des test d impression"

    #conversion unites attention a la division par zero
    if size != 0 :#pr le moment hypothese de la taille en nbre octets (unite= bloc de 512 octets)
        nb_blocs=size/512.
    if age != 0 :#pr le moment hypothese de l age en nombre d heures (unite=bloc de 24h-1jour)
        nb_jours=age/24.
    if access != 0 :#pr le moment hypothese de l acces en nombre d heures (unite=bloc de 24h-1jour)
        nb_j_acc=access/24.

    #commande pour la recherche sur size/age/access
    command=""
    sortie_find=""
    list_search_files=[]
    
    #regarder pour sortir de la boucle des qu on est ds un cas ?
    if size != 0 :
        if age != 0 :
            if access != 0 :
                #command="find "+cpath+"/../../tmp/climaf_cache/*/* -size +"+str(int(nb_blocs))+" -ctime +"+str(int(nb_jours))+" -atime +"+str(int(nb_j_acc))+" -print"
                command="find %s/../../tmp/climaf_cache/*/* -size +%s -ctime +%s -atime +%s -print" %(cpath, str(int(nb_blocs)), str(int(nb_jours)), str(int(nb_j_acc)))                
                print "recherche sur size + age + access"
            else :
                #command="find "+cpath+"/../../tmp/climaf_cache/*/* -size +"+str(int(nb_blocs))+" -ctime +"+str(int(nb_jours))+" -print"
                command="find %s/../../tmp/climaf_cache/*/* -size +%s -ctime +%s -print" %(cpath, str(int(nb_blocs)), str(int(nb_jours))) 
                print "recherche sur size + age"
        elif age == 0 and access != 0 : #age=0 a preciser ?
            #command="find "+cpath+"/../../tmp/climaf_cache/*/* -size +"+str(int(nb_blocs))+" -atime +"+str(int(nb_j_acc))+" -print"
            command="find %s/../../tmp/climaf_cache/*/* -size +%s -atime +%s -print" %(cpath, str(int(nb_blocs)), str(int(nb_j_acc)))      
            print "recherche sur size + access"
        elif age ==0 and access == 0 : #age=0 a preciser ?
            #command="find "+cpath+"/../../tmp/climaf_cache/*/* -size +"+str(int(nb_blocs))+" -print"
            command="find %s/../../tmp/climaf_cache/*/* -size +%s -print" %(cpath, str(int(nb_blocs)))
            print "recherche sur size" 
    elif size == 0 and age != 0 : #size=0 a preciser ?
        if access != 0 :
            #command="find "+cpath+"/../../tmp/climaf_cache/*/* -ctime +"+str(int(nb_jours))+" -atime +"+str(int(nb_j_acc))+" -print"
            command="find %s/../../tmp/climaf_cache/*/* -ctime +%s -atime +%s -print" %(cpath, str(int(nb_jours)), str(int(nb_j_acc)))
            print "recherche sur age + access"
        else:
            #command= "find "+cpath+"/../../tmp/climaf_cache/*/* -ctime +"+str(int(nb_jours))+" -print"
            command="find %s/../../tmp/climaf_cache/*/* -ctime +%s -print" %(cpath, str(int(nb_jours)))
            print "recherche sur age"
    elif size == 0 and age == 0 : #size=0 a preciser ?
        if access != 0 :
            #command="find "+cpath+"/../../tmp/climaf_cache/*/* -atime +"+str(int(nb_j_acc))+" -print"
            command="find %s/../../tmp/climaf_cache/*/* -atime +%s -print" %(cpath, str(int(nb_j_acc)))
            print "recherche sur access"
            
    print command
    
    var_find=False
    if size != 0 or age != 0 or access != 0 :
        var_find=True

    #new_dict_crs2filename=dict()
    if var_find is True:
        new_dict_crs2filename=dict()
        sortie_find=os.popen(command).read()
        #os.system(command)
        list_search_files=sortie_find.split('\n')
        list_search_files.pop(-1)
        print "liste des fichiers selon les criteres de recherche", list_search_files

        list_search_files_crs=[]
        for files in list_search_files :
            list_search_files_crs.append(getCRS(files))
            print "liste des crs des fichiers recherches", list_search_files_crs

        for files in list_search_files :
            new_dict_crs2filename[getCRS(files)]=files
        print "new dico", new_dict_crs2filename
    #else:
    #    new_dict_crs2filename=crs2filename.copy()

        print "dictionnaire apres recherche size/age/access", new_dict_crs2filename
    #new_dict_crs2filename.keys()
    #new_dict_crs2filename.values()

#    if filtre is not "" :
#        if len(new_dict_crs2filename) != 0 : #il y a eu une recherche sur size, age ou access qui a rendu un resu#ltat, et on va chercher le filtre ds ce resultat
#            list_crs_to_rm=[]
#            for crs in new_dict_crs2filename :
#                if re.search(filtre, crs) or re.search(filtre, new_dict_crs2filename[crs]) :
#                    print "chaine trouvee ds le nouveau dico", crs, new_dict_crs2filename[crs]
#                else:
#                    list_crs_to_rm.append(crs)
#            if len(list_crs_to_rm) != 0 : 
#                for crs in list_crs_to_rm :
#                    del new_dict_crs2filename[crs]
#            print "mise a jour", new_dict_crs2filename
#        elif len(new_dict_crs2filename) == 0 and var_find is False: #il n y a pas eu de recherche sur size/age/access dc on cherche le filtre dans le dico d origine
#            print "find =",var_find
#            new_dict_crs2filename=crs2filename.copy()
#            list_crs_to_rm=[]
#            for crs in crs2filename :
#                if re.search(filtre, crs) or re.search(filtre, crs2filename[crs]):
#                    print "chaine trouvee ds", crs, crs2filename[crs]
#                else:
#                    list_crs_to_rm.append(crs)
#            if len(list_crs_to_rm) != 0 :
#                for crs in list_crs_to_rm :
#                    del new_dict_crs2filename[crs]
#                print "new dico update", new_dict_crs2filename
#            else:
#                print "aucun chgt", new_dict_crs2filename
#        elif len(new_dict_crs2filename) == 0 and var_find is True: # il y a eu une une recherche sur size, age ou access qui a rendu un resultat vide donc on ne recherche pas le filtre 
#            print "find =",var_find
#            new_dict_crs2filename={}
#            print "fin de la recherche"

    #dict_filter=dict()
    if filtre is not "" :
        dict_filter=dict()
        dict_filter=crs2filename.copy()
        list_crs_to_rm=[]
        for crs in crs2filename :
            if re.search(filtre, crs) or re.search(filtre, crs2filename[crs]):
                print "chaine trouvee ds", crs, crs2filename[crs]
            else:
                list_crs_to_rm.append(crs)
        if len(list_crs_to_rm) != 0 :
            for crs in list_crs_to_rm :
                del dict_filter[crs]
            print "new dico pr filter", dict_filter
        else:
            print "aucun chgt apres recherche sur filter", dict_filter
    #else:
    #    dict_filter=crs2filename.copy()
        
    #pb qui a pr consequence un chgt de methose: si le filtre est non vide et que le dico est vide
    #dict_notfilter=dict()
    if notfilter is not "" :
        dict_notfilter=dict()
        dict_notfilter=crs2filename.copy()
        list_crs_to_rm=[]
        for crs in crs2filename :
            if re.search(notfilter, crs) is None and re.search(notfilter, crs2filename[crs]) is None:
                print "chaine non presente ds", crs, crs2filename[crs]
            else:
                list_crs_to_rm.append(crs)
        if len(list_crs_to_rm) != 0 :
            for crs in list_crs_to_rm :
                del dict_notfilter[crs]
            print "new dico pr notfilter", dict_notfilter
        else:
            print "aucun chgt apres recherche sur notfilter", dict_notfilter
    #else:
    #    dict_notfilter=crs2filename.copy()

    #intersection des criteres de recherche
    dict_final=dict()
    #avec copies de dict meme sil n y a pas de recherche
    #for crs in crs2filename :
        #if crs in new_dict_crs2filename and crs in dict_filter and crs in dict_notfilter :
        #    dict_final[crs]=new_dict_crs2filename[crs]
    if var_find is True :
        if filtre is not "" :
            if notfilter is not "" :
                print "construction du dic avec dic_find, dict_filter and dict_notfilter "
                for crs in crs2filename :
                    if crs in new_dict_crs2filename and crs in dict_filter and crs in dict_notfilter :
                        dict_final[crs]=new_dict_crs2filename[crs]
            else:
                print "construction du dic avec dic_find and dict_filter "
                for crs in crs2filename :
                    if crs in new_dict_crs2filename and crs in dict_filter :
                        dict_final[crs]=new_dict_crs2filename[crs]
        elif filtre is "" and notfilter is not "" :
            print "construction du dic avec dic_find and dict_notfilter "
            for crs in crs2filename :
                if crs in new_dict_crs2filename and crs in dict_notfilter :
                    dict_final[crs]=new_dict_crs2filename[crs]
        elif filtre is "" and notfilter is "" :
            print "construction du dic avec dic_find"
            dict_final=new_dict_crs2filename.copy()
            new_dict_crs2filename.clear()
    elif var_find is False and filtre is not "" :
        if notfilter is not "" :
            print "construction du dic avec dic_filter and dict_notfilter "
            for crs in crs2filename :
                if crs in dic_filter and crs in dict_notfilter :
                    dict_final[crs]=dict_filter[crs]
        else:
            print "construction du dic avec dic_filter"
            dict_final=dic_filter.copy()
            dict_filter.clear()
    elif var_find is False and filtre is "" :
        if notfilter is not "" :
            print "construction du dic avec dict_notfilter"
            dict_final=dic_notfilter.copy()
            dict_notfilter.clear()
        else:
            print "construction sur le dic d origine"

    #dictionnaire avec les criteres de recherche appliquees 
    #new_dict_crs2filename.clear()
    #dict_filter.clear()
    #dict_notfilter.clear()

    #retour de la fonction cls
    if var_find is True or filtre is not "" or notfilter is not "" :
        if filename is True :
            for crs in dict_final :
                print "dictionnaire final", dict_final[crs]
        else:
            for crs in dict_final :
                print "dictionnaire final", crs, dict_final[crs]
    else:
        if filename is True :
            for crs in crs2filename :
                print "le dic est l original", crs2filename[crs]
        else:
            for crs in crs2filename :
                print "le dic est l original", crs, crs2filename[crs]
      
    if usage is True :
        print "usage est a vrai"
        if var_find is True or filtre is not "" or notfilter is not "" : #on parcoure le dic construit
            for crs in dict_final :
                os.system("du -sh "+dict_final[crs])               
        else: #on parcoure le dic d origine
            for crs in crs2filename :
                os.system("du -sh "+crs2filename[crs])
            
    if count is True :
        print "count"
        if var_find is True or filtre is not "" or notfilter is not "" : #on parcoure le dic construit
            if filename is True:
                return(dict_final[crs], len(dict_final))
            else:
                return(len(dict_final))
        else: #on parcoure le dic d origine
            if filename is True:
                return(crs2filename[crs], len(crs2filename))
            else:
                return(len(crs2filename))
            
    if remove is True :
        print "remove"
        if var_find is True or filtre is not "" or notfilter is not "" : #on parcoure le dic construit
            if filename is True :
                for crs in dict_final :
                    os.system("rm -rf "+dict_final[crs])
                    print "%s fichier efface", dict_final[crs]
            else:
                for crs in dict_final :
                    os.system("rm -rf "+dict_final[crs])
        else: #on parcoure le dic d origine
            if filename is True :
                for crs in crs2filename :
                    os.system("rm -rf "+crs2filename[crs])
                    print "%s fichier efface", crs2filename[crs]
            else:
                for crs in crs2filename :
                    os.system("rm -rf "+crs2filename[crs])

    if special is True :
        print "special"
        dic_special=dict()
        if var_find is True or filtre is not "" or notfilter is not "" : #on parcoure le dic construit
            dic_special=dict_final.copy()
        else: #on parcoure le dic d origine
            dic_special=crs2filename.copy()
        print "liste figures speciales", dic_special.values()
        return(dic_special)




 #-------------------------------------    
#    sortie=""
#    list_search_files=[]
#    if size != 0 : #pr le moment hypothese de la taille en nbre octets (unite= bloc de 512 octets)
#        nb_blocs=size/512.
#        os.system("find "+cpath+"/../../tmp/climaf_cache/*/* -size +"+str(int(nb_blocs))+" -print")
#        print "apres le os system"
#        sortie=os.popen("find /home/vignonl/tmp/climaf_cache/*/* -size +%s -print"%str(int(nb_blocs))).read()
#        #list_search_files.append(a)
#        #cm3=os.popen("find /home/vignonl/tmp/climaf_cache/*/* -size +%s -print"%str(int(nb_blocs)))
#        #print cm3.read()
#        #print list_search_files
#    print "sortie", sortie
#    list_search_files.append(sortie)
#    print list_search_files
#    if age != 0 :
#        nb_jours=age/24. #pr le moment hypothese de l age en nombre d heures (unite=bloc de 24h-1jour)
#        #par date de creation
#        os.system("find "+cpath+"/../../tmp/climaf_cache/*/* -ctime +"+str(int(nb_jours))+" -print")
#    if access != 0 :
#        nb_j_acc=access/24. #pr le moment hypothese de l acces en nombre d heures (unite=bloc de 24h-1jour)
#        #par date d acces aux fichiers
#        os.system("find "+cpath+"/../../tmp/climaf_cache/*/* -atime +"+str(int(nb_j_acc))+" -print")
    #-------------------------------------




if __name__ == "__main__":
    cachedirs=[ "~/tmp/climaf_cache" ]
    e=getCRS("~/tmp/climaf_cache/test_expressionOf")
    searchFile("test_expressionOf") 
    stringToPath("aerzed",4)    
    print generateUniqueFileName("azertyuiop")


# Todo :

# a function for restoring the index from directory content, in case it has not been written on disk at the end of a session, or it is broken n some other way
