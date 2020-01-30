#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cdms2
import cdutil
# from pcmdi_metrics.pcmdi.pmp_parser import *
import genutil

from climaf.site_settings import atCerfacs

# import argparse
# parser = argparse.ArgumentParser(description='Linear Regression between X and Y')
# parser = PMPParser()

from optparse import OptionParser

desc = " "
parser = OptionParser(" ")
parser.set_usage("%%prog [-h]\n%s" % desc)

parser.add_option('--X',
                  dest='xfile',
                  help='X is the netcdf file in the equation Y = aX + b')
parser.add_option('--Y',
                  dest='yfile',
                  help='Y is the netcdf file in the equation Y = aX + b')
parser.add_option('--xvariable',
                  dest='xvariable',
                  help='Variable to reach in X')
parser.add_option('--yvariable',
                  dest='yvariable',
                  help='Variable to reach in Y')
parser.add_option('--outfile',
                  dest='outfile',
                  help='Name of the out file')

(opts, args) = parser.parse_args()

xfile = opts.xfile
yfile = opts.yfile
xvariable = opts.xvariable
yvariable = opts.yvariable
outfile = opts.outfile

# parser.add_argument('--X',
#                    dest='xfile',
#                    required=True,
#                    help='X is the netcdf file in the equation Y = aX + b')
# parser.add_argument('--Y',
#                    dest='yfile',
#                    required=True,
#                    help='Y is the netcdf file in the equation Y = aX + b')
# parser.add_argument('--xvariable',
#                    dest='xvariable',
#                    required=True,
#                    help='Variable to reach in X')
# parser.add_argument('--yvariable',
#                    dest='yvariable',
#                    help='Variable to reach in Y')
# parser.add_argument('--outfile',
#                    dest='outfile',
#                    required=True,
#                    help='Name of the out file')

# parameters = parser.get_parameter()


# xfile = parameters.xfile
# yfile = parameters.yfile
# xvariable = parameters.xvariable
# yvariable = parameters.yvariable
# outfile = parameters.outfile


# -- X
ncxfile = cdms2.open(xfile)
xdat = ncxfile(xvariable)

xlon = xdat.getLongitude()
xlat = xdat.getLatitude()
xlon.id = 'lon'
xlat.id = 'lat'

# if type(xlon)!=cdms2.coord.TransientAxis2D and type(xlat)!=cdms2.coord.TransientAxis2D:
if len(xlon) == 1 and len(xlat) == 1:
    xdat = xdat[:, 0, 0]

# -- Y
ncyfile = cdms2.open(yfile)
ydat = ncyfile(yvariable)
ylon = ydat.getLongitude()
ylat = ydat.getLatitude()

# if type(ylon)!=cdms2.coord.TransientAxis2D and type(ylat)!=cdms2.coord.TransientAxis2D:
if len(ylon) == 1 and len(ylat) == 1:
    ydat = ydat[:, 0, 0]

# -- Compute the linear regression

result = genutil.statistics.linearregression(y=ydat, x=xdat, nointercept=1)

# -- Save the results
# result.coordinates = 'Longitude Latitude'
result.coordinates = 'lon lat'
result.longname = 'Linear regression slope'
# result.units = 'Y('+ydat.id+'['+ydat.units+'])/X('+xdat.id+'['+xdat.units+'])'
result.units = 'Y/X'
# atCerfacs
if not atCerfacs:
    cdms2.setNetcdf4Flag(1)

out = cdms2.open(outfile, 'w')
# if type(xlon)!=cdms2.coord.TransientAxis2D and type(xlat)!=cdms2.coord.TransientAxis2D:
# if len(xlon)==2 and len(xlat)==2:
if len(xlon) == 1 and len(xlat) == 1:
    print 'Using coordinates of ylon and ylat'
    print 'ylon = ', ylon
    print 'ylat = ', ylat
    if type(ylon) == cdms2.coord.TransientAxis2D:
        out.write(ylon)
        out.write(ylat)
    else:
        result.setAxis(0, ylat)
        result.setAxis(1, ylon)

# if type(ylon)!=cdms2.coord.TransientAxis2D and type(ylat)!=cdms2.coord.TransientAxis2D:
if len(ylon) == 1 and len(ylat) == 1:
    print 'Using coordinates of xlon and xlat'
    print 'xlon = ', xlon
    print 'xlat = ', xlat
    if type(xlon) == cdms2.coord.TransientAxis2D:
        out.write(xlon)
        out.write(xlat)
    else:
        result.setAxis(0, xlat)
        result.setAxis(1, xlon)
    #   out.write(cdms2.coord.TransientAxis2D(xlon))
    #   out.write(cdms2.coord.TransientAxis2D(xlat))

out.write(result)
out.close()
