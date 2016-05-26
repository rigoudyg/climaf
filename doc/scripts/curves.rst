curves : plot multiple profiles (along p, lat, lon, time, ...) 
---------------------------------------------------------------

Plot a series of xy curves (along time, lat, lon or pressure/z_index)
for an ensemble dataset using NCL, and allowing for tuning a number of
graphic attributes   

**References** : http://www.ncl.ucar.edu

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - an ensemble dataset which can be up to 4-dimensional, but with
    only one non-degenerated dimension. Members can have different
    vector size.  

Remark : If x axis is time and time units are different among members,
the script convert all time periods to first's one

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
  - ``scale_aux``, ``offset_aux`` : for scaling the input auxiliary
    fields (x -> x*scale_aux + offset_aux); default = 1. and 0. (no
    scaling). These arguments will apply of the second to the nth
    field. 
  - ``units`` : name of the main field units; used in the caption;
    default is to use the corresponding CF metadata
  - ``y`` : y axis style
    
    - "lin" (default): data-linear spacing 
    - "index" : index-linear spacing, or
    - "log"  : logarithmic scale
  - ``X_axis`` : drives X axis when member profiles do not cover 
    the same range :   

    - X_axis="real" (default) : X axis will be the union of all X axes 
    - X_axis="aligned" : X axes will be aligned to the same origin
      (taking the first dataset as reference)  
  - ``invXY`` : set it to True to invert X axis and Y axis; default:
    False  
  - ``min``, ``max`` : min and max values for main field axis
  - ``fmt``: a string specifying the format of the tick labels for
    time x axis. This string is parsed as follows: the '%' acts as the
    escape character. The single character after every '%' is
    formatted according to the rule described here: 

    https://www.ncl.ucar.edu/Document/Functions/User_contributed/time_axis_labels.shtml

    In case fmt is absent, a minimal algorithm exists which tries to
    determine the format string depending on the time range length.
  - ``lgcols`` : number of columns for legend; default: 3.
  - ``options``, ``aux_options`` : strings for setting NCL graphic
    resources directly for main field and auxiliary fields
    respectively. These resources are separated by "|", as e.g. : 
    ' options="tiMainString=lv|xyLineThicknessF=5.",
    aux_options="xyLineColor=red" '. It is recommended to use argument
    ``aux_options`` only if you plot exactly two fields. Warning: all
    graphic resources set by ``options`` are applied to all fields,
    and graphic resources set by ``aux_options`` overwrite it for the
    second to the nth field. 

    These resources have higher priority than CliMAF default ones,
    which are :    

    - txFontHeightF = 0.010
    - tmXBLabelFontHeightF=0.008
    - tmYLLabelFontHeightF=0.008
    - tiXAxisFontHeightF=0.014
    - tiYAxisFontHeightF=0.014
    - tmXBLabelFontThicknessF = 3.0
    - tmYLLabelFontThicknessF = 3.0
    - txFontThicknessF = 3.0
    - xyLineThicknessF     = 3.0    
    - xyMonoDashPattern      = True
    - pmLegendDisplayMode    = "Always"            
    - pmLegendWidthF         = 0.12               
    - pmLegendHeightF        = 0.15               
    - lgLabelFontHeightF     = 0.009            
    - lgPerimOn              = False            
    - lgBoxMinorExtentF      = 0.2    
    - tiXAxisString, tiYAxisString= data @long_name (units) if data
      has "long_name" attribute (take the first file as ref.) 

    For more details, see: https://www.ncl.ucar.edu/

  - ``format`` : graphic output format, either 'png', 'pdf' or 'eps';
    default: 'png'. For 'png' format, all the surrounding extra white
    space are cropped with optional argument ``trim`` (but not for
    'pdf' or 'eps' format). In case of 'pdf' or 'eps' format, if you
    want to trim extra white space, use 'cpdfcrop' (which is 'pdfcrop'
    tool) or 'cepscrop' operator respectively.  
  - ``trim`` : set it to True if you want to crop all the surrounding
    extra white space for 'png' format; default: True. 
  - ``resolution`` : string for output image resolution

    - if format is "png", resolution specifies the width and height of
      resultant image in pixels as e.g. 800x1200; default (ncl):
      1024x1024
    - if format is "pdf" or "eps", resolution specifies either the
      width and height of the paper, as above but in inches unit, or a
      standard paper size by name, as e.g. 'A4'. Ncl uses a resolution
      of 72 dots per inch (dpi); default (ncl): 8.5x11 or "letter" (<=>
      612x792 in pixels)   
  
**Outputs** :
  - main output : a PNG or PDF or EPS figure

**Climaf call example**::
 
  >>> # Two time series
  >>> j0=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
  >>> j1=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")
  >>> ens=cens({'1980':j0, '1981':j1})
  >>> tas_ga=space_average(ens)
  >>> # Time axis is "aligned"
  >>> p=curves(tas_ga,title="Surface Temperature global average",X_axis="aligned",fmt="%c",options="tiMainString=my_title|xyLineThicknessF=5.",
  ... lgcols=2,format="pdf",resolution="11*17")  
  >>> cshow(p)
  >>> # Time axis is "real" and X and Y are inverted
  >>> p=curves(tas_ga,title="Surface Temperature global average",fmt="%c",options="tiMainString=my_title|xyLineThicknessF=5.",
  ... lgcols=2,trim=False,invXY=True)
  >>> cshow(p)

  >>> # Some datasets of "CNRM-CM5" model
  >>> d0=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1860")
  >>> d1=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1861")
  >>> d2=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1862")
  >>> d3=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1863")
  >>> d4=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1864")
  >>> ens2=cens({'1960':d0, '1961':d1, '1962':d2, '1963':d3, '1964':d4})
  >>> moy=space_average(ens2)
  >>> p=curves(moy,title="Surface Temperature global average") # Time axis is "real"
  >>> cshow(p)

  >>> # Zonal mean on different domains (different vector size)
  >>> d0=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="186001", domain=[-90,0,30,80])
  >>> d1=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="186001", domain=[0,40,30,80])
  >>> ta_zonal_mean=ccdo(d0,operator="zonmean")
  >>> ta_zonal_mean1=ccdo(d1,operator="zonmean")
  >>> ens=cens({'box1':ta_zonal_mean,'box2':ta_zonal_mean1})
  >>> figens=curves(ens,title="zonal mean")
  >>> cshow(figens)
  >>> # Same as above and X and Y are inverted
  >>> figens=curves(ens,title="zonal mean", invXY=True)
  >>> cshow(figens)

  >>> # Profil pressure/z_index
  >>> january_ta=ds(project='example', simulation="AMIPV6ALB2G", variable="ta", frequency='monthly', period="198001")
  >>> ta_zonal_mean=ccdo(january_ta, operator="zonmean")
  >>> ta_profile=ccdo(ta_zonal_mean, operator="mermean")
  >>> a=curves(ta_profile, title='A profile',y="index") 
  >>> cshow(a)
  >>> # Same as above and X and Y are inverted
  >>> a=curves(ta_profile, title='A profile',y="index",invXY=True) 
  >>> cshow(a)

**Side effects** : None

**Implementation** : Basic use of ncl: gsn_csm_xy
