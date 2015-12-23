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
; ncl lineplot.ncl infile=.. plotname=.. var=.. title=.. labels=.. colors=.. scale=.. offset=.. linp=1  X_axis=.. invXY=.. fmt=.. lgcols=.. options=... format=.. trim=.. resolution=..
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
; scale, offset : for scaling the input field (x -> x*scale + offset); default = 1. 
; and 0. (no scaling) 
;
; If argument linp=1 and data is a vertical profile, do not plot it in log(p) 
;
; X_axis : a string ("real" or "aligned") which determines X axis when datasets
; does not cover the same range;  default to "real".
;    - X_axis="real"           : X axis will be the union of all X axis
;    - X_axis="aligned"        : X axis will be aligned to the same origin 
;                                (take the first file as ref.)  
;
; invXY : set it to True to invert X axis and Y axis; default: False 
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
; options : a string for all graphic resources defined by user, each separated by "|", 
; as e.g. : ' options="tiMainString=lv|xyLineThicknessF=5." '.This list is priority in 
; front of graphic resources in this script.
;
; format : graphic output format, either 'png' or 'pdf'; default: 'png'.
;
; trim : set it to True if you want to crop all the surrounding white extra space for 'png' 
; format; default: True.
;
; resolution : string for output image resolution
;  - if format is "png", resolution specifies the width and height of resultant image in pixels 
;    as e.g. 800x1200; default (ncl): 1024x1024
;  - if format is "pdf", resolution specifies either the width and height of the paper, as above 
;    but in inches unit, or a standard paper size by name, as e.g. 'A4'; default (ncl): 8.5x11 or
;    "letter" (<=> 612x792 in pixels)  
;
;
; Third version : L.Vignon - december 2015

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
  
  if .not. ismissing(str_match(str,"True")) then
    return(True)
  else
    if .not. ismissing(str_match(str,"False")) then
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
  files=str_split(infile," ")
  n=dimsizes(files)
  if .not. all(isfilepresent(files)) then
    print("Some file cannot be accessed")
    status_exit(2)
  end if
  
  if (.not. isvar("X_axis")) then X_axis="real" end if
  if (.not. isvar("scale")) then scale=1.0 end if 
  if (.not. isvar("offset")) then offset=0.0 end if
  if (.not. isvar("type")) then type="png" end if
  if (.not. isvar("trim")) then trim=True end if
  if (.not. isvar("invXY")) then invXY=False end if

  ;---Read all data
;  all_files=addfiles(files,"r")
;  ListSetType (all_files, "cat") ; default
  
  ;---Extraction of Xaxis values to obtain min and max, and to have smartly tick marks if x axis is time 
;  all_fld=all_files[:]->$var$
;  Var_DimNames = getvardims(all_fld)  ; getting dimensions from metadata
;  dime=dimsizes(all_fld)
  ;print(all_files[:]->$var$)
  ;print("different of")
  ;print(all_fld)
  ;print(all_fld&$Var_DimNames(1)$) ; latitude of first file
  ;print(all_files[:]->$var$&$Var_DimNames(1)$) ; latitude of two files
  ;print(all_fld); time duplicated (if a single and same value in each file) but not for lat and lon which are the ones of first file

;  found=False
;  coord=""
;  do dim=0,dimsizes(dime)-1
    
;    if ( (.not. ismissing(str_match(Var_DimNames(dim),"time"))) .or. (.not. ismissing(str_match(Var_DimNames(dim),"Time"))) ) .and. (count_unique_values(all_fld&$Var_DimNames(dim)$) .eq. 1) then
;      dime(dim)=1 ; remove same time values
;    end if

;    if (dime(dim) .gt. 1) .and. ismissing(str_match(Var_DimNames(dim),"bnds")) then
  
;      if found then
;        print("There is more than one non-singleton dim in one of files:"+coord+" "+Var_DimNames(dim))
;        print(Var_DimNames(dim))
;        status_exit(1)
;      end if 
      ; print("First non-singleton dim is :"+Var_DimNames(dim)+" size is "+dime(dim))
;      found=True

;      coord=Var_DimNames(dim)
      ;
      ; useless (addfiles: if the aggregated time coordinate has different units in the individual aggregated
      ; files, the values are adjusted to conform to the units of the first file in the aggregation)
      ; => Don't work !!!!
;      if (all(all_files[:]&$coord$@standard_name .eq. "time")) then  ; add str_match (with "time" or "Time") & different units 
;          all_fld&$coord$=cd_convert(all_fld&$coord$, all_files[0]->$var$&$coord$@units) ; all_fld&$coord$ with metadata
;      end if
      ; => Don't work.......... => read data individually (cf. below)

      ;
      ; check if all X axis have same standard name
;      if isatt(all_files[0]->$var$&$coord$,"standard_name") then
;        first_file_std_name=all_files[0]->$var$&$coord$@standard_name
;      end if
  
      ;if ( (.not. ismissing(str_match(all_files[:]&$coord$@standard_name,"Time"))) .or. (.not. ismissing(str_match(all_files[:]&$coord$@standard_name,"time"))) ) .and. (.not. all(all_files[:]&$coord$@standard_name .eq. first_file_std_name)) then
      ;  print("Files have not the same standard_name for coordinate variable "+coord)
      ;  status_exit(1)
      ;end if 
        
;      do i=0, n-1
;        if isatt(all_files[i]->$var$&$coord$,"standard_name") \
;          .and. (all_files[i]->$var$&$coord$@standard_name .ne. first_file_std_name) then
;          print("Warning: Files have not the same standard_name for coordinate variable "+coord)
          ;status_exit(1) ; it is possible that standard_name are not the same but it is the same coordinate variable (ex: lat & latitude)
;        end if   
;      end do

      ; data vector for X axis
      ;if (.not. ismissing(str_match(coord,"time"))) .or. (.not. ismissing(str_match(coord,"Time"))) then ;;add
;      if ( X_axis .eq. "real" ) then
;        if (.not. ismissing(str_match(coord,"time"))) .or. (.not. ismissing(str_match(coord,"Time"))) then 
;          Xaxis=all_fld&$coord$             ; take union of all time periods (with metadata but ok just for time)
;        else
;          Xaxis=all_files[:]->$var$&$coord$ ; no metadata but cat of all coordinate variable 
;        end if
;      else
;        Xaxis=all_files[0]->$var$&$coord$ ; take first file origin as reference for time axis
;      end if  

;    end if ; dime(dim) .gt. 1
;  end do ; dim
  
  
  ;---Read data individually for extraction of Xaxis values to obtain min and max,
  ;---and to have smartly tick marks if x axis is time 
  ;my_list=NewList("lifo")

  do i=0, n-1
    ffile=addfile(files(i),"r")
    if isfilevar(ffile,var) then 
      if i .ne. 0 then delete(fld) end if
      if (getfilevartypes(ffile,var) .eq. "short") then
        fld = short2flt( ffile->$var$ )
      else
        fld = ffile->$var$
      end if
    else
      print("File "+infile+" does not include variable "+var)
      status_exit(1)
    end if
    
    ;fld=fld*tofloat(scale)+tofloat(offset)
    
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

	; time conversion if necessary (useless if X_axis is not real so add condition ??)
        if ( ( (.not. ismissing(str_match(fld&$coord$@standard_name,"Time"))) .or. (.not. ismissing(str_match(fld&$coord$@standard_name,"time"))) ) \
          .or. ( (.not. ismissing(str_match(coord,"Time"))) .or. (.not. ismissing(str_match(coord,"time"))) ) ) \
          .and. isatt(fld&$coord$,"units") .and. (fld&$coord$@units .ne. unit_first_file) then
          fld&$coord$=cd_convert(fld&$coord$, unit_first_file) 
        end if

	; data vector for X axis

        ;if X_axis .eq. "real" then
        ;  ListAppend(my_list,lfld&$lcoord$) ; Store coordinate in 'my_list'. PB : List :dynamic !!!!
        ;else 
        ;  if i .eq. 0 then
        ;    Xaxis=lfld&$lcoord$
        ;  end if
        ;end if
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
 
  ; Reconstruction of all Xaxis if X_axis is "real" : PB because List is dynamic
;  if X_axis .eq. "real" then
;    Xaxis=my_list[0]
;    do i=1, ListCount(my_list)-1
;      if ( (dimsizes(my_list[i]) .eq. dimsizes(Xaxis)) .and. (.not. (any(my_list[i] .eq. Xaxis))) ) \
;        .or. (dimsizes(my_list[i]) .ne. dimsizes(Xaxis)) then   
;        if typeof(my_list[i]) .ne. typeof(Xaxis) then
;          t=todouble(my_list[i])
;          tmp_new_tab = array_append_record (Xaxis, t, 0)
;        else
;          tmp_new_tab = array_append_record (Xaxis, my_list[i], 0)
;        end if
;        delete(Xaxis)
;        Xaxis=tmp_new_tab
;        delete(tmp_new_tab)
;      end if
;    end do
;  end if

  ;---Resources for "left" variable
  res=True
  res@gsnDraw          = False   ; Will draw later, after overlaying
  res@gsnFrame         = False   ; all plots
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
  if ( .not. ( isatt(Xaxis,"axis") .and. (Xaxis@axis .eq. "Z") ) .and. (.not. invXY) ) \
    .or. ( isatt(Xaxis,"axis") .and. (Xaxis@axis .eq. "Z") .and. invXY ) then
    res@trXMinF=min(Xaxis)
    res@trXMaxF=max(Xaxis)
  else
    res@trYMinF=min(Xaxis)
    res@trYMaxF=max(Xaxis)
    ;res@trXMinF=min(all_fld)
    ;res@trXMaxF=max(all_fld)
  end if
  ;print(Xaxis)
  ;print(min(Xaxis))
  ;print(max(Xaxis))
  
  ;---Thickness
  res@xyLineThicknessF     = 3.0      ; default is 1
  res@xyMonoDashPattern    = True     ; force all solid lines

  ;---Set resources for colors 
  colornames=new(n, string)
  if n .le. 9 then
    stdcolors=(/"black","red","blue","green","orange","purple","violet","grey","brown"/)
  else
    stdcolors=new(n, string)
    stdcolors(0:8)=(/"black","red","blue","green","orange","purple","violet","grey","brown"/)
    do i=0,(n-9)-1 stdcolors(i+9)=stdcolors(i) end do
  end if
 
  do i=0,n-1 colornames(i)=stdcolors(i) end do

  if isvar("colors") then 
    tab=str_split(colors," ")
    do i=0,dimsizes(tab)-1 
      colornames(i)=tab(i) 
    end do
  end if 
   
  ;---Titles and labels
  if .not. isvar("title") then title="title" end if

  if .not. isvar("labels") then labels=title end if
  tab_labels=str_split(labels,"$")

  res@tiMainString     = title                       ; add title
  
  ;---Resources for legend
  res@pmLegendDisplayMode    = "Always"              ; turn on legend
  res@pmLegendWidthF         = 0.12                  ; Change width and
  res@pmLegendHeightF        = 0.15                  ; height of legend.
  res@lgLabelFontHeightF     = 0.009;.011            ; change font height
  res@lgPerimOn              = False                 ; no box around
  ;res@lgItemOrder           = (/1,0/)               ; reverse legend
  res@lgBoxMinorExtentF      = 0.2                   ; Shorten the legend lines (ncl default: 0.6)
  
  ;---linp
  logp=True
  if (isvar("linp")) then if linp .eq. 1 then logp=False end if end if
  
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
        if type .eq. "pdf" then ;image resolution in inches
          type@wkPaperWidthF  = width 
          type@wkPaperHeightF = height
        end if
      end if
      
    else ; resolution is not given by 'widthxheight' or 'width*height'
      
      if type .eq. "png" then 
        print("For PNG output, resolution must be given by 'widthxheight' or 'width*height'")
        status_exit(1)
      else
        if type .eq. "pdf" then
          type@wkPaperSize = resolution
        end if
      end if
      
    end if ; str_match
  end if ;resolution
  ;if type .eq. "pdf" then
  ;  type@wkPDFResolution = 3600
  ;end if

  wks = gsn_open_wks(type,plotname) 

  ;xvalue=new(3, float)        ; for res@pmLegendParallelPosF
  ;xvalue=(/0.15,0.5,0.85/)   
  ;yvalue=new(4, float)        ; for res@pmLegendOrthogonalPosF  
  ;yvalue=(/-0.1,0.,0.1,0.2/)

  ;---Create n plots
  do i=0, n-1 

    ; Read variable
    ffile=addfile(files(i),"r") ; all_files[i]
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
        ; Store coordinate in 'ax'
        if ( X_axis .eq. "real" ) then
          ;ax:=fld&$coord$
          if i .ne. 0 then delete(ax) end if
          ax=fld&$coord$
        else
          ; Take first file as reference for X axis if X_axis .eq. "aligned"
          if (i .eq. 0 ) then 
            ax=fld&$coord$
          end if
        end if
        
        ;if isatt(fld, "long_name") then
        ;  fld_long_name=fld@long_name
        ;end if
        ;fld=fld*tofloat(scale)+tofloat(offset)

        ; Create plot
        res@xyLineColor = colornames(i)
        res@xyExplicitLegendLabels = "  "+tab_labels(i)
        
        if (i .eq. 0) then 
          res@pmLegendParallelPosF   = 0.1    ;0.15 ;xvalue(0) 
          res@pmLegendOrthogonalPosF = -0.14  ;-0.15 ;yvalue(0)      ; move up slightly 

          if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
            if (ax@positive .eq. "down") then 
              res@trYReverse = True ; reverse Y-axis
            end if
            if logp then 
              res@xyYStyle = "Log" 
              set_pres_hgt_axes(ax,res,True)
            end if

            if isatt(fld, "long_name") then
            ;if isvar(fld_long_name) then
              if invXY then
                res@tiYAxisString = fld@long_name ;fld_long_name
              else
                res@tiXAxisString = fld@long_name ;fld_long_name
              end if
            end if
            ; Read graphic resources list defined by user (with optional argument 'options')
            if isvar("options") then
              res_list(options, res)
            end if

            if invXY then
              plot = gsn_csm_xy(wks,ax,ndtooned(fld),res)
            else
              plot = gsn_csm_xy(wks,ndtooned(fld),ax,res) 
            end if
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
            ;if isvar(fld_long_name) then
              if invXY then
                res@tiXAxisString = fld@long_name ;fld_long_name 
              else
                res@tiYAxisString = fld@long_name ;fld_long_name  
              end if
            end if
            if isvar("options") then
              res_list(options, res)
            end if
            if invXY then
              plot = gsn_csm_xy(wks,ndtooned(fld),ax,res)
            else
              plot = gsn_csm_xy(wks,ax,ndtooned(fld),res)
            end if

          end if  ; fld&$coord$@axis .eq. "Z"

        else
          ;res@pmLegendParallelPosF   = 0.15+0.35*(tointeger(i/4.)) ;xvalue(tointeger(i/4.)) 
          ;res@pmLegendOrthogonalPosF = -0.15+0.05*(mod(i,4.)) ;-0.1+0.1*(mod(i,4.))  ;yvalue(mod(i,4.)) 
          if isvar("lgcols") then
            lgcols=lgcols
          else
            lgcols=3
          end if
          line_labels_space=0.9/lgcols ; space between labels on a line
          res@pmLegendParallelPosF   = 0.1+line_labels_space*(mod(i,lgcols)) 
          res@pmLegendOrthogonalPosF = -0.14+0.05*(tointeger(i/lgcols))   
          
          if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
            if (ax@positive .eq. "down") then 
              res@trYReverse = True ; reverse Y-axis
            end if
            if logp then 
              res@xyYStyle = "Log" 
              set_pres_hgt_axes(ax,res,True)
            end if
 
            if invXY then
              over = gsn_csm_xy(wks,ax,ndtooned(fld),res)
            else
              over = gsn_csm_xy(wks,ndtooned(fld),ax,res)
            end if

          else

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



