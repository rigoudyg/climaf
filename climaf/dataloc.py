""" CliMAF datasets location handling and data access module

Handles a database of attributes for describing organization and location of datasets
"""

# Created : S.Senesi - 2014

import os, os.path, re, string, glob, subprocess
from string import Template

import classes
from climaf.period import init_period
from climaf.netcdfbasics import fileHasVar
from clogging import clogger,dedent
from operator import itemgetter

locs=[]

class dataloc():
    def __init__(self, project="*", organization='generic', url=None, model="*", simulation="*", 
                 realm="*", table="*", frequency="*"):
        """
        Create an entry in the data locations dictionary for an ensemble of datasets.

        Args:
          project (str,optional): project name
          model (str,optional): model name
          simulation (str,optional): simulation name
          frequency (str,optional): frequency
          organization (str): name of the organization type, among 
           those handled by :py:func:`~climaf.dataloc.selectLocalFiles`
          url (list of strings): list of URLS for the data root directories

        Each entry in the dictionary allows to store :
        
         - a list of path or URLS, which are root paths for
           finding some sets of datafiles which share a file organization scheme
         - the name for the corresponding data files organization scheme. The current set of known
           schemes is :

           - CMIP5_DRS : any datafile organized after the CMIP5 data reference syntax, such as on IPSL's Ciclad and CNRM's Lustre
           - EM : CNRM-CM post-processed outputs as organized using EM (please use a list of anyone string for arg urls)
           - generic : a data organization described by the user, using patterns such as described for 
             :py:func:`~climaf.dataloc.selectGenericFiles`. This is the default

           Please ask the CliMAF dev team for implementing further organizations. 
           It is quite quick for data which are on the filesystem. Organizations 
           considered for future implementations are :

           - NetCDF model outputs as available during an ECLIS or ligIGCM simulation
           - ESGF
           
         - the set of attribute values which which simulation's data are 
           stored at that URLS and with that organization

        For the sake of brievity, each attribute can have the '*'
        wildcard value; when using the dictionary, the most specific
        entries will be used (whic means : the entry (or entries) with the lowest number of wildcards)

        Example :

         - Declaring that all IPSLCM-Z-HR data for project PRE_CMIP6 are stored under a single root path and folllows organization named CMIP6_DRS::
            
            >>> dataloc(project='PRE_CMIP6', model='IPSLCM-Z-HR', organization='CMIP6_DRS', url=['/prodigfs/esg/'])
            
         - and declaring an exception for one simulation (here, both location and organization are supposed to be different)::
            
            >>> dataloc(project='PRE_CMIP6', model='IPSLCM-Z-HR', simulation='my_exp', organization='EM', url=['~/tmp/my_exp_data'])

         Please refer to the :ref:`example section <examples>` of the documentation for an example with each organization scheme

                
        """
        self.project=project
        self.model=model
        self.simulation=simulation
        self.frequency=frequency
        self.organization=organization
        if organization not in ['EM', 'CMIP5_DRS', 'generic' ] :
            raise Climaf_Data_Error("Cannot process organization "+organization)
        if (isinstance(url,list)) : self.urls=url
        else :
            if re.findall("^esgf://.*",url) : self.organization="ESGF"
            self.urls=[url]
        self.urls = map(os.path.expanduser,self.urls)
        alt=[]
        for u in self.urls :
            if u[0] != '$' : alt.append(os.path.abspath(u))
            else : alt.append(u)
        self.urls=alt
        # Register new dataloc only if not already registered
        if not (any([ l == self for l in locs])) : locs.append(self)
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)        
    def __str__(self):
        return self.model+self.project+self.simulation+self.frequency+self.organization+`self.urls`
    def pr(self):
        print "For model "+self.model+" of project "+ self.project +\
              " for simulation "+self.simulation+" and freq "+self.frequency +\
              " locations are : " + `self.urls` + " and org is :" + self.organization

 
def getlocs(project="*",model="*",simulation="*",frequency="*"):
    """ Returns the list of org,freq,url triples which may match the 
    list of given attributes values (allowing for wildcards '*') and which have 
    the lowest number of wildcards (*) in attributes 

    """
    rep=[]
    for loc in locs :
        stars=0
        # loc.pr()
        if ( loc.project == "*" or project==loc.project ) :
            if ( loc.project == "*" or project=="*" ) : stars+=1
            if ( loc.model == "*" or model==loc.model ) :
                if ( loc.model == "*" or model=="*" ) : stars+=1
                if ( loc.simulation == "*" or simulation==loc.simulation ) :
                    if ( loc.simulation == "*" or simulation=="*" ) : stars+=1
                    if ( loc.frequency == "*" or frequency==loc.frequency ) :
                        if ( loc.frequency == "*" or frequency=="*" ) : stars+=1
                        rep.append((loc.organization,loc.frequency,loc.urls,stars))
                        # print("appended")
    # Must mimimize the number of '*' ? (allows wildcards in dir names, avoid too generic cases)
    # When multiple answers with wildcards, return the ones with the lowest number
    filtered=[]
    mini=100
    for org,freq,url,stars in rep :
        if (stars < mini) : mini=stars
    for org,freq,url,stars in rep :
        if (stars==mini) : filtered.append((org,freq,url))
    # Should we further filter ?
    return(filtered)


def isLocal(project, model, simulation, frequency) :
    if project == 'file' : return True
    ofu=getlocs(project=project, model=model, simulation=simulation, frequency=frequency) 
    if (len(ofu) == 0 ) : return False
    rep=True
    for org,freq,llocs in ofu :
        for l in llocs :
            if re.findall(".*:.*",l) : rep=False
    return rep

def selectLocalFiles(**kwargs):
    """
    Returns the shortest list of (local) files which include the data
    for the list of (facet,value) pairs provided

    Method : 
    
    - use datalocations indexed by :py:func:`~climaf.dataloc.dataloc` to 
      identify data organization and data store urls for these (facet,value) 
      pairs

    - check that data organization is as known one, i.e. is one of 'generic', 
      CMIP5_DRS' or 'EM'
    
    - derive relevant filenames search function such as as :
      py:func:`~climaf.dataloc.selectCmip5DrsFiles` from data
      organization scheme

    - pass urls and relevant facet values to this filenames search function

    """
    rep=[]
    project=kwargs['project']
    simulation=kwargs['simulation']
    variable=kwargs['variable']
    period=kwargs['period']

    if 'model' in kwargs : model=kwargs['model']
    else : model="*"
    if 'frequency' in kwargs : frequency=kwargs['frequency']
    else : frequency="*"

    ofu=getlocs(project=project, model=model, simulation=simulation, frequency=frequency)
    clogger.debug("locs="+ `ofu`)
    if ( len(ofu) == 0 ) :
        clogger.warning("no datalocation found for %s %s %s %s "%(project, model, simulation, frequency))
    for org,freq,urls in ofu :
        kwargs2=kwargs.copy()
        # Convert normalized frequency to project-specific frequency if applicable
        if "frequency" in kwargs and project in classes.frequencies :
            normfreq=kwargs2['frequency'] 
            if normfreq in classes.frequencies[project]: 
                kwargs2['frequency']=classes.frequencies[project][normfreq]
        #
        # Call organization-specific routine
        if (org == "EM") :
            rep.extend(selectEmFiles(**kwargs2))
        elif (org == "CMIP5_DRS") :
            rep.extend(selectCmip5DrsFiles(urls,**kwargs2))
        elif (org == "generic") :
            rep.extend(selectGenericFiles(urls, **kwargs2))
        else :
            raise Climaf_Data_Error("Cannot process organization "+org+ \
                " for simulation "+simulation+" and model "+model+\
                " of project "+project)
    if (not ofu) :
        return None
    else :
        if (len(rep) == 0 ) :
            clogger.warning("no file found for %s, at these "
                            "data locations %s "%(`kwargs` , `urls`))
            return None
    # Discard duplicates (assumes that sorting is harmless for later processing)
    rep.sort()
    last=None
    for f in rep :
        if f == last : rep.remove(last)
        last=f
    # Assemble filenames in one single string
    return(string.join(rep))

# u="/home/stephane/Bureau/climaf/examples/data/${simulation}/L/${simulation}SFXYYYY.nc"
# selectGenericFiles(simulation="AMIPV6ALBG2", variable="tas", period="1980", urls=[u])

def selectGenericFiles(urls, **kwargs):
    """
    Allow to describe a ``generic`` file organization : the list of files returned 
    by this function is composed of files which :

    - match the patterns in ``url`` once these patterns are instantiated by 
      the values in kwargs, and 

     - contain the ``variable`` provided in kwargs

     - match the `period`` provided in kwargs

    In the pattern strings, no keyword is mandatory

    Example :

    >>> selectGenericFiles(project='my_projet',model='my_model', simulation='lastexp', variable='tas', period='1980', urls=['~/DATA/${project}/${model}/*${variable}*YYYY*.nc)']
    /home/stephane/DATA/my_project/my_model/somefilewith_tas_Y1980.nc

    In the pattern strings, the keywords that can be used in addition to the argument
    names (e.g. ${model}) are:
    
    - ${variable} : use it if the files are split by variable and 
      filenames do include the variable name, as this speed up the search

    - YYYY, YYYYMM, YYYYMMDD : use it for indicating the start date of
      the period covered by each file, if this is applicable in the
      file naming; use a second time for end date, if applicable
      (otherwise the assumption is that the whole year -resp. month or
      day- is included in the file

    - wildcards '?' and '*' for matching respectively one and any number of characters


    """
    rep=[]
    period=kwargs['period']
    if type(period) is str : period=init_period(period)
    variable=kwargs['variable']
    altvar=kwargs.get('filenameVar',variable)
    # a dict and an ordered list of date globbing patterns
    dt=dict(YYYY="????",YYYYMM="??????",YYYYMMDD="????????")
    lkeys=dt.keys() ; lkeys.sort(reverse=True)
    # a dict and an ordered list for matching dates
    dr=dict(YYYY="([0-9]{4})",YYYYMM="([0-9]{6})", YYYYMMDD="([0-9]{8})")
    rkeys=dr.keys() ; rkeys.sort(reverse=True)
    #
    for l in urls :
        # Instantiate keywords in pattern with attributes values
        template=Template(l).safe_substitute(**kwargs)
        #print "template after attributes replace : "+template
        #
        # Construct a pattern for globbing dates
        temp2=template ; 
        for k in lkeys : temp2=temp2.replace(k,dt[k])
        lfiles=glob.glob(temp2)
        clogger.debug("Globbing %d files for varname on %s : "%(len(lfiles),temp2))
        #
        # If unsuccessful using varname, try with filenameVar
        if len(lfiles)==0 and "filenameVar" in kwargs and kwargs['filenameVar'] :
            kwargs['variable']=kwargs['filenameVar']
            template=Template(l).safe_substitute(**kwargs)
            temp2=template
            for k in lkeys : temp2=temp2.replace(k,dt[k])
            #
            lfiles=glob.glob(temp2)
            clogger.debug("Globbing %d files for filenamevar on %s: "%(len(lfiles),temp2))

        # Construct regexp for extracting dates from filename
        regexp=None
        #print "template before searching dates : "+template
        for key in rkeys :
            #print "searchin "+key+" in "+=Template(l)
            start=template.find(key)
            if (start>=0 ) :
                #print "found "+key
                regexp=template.replace(key,dr[key],1)
                hasEnd=False
                start=regexp.find(key)
                if (start >=0 ) :
                    hasEnd=True
                    regexp=regexp.replace(key,dr[key],1)
                break
        #print "regexp before searching dates : "+regexp
        #
        for f in lfiles :
            #print "processing file "+f
            #
            # Analyze file time period
            fperiod=None
            if regexp :
                regexp0=regexp.replace("*",".*").replace("?",r".")
                #print "regexp for extracting dates : "+regexp
                start=re.sub(regexp0,r'\1',f)
                if start==f:
                    raise Climaf_Data_Error("Start period not found") #? 
                if hasEnd :
                    end=re.sub(regexp0,r'\2',f)
                    fperiod=init_period("%s-%s"%(start,end))
                else :
                    fperiod=init_period(start)
                #print "period for file %s is %s"%(f,fperiod)
                #
                # Filter file time period against required period
            else :
                if ( 'frequency' in kwargs and ((kwargs['frequency']=="fx") or \
                    kwargs['frequency']=="seasonnal" or kwargs['frequency']=="annual_cycle" )) :
                    if (l.find("${variable}")>=0) or variable=='*' or \
                       fileHasVar(f,variable) or (variable != altvar and fileHasVar(f,altvar)) : 
                        clogger.debug("adding fixed field :"+f)
                        rep.append(f)
                else :
                    clogger.warning("Cannot yet filter files re. time using only file content. TBD")
                    rep.append(f)
            if (fperiod and period.intersects(fperiod)) or not regexp :
                clogger.debug('Period is OK - Considering variable filtering on %s and %s for %s'%(variable,altvar,f)) 
                # Filter against variable 
                if (l.find("${variable}")>=0):
                    clogger.debug('appending %s based on variable in filename'%f)
                    rep.append(f)
                    continue
                if (f not in rep) and \
                   (variable=='*' or "," in variable or fileHasVar(f,variable) or \
                    (altvar != variable and fileHasVar(f,altvar))) :
                    # Should check time period in the file if not regexp
                    clogger.debug('appending %s based on multi-var or var exists in file '%f)
                    rep.append(f)
                    continue
            else:
                if not fperiod :
                    clogger.debug('not appending %s because period is None '%f)
                else:
                    if not period.intersects(fperiod) :
                        clogger.debug('not appending %s because period doesn t intersect %s'%(f,period))

    return rep


def selectEmFiles(**kwargs) :
    #POur A et L : mon, day1, day2, 6hLev, 6hPlev, 3h
    simulation=kwargs['simulation']
    frequency=kwargs['frequency']
    variable=kwargs['variable']
    period=kwargs['period']
    realm=kwargs['realm']
    #
    freqs={ "mon" : "" , "3h" : "_3h"}
    f=frequency
    if f in freqs : f=freqs[f]
    rep=[]
    # Must look for all realms, here identified by a single letter
    if realm=="*" : lrealm= ["A", "L", "O", "I" ]
    else: lrealm=[ realm ]
    for realm in lrealm :
        clogger.debug("Looking for realm "+realm)
        # Use EM data for finding data dir
        freq_for_em=f
        if realm == 'I' : freq_for_em=""  # This is a special case ...
        command=["grep", "^export EM_DIRECTORY_"+realm+freq_for_em+"=",
                 os.path.expanduser(os.getenv("EM_HOME"))+"/expe_"+simulation ]
        try :
            ex = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except :
            clogger.error("Issue getting archive_location for "+
                          simulation+" for realm "+realm+" with: "+`command`)
            break
        if ex.wait()==0 :
            dir=ex.stdout.read().split("=")[1].replace('"',"").replace("\n","")
            clogger.debug("Looking at dir "+dir)
            if os.path.exists(dir) :
                lfiles= os.listdir(dir)
                for fil in lfiles :
                    #clogger.debug("Looking at file "+fil)
                    fileperiod=periodOfEmFile(fil,realm,f)
                    if fileperiod and period.intersects(fileperiod) :
                        if fileHasVar(dir+"/"+fil,variable) :
                            rep.append(dir+"/"+fil)
                    #clogger.debug("Done with Looking at file "+fil)
            else : clogger.error("Directory %s does not exist for simulation %s, realm %s "
                                 "and frequency %s"%(dir,simulation,realm,f))
        else :
            clogger.info("No archive location found for "+
                          simulation+" for realm "+realm+" with: "+`command`)
    return rep


def periodOfEmFile(filename,realm,freq):
    """
    Return the period covered by a file handled by EM, based on filename
    rules for EM. returns None if file frequency does not fit freq
    """
    if (realm == 'A' or realm == 'L' ) :
        if freq=='mon' or freq=='' :
            year=re.sub(r'^.*([0-9]{4}).nc',r'\1',filename)
            if year.isdigit(): 
                speriod="%s01-%s12"%(year,year)
                return init_period(speriod)
        else:
                raise Climaf_Data_Error("can yet handle only monthly frequency for realms A and L - TBD")
    elif (realm == 'O' or realm == 'I' ) :
        if freq=='monthly' or freq=='mon' or freq=='' : altfreq='m'
        elif freq[0:2] =='da' : altfreq='d'
        else:
            raise Climaf_Data_Error("Can yet handle only monthly and daily frequency for realms O and I - TBD")
        patt=r'^.*_1'+altfreq+r'_([0-9]{8})_*([0-9]{8}).*nc'
        beg=re.sub(patt,r'\1',filename)
        end=re.sub(patt,r'\2',filename)
        #clogger.debug("beg=%s,end=%s,fn=%s"%(beg,end,filename))
        if (end==filename or beg==filename) : return None
        return init_period("%s-%s"%(beg,end))
    else:
        raise Climaf_Data_Error("unexpected realm "+realm)

        


                        
def selectExampleFiles(urls,**kwargs) :
    rep=[]
    if (kwargs['frequency'] == "monthly") :
        for l in urls :
            for realm in ["A","L"] :
                #dir=l+"/"+realm+"/Origin/Monthly/"+simulation
                dir=l+"/"+realm
                clogger.debug("Looking at dir "+dir)
                if os.path.exists(dir) :
                    lfiles= os.listdir(dir)
                    for f in lfiles :
                        clogger.debug("Looking at file "+f)
                        fileperiod=periodOfEmFile(f,realm,'mon')
                        if fileperiod and fileperiod.intersects(kwargs['period']) :
                            if fileHasVar(dir+"/"+f,kwargs['variable']) :
                                rep.append(dir+"/"+f)
                            #else: print "No var ",variable," in file", dir+"/"+f
    return rep
                        

def selectCmip5DrsFiles(urls, **kwargs) :
    # example for path : CMIP5/[output1/]CNRM-CERFACS/CNRM-CM5/1pctCO2/mon/atmos/
    #      Amon/r1i1p1/v20110701/clivi/clivi_Amon_CNRM-CM5_1pctCO2_r1i1p1_185001-189912.nc
    #
    # second path segment can be any string (allows for : output,output1, merge...), 
    # but if 'merge' exists, it is used alone
    # This segment ca also be empty
    #
    # If version is 'last', tries provide version from directory 'last' if available,
    # otherwise those of last dir
    project=kwargs['project']
    model=kwargs['model']
    simulation=kwargs['simulation']
    frequency=kwargs['frequency']
    variable=kwargs['variable']
    realm=kwargs['realm']
    table=kwargs['table']
    period=kwargs['period']
    experiment=kwargs['experiment']
    version=kwargs['version']
    #
    rep=[]
    frequency2drs=dict({'monthly':'mon'})
    freqd=frequency
    if frequency in frequency2drs : freqd=frequency2drs[frequency]
    # TBD : analyze ambiguity of variable among realms+tables
    for l in urls :
        totry=['merge/','output/','output?/','main/','']
        for p in totry :
            pattern1=l+"/"+project+"/"+p+"*/"+model # one * for modelling center
            if len(glob.glob(pattern1))>0 : break
        patternv=pattern1+"/"+experiment+"/"+freqd+"/"+realm+"/"+table+"/"+simulation
        # Get version directories list
        ldirs=glob.glob(patternv)
        clogger.debug("Globbing with "+patternv+ " gives:" +`ldirs`)
        for repert in ldirs :
            lversions=os.listdir(repert)
            lversions.sort()
            #print "lversions="+`lversions`+ "while version="+version
            cversion=version # initial guess of the version to use
            if (version == "last") :
                if (len(lversions)== 1) : cversion=lversions[0]
                elif (len(lversions)> 1) :
                    if "last" in lversions : cversion="last"
                    else :
                        cversion=lversions[-1] # Assume that order provided by sort() is OK
            #print "using version "+cversion+" for requested version: "+version
            lfiles=glob.glob(repert+"/"+cversion+"/"+variable+"/*.nc")
            #print "listing "+repert+"/"+cversion+"/"+variable+"/*.nc"
            #print 'lfiles='+`lfiles`
            for f in lfiles :
                if freqd != 'fx' :
                    #clogger.debug("checking period for "+ f)
                    regex=r'^.*([0-9]{4}[0-9]{2}-[0-9]{4}[0-9]{2}).nc$'
                    fileperiod=init_period(re.sub(regex,r'\1',f))
                    if (fileperiod and period.intersects(fileperiod)) :
                        rep.append(f)
                else :
                    clogger.debug("adding fixed field "+ f)
                    rep.append(f)

    return rep


class Climaf_Data_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)
    def __str__(self):
        return `self.valeur`


def test2() :
    return

if __name__ == "__main__":
    test2()



