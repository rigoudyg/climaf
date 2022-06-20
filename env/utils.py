#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standard site settings for working with CliMAF.

"""

from __future__ import print_function, division, unicode_literals, absolute_import

import subprocess


def get_subprocess_output(command, to_replace=list()):
	rep = subprocess.check_output(command, shell=True).decode("utf-8")
	for (rep1, rep2) in to_replace:
		rep.replace(rep1, rep2)
	return rep
