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

  ;---------------------------------------------------------
  ; Evaluate number of fields and if drawing vectors or not
  ;---------------------------------------------------------

  AUX_FIELD=False
  if (isvar("infile2")) then  
    AUX_FIELD=True
  end if

  VECT=False
  if (isvar("infile3") .and. isvar("infile4")) then  
    VECT=True
  end if
  
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

  LEVELS_CONTOURS=False ; by default, contours lines (if actived i.e. if LINEON is True) follow color filled contours
  LINEON=False
  if .not. AUX_FIELD then
    if (isvar("contours") .and. (contours .ne. 0)) then LINEON=True end if
  end if

  if isvar("focus") then
    if (.not. (focus .eq. "" .or. focus .eq. "land" .or. focus .eq. "ocean")) then
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
  delete(Var_DimNames)
  Var_DimNames = getVarDimNames(new_fld)
  delete(dime)
  dime=dimsizes(new_fld)
  delete(rank)
  rank=dimsizes(dime)
  delete(fld)
  fld=new_fld
  delete(new_fld)
  
  ; Assume first dimension is time. Select first time slice before further processing
  if (rank .eq. 4) then
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
  
  ; Assume second dimension is depth. Select first level before further processing
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
     
  ; fld is now 2D, with one or two horizontal dimension(s). Last dim is assumed to be horizontal
  useLatDim=False
  useLonDim=False

  if (rank .eq. 2) then
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(fld) 

    if ( isatt(fld,"coordinates") .and. (.not. ismissing(str_match(fld@coordinates,"lon"))) .and. (.not. ismissing(str_match(fld@coordinates,"lat"))) ) \ 
      .or. ( (.not. ismissing(str_match(Var_DimNames(0),"lat"))) \ 
           .and. (.not. ismissing(str_match(Var_DimNames(1),"lon"))) ) \
      .or. ( isatt(fld&$Var_DimNames(0)$,"standard_name") \
           .and. (fld&$Var_DimNames(0)$@standard_name .eq. "latitude") \
           .and. isatt(fld&$Var_DimNames(1)$,"standard_name") \
           .and. (fld&$Var_DimNames(1)$@standard_name .eq. "longitude") ) \
      .or. ( isatt(fld&$Var_DimNames(0)$,"axis") \
           .and. (fld&$Var_DimNames(0)$@axis .eq. "y") \
           .and. isatt(fld&$Var_DimNames(1)$,"axis") \
           .and. (fld&$Var_DimNames(0)$@axis .eq. "x") ) then
      horizontal=True 
    end if
        
    ;We have a true cross-section or a horizontal map
    if logp  then useXY=False end if
    latname="lat"
    lonname="lon"
    if .not. ismissing(str_match(Var_DimNames,"latitude"))
      latname="latitude"
      lonname="longitude"
    end if
    if (ismissing(str_match(Var_DimNames,"lat"))) then
      if isatt(fld,"coordinates") .and. (.not. ismissing(str_match(fld@coordinates,"lat"))) then
        useLatDim=True
        if isfilevar(ffile,"nav_lat") then 
          latname="nav_lat" 
          lonname="nav_lon"
        end if
      end if
    end if
    latdim=ffile->$latname$
    londim=ffile->$lonname$                  
  end if ; rk eq 2

  if (rank .eq. 1) then 
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
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

  if (AUX_FIELD) then

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
  
    ; Assume first dimension is time. Select first time slice before further processing
    if (rank2 .eq. 4) then
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
  
    ; Assume second dimension is depth. Select first level before further processing
    if (rank2 .eq. 3) then
      print("plotting an auxiliary field with 2 horizontal dimensions")
      fldtmp2=fld2(0,:,:)
      delete(fld2)
      fld2=fldtmp2
      delete(fldtmp2)
      delete(dime2)         
      dime2=dimsizes(fld2)  
      rank2=dimsizes(dime2)  
    end if ; rk eq 3  
     
    ; fld2 is now 2D, with one or two horizontal dimension(s). Last dim is assumed to be horizontal  
    useLatDim2=False
    useLonDim2=False
    
    if (rank2 .eq. 2) then  
      delete(Var_DimNames2)
      Var_DimNames2 = getVarDimNames(fld2) 
      
      latname2="lat"
      lonname2="lon"
      if .not. ismissing(str_match(Var_DimNames2,"latitude"))
        latname2="latitude"
        lonname2="longitude"
      end if
      if (ismissing(str_match(Var_DimNames2,"lat"))) then
        if isatt(fld2,"coordinates") .and. (.not. ismissing(str_match(fld2@coordinates,"lat"))) then
          useLatDim2=True
          if isfilevar(ffile2,"nav_lat") then 
            latname2="nav_lat" 
            lonname2="nav_lon" 
          end if
        end if
      end if
      latdim2=ffile2->$latname2$
      londim2=ffile2->$lonname2$  
    end if; rk eq 2  

    if (rank2 .eq. 1) then 
      delete(Var_DimNames2)
      Var_DimNames2 = getVarDimNames(fld2)  ; getting dimensions from metadata
      hdim2=fld2&$Var_DimNames2(0)$
    end if

  end if ; AUX_FIELD is True

  ;-----------------------
  ; Vectors : fld3 & fld4
  ;-----------------------

  if VECT then

    ; Reading vector fields 
    if isfilepresent(infile3) then
      ffile3=addfile(infile3,"r")
      if isfilevar(ffile3,var3) then 
        if (getfilevartypes(ffile3,var3) .eq. "short") then
          fld3 = short2flt( ffile3->$var3$ )
        else
          fld3 = ffile3->$var3$
        end if
      else
        print("File "+infile3+" does not include variable "+var3)
        status_exit(1)
      end if
    else
      print("File "+infile3+" cannot be accessed")
      status_exit(2)
    end if

    if isfilepresent(infile4) then
      ffile4=addfile(infile4,"r")
      if isfilevar(ffile4,var4) then 
        if (getfilevartypes(ffile4,var4) .eq. "short") then
          fld4 = short2flt( ffile4->$var4$ )
        else
          fld4 = ffile4->$var4$
        end if
      else
        print("File "+infile4+" does not include variable "+var4)
        status_exit(1)
      end if
    else
      print("File "+infile4+" cannot be accessed")
      status_exit(2)
    end if

    ; Assume dimensions order is anyway t,z,y,x, but that some may be missing
    Var_DimNames3 = getVarDimNames(fld3)  ; getting dimensions from metadata
    dime3=dimsizes(fld3)
    rank3=dimsizes(dime3)
    
    Var_DimNames4 = getVarDimNames(fld4) 
    dime4=dimsizes(fld4)
    rank4=dimsizes(dime4)
    
    if ((rank3.gt.4) .or. (rank4.gt.4)) then 
      print("This script is not tuned for high rank data for vectors ( ranku="+rank3+", rankv="+rank4+" )")
      print(Var_DimNames3)
      print(Var_DimNames4)
      status_exit(1)
    end if  

    ; Removes singleton (degenerate) dimensions from fld3 and fld4 while preserving meta data
    new_fld3=rm_single_dims(fld3)
    delete(Var_DimNames3) 
    Var_DimNames3 = getVarDimNames(new_fld3) 
    delete(dime3) 
    dime3=dimsizes(new_fld3)
    delete(rank3) 
    rank3=dimsizes(dime3)
    delete(fld3)
    fld3=new_fld3
    delete(new_fld3)

    new_fld4=rm_single_dims(fld4)
    delete(Var_DimNames4) 
    Var_DimNames4 = getVarDimNames(new_fld4) 
    delete(dime4) 
    dime4=dimsizes(new_fld4)
    delete(rank4) 
    rank4=dimsizes(dime4)
    delete(fld4)
    fld4=new_fld4
    delete(new_fld4)
    
    ; Assume first dimension is time. Select first time slice before further processing
    if (rank3 .eq. 4) then
      ;print("Selecting first time step for vector u")
      fldtmp3=fld3(0,:,:,:)
      delete(fld3)
      fld3=fldtmp3
      delete(fldtmp3)
      delete(Var_DimNames3)
      Var_DimNames3 = getVarDimNames(fld3) 
      delete(dime3)
      dime3=dimsizes(fld3)
      rank3=dimsizes(dime3)
    end if
    if (rank4 .eq. 4) then
      ;print("Selecting first time step for vector v")
      fldtmp4=fld4(0,:,:,:)
      delete(fld4)
      fld4=fldtmp4
      delete(fldtmp4)
      delete(Var_DimNames4)
      Var_DimNames4 = getVarDimNames(fld4) 
      delete(dime4)
      dime4=dimsizes(fld4)
      rank4=dimsizes(dime4)
    end if

    ; Assume second dimension is depth. Select first level before further processing
    if (rank3 .eq. 3) then
      fldtmp3=fld3(0,:,:)
      delete(fld3)
      fld3=fldtmp3
      delete(fldtmp3)
    end if 
    if (rank4 .eq. 3) then
      fldtmp4=fld4(0,:,:)
      delete(fld4)
      fld4=fldtmp4
      delete(fldtmp4)
    end if   
     
    ; Rotation des champs de la grille du modele NEMO -> GEO si le fichier des champs d angles est present 
    ; Ex. tests: fld3(:,:)=0.,fld4(:,:)=0.01
    if ( isvar("rotation") .and. (rotation .eq. 1) ) then  
      if isfilepresent("angles.nc") then
        angle_file=addfile("angles.nc","r")
        gcosu=angle_file->GCOSU
        gsinu=angle_file->GSINU
        gsinv=angle_file->GSINV
        gcosv=angle_file->GCOSV
        ; Remove singleton (degenerate) dimensions: (t,y,x) -> (y,x)
        new_gcosu=rm_single_dims(gcosu)
        new_gsinu=rm_single_dims(gsinu)
        new_gcosv=rm_single_dims(gcosv)
        new_gsinv=rm_single_dims(gsinv)
        ; Rotation
        x=fld3
        y=fld4
        fld3= x * new_gcosu - y * new_gsinu
        fld4= x * new_gsinv + y * new_gcosv
      end if
    end if
    
    ; fld3 & fld4 is now 2D ;fld3 <=> u <=> X, fld4 <=> v <=> Y
    useLatDimv=False
    useLonDimv=False
    
    delete(Var_DimNames3)
    Var_DimNames3 = getVarDimNames(fld3) 
    delete(Var_DimNames4)
    Var_DimNames4 = getVarDimNames(fld4) 
    
    latnamev="lat"
    lonnamev="lon"
    if .not. ismissing(str_match(Var_DimNames4,"latitude"))
      latnamev="latitude"
      lonnamev="longitude"
    end if
    if (ismissing(str_match(Var_DimNames4,"lat"))) then
      if isatt(fld4,"coordinates") .and. (.not. ismissing(str_match(fld4@coordinates,"lat"))) then
        useLatDimv=True
        if isfilevar(ffile4,"nav_lat") then 
          latnamev="nav_lat" 
          lonnamev="nav_lon"
        end if
      end if
    end if
    latdimv=ffile4->$latnamev$
    londimv=ffile3->$lonnamev$      
      
  end if ; VECT

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

    if .not. AUX_FIELD then
      if (LINEON) then 
        if (contours .eq. 1) then 
          res@cnLinesOn=True
          res@gsnContourNegLineDashPattern = 1
          res@gsnContourZeroLineThicknessF = 1.5  
        else
          if (isstring(contours)) then
            LEVELS_CONTOURS=True
            res2=True
            res2@gsnFrame= False
            res2@gsnDraw=False
            res2@gsnMaximize = True
            res2@gsnLeftString     = ""
            res2@gsnRightString    = ""
            res2@gsnCenterString   = ""

            res2@cnFillOn=False
            res2@cnLineLabelsOn = False
            res2@cnInfoLabelString = ""

            res2@cnLinesOn=True
            res2@gsnContourNegLineDashPattern = 1
            res2@gsnContourZeroLineThicknessF = 1.5  
            
            res2@cnLevelSelectionMode = "ExplicitLevels"
            res2@cnLevels=tofloat(str_split(contours," "))
            delete(contours)

            if (horizontal) then
              res2@gsnAddCyclic = False
              if useLatDim then
                res2@sfXArray            = londim
                res2@sfYArray            = latdim
                res2@gsnAddCyclic        = False
              end if
            end if

          end if 
        end if
      end if   
    else
      ; auxiliary field
      res2=True
      res2@gsnFrame= False
      res2@gsnDraw=False
      res2@gsnMaximize = True
      
      res2@gsnLeftString     = ""
      res2@gsnRightString    = ""
      res2@gsnCenterString   = ""
      
      res2@cnFillOn=False
      res2@cnLineLabelsOn = False
      res2@cnInfoLabelString = ""
      
      res2@cnLinesOn=True
      res2@gsnContourNegLineDashPattern = 1
      res2@gsnContourZeroLineThicknessF = 1.5  
      
      if ( isvar("contours") ) then 
        res2@cnLevelSelectionMode = "ExplicitLevels"
        res2@cnLevels=tofloat(str_split(contours," "))
        delete(contours)     
      end if 

      if (horizontal) then
        res2@gsnAddCyclic = False
        if useLatDim2 then
          res2@sfXArray            = londim2
          res2@sfYArray            = latdim2
          res2@gsnAddCyclic        = False
        end if
      end if

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

    if (horizontal) then ; only for map
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
        res@mpMinLatF                = min(latdim)
        res@mpMaxLatF                = max(latdim)
        if (isvar("mpCenterLonF")) then 
          res@mpCenterLonF=tofloat(mpCenterLonF)
        else
          res@mpMinLonF                = min(londim)
          res@mpMaxLonF                = max(londim)
          res@mpCenterLonF=(min(londim)+max(londim))/2
        end if

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
                                
    if VECT then 
      if (isvar("vcRefMagnitudeF")) then                ; define vector ref magnitude
        res@vcRefMagnitudeF=tofloat(vcRefMagnitudeF)
      end if
    
      if (isvar("vcRefLengthF")) then         	        ; define size of ref vector
        res@vcRefLengthF=tofloat(vcRefLengthF)
      end if
      
      if (isvar("vcMinDistanceF")) then                 ; define density of vectors
        res@vcMinDistanceF        = tofloat(vcMinDistanceF)
      else
        res@vcMinDistanceF        = 0.017               ; thins arrows near pole
      end if
      
      if (isvar("vcGlyphStyle")) then                   ; style of vectors: "LineArrow" (default), "CurlyVector", ...
        res@vcGlyphStyle          = vcGlyphStyle
      end if
      
      ;res@vcRefAnnoOrthogonalPosF   = -1.0             ; move ref vector  
      res@vcMonoLineArrowColor  =  True                 ; vectors color by magnitude
      if (isvar("vcLineArrowColor")) then               ; change vector color
        res@vcLineArrowColor      =  vcLineArrowColor
      else
        res@vcLineArrowColor      = "white"            
      end if
      
      res@vcLineArrowThicknessF   = 2                   ; change vector thickness
      res@gsnScalarContour=True                         ; contours desired
      res@vcVectorDrawOrder       = "PostDraw"          ; draw vectors last  
      
      if (horizontal) then 
        if useLatDimv then
          res@vfXArray            = londimv
          res@vfYArray            = latdimv
          res@gsnAddCyclic        = False
        end if
      end if
    end if ; VECT
    
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
    xyres@vpXF = 0.5
    xyres@vpWidthF = 0.45
    xyres@vpHeightF = 0.45
    xyres@tmXBLabelFontHeightF = 0.008
    xyres@tmYLLabelFontHeightF = 0.008
    xyres@gsnDraw = False
    xyres@gsnFrame = False
    xyres@txFontHeightF = 0.010
    xyres@xyLineThicknesses = 3.0 ;(/ 2.0, 3.0/)
    xyres@xyLineColors = "black" ; (/"red", "black"/)
    xyres@tiMainString       = title
   
    ; auxiliary field
    if AUX_FIELD then
      xyres2 = True
      xyres2@gsnDraw = False
      xyres2@gsnFrame = False
    end if
    
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
      if AUX_FIELD then
        plot1=gsn_csm_xy(wks,fld2,hdim2,xyres2)
      end if
    else
      plot0=gsn_csm_xy(wks,hdim,fld,xyres)
      if AUX_FIELD then
        plot1=gsn_csm_xy(wks,hdim2,fld2,xyres2)
      end if
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
        if VECT then
          plot0=gsn_csm_vector_scalar_map(wks,fld3,fld4,fld,res)
        else
          plot0=gsn_csm_contour_map(wks,fld,res)
        end if
        
        if .not. AUX_FIELD then
          if(LEVELS_CONTOURS) then
            plot1=gsn_csm_contour(wks,fld,res2)
          end if
        else
          plot1=gsn_csm_contour(wks,fld2,res2)
        end if
        ;if VECT then
        ;  plot2=gsn_csm_vector(wks,fld3,fld4,res)
        ;end if
        
      else 

        print("using gsn_csm_contour_map_ce")
        if VECT then
          plot0=gsn_csm_vector_scalar_map_ce(wks,fld3,fld4,fld,res)
        else
          plot0=gsn_csm_contour_map_ce(wks,fld,res)
        end if

        if .not. AUX_FIELD then
          if(LEVELS_CONTOURS) then
            plot1=gsn_csm_contour(wks,fld,res2)
          end if
        else
          plot1=gsn_csm_contour(wks,fld2,res2)
        end if
        ;if VECT then
        ;  plot2=gsn_csm_vector(wks,fld3,fld4,res)
        ;end if

      end if 
    else
      if logp then 

        print("using gsn_csm_pres_hgt")
        plot0=gsn_csm_pres_hgt(wks,fld,res)
        if .not. AUX_FIELD then
          if(LEVELS_CONTOURS) then
            plot1=gsn_csm_pres_hgt(wks,fld,res2)
          end if
        else
          plot1=gsn_csm_pres_hgt(wks,fld2,res2)
        end if

      else
        if ((isvar("linp")) .and. (linp .eq. 1)) then          

          print("using gsn_csm_contour; linp=1")
          ; useless :
          ;res@sfYArray            = zdim
          res@trYReverse        = True ; reverse Y-axis          
          plot0=gsn_csm_contour(wks,fld,res)
          if .not. AUX_FIELD then
            if(LEVELS_CONTOURS) then
              plot1=gsn_csm_contour(wks,fld,res2)
            end if
          else
            plot1=gsn_csm_contour(wks,fld2,res2)
          end if

        else 
          if ((isvar("linp")) .and. (linp .eq. -1)) then  

            print("using gsn_csm_contour; linp=-1")
            res@trYReverse        = True ; reverse Y-axis
            res@gsnYAxisIrregular2Linear= True
            plot0=gsn_csm_contour(wks,fld,res)
            if .not. AUX_FIELD then
              if(LEVELS_CONTOURS) then
                res2@gsnYAxisIrregular2Linear= True
                plot1=gsn_csm_contour(wks,fld,res2)
              end if
            else              
              res2@gsnYAxisIrregular2Linear= True
              plot1=gsn_csm_contour(wks,fld2,res2)
            end if

          end if
        end if

      end if 
    end if
    
  end if

  if LEVELS_CONTOURS .or. AUX_FIELD then
    overlay(plot0,plot1)   
  end if
  
  ;if VECT then
  ;  overlay(plot0,plot2)  
  ;end if

  draw(plot0)
  
  frame(wks)

  status_exit(0)
  
end