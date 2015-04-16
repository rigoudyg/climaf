.. _requirements:

Requirements
------------

- Python version 2.x, with package Scientific.IO.NetCDF
- `ImageMagick <http://www.imagemagick.org/>`_ (modules : convert,  identify) ; this is usually included in Linux distributions
- `nco <http://nco.sourceforge.net/>`_ (ncatted, ncdump, ncwa, ncrcat) 
- `cdo <https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html>`_
- Data files must be `CF compliant <http://cfconventions.org/>`_

Other requirements if using some CliMAF standard operators (see :ref:`standard_operators`) :  

- `ncview <http://meteora.ucsd.edu:80/~pierce/ncview_home_page.html>`_
- `Ncl 6 <http://www.ncl.ucar.edu/>`_

If wanting to build or modify CliMAF documentation :

- Sphinx : executable sphinx-build and 
- one of the Python package : sphinx.ext.napoleon or sphinxcontrib.napoleon
