#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CliMAF scripts operators tools.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


class scriptFlags():
    def __init__(self, canOpendap=False, canSelectVar=False,
                 canSelectTime=False, canSelectDomain=False,
                 canAggregateTime=False, canAlias=False,
                 canMissing=False, commuteWithEnsemble=True,
                 commuteWithTimeConcatenation=False, commuteWithSpaceConcatenation=False):
        self.canOpendap = canOpendap
        self.canSelectVar = canSelectVar
        self.canSelectTime = canSelectTime
        self.canSelectDomain = canSelectDomain
        self.canAggregateTime = canAggregateTime
        self.canAlias = canAlias
        self.canMissing = canMissing
        self.commuteWithEnsemble = commuteWithEnsemble
        self.commuteWithTimeConcatenation = commuteWithTimeConcatenation
        self.commuteWithSpaceConcatenation = commuteWithSpaceConcatenation

    def unset_selectors(self):
        self.canSelectVar = False
        self.canSelectTime = False
        self.canSelectDomain = False
        self.canAlias = False
        self.canMissing = False