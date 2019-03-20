#!/usr/bin/python
# -*- coding: utf-8 -*-

# Retrieve input remote files in local (located at 'remote_cachedir')
# if necessary;
# and launch script 'mcdo.sh' with input local files
#
# Created : L.Vignon - 2017

import os, sys, subprocess, re, time, datetime
import ftplib as ftp
import getpass
import netrc
from dateutil import tz
from Tkinter import *

# Climaf
from climaf import __path__ as cpath, remote_cachedir
from climaf.clogging import clogger, dedent as cdedent
from climaf.dataloc import remote_to_local_filename

scriptpath=cpath[0]+"/../scripts/"

operator=sys.argv[1]
out=sys.argv[2]
var=sys.argv[3]
period=sys.argv[4]
region=sys.argv[5]
alias=sys.argv[6]
units=sys.argv[7]
vm=sys.argv[8]
files=sys.argv[9:]

# Dictionary of input files for each pair (host,user)
host_user=dict()

for i in files:
    if len(i.split(":")) == 3: k=1
    else: k=0
    host_key=i.split(":")[k].split("@")[-1]
    user_key=i.split(":")[k].split("@")[0]
    if re.findall("@",i.split(":")[k]):
        if not host_user.has_key((host_key,user_key)):
            host_user[(host_key,user_key)]=[]
        host_user[(host_key,user_key)].append(i.split(":")[-1])
    else:
        if not host_user.has_key((i.split(":")[k],'')): host_user[(i.split(":")[k],'')]=[]
        host_user[(i.split(":")[k],'')].append(i.split(":")[-1])


# 'dynamic_host' is an host with incremental files.
dynamic_host=['hendrix', 'beaufix']

# If one or all files returned by ds.baseFiles() are found in cache:
# - in case of a dynamic host, this file is only transferred if its date on server
# is more recent than that found in cache;
# - for other hosts, files found in cache are used

# Dictionary for each pair (host,user) of:
# - input files not found in cache for 'not-dynamic' host, so to retrieve;
# - and all input files for 'dynamic' host
host_user2=dict()

for host,username in host_user:
    if host not in dynamic_host:
        for ffile in host_user[host,username]:
            if not os.path.exists(os.path.expanduser(remote_cachedir)+'/'+host+ffile):
                if not host_user2.has_key((host,username)): host_user2[(host,username)]=[]
                host_user2[(host,username)].append(ffile)
    else:
        if not host_user2.has_key((host,username)): host_user2[(host,username)]=[]
        host_user2[(host,username)]=host_user[(host,username)]

if not os.path.exists(os.path.expanduser(remote_cachedir)): os.mkdir(os.path.expanduser(remote_cachedir))


secrets = netrc.netrc()
#netrc module does not handle multiple entries for a single host:
#If netrc file has two entries for the same host, the netrc module only returns the last entry.

def input_user_pass(host):
    """
    Prompt the user for entering login and corresponding password for host

    Return login and password given by user
    """
    Mafenetre = Tk()
    Mafenetre.title('Enter login and password for host %s:'%host)

    Login= StringVar()
    Motdepasse= StringVar()

    Label(Mafenetre,text="Enter login and pass:", fg='red', bg='white').pack(padx=5,pady=5)

    Frame1 = Frame(Mafenetre,borderwidth=2,relief=GROOVE)
    Frame1.pack(side=TOP,padx=10,pady=10)

    Frame11 = Frame(Frame1,borderwidth=2,relief=GROOVE, bg ='white')
    Frame11.pack(side=LEFT,padx=15,pady=15)
    Label(Frame11,text="Enter login:", fg="navy").pack(side=TOP,padx=10,pady=10)
    Label(Frame11,text="Enter pass:", fg="navy").pack(side=BOTTOM,padx=10,pady=10)

    Frame12 = Frame(Frame1,borderwidth=2,relief=GROOVE)
    Frame12.pack(side=RIGHT,padx=15,pady=15)
    Champ1 = Entry(Frame12, textvariable= Login, bg ='bisque', fg='maroon')
    Champ2 = Entry(Frame12, textvariable= Motdepasse, show='*', bg ='bisque', fg='maroon')
    Champ1.focus_set()
    Champ2.focus_set()
    Champ1.pack(side = TOP,padx = 5, pady = 5)
    Champ2.pack(side = BOTTOM,padx = 5, pady = 5)

    Frame3 = Frame(Mafenetre,borderwidth=2,relief=GROOVE)
    Frame3.pack(side = BOTTOM,padx=15,pady=15)
    Button(Frame3, text ='Valider', fg='navy', command = Mafenetre.destroy ).pack(side=BOTTOM,padx = 5, pady = 5)

    Mafenetre.mainloop()

    return(Login.get(), Motdepasse.get())


for host,username in host_user2:

# If 'user' is given:
#  - if 'host' is in $HOME/.netrc file, we check if corresponding 'login' is the same of 'user'. If it
#    is, we get associated password; otherwise it prompt the user for entering password;
#  - if 'host' is not present in $HOME/.netrc file, we prompt the user for entering password.
# If 'user' is not given:
#  - if 'host' is in $HOME/.netrc file, we get corresponding 'login' as 'user' and also get associated
#    password;
#  - if 'host' is not present in $HOME/.netrc file, we prompt the user for entering 'user' and 'password'.

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
            login, password= input_user_pass(host)

        connect=ftp.FTP(host,login,password)

    etat = connect.getwelcome()
    print 'Connect to host: %s'%host
    print etat

    for ffile in host_user2[host,username]:
        if not os.path.exists(os.path.expanduser(remote_cachedir)+'/'+host+ffile) or host in dynamic_host:
            filename=os.path.basename(ffile)
            dir=os.path.dirname(ffile)
            if not os.path.exists(os.path.expanduser(remote_cachedir)+'/'+host+dir):
                os.makedirs(os.path.expanduser(remote_cachedir)+'/'+host+dir)
            connect.cwd(dir)
            if host in dynamic_host and \
               os.path.exists(os.path.expanduser(remote_cachedir)+'/'+host+ffile):
                filetransfer=False
                resp=connect.sendcmd("MDTM %s" %filename)
                if resp[0] == '2':
                    remote_timestamp = time.mktime(datetime.datetime.strptime(resp[4:18],"%Y%m%d%H%M%S").timetuple())
                    local_file_datetime=datetime.datetime.fromtimestamp(os.stat(os.path.expanduser(remote_cachedir)+\
                                '/'+host+ffile).st_mtime)
                    local_file_ut_datetime=local_file_datetime.replace(tzinfo=tz.tzlocal()).astimezone(tz.gettz('UTC'))
                    if time.mktime(local_file_ut_datetime.timetuple()) >= remote_timestamp:
                        print 'Most recent file found in cache: %s is at %s \n'%\
                            (ffile,os.path.expanduser(remote_cachedir)+'/'+host+ffile)
                    else:
                        print 'File found in cache %s is older than %s \n'%\
                            (os.path.expanduser(remote_cachedir)+'/'+host+ffile,ffile)
                        filetransfer=True
#                        connect.retrbinary('RETR '+filename, open(os.path.expanduser(remote_cachedir)+'/'+host+ffile, 'wb').write)
#                        os.utime(os.path.expanduser(remote_cachedir)+'/'+host+ffile, (timestamp, timestamp))
                else: filetransfer=True
            if ( host in dynamic_host and \
                 os.path.exists(os.path.expanduser(remote_cachedir)+'/'+host+ffile) and \
                 filetransfer ) or \
                 not os.path.exists(os.path.expanduser(remote_cachedir)+'/'+host+ffile) :
                print 'File %s transfered \n'%ffile
                connect.retrbinary('RETR '+filename, open(os.path.expanduser(remote_cachedir)+'/'+host+ffile, 'wb').write)
                #if host in dynamic_host and filetransfer: os.utime(os.path.expanduser(remote_cachedir)+'/'+host+ffile, (timestamp, timestamp))

        else:
            print 'File found in cache: %s is at %s \n'%(ffile,os.path.expanduser(remote_cachedir)+'/'+host+ffile)

    connect.quit()


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
except:
    raise Climaf_Script_Error("Issue when executing: %s"%' '.join(args))
