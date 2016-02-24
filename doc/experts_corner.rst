.. _experts_corner:

---------------
Experts' corner
---------------

..to change formatter for log messages on stderr and log file
--------------------------------------------------------------

The Formatter of the Logger is initialized with the format string: 
'%(levelname)-8s : %(message)s'. 

If you want to have a more verbose Formatter, the function
'climaf.clogging.log_e()' allows to switch with the following format
string: 

'[%(funcName)-10.10s : %(filename)-10s, L. %(lineno)-4d] :
%(levelname)-8s : %(message)s'  

For it, you have to do what follows :

>>> climaf.clogging.clogger=climaf.clogging.log_e()
>>> # And resets the verbosity level for CliMAF log messages on stderr
>>> # and/or for log file
>>> clog(level="info")  # level among "debug", "info", "warning", "critical"
>>> clog_file(level="info")
>>> # An example to have a look to the format for log messages
>>> csync()
[csync      : cache.py  , L. 348 ] : info     : No cache index file yet

If you want to return in the standard format, you have to proceed in
the same way but with the function 'climaf.clogging.log_l()', i.e. : 

>>> climaf.clogging.clogger=climaf.clogging.log_l()
>>> # And resets the verbosity level for CliMAF log messages on stderr
>>> # and/or for log file
>>> clog(level="info")  # level among "debug", "info", "warning", "critical"
>>> clog_file(level="info")
>>> # An example to have a look to the format for log messages
>>> csync()
info     : No cache index file yet

