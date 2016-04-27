slice : extract a slice at a given dimension's range
------------------------------------------------------

Extract a slice on specified dimension at a given range from the input
dataset, and average this dimension.

**References** : http://nco.sourceforge.net/nco.html#ncks

**Provider / contact** : climaf at meteo dot fr

**Inputs** : any dataset (but only one)

**Mandatory arguments**: 
  - ``dim`` : dimension on which you want to do the extraction 
  - ``min``, ``max`` : range for the specified dimension. Set it to
    integers if you want to extract the corresponding index or floats
    if you want to extract closest coordinate value.   

**Optional arguments**:
  - none

**Output** : the extracted object

**Climaf call example**::
 
  >>> # Plot a model MOC slice
  >>> moc_model=ds(variable="msftmyz", project='CMIP5',model='CNRM-CM5', frequency="mon", realm="ocean",
  >>> ... table="Omon", version="*", period="1980", experiment="historical",simulation="r1i1p1")
  >>> moc_model_mean=time_average(moc_model)
  >>> # Extract basin of rank 1 (def: Atlantique=1)
  >>> moc_model_mean_atl=slice(moc_model_mean, dim='x', min=1, max=1)
  >>> # Mask values
  >>> moc_model_mean_atl_mask=mask(moc_model_mean_atl,miss=0.0)
  >>> # Plot 
  >>> plot_moc_slice=plot(moc_model_mean_atl_mask, title="MOC",y="index",
  >>> ... min=-10.,max=30.,delta=1.,scale=1e-3,units="Sv",options="trXMinF=-30.")
  >>> cshow(plot_moc_slice)

  >>> # Plot a model MOC slice at latitude 26
  >>> moc_model_26=slice(moc_model_mean_atl_mask, dim='lat', min=26.5, max=26.5)
  >>> plot_moc_slice2=plot(moc_model_26, title="MOC",y="index",
  >>> ... min=-10.,max=30.,delta=1.,scale=1e-3,units="Sv",options="trXMinF=-30.")
  >>> cshow(plot_moc_slice2)

**Side effects** : none

**Implementation** : using NCO operators (ncks, ncwa)
