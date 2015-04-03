import logging

def log_l():
    global formatter
    logger = logging.getLogger('')
    # create formatter
    formatter = logging.Formatter('\n[%(funcName)-10.10s : %(filename)-10s, L. %(lineno)-4d] : %(levelname)-8s : %(message)s')
    return logger
    
clogger=log_l()

def clog(arg) :
    """
    Sets the verbosity level for CliMAF log messages on stderr.

    Among : logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL

    """
    clogger.setLevel(arg) 
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


def clog_file(argf) :
    """
    Sets the verbosity level for CliMAF log messages on file climaf.log

    Among : logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL
    """
    exist_file_handler=False
    for h in clogger.handlers :
        if type(h) is logging.FileHandler :
            #print "il existe deja un FileHandler => on change le niveau d informations", h
            h.setLevel(argf)
            exist_file_handler=True    
            
    if exist_file_handler==False:
        #print "ajout d un FileHandler"
        fh = logging.FileHandler('climaf.log',mode='w') 
        fh.setLevel(argf)
        fh.setFormatter(formatter)
        clogger.addHandler(fh)
