"""
Standard site settings for working with CliMAF.

"""

import os

atCNRM   = False
onCiclad = False
atTGCC   = False
onAda    = False
onErgon  = False
atIDRIS  = False
onSpip   = False

HostName = os.uname()[1].strip().lower()
Home    = os.getenv ('HOME')

print 'Hostname:', HostName

if os.path.exists ('/ccc')  :
    atTGCC   = True
if os.path.exists ('/cnrm') :
    atCNRM   = True
if 'ciclad' in HostName     :
    onCiclad = True
if 'ada' in HostName        :
    onAda    = True   ; atIDRIS = True
if 'ergon' in HostName      :
    onErgon  = True   ; atIDRIS = True
if 'Spip' in HostName or 'lsce3005' in HostName or 'lsce3072' in HostName or os.path.exists(Home+'/.spip') :
    onSpip = True
    print 'Spip trouve'
    VolumesDir = os.getenv ('VolumesDir')


