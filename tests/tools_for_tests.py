#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools to deal with tests.
"""

from __future__ import unicode_literals, absolute_import, print_function, division

import os
import subprocess
import unittest
import re
import sys
import six

from climaf.api import cshow, ncview, cfile
from climaf import xdg_bin
from env.environment import *


def skipUnless_CNRM_Lustre():
    if os.path.exists('/cnrm/cmip'):
        return lambda func: func
    return unittest.skip("because CNRM's Lustre not available")


def skipUnless_Ciclad():
    if os.path.exists('/prodigfs') or os.path.exists('/home/senesi/tmp/ciclad/prodigfs/esg/CMIP5'):
        return lambda func: func
    return unittest.skip("because not on Ciclad")


def remove_dir_and_content(dirname):
    if os.path.isdir(dirname):
        # Deal with files
        listfiles = list()
        listdirs = list()
        for (d, subdirs, files) in os.walk(dirname):
            for name in files:
                listfiles.append(os.path.sep.join([d, name]))
            for subd in subdirs:
                listdirs.append(os.path.sep.join([d, subd]))
        for f in listfiles:
            os.remove(f)
        # Deal with subdirectories
        for d in sorted(listdirs, reverse=True):
            os.rmdir(d)


def get_figures_and_content_from_html(html_file, regexp, patterns_to_exclude=list()):
    with open(html_file, "r") as fic:
        content = fic.read()
    list_figures = list()
    list_replacement = list()
    for regexp_match in regexp.finditer(content):
        value = regexp_match.groupdict()["value"]
        list_replacement.append(value)
        if not value.startswith(os.sep):
            value = os.sep.join([os.path.dirname(html_file), value])
        if value not in list_figures and not any([p in value for p in patterns_to_exclude]):
            list_figures.append(value)
    for fig in list(set(list_replacement)):
        content = content.replace(fig, "FIGURE")
    return list_figures, content


def compare_html_files(file_test, file_ref):
    if not os.path.exists(file_test) or not os.path.exists(file_ref):
        raise OSError("Check files existence: %s - %s" % (file_test, file_ref))
    if file_ref.split(".")[-1] != "html":
        raise ValueError("This function only apply to html files.")
    if file_test.split(".")[-1] != file_ref.split(".")[-1]:
        raise ValueError("Files have different formats: %s / %s" % (os.path.basename(file_test),
                                                                    os.path.basename(file_ref)))
    fig_regexp = re.compile(r'(HREF|SRC)="(?P<value>[^"]*\.png)"')
    patterns_to_exclude = ["Logo-CliMAF-compact.png", ]
    list_figures_test, content_test = get_figures_and_content_from_html(file_test, fig_regexp, patterns_to_exclude)
    list_figures_ref, content_ref = get_figures_and_content_from_html(file_ref, fig_regexp, patterns_to_exclude)
    if content_test != content_ref:
        raise ValueError("The content of files %s and %s are different\n%s\n!=\n%s" % (file_test, file_ref,
                                                                                       content_test, content_ref))
    if len(list_figures_ref) != len(list_figures_test):
        raise ValueError("The number of figures if different in %s and %s" % (file_test, file_ref))
    for (fig_ref, fig_test) in zip(list_figures_ref, list_figures_test):
        compare_picture_files(fig_test, fig_ref)


def compare_text_files(file_test, file_ref, **kwargs):
    if not os.path.exists(file_test) or not os.path.exists(file_ref):
        raise OSError("Check files existence: %s - %s" % (file_test, file_ref))
    with open(file_test, "r") as fic:
        content_test = fic.read()
    with open(file_ref, "r") as fic:
        content_ref = fic.read()
    for (key, value) in kwargs.items():
        content_test = content_test.replace(key, value)
        content_ref = content_ref.replace(key, value)
    content_test = re.sub(os.path.sep.join([os.environ.get("TMPDIR", "/tmp"), "climaf_\w+"]), "/tmp/climaf_XXX",
                          content_test)
    if content_test != content_ref:
        raise ValueError("The content of files %s and %s are different:\n%s\n%s" % (file_test, file_ref, content_test,
                                                                                    content_ref))


def compare_netcdf_files(file_test, file_ref, display=False):
    # Todo: Check the metadata of the files
    if not (isinstance(file_test, six.string_types) and os.path.isfile(file_test)):
        fic_test = cfile(file_test)
    else:
        fic_test = file_test
    if not os.path.exists(fic_test) or not os.path.exists(file_ref):
        raise OSError("Check files existence: %s - %s" % (fic_test, file_ref))
    if file_ref.split(".")[-1] != "nc":
        raise ValueError("This function only apply to netcdf files.")
    if fic_test.split(".")[-1] != file_ref.split(".")[-1]:
        raise ValueError("Files have different formats: %s / %s" % (os.path.basename(fic_test),
                                                                    os.path.basename(file_ref)))
    if display:
        ncview(fic_test)
    rep = subprocess.check_output("cdo diffn {} {}".format(fic_test, file_ref), shell=True)
    if len(str(rep).split("\n")) > 1:
        raise ValueError("The content of files %s and %s are different" % (fic_test, file_ref))


def compare_picture_files(object_test, fic_ref, display=False, display_error=True):
    # TODO: Check the metadata of the files
    # Transform the strings in list of strings
    if not (isinstance(object_test, six.string_types) and os.path.isfile(object_test)):
        fic_test = cfile(object_test)
    else:
        fic_test = object_test
    fic_test = fic_test.split(" ")
    if not isinstance(fic_ref, list):
        fic_ref = [fic_ref, ]
    # Loop on the files
    for (file_test, file_ref) in zip(fic_test, fic_ref):
        # Check the existence and the consistency of the comparison
        if not (os.path.exists(file_test) and os.path.exists(file_ref)):
            raise ValueError("Check files existence: %s - %s" % (file_test, file_ref))
        # Find out the format of the files and the dedicated display command
        files_format = list(set([file_test.split(".")[-1], file_ref.split(".")[-1]]))
        if len(files_format) > 1:
            raise ValueError("Files to compare have not the same format: %s" % " - ".join(files_format))
        else:
            files_format = files_format[0]
        if files_format not in ["png", "eps", "jpeg", "pdf"]:
            raise ValueError("Unknown format found %s" % files_format)
        if xdg_bin and files_format in ["eps", "pdf"]:
            display_cmd = "xdg-open {}"
        else:
            display_cmd = "display {}"
        diff_file = file_test + "_diff.{}".format(files_format)
        if display:
            cshow(object_test)
        # Compare the two files, display the difference if needed
        rep = subprocess.call("compare -compose src -metric AE {} {} {}".format(file_test, file_ref, diff_file),
                              shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if rep != 0:
            if display_error:
                subprocess.check_call(display_cmd.format(diff_file), shell=True)
            os.remove(diff_file)
            raise ValueError("The following files differ: %s - %s" % (file_test, file_ref))
        else:
            os.remove(diff_file)
