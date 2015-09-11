; Plotting any series of data vectors from A SERIES of NetCDF file, 
; for the same variable (indicated by arg "var")

; Check on all files that only one dimension is not a singleton

; Do not assume that all datasets have the same dimensions set

; Do not assume that all data vectors have the same size and coordinate
; array (take the first one as ref. to aligne time axis to the same origin, 
; or take the union of all time periods)

; Tick marks are smartly adapted to the time period duration

; Usage:
;;;;;;;;;;
; ncl lineplot.ncl infile=.. plotname=.. var=.. T_axis="real" title=.. labels=.. colors=.. thickness=.. linp=1 fmt=..
;
; infile, plotname and var are mandatory
;
; infile : a string holding the series of filenames, separated by whitespaces
;
; T_axis : a string ("real" or "tweaked") which determines time axis when datasets
; does not cover the same time period; 
;    - T_axis="real"    : time axis will be the union of all time periods
;    - T_axis="tweaked" : time axis will be aligned to the same origin (take the 
;                         first file as ref.) 
;
; colors : a string holding a series of color NCL names, separated by whitespaces
;
; thickness : the common thickness (defaults to 2.0)
;
; If argument linp=1 and data is a vertical profile, do not plot it in log(p) 
;
; fmt : a string specifying the format of the tick labels. This string is parsed 
; as follows: the '%' acts as the escape character. The single character after 
; every '%' is formatted according to the rule described here:
; https://www.ncl.ucar.edu/Document/Functions/User_contributed/time_axis_labels.shtml
; In case fmt is absent, a minimal algorithm exists which tries to determine the 
; format string depending on the length and values of the date-time.
;
; Second version : L.Vignon - july 2015

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl" 

begin
  files=str_split(infile," ")
  n=dimsizes(files)
  if .not. all(isfilepresent(files)) then
    print("Some file cannot be accessed")
    status_exit(2)
  end if
  
  ;---Read all data
  all_files=addfiles(files,"r")

  ;---Extraction of min and max x-range 
  if (.not. isvar("T_axis")) then T_axis="real" end if

  all_fld=all_files[:]->$var$
  ;print(all_fld)
  Var_DimNames = getvardims(all_fld)  ; getting dimensions from metadata
  dime=dimsizes(all_fld)
  found=False
  coord=""
  do dim=0,dimsizes(dime)-1
    if dime(dim) .gt. 1 then

      if found then
        print("There is more than one non-singleton dim for file "+ffile+ " :"+coord+ Var_DimNames(dim))
        status_exit(1)
      end if 
      found=True

      coord=Var_DimNames(dim)
      ;
      ; useless (addfiles: if the aggregated time coordinate has different units in the individual aggregated
      ; files, the values are adjusted to conform to the units of the first file in the aggregation)
      ;if (all(all_files[:]&$coord$@standard_name .eq. "time")) then  
      ;  all_fld&$coord$ = cd_convert(all_fld&$coord$, all_files[0]->$var$&$coord$@units)
      ;
      ; check if all X axis are "time" else NCL sets first file attributes to other files
      ;;if (.not. all(all_files[:]&$coord$@standard_name .eq. "time")) then
      ;;  first_file_axis_name=all_files[0]->$var$&$coord$@standard_name
      if (.not. ismissing(str_match(all_files[:]&$coord$@long_name,"Time"))) .or. (.not. ismissing(str_match(all_files[:]&$coord$@long_name,"time"))) then
        first_file_axis_name=all_files[0]->$var$&$coord$@long_name
        if (.not. all(all_files[:]&$coord$@long_name .eq. first_file_axis_name)) then
          print("Files have not same axis for variable "+coord)
          status_exit(1)
        end if        
      end if
      ; data vector for X axis
      if (.not. ismissing(str_match(coord,"time"))) then ;;add
        if ( T_axis .eq. "real" ) then
          Xaxis=all_fld&$coord$             ; take union of all time periods
        else
          Xaxis=all_files[0]->$var$&$coord$ ; take first file origin as reference for time axis
        end if      
      end if
    end if
  end do
  
  ;---Resources for "left" variable
  res=True
  res@gsnDraw          = False   ; Will draw later, after overlaying
  res@gsnFrame         = False   ; all plots
 
  res@vpWidthF    = 0.7          ; Make plots wider
  res@vpHeightF   = 0.5

  res@trXMinF=min(Xaxis)
  res@trXMaxF=max(Xaxis)
  res@trYMinF=min(all_fld) 
  res@trYMaxF=max(all_fld) 

  ;---Thickness
  if isvar("thickness") then 
    res@xyLineThicknessF     = thickness 
  else
    res@xyLineThicknessF     = 2.0      ; default is 1
  end if
  res@xyMonoDashPattern      = True     ; force all solid lines

  ;---Set resources for colors and labels
  colornames=new(n, string)
  if n .le. 9 then
    stdcolors=(/"black","red","blue","yellow","green","orange","purple","violet","grey"/)
  else
    stdcolors=new(n, string)
    stdcolors(0:8)=(/"black","red","blue","yellow","green","orange","purple","violet","grey"/)
    do i=0,(n-9)-1 stdcolors(i+9)=stdcolors(i) end do
  end if
 
  do i=0,n-1 colornames(i)=stdcolors(i) end do
  if isvar("colors") then 
    tab=str_split(colors," ")
    do i=0,dimsizes(tab)-1 
      colornames(i)=tab(i) 
    end do
  end if 
  
  ;---Titles
  if .not. isvar("title") then title="title" end if

  if .not. isvar("labels") then labels=title end if
  tab_labels=str_split(labels,"$")

  res@tiMainString     = title                    ; add title
  
  ;---Resources for legend
  res@pmLegendDisplayMode    = "Always"              ; turn on legend
  res@pmLegendWidthF         = 0.12                  ; Change width and
  res@pmLegendHeightF        = 0.15                  ; height of legend.
  res@lgLabelFontHeightF     = .011                  ; change font height
  res@lgPerimOn              = False                 ; no box around
  ;res@lgItemOrder           = (/1,0/)               ; reverse legend

  ;---linp
  logp=True
  if (isvar("linp")) then if linp .eq. 1 then logp=False end if end if
  
  ;--------------------------------------------------
  ; The time_axis_label function adds additional
  ; resources to "res" to produce nicely-formatted
  ; time labels on X axis. This function only works
  ; if you have a time "units" recognized by the
  ; cd_calendar function.
  ;---------------------------------------------------
  restick = True
    
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
      else if (abs(ymdhms(nt-1,0)-ymdhms(0,0)) .eq. 9) then ;10 years 
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

  ;---Open workstation
  wks = gsn_open_wks ("png",plotname) 

  ;xvalue=new(3, float)        ; for res@pmLegendParallelPosF
  ;xvalue=(/0.15,0.5,0.85/)   
  ;yvalue=new(4, float)        ; for res@pmLegendOrthogonalPosF  
  ;yvalue=(/-0.1,0.,0.1,0.2/)

  ;---Create n plots
  do i=0, n-1 

    ; Read variable
    ffile=all_files[i]
    if isfilevar(ffile,var) then
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
    Var_DimNames:= getvardims(fld)  ; getting dimensions from metadata
    dime:=dimsizes(fld)
    rank=dimsizes(dime)
    found=False
    coord:=""
   
    do dim=0,rank-1
      ;print("analyzing "+Var_DimNames(dim))
      if dime(dim) .gt. 1 then 
       
        if found then
          print("There is more than one non-singleton dim for file "+ffile+ " :"+coord+ Var_DimNames(dim))
          status_exit(1)
        end if 
        found=True

        coord=Var_DimNames(dim)
        ;print(coord)
        ; Store coordinate in 'ax'
        if ( T_axis .eq. "real" ) then
          ax:=fld&$coord$
        else
          ; Take first file as reference for X axis if T_axis .eq. "tweaked"
          if (i .eq. 0 ) then 
            ax=fld&$coord$
          end if
        end if
      
        ; Create plot
        res@xyLineColor = colornames(i)
        res@xyExplicitLegendLabels = tab_labels(i)
        
        if (i .eq. 0) then 
          res@pmLegendParallelPosF   = 0.15 ;xvalue(0) 
          res@pmLegendOrthogonalPosF = -0.1 ;yvalue(0)      ; move up slightly 

          if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
            if (ax@positive .eq. "down") then 
              res@trYReverse = True ; reverse Y-axis
            end if
            if logp then 
              res@xyYStyle = "Log" 
              set_pres_hgt_axes(ax,res,True)
            end if
            plot = gsn_csm_xy(wks,ndtooned(fld),ax,res)
          else
            plot = gsn_csm_xy(wks,ax,ndtooned(fld),res)
          end if

        else
          res@pmLegendParallelPosF   = 0.15+0.35*(tointeger(i/4.)) ;xvalue(tointeger(i/4.)) 
          res@pmLegendOrthogonalPosF = -0.1+0.1*(mod(i,4.))        ;yvalue(mod(i,4.)) 
          
          if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
            if (ax@positive .eq. "down") then 
              res@trYReverse = True ; reverse Y-axis
            end if
            if logp then 
              res@xyYStyle = "Log" 
              set_pres_hgt_axes(ax,res,True)
            end if
            over = gsn_csm_xy(wks,ndtooned(fld),ax,res)
          else
            over = gsn_csm_xy(wks,ax,ndtooned(fld),res)
          end if

          ;---Overlay one plot on the other
          overlay(plot,over)
        end if ; condition 'if' on files
       
      end if 
    end do ; loop on dimensions

    if .not. found then 
      print("There is no non-sigleton dim for file "+ffile)
      status_exit(1)
    end if 
    
  end do ; loop on files  

  draw(plot) ; This will draw all n plots
  frame(wks)

end



