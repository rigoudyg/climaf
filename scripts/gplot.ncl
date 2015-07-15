; General-purpose plot using NCL, for use in CliMAF. 
; Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/gplot.html

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin 
  if (.not. isvar("cmap")) then cmap="BlueDarkRed18" end if
  if (.not. isvar("scale")) then scale=1.0 end if
  if (.not. isvar("offset")) then offset=0.0 end if
  ;print("plotting cross section "+plotname+ " from "+infile)
  
  type="png"
  LABELON=False
  RASTER=True 
  
  ; Reading the field and its unit, setting REDU, and scaling the field
  if isfilepresent(infile) then
    ffile=addfile(infile,"r")
    if isfilevar(ffile,var) then fld = ffile->$var$
    else
      print("File "+infile+" does not include variable "+var)
      status_exit(1)
    end if
  else
    print("File "+infile+" cannot be accessed")
    status_exit(2)
  end if
  
  if (.not. isvar("units")) then 
    if ( isatt(fld,"units")) then units=fld@units else units="None" end if
  end if
  
  logp=True ; by default, vertical cross-sections (and profiles) in pressure coordinates will have a logarihtmic scale

  if (isvar("linp")) then if linp .eq. 1 then logp=False end if end if
  if (.not. isvar("contours")) then contours=0 end if
  LINEON=False
  if (contours .ne. 0 ) then LINEON=True 
  end if
  
  if isvar("focus") then
    if ( .not. (focus .eq. "" .or. focus .eq. "land" .or. focus .eq. "ocean")) then
      print("Wrong focus option '"+focus+"' . Only 'ocean' and 'land' are allowed")
      status_exit(2)
    end if
  else
    focus=""
  end if
      

  ; Try to adapt to various cases, using heuristics !
  ; Assume dimensions order is anyway t,z,y,x, but that some may be missing

  Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
  dime=dimsizes(fld)
  rank=dimsizes(dime)
  if (rank.gt.4) then 
    print("This script is not tuned for high rank data ( rank="+rank+")")
    print(Var_DimNames)
    status_exit(1)
  end if

  if (rank.eq.4) then
    ; assume first dimension is time. Select first time slice before further processing
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
; NOTE : this should be done only if at least two other dimensions have size > 1, otherwise we
; should plot some Hovmoeller diagram
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
  horizontal=False  
  if (rank .eq. 3) then
    ; Must identify which horizontal dimension(s) is/are degenerated
    zname   = Var_DimNames(0)
    latname = Var_DimNames(1)
    lonname = Var_DimNames(2)
    zdim=fld&$zname$
    if (dime(1) .eq. 1) then 
      ;print("We are plotting height-longitude")
      ;print("Selecting sole latitude")
      fldtmp=fld(:,0,:)
      delete(fld)
      fld=fldtmp
      delete(fldtmp)
      hdim=fld&$lonname$
    else ; dim1 ne 1
      if (dime(2) .eq. 1) then 
        print("We are plotting height-latitude")
        ;print("Selecting sole longitude")
        fldtmp=fld(:,:,0)
        delete(fld)
        fld=fldtmp
        delete(fldtmp)
        hdim= fld&$latname$
      else
        print("plotting a field with 2 horizontal dimensions")
        ;print(dime)
        ;status_exit(1)
        fldtmp=fld(0,:,:)
        delete(fld)
        fld=fldtmp
        delete(fldtmp)
        horizontal=True
      end if ; dim2 vs 1
    end if ; dim1 vs 1 
    delete(dime)
    dime=dimsizes(fld)
    rank=dimsizes(dime)
  end if ; rk eq 3

  ; fld is now 2D , with one or two horizontal dimension(s). Last dim is assumed to be horizontal
  useLatDim=False
  useLonDim=False

  if (rank .eq. 2) then
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(fld) 
    if (isatt(fld,"coordinates") .and. (.not. ismissing(str_match(fld@coordinates,"lon"))) .and. (.not. ismissing(str_match(fld@coordinates,"lat"))) ) then
      horizontal=True
    end if
    ;if (isatt(fld!0,"axis") .and. ismissing(str_match(fld!0@axis,"Z")))
    ;  horizontal=True
    ;end if
    ; analyze if last (horizontal) dimension is singleton
    if (dime(1).eq. 1) then
      ; We have a profile (either vertical or horizontal)
      useXY=True
      if (.not. horizontal) then 
        vprofile=True
      end if
      dim=Var_DimNames(0)
      delete(hdim)
      hdim=fld&$dim$
      fldtmp=fld(:,0)
      delete(fld)
      fld=fldtmp
      delete(fldtmp)
    else 
      ; analyze if first dimension (either vertical or first horizontal) is singleton
      if (dime(0).eq. 1) then
        ; We have a curve y=f(longitude) or f(latitude)
        useXY=True
        if (.not. horizontal) then 
          vprofile=True
        end if
        vprofile=False
        delete(hdim)
        hdim=fld&$Var_DimNames(1)$
        fldtmp=fld(0,:)
        delete(fld)
        fld=fldtmp
        delete(fldtmp)
      else
        ;We have a true cross-section or a horizontal map
        if logp  then useXY=False end if
        latname="lat"
        if .not. ismissing(str_match(Var_DimNames,"latitude"))
          latname="latitude"
        end if
        if (ismissing(str_match(Var_DimNames,"lat"))) then
          if isatt(fld,"coordinates") .and. (.not. ismissing(str_match(fld@coordinates,"lat"))) then
            useLatDim=True
            if isfilevar(ffile,"nav_lat") then latname="nav_lat" end if
          end if
        end if
        latdim=ffile->$latname$
        ;
        lonname="lon"
        if .not. ismissing(str_match(Var_DimNames,"longitude"))
          lonname="longitude"
        end if
        if (ismissing(str_match(Var_DimNames,"lon"))) then 
          if isatt(fld,"coordinates") .and. (.not. ismissing(str_match(fld@coordinates,"lon"))) then
            useLonDim=True
            if isfilevar(ffile,"nav_lat") then lonname="nav_lon" end if
          end if
        end if
        londim=ffile->$lonname$
      end if
    end if
  end if

  if (rank .eq. 1 ) then 
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
    hdim=fld&$Var_DimNames[0]$
    vprofile=False
    useXY=True
    if ((str_match(dim,"lat") .eq. "missing") .and. (str_match(dim,"lon") .eq. "missing")) then
      print("We have a vertical profile")
      vprofile=True
    end if
  end if
    

  units=units
  fld=fld*tofloat(scale)+tofloat(offset)
  
  controlMinMax= isvar("vmin") .and. isvar("vmax") .and. isvar("vdelta")
  if ( controlMinMax ) then      
    power10=floattoint(log10(dim_max(ndtooned(fld))))
    if power10.ge.4 then
      fld=fld/10^power10
      vmin=tofloat(vmin/10^power10)
      vmax=tofloat(vmax/10^power10)
      vdelta=tofloat(vdelta/10^power10)
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
  res@gsnLeftString     = ""
  ;res@gsnRightString    = ""
  ;res@gsnCenterString   = ""

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ContourPlot resources
  if (.not. useXY  ) then 
    res@gsnSpreadColors     = True
    res@gsnSpreadColorEnd   = -2
    res@gsnLeftString     = ""
    res@gsnRightString    = ""
    res@gsnCenterString   = ""

    res@cnFillOn=True 
    if (controlMinMax) then 
      res@cnLevelSelectionMode = "ManualLevels" 
      res@cnMinLevelValF = vmin
      res@cnMaxLevelValF = vmax
      res@cnLevelSpacingF = vdelta
    end if
    if ( isvar("levels") ) then
        res@cnLevelSelectionMode = "ExplicitLevels"
        res@cnLevels=tofloat(str_split(levels," "))
        delete(levels)
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
      if (.not. LINEON) then 
        res@cnLinesOn=False
        res@cnLineLabelsOn=False
      end if
      res@cnRasterModeOn=True
    end if

    res@mpFillColors    = (/-1,-1,-1,-1/)
    res@mpPerimOn = False
    res@mpGeophysicalLineThicknessF = 2
    res@mpFillOn=False
    res@mpFillDrawOrder="PostDraw"
    if (focus .eq. "land")  then 
      print("Greying out oceans")
      res@mpFillOn=True
      res@mpLandFillColor=-1
      res@mpInlandWaterFillColor = -1 
      res@mpOceanFillColor="grey" 
    end if
    if (focus .eq. "ocean") then 
      res@mpFillOn=True
      res@mpLandFillColor="grey" 
    end if
    

    if (isvar("proj")) then 
      prj = getSubString( proj,0,1 )
      if ( prj .eq. "NH" .or. prj .eq. "SH" ) then
        res@gsnPolar=prj
        lenproj = strlen(proj)
        minlat = 50.
        if ( lenproj .ge. 3 ) then minlat = tofloat( getSubString(proj,2,lenproj-1) ) end if
        if ( prj .eq. "SH" ) then
          res@mpMaxLatF=-minlat
          ;delete(res@mpMinLatF)
        end if
        if ( prj .eq. "NH" ) then
          res@mpMinLatF=minlat
          ;delete(res@mpMaxLatF)
        end if 
      end if
    else
      res@mpMinLonF                = min(londim)
      res@mpMaxLonF                = max(londim)
      res@mpMinLatF                = min(latdim)
      res@mpMaxLatF                = max(latdim)
      res@mpCenterLonF=(min(londim)+max(londim))/2
    end if
  
    res@lbLabelBarOn =True
    if power10.ge.4 then
      res@lbTitleString=units+" x10~S~"+sprinti("%0.1i", power10)+""
    else
      res@lbTitleString=units
    end if
  
    res@lbTitleFontHeightF=0.012
    res@lbLabelFontHeightF=0.012
    res@lbLabelFontThicknessF= 3.0
    res@lbTitleFontThicknessF= 3.0
    res@lbLabelAutoStride = True
    res@lbOrientation     = "vertical"

  end if  ; not useXY

  if (.not. isvar("proj")) then 
    res@tmYLLabelFontHeightF = 0.020
    res@tmXBLabelFontHeightF = 0.020
  
    if type.eq."png" then
      res@tmYLLabelFontThicknessF=2.0
      res@tmXBLabelFontThicknessF=2.0
    end if
  end if
  
  res@tiMainFont=22 
  res@tiMainFontHeightF  = .030       
  
  ; Viewport resources
  res@vpWidthF  = 0.8
  res@vpHeightF = 0.8
  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  if (.not. isvar("title")) then title=var end if

  res@tiMainString       = title
  res@vpXF      = 0.1
  res@vpYF      = 0.96

  if useXY then 
    xyres = True
    xyres@vpXF = 0.08
    xyres@vpWidthF = 0.45
    xyres@vpHeightF = 0.45
    xyres@tmXBLabelFontHeightF = 0.008
    xyres@tmYLLabelFontHeightF = 0.008
    xyres@gsnDraw = False
    xyres@gsnFrame = False
    xyres@txFontHeightF = 0.010
    xyres@xyLineThicknesses = 3.0 ;(/ 2.0, 3.0/)
    xyres@xyLineColors = "black" ; (/"red", "black"/)
    if type.eq."png" then
      xyres@tmXBLabelFontThicknessF = 3.0
      xyres@tmYLLabelFontThicknessF = 3.0
      xyres@txFontThicknessF = 3.0
    end if
    if vprofile then
      xyres@trYReverse = True ; reverse Y-axis
      if logp then 
        xyres@xyYStyle = "Log" 
        ;delete(xyres@tmYLMode)
        set_pres_hgt_axes(hdim,xyres,True)
      end if
      plot0=gsn_csm_xy(wks,fld,hdim,xyres)
    else
      plot0=gsn_csm_xy(wks,hdim,fld,xyres)
    end if
  else
    if (horizontal) then 
      res@gsnAddCyclic = False
      if useLatDim then 
        ;res@trGridType          = "TriangularMesh"
        res@sfXArray            = londim
        res@sfYArray            = latdim
        res@gsnAddCyclic        = False
      end if
      if (isvar("proj")) then 
        print("using gsn_csm_contour_map")
        plot0=gsn_csm_contour_map(wks,fld(:,:),res)
      else 
        print("using gsn_csm_contour_map_ce")
        plot0=gsn_csm_contour_map_ce(wks,fld(:,:),res)
      end if 
    else
      if logp then 
        print("using gsn_csm_pres_hgt")
        plot0=gsn_csm_pres_hgt(wks,fld,res)
      else
        print("using gsn_csm_contour")
        ; useless :
        ;res@sfYArray            = zdim
        res@trYReverse        = True ; reverse Y-axis
        plot0=gsn_csm_contour(wks,fld,res)
      end if 
    end if

  end if
  draw(plot0)
  
  frame(wks)
  status_exit(0)
  
end

