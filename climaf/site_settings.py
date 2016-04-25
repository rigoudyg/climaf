"""
Standard site settings for working with CliMAF.

"""

import os

atCNRM=False
onCiclad=False
atTGCC=False
atCerfacs=False

if os.path.exists('/ccc'):
    atTGCC=True
elif os.path.exists('/cnrm'):
    atCNRM=True
elif os.path.exists('/prodigfs') :
    onCiclad=True
elif os.path.exists('/data8/datamg/') :
    atCerfacs=True

    
