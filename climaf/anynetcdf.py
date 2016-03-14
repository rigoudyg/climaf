from climaf.clogging import clogger

try :
    from Scientific.IO.NetCDF import NetCDFFile as ncf
except ImportError:
    try :
        from NetCDF4 import netcdf_file as ncf
    except ImportError:
        try :
            from NetCDF4 import Dataset as ncf
        except ImportError:
            try :
                from scipy.io.netcdf import netcdf_file as ncf
            except ImportError:
                clogger.critical("Netcdf handling is yet available only with modules Scientific.IO.Netcdf or NetCDF4 or scipy.io.netcdf ")
                #raise Climaf_Netcdf_Error("Netcdf handling is yet available only with modules Scientific.IO.Netcdf or NetCDF4 or scipy.io.netcdf ")

