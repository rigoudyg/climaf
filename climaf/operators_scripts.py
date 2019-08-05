#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CliMAF scripts operators tools.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


class scriptFlags(object):
    def __init__(self, canOpendap=False, canSelectVar=False,
                 canSelectTime=False, canSelectDomain=False,
                 canAggregateTime=False, canAlias=False,
                 canMissing=False, commuteWithEnsemble=True,
                 commuteWithTimeConcatenation=False, commuteWithSpaceConcatenation=False,
                 doCatTime=False):
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
        self.doCatTime = doCatTime

    def __eq__(self, other):
        return isinstance(other, scriptFlags) and \
               (self.canOpendap == other.canOpendap) and \
               (self.canSelectVar == other.canSelectVar) and \
               (self.canSelectTime == other.canSelectTime) and \
               (self.canSelectDomain == other.canSelectDomain) and \
               (self.canAggregateTime == other.canAggregateTime) and \
               (self.canAlias == other.canAlias) and \
               (self.canMissing == other.canMissing) and \
               (self.commuteWithEnsemble == other.commuteWithEnsemble) and \
               (self.commuteWithTimeConcatenation == other.commuteWithTimeConcatenation) and \
               (self.commuteWithSpaceConcatenation == other.commuteWithSpaceConcatenation) and \
               (self.doCatTime == other.doCatTime)

    def unset_selectors(self):
        self.canSelectVar = False
        self.canSelectTime = False
        self.canSelectDomain = False
        self.canAlias = False
        self.canMissing = False
