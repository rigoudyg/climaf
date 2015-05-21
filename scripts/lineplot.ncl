; Plotting any series of data vectors from A SERIES of NetCDF file, 
; for the same variable (indicated by arg "var")

; Check on first file that only one dimension is not a singleton.

; Do not assume that all datasets have the same dimensions set

; But assume that all data vectors have the same size and coordinate
;   array (take the first one as ref.)

; Usage:
;;;;;;;;;;
; ncl lineplot.ncl infile=.. plotname=.. var=.. title=.. labels=.. colors=.. thickness=.. linp=1

; infile, plotname and var are mandatory
; infile : a string holding the series of filenames, separated by whitespaces
; colors : a string holding a series of color NCL names, separated by whitespaces
; thickness : the common thickness (defaults to 2.0)
; If argument linp=1 and data is a vertical profile, do not plot it in log(p) 

; First version : S.Sénési - may 2015

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
  files=str_split(infile," ")
  n=dimsizes(files)
  if .not. all(isfilepresent(files)) then
    print("Some file cannot be accessed")
    status_exit(2)
  end if
  ;
  do i=0, n-1 

    ; Read variable
    ffile=addfile(files(i),"r")
    if isfilevar(ffile,var) then 
      fld = ffile->$var$
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
          print("There is more than one non-singleton dim for file "+f+ " :"+coord+ Var_DimNames(dim))
          status_exit(1)
        end if 
        found=True
        ; if processing first line/file : allocate multi-line array, and store coordinate array in 'ax'
        if (i .eq. 0 ) then 
          vec=new((/n,dime(dim)/),float)
          coord=Var_DimNames(dim)
          ax=fld&$coord$
        end if
        printVarSummary(fld)
        printVarSummary(ndtooned(fld))
        printVarSummary(vec)
        vec(i,:)=ndtooned(fld)
      end if
    end do ; loop on dimensions

    if .not. found then 
      print("There is no non-sigleton dim for file "+f)
      status_exit(1)
    end if 

  end do ; loop on files

  res=True
  if isvar("thickness") then 
    res@xyLineThicknessF       = thickness 
  else
    res@xyLineThicknessF       = 2.0      ; default is 1
  end if
  res@xyMonoDashPattern      = True     ; force all solid lines
  
  colornames=new(n, string)
  stdcolors=(/"black","red","blue","yellow","green","orange","purple","violet","grey"/)
  do i=0,n-1 colornames(i)=stdcolors(i) end do
  if isvar("colors") then 
    tab=str_split(colors," ")
    do i=0,dimsizes(tab)-1 
      colornames(i)=tab(i) 
    end do
  end if 
  res@xyLineColors=colornames
  
  if .not. isvar("title") then title="title" end if
  res@tiMainString     = title                    ; add title
  
;---Resources for legend
  res@pmLegendDisplayMode    = "Always"              ; turn on legend
  res@pmLegendWidthF         = 0.12                  ; Change width and
  res@pmLegendHeightF        = 0.15                  ; height of legend.
  ;res@pmLegendOrthogonalPosF = -0.08                 ; move up slightly 
  res@lgLabelFontHeightF     = .011                  ; change font height
  res@lgPerimOn              = True                 ; no box around
  ;res@lgItemOrder            = (/1,0/)               ; reverse legend
  if ( isvar("labels")) then 
    res@xyExplicitLegendLabels=str_split(labels,"$")
  end if

  logp=True
  if (isvar("linp")) then if linp .eq. 1 then logp=False end if end if

  res@vpWidthF    = 0.7        ; Make plots wider
  res@vpHeightF   = 0.5

  ; Just plot
  wks   = gsn_open_wks ("png",plotname)             ; open workstation
  ;
  if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
    if (ax@positive .eq. "down") then 
      res@trYReverse = True ; reverse Y-axis
    end if
    if logp then 
      res@xyYStyle = "Log" 
      set_pres_hgt_axes(ax,res,True)
    end if
    plot = gsn_csm_xy(wks,vec,ax,res)
  else
    plot = gsn_csm_xy (wks,ax,vec,res) ; create plot
  end if
end
