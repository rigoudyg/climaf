e1=ds(project="CMIP5",experiment='historical',variable='ta',frequency='monthly',period='1975',rip="*")

e1=ds(project="CMIP5",experiment=['historical','histnat','histant','histGHG'],variable='ta',frequency='monthly',period='1975',rip='r1i1p1')

#import sys; sys.path.append("/home/stephane/Bureau/climaf")
from climaf.api import *
from climaf.classes import cens
craz()

j0=ds(project='example',experiment="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1980")
j1=ds(project='example',experiment="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1981")
#j2=ds(project='example',experiment="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1982")
e2=cens(j0,j1,labels=['1980','1981'])
m=ccdo(e2,operator='zonmean')

- capply : si squeez_ens -> cobject, sinon -> ensemble (par itération)

1° obj : fonction 'ensemble' et script qui squeeze