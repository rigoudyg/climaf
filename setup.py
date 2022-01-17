#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = __import__('climaf').version
description = 'CliMAF: a Climate Model Assessment Framework.'
long_description = (
    open('README.rst').read()
)

requires = [line.strip() for line in open('requirements.txt')]

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    # 'License :: CeCILL-C Free Software License Agreement (CECILL-C)'
]

setup(name='climaf',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=classifiers,
      keywords='python climate model',
      author='Stéphane Sénési',
      author_email="",
      url='https://github.com/rigoudyg/climaf',
      license="CeCILL-C license",
      packages=find_packages(),
      include_package_data=True,
      install_requires=requires,
      test_suite="tests",
      data_files=[
          ("scripts", ["scripts/ml2pl", ])
      ],
      scripts=[
          'bin/climaf',
          'bin/pdfcrop',
          'bin/exiv2',
          'scripts/cdfsectionsm.sh',
          'scripts/cdfsections.sh',
          'scripts/cdftransport.sh',
          'scripts/cdftransp.sh',
          'scripts/clean_pdf.sh',
          'scripts/curl_tau_atm.jnl',
          'scripts/curves.ncl',
          'scripts/ensemble_time_series_plot.py',
          'scripts/gplot.ncl',
          'scripts/hovmoller.ncl',
          'scripts/ks.sh',
          'scripts/LinearRegression_UVCDAT.py',
          'scripts/mcdo_remote.py',
          'scripts/mcdo.sh',
          'scripts/mcdo_aux.sh',
          'scripts/mcdo.py',
          'scripts/mean_and_std.sh',
          'scripts/ml2pl.sh',
          'scripts/mtimavg.sh',
          'scripts/plot_cross_section.ncl',
          'scripts/plotmap.ncl',
          'scripts/read_ncks.sh',
          'scripts/regridll.sh',
          'scripts/regrid.sh',
          'scripts/time_average_basics.sh',
          'scripts/wcdo.sh',
      ],
      )
