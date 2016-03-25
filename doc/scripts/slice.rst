slice : extract selected variable on specified dimension at a given value
--------------------------------------------------------------------------

Extract selected variable on specified dimension at a given value from
the input file. 

**References** : http://nco.sourceforge.net/nco.html#ncks

**Provider / contact** : climaf at meteo dot fr

**Inputs** : any dataset (but only one)

**Mandatory arguments**: 
  - ``dim`` : dimension on which you want to do the extraction 
  - ``num`` : value for the specified dimension

**Optional arguments**:
  - none

**Output** : the extracted object

**Climaf call example**::
 
  >>> # These two examples only work on Ciclad

  >>> # Plot a model MOC slice
  >>> moc_model=ds(variable="msftmyz", project='CMIP5',model='CNRM-CM5', frequency="mon", realm="ocean",
  >>> ... table="Omon", version="latest", period="1980", experiment="historical",simulation="r1i1p1")
  >>> moc_model_mean=time_average(moc_model)
  >>> # Extract basin of rank 1 (def: Atlantique=1)
  >>> moc_model_mean_atl=slice(moc_model_mean, dim='x', num=1)
  >>> # Mask values
  >>> moc_model_mean_atl_mask=mask(moc_model_mean_atl,miss=0.0)
  >>> # Plot 
  >>> plot_moc_slice=plot(moc_model_mean_atl_mask, title="MOC",y="index",
  >>> ... min=-10.,max=30.,delta=1.,scale=1e-3,units="Sv",options="trXMinF=-30.")
  >>> cshow(plot_moc_slice)

  >>> # Plot a model MOC slice at latitude 26
  >>> moc_model_26=slice(moc_model_mean_atl_mask, dim='lat', num=26.5)
  >>> plot_moc_slice2=plot(moc_model_26, title="MOC",y="index",
  >>> ... min=-10.,max=30.,delta=1.,scale=1e-3,units="Sv",options="trXMinF=-30.")
  >>> cshow(plot_moc_slice2)

**Side effects** : none

**Implementation** : using NCO operators (ncks, ncwa)
