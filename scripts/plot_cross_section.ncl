; Basic cross-section plot using NCL, for use in CliMAF. 
; Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/plotxsec.html

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin 
  if (.not. isvar("cmap")) then      
    cmap="BlueDarkRed18"
  end if
  if (.not. isvar("scale")) then      
    scale=1.0
  end if
  if (.not. isvar("offset")) then      
    offset=0.0
  end if
  ;print("plotting cross section "+plotname+ " from "+infile)
  
  type="png"
  LINEON=False
  LABELON=False
  RASTER=True 
  
                                ; Reading the field and its unit, setting REDU, and scaling the field
  if isfilepresent(infile) then
    ffile=addfile(infile,"r")
    if isfilevar(ffile,var) then 
      fld = ffile->$var$
    else
      print("File "+infile+" does not include variable "+var)
      status_exit(1)
    end if
  else
    print("File "+infile+" cannot be accessed")
    status_exit(2)
  end if
  
  if (.not. isvar("units")) then 
    if ( isatt(fld,"units")) then
      units=fld@units
    else
      units="None"
    end if
  end if
  
  ; Try to adapt to various cases, using heuristics !
  ; Assume dimensions order is anyway t,z,y,x, but that some may be missing

  Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
  dime=dimsizes(fld)
  rank=dimsizes(dime)
  if (rank.gt.4) then 
    print("This script is not tuned for high rank data ("+rank+")")
    print(Var_DimNames)
    status_exit(1)
  end if
  if (rank.eq.4) then
    ; assume first dimension is time. Select first time slice before further processing
    ;print("Selecting first time step")
    fldtmp=fld(0,:,:,:)
    delete(fld)
    fld=fldtmp
    delete(fldtmp)
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(fld) 
    delete(dime)
    dime=dimsizes(fld)
    rank=dimsizes(dime)
  end if
  
  useXY=False

  if (rank .eq. 3) then
    ; Must identify which horizontal dimension(s) is/are degenerated
    zname   = Var_DimNames(0)
    zdim=fld&$zname$
    latname = Var_DimNames(1)
    latdim=fld&$latname$
    lonname = Var_DimNames(2)
    londim=fld&$lonname$
    if (dime(0) .eq. 1) then
      print("This script is not tuned for plotting data with singleton vertical dim")
      print(dime)
      status_exit(1)
    end if
    if (dime(1) .eq. 1) then 
      ; We are plotting height-longitude
      plotlon=True
      ;print("Selecting only latitude")
      fldtmp=fld(:,0,:)
      delete(fld)
      fld=fldtmp
      delete(fldtmp)
      ;fld!1="lat"
      ;fld&lat=latdim
    else ; dim1 ne 1
      if (dime(2) .ne. 1) then 
        useXY=True
        fldtmp=fld(:,:,0)
        delete(fld)
        fld=fldtmp
        delete(fldtmp)
        ;print("This script is not yet tuned for plotting a vertical profile")
        ;print(dime)
        ;status_exit(1)
      else
        ; We are plotting height-latitude
        ;print("Selecting only longitude")
        fldtmp=fld(:,:,0)
        delete(fld)
        fld=fldtmp
        delete(fldtmp)
        ;fld!1="lon"
        ;fld&lon=londim
      end if ; dim2 vs 1
    end if ; dim1 vs 1 
  end if ; rk eq 3

  if (rank .eq. 2) then
    ; Assume data is OK for feeding plot routine directly 
  end if

  units=units
  fld=fld*scale+offset
  
  controlMinMax= isvar("vmin") .and. isvar("vmax") .and. isvar("vdelta")
  if ( controlMinMax ) then      
    power10=floattoint(log10(dim_max(ndtooned(fld))))
    if power10.ge.4 then
      fld=fld/10^power10
      vmin=vmin/10^power10
      vmax=vmax/10^power10
      vdelta=vdelta/10^power10
    end if
  else
    power10=0
  end if

  if type.eq."png" then
    type@wkWidth= 900
    type@wkHeight=900 
  end if

  wks = gsn_open_wks(type,plotname)
  
  gsn_define_colormap(wks,cmap) 
  i = NhlNewColor(wks,0.8,0.8,0.8)
  
  res=True
  res@gsnFrame= False
  res@gsnDraw= False
  res@gsnMaximize = True
  ; preferabel pour plot en domaine limite :
  res@gsnAddCyclic = False
  res@gsnSpreadColors     = True
  res@gsnSpreadColorEnd   = -2
  res@gsnLeftString     = ""
  ;res@gsnRightString    = ""
  ;res@gsnCenterString   = ""

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ContourPlot resources
  res@cnFillOn=True 
  if (controlMinMax) then 
    res@cnLevelSelectionMode = "ManualLevels" 
    res@cnMinLevelValF = vmin
    res@cnMaxLevelValF = vmax
    res@cnLevelSpacingF = vdelta
  end if

  res@cnLinesOn=False
  res@cnLineLabelsOn = False
  res@cnLineLabelBackgroundColor = "white"
  res@cnInfoLabelString =""
  if (LINEON) then 
    res@cnLinesOn=True
    res@gsnContourNegLineDashPattern = 1
    res@gsnContourZeroLineThicknessF = 1.5  
  end if   
  if (LABELON) then 
    res@cnLineLabelsOn=True
  end if   
  if (RASTER) then
    res@cnLinesOn=False
    res@cnLineLabelsOn=False
    res@cnRasterModeOn=True
  end if

  
  res@lbLabelBarOn =True
  if power10.ge.4 then
    res@lbTitleString=units+" x10~S~"+sprinti("%0.1i", power10)+""
  else
    res@lbTitleString=units
  end if
  
  res@lbTitleFontHeightF=0.012
  res@lbLabelFontHeightF=0.012
  res@lbLabelAutoStride = True
  res@lbOrientation     = "vertical"
  
  res@tmYLLabelFontHeightF = 0.020
  res@tmXBLabelFontHeightF = 0.020
  
  if type.eq."png" then
    res@lbTitleFontThicknessF= 3.0
    res@lbLabelFontThicknessF= 3.0
    res@tmYLLabelFontThicknessF=2.0
    res@tmXBLabelFontThicknessF=2.0
  end if
  
  res@tiMainFont=22 
  res@tiMainFontHeightF  = .030       
  
  ; Viewport resources
  res@vpWidthF  = 0.8
  res@vpHeightF = 0.8
  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  if (.not. isvar("title")) then      
    title=var
  end if

  res@tiMainString       = title
  res@vpXF      = 0.1
  res@vpYF      = 0.96

  if useXY then 
    xyres = True
    xyres@vpXF = 0.08
    xyres@vpWidthF = .10
    xyres@vpHeightF = .26
    xyres@tmXBLabelFontHeightF = 0.008
    xyres@tmYLLabelFontHeightF = 0.008
    xyres@gsnDraw = False
    xyres@gsnFrame = False
    xyres@txFontHeightF = 0.010
    xyres@trXReverse = True
    ;xyres@xyLineThicknesses = (/ 2.0, 3.0/)
    ;xyres@xyLineColors = (/"red", "black"/)
    if type.eq."png" then
      xyres@tmXBLabelFontThicknessF = 3.0
      xyres@tmYLLabelFontThicknessF = 3.0
      xyres@txFontThicknessF = 3.0
    end if
    print(zdim)
    print(fld)
    plot0=gsn_csm_xy(wks,zdim,fld,res)

  else

    plot0=gsn_csm_pres_hgt(wks,fld,res)

  end if
  draw(plot0)
  
  frame(wks)
  status_exit(0)
  
end
