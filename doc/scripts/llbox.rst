llbox : extract a latitude-longitude box
---------------------------------------------------------

Extract a lat-lon domain using CDO 

**References** : https://code.zmaw.de/projects/cdo/embedded/1.6.4/cdo.html#x1-1250002.3.4

**Provider / contact** : climaf at meteo dot fr

**Input** : any object or dataset 

**Mandatory argument**: 

- ``latmin`` : minimum latitude
- ``latmax`` : maximum latitude
- ``lonmin`` : minimum longitude
- ``lonmax`` : maximum longitude

**Output** : the same object, extracted

**Climaf call example** ::
 
  >>> ds= .... #some dataset, with whatever variable
  >>> sub_ds=llbox(ds, latmin=30, latmax=60, lonmin=-30, lonmax=30)  

**Side effects** : none

**Implementation** : using cdo with operator ``sellonlatbox`` through script mcdo.sh, which can also select a
variable, a time period ...; 

**Note** : it is generally more cost-effective to select the latlon
box at the stage of the dataset definition, as in e.g.::

  >>> dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980-1981", domain=[10,80,-50,40])

