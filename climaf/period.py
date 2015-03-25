"""  Basic types and syntax for managing time periods in CLIMAF 

"""

# S.Senesi 08/2014 : created

# The CliMAF software is an environment for Climate Model Assessment. It
# has been developped mainly by CNRM-GAME (Meteo-France and CNRS), and
# by IPSL, in the context of the `CONVERGENCE project
# <http://convergence.ipsl.fr/>`_, funded by The
# French 'Agence Nationale de la Recherche' under grant #
# ANR-13-MONU-0008-01
# 
# This software is governed by the CeCILL-C license under French law and
# biding by the rules of distribution of free software. The CeCILL-C
# licence is a free software license,explicitly compatible with the GNU
# GPL (see http://www.gnu.org/licenses/license-list.en.html#CeCILL)

import re, datetime, logging

class cperiod():
    """
    A class for handling a pair of datetime objects defining a period.

    Period is defined as \[ date1, date2 \[

    """
    def __init__(self,start,end,leng) :
        if not isinstance(start,datetime.datetime) or not isinstance(end,datetime.datetime) : 
            logging.error("classes.cperiod : issue with start or end")
            return(None)
        self.start=start ; self.end=end ; self.len=leng
    #
    def __repr__(self):
        return "%04d%02d%02d-%04d%02d%02d"%(
              self.start.year,self.start.month,self.start.day,
              self.end.year,self.end.month,self.end.day)
    def pr(self) :
        return("%04d%02d%02d%02d%02d-%04d%02d%02d%02d%02d"%(\
              self.start.year,self.start.month,self.start.day,self.start.hour,self.start.minute,
              self.end.year,self.end.month,self.end.day,self.end.hour,self.end.minute))
    #
    def hasFullYear(self,year):
        return( int(year) >= self.start.year and int(year) < self.end.year) 

    def start_with(self,begin) :
        """ If period BEGIN actually begins period SELF, returns the 
        complement of BEGIN in SELF; otherwise returns None """
        if self.start==begin.start and self.end >= begin.end : 
            return cperiod(begin.end,self.end,self.len)
                
    def includes(self,included) :
        """ if period self does include period 'included', returns a pair of
        periods which represents the difference """
        if self.start <= included.start and included.end <= self.end :
            return cperiod(self.start,included.start,self.len), 
        cperiod(included.end,self.end,self.len)

def init_period(dates) :
    """
    Init a CliMAF 'period' object

    Args:
      dates (str): must match YYYY[MM[DD[HH[MM]]]][(-\|_)YYYY[MM[DD[HH[MM]]]]]

    Returns:
      the corresponding CliMAF 'period' object
      
    TBD : If second part is missing, assume the longest possible duration re. accuracy
    """
    
    logging.debug("climaf.period.init_period : processing %s"%dates)
    start=re.sub(r'^([0-9]{4,12}).*',r'\1',dates)
    # TBD : check that start actually matches a date
    end=re.sub(r'.*[-_]([0-9]{4,12})$',r'\1',dates)
    logging.debug("climaf.period.init_period : start= %s, end=%s"%(start,end))
    start2=start
    if (end==dates) :
        logging.critical("classes.period.init : must code single date period")
        return None
    syear  =int(start[0:4])
    smonth =int(start[4:6])  if len(start) > 5  else 1
    sday   =int(start[6:8])  if len(start) > 7  else 1
    shour  =int(start[8:10]) if len(start) > 9  else 0
    sminute=int(start[10:12])if len(start) > 11 else 0
    #
    eyear  =int(end[0:4])
    emonth =int(end[4:6])  if len(end) > 5  else 1
    eday   =int(end[6:8])  if len(end) > 7  else 1
    ehour  =int(end[8:10]) if len(end) > 9  else 0
    eminute=int(end[10:12])if len(end) > 11 else 0
    #
    yearstart=False
    if len(end) < 6 :
        eyear+=1
        yearstart=True
        if len(end) < 8 and (not yearstart) : emonth+=1
        if (emonth > 12) :
            emonth=1
            eyear+=1
    #
    if len(start) != len(end) :
        logging.error("climaf.classes : must have the same number of digits "+\
                          "for period's start and end")
    else :
        s=datetime.datetime(year=syear,month=smonth,day=sday,hour=shour,minute=sminute)
        e=datetime.datetime(year=eyear,month=emonth,day=eday,hour=ehour,minute=eminute)
        if s > e :
            logging.error("climaf.classes : must have start before (or equals to) end ")
        else :
            return cperiod(s,e,len(start))
