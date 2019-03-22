from climaf.api import *
from climaf.cache import csync
from joblib import Parallel, delayed
import multiprocessing


def parallel_section(section, **kwargs):
    wkwargs = kwargs.copy()
    # -- Get the number of cores available
    if 'num_cores' not in wkwargs:
        num_cores = multiprocessing.cpu_count()
    else:
        num_cores = wkwargs[num_cores]
        wkwargs.pop('num_cores')
    #
    # -- Build the list of plot CRS we will execute in parallel with do_cfile=True
    wkwargs.update(dict(do_cfile=False))
    plots_crs = section(**wkwargs)
    #
    #
    if len(plots_crs) < num_cores:
        num_cores = len(plots_crs)
    print 'num_cores = ', num_cores
    #
    # -- Execute the plots in parallel
    r = Parallel(n_jobs=num_cores)(delayed(safe_mode_cfile_plot)(climaf_crs) for climaf_crs in plots_crs)
    #
    # -- Synchronize the cache after parallel computation
    csync(True)
    #
    wkwargs.update(dict(do_cfile=True))
    if 'do_parallel' in wkwargs:
        wkwargs.update(dict(do_parallel=False))
    return section(**wkwargs)
