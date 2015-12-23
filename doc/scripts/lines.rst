lines : plot multiple profiles (along p, lat, lon, time, ...) 
---------------------------------------------------------------

Plot a series of xy curves (along time, lat, lon or pressure/z_index)
for an ensemble dataset using NCL 

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - an ensemble dataset which can be up to 4-dimensional, but with
    only one non-degenerated dimension. Members can have different
    vector size.  

Remark : If x axis is time and time units are different, the script
convert all time period into the same unit (take the first file as
ref.)  

**Mandatory arguments**: None (but ``title`` is recommended)

**Optional arguments**:

  - ``title`` : string for graphic title; optional : CliMAF will
    provide the CRS of the dataset 
  - ``labels`` : a string with one label per member, separated by
    character '$'
  - ``colors`` : a string with one NCL color name per member,
    separated by whitespaces
  - ``scale``, ``offset`` : for scaling the input field (x ->
    x*scale + offset); default = 1. and 0. (no scaling) 
  - ``linp`` : set it to 1 for getting a vertical axis with
    index-linear spacing  
  - ``X_axis`` : a string ("real" or "aligned") which determines X
    axis when datasets does not cover the same range; default to
    "real".   

    - X_axis="real"    : X axis will be the union of all X axis 
    - X_axis="aligned" : X axis will be aligned to the same origin
      (take the first file as ref.)  
  - ``invXY`` : set it to True to invert X axis and Y axis; default:
    False  
  - ``fmt``: a string specifying the format of the tick labels for
    time x axis. This string is parsed as follows: the '%' acts as the
    escape character. The single character after every '%' is
    formatted according to the rule described here: 

    https://www.ncl.ucar.edu/Document/Functions/User_contributed/time_axis_labels.shtml

    In case fmt is absent, a minimal algorithm exists which tries to
    determine the format string depending on the length and values of
    the date-time. 
  - ``lgcols`` : number of columns for legend. lgcols must be
    different from 0; default: 3.
  - ``options`` : a string for all graphic resources defined by user,
    each separated by "|", as e.g. :
    ' options="tiMainString=lv|xyLineThicknessF=5." '. This list is
    priority in front of graphic resources in the script, the list of
    CliMAF default graphic resource is here : 

    - res@txFontHeightF = 0.010
    - res@tmXBLabelFontHeightF=0.008
    - res@tmYLLabelFontHeightF=0.008
    - res@tiXAxisFontHeightF=0.014
    - res@tiYAxisFontHeightF=0.014
    - res@tmXBLabelFontThicknessF = 3.0
    - res@tmYLLabelFontThicknessF = 3.0
    - res@txFontThicknessF = 3.0
    - res@xyLineThicknessF     = 3.0    
    - res@xyMonoDashPattern      = True
    - res@pmLegendDisplayMode    = "Always"            
    - res@pmLegendWidthF         = 0.12               
    - res@pmLegendHeightF        = 0.15               
    - res@lgLabelFontHeightF     = 0.009            
    - res@lgPerimOn              = False            
    - res@lgBoxMinorExtentF      = 0.2    
    - res@tiXAxisString, res@tiYAxisString= data@long_name if data has
      "long_name" attribute (take the first file as ref.)
    For more details, see: https://www.ncl.ucar.edu/

  - ``format`` : graphic output format, either 'png' or 'pdf';
    default: 'png'. For 'png' format, all the surrounding white extra
    space are cropped with optional argument ``trim`` (but not for
    'pdf' format). In case of 'pdf' format, if you want to trim white
    extra space, use 'cpdfcrop' operator which is 'pdfcrop' tool and
    which preserves in more metadata.  
  - ``trim`` : set it to True if you want to crop all the surrounding
    white extra space for 'png' format; default: True.
  - ``resolution`` : string for output image resolution

    - if format is "png", resolution specifies the width and height of
      resultant image in pixels as e.g. 800x1200; default (ncl):
      1024x1024
    - if format is "pdf", resolution specifies either the width and
      height of the paper, as above but in inches unit, or a standard
      paper size by name, as e.g. 'A4'; default (ncl): 8.5x11 or
      "letter" (<=> 612x792 in pixels)  
  
**Outputs** :

  - main output : a PNG or PDF figure

**Climaf call example**::
 
  >>> # Two time series
  >>> j0=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
  >>> j1=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")
  >>> ens=cens(['1980','1981'],j0,j1)
  >>> tas_ga=space_average(ens)
  >>> # Time axis is "aligned"
  >>> p=lines(tas_ga,title="Surface Temperature global average",X_axis="aligned",fmt="%c",options="tiMainString=my_title|xyLineThicknessF=5.",
  ... lgcols=2,format="pdf",resolution="11*17")  
  >>> cshow(p)
  >>> # Time axis is "real" and X and Y are inverted
  >>> p=lines(tas_ga,title="Surface Temperature global average",fmt="%c",options="tiMainString=my_title|xyLineThicknessF=5.",
  ... lgcols=2,trim=False,invXY=True)
  >>> cshow(p)

  >>> # Some datasets of "CNRM-CM5" model
  >>> d0=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1860")
  >>> d1=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1861")
  >>> d2=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1862")
  >>> d3=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1863")
  >>> d4=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1864")
  >>> ens2=cens(['1960','1961','1962','1963','1964'],d0,d1,d2,d3,d4)
  >>> moy=space_average(ens2)
  >>> p=lines(moy,title="Surface Temperature global average") # Time axis is "real"
  >>> cshow(p)

  >>> # Zonal mean on different domains (different vector size)
  >>> d0=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="186001", domain=[-90,0,30,80])
  >>> d1=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="186001", domain=[0,40,30,80])
  >>> ta_zonal_mean=ccdo(d0,operator="zonmean")
  >>> ta_zonal_mean1=ccdo(d1,operator="zonmean")
  >>> ens=cens(['lat1','lat2'],ta_zonal_mean,ta_zonal_mean1)
  >>> figens=lines(ens,title="zonal mean")
  >>> cshow(figens)
  >>> # Same as above and X and Y are inverted
  >>> figens=lines(ens,title="zonal mean", invXY=True)
  >>> cshow(figens)

  >>> # Profil pressure/z_index
  >>> january_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
  >>> ta_zonal_mean=ccdo(january_ta, operator="zonmean")
  >>> ta_profile=ccdo(ta_zonal_mean, operator="mermean")
  >>> plot_profile1=lines(ta_profile, title='A profile',linp=1) 
  >>> a=lines(ta_profile, title='A profile',linp=1) 
  >>> cshow(a)
  >>> # Same as above and X and Y are inverted
  >>> a=lines(ta_profile, title='A profile',linp=1,invXY=True) 
  >>> cshow(a)
