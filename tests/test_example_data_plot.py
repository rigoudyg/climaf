#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test based on examples/index_html.py
"""

import os
import unittest

from tests.tools_for_tests import remove_dir_and_content, compare_picture_files, skipUnless_CNRM_Lustre

from climaf.cache import setNewUniqueCache
from climaf import __path__ as cpath
from climaf.api import craz, plot, cdef, cfile, time_average, ds, space_average, curves, cpage, cpage_pdf, cpdfcrop, \
    cens, llbox, cproject, dataloc, calias, fixed_fields, ccdo

if not isinstance(cpath, list):
    cpath = cpath.split(os.sep)


class DataGplotMaps(unittest.TestCase):

    def setUp(self):
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_data_plot"])
        self.tas = ds(project='example', simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="198001")
        self.sub_tas = llbox(self.tas, latmin=30, latmax=80, lonmin=60, lonmax=120)
        self.uas = ds(project='example', simulation="AMIPV6ALB2G", variable="uas", period="198001")
        self.vas = ds(project='example', simulation="AMIPV6ALB2G", variable="vas", period="198001")
        self.ta_1980 = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly',
                          period="1980")
        self.sub_ta_1980 = llbox(self.ta_1980, latmin=30, latmax=80, lonmin=60, lonmax=120)
        self.tas_1980 = ds(project='example', simulation="AMIPV6ALB2G", variable="tas", frequency='monthly',
                           period="1980")
        self.sub_tas_1980 = llbox(self.tas_1980, latmin=30, latmax=80, lonmin=60, lonmax=120)
        self.uas_1980 = ds(project='example', simulation="AMIPV6ALB2G", variable="uas", period="1980")
        self.vas_1980 = ds(project='example', simulation="AMIPV6ALB2G", variable="vas", period="1980")

    def test_gplot_maps_1(self):
        """
        A Map with one field and vectors, with contours lines like color fill, default projection (a cylindrical
        equidistant), with 'pdf' output format and paper resolution of 17x22 inches (<=> 1224x1584 pixels)
        """
        plot_map = plot(self.tas, None, self.uas, self.vas,
                        title='1 field (contours lines follow color filled contours) + vectors',
                        contours=1, vcRefLengthF=0.02, vcRefMagnitudeF=11.5, format="pdf", resolution='17*22')
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|uas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|198001|global|monthly'),contours=1,format='pdf',"
                         "resolution='17*22',title='1 field (contours lines follow color filled contours) + vectors',"
                         "vcRefLengthF=0.02,vcRefMagnitudeF=11.5)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.1.pdf"])
        compare_picture_files(plot_map, ref_plotmap)
        #
        plot_map_crop = cpdfcrop(plot_map)
        self.assertEqual(str(plot_map_crop),
                         "cpdfcrop(plot(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|uas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|198001|global|monthly'),contours=1,format='pdf',"
                         "resolution='17*22',title='1 field (contours lines follow color filled contours) + vectors',"
                         "vcRefLengthF=0.02,vcRefMagnitudeF=11.5))")
        ref_plotmap_crop = os.sep.join([self.reference_directory, "test_A.2.pdf"])
        compare_picture_files(plot_map_crop, ref_plotmap_crop)

    def test_gplot_maps_2(self):
        """
        A Map of one field and vectors, with user-controled contours lines, stereopolar projection
        and with 'png' output format (default)
        """
        plot_map = plot(self.tas, None, self.uas, self.vas, title='1 field (user-controled contours) + vectors',
                        proj='NH', contours='230 235 240 245 250 255 260 265 270 275 280', vcRefLengthF=0.03,
                        vcRefMagnitudeF=11.5)
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|uas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|198001|global|monthly'),"
                         "contours='230 235 240 245 250 255 260 265 270 275 280',proj='NH',"
                         "title='1 field (user-controled contours) + vectors',vcRefLengthF=0.03,vcRefMagnitudeF=11.5)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.3.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_3(self):
        """
        A Map of two fields and vectors, with explicit contours levels for auxiliary field, and addition of a box
        """
        plot_map = plot(self.tas, self.sub_tas, self.uas, self.vas,
                        title='2 fields (user-controled auxiliary field contours) + vectors',
                        contours='230 235 240 245 250 255 260 265 270', vcRefLengthF=0.02, vcRefMagnitudeF=11.5,
                        xpolyline="45.0, 90.0, 90.0, 45.0, 45.0", ypolyline="30.0, 30.0, 0.0, 0.0, 30.0",
                        polyline_options='gsLineColor=blue')
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),"
                         "llbox(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),latmax=80,latmin=30,lonmax=120,"
                         "lonmin=60),ds('example|AMIPV6ALB2G|uas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|198001|global|monthly'),"
                         "contours='230 235 240 245 250 255 260 265 270',polyline_options='gsLineColor=blue',"
                         "title='2 fields (user-controled auxiliary field contours) + vectors',vcRefLengthF=0.02,"
                         "vcRefMagnitudeF=11.5,xpolyline='45.0, 90.0, 90.0, 45.0, 45.0',"
                         "ypolyline='30.0, 30.0, 0.0, 0.0, 30.0')")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.4.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_4(self):
        """
        A Map of two fields and vectors, with automatic contours levels for auxiliary field
        """
        plot_map = plot(self.tas, self.sub_tas, self.uas, self.vas,
                        title='2 fields (automatic contours levels for auxiliary field) + vectors',
                        proj="NH", vcRefLengthF=0.05, vcRefMagnitudeF=11.5, vcMinDistanceF=0.012,
                        vcLineArrowColor="yellow")
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),"
                         "llbox(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),latmax=80,latmin=30,lonmax=120,"
                         "lonmin=60),ds('example|AMIPV6ALB2G|uas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|198001|global|monthly'),proj='NH',"
                         "title='2 fields (automatic contours levels for auxiliary field) + vectors',"
                         "vcLineArrowColor='yellow',vcMinDistanceF=0.012,vcRefLengthF=0.05,vcRefMagnitudeF=11.5)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.5.png"])
        compare_picture_files(plot_map, ref_plotmap)

    @unittest.expectedFailure
    def test_gplot_maps_5(self):
        """
        Same map but with an other vector style: curly vectors (default: "LineArrow")

        TODO: Check why this test fails
        """
        plot_map = plot(self.tas, self.sub_tas, self.uas, self.vas,
                        title='2 fields (automatic contours levels for auxiliary field) + vectors (curly)',
                        proj="NH", vcRefLengthF=0.05, vcRefMagnitudeF=11.5, vcMinDistanceF=0.012,
                        vcLineArrowColor="yellow", vcGlyphStyle="CurlyVector")
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),"
                         "llbox(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),latmax=80,latmin=30,lonmax=120,"
                         "lonmin=60),ds('example|AMIPV6ALB2G|uas|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|198001|global|monthly'),proj='NH',"
                         "title='2 fields (automatic contours levels for auxiliary field) + vectors (curly)',"
                         "vcGlyphStyle='CurlyVector',vcLineArrowColor='yellow',vcMinDistanceF=0.012,vcRefLengthF=0.05,"
                         "vcRefMagnitudeF=11.5)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.6.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_6(self):
        """
        Same map without vectors
        """
        plot_map = plot(self.tas, self.sub_tas, title='2 fields (automatic contours levels for auxiliary field)',
                        proj="NH")
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),"
                         "llbox(ds('example|AMIPV6ALB2G|tas|198001|global|monthly'),latmax=80,latmin=30,lonmax=120,"
                         "lonmin=60),proj='NH',title='2 fields (automatic contours levels for auxiliary field)')")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.7.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_7(self):
        """
        A Map of two fields and vectors, with index selection of time step and/or level step for all fields which have
        this dimension : case where (t,z,y,x) are not degenerated
        """
        plot_map = plot(self.ta_1980, self.sub_ta_1980, self.uas_1980, self.vas_1980,
                        title='Selecting index 10 for level and 0 for time', vcRefLengthF=0.02, vcRefMagnitudeF=11.5,
                        level=10, time=0)
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),"
                         "llbox(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),latmax=80,latmin=30,lonmax=120,"
                         "lonmin=60),ds('example|AMIPV6ALB2G|uas|1980|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|1980|global|monthly'),level=10,time=0,"
                         "title='Selecting index 10 for level and 0 for time',vcRefLengthF=0.02,vcRefMagnitudeF=11.5)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.8.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_8(self):
        """
        A Map of two fields and vectors, with value selection of time step and/or level step for all fields which have
        this dimension : case where (t,y,x) are not degenerated
        """
        plot_map = plot(self.tas_1980, self.sub_tas_1980, self.uas_1980, self.vas_1980,
                        title='Selecting level and time close to 10 and 1400000 respectively',
                        vcRefLengthF=0.02, vcRefMagnitudeF=11.5, level=10., time=1400000.)
        self.assertEqual(str(plot_map),
                         "plot(ds('example|AMIPV6ALB2G|tas|1980|global|monthly'),"
                         "llbox(ds('example|AMIPV6ALB2G|tas|1980|global|monthly'),latmax=80,latmin=30,lonmax=120,"
                         "lonmin=60),ds('example|AMIPV6ALB2G|uas|1980|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|1980|global|monthly'),level=10.0,time=1400000.0,"
                         "title='Selecting level and time close to 10 and 1400000 respectively',vcRefLengthF=0.02,"
                         "vcRefMagnitudeF=11.5)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_A.9.png"])
        compare_picture_files(plot_map, ref_plotmap)
        plot_map_bis = plot(self.tas_1980, self.sub_tas_1980, self.uas_1980, self.vas_1980,
                            title='Selecting level and time close to 10 and 19800131 respectively',
                            vcRefLengthF=0.02, vcRefMagnitudeF=11.5, level=10., date=19800131)
        self.assertEqual(str(plot_map_bis),
                         "plot(ds('example|AMIPV6ALB2G|tas|1980|global|monthly'),"
                         "llbox(ds('example|AMIPV6ALB2G|tas|1980|global|monthly'),latmax=80,latmin=30,lonmax=120,"
                         "lonmin=60),ds('example|AMIPV6ALB2G|uas|1980|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|vas|1980|global|monthly'),date=19800131,level=10.0,"
                         "title='Selecting level and time close to 10 and 19800131 respectively',vcRefLengthF=0.02,"
                         "vcRefMagnitudeF=11.5)")
        ref_plotmap_bis = os.sep.join([self.reference_directory, "test_A.10.png"])
        compare_picture_files(plot_map_bis, ref_plotmap_bis)


@skipUnless_CNRM_Lustre()
class DataGplotMapsRotation(unittest.TestCase):

    def setUp(self):
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_data_plot"])
        # -----------------------------------------------------------
        # Declare "data_CNRM" project with some 'standard' Nemo output files
        # (actually, they are easier accessible using project "EM")
        # -----------------------------------------------------------
        cproject('data_CNRM')
        root = "/cnrm/est/COMMON/climaf/test_data/${simulation}/O/"
        suffix = "${simulation}_1m_YYYYMMDD_YYYYMMDD_${variable}.nc"
        data_url = root + suffix
        dataloc(project='data_CNRM', organization='generic', url=data_url)
        # -----------------------------------------------------------
        # Declare how variables are scattered/grouped among files
        # -----------------------------------------------------------
        calias("data_CNRM", "tos,thetao", filenameVar="grid_T_table2.2")
        calias("data_CNRM", "uo", filenameVar="grid_U_table2.3")
        calias("data_CNRM", "vo", filenameVar="grid_V_table2.3")

        # -----------------------------------------------------------
        # Define datasets for main field, auxiliary field and vectors
        # -----------------------------------------------------------
        self.tos = ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="tos", period="199807")
        self.sub_tos = llbox(self.tos, latmin=30, latmax=80, lonmin=-60, lonmax=0)
        self.duo = ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="uo", period="199807")
        self.dvo = ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="vo", period="199807")
        self.duo_1998 = ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="uo", period="1998")
        self.dvo_1998 = ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="vo", period="1998")
        self.tos_1998 = ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="tos", period="1998")
        self.sub_tos_1998 = llbox(self.tos_1998, latmin=30, latmax=80, lonmin=-60, lonmax=0)
        self.thetao_1998 = ds(project="data_CNRM", simulation="PRE6CPLCr2alb", variable="thetao", period="1998")
        self.sub_thetao_1998 = llbox(self.thetao_1998, latmin=30, latmax=80, lonmin=-60, lonmax=0)

        # -----------------------------------------------------------
        # How to get the required file for rotating vectors from model grid on geographic grid
        # -----------------------------------------------------------
        fixed_fields('plot', ('angles.nc', os.sep.join(cpath + ["..", "tools", "angle_${project}.nc"])))

    def test_gplot_maps_rotation_1(self):
        """
        A Map with one field and vectors, with contours lines like color fill, rotation of vectors on geographic grid,
        default projection (a cylindrical equidistant)
        """
        plot_map = plot(self.tos, None, self.duo, self.dvo,
                        title='1 field (contours lines follow color filled contours) + vectors',
                        contours=1, rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
        self.assertEqual(str(plot_map),
                         "plot(ds('data_CNRM.PRE6CPLCr2alb.tos.199807.global'),"
                         "ds('data_CNRM.PRE6CPLCr2alb.uo.199807.global'),"
                         "ds('data_CNRM.PRE6CPLCr2alb.vo.199807.global'),contours=1,rotation=1,"
                         "title='1 field (contours lines follow color filled contours) + vectors',vcRefLengthF=0.002,"
                         "vcRefMagnitudeF=0.02)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_B.1.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_rotation_2(self):
        """
        A Map of one field and vectors, with user-controled contours lines, rotation as above, stereopolar projection
        and with 'png' output format (default)
        """
        plot_map = plot(self.tos, None, self.duo, self.dvo, title='1 field (user-controled contours) + vectors',
                        contours='1 3 5 7 9 11 13', proj='NH', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
        self.assertEqual(str(plot_map),
                         "plot(ds('data_CNRM.PRE6CPLCr2alb.tos.199807.global'),"
                         "ds('data_CNRM.PRE6CPLCr2alb.uo.199807.global'),"
                         "ds('data_CNRM.PRE6CPLCr2alb.vo.199807.global'),contours='1 3 5 7 9 11 13',proj='NH',"
                         "rotation=1,title='1 field (user-controled contours) + vectors',vcRefLengthF=0.002,"
                         "vcRefMagnitudeF=0.02)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_B.2.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_rotation_3(self):
        """
        A Map of two fields and vectors, with explicit contours levels for auxiliary field and rotation of vectors on
        geographic grid
        """
        plot_map = plot(self.tos, self.sub_tos, self.duo, self.dvo,
                        title='2 fields (user-controled auxiliary field contours) + vectors',
                        contours='0 2 4 6 8 10 12 14 16', rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02)
        self.assertEqual(str(plot_map),
                         "plot(ds('data_CNRM.PRE6CPLCr2alb.tos.199807.global'),"
                         "llbox(ds('data_CNRM.PRE6CPLCr2alb.tos.199807.global'),latmax=80,latmin=30,lonmax=0,"
                         "lonmin=-60),ds('data_CNRM.PRE6CPLCr2alb.uo.199807.global'),"
                         "ds('data_CNRM.PRE6CPLCr2alb.vo.199807.global'),contours='0 2 4 6 8 10 12 14 16',rotation=1,"
                         "title='2 fields (user-controled auxiliary field contours) + vectors',vcRefLengthF=0.002,"
                         "vcRefMagnitudeF=0.02)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_B.3.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_rotation_4(self):
        """
        A Map of two fields and vectors, with automatic contours levels for auxiliary field and rotation of vectors on
        geographic grid
        """
        plot_map = plot(self.tos, self.sub_tos, self.duo, self.dvo,
                        title='2 fields (automatic contours levels for auxiliary field) + vectors',
                        proj="NH", rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, vcMinDistanceF=0.01,
                        vcLineArrowColor="yellow")
        self.assertEqual(str(plot_map),
                         "plot(ds('data_CNRM.PRE6CPLCr2alb.tos.199807.global'),"
                         "llbox(ds('data_CNRM.PRE6CPLCr2alb.tos.199807.global'),latmax=80,latmin=30,lonmax=0,"
                         "lonmin=-60),ds('data_CNRM.PRE6CPLCr2alb.uo.199807.global'),"
                         "ds('data_CNRM.PRE6CPLCr2alb.vo.199807.global'),proj='NH',rotation=1,"
                         "title='2 fields (automatic contours levels for auxiliary field) + vectors',"
                         "vcLineArrowColor='yellow',vcMinDistanceF=0.01,vcRefLengthF=0.002,vcRefMagnitudeF=0.02)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_B.4.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_rotation_5(self):
        """
        A Map of two fields and vectors, with index selection of time step and/or level step for all fields which have
        this dimension : case where (t,z,y,x) are not degenerated
        """
        plot_map = plot(self.thetao_1998, self.sub_thetao_1998, self.duo, self.dvo,
                        title='Selecting index 10 for level and 0 for time', rotation=1,
                        vcRefLengthF=0.002, vcRefMagnitudeF=0.02, level=10, time=0)
        self.assertEqual(str(plot_map),
                         "plot(ds('data_CNRM.PRE6CPLCr2alb.thetao.1998.global'),"
                         "llbox(ds('data_CNRM.PRE6CPLCr2alb.thetao.1998.global'),latmax=80,latmin=30,lonmax=0,"
                         "lonmin=-60),ds('data_CNRM.PRE6CPLCr2alb.uo.199807.global'),"
                         "ds('data_CNRM.PRE6CPLCr2alb.vo.199807.global'),level=10,rotation=1,time=0,"
                         "title='Selecting index 10 for level and 0 for time',vcRefLengthF=0.002,vcRefMagnitudeF=0.02)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_B.5.png"])
        compare_picture_files(plot_map, ref_plotmap)

    def test_gplot_maps_rotation_6(self):
        """
        A Map of two fields and vectors, with value selection of time step and/or level step for all fields which have
        this dimension : case where (t,y,x) are not degenerated
        """
        plot_map = plot(self.tos_1998, self.sub_tos_1998, self.duo_1998, self.dvo_1998,
                        title='Selecting level and time close to 10 and 1400000 respectively',
                        rotation=1, vcRefLengthF=0.002, vcRefMagnitudeF=0.02, level=10., time=1400000.)
        self.assertEqual(str(plot_map),
                         "plot(ds('data_CNRM.PRE6CPLCr2alb.tos.1998.global'),"
                         "llbox(ds('data_CNRM.PRE6CPLCr2alb.tos.1998.global'),latmax=80,latmin=30,lonmax=0,lonmin=-60),"
                         "ds('data_CNRM.PRE6CPLCr2alb.uo.1998.global'),ds('data_CNRM.PRE6CPLCr2alb.vo.1998.global'),"
                         "level=10.0,rotation=1,time=1400000.0,"
                         "title='Selecting level and time close to 10 and 1400000 respectively',vcRefLengthF=0.002,"
                         "vcRefMagnitudeF=0.02)")
        ref_plotmap = os.sep.join([self.reference_directory, "test_B.6.png"])
        compare_picture_files(plot_map, ref_plotmap)


class DataGplotCrossSections(unittest.TestCase):

    def setUp(self):
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_data_plot"])
        self.ta = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", period="1980")
        self.january_ta = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly',
                             period="198001")
        self.january_ta_zonal_mean = ccdo(self.january_ta, operator="zonmean")
        self.ta_zonal_mean = ccdo(self.ta, operator="zonmean")
        self.january_cross_field = llbox(self.january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150)
        self.cross_field = llbox(self.ta, latmin=10, latmax=90, lonmin=50, lonmax=150)
        self.january_ta_zonal_mean2 = ccdo(self.january_cross_field, operator="zonmean")
        self.ta_zonal_mean2 = ccdo(self.cross_field, operator="zonmean")

    @unittest.expectedFailure
    def test_gplot_cross_sections_1(self):
        """
        A vertical cross-section in pressure coordinates of one field without contours lines and with logarithmic scale,
        and addition of a box

        TODO: Check why this test fails
        """
        plot_cross = plot(self.january_ta_zonal_mean, title='1 field cross-section (without contours lines)', y="log",
                          xpolyline="-60.0, -30.0, -30.0, -60.0, -60.0", ypolyline="70.0, 70.0, 50.0, 50.0, 70.0")
        self.assertEqual(str(plot_cross),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),"
                         "title='1 field cross-section (without contours lines)',"
                         "xpolyline='-60.0, -30.0, -30.0, -60.0, -60.0',y='log',"
                         "ypolyline='70.0, 70.0, 50.0, 50.0, 70.0')")
        ref_plotcross = os.sep.join([self.reference_directory, "test_C.1.png"])
        compare_picture_files(plot_cross, ref_plotcross)

    def test_gplot_cross_sections_2(self):
        """
        A cross-section of one field, which contours lines follow color filled contours
        """
        plot_cross = plot(self.january_ta_zonal_mean, contours=1,
                          title='1 field (contours lines follow color filled contours)')
        self.assertEqual(str(plot_cross),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),contours=1,"
                         "title='1 field (contours lines follow color filled contours)')")
        ref_plotcross = os.sep.join([self.reference_directory, "test_C.2.png"])
        compare_picture_files(plot_cross, ref_plotcross)

    def test_gplot_cross_sections_3(self):
        """
        A cross-section of one field, which contours lines don t follow color filled contours
        """
        plot_cross = plot(self.january_ta_zonal_mean, contours="240 245 250", title='1 field (user-controled contours)')
        self.assertEqual(str(plot_cross),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),"
                         "contours='240 245 250',title='1 field (user-controled contours)')")
        ref_plotcross = os.sep.join([self.reference_directory, "test_C.3.png"])
        compare_picture_files(plot_cross, ref_plotcross)

    def test_gplot_cross_sections_4(self):
        """
        Same cross-section but with y="index" (vertical axis will have a index-linear spacing, and logarithmic in
        pressure)
        """
        plot_cross = plot(self.january_ta_zonal_mean, y="index", contours="240 245 250",
                          title='1 field (user-controled contours)')
        self.assertEqual(str(plot_cross),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),"
                         "contours='240 245 250',title='1 field (user-controled contours)',y='index')")
        ref_plotcross = os.sep.join([self.reference_directory, "test_C.4.png"])
        compare_picture_files(plot_cross, ref_plotcross)

    def test_gplot_cross_sections_5(self):
        """
        A cross-section of two fields, with explicit contours levels for auxiliary field
        """
        plot_cross = plot(self.january_ta_zonal_mean, self.january_ta_zonal_mean2, contours="240 245 250",
                          title='2 fields (user-controled auxiliary field contours)')
        self.assertEqual(str(plot_cross),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),"
                         "ccdo(llbox(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),latmax=90,latmin=10,lonmax=150,"
                         "lonmin=50),operator='zonmean'),contours='240 245 250',"
                         "title='2 fields (user-controled auxiliary field contours)')")
        ref_plotcross = os.sep.join([self.reference_directory, "test_C.5.png"])
        compare_picture_files(plot_cross, ref_plotcross)

    def test_gplot_cross_sections_6(self):
        """
        A cross-section of two fields, with automatic contours levels for auxiliary field and a pressure-linear spacing
        and logarithmic in index for vertical axis (y="lin", it is by default)
        """
        plot_cross = plot(self.january_ta_zonal_mean, self.january_ta_zonal_mean2, y="lin",
                          title='2 fields (automatic contours levels for auxiliary field)')
        self.assertEqual(str(plot_cross),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),"
                         "ccdo(llbox(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),latmax=90,latmin=10,lonmax=150,"
                         "lonmin=50),operator='zonmean'),"
                         "title='2 fields (automatic contours levels for auxiliary field)',y='lin')")
        ref_plotcross = os.sep.join([self.reference_directory, "test_C.6.png"])
        compare_picture_files(plot_cross, ref_plotcross)

    def test_gplot_cross_sections_7(self):
        """
        Two plots where (t,z,y) are not degenerated, with selection of time step and/or level step for all fields which
        have this dimension : we will have a cross-section or a profile depending on time and level selection
        """
        plot_cross = plot(self.ta_zonal_mean, self.ta_zonal_mean2, title='Selecting index 10 for time', y="index",
                          time=3000.)
        self.assertEqual(str(plot_cross),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),operator='zonmean'),"
                         "ccdo(llbox(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),latmax=90,latmin=10,lonmax=150,"
                         "lonmin=50),operator='zonmean'),time=3000.0,title='Selecting index 10 for time',y='index')")
        ref_plotcross = os.sep.join([self.reference_directory, "test_C.7.png"])
        compare_picture_files(plot_cross, ref_plotcross)
        plot_cross_bis = plot(self.ta_zonal_mean, self.ta_zonal_mean2, title='Time and level selection => profile',
                              y="index", time=0, level=4)
        self.assertEqual(str(plot_cross_bis),
                         "plot(ccdo(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),operator='zonmean'),"
                         "ccdo(llbox(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),latmax=90,latmin=10,lonmax=150,"
                         "lonmin=50),operator='zonmean'),level=4,time=0,title='Time and level selection => profile',"
                         "y='index')")
        ref_plotcross_bis = os.sep.join([self.reference_directory, "test_C.8.png"])
        compare_picture_files(plot_cross_bis, ref_plotcross_bis)


class DataGplotProfiles(unittest.TestCase):

    def setUp(self):
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_data_plot"])
        self.january_ta = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly',
                             period="198001")
        self.ta = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="1980")
        self.january_ta_zonal_mean = ccdo(self.january_ta, operator="zonmean")
        self.ta_zonal_mean = ccdo(self.ta, operator="zonmean")
        self.january_cross_field = llbox(self.january_ta, latmin=10, latmax=90, lonmin=50, lonmax=150)
        self.cross_field = llbox(self.ta, latmin=10, latmax=90, lonmin=50, lonmax=150)
        self.january_ta_zonal_mean2 = ccdo(self.january_cross_field, operator="zonmean")
        self.ta_zonal_mean2 = ccdo(self.cross_field, operator="zonmean")
        self.january_ta_profile = ccdo(self.january_ta_zonal_mean, operator="mermean")
        self.ta_profile = ccdo(self.ta_zonal_mean, operator="mermean")
        self.january_ta_profile2 = ccdo(self.january_ta_zonal_mean2, operator="mermean")
        self.ta_profile2 = ccdo(self.ta_zonal_mean2, operator="mermean")

    @unittest.expectedFailure
    def test_gplot_profiles_1(self):
        """
        One profile, with a logarithmic scale

        TODO: Check why this test fails
        """
        plot_profile = plot(self.january_ta_profile, title='A profile', y="log")
        self.assertEqual(str(plot_profile),
                         "plot(ccdo(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),"
                         "operator='mermean'),title='A profile',y='log')")
        ref_plotprofile = os.sep.join([self.reference_directory, "test_D.1.png"])
        compare_picture_files(plot_profile, ref_plotprofile)

    @unittest.expectedFailure
    def test_gplot_profiles_2(self):
        """
        Two profiles, with a index-linear spacing for vertical axis (default)

        TODO: Check why this test fails
        """
        plot_profile = plot(self.january_ta_profile, self.january_ta_profile2, title='Two profiles', y="lin")
        self.assertEqual(str(plot_profile),
                         "plot(ccdo(ccdo(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),operator='zonmean'),"
                         "operator='mermean'),ccdo(ccdo(llbox(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),"
                         "latmax=90,latmin=10,lonmax=150,lonmin=50),operator='zonmean'),operator='mermean'),"
                         "title='Two profiles',y='lin')")
        ref_plotprofile = os.sep.join([self.reference_directory, "test_D.2.png"])
        compare_picture_files(plot_profile, ref_plotprofile)

    @unittest.expectedFailure
    def test_gplot_profiles_3(self):
        """
        A (t,z) profile, with a a logarithmic scale

        TODO: Check why this test fails
        """
        plot_profile = plot(self.ta_profile, self.ta_profile2, title='Profiles (t,z)', y="log", invXY=True)
        self.assertEqual(str(plot_profile),
                         "plot(ccdo(ccdo(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),operator='zonmean'),"
                         "operator='mermean'),ccdo(ccdo(llbox(ds('example|AMIPV6ALB2G|ta|1980|global|monthly'),"
                         "latmax=90,latmin=10,lonmax=150,lonmin=50),operator='zonmean'),operator='mermean'),invXY=True,"
                         "title='Profiles (t,z)',y='log')")
        ref_plotprofile = os.sep.join([self.reference_directory, "test_D.3.png"])
        compare_picture_files(plot_profile, ref_plotprofile)


class DataPlot(unittest.TestCase):

    def setUp(self):
        cdef("project", "example")
        cdef("frequency", "monthly")
        self.my_dataset = ds(simulation="AMIPV6ALB2G", variable="tas", period="1980-1981")
        self.my_dataset_light_80 = ds(simulation="AMIPV6ALB2G", variable="tas", period="198001")
        self.my_dataset_light_81 = ds(simulation="AMIPV6ALB2G", variable="tas", period="198101")
        cfile(self.my_dataset)
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_data_plot"])

    def test_data_plot_1(self):
        ta = time_average(self.my_dataset)
        map_test = plot(ta, title="TAS")
        map_ref = os.sep.join([self.reference_directory, "test_1.1.png"])
        compare_picture_files(map_test, map_ref)
        map_test = plot(ta, title="TAS", min=-15, max=25, delta=2., offset=-273.15, units="C")
        map_ref = os.sep.join([self.reference_directory, "test_1.2.png"])
        compare_picture_files(map_test, map_ref)

    def test_data_plot_2(self):
        ta = space_average(self.my_dataset)
        curve = curves(ta, title="AMIPV6")
        curve_ref = os.sep.join([self.reference_directory, "test_2.png"])
        compare_picture_files(curve, curve_ref)

    @unittest.expectedFailure
    def test_data_plot_3(self):
        """
        TODO: Check why this test fails
        """
        fig1 = plot(self.my_dataset_light_80, title="title", resolution="1600*2400")
        page1 = cpage([[None, fig1], [fig1, fig1], [fig1, fig1]],
                      widths=[0.2, 0.8], heights=[0.33, 0.33, 0.33], page_width=800, page_height=1200)
        ref_page1 = os.sep.join([self.reference_directory, "test3.1.png"])
        compare_picture_files(page1, ref_page1)
        page2 = cpage([[None, fig1], [fig1, fig1], [fig1, fig1]],
                      widths=[0.2, 0.8], heights=[0.33, 0.33, 0.33], title="Page title", background="grey90", x=-300,
                      y=26, pt=20, font='Utopia', ybox=60)
        ref_page2 = os.sep.join([self.reference_directory, "test3.2.png"])
        compare_picture_files(page2, ref_page2)
        page3 = cpage([[None, fig1], [fig1, fig1], [fig1, fig1]],
                      widths=[0.2, 0.8], heights=[0.33, 0.33, 0.33], title="Page title")
        ref_page3 = os.sep.join([self.reference_directory, "test3.3.png"])
        compare_picture_files(page3, ref_page3)
        page4 = cpage([[None, fig1], [fig1, fig1], [fig1, fig1]])
        ref_page4 = os.sep.join([self.reference_directory, "test3.4.png"])
        compare_picture_files(page4, ref_page4)
        page5 = cpage([[None, fig1], [fig1, fig1], [fig1, fig1]], page_trim=False)
        ref_page5 = os.sep.join([self.reference_directory, "test3.5.png"])
        compare_picture_files(page5, ref_page5)
        ens = cens({'1980': self.my_dataset_light_80, '1981': self.my_dataset_light_81})
        fig_ens = plot(ens, title="title")
        ref_ens_1 = os.sep.join([self.reference_directory, "test3.6-1.png"])
        ref_ens_2 = os.sep.join([self.reference_directory, "test3.6-2.png"])
        compare_picture_files(fig_ens, [ref_ens_1, ref_ens_2])
        page6 = cpage(fig_ens)
        ref_page6 = os.sep.join([self.reference_directory, "test3.7.png"])
        compare_picture_files(page6, ref_page6)
        page7 = cpage(fig_ens, heights=[0.8, 0.2], page_trim=False)
        ref_page7 = os.sep.join([self.reference_directory, "test3.8.png"])
        compare_picture_files(page7, ref_page7)
        pdfpage1 = cpage_pdf([[fig1, fig1], [fig1, fig1], [fig1, fig1]],
                             widths=[0.2, 0.8], heights=[0.33, 0.33, 0.33], page_width=1000., page_height=1500.,
                             scale=0.95, title='Page title', x=-5, y=5, font='ptm', pt='Huge', titlebox=True,
                             background="red")
        ref_pdfpage1 = os.sep.join([self.reference_directory, "test3.1.pdf"])
        compare_picture_files(pdfpage1, ref_pdfpage1)
        fig2 = plot(self.my_dataset_light_80, title="title", resolution="13*19", format="pdf")
        fig2_crop = cpdfcrop(fig2)
        pdfpage2 = cpage_pdf([[fig2_crop, fig2_crop], [fig2_crop, fig2_crop], [fig2_crop, fig2_crop]],
                             widths=[0.2, 0.8], heights=[0.33, 0.33, 0.33], page_width=1000., page_height=1500.,
                             scale=0.95, title='Page title', x=-5, y=10, font='ptm', pt='huge', titlebox=True,
                             background='yellow')
        ref_pdfpage2 = os.sep.join([self.reference_directory, "test3.2.pdf"])
        compare_picture_files(pdfpage2, ref_pdfpage2)


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_data_plot"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    craz()
    unittest.main()
    craz()
    remove_dir_and_content(tmp_directory)
