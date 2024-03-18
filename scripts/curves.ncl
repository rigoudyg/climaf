; Plotting any series of data vectors from A SERIES of NetCDF file, 
; for the same variable (indicated by arg "var")

; Check on all files that only one dimension is not a singleton

; Do not assume that all datasets have the same dimensions set

; Do not assume that all data vectors have the same size and coordinate
; array (take the first one as ref. to aligne x axis to the same origin, 
; or take the union of all x axis)

; Tick marks are smartly adapted to the time period duration

; Usage:
;;;;;;;;;;
; ncl curves.ncl infile=.. plotname=.. var=.. title=.. labels=.. colors=.. myscale=.. myoffset=.. myscale_aux=.. myoffset_aux=.. y="log"  X_axis=.. invXY=..vmin=.. vmax=.. fmt=.. lgcols=.. options=... format=.. trim=.. resolution=..
;
; infile, plotname and var are mandatory
;
; infile : a string holding the series of filenames, separated by whitespaces
;
; title : string for graphic title
;
; labels : a string with one label per member, separated by character '$'
;
; colors : a string holding a series of color NCL names, separated by whitespaces
; 
; myscale, myoffset : for scaling the input field (x -> x*scale + offset); default = 1. 
; and 0. (no scaling) 
;
; myscale_aux, myoffset_aux : for scaling the input auxiliary fields 
; (x -> x*scale_aux + offset_aux); default = 1. and 0. (no scaling). 
; These arguments will apply of the second to the nth field.
;
; units : name of the main field units; used in the caption; default is to use the 
; corresponding CF metadata
;
; y : y axis style
;    - default: vertical axis with data-linear spacing (y="lin"), or
;    - "index" for getting a vertical axis with index-linear spacing, or
;    - "log" for getting a vertical axis will have a logarithmic scale
;
; X_axis : a string ("real" or "aligned") which determines X axis when datasets
; does not cover the same range;  default to "real".
;    - X_axis="real"           : X axis will be the union of all X axis
;    - X_axis="aligned"        : X axis will be aligned to the same origin 
;                                (take the first file as ref.)  
;
; invXY : set it to True to invert X axis and Y axis; default: False 
;
; vmin, vmax : min and max values for main field axis
;
; fmt : a string specifying the format of the tick labels for time x axis. This 
; string is parsed as follows: the '%' acts as the escape character. The single 
; character after every '%' is formatted according to the rule described here:
; https://www.ncl.ucar.edu/Document/Functions/User_contributed/time_axis_labels.shtml
; In case fmt is absent, a minimal algorithm exists which tries to determine the 
; format string depending on the length and values of the date-time.
; 
; lgcols : number of columns for legend. lgcols must be different from 0; default: 3.
;
; options, aux_options : strings for all graphic resources defined by user for main field 
; and auxiliary field respectively. These resources are separated by "|", 
; as e.g. : ' options="tiMainString=lv|xyLineThicknessF=5.", aux_options="xyLineColor=red" '.
; This list is priority in front of graphic resources in this script.
; It is recommended to use argument aux_options only if you plot exactly two fields.
;
; format : graphic output format, either 'png', 'pdf' or 'eps'; default: 'png'.
;
; trim : set it to True if you want to crop all the surrounding white extra space for 'png' 
; format; default: True.
;
; resolution : string for output image resolution
;  - if format is "png", resolution specifies the width and height of resultant image in pixels 
;    as e.g. 800x1200; default (ncl): 1024x1024
;  - if format is "pdf" or "eps", resolution specifies either the width and height of the paper, 
;    as above but in inches unit, or a standard paper size by name, as e.g. 'A4'. Ncl uses a 
;    resolution of 72 dots per inch (dpi); default (ncl): 8.5x11 or "letter" (<=> 612x792 in pixels)  
;
;
; Third version : L.Vignon - january 2016

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl" 

;--------------------------------------------------------------------------------------------
undef("str_convert")
; Convert an input string into logical, integer, float or the same string
function str_convert(str:string)

local val, valf
begin
  
  if .not. ismissing(str_match(str,"true")) then
    return(True)
  else
    if .not. ismissing(str_match(str,"false")) then
      return(False)
    else

      if ismissing(str_match(str,".")) then ; integer or string
        val=stringtoint(str)
        if ismissing(val) then 
          return(str)
        else
          return(val)
        end if
      else                                  ; float (or string)
        valf=stringtofloat(str)
        if ismissing(valf) then 
          return(str)
        else
          return(valf)
        end if
      end if

    end if ; if False
  end if ; if True

end 

;--------------------------------------------------------------------------------------------

undef("res_list")
; Extract graphic resources from 'opt' associated to resource 'fct_res'
procedure res_list(opt:string, fct_res:logical)

local reslist, resval, key, value, value_convert
begin
  
  reslist=str_split(opt,"|")
  do i=0,dimsizes(reslist)-1 
    resval=str_split(reslist(i),"=")
    key=resval(0)
    value=resval(1)
    value_convert=str_convert(value)
    fct_res@$key$=value_convert
    delete(value_convert)
  end do
  
  return
end

;--------------------------------------------------------------------------------------------


begin
  if (.not. isvar("X_axis")) then X_axis="real" end if
  if (.not. isvar("myscale")) then myscale=1.0 end if 
  if (.not. isvar("myoffset")) then myoffset=0.0 end if
  if (.not. isvar("myscale_aux")) then myscale_aux=1.0 end if
  if (.not. isvar("myoffset_aux")) then myoffset_aux=0.0 end if 
  if (.not. isvar("type")) then type="png" end if

  if (.not. isvar("invXY")) then
    invXY=False
  else
    inv=str_convert(invXY)
    delete(invXY)
    invXY=inv
  end if

  if (.not. isvar("trim")) then
    trim=True
  else
    inv=str_convert(trim)
    delete(trim)
    trim=inv
  end if

  files=str_split(infile," ")
  n=dimsizes(files)
  if .not. all(isfilepresent(files)) then
    print("Some file cannot be accessed")
    status_exit(2)
  end if 

  do i=0, n-1
    ffile=addfile(files(i),"r")
    if isfilevar(ffile,var) then 
      if i .ne. 0 then delete(fld) end if
      if (getfilevartypes(ffile,var) .eq. "short") then
        fld = short2flt( ffile->$var$ )
      else if (getfilevartypes(ffile,var) .eq. "double") then
        fld = dble2flt( ffile->$var$ )
      else
        fld = ffile->$var$
      end if
      end if
    else
      print("File "+infile+" does not include variable "+var)
      status_exit(1)
    end if
    if (i .eq. 0) then
      fld_min=min(fld*tofloat(myscale)+tofloat(myoffset))
      fld_max=max(fld*tofloat(myscale)+tofloat(myoffset))
    else 
      alt_fld_min=min(fld*tofloat(myscale_aux)+tofloat(myoffset_aux))
      if (fld_min .gt. alt_fld_min) then fld_min=alt_fld_min end if
      alt_fld_max=max(fld*tofloat(myscale_aux)+tofloat(myoffset_aux))
      if (fld_max .lt. alt_fld_max) then fld_max=alt_fld_max end if
     end if
   
    ;fld=fld*tofloat(myscale)+tofloat(myoffset)
    
    Var_DimNames = getvardims(fld)  ; getting dimensions from metadata
    dime=dimsizes(fld)
    found=False
    coord=""
    
    do dim=0,dimsizes(dime)-1
      if (dime(dim) .gt. 1) .and. ismissing(str_match(Var_DimNames(dim),"bnds")) then
        
        if found then
          print("There is more than one non-singleton dim in one of files:"+coord+" "+Var_DimNames(dim))
          print(Var_DimNames(dim))
          status_exit(1)
        end if 
        ; print("First non-singleton dim is :"+Var_DimNames(dim)+" size is "+dime(dim))
        found=True
        coord=Var_DimNames(dim)
      
        if (i .eq. 0) then
          if isatt(fld&$coord$,"units") then
            unit_first_file=fld&$coord$@units
          end if
          if isatt(fld&$coord$,"standard_name") then
            first_file_std_name=fld&$coord$@standard_name
          end if
        end if
        
	; check if all X axis have same standard name
        if isatt(fld&$coord$,"standard_name") \
          .and. (fld&$coord$@standard_name .ne. first_file_std_name) then
          print("Warning: Files have not the same standard_name for coordinate variable "+coord)
          ;status_exit(1) ; it is possible that standard_name are not the same but it is the same coordinate variable (ex: lat & latitude)
        end if   
      
	; time conversion if necessary (useless if X_axis is not real so add condition ?)
        if ( ( (.not. ismissing(str_match(fld&$coord$@standard_name,"Time"))) .or. (.not. ismissing(str_match(fld&$coord$@standard_name,"time"))) ) \
          .or. ( (.not. ismissing(str_match(coord,"Time"))) .or. (.not. ismissing(str_match(coord,"time"))) ) ) \
          .and. isatt(fld&$coord$,"units") .and. (fld&$coord$@units .ne. unit_first_file) then
          fld&$coord$=dble2flt(cd_convert(fld&$coord$, unit_first_file))
        end if

	; data vector for X axis
        if (i .eq. 0) then
          Xaxis=fld&$coord$              ; Take first file as reference for X axis  
        else
          if (X_axis .eq. "real") then
       
            if ( (dimsizes(fld&$coord$) .eq. dimsizes(Xaxis)) .and. (.not. (any(fld&$coord$ .eq. Xaxis))) ) \
              .or. (dimsizes(fld&$coord$) .ne. dimsizes(Xaxis)) then
              
              if typeof(fld&$coord$) .ne. typeof(Xaxis) then
                t=todouble(fld&$coord$)
                tmp_new_tab = array_append_record (Xaxis, t, 0)
              else
                tmp_new_tab = array_append_record (Xaxis, fld&$coord$, 0)
              end if
              delete(Xaxis)
              Xaxis=tmp_new_tab
              delete(tmp_new_tab)
            end if

          end if ; X_axis is "real"
        end if ; i eq 0

      end if ; dime(dim) .gt. 1
    end do ; dim
  end do ; file
  qsort(Xaxis)
  tmpXaxis=get_unique_values(Xaxis)
  copy_VarMeta(Xaxis,tmpXaxis)
  delete(Xaxis)
  Xaxis=tmpXaxis
  delete(tmpXaxis)
 
  ;---Resources for "left" variable
  res=True
  res@gsnDraw          = False    ; Will draw later, after overlaying
  res@gsnFrame         = False    ; all plots
  res@gsnMaximize = True
  ;res@vpWidthF    = 0.7          ; Make plots wider
  ;res@vpHeightF   = 0.5
  res@vpXF = 0.5
  res@vpWidthF = 0.45
  res@vpHeightF = 0.45
  res@txFontHeightF = 0.010
  res@tmXBLabelFontHeightF=0.008
  res@tmYLLabelFontHeightF=0.008
  res@tiXAxisFontHeightF=0.014
  res@tiYAxisFontHeightF=0.014
  if type.eq."png" then
    res@tmXBLabelFontThicknessF = 3.0
    res@tmYLLabelFontThicknessF = 3.0
    res@txFontThicknessF = 3.0
  end if

  ; Min and max x axis
  if ( .not. ( (isatt(Xaxis,"axis") .and. ((Xaxis@axis .eq. "Z") .or. (Xaxis@axis .eq. "z"))) \
    .or. .not. ismissing(str_match(coord,"dept")) .or. (coord .eq. "sigma") .or. (coord .eq. "z") \
    .or. (coord .eq. "Z") .or. (coord .eq. "plev") .or. (coord .eq. "lev") .or. (coord .eq. "level") \
    .or. (coord .eq. "p") .or. (coord .eq. "pressure") ) .and. (.not. invXY) ) \
    .or. ( ( (isatt(Xaxis,"axis") .and. ((Xaxis@axis .eq. "Z") .or. (Xaxis@axis .eq. "z"))) \
    .or. .not. ismissing(str_match(coord,"dept")) .or. (coord .eq. "sigma") \
    .or. (coord .eq. "z") .or. (coord .eq. "Z") .or. (coord .eq. "plev") \
    .or. (coord .eq. "lev") .or. (coord .eq. "level") .or. (coord .eq. "p") .or. (coord .eq. "pressure") ) .and. invXY ) then
    res@trXMinF=min(Xaxis)
    res@trXMaxF=max(Xaxis)
    res@trYMinF=fld_min
    res@trYMaxF=fld_max
    if isvar("vmin") then res@trYMinF=vmin end if
    if isvar("vmax") then res@trYMaxF=vmax end if
  else
    res@trYMinF=min(Xaxis)
    res@trYMaxF=max(Xaxis)
    res@trXMinF=fld_min
    res@trXMaxF=fld_max
    if isvar("vmin") then res@trXMinF=vmin end if
    if isvar("vmax") then res@trXMaxF=vmax end if
  end if
  
  ;---Thickness
  res@xyLineThicknessF     = 3.0      ; default is 1
  res@xyMonoDashPattern    = True     ; force all solid lines

  ;---Set resources for colors
  ncolors=10
  set13=(/"black","red","blue","green","orange","purple","violet","grey","brown","darkgreen","cyan3","goldenrod4","rosybrown3"/)
  set10=(/"black","red","blue","green","orange","purple","violet","grey","brown","darkgreen"/)
  if n .le. ncolors then
    stdcolors=set10
  else
    stdcolors=new(n, string)
    stdcolors(0:ncolors-1)=set10
    do i=ncolors,n-1 stdcolors(i)=stdcolors(i-ncolors) end do
  end if
  ;print(stdcolors)
 
  colornames=new(n, string)
  do i=0,n-1 colornames(i)=stdcolors(i) end do

  if isvar("colors") then 
    tab=str_split(colors," ")
    do i=0,dimsizes(tab)-1 
      colornames(i)=tab(i) 
    end do
  end if 
   
  ;---Titles and labels
  tab_labels=new(n,string)
  do i=0,n-1 tab_labels(i)="no_label" end do
  if .not. isvar("labels") then 
    if isvar("title") then 
      labels=title
    else
      labels="no_label"
    end if
  end if
  tmp_labels=str_split(labels,"$")
  do i=0,dimsizes(tmp_labels)-1 
    if i .lt. n then
      tab_labels(i)=tmp_labels(i) 
    end if
  end do
  
  if isvar("title") then res@tiMainString = title end if ; add title
  if (.not. isvar("units")) then 
    if (isatt(fld,"units")) then units=fld@units else units="None" end if
  end if
  
  ;---Resources for legend
  res@pmLegendDisplayMode    = "Always"              ; turn on legend
  res@pmLegendWidthF         = 0.12                  ; Change width and
  res@pmLegendHeightF        = 0.15                  ; height of legend.
  res@lgLabelFontHeightF     = 0.009;.011            ; change font height
  res@lgPerimOn              = False                 ; no box around
  ;res@lgItemOrder           = (/1,0/)               ; reverse legend
  res@lgBoxMinorExtentF      = 0.2                   ; Shorten the legend lines (ncl default: 0.6)
  
  ;---y axis style
  if .not. isvar("y") then y="lin" end if
  
  if (.not. ismissing(str_match(coord,"time"))) .or. (.not. ismissing(str_match(coord,"Time"))) then 
    ;--------------------------------------------------
    ; The time_axis_label function adds additional
    ; resources to "res" to produce nicely-formatted
    ; time labels on X axis. This function only works
    ; if you have a time "units" recognized by the
    ; cd_calendar function.
    ; ---------------------------------------------------
    restick = True

    if invXY then 
      restick@ttmAxis="YL"  ; "XB" by default
    end if

    if (isvar("fmt")) then
      restick@ttmFormat=fmt
    else
      ymdhms = cd_calendar(Xaxis,0) ;return array of dimension dimsizes(Xaxis) x 6 and of type float
                                    ;ymdhms(:,0) <=> years, ymdhms(:,1) <=> months, etc
      ymdhms_dim = dimsizes(ymdhms)
      nt = ymdhms_dim(0)
      
      if ymdhms(nt-1,0) .ne. ymdhms(0,0) then ;year changes
        
        if (abs(ymdhms(nt-1,0)-ymdhms(0,0)) .eq. 1) then ;2 years 
        ;(by default, 'time_axis_labels' sets "%c%y")
          restick@ttmNumTicks=8      ; approximate number of tick labels
          restick@ttmMajorStride=3   ; number of timesteps desired between major tickmarks 
          restick@ttmMinorStride=1   ; number of timesteps desired between minor tickmarks
          restick@ttmFormat="%N/%y"         
        else 
          if (abs(ymdhms(nt-1,0)-ymdhms(0,0)) .eq. 9) then ;10 years 
          ;(by default, 'time_axis_labels' sets "%Y")
            restick@ttmNumTicks=12
            restick@ttmMajorStride=12
            restick@ttmMinorStride=3
            restick@ttmFormat="%N/%y" 
          end if
        end if
      end if
    end if
    time_axis_labels(Xaxis,res,restick)
  end if

  ;---Open workstation

  if isvar("resolution") then
    if ( .not. ismissing(str_match(resolution,"x")) .or. .not. ismissing(str_match(resolution,"*")) ) then
      
      if .not. ismissing(str_match(resolution,"x")) then
        nb_pixels_or_inches = str_split(resolution, "x")
      else
        if .not. ismissing(str_match(resolution,"*")) then
          nb_pixels_or_inches = str_split(resolution, "*")
        end if
      end if
      width = stringtofloat(nb_pixels_or_inches(0))
      height = stringtofloat(nb_pixels_or_inches(1))
      
      if type .eq. "png" then ;image resolution in pixels
        type@wkWidth = width
        type@wkHeight = height
      else 
        if (type .eq. "pdf") .or. (type .eq. "eps") then ;image resolution in inches
          type@wkPaperWidthF  = width 
          type@wkPaperHeightF = height
        end if
      end if
      
    else ; resolution is not given by 'widthxheight' or 'width*height'
      
      if type .eq. "png" then 
        print("For PNG output, resolution must be given by 'widthxheight' or 'width*height'")
        status_exit(1)
      else
        if (type .eq. "pdf") .or. (type .eq. "eps") then
          type@wkPaperSize = resolution
        end if
      end if
      
    end if ; str_match
  end if ;resolution
  ;if type .eq. "pdf" then
  ;  type@wkPDFResolution = 3600
  ;end if

  wks = gsn_open_wks(type,plotname) 

  ;---Create n plots
  do i=0, n-1 

    ; Read variable
    ffile=addfile(files(i),"r") 
    if isfilevar(ffile,var) then
      delete(fld)
      if (getfilevartypes(ffile,var) .eq. "short") then
        fld = short2flt( ffile->$var$ )
      else
        fld = ffile->$var$
      end if
    else
      print("File "+infile+" does not include variable "+var)
      status_exit(1)
    end if
    
    ; Search and extract relevant vector
    Var_DimNames = getvardims(fld)  ; getting dimensions from metadata
    dime=dimsizes(fld)
    rank=dimsizes(dime)
    found=False
    coord=""

    do dim=0,rank-1
      ;print("analyzing "+Var_DimNames(dim))
      
      if dime(dim) .gt. 1 then 
       
        if found then
          print("There is more than one non-singleton dim for file "+ffile+ " :"+coord+" "+Var_DimNames(dim))
          status_exit(1)
        end if 
        found=True

        coord=Var_DimNames(dim)

        ; Time conversion if necessary (useless if X_axis is not real so add condition ?)
        if ( ( (.not. ismissing(str_match(fld&$coord$@standard_name,"Time"))) .or. (.not. ismissing(str_match(fld&$coord$@standard_name,"time"))) ) \
          .or. ( (.not. ismissing(str_match(coord,"Time"))) .or. (.not. ismissing(str_match(coord,"time"))) ) ) \
          .and. isatt(fld&$coord$,"units") .and. (fld&$coord$@units .ne. unit_first_file) then
          fld&$coord$=tofloat(cd_convert(fld&$coord$, unit_first_file))
        end if

        ; Store coordinate in 'ax'
        if ( X_axis .eq. "real" ) then
          ;ax:=fld&$coord$
          if i .ne. 0 then delete(ax) end if
          ax=fld&$coord$
        else
          ; Take first file as reference for X axis if X_axis .eq. "aligned"
          if (i .eq. 0) then 
            ax=fld&$coord$
          end if
        end if

        ; Create plot
        res@xyLineColor = colornames(i)
        res@xyDashPattern = i/ncolors 
        res@xyExplicitLegendLabels = "  "+tab_labels(i)
        
        if (i .eq. 0) then 
          
          tmpfld=fld*tofloat(myscale)+tofloat(myoffset)
          copy_VarMeta(fld,tmpfld)
          delete(fld)
          fld=tmpfld
          delete(tmpfld)

          res@pmLegendParallelPosF   = 0.1        ; move right slightly 
          res@pmLegendOrthogonalPosF = -0.14      ; move up slightly 

          if ( (isatt(ax,"axis") .and. ((ax@axis .eq. "Z") .or. (ax@axis .eq. "z"))) \
            .or. .not. ismissing(str_match(coord,"dept")) .or. (coord .eq. "sigma") \
            .or. (coord .eq. "z") .or. (coord .eq. "Z") .or. (coord .eq. "plev") \
            .or. (coord .eq. "lev") .or. (coord .eq. "level") .or. (coord .eq. "p") \
            .or. (coord .eq. "pressure") ) then

            if invXY then
              if (ax@positive .eq. "down") then 
                res@trXReverse = True ; reverse X-axis
              end if
              if (y .eq. "log") then
                res@xyXStyle = "Log" 
              else
                if (y .eq. "index") then  ; index linear 
                  res@xyXStyle = "Irregular"
                  res@xyXIrregularPoints = ax
                end if
              end if
              if isatt(fld, "long_name") then res@tiYAxisString = fld@long_name + " (" + units + ")" end if
              ;Read graphic resources list defined by user (with optional argument 'options')
              if isvar("options") then res_list(options, res) end if
              plot = gsn_csm_xy(wks,ax,ndtooned(fld),res)

            else
              if (ax@positive .eq. "down") then 
                res@trYReverse = True ; reverse Y-axis
              end if
              if (y .eq. "log") then
                res@xyYStyle = "Log" 
                set_pres_hgt_axes(ax,res,True)
              else
                if (y .eq. "index") then  ; index linear 
                  res@xyYStyle = "Irregular"
                  res@xyYIrregularPoints = ax
                end if
              end if
              if isatt(fld, "long_name") then res@tiXAxisString = fld@long_name + " (" + units + ")" end if
              if isvar("options") then res_list(options, res) end if
              plot = gsn_csm_xy(wks,ndtooned(fld),ax,res) 
            end if ; invXY
          else

            if isatt(ax, "long_name") \
              .and. (ismissing(str_match(coord,"time"))) .and. (ismissing(str_match(coord,"Time"))) then
              if invXY then
                res@tiYAxisString = ax@long_name
              else
                res@tiXAxisString = ax@long_name
              end if
            end if
            if isatt(fld, "long_name") then
              if invXY then
                res@tiXAxisString = fld@long_name + " (" + units + ")"
              else
                res@tiYAxisString = fld@long_name + " (" + units + ")"
              end if
            end if
            if isvar("options") then res_list(options, res) end if
            if invXY then
              plot = gsn_csm_xy(wks,ndtooned(fld),ax,res)
            else
              plot = gsn_csm_xy(wks,ax,ndtooned(fld),res)
            end if

          end if  ; fld&$coord$@axis .eq. "Z"

        else ; field '2' to 'n'

          tmpfld=fld*tofloat(myscale_aux)+tofloat(myoffset_aux)
          copy_VarMeta(fld,tmpfld)
          delete(fld)
          fld=tmpfld
          delete(tmpfld)
      
          if isvar("lgcols") then
            lgcols=lgcols
          else
            lgcols=3
          end if
          line_labels_space=0.9/lgcols ; space between labels on a line
          res@pmLegendParallelPosF   = 0.1+line_labels_space*(mod(i,lgcols)) 
          res@pmLegendOrthogonalPosF = -0.14+0.05*(tointeger(i/lgcols))   
          
          if ( (isatt(ax,"axis") .and. ((ax@axis .eq. "Z") .or. (ax@axis .eq. "z"))) \
            .or. .not. ismissing(str_match(coord,"dept")) .or. (coord .eq. "sigma") \
            .or. (coord .eq. "z") .or. (coord .eq. "Z") .or. (coord .eq. "plev") \
            .or. (coord .eq. "lev") .or. (coord .eq. "level") .or. (coord .eq. "p") \
            .or. (coord .eq. "pressure") ) then

            if invXY then
              if (ax@positive .eq. "down") then 
                res@trXReverse = True ; reverse X-axis
              end if
              if (y .eq. "log") then
                res@xyXStyle = "Log" 
              else
                if (y .eq. "index") then  ; index linear 
                  res@xyXStyle = "Irregular"
                  res@xyXIrregularPoints = ax
                end if
              end if
              if (i .eq. 1) .and. isvar("aux_options") then res_list(aux_options, res) end if
              over = gsn_csm_xy(wks,ax,ndtooned(fld),res)
            else
              if (ax@positive .eq. "down") then 
                res@trYReverse = True ; reverse Y-axis
              end if
              if (y .eq. "log") then
                res@xyYStyle = "Log" 
              else
                if (y .eq. "index") then  ; index linear 
                  res@xyYStyle = "Irregular"
                  res@xyYIrregularPoints = ax
                end if
              end if
              if (i .eq. 1) .and. isvar("aux_options") then res_list(aux_options, res) end if
              over = gsn_csm_xy(wks,ndtooned(fld),ax,res)
            end if ; invXY

          else

            if (i .eq. 1) .and. isvar("aux_options") then res_list(aux_options, res) end if
            if invXY then
              over = gsn_csm_xy(wks,ndtooned(fld),ax,res)
            else
              over = gsn_csm_xy(wks,ax,ndtooned(fld),res)
            end if

          end if  ; fld&$coord$@axis .eq. "Z"

          ;---Overlay one plot on the other
          overlay(plot,over)
        end if ; condition 'if' on files
       
      end if ; dime .gt. 1 
    end do ; loop on dimensions

    if .not. found then 
      print("There is no non-sigleton dim for file "+ffile)
      status_exit(1)
    end if 
    
  end do ; loop on files  

  draw(plot) ; This will draw all n plots
  frame(wks)

  if ( type .eq. "png" .and. trim ) then
      system("convert "+plotname+" -trim "+plotname)
  end if
  
  status_exit(0)

end



