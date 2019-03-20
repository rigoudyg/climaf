#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module declares a dummy project named 'file' which allows to describe dataset very simply from datafile using fucntion :py:func:`~climaf.classes.fds()`

Example for a dataset declaration ::

 >>> my_ds=fds('toto.nc',simulation='my_simu')


"""

from climaf.classes import cproject

cproject("file" ,"model","path",separator="|")

