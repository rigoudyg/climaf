"""
Standard site settings for working with CliMAF.

"""

import os

atCNRM   = False
atCerfacs= False
atIPSL   = False
onCiclad = False
atTGCC   = False
onAda    = False
onErgon  = False
atIDRIS  = False
onSpip   = False

HostName = os.uname()[1].strip().lower()
Home    = os.getenv ('HOME')

#print 'Hostname:', HostName

if os.path.exists ('/ccc') and not os.path.exists ('/data')  :
    atTGCC   = True
    atIPSL   = True
if os.path.exists ('/cnrm') :
    atCNRM   = True
if 'ciclad' in HostName   or 'ipsl.polytechnique.fr' in HostName  :
    onCiclad = True
    atIPSL   = True
if 'ada' in HostName        :
    onAda    = True   ; atIDRIS = True
    atIPSL   = True
if 'ergon' in HostName      :
    onErgon  = True   ; atIDRIS = True
    atIPSL   = True
if 'Spip' in HostName or 'lsce3005' in HostName or 'lsce3072' in HostName or os.path.exists(Home+'/.spip') :
    onSpip = True
    atIPSL   = True
    print 'Spip trouve'
    VolumesDir = os.getenv ('VolumesDir')
if os.path.exists('/data8/datamg/') :
    atCerfacs=True

    
