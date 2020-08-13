#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Retrieve input remote files in local (located at 'remote_cachedir')
# if necessary;
# and launch script 'mcdo.sh' with input local files
#
# Created : L.Vignon - 2017

from __future__ import print_function, division, unicode_literals, absolute_import

import os
import sys
import subprocess
import re
import time
import datetime
import ftplib as ftp
import getpass
import netrc
from dateutil import tz
import future
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter
import argparse
from collections import defaultdict
import mcdo

# Climaf
from climaf import __path__ as cpath, remote_cachedir
from env.clogging import clogger, dedent as cdedent
from climaf.dataloc import remote_to_local_filename

scriptpath = cpath[0] + "/../scripts/"

parser = argparse.ArgumentParser()
parser.add_argument("input_files", action="append")
parser.add_argument("--operator", help="Operator to be applied")
parser.add_argument("--apply_operator_after_merge", type=bool, default=True,
                    help="If True, the operator is applied after merge time. If false, it is applied before.")
parser.add_argument("--output_file", help="Name of the output file")
parser.add_argument("--var", help="Variable to be considered")
parser.add_argument("--period", help="Period to be considered")
parser.add_argument("--region", type=list,
                    help="Region to be considered, i.e. latmin,latmax,lonmin,lonmax")
parser.add_argument("--alias", help="Alias to be used")
parser.add_argument("--units", help="Units of the variable")
parser.add_argument("--vm", help="")

args = parser.parse_args()

operator = args.operator
out = args.output_file
var = args.var
period = args.period
region = args.region
alias = args.alias
units = args.units
vm = args.vm
files = args.input_file

# Dictionary of input files for each pair (host,user)
host_user = defaultdict(list)

for i in files:
    infos = i.split(":")
    if len(infos) == 3:
        k = 1
    else:
        k = 0
    if '@' in infos[k]:
        user_key, host_key = infos[k].split("@")
        host_user[(host_key, user_key)].append(infos[-1])
    else:
        host_user[(infos[k], '')].append(infos[-1])

# 'dynamic_host' is an host with incremental files.
dynamic_host = ['hendrix', 'beaufix']

# If one or all files returned by ds.baseFiles() are found in cache:
# - in case of a dynamic host, this file is only transferred if its date on server
# is more recent than that found in cache;
# - for other hosts, files found in cache are used

# Dictionary for each pair (host,user) of:
# - input files not found in cache for 'not-dynamic' host, so to retrieve;
# - and all input files for 'dynamic' host
host_user2 = defaultdict(list)

for host, username in host_user:
    if host not in dynamic_host:
        for ffile in host_user[host, username]:
            if not os.path.exists(os.path.expanduser(remote_cachedir) + '/' + host + ffile):
                host_user2[(host, username)].append(ffile)
    else:
        host_user2[(host, username)] = host_user[(host, username)]

if not os.path.exists(os.path.expanduser(remote_cachedir)):
    os.mkdir(os.path.expanduser(remote_cachedir))

secrets = netrc.netrc()


# netrc module does not handle multiple entries for a single host:
# If netrc file has two entries for the same host, the netrc module only returns the last entry.

def input_user_pass(host):
    """
    Prompt the user for entering login and corresponding password for host

    Return login and password given by user
    """
    Mafenetre = tkinter.Tk()
    Mafenetre.title('Enter login and password for host %s:' % host)

    Login = tkinter.StringVar()
    Motdepasse = tkinter.StringVar()

    tkinter.Label(Mafenetre, text="Enter login and pass:", fg='red', bg='white').pack(padx=5, pady=5)

    Frame1 = tkinter.Frame(Mafenetre, borderwidth=2, relief=tkinter.GROOVE)
    Frame1.pack(side=tkinter.TOP, padx=10, pady=10)

    Frame11 = tkinter.Frame(Frame1, borderwidth=2, relief=tkinter.GROOVE, bg='white')
    Frame11.pack(side=tkinter.LEFT, padx=15, pady=15)
    tkinter.Label(Frame11, text="Enter login:", fg="navy").pack(side=tkinter.TOP, padx=10, pady=10)
    tkinter.Label(Frame11, text="Enter pass:", fg="navy").pack(side=tkinter.BOTTOM, padx=10, pady=10)

    Frame12 = tkinter.Frame(Frame1, borderwidth=2, relief=tkinter.GROOVE)
    Frame12.pack(side=tkinter.RIGHT, padx=15, pady=15)
    Champ1 = tkinter.Entry(Frame12, textvariable=Login, bg='bisque', fg='maroon')
    Champ2 = tkinter.Entry(Frame12, textvariable=Motdepasse, show='*', bg='bisque', fg='maroon')
    Champ1.focus_set()
    Champ2.focus_set()
    Champ1.pack(side=tkinter.TOP, padx=5, pady=5)
    Champ2.pack(side=tkinter.BOTTOM, padx=5, pady=5)

    Frame3 = tkinter.Frame(Mafenetre, borderwidth=2, relief=tkinter.GROOVE)
    Frame3.pack(side=tkinter.BOTTOM, padx=15, pady=15)
    tkinter.Button(Frame3, text='Valider', fg='navy', command=Mafenetre.destroy).pack(side=tkinter.BOTTOM, padx=5,
                                                                                      pady=5)

    Mafenetre.mainloop()

    return Login.get(), Motdepasse.get()


for host, username in host_user2:

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
            login, account, password = secrets.authenticators(host)
            if login != username:
                password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))
        else:
            password = getpass.getpass("Password for host '%s' and user '%s': " % (host, username))
        connect = ftp.FTP(host, username, password)
    else:
        if host in secrets.hosts:
            login, account, password = secrets.authenticators(host)
        else:
            login, password = input_user_pass(host)

        connect = ftp.FTP(host, login, password)

    etat = connect.getwelcome()
    print('Connect to host: %s' % host)
    print(etat)

    for ffile in host_user2[host, username]:
        if not os.path.exists(os.path.expanduser(remote_cachedir) + '/' + host + ffile) or host in dynamic_host:
            filename = os.path.basename(ffile)
            dir = os.path.dirname(ffile)
            if not os.path.exists(os.path.expanduser(remote_cachedir) + '/' + host + dir):
                os.makedirs(os.path.expanduser(remote_cachedir) + '/' + host + dir)
            connect.cwd(dir)
            if host in dynamic_host and \
                    os.path.exists(os.path.expanduser(remote_cachedir) + '/' + host + ffile):
                filetransfer = False
                resp = connect.sendcmd("MDTM %s" % filename)
                if resp[0] == '2':
                    remote_timestamp = time.mktime(datetime.datetime.strptime(resp[4:18], "%Y%m%d%H%M%S").timetuple())
                    local_file_datetime = datetime.datetime.fromtimestamp(os.stat(os.path.expanduser(remote_cachedir)
                                                                                  + '/' + host + ffile).st_mtime)
                    local_file_ut_datetime = local_file_datetime.replace(tzinfo=tz.tzlocal()).astimezone(
                        tz.gettz('UTC'))
                    if time.mktime(local_file_ut_datetime.timetuple()) >= remote_timestamp:
                        print('Most recent file found in cache: %s is at %s \n' %
                              (ffile, os.path.expanduser(remote_cachedir) + '/' + host + ffile))
                    else:
                        print('File found in cache %s is older than %s \n' %
                              (os.path.expanduser(remote_cachedir) + '/' + host + ffile, ffile))
                        filetransfer = True
                #                        connect.retrbinary('RETR '+filename, open(os.path.expanduser(remote_cachedir)+
                #                        '/'+host+ffile, 'wb').write)
                #                        os.utime(os.path.expanduser(remote_cachedir)+'/'+host+ffile, (timestamp,
                #                                                                                      timestamp))
                else:
                    filetransfer = True
            if (host in dynamic_host
                and os.path.exists(os.path.expanduser(remote_cachedir) + '/' + host + ffile) and filetransfer)\
                    or not os.path.exists(os.path.expanduser(remote_cachedir) + '/' + host + ffile):
                print('File %s transfered \n' % ffile)
                connect.retrbinary('RETR ' + filename,
                                   open(os.path.expanduser(remote_cachedir) + '/' + host + ffile, 'wb').write)
                # if host in dynamic_host and filetransfer: os.utime(os.path.expanduser(remote_cachedir)+'/'+host+ffile,
                #  (timestamp, timestamp))

        else:
            print('File found in cache: %s is at %s \n' % (ffile,
                                                           os.path.expanduser(remote_cachedir) + '/' + host + ffile))

    connect.quit()


loc_files = [remote_to_local_filename(url) for url in files]


class Climaf_Script_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        cdedent(100)

    def __str__(self):
        return repr(self.valeur)


try:
    mcdo.main(operator=operator, output_file=out, variable=var, period=period, region=region, alias=alias, units=units,
              vm=vm, input_files=loc_files)
    comm = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Remote files %s were saved as local files as %s" % (files, loc_files))
except:
    raise Climaf_Script_Error("Issue when executing: %s" % ' '.join(args))
