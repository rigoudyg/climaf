ensemble_ts_plot : plot time series
---------------------------------------------------------------

Plot time series using a matplotlib python script. Allows a variety of controls on the plot (see below).
The input is a CliMAF ensemble. You can use ts_plot for a more user-friendly use of ensemble_ts_plot (allowing other inputs).


**References** : https://matplotlib.org/ 

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):

  - a CliMAF ensemble
  - optional arguments listed below

Remarks : 

- 

**Mandatory arguments**: None
  

**Optional arguments**:

   - colors: colors separated by commas
   - lw: lines thicknesses (commas separated)
   - highlight_period: Highlight a period on a time series (thicker line) ; provide the periods yearstart_yearend separated by commas (Ex: 1980_2005,1990_2000 to highlight the first period on the first dataset, and the second period on the second dataset)
   - highlight_period_lw: Thickness of the highlighted period
   - min, max: minimum and maximum value
   - offset, scale: apply an offset and a scale to all your time series
   - xlim: Provide the start date and end date to force the X axis. Ex: 1950-01-01,2005-12-31
   - ylim: Provide the interval for the Y axis
   #- time_offset', action='store', default=None, help='Add a time offset to the beginning of the time series')
   - text: add some text in the plot; the user provides a triplet separared with commas x,y,text; separate the triplets with | if you want to provide multiple texts. Ex: x1,y1,text1|x2,y2,text2
   - text_fontsize: fontsize of the text (separate with commas if provide several
   - text_colors: color of the text (separate with commas if provide several)
   - text_verticalalignment: Vertical alignment of the text (separate with commas if provide several
   - text_horizontalalignment: Horizontal alignment of the text (separate with commas if provide several

   - xlabel, ylabel: X and Y axis label
   - xlabel_fontsize, ylabel_fontsize: X and Y axis label size
   - tick_size: Ticks size
   - fig_size: Size of the figure in inches => width*height Ex: 15*5
   - left_string: Left string
   - right_string: Right string
   - center_string: Center string
   - left_string_fontsize: Left string size
   - right_string_fontsize: Right string size
   - center_string_fontsize: Center string size

   - legend_colors: legend colors separated by commas
   - legend_labels: Labels of the legend
   - legend_xy_pos: x,y Position of the corner of the box (by default = upper left corner). Example= "1.02,1"
   - legend_loc: Choose the corner of the legend box to specify the position of the legend box; by default 2 (upper left corner), take values 1, 2, 3 or 4 (see resource loc of pyplot legend)
   - legend_fontsize: Font size in the legend
   - legend_ncol: Number of columns in the legend
   - legend_frame: Draw the box around the legend? True/False
   - legend_lw: Line widths (provide either one for all, or one by time series separated by commas)
   - draw_legend: Draw the legend? True/False
   - append_custom_legend_to_default: Append the custom legend to the default one? True/False

   # -- Control margins
   - left_margin: Position of the left border of the figure in the plot
   - right_margin: Position of the right border of the figure in the plot
   - bottom_margin: Position of the bottom border of the figure in the plot
   - top_margin: Position of the top border of the figure in the plot

   - horizontal_lines_values: Y values for horizontal lines
   - horizontal_lines_styles: Horizontal lines styles
   - horizontal_lines_lw: Horizontal lines thickness
   - horizontal_lines_colors: Horizontal lines colors
   - vertical_lines_values: Y values for vertical lines
   - vertical_lines_styles: vertical lines styles
   - vertical_lines_lw: vertical lines thickness
   - vertical_lines_colors: vertical lines colors

# -- Default values
default_left_string_fontsize = 30.
default_center_string_fontsize = 20.
default_right_string_fontsize = 20.
default_tick_size = 15.
default_xlabel_fontsize = 20.
default_ylabel_fontsize = 20.



  - ``title`` : string for graphic title; default: no title

    Remarks: the ~ character has a special meaning in NCL strings. It
    represents a function code. See function codes example page
    http://www.ncl.ucar.edu/Applications/fcodes.shtml for (more)
    examples of function codes. Particularly: 

    - The ~C~ will put a carriage return to the title. By default it
      is left justified. If you need it centered, you will have to add
      spaces.
    - Use a ~Z#~ to resize text in mid-stream. The # refers to the
      percent of normal. 

  - ``labels`` : a string with one label per member, separated by
    character '$'
  - ``colors`` : a string with one NCL color name per member,
    separated by whitespaces
    - X_axis="real" (default) : X axis will be the union of all X axes 
    - X_axis="aligned" : X axes will be aligned to the same origin
      (taking the first dataset as reference)  

**Outputs** :
  - main output : a PNG figure

**Climaf call example**::
 
  >>> # Two time series
  >>> j0=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1980")
  >>> j1=ds(project='example',simulation="AMIPV6ALB2G", variable="tas", frequency='monthly', period="1981")
  >>> ens=cens({'1980':j0, '1981':j1})
  >>> tas_ga=space_average(ens)
  >>> # Time axis is "aligned"
  >>> p=curves(tas_ga,title="Surface Temperature global average",X_axis="aligned",fmt="%c",options="tiMainString=my_title|xyLineThicknessF=5.",
  ... lgcols=2,format="pdf",resolution="11*17")  
  
  >>> # Some datasets of "CNRM-CM5" model
  >>> d0=ds(project='CMIP5', model="CNRM-CM5", experiment="1pctCO2", variable="tas", period="1860")

**Side effects** : None

**Implementation** : script based on matplotlib pyplot 
