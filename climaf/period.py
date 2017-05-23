"""  Basic types and syntax for managing time periods in CLIMAF 

"""

# S.Senesi 08/2014 : created

import re, datetime
from climaf.clogging import clogger, dedent

class cperiod():
    """
    A class for handling a pair of datetime objects defining a period.

    Period is defined as [ date1, date2 ]. Resolution for date2 is 1 minute
    Attribute 'pattern' usually provides a more condensed form

    """
    def __init__(self,start,end=None,pattern=None) :
        self.fx=False
        if start == 'fx' :
            self.fx=True
            self.pattern='fx'
        elif not isinstance(start,datetime.datetime) or not isinstance(end,datetime.datetime) : 
            raise Climaf_Period_Error("issue with start or end")
        else :
            self.start=start ; self.end=end ;
            if pattern is None :
                self.pattern=self.__repr__()
            else:
                self.pattern=pattern
    #
    def __repr__(self):
        return self.pr()
        #return("%04d%02d%02d%02d%02d-%04d%02d%02d%02d%02d"%(\
        #      self.start.year,self.start.month,self.start.day,self.start.hour,self.start.minute,
        #      self.end.year,self.end.month,self.end.day,self.end.hour,self.end.minute))
    #
    def iso(self):
        """ Return isoformat(start)-isoformat(end), (with inclusive end, and 1 minute accuracy)
        e.g. : 1980-01-01T00:00:00,1980-12-31T23:59:00
        """
        if (self.fx) :
            raise Climaf_Period_Error("There is no ISO representation for period 'fx'")
        endproxy = self.end - datetime.timedelta(0,60)  # substract 1 minute
        return "%s,%s"%(self.start.isoformat(),endproxy.isoformat())
    #
    def pr(self) :
        if self.fx : return 'fx'
        if (self.start.minute != 0 or self.start.minute != 0):
            return("%04d%02d%02d%02d%02d-%04d%02d%02d%02d%02d"%(\
                    self.start.year,self.start.month,self.start.day,self.start.hour,self.start.minute,
                    self.end.year,self.end.month,self.end.day,self.end.hour,self.end.minute))
        elif (self.start.hour != 0 or self.end.hour != 0 ):
            return("%04d%02d%02d%02d-%04d%02d%02d%02d"%(\
                    self.start.year,self.start.month,self.start.day,self.start.hour,
                    self.end.year,self.end.month,self.end.day,self.end.hour))
        elif (self.start.day != 1 or self.end.day != 1 ):
            if (self.end.day != 1 ): 
                d=self.end.day -1
                m=self.end.month
                y=self.end.year
            else : 
                end=self.end - datetime.timedelta(1)
                y=end.year ; m=end.month; d=end.day
            if (self.start.year,self.start.month,self.start.day)== (y,m,d) :
                return("%04d%02d%02d"%(y,m,d))
            else:
                return("%04d%02d%02d-%04d%02d%02d"%(\
                    self.start.year,self.start.month,self.start.day,
                    y,m,d))
        elif (self.start.month != 1 or self.end.month != 1 ):
            if (self.end.month != 1 ): 
                m=self.end.month -1
                y=self.end.year
            else : 
                m=12
                y=self.end.year-1
            if self.start.year==y and self.start.month==m :
                return("%04d%02d"%(self.start.year,self.start.month))
            else:
                return("%04d%02d-%04d%02d"%(self.start.year,self.start.month,y, m))
        else :
            if self.start.year != self.end.year-1 : 
                return("%04d-%04d"%(self.start.year, self.end.year-1))
            else:
                return("%04d"%(self.start.year))
    #
    def hasFullYear(self,year):
        if (self.fx) :
            raise Climaf_Period_Error("Meaningless for period 'fx'")
        return( int(year) >= self.start.year and int(year) < self.end.year) 
    #
    def start_with(self,begin) :
        """ If period BEGIN actually begins period SELF, returns the 
        complement of BEGIN in SELF; otherwise returns None """
        if (self.fx) :return(False)
        if self.start==begin.start and self.end >= begin.end : 
            return cperiod(begin.end,self.end)
    #
    def includes(self,included) :
        """ if period self does include period 'included', returns a pair of
        periods which represents the difference """
        if (self.fx) :return(False)
        #raise Climaf_Period_Error("Meaningless for period 'fx'")
        if self.start <= included.start and included.end <= self.end :
            return cperiod(self.start,included.start), cperiod(included.end,self.end)
    #
    def intersects(self,other) :
        """ 
        Returns the intersection of period self and period 'other' if any
        """
        if (self.fx) :
            raise Climaf_Period_Error("Meaningless for period 'fx'")
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
      dates (str): must match YYYY[MM[DD[HH[MM]]]][(-\|_)YYYY[MM[DD[HH[MM]]]]] , or
        be 'fx' for fixed fields

    Returns:
      the corresponding CliMAF 'period' object

    When using only YYYY, can omit some Ys (for zeros). 
    Cannot handle year 0000

    Examples :
    
    -  a one-year long period : '1980', or '1980-1980'
    -  a decade : '1980-1989'
    -  first millenium : 1-1000  # Must have leading zeroes if you want to quote a month
    -  first century : 1-100
    -  one month : '198005'
    -  two months : '198003-198004'
    -  one day : '17890714'
    -  the same single day, in a more complicated way : '17890714-17890714'

    CliMAF internally handles date-time values with a 1 minute accurracy; it can provide date
    information to external scripts in two forms; see keywords 'period' and 'period_iso' in
    :py:func:`~climaf.operators.cscript`
      
    """
    
    #clogger.debug("analyzing  %s"%dates)
    if not type(dates) is str :
        raise Climaf_Period_Error("arg is not a string : "+`dates`)
    if (dates == 'fx' ) : return cperiod('fx')
    
    start=re.sub(r'^([0-9]{1,12}).*',r'\1',dates)
    # Pad with leading 0 to reach a length of 4 characters
    start=(4-len(start))*"0"+start
    # TBD : check that start actually matches a date
    syear  =int(start[0:4])  
    smonth =int(start[4:6])  if len(start) > 5  else 1
    sday   =int(start[6:8])  if len(start) > 7  else 1
    shour  =int(start[8:10]) if len(start) > 9  else 0
    sminute=int(start[10:12])if len(start) > 11 else 0
    try :
        s=datetime.datetime(year=syear,month=smonth,day=sday,hour=shour,minute=sminute)
    except :
        raise Climaf_Period_Error("period start string %s is not a date (%s %s %s %s %s)"%(start,syear,smonth,sday,shour,sminute))
    #
    end=re.sub(r'.*[-_]([0-9]{1,12})$',r'\1',dates)
    end=(4-len(end))*"0"+end
    #clogger.debug("For dates=%s, start= %s, end=%s"%(dates,start,end))
    done=False
    if (end==dates) :
        # No string found for end of period
        if (len(start)<=4 ) : eyear=syear+1 ; emonth=1 ; eday=1 ; ehour=0 
        elif (len(start)==6 ) :
            eyear=syear ; emonth=smonth+1 ;
            if (emonth > 12) :
                emonth=1
                eyear=eyear+1
            eday=1 ; ehour=0 
        elif (len(start)==8 ) :
            eyear=syear ; emonth=smonth ; eday=sday ; ehour=0 
            if (sday > 27) :
                # Must use datetime for handling month length
                e=s+datetime.timedelta(1)
                done=True
            else : eday=sday+1
        elif (len(start)==10 ) :
            eyear=syear ; emonth=smonth ; eday=sday ; ehour=shour+1
            if (ehour > 23) :
                ehour=0
                eday=eday+1
        eminute = 0
    else:
        #clogger.debug("len(end)=%d"%len(end))
        if len(start) != len(end) :
            raise Climaf_Period_Error("Must have same numer of digits for start and end dates (%s and %s)"%(start,end))
        if (len(end)<12)  :
            eminute = 0
        else :
            eminute=int(end[10:12])
        if (len(end)==4 ) : eyear=int(end[0:4])+1 ; emonth=1 ; eday=1 ; ehour=0 
        elif (len(end)==6 ) :
            eyear=int(end[0:4]) ; emonth=int(end[4:6])+1 ; eday=1 ; ehour=0
            if (emonth > 12) :
                emonth=1
                eyear=eyear+1
        elif (len(end)==8 ) :
            eyear=int(end[0:4]) ; emonth=int(end[4:6]) ; eday=int(end[6:8])  ; ehour=0 
            if (eday > 27) :
                try :
                    #print "trying %d %d %d %d %d"%(eyear,emonth,eday,ehour,eminute)
                    e=datetime.datetime(year=eyear,month=emonth,day=eday,hour=ehour,minute=eminute)
                except:
                    raise Climaf_Period_Error("period end string %s is not a date"%end)
                e=e+datetime.timedelta(1)
                done=True
            else:
                eday=eday+1
        elif (len(end)==10 ) :
            eyear=int(end[0:4]) ; emonth=int(end[4:6]) ; eday=int(end[6:8])  ; ehour=int(end[8:10])+1 
            if (ehour > 23) :
                ehour=0
                eday=eday+1
        elif (len(end)==12 ) :
            eyear=int(end[0:4]) ; emonth=int(end[4:6]) ; eday=int(end[6:8])  ; ehour=int(end[8:10]) ; eminute=int(end[10:12])
    #
    if not done :
        try :
            #print "try:%d %02d %02d %02d %02d"%(eyear,emonth,eday,ehour,eminute)
            e=datetime.datetime(year=eyear,month=emonth,day=eday,hour=ehour,minute=eminute)
        except:
            raise Climaf_Period_Error("period end string %s is not a date"%end)
    if s < e :
        return cperiod(s,e,None)
    else :
        raise Climaf_Period_Error("Must have start ("+`s`+") before,(or equal to, end ("+`e`+")")


class Climaf_Period_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)
    def __str__(self):
        return `self.valeur`
