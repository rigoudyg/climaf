#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares a dummy project named 'file' which allows to describe dataset very simply from datafile using
function :py:func:`~climaf.classes.fds()`

Example for a dataset declaration ::

 >>> my_ds=fds('toto.nc',simulation='my_simu')


"""

from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *
from climaf.classes import cproject

cproject("file", "model", "path", separator="|")
