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
  
  ;-----------------
  ; Main field: fld
  ;-----------------

  ; Reading the main field and its unit, setting REDU, and scaling the field
  if isfilepresent(infile) then
    ffile=addfile(infile,"r")
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
  else
    print("File "+infile+" cannot be accessed")
    status_exit(2)
  end if

  if (.not. isvar("units")) then 
    if (isatt(fld,"units")) then units=fld@units else units="None" end if
  end if
  
  logp=True ; by default, vertical cross-sections (and profiles) in pressure coordinates will have a logarithmic scale

  if (isvar("linp")) then if ((linp .eq. 1) .or. (linp .eq. -1)) then logp=False end if end if
  ;if (.not. isvar("contours")) then contours=0 end if
  ;LINEON=False
  ;if (contours .ne. 0 ) then LINEON=True 
  ;end if
  print(isvar("contours"))
  print("test")
  ;print(contours)
  
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
    print("This script is not tuned for high rank data for main field ( rank="+rank+")")
    print(Var_DimNames)
    status_exit(1)
  end if
  
  ; Removes singleton (degenerate) dimensions from fld while preserving meta data
  new_fld=rm_single_dims(fld)

  ;do dim=0,rank-1 
  ;  if isatt(new_fld,Var_DimNames(dim)) then
  ;    print(Var_DimNames(dim))
  ;  end if
  ;end do
  delete(Var_DimNames)
  Var_DimNames = getVarDimNames(new_fld)
  delete(dime)
  dime=dimsizes(new_fld)
  delete(rank)
  rank=dimsizes(dime)
  delete(fld)
  fld=new_fld
  delete(new_fld)
  
  if (rank .eq. 4) then
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
    print("plotting a field with 2 horizontal dimensions")
    fldtmp=fld(0,:,:)
    delete(fld)
    fld=fldtmp
    delete(fldtmp)
    horizontal=True
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

    if ( isatt(fld,"coordinates") .and. (.not. ismissing(str_match(fld@coordinates,"lon"))) .and. (.not. ismissing(str_match(fld@coordinates,"lat"))) ) .or. ( (.not. ismissing(str_match(Var_DimNames(0),"lat"))) .and. (.not. ismissing(str_match(Var_DimNames(1),"lon"))) ) .or. ( isatt(fld&$Var_DimNames(0)$,"standard_name") .and. (fld&$Var_DimNames(0)$@standard_name .eq. "latitude") .and. isatt(fld&$Var_DimNames(1)$,"standard_name") .and. (fld&$Var_DimNames(1)$@standard_name .eq. "longitude")  ) .or. ( isatt(fld&$Var_DimNames(0)$,"axis") .and. (fld&$Var_DimNames(0)$@axis .eq. "y") .and. isatt(fld&$Var_DimNames(1)$,"axis") .and. (fld&$Var_DimNames(0)$@axis .eq. "x") ) then
      horizontal=True 
    end if
        
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

  if (rank .eq. 1) then 
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
    ;hdim=fld&$Var_DimNames[0]$ ; ancienne version pb
    ;new
    ;dim=Var_DimNames(0)
    ;hdim=fld&$dim$
    hdim=fld&$Var_DimNames(0)$
    vprofile=False
    useXY=True
    if ( ismissing(str_match(Var_DimNames(0),"lat")) .and. ismissing(str_match(Var_DimNames(0),"lon")) ) then
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
    
  ;-----------------------
  ; Auxiliary field: fld2
  ;-----------------------
  ;tester la presence du champ auxiliaire et ne faire que ceux qui suit sil y en a un
  ;if (aux_field) then 
  ; Reading the auxiliary field 
  if isfilepresent(infile2) then
    ffile2=addfile(infile2,"r")
    if isfilevar(ffile2,var2) then 
      if (getfilevartypes(ffile2,var2) .eq. "short") then
        fld2 = short2flt( ffile2->$var2$ )
      else
        fld2 = ffile2->$var2$
      end if
    else
      print("File "+infile2+" does not include variable "+var2)
      status_exit(1)
    end if
  else
    print("File "+infile2+" cannot be accessed")
    status_exit(2)
  end if
  
  ; Try to adapt to various cases, using heuristics !
  ; Assume dimensions order is anyway t,z,y,x, but that some may be missing
  
  Var_DimNames2 = getVarDimNames(fld2)  ; getting dimensions from metadata
  dime2=dimsizes(fld2)
  rank2=dimsizes(dime2)
  if (rank2.gt.4) then 
    print("This script is not tuned for high rank data for auxiliary field ( rank="+rank2+")")
    print(Var_DimNames2)
    status_exit(1)
  end if
  
  ; Removes singleton (degenerate) dimensions from fld2 while preserving meta data
  new_fld2=rm_single_dims(fld2)
  delete(Var_DimNames2) 
  Var_DimNames2 = getVarDimNames(new_fld2) 
  delete(dime2) 
  dime2=dimsizes(new_fld2)
  delete(rank2) 
  rank2=dimsizes(dime2)
  delete(fld2)
  fld2=new_fld2
  delete(new_fld2)
  
  if (rank2 .eq. 4) then
    ; assume first dimension is time. Select first time slice before further processing
    ;print("Selecting first time step for auxiliary field")
    fldtmp2=fld2(0,:,:,:)
    delete(fld2)
    fld2=fldtmp2
    delete(fldtmp2)
    delete(Var_DimNames2)
    Var_DimNames2 = getVarDimNames(fld2) 
    delete(dime2)
    dime2=dimsizes(fld2)
    rank2=dimsizes(dime2)
  end if
  
  if (rank2 .eq. 3) then
    print("plotting an auxiliary field with 2 horizontal dimensions")
    fldtmp2=fld2(0,:,:)
    delete(fld2)
    fld2=fldtmp2
    delete(fldtmp2)
    ;delete(dime2)
    ;dime2=dimsizes(fld2)
    ;rank2=dimsizes(dime2)
  end if ; rk eq 3  
     
  ; fld2 is now 2D, with one or two horizontal dimension(s). Last dim is assumed to be horizontal
  ;utile ???
  ;if (rank2 .eq. 2) then 
  ;  ; We have a true cross-section or a horizontal map                   
  ;  delete(Var_DimNames2)
  ;  Var_DimNames2 = getVarDimNames(fld2)
  ;end if
  
  if (rank2 .eq. 1) then 
    delete(Var_DimNames2)
    Var_DimNames2 = getVarDimNames(fld2)  ; getting dimensions from metadata
    hdim2=fld2&$Var_DimNames2(0)$
  end if

  ;-----------------
  ; Open workstation
  ;-----------------

  if type.eq."png" then
    type@wkWidth= 900
    type@wkHeight=900 
  end if

  wks = gsn_open_wks(type,plotname)
  
  gsn_define_colormap(wks,cmap) 
  i = NhlNewColor(wks,0.8,0.8,0.8)
  
  ; main field resources
  res=True
  res@gsnFrame= False
  res@gsnDraw= False

  res@gsnMaximize = True
  ; preferable pour plot en domaine limite :
  res@gsnLeftString     = ""
  ;res@gsnRightString    = ""
  ;res@gsnCenterString   = ""

  ; auxiliary field resources
  ;if (aux_field) then
  res2=True
  OVER=True
  res2@gsnFrame= False
  res2@gsnDraw=False

  ;if (.not. OVER) then
  ;  res2@gsnFrame= True
  ;  res2@gsnDraw= True
  ;end if
  res2@gsnMaximize = True
  res2@gsnLeftString = ""

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
    ;tmp
    ;if (LINEON) then 
    ;  res@cnLinesOn=True
    ;  res@gsnContourNegLineDashPattern = 1
    ;  res@gsnContourZeroLineThicknessF = 1.5  
    ;end if   
    if (LABELON) then 
      res@cnLineLabelsOn=True
    end if   
    if (RASTER) then
      ;tmp;
      ;if (.not. LINEON) then 
      ;  res@cnLinesOn=False
      ;  res@cnLineLabelsOn=False
      ;end if
      res@cnRasterModeOn=True
    end if

    if (horizontal) then ;add only map
      res@mpFillColors = (/-1,-1,-1,-1/)
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
    end if ;end horizontal

    res@lbLabelBarOn = True
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

    ; auxiliary field
    ;if (aux_field) then
    res2@gsnLeftString     = ""
    res2@gsnRightString    = ""
    res2@gsnCenterString   = ""
    
    res2@cnFillOn=False
    res2@cnLinesOn=True
    res2@cnLineLabelsOn = False

    res2@cnInfoLabelString = ""

    ;add
    res2@gsnContourNegLineDashPattern = 1
    res2@gsnContourZeroLineThicknessF = 1.5  

    if ( isvar("contours") ) then ;: bug
    ;if (LINEON) then
      print(contours)
      res2@cnLevelSelectionMode = "ExplicitLevels"
      res2@cnLevels=tofloat(str_split(contours," "))
      delete(contours)
    else
      
      
    end if 
    ;end if (aux_field) 
                                
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
  res@vpWidthF  =0.8
  res@vpHeightF = 0.8

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  if (.not. isvar("title")) then title=var end if

  res@tiMainString       = title
  res@vpXF      =0.1
  res@vpYF      =0.96

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
    ; auxiliary field
    ;if (aux_field) then
    xyres2 = True
    xyres2@gsnDraw = False
    xyres2@gsnFrame = False
    ;
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
      ;if (aux_field) then
      plot1=gsn_csm_xy(wks,fld2,hdim2,xyres2)
      ;plot1=gsn_csm_contour(wks,fld2,xyres2)
      ;end if
    else
      plot0=gsn_csm_xy(wks,hdim,fld,xyres)
      ;if (aux_field) then
      ;plot1=gsn_csm_xy(wks,hdim2,fld2,xyres2)
      plot1=gsn_csm_contour(wks,fld2,xyres2)
      ;end if
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
        plot0=gsn_csm_contour_map(wks,fld,res)
        ;if (aux_field) then
        ;plot1=gsn_csm_contour_map(wks,fld2,res2)
        plot1=gsn_csm_contour(wks,fld2,res2)
        ;end if
      else 
        print("using gsn_csm_contour_map_ce")
        plot0=gsn_csm_contour_map_ce(wks,fld,res)
        ;if (aux_field) then
        ;plot1=gsn_csm_contour_map_ce(wks,fld2,res2)
        plot1=gsn_csm_contour(wks,fld2,res2)
        ;end if
      end if 
    else
      if logp then 
        print("using gsn_csm_pres_hgt")
        plot0=gsn_csm_pres_hgt(wks,fld,res)
        ;if (aux_field) then
        ;plot1=gsn_csm_pres_hgt(wks,fld2,res2)
        plot1=gsn_csm_contour(wks,fld2,res2)
        ;end if
      else
        if ((isvar("linp")) .and. (linp .eq. 1)) then          
          print("using gsn_csm_contour; linp=1")
          print(linp)
          ; useless :
          ;res@sfYArray            = zdim
          res@trYReverse        = True ; reverse Y-axis          
          plot0=gsn_csm_contour(wks,fld,res)
          ;if (aux_field) then
          plot1=gsn_csm_contour(wks,fld2,res2)
          ;end if
        else 
          if ((isvar("linp")) .and. (linp .eq. -1)) then  
            print("using gsn_csm_contour; linp=-1")
            print(linp)
            res@trYReverse        = True ; reverse Y-axis
            ;res@gsnYAxisIrregular2Log = False
            res@gsnYAxisIrregular2Linear= True
            plot0=gsn_csm_contour(wks,fld,res)
            ;res2@trYReverse        = True ; reverse Y-axis
            res2@gsnYAxisIrregular2Linear= True
            plot1=gsn_csm_contour(wks,fld2,res2)
          end if
        end if

      end if 
    end if
    
  end if

  ;if (aux_field) then
  ;if (OVER) then
  overlay(plot0,plot1)      
  draw(plot0)
  frame(wks)
  ;end

  ;else
  ;draw(plot0)
  ;end if

  ;frame(wks)
  status_exit(0)
  
end