import logging

logdir="."

class MyFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return logging.Formatter.format(self, record)

def log_l():
    global formatter
    logger = logging.getLogger('')
    # create formatter
    formatter = MyFormatter('%(levelname)-8s : %(message)s')#logging.Formatter
    return logger

def log_e():
    global formatter
    logger = logging.getLogger('')
    # create formatter
    formatter = MyFormatter('[%(funcName)-10.10s : %(filename)-10s, L. %(lineno)-4d] : %(levelname)-8s : %(message)s')#logging.Formatter
    return logger

clogger=log_l()

def clog(level=None) :
    """
    Sets the verbosity level for CliMAF log messages on stderr.

    Args:
     level(str) : among : \"debug\", \"info\", \"warning\", \"critical\"

    Note : at CliMAF startup, the level is set to the value of envrionment variable $CLIMAF_LOG_LEVEL

    """
    if (level) : clogger.setLevel(transl(level)) 
    exist_stream_handler=False
    for h in clogger.handlers :
        if type(h) is logging.StreamHandler :
            #print "il existe deja un StreamHandler => on change le niveau d informations et on formatte le msg ", h
            #clogger.setLevel(arg) 
            h.setFormatter(formatter)
            exist_stream_handler=True    
            
    if not exist_stream_handler :
        #print "ajout d un StreamHandler"
        console = logging.StreamHandler()
        #console.setLevel(arg)
        console.setFormatter(formatter)
        clogger.addHandler(console)


def clog_file(level=None) :
    """
    Sets the verbosity level for CliMAF log messages on file CLIMAF_LOG_DIR/climaf.log

   Args:
     level(str) : among : \"debug\", \"info\", \"warning\", \"critical\"

    Note : at CliMAF startup, the level is set to the value of environment variable $CLIMAF_LOGFILE_LEVEL

    """
    exist_file_handler=False
    for h in clogger.handlers :
        if type(h) is logging.FileHandler :
            #print "il existe deja un FileHandler => on change le niveau d informations", h
            if level : h.setLevel(transl(level))
            h.setFormatter(formatter)
            exist_file_handler=True    
            
    if exist_file_handler==False:
        #print "ajout d un FileHandler"
        fh = logging.FileHandler(logdir+"/"+'climaf.log',mode='w') 
        if level : fh.setLevel(transl(level))
        fh.setFormatter(formatter)
        clogger.addHandler(fh)

def indent():
    """ 
    Forces log messages to be indented by one more TAB
    """
    global formatter
    form="\t"+getattr(formatter,'_fmt')
    formatter = MyFormatter(form)#logging.Formatter(form)
    clog()
    clog_file()

def dedent(n=1):
    """ 
    Forces log messages to be de-indented by one or more TAB
    """
    global formatter
    form=getattr(formatter,'_fmt').replace("\t","",n)
    formatter = MyFormatter(form)#logging.Formatter(form)
    clog()
    clog_file()

def transl(level) :
    if type(level) is str:
        if level.lower()=='debug': return logging.DEBUG
        elif level.lower()=='critical': return logging.CRITICAL
        elif level.lower()=='info': return logging.INFO
        elif level.lower()=='warning': return logging.WARNING
        elif level.lower()=='error': return logging.ERROR
    else : return level
