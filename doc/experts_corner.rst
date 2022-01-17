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

For that, type :

>>> env.clogging.clogger=env.clogging.log_e()

And reset the verbosity level for CliMAF log messages on stderr
and/or for log file; e.g.

>>> clog(level="info")  
>>> clog_file(level="info")
>>> csync() # For an example of log message
[csync      : cache.py  , L. 348 ] : info     : No cache index file yet

If you want to return back to the standard format, you have to proceed in
the same way but with the function 'climaf.clogging.log_l()', i.e. : 

>>> env.clogging.clogger=env.clogging.log_l()
>>> clog(level="info")  
>>> clog_file(level="info")
>>> csync() # For an example
info     : No cache index file yet

