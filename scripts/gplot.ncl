; General-purpose plot using NCL, for use in CliMAF. 
; Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/gplot.html

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

;--------------------------------------------------------------------------------------------
undef("data_select")
; Select value 'arg' of optional argument 'arg_name' for dimension 'dim_field_name' of 'field'
function data_select(arg_name:string, arg:numeric, field:numeric, dim_field_name:string)

local VarDimNames, dim, rk, index
begin
  
  VarDimNames = getVarDimNames(field)  ; getting dimensions from metadata
  dim=dimsizes(field)
  rk=dimsizes(dim)

  if isint(arg) then
    print("Selecting index "+arg+" for "+arg_name+" step, i.e. "+arg_name+" = "+field&$dim_field_name$(arg))
    
    if rk .eq. 4 then
      new_fld=field(arg,:,:,:)     
    else 
      if rk .eq. 3 then
        new_fld=field(arg,:,:)
      else 
        if rk .eq. 2 then
          new_fld=field(arg,:)
        end if ;rk eq 2
      end if ; rk eq 3
    end if ; rk eq 4
    
  else
    if isfloat(arg) then 
      ; To convert date to a UT-referenced date => 'time' would be given in the format 'YYYYMM.': to be continued.  
      ;utc_time=cd_calendar(field&$Var_DimNames(0)$,1)
      ;index=closest_val(time,utc_time)
      ;print("Selecting time closed to "+time+", i.e. time = "+utc_time(index))
      index=closest_val(arg,field&$dim_field_name$)
      print("Selecting "+arg_name+" closed to "+arg+", i.e. "+arg_name+" = "+field&$dim_field_name$(index))
      
      if rk .eq. 4 then
        new_fld=field(index,:,:,:)     
      else 
        if rk .eq. 3 then
          new_fld=field(index,:,:)
        else 
          if rk .eq. 2 then
            new_fld=field(index,:)
          end if ;rk eq 2
        end if ; rk eq 3
      end if ; rk eq 4
      
    end if ;arg is float
  end if ;arg is integer
  
  return(new_fld)

end

;--------------------------------------------------------------------------------------------

undef("field_reduce")
; Reduce rank of field called 'varname' in file 'filename' by adapting to various cases, output field is 2D or 1D
function field_reduce(filename:string, varname:string, logp:logical, useXY:logical, horizontal:logical, useLatDim:logical, vprofile:logical)

local ffile, field, Var_DimNames, dime, rank, new_field, fldtmp, index, hor_dim, lat_dim, lon_dim
begin
  
  ; Reading the field 
  if isfilepresent(filename) then
    ffile=addfile(filename,"r")
    if isfilevar(ffile,varname) then 
      if (getfilevartypes(ffile,varname) .eq. "short") then
        field = short2flt( ffile->$varname$ )
      else
        field = ffile->$varname$
      end if
    else
      print("File "+filename+" does not include variable "+varname)
      status_exit(1)
    end if
  else
    print("File "+filename+" cannot be accessed")
    status_exit(2)
  end if

  ; Try to adapt to various cases, using heuristics !
  ; Assume dimensions order is anyway t,z,y,x, but that some may be missing 
  Var_DimNames = getVarDimNames(field)  ; getting dimensions from metadata
  dime=dimsizes(field)
  rank=dimsizes(dime)
  if (rank.gt.4) then 
    print("This script is not tuned for high rank data for field ( rank="+rank+")")
    print(Var_DimNames)
    status_exit(1)
  end if
  
  ; Removes singleton (degenerate) dimensions from field while preserving meta data
  field:=rm_single_dims(field)
  Var_DimNames:=getVarDimNames(field)
  dime:=dimsizes(field)
  rank:=dimsizes(dime)
  
  ; Assume first dimension is time. Select first time slice before further processing
  if (rank .eq. 4) then
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
; NOTE : this should be done only if at least two other dimensions have size > 1, otherwise we
; should plot some Hovmoeller diagram
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ; case where (t,z,y,x) are not degenerated
    if ( (isvar("time")) .and. (.not. ismissing(str_match(Var_DimNames(0),"time"))) ) \
      .or. ( (isvar("time")) .and. iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
      .and. (field&$Var_DimNames(0)$@standard_name .eq. "time") ) then
    
      field:=data_select("time", time, field, Var_DimNames(0))
      
    else
      ; case where no time argument or 'bad' files
      print("Selecting first time step")
      field:=field(0,:,:,:)
    end if

    Var_DimNames:=getVarDimNames(field) 
    dime:=dimsizes(field)
    rank:=dimsizes(dime)
  end if
 
  ; Assume second dimension is depth. Select first level before further processing
  if (rank .eq. 3) then 
    ;print("plotting a field with 2 horizontal dimensions")
    ; case where (t,y,x) or (t,z,y) or (t,z,x) are not degenerated
    if ( (isvar("time")) .and. (.not. ismissing(str_match(Var_DimNames(0),"time"))) ) \
      .or. ( (isvar("time")) .and. iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
      .and. (field&$Var_DimNames(0)$@standard_name .eq. "time") ) then
        
      field:=data_select("time", time, field, Var_DimNames(0))

      ; case where (t,z,y) or (t,z,x) are not degenerated
      if ( (isvar("level")) .and. (.not. ismissing(str_match(Var_DimNames(1),"depth"))) ) \
        .or. ( (isvar("level")) .and. iscoord(field,Var_DimNames(1)) .and. isatt(field&$Var_DimNames(1)$,"axis") \
        .and. (field&$Var_DimNames(1)$@axis .eq. "Z") ) then

        field:=data_select("level", level, field, Var_DimNames(1))
      end if  

    else
      ; case where (z,y,x) are not degenerated
      if ( (isvar("level")) .and. (.not. ismissing(str_match(Var_DimNames(0),"depth"))) ) \
        .or. ( (isvar("level")) .and. iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"axis") \
        .and. (field&$Var_DimNames(0)$@axis .eq. "Z") ) then

        field:=data_select("level", level, field, Var_DimNames(0))
      else
        ; case where no time/level arguments or 'bad' files
        print("Selecting first time or level step")
        field:=field(0,:,:)
      
      end if ; level
    end if ; time

    dime:=dimsizes(field)
    rank:=dimsizes(dime)
  end if ; rk eq 3  

  ; field is now 2D, with one or two horizontal dimension(s). Last dim is assumed to be horizontal
  if (rank .eq. 2) then
    Var_DimNames:=getVarDimNames(field) 

    if ( isatt(field,"coordinates") .and. ( (.not. ismissing(str_match(field@coordinates,"lon"))) .or. (.not. ismissing(str_match(field@coordinates,"LON"))) ) \ 
           .and. ( (.not. ismissing(str_match(field@coordinates,"lat"))) .or. (.not. ismissing(str_match(field@coordinates,"LAT"))) ) ) \ 
      .or. ( (.not. ismissing(str_match(Var_DimNames(0),"lat"))) \ 
           .and. (.not. ismissing(str_match(Var_DimNames(1),"lon"))) ) \
      .or. ( (.not. ismissing(str_match(Var_DimNames(0),"LAT"))) \ 
           .and. (.not. ismissing(str_match(Var_DimNames(1),"LON"))) ) \
      .or. ( iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
           .and. (field&$Var_DimNames(0)$@standard_name .eq. "latitude") \
           .and. iscoord(field,Var_DimNames(1)) .and. isatt(field&$Var_DimNames(1)$,"standard_name") \
           .and. (field&$Var_DimNames(1)$@standard_name .eq. "longitude") ) \
      .or. (  iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"axis") \
           .and. ( (field&$Var_DimNames(0)$@axis .eq. "y") .or. (field&$Var_DimNames(0)$@axis .eq. "Y") ) \
           .and. iscoord(field,Var_DimNames(1)) .and. isatt(field&$Var_DimNames(1)$,"axis") \
           .and. ( (field&$Var_DimNames(1)$@axis .eq. "x") .or. (field&$Var_DimNames(1)$@axis .eq. "X") ) ) then
      horizontal=True 
    end if

    ;We have a true cross-section or a horizontal map
    if logp  then useXY=False end if
    latname="lat"
    lonname="lon"
    if .not. ismissing(str_match(Var_DimNames,"latitude")) then
      latname="latitude"
      lonname="longitude"
    end if
    if .not. ismissing(str_match(Var_DimNames,"LAT")) then
      latname="LAT"
      lonname="LON"
    end if
    if ( (ismissing(str_match(Var_DimNames,"lat"))) .and. ismissing(str_match(Var_DimNames,"LAT")) ) then
      if ( isatt(field,"coordinates") .and. ( (.not. ismissing(str_match(field@coordinates,"lat"))) .or. (.not. ismissing(str_match(field@coordinates,"LAT"))) ) ) \ 
        .or. ( iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
             .and. (field&$Var_DimNames(0)$@standard_name .eq. "latitude") ) \
        .or. (  iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"axis") \
             .and. ( (field&$Var_DimNames(0)$@axis .eq. "y") .or. (field&$Var_DimNames(0)$@axis .eq. "Y") ) ) then
        useLatDim=True
        if isfilevar(ffile,"nav_lat") then 
          latname="nav_lat" 
          lonname="nav_lon"
        end if
      end if
    end if
    lat_dim=ffile->$latname$
    lon_dim=ffile->$lonname$                  
  end if ; rk eq 2

  if (rank .eq. 1) then 
    Var_DimNames:=getVarDimNames(field)  ; getting dimensions from metadata
    hor_dim=field&$Var_DimNames(0)$
    vprofile=False
    useXY=True
    if ( .not. ismissing(str_match(Var_DimNames(0),"depth")) .or. (Var_DimNames(0) .eq. "sigma") \
      .or. (Var_DimNames(0) .eq. "z") .or. (Var_DimNames(0) .eq. "Z") \
      .or. (Var_DimNames(0) .eq. "plev") .or. (Var_DimNames(0) .eq. "lev") .or. (Var_DimNames(0) .eq. "level") \
      .or. (Var_DimNames(0) .eq. "p") .or. (Var_DimNames(0) .eq. "pressure") \
      .or. ( iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"axis") .and. ( (field&$Var_DimNames(0)$@axis .eq. "z") .or. (field&$Var_DimNames(0)$@axis .eq. "Z") ) ) ) then
      print("We have a vertical profile")
      vprofile=True
    end if
  end if

  ; Return depending on rank=1 or rank=2
  if (rank .eq. 1) then 
    return([/field, hor_dim/])
  else ;rk eq 2
    return([/field, lat_dim, lon_dim/])
  end if
  
end

;--------------------------------------------------------------------------------------------


begin

  if (.not. isvar("cmap")) then cmap="BlueDarkRed18" end if
  if (.not. isvar("scale")) then scale=1.0 end if
  if (.not. isvar("offset")) then offset=0.0 end if
  if (.not. isvar("type")) then type="png" end if
  LABELON=False
  RASTER=True 

  ;---------------------------------------------------------
  ; Evaluate number of fields and if drawing vectors or not
  ;---------------------------------------------------------

  AUX_FIELD=False
  if (isvar("aux_file")) then
    if (aux_file .ne. "") then  
      AUX_FIELD=True
    end if
  end if

  VECT=False
  if (isvar("u_file") .and. isvar("v_file")) then  
    if (u_file .ne. "" .and. v_file .ne. "") then
      VECT=True
    end if
  end if
  
  ;-----------------
  ; Main field: fld
  ;-----------------
  
  ; Setting variables depending on optional arguments
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

  print("---------------")
  print("  MAIN FIELD  ")
  print("---------------")

  useXY=False
  horizontal=False
  useLatDim=False
  vprofile=False
  
  ; Reading main field and reduction if necessary
  array=field_reduce(main_file, main_var, logp, useXY, horizontal, useLatDim, vprofile)
  
  fld=array[0]
  if ListCount(array) .eq. 2 then
    hdim=array[1]
  else ; ListCount eq 3
    latdim=array[1]
    londim=array[2]
  end if
  
  ; Reading main field unit, scaling the field and setting REDU
  if (.not. isvar("units")) then 
    if (isatt(fld,"units")) then units=fld@units else units="None" end if
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
    
    print("---------------------")
    print("   AUXILIARY FIELD   ")
    print("---------------------")

    useLatDim2=False
    
    logp_dummy=False
    useXY_dummy=False
    horizontal_dummy=False
    vprofile_dummy=False
  
    ; Reading auxiliary field and reduction if necessary
    array2=field_reduce(aux_file, aux_var, logp_dummy, useXY_dummy, horizontal_dummy, useLatDim2, vprofile_dummy)
  
    fld2=array2[0]
    if ListCount(array2) .eq. 2 then
      hdim2=array2[1]
    else ; ListCount eq 3
      latdim2=array2[1]
      londim2=array2[2]
    end if
  
  end if ; AUX_FIELD is True

  ;-----------------------
  ; Vectors : fld3 & fld4
  ;-----------------------
 
  if VECT then

    print("---------------------")
    print("    VECTOR FIELDS    ")
    print("---------------------")
    ; fld3 <=> u <=> X, fld4 <=> v <=> Y

    print("-----> Vector u ")

    ; Reading vector u and reduction if necessary
    logp_dummy=False
    useXY_dummy=False
    horizontal_dummy=False
    vprofile_dummy=False

    useLatDimv=False
    array3=field_reduce(u_file, u_var, logp_dummy, useXY_dummy, horizontal_dummy, useLatDimv, vprofile_dummy)
  
    fld3=array3[0]
    if ListCount(array3) .eq. 2 then
      print("Rank data for vector u is 1 !!! Vectors fields must have a rank >= 2 !")
      status_exit(1)
    else ; ListCount eq 3
      ;latdimv=array3[1]
      londimv=array3[2]
    end if

    print("-----> Vector v ")
    
    ; Reading vector v and reduction if necessary
    useLatDimv=False
    array4=field_reduce(v_file, v_var, logp_dummy, useXY_dummy, horizontal_dummy, useLatDimv, vprofile_dummy)
  
    fld4=array4[0]
    if ListCount(array4) .eq. 2 then
      print("Rank data for vector v is 1 !!! Vectors fields must have a rank >= 2 !")
      status_exit(1)
    else ; ListCount eq 3
      latdimv=array4[1]
      ;londimv=array4[2]
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
        gcosu:=rm_single_dims(gcosu)
        gsinu:=rm_single_dims(gsinu)
        gcosv:=rm_single_dims(gcosv)
        gsinv:=rm_single_dims(gsinv)
        ; Rotation
        x=fld3
        y=fld4
        fld3 := x * gcosu - y * gsinu
        fld4 := x * gsinv + y * gcosv
      else
        print("File angles.nc cannot be accessed")
        status_exit(2)
      end if
    end if 
      
  end if ; VECT

  ;-----------------
  ; Open workstation
  ;-----------------

  ;if type.eq."png" then
  ;  type@wkWidth= 900
  ;  type@wkHeight=900 
  ;end if

  wks = gsn_open_wks(type,plotname)
  
  gsn_define_colormap(wks,cmap) 
  i = NhlNewColor(wks,0.8,0.8,0.8)
  
  ; main field resources
  res=True
  res@gsnFrame= False
  res@gsnDraw= False
  res@gsnMaximize = True
  res@gsnPaperOrientation="portrait"
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
    if ( isvar("colors") ) then
      res@cnLevelSelectionMode = "ExplicitLevels"
      res@cnLevels=tofloat(str_split(colors," "))
      delete(colors)
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
  if (.not. isvar("title")) then title=main_var end if 

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

  if type .eq. "png" then
    system("convert "+plotname+" -trim "+plotname)
  end if
  
  status_exit(0)
  
end
