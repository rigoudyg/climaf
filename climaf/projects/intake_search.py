#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Query intake catalogs for searching datasets files, adapting facets
as required. Also, optimize search when some facets are shell-like
wildcards (i.e. include * or ?).

"""

from __future__ import print_function, division, unicode_literals, \
    absolute_import
import time

from env.environment import intake_catalog, cprojects
from env.clogging import clogger
from climaf.netcdfbasics import extract_period


if intake_catalog is not None:
    import intake
    import intake_esm

    catalogs = dict()

    def intake_find(kwargs, with_period=False):
        """
        Return a dict of keyword/value for the search of an intake catalog,
        accounting for translation of facet names from CliMAF's to project's
        and for transforming glob-like wildcards to regexp wildcards. 

        Period is withdrawn from search, except if WITH_PERIOD is True
        """
        global catalogs

        project = kwargs['project']
        alias = cprojects[project].translate_facet

        # A dict of values for facets not handled by the intake
        # catalog for the project (they are removed for the search,
        # then restored)
        non_project_values = dict()

        # Rename some facets, withdraw some others
        for facet, project_facet in alias.items():
            if facet in kwargs:
                if project_facet is not None:
                    kwargs[project_facet] = kwargs.pop(facet)
                else:
                    non_project_values[facet] = kwargs.pop(facet)

        # For CMIP, users are accustomed to request version 'latest',
        # which is not available 'as is' when using intake.
        if project in ['CMIP5', 'CMIP6'] and kwargs.get('version', None) == 'latest':
            kwargs['version'] = '*'
            kwargs['latest'] = True

        # Change glob-style wildcards to regexp wildcards
        for kw in kwargs:
            if type(kwargs[kw]) is str:
                kwargs[kw] = kwargs[kw].replace("?", ".").replace("*", ".*")

        if not with_period:
            kwargs.pop('period', None)

        # Do search and convert results to a list of dicts
        if project not in catalogs:
            clogger.info("Opening %s intake catalog " %
                         project + intake_catalog)
            tim1 = time.time()
            catalog = intake.open_catalog(intake_catalog)
            catalogs[project] = catalog[project]
            clogger.info("Done opening in %d seconds" % (time.time() - tim1))
        clogger.info("Querying catalog with " + str(kwargs))
        tim1 = time.time()
        subcat = intake_search(catalogs[project], **kwargs)
        clogger.info("Done querying in %d seconds" % (time.time() - tim1))
        dic_list = subcat.df.to_dict(orient='records')
        clogger.debug("Query result is %s" % dic_list)

        for dico in dic_list:
            # Translate back facet names
            for facet, project_facet in alias.items():
                if project_facet is not None:
                    dico[facet] = dico.pop(project_facet)

            # Convert period_start + period_end in CliMAF period
            start = dico.pop('period_start')
            end = dico.pop('period_end')
            if type(start) is str and type(end) is str:
                # Should use period_start and period_end from catalog,
                # but, as of 20240517, they are buggy : they do not
                # represent time_bounds nor average period centers
                # Hence, we could scrutinize files using
                # timeLimits(). But this can take time...  So, we
                # extract the period from the filename, using a
                # project specific pattern

                # dico['period'] = init_period_iso(start, end)
                # dico['period'] = timeLimits(dico['path'])
                dico['period'] = extract_period(
                    dico['path'], cprojects[project].period_pattern)

                # clogger.debug('Period start and end %s %s   -> %s' %
                #              (start, end, dico['period']))
            else:
                # This happens for data not matching the DRS, and frequently
                # having bad time values ->  set dummy dates
                dico['period'] = None

            # Discard facets that CliMAF doesn't manage
            for project_facet in list(dico.keys()):
                if project_facet not in cprojects[project].facets and \
                        project_facet != "path":
                    dico.pop(project_facet)

            # Restore facets not managed by the project
            dico.update(non_project_values)

        return dic_list

    def intake_search(catalog, **kwargs):
        """
        Intake is not smart at searching large catalogs with
        wildcards. Better first search for non-wildcard facets, and then
        search again using wildcard facets.

        """
        plain = {key: value for key, value in kwargs.items()
                 if "." not in value}
        wild = {key: value for key, value in kwargs.items() if "." in value}
        subcat = catalog.search(**plain)
        clogger.debug("Search with plain arguments %s returned : %s" %
                      (plain, len(subcat.df.to_dict(orient='records'))))
        if len(wild) == 0:
            clogger.debug("And there is no wildcard args")
            return subcat
        else:
            rep = subcat.search(**wild)
            clogger.debug("Search with wildcard arguments %s returned : %s" %
                          (wild, len(rep.df.to_dict(orient='records'))))
            return rep
else:

    def intake_find(kwargs):

        raise Error("No intake catalog is defined (in env.environment")
