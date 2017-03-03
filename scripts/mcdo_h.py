import os, sys, subprocess, re
import ftplib as ftp
import getpass
import netrc

# Climaf 
from climaf import __path__ as cpath, cachedir
from climaf.clogging import clogger, dedent as cdedent

scriptpath=cpath[0]+"/../scripts/" 
remote_cachedir=os.path.expanduser(cachedir)+'/remote_data'

operator=sys.argv[1]
out=sys.argv[2]
var=sys.argv[3]
period=sys.argv[4]
region=sys.argv[5]
alias=sys.argv[6]
units=sys.argv[7]
vm=sys.argv[8]
files=sys.argv[9:]

host_user=dict()

for i in files:
    for el in i.split(":"):
        if re.findall("@",el):
            if not host_user.has_key((el.split("@")[-1],el.split("@")[0])):
                host_user[(el.split("@")[-1],el.split("@")[0])]=[]
            host_user[(el.split("@")[-1],el.split("@")[0])].append(i.split(":")[-1])

if not os.path.exists(remote_cachedir): os.mkdir(remote_cachedir)

for host,username in host_user:
    
    secrets = netrc.netrc()
    #netrc module does not handle multiple entries for a single host:
    #If netrc file has two entries for the same host, the netrc module only returns the last entry.

    if username:        
        if host in secrets.hosts:
            login, account, password = secrets.authenticators( host )
            if login != username: password = getpass.getpass("Password for host '%s' and user '%s': "%(host,username))
        else:
            password = getpass.getpass("Password for host '%s' and user '%s': "%(host,username))            
        connect=ftp.FTP(host,username,password)
    else:
        if host in secrets.hosts:
            login, account, password = secrets.authenticators( host )
        else:
            login = raw_input('Enter login : ')
            password = getpass.getpass("Password for host '%s' and user '%s': "%(host,login))
        connect=ftp.FTP(host,login,password)
        
    #etat = connect.getwelcome()
    
    for ffile in host_user[host,username]:
        dir=os.path.dirname(ffile)
        filename=os.path.basename(ffile)   
        if not os.path.exists(remote_cachedir+'/'+host+dir): os.makedirs(remote_cachedir+'/'+host+dir)
        connect.cwd(dir)        
        connect.retrbinary('RETR '+filename, open(remote_cachedir+'/'+host+ffile, 'wb').write)

    connect.quit()


def remote_to_local_filename(url):
    """
    url: an url of remote data

    Return local filename of remote file
    """
    for el in url.split(":"):
        if re.findall("@",el):
            hostname=el.split("@")[-1]
            local_filename=remote_cachedir+'/'+hostname+os.path.abspath(url.split(":")[-1])
            return(local_filename)

loc_files=[]
for i in files: loc_files.append(remote_to_local_filename(i))

args=[scriptpath+"mcdo.sh","%s"%operator, "%s"%out, "%s"%var, "%s"%period, "%s"%region,"%s"%alias, "%s"%units, "%s"%vm,"%s"%' '.join(loc_files)]


class Climaf_Script_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        cdedent(100)
    def __str__(self):
         return `self.valeur`


try:
    comm=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print "Remote files %s were saved as local files as %s"%(files,loc_files)
    clogger.info("Remote files %s were saved as local files as %s"%(files,loc_files))
except:
    raise Climaf_Script_Error("Issue when executing: %s"%' '.join(args))
    #clogger.error("Issue when executing: %s"%' '.join(args))
