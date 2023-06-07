#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to generate pdf documents using latex syntax from python.
"""
from __future__ import unicode_literals, absolute_import, print_function, division

from env.environment import *

import os
import pdflatex
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filenames", nargs="+", help="Filenames of the files to include")
parser.add_argument("--preamble", required=True, help="String to be added in the preamble")
parser.add_argument("--papersize", required=True, help="String defining the page size")
parser.add_argument("--delta", required=True, help="String defining the delta")
parser.add_argument("--nup", required=True, help="String defining the number of lines and columns")
parser.add_argument("--outfile", required=True, help="Output file")
parser.add_argument("--pagecommand", required=True, help="Command to apply")
parser.add_argument("--openright", default="false", choices=["false", "False", "true", "True"],
                    help="Should the document begin with a blank page?")
parser.add_argument("--scale", default="1.", help="Scale to apply")
parser.add_argument("--keepinfo", action="store_true")
args = parser.parse_args()

template = r"""
\documentclass{article}
\usepackage{pdfpages}
%s
\geometry{papersize=%s}
\begin{document}
\includepdfmerge[nup=%s, delta=%s,scale=%s, openright=%s, pagecommand={%s}]{%s}
\end{document}
""" % (args.preamble,
       args.papersize,
       args.nup,
       args.delta,
       args.scale,
       args.openright.lower(),
       args.pagecommand,
       ",".join(args.filenames))

output_basename = os.path.basename(args.outfile)
if output_basename.endswith(".pdf"):
    output_basename = output_basename[:-4]

pdfl = pdflatex.PDFLaTeX.from_binarystring(template.encode("utf-8"), output_basename)
pdfl.set_output_directory(os.path.dirname(args.outfile))
pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True)
