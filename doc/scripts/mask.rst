mask : set constant to missing value
--------------------------------------

Set the given constant to missing value.

**References** : https://code.zmaw.de/projects/cdo/embedded/index.html#x1-2440002.6.14

**Provider / contact** : climaf at meteo dot fr

**Inputs** : any dataset (but only one)

**Mandatory arguments**: 
  - ``miss`` : the value you want to mask

**Optional arguments**:
  - none

**Output** : the masked object

**Climaf call example**::
 
  >>> # This example only work on Ciclad

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

**Side effects** : none

**Implementation** : using CDO with operator setctomiss
