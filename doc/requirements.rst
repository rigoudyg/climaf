.. _requirements:

Requirements and ackowledgements
---------------------------------

This is a natural place for acknowledging the unvaluable contribution
by the tools/packages listed below, with a special thanks to CDO
2015: Climate Data Operators. Available at: http://www.mpimet.mpg.de/cdo

- Python version 2.7, with one NetCDF package (either
  Scientific.IO.NetCDF, or NETCDF4 or scipy.io.netcdf)
- `ImageMagick <http://www.imagemagick.org/>`_ (modules : convert,  identify) ; this is usually included in Linux distributions
- `nco <http://nco.sourceforge.net/>`_ (ncatted, ncdump, ncwa, ncrcat) 
- `cdo <https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html>`_
- `Ncl 6.3.0 <http://www.ncl.ucar.edu/>`_  (Ncl >= 6.1.2 may work, nevertheless)
- Data files must be `CF compliant <http://cfconventions.org/>`_
- `exiv2 <http://www.exiv2.org/>`_ (Image metadata manipulation tool); exiv2 is a program to read and write Exif, IPTC, XMP metadata and image comments.

Optional 

- `ncview <http://meteora.ucsd.edu:80/~pierce/ncview_home_page.html>`_

If wanting to build or modify CliMAF documentation :

- Sphinx : 

  - executable 'sphinx-build' 
  - package sphinxcontrib.napoleon 
