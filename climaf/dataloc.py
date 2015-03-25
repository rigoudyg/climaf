""" CliMAF datasets location handling and data access module

Handles a database of attributes for describing organization and location of datasets
"""

# Created : S.Senesi - 2014

import os, re,logging, string, glob
from climaf.period import init_period

locs=[]

class dataloc():
    def __init__(self,project="*",model="*",experiment="*",frequency="*",rip="*",organization="CLIPROC",url="/cnrm/aster/data1/simulations"):
        """
        Create an entry in the data locations dictionnary for an ensemble of datsets.

        Args:
          project (str): project name
          model (str): model name
          experiment (str): exepriment name
          frequency (str): frequency
          organization (str): name of the organization type, among those handled by :py:func:`selectLocalFiles`
          url (list of strings): list of URLS for the data root directories

        Each entry provides :
         - a list of path or URLS, which are root paths for
           finding datafiles for datasets;
         - the name for the corresponding data files organization

        Datasets sets are there indexed by a combination of attributes
        values (the arguments keywords);

        For the sake of brievity, each attribute can have the '*'
        wildcard value; when using the dictionnary, the most specific
        entries will be used

        Example, for declaring that all IPSLCM-Z-HR data for project
        PRE_CMIP6 are stored under a single root path and folllows
        organization named CMIP6_DRS::
        
        >>> cdataloc(project='PRE_CMIP6', model='IPSLCM-Z-HR', organization='CMIP6_DRS', url=['/prodigfs/esg/'])

        """
        self.project=project
        self.model=model
        self.experiment=experiment
        self.frequency=frequency
        self.organization=organization
        if (isinstance(url,list)) : self.urls=url
        else :
            if re.findall("^esgf://.*",url) : self.organization="ESGF"
            self.urls=[url]
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
        return self.model+self.project+self.experiment+self.frequency+self.organization+`self.urls`
    def pr(self):
        print "For model "+self.model+" of project "+ self.project +\
              " for experiment "+self.experiment+" and freq "+self.frequency +\
              " locations are : " + `self.urls` + " and org is :" + self.organization

 
def getlocs(project="*",model="*",experiment="*",frequency="*"):
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
                if ( loc.experiment == "*" or experiment==loc.experiment ) :
                    if ( loc.experiment == "*" or experiment=="*" ) : stars+=1
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


def oneVarPerFile(project="*",model="*",experiment="*",frequency="*"):
    org,freq,llocs=getlocs(project,model,experiment,frequency)
    if len(llocs) > 1 :
        logging.warning("dataloc.oneVarPerFile : cannot yet handle case of multiple locs "+\
                         " for experiment "+experiment+", model "+model+" , and project "+project)
        return(False)
    else :
        org=llocs[0][0]
        if org=="CLIPROC" : return False
        if org=="ESGF"    : return True
        if org=="DRS"     : return True
        if org=="COUGAR"  : return False
        logging.warning("dataloc.oneVarPerFile : cannot yet handle organization "+m.organization+\
                         " for experiment "+experiment+", model "+model+" , and project "+project)
        return False
        

def isLocal(project, model, experiment, frequency) :
    ofu=getlocs(project=project, model=model, experiment=experiment, frequency=frequency) 
    if (len(ofu) == 0 ) : return False
    rep=True
    for org,freq,llocs in ofu :
        for l in llocs :
            if re.findall(".*:.*",l) : rep=False
    return rep

def selectLocalFiles(project, model, experiment, frequency, variable, period, rip="r1i1p1", version="last"):
    """
    Returns the shortest list of (local) files which include the data for the dataset
    
    Method : depending on the data organization, select the relevant files for the
    requested period and variable, using datalocations indexed by :py:func:`dataloc`, and based
    on the datafiles organization for the corresponding datasets; each organization has a
    corresponding filename search function sur as :py:func:selectCmip5DrsFiles

    Known organizations as of today: EM, CMIP5_DRS, OCMIP5_Ciclad, OBS4MIPS_CNRM, OBS_CAMI
    
    """
    rep=[]
    ofu=getlocs(project=project, model=model, experiment=experiment, frequency=frequency)
    logging.debug("dataloc.selectLocalFiles : locs="+ `ofu`)
    if ( len(ofu) == 0 ) :
        logging.warning("dataloc.selectLocalFiles : no datalocation found for %s %s %s %s "%(project, model, experiment, frequency))
    for org,freq,urls in ofu :
        if (org == "EM") :
            rep.extend(selectEmFiles(experiment, frequency, period, urls))
        elif (org == "CMIP5_DRS") :
            rep.extend(selectCmip5DrsFiles(project, model, experiment, frequency, variable, period, rip, version, urls))
        elif (org == "OCMIP5_Ciclad") :
            rep.extend(selectOcmip5CicladFiles(project, model, experiment, frequency, variable, period, urls))
        elif (org == "OBS4MIPS_CNRM") :
            rep.extend(selectObs4mipsCnrmFiles(model, frequency, variable, period, urls))
        elif (org == "OBS_CAMI") :
            rep.extend(selectCamiObsFiles(model, frequency, variable, period, urls))
        else :
            logging.error("dataloc.selectLocalFiles : cannot process organization "+org+ \
                             " for experiment "+experiment+" and model "+model+\
                             " of project "+project)
    if (not ofu) :
        return None
    else :
        if (len(rep) == 0 ) :
            logging.warning("dataloc.selectLocalFiles : no file found for variable : %s, period : %s, and rip : %s , at these data locations %s , for model : %s, experiment : %s frequency : %s "%(variable, `period`, rip,  `urls`,model,experiment,frequency))
            return None
    # Discard duplicates (assumes that sorting is harmless for later processing)
    rep.sort()
    last=None
    for f in rep :
        if f == last : rep.remove(last)
        last=f
    # Assemble filenames in one single string
    return(string.join(rep))

def selectEmFiles(experiment, frequency, period, urls) :
    rep=[]
    if (frequency == "monthly") :
        for l in urls :
            for realm in ["A","L"] :
                #dir=l+"/"+realm+"/Origin/Monthly/"+experiment
                dir=l+"/"+realm
                logging.debug("dataloc.selectEmFiles : Looking at dir "+dir)
                if os.path.exists(dir) :
                    lfiles= os.listdir(dir)
                    for f in lfiles :
                        logging.debug("dataloc.selectEmFiles: Looking at file "+f)
                        year=re.sub(r'^.*([0-9]{4}).nc',r'\1',f)
                        if year.isdigit() and period.hasFullYear(year) : rep.append(dir+"/"+f)
    return rep
                        

def selectCmip5DrsFiles(project, model, experiment, frequency, variable, period, rip, version, urls) :
    # example for path : CMIP5/output1/CNRM-CERFACS/CNRM-CM5/1pctCO2/mon/atmos/
    #      Amon/r1i1p1/v20110701/clivi/clivi_Amon_CNRM-CM5_1pctCO2_r1i1p1_185001-189912.nc
    # We use wildcards for : lab, realm and MIP_table
    # second path segment can be any string (allows for : output,output1, merge...), but if 'merge' exists, it is 
    # used alone
    # If version is 'last', tries provide version from directory 'last' if available, otherwise those of last dir
    rep=[]
    frequency2drs=dict({'monthly':'mon'})
    freqd=frequency
    if frequency in frequency2drs : freqd=frequency2drs[frequency]
    for l in urls :
        pattern1=l+"/"+project+"/merge"
        if not os.path.exists(pattern1) : pattern1=l+"/"+project+"/*"
        patternv=pattern1+"/*/"+model+"/"+experiment+"/"+freqd+"/*/*/"+rip
        # Get version directories list
        ldirs=glob.glob(patternv)
        for repert in ldirs :
            lversions=os.listdir(repert)
            lversions.sort()
            if (version == "last") :
                if (len(lversions)== 1) : version=lversions[0]
                elif (len(lversions)> 1) :
                    if "last" in lversions : lversions=["last"]
                    else : version=lversions[-1] # Assume that order provided by sort() is OK
            if version in lversions :
                lfiles=glob.glob(repert+"/"+version+"/"+variable+"/*.nc")
                for f in lfiles :
                    logging.debug("dataloc.selectCmip5DrsFiles : checking period for "+ f)
                    regex=r'^.*([0-9]{4}[0-9]{2}-[0-9]{4}[0-9]{2}).nc$'
                    fileperiod=init_period(re.sub(regex,r'\1',f))
                    if fileperiod is not None : 
                        if (period.start <= fileperiod.end and period.end >= fileperiod.start) :
                            rep.append(f) 
    return rep

def selectOcmip5CicladFiles(project, model, experiment, frequency, variable, period, urls):
    rep=[]
    # [/prodigfs]/OCMIP5/OUTPUT/IPSL/IPSL-CM4/CTL/mon/CACO3/CACO3_IPSL_IPSL-CM4_CTL_1860-1869.nc
    frequency2drs=dict({'monthly':'mon', 'yearly':'yr','year':'yr'})
    freqd=frequency
    if frequency in frequency2drs : freqd=frequency2drs[frequency]
    for l in urls :
        patternv="/"+project+"/OUTPUT/*/"+model+"/"+experiment+"/"+freqd
        ldirs=glob.glob(l+patternv)
        for repert in ldirs :
            lfiles=glob.glob(repert+"/"+variable+"/"+variable+"*.nc")
            for f in lfiles :
                logging.debug("dataloc.selectOcmip5CicladFiles : checking period for "+ f)
                regex=r'^.*_([0-9]*-[0-9]*).nc$'
                fileperiod=init_period(re.sub(regex,r'\1',f))
                if fileperiod is not None : 
                    if (period.start <= fileperiod.end and period.end >= fileperiod.start) :
                        rep.append(f)
    return rep


def selectObs4mipsCnrmFiles(instrument, frequency, variable, period, urls):
    rep=[]
    # [/cnrm/vdr/DATA/Obs4MIPs/netcdf/]monthly_mean/clt_MODIS_L3_C5_200003-201109.nc
    frequency2drs=dict({'monthly':'monthly_mean'})
    freqd=frequency
    if frequency in frequency2drs : freqd=frequency2drs[frequency]
    for l in urls :
        pattern=l+"/"+freqd+"/"+variable+"_"+instrument+"*nc"
        logging.debug("dataloc.selectObs4mipsCnrmFiles : looking at loc "+ l+" for "+pattern)
        lfiles=glob.glob(pattern)
        for f in lfiles :
            logging.debug("dataloc.selectObs4mipsCnrmFiles : checking period for "+ f)
            regex=r'^.*_([0-9]*-[0-9]*).nc$'
            fileperiod=init_period(re.sub(regex,r'\1',f))
            if fileperiod is not None : 
                if (period.start <= fileperiod.end and period.end >= fileperiod.start) :
                    rep.append(f)
    return rep

def selectCamiObsFiles(instrument, frequency, variable, period, urls):
    rep=[]
    # /cnrm/aster/data1/UTILS/cami/V1.7/climlinks/CAYAN/hfls_1m_194601_199803_CAYAN.nc
    frequency2drs=dict({'monthly':'1m'})
    freqd=frequency
    if frequency in frequency2drs : freqd=frequency2drs[frequency]
    for l in urls :
        pattern=l+"/"+instrument+"/"+variable+"_"+freqd+"_"+"*.nc"
        logging.debug("dataloc.selectCamiObsFiles : looking at loc "+ l+" for "+pattern)
        lfiles=glob.glob(pattern)
        for f in lfiles :
            logging.debug("dataloc.selectCamiObsFiles : checking period for "+ f)
            regex=r'^.*_([0-9]*_[0-9]*)_'+instrument+'.nc$'
            fileperiod=init_period(re.sub(regex,r'\1',f))
            if fileperiod is not None : 
                if (period.start <= fileperiod.end and period.end >= fileperiod.start) :
                    rep.append(f)
    return rep


def cliproc_listfiles(loc,variable,period):
    rep=[]
    if (loc.frequency == "monthly") :
        for l in loc.urls :
            for realm in ["A","L"] :
                dir=l+"/"+loc.experiment+"/"+realm
                if os.path.exists(dir) :
                    lfiles= os.listdir(dir)
                    for f in lfiles :
                        year=re.sub(r'^.*([0-9]{4}).nc',r'\1',f)
                        if year.isdigit() and period.hasFullYear(year) : rep.append(dir+"/"+f)
    else :
        logging.error("dataloc.cliproc_listFiles : cannot yet process frequency "+loc.frequency+ \
                         " ( for experiment "+experiment+", model "+model+" , and project "+project+")")
    return(rep)


def test2() :
    dataloc(experiment="SPE",organization="CLIPROC",frequency="*",url="/cnrm/aster/data1/simulations/AR5")
    l=getlocs(experiment="SPE", frequency="monthly")
    #print l
    l=selectLocalFiles(None,None,"SPE","monthly",None,"1800-1800")
    return(l)


if __name__ == "__main__":
    test2()


