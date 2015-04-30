from climaf.api import *
#clog('debug')
clog_file('debug')

cdef("frequency","monthly")
cdef("period","1980-1981")
tas_ds=ds(project='example', experiment="AMIPV6ALB2G", variable="tas")
tas_ds
tas_ds.baseFiles()
cfile(tas_ds)

tas_avg=time_average(tas_ds)
cfile(tas_avg)

#Quelques tests sur clist pour tester sa robustesse
clist()
clist(size="3M", age="-1")
clist(size="3", age="-1", access=1)
clist(size="3", age="-1", pattern= "ds")
clist(size="3", age="-1", pattern= "lb")
clist(size="3", age="+1", pattern= "lb")
clist(size="3", age="+1", pattern= "ds")
clist(size="3", age="-1", not_pattern= "lb")
clist(size="3", age="-1", not_pattern= "ds")
clist(size="3", age="-1", not_pattern= "ds", usage=True)
clist(size="3", age="-1", not_pattern= "lb", usage=True)
clist(size="3", age="-1", not_pattern= "lb", usage=True, count=True)
clist(size="3", age="-1", not_pattern= "lb", count=True)
clist(size="3", age="-1", not_pattern= "lb", count=True, CRS=True)

cls()
crm()
cdu()
cwc()
