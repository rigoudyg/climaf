#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools to deal with tests.
"""

from __future__ import unicode_literals, absolute_import, print_function, division

import os
import unittest
import re
import six
import shutil
import subprocess

from env.environment import *
from climaf.api import cshow, ncview, cfile


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
        shutil.rmtree(dirname)
        print("Remove directory: %s" % dirname)
    else:
        print("Try to remove a non existing directory: %s" % dirname)


def get_figures_and_content_from_html(html_file, regexp, patterns_to_exclude=list(), add_dir=False):
    with open(html_file, "r") as fic:
        content = fic.read()
    list_figures = list()
    list_replacement = list()
    for regexp_match in regexp.finditer(content):
        value = regexp_match.groupdict()["value"]
        list_replacement.append(value)
        if add_dir and not value.startswith(os.sep):
            value = os.sep.join([os.path.dirname(html_file), value])
        if value not in list_figures and not any([p in value for p in patterns_to_exclude]):
            list_figures.append(value)
    for fig in list(set(list_replacement)):
        content = content.replace(fig, "FIGURE")
    return list_figures, content


def compare_html_files(file_test, file_ref_name, dir_ref, dir_ref_default=None, display_error=True, replace=None,
                       by=None, allow_url_change=False, generate_diffs_html=False):
    if not os.path.isdir(dir_ref) and not os.path.isdir(dir_ref_default):
        raise ValueError("Neither reference directory nor default one exists")
    file_ref = os.path.sep.join([dir_ref, file_ref_name])
    if not os.path.exists(file_ref):
        default_file_ref = os.path.sep.join([dir_ref_default, file_ref_name])
        if not os.path.exists(default_file_ref):
            raise ValueError(
                "Could not find a reference file for %s" % file_ref_name)
        else:
            file_ref = default_file_ref
            dir_ref = dir_ref_default
    if not os.path.exists(file_test) or not os.path.exists(file_ref):
        raise OSError("Check files existence: %s - %s" % (file_test, file_ref))
    if file_ref.split(".")[-1] != "html":
        raise ValueError("This function only apply to html files.")
    if file_test.split(".")[-1] != file_ref.split(".")[-1]:
        raise ValueError("Files have different formats: %s / %s" % (os.path.basename(file_test),
                                                                    os.path.basename(file_ref)))
    fig_regexp = re.compile(r'(HREF|SRC)="(?P<value>[^"]*\.png)"')
    patterns_to_exclude = ["Logo-CliMAF-compact.png", ]
    list_figures_test, content_test = get_figures_and_content_from_html(file_test, fig_regexp, patterns_to_exclude,
                                                                        add_dir=True)
    list_figures_ref, content_ref = get_figures_and_content_from_html(
        file_ref, fig_regexp, patterns_to_exclude)
    if allow_url_change:
        url_line_pattern = "<a href=.*Back to C-ESM-EP frontpage.*</a>"
        text = re.findall(url_line_pattern, content_ref)[0]
        content_ref = content_ref.replace(text, "")
        text = re.findall(url_line_pattern, content_test)[0]
        content_test = content_test.replace(text, "")
    if replace is not None:
        content_ref = content_ref.replace(replace, by)
    if content_test != content_ref:
        raise ValueError("The content of files %s and %s are different\n%s\n!=\n%s" % (file_test, file_ref,
                                                                                       content_test, content_ref))
    if len(list_figures_ref) != len(list_figures_test):
        raise ValueError(
            "The number of figures if different in %s and %s" % (file_test, file_ref))
    nb_NOK = 0
    if generate_diffs_html:
        diffs_triplets = []
    for (fig_ref, fig_test) in zip(list_figures_ref, list_figures_test):
        try:
            triplets = compare_picture_files(fig_test, fig_ref, dir_ref,
                                             dir_ref_default=None, display_error=display_error,
                                             provide_triplets=generate_diffs_html)
            if generate_diffs_html:
                diffs_triplets.extend(triplets)
        except ValueError as error:
            nb_NOK += 1
            print(error.args)
    if nb_NOK > 0:
        raise ValueError(f" {nb_NOK} pictures are "
                         f"different between {file_test} and {file_ref}")
    if generate_diffs_html:
        if len(diffs_triplets) > 0:
            html_file = build_diffs_html(diffs_triplets, file_test)
            if html_file.startswith("/thredds/ipsl/"):
                html_file = html_file.replace(
                    "/thredds/ipsl/",
                    "https://thredds-su.ipsl.fr/thredds/fileServer/ipsl_thredds/")
            raise ValueError(
                "%d pictures are different. See html diff file %s" %
                (len(diffs_triplets),html_file))


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
    content_test = re.sub(os.path.sep.join([os.environ.get("TMPDIR", "/tmp"), r"climaf_\w+"]), "/tmp/climaf_XXX",
                          content_test)
    if content_test != content_ref:
        raise ValueError("The content of files %s and %s are different:\n%s\n%s" % (file_test, file_ref, content_test,
                                                                                    content_ref))


def compare_netcdf_files(file_test, file_ref, display=False):
    # Todo: Check the metadata of the files
    if not os.path.exists(file_test) or not os.path.exists(file_ref):
        raise OSError("Check files existence: %s - %s" % (file_test, file_ref))
    if file_ref.split(".")[-1] != "nc":
        raise ValueError("This function only apply to netcdf files.")
    if file_test.split(".")[-1] != file_ref.split(".")[-1]:
        raise ValueError("Files have different formats: %s / %s" % (os.path.basename(file_test),
                                                                    os.path.basename(file_ref)))
    if display:
        ncview(file_test)
    rep = subprocess.check_output(
        "cdo diffn {} {}".format(file_test, file_ref), shell=True)
    if len(str(rep).split("\n")) > 1:
        raise ValueError(
            "The content of files %s and %s are different" % (file_test, file_ref))


def compare_picture_files(object_test, fic_ref, dir_ref, dir_ref_default=None, display=False, display_error=True, provide_triplets=False):
    # provide_triplets True -> don't raise an error for differing files, but
    # provide a list of triplets (file_test, file_ref, diff_file)

    # TODO: Check the metadata of the files
    # Transform the strings in list of strings
    if isinstance(object_test, six.string_types) and os.path.exists(object_test):
        fic_test = object_test
        object_is_fic = True
    else:
        fic_test = cfile(object_test)
        object_is_fic = False
    fic_test = fic_test.split(" ")
    if not os.path.isdir(dir_ref) and not os.path.isdir(dir_ref_default):
        raise ValueError("Neither reference directory nor default one exists")
    if not isinstance(fic_ref, list):
        fic_ref = [fic_ref, ]
    for (i, elt) in enumerate(fic_ref):
        elt_ref = os.path.sep.join([dir_ref, elt])
        if dir_ref_default is not None:
            elt_default_ref = os.path.sep.join([dir_ref_default, elt])
        else:
            elt_default_ref = "foo"
        if os.path.exists(elt_ref):
            fic_ref[i] = elt_ref
        elif os.path.exists(elt_default_ref):
            fic_ref[i] = elt_default_ref
        else:
            raise ValueError("Could not find the reference file for %s" % elt)
    if provide_triplets:
        triplets = []  # Will list triplets of files when there is a differnece
    # Loop on the files
    for (file_test, file_ref) in zip(fic_test, fic_ref):
        # Check the existence and the consistency of the comparison
        if not (os.path.exists(file_test) and os.path.exists(file_ref)):
            raise ValueError("Check files existence: %s - %s" %
                             (file_test, file_ref))
        # Find out the format of the files and the dedicated display command
        files_format = list(
            set([file_test.split(".")[-1], file_ref.split(".")[-1]]))
        if len(files_format) > 1:
            raise ValueError(
                "Files to compare have not the same format: %s" % " - ".join(files_format))
        else:
            files_format = files_format[0]
        if files_format not in ["png", "eps", "jpeg", "pdf"]:
            raise ValueError("Unknown format found %s" % files_format)
        if xdg_bin is not None and files_format in ["eps", "pdf"]:
            display_cmd = "%s {}" % xdg_bin
        else:
            display_cmd = "display {}"
        diff_file = file_test + "_diff.{}".format(files_format)
        if display:
            cshow(object_test)
        # Compare the two files, display the difference if needed
        rep = subprocess.call("compare -compose src -metric AE {} {} {}".format(file_test, file_ref, diff_file),
                              shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if rep != 0:
            tmp_dir = os.sep.join([os.path.dirname(file_test), "..", "tmp"])
            os.makedirs(tmp_dir, exist_ok=True)
            if not object_is_fic:
                cfile(object_test,
                      target=os.sep.join([tmp_dir, os.path.basename(file_test)]))
            if display_error:
                message = ""
                try:
                    subprocess.check_call(
                        display_cmd.format(diff_file), shell=True)
                    os.remove(diff_file)
                except subprocess.SubprocessError:
                    print("Could not display %s" % diff_file)
            else:
                message = "\n" + f"See diff file : {diff_file}"
            message = "The following files differ: %s - %s" % (
                file_test, file_ref) + message
            if provide_triplets:
                # print(message)
                triplets.append((file_test, file_ref, diff_file))
            else:
                raise ValueError(message)
        else:
            os.remove(diff_file)
    if provide_triplets:
        return(triplets)


def build_diffs_html(diffs_triplets, file_test):
    # Provided with a list of image filename triplets, create an html doc that show
    # one line of images per triplet
    # The html file is located with file_test in subdir diff/ and has the same basename
    # The image files are copied in the same subdir
    #
    header='<?xml version="1.0" encoding="iso-8859-1"?>\n' +\
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n' +\
        '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n' +\
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">\n' +\
        '<head>\n<title>[ DIFFS ]</title>\n</head>\n<body>' +\
        '<TABLE CELLSPACING=5>\n'
    text=header
    #
    form='\n<TD ALIGN=RIGHT><A HREF="{}"><IMG HEIGHT=350 WIDTH=600 SRC="{}"></a></TD>'
    tmp_dir=os.sep.join([os.path.dirname(file_test), "diffs"])
    os.makedirs(tmp_dir, exist_ok=True)
    for triplet in diffs_triplets:
        text += "\n<TR>"
        for fic in triplet:
            ficb=os.path.basename(fic)
            fic_copy=os.sep.join([tmp_dir, ficb])
            shutil.copy(fic, fic_copy)
            text += form.format(ficb, ficb)
        text += "\n<TR>"
        #
    text += "\n</TABLE>"
    text += "\n</body>"
    #
    target=os.sep.join([tmp_dir, os.path.basename(file_test)])
    with open(target, "w") as fic:
        fic.write(text)
    return(target)
