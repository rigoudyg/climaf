"""  Basic types and syntax for managing time periods in CLIMAF 

"""

# S.Senesi 08/2014 : created

import re, datetime, logging

class cperiod():
    """
    A class for handling a pair of datetime objects defining a period.

    Period is defined as \[ date1, date2 \[

    """
    def __init__(self,start,end) :
        if not isinstance(start,datetime.datetime) or not isinstance(end,datetime.datetime) : 
            logging.error("classes.cperiod : issue with start or end")
            return(None)
        self.start=start ; self.end=end 
    #
    def __repr__(self):
        return "%04d%02d%02d-%04d%02d%02d"%(
              self.start.year,self.start.month,self.start.day,
              self.end.year,self.end.month,self.end.day)
    #
    def iso(self):
        """ Return isoformat(start)-isoformat(end), (with inclusive end, and 1 minute accuracy)
        e.g. : 1980-01-01T00:00:00-1980-12-31T23:59:00
        """
        endproxy = self.end - datetime.timedelta(0,60)  # substract 1 minute
        return "%s-%s"%(self.start.isoformat(),endproxy.isoformat())
    #
    def pr(self) :
        return("%04d%02d%02d%02d%02d-%04d%02d%02d%02d%02d"%(\
              self.start.year,self.start.month,self.start.day,self.start.hour,self.start.minute,
              self.end.year,self.end.month,self.end.day,self.end.hour,self.end.minute))
    #
    def hasFullYear(self,year):
        return( int(year) >= self.start.year and int(year) < self.end.year) 
    #
    def start_with(self,begin) :
        """ If period BEGIN actually begins period SELF, returns the 
        complement of BEGIN in SELF; otherwise returns None """
        if self.start==begin.start and self.end >= begin.end : 
            return cperiod(begin.end,self.end)
    #
    def includes(self,included) :
        """ if period self does include period 'included', returns a pair of
        periods which represents the difference """
        if self.start <= included.start and included.end <= self.end :
            return cperiod(self.start,included.start), 
        cperiod(included.end,self.end)
    #
    def intersects(self,other) :
        """ 
        Returns the intersection of period self and period 'other' if any
        """
        if other :
            start=self.start
            if (other.start > start) : start=other.start
            end=self.end
            if (other.end < end) : end=other.end
            if (start < end) : return cperiod(start,end)

def init_period(dates) :
    """
    Init a CliMAF 'period' object

    Args:
      dates (str): must match YYYY[MM[DD[HH[MM]]]][(-\|_)YYYY[MM[DD[HH[MM]]]]]

    Returns:
      the corresponding CliMAF 'period' object
      
    """
    
    start=re.sub(r'^([0-9]{4,12}).*',r'\1',dates)
    # TBD : check that start actually matches a date
    syear  =int(start[0:4])
    smonth =int(start[4:6])  if len(start) > 5  else 1
    sday   =int(start[6:8])  if len(start) > 7  else 1
    shour  =int(start[8:10]) if len(start) > 9  else 0
    sminute=int(start[10:12])if len(start) > 11 else 0
    try :
        s=datetime.datetime(year=syear,month=smonth,day=sday,hour=shour,minute=sminute)
    except :
        logging.debug("climaf.period.init_period : period start string %s is not a date"%start)
        return(NOne)
    #
    end=re.sub(r'.*[-_]([0-9]{4,12})$',r'\1',dates)
    logging.debug("climaf.period.init_period : for dates=%s, start= %s, end=%s"%(dates,start,end))
    if (end==dates) :
        # No string found for end of period 
        print "lstart=",len(start)
        eyear   = syear  if len(start) > 5  else  syear+1
        emonth  = smonth if len(start) > 7  else  smonth+1
        eday    = sday   if len(start) > 9  else  sday+1
        ehour   = shour+1
        eminute = 0
    else:
        eyear  =int(end[0:4])
        emonth =int(end[4:6])  if len(end) > 5  else 1
        eday   =int(end[6:8])  if len(end) > 7  else 1
        ehour  =int(end[8:10]) if len(end) > 9  else 0
        eminute=int(end[10:12])if len(end) > 11 else 0
    #
    try :
        e=datetime.datetime(year=eyear,month=emonth,day=eday,hour=ehour)
    except:
        logging.debug("climaf.period.init_period : period end string %s is not a date"%end)
    # yearstart=False
    # if len(end) < 6 :
    #     eyear+=1
    #     yearstart=True
    # if len(end) < 8 and (not yearstart) : emonth+=1
    # if (emonth > 12) :
    #     emonth=1
    #     eyear+=1
    #
    if s < e :
        return cperiod(s,e)
    else :
        logging.error("climaf.classes : must have start before (or equals to) end ")
