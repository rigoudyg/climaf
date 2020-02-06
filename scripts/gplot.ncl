; General-purpose plot using NCL, for use in CliMAF. 
; Usage and interfacing : see CliMAF doc http://climaf.readthedocs.org/en/latest/scripts/curves.html

; Second version : L.Vignon - november 2015

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl" 

;--------------------------------------------------------------------------------------------

undef("str_convert")
; Convert an input string into logical, integer, float, float array or the same string
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

undef("shading")
; Shade contour regions given low and/or high values using patterns
function shading(routname, field:numeric, resname:logical)

begin

  if ( isvar("shade_below") .or. isvar("shade_above") ) then 

    if ( isvar("shade_below") .and. (.not. isvar("shade_above")) ) then 
      resname@gsnShadeLow = 17   
      if isvar("shading_options") then res_list(shading_options, resname) end if
      routname = gsn_contour_shade(routname, shade_below, min(field), resname) 
    else 
      if ( isvar("shade_above") .and. (.not. isvar("shade_below")) ) then 
        resname@gsnShadeHigh = 17
        if isvar("shading_options") then res_list(shading_options, resname) end if
        routname = gsn_contour_shade(routname, max(field), shade_above, resname) 
      else 
        
        if ( shade_above .lt. shade_below ) then
          resname@gsnShadeMid = 17
          if isvar("shading_options") then res_list(shading_options, resname) end if
          routname = gsn_contour_shade(routname, shade_above, shade_below, resname) 
        else
          resname@gsnShadeLow = 17   
          resname@gsnShadeHigh =17
	  if isvar("shading_options") then res_list(shading_options, resname) end if
          routname = gsn_contour_shade(routname, shade_below, shade_above, resname) 
        end if

      end if
    end if 
   
    return(routname)

  end if
  
end

;--------------------------------------------------------------------------------------------

undef("data_select")
; Select value 'arg' of optional argument 'arg_name' for dimension 'dim_field_name' of 'field' 
; and create a list, called 'select_list', of extracted values 
function data_select(arg_name:string, arg, field:numeric, dim_field_name:string, select_list:string)
 
local VarDimNames, dim, rk, k, dim_pos, index, input_arg, utc_fld_time, utc_date, year, month, day, hour, value
begin

  VarDimNames = getVarDimNames(field)  ; getting dimensions from metadata
  dim=dimsizes(field)
  rk=dimsizes(dim)
 
  ; get position of 'dim_field_name' for 'field' 
  do k=0,dimsizes(VarDimNames)-1
    if .not. ismissing(str_match(VarDimNames(k),dim_field_name)) then dim_pos=k end if
  end do

  ; compute index of selected value
  if isint(arg) then
    index=arg

  else
    if isfloat(arg) then 
      index=closest_val(arg,field&$dim_field_name$)

    else
      if isstring(arg) then 
        if arg_name .eq. "date" then   ; 'date' is given in the format 'YYYY','YYYYMM', 'YYYYMMDD' or 'YYYYMMDDHH'   
          input_arg=arg(:)
          ; convert time dimension of 'field' to a UT-referenced date in the format YYYYMMDDHH
          utc_fld_time=cd_calendar(field&$dim_field_name$,3)
       
          ; convert time dimension of 'arg' in the format YYYYMMDDHH
          if strlen(arg) .eq. 4 then     ; input value is in the format 'YYYY' so add 'MMDDHH'
            arg=arg+"010101" 
          else
            if strlen(arg) .eq. 6 then   ; input value is in the format 'YYYYMM' so add 'DDHH' 
              arg=arg+"0101"
            else
              if strlen(arg) .eq. 8 then ; input value is in the format 'YYYYMMDD' so add 'HH' 
                arg=arg+"01"
              else
                if (strlen(arg) .gt. 10) .or. (strlen(arg) .lt. 4) .or. .not. ismissing(str_match(arg,".")) then
                  print("'date' must be given in the format 'YYYY','YYYYMM', 'YYYYMMDD' or 'YYYYMMDDHH'.")
                  status_exit(1) 
                end if
              end if
            end if
          end if 
          
          index=closest_val(tointeger(arg), utc_fld_time)
        end if

      end if ; arg is string
    end if ; arg is float
  end if ; arg is integer

  ; compute of new field with extraction at 'index'
  if rk .eq. 4 then
    if dim_pos .eq. 0 then new_fld=field(index,:,:,:) end if
    if dim_pos .eq. 1 then new_fld=field(:,index,:,:) end if
    if dim_pos .eq. 2 then new_fld=field(:,:,index,:) end if
    if dim_pos .eq. 3 then new_fld=field(:,:,:,index) end if
  else 
    if rk .eq. 3 then
      if dim_pos .eq. 0 then new_fld=field(index,:,:) end if
      if dim_pos .eq. 1 then new_fld=field(:,index,:) end if
      if dim_pos .eq. 2 then new_fld=field(:,:,index) end if
    else 
      if rk .eq. 2 then
        if dim_pos .eq. 0 then new_fld=field(index,:) end if
        if dim_pos .eq. 1 then new_fld=field(:,index) end if
      end if ;rk eq 2
    end if ; rk eq 3
  end if ; rk eq 4
  
  ; to print extracted value
  if (arg_name .eq. "time") .or. (arg_name .eq. "date") then
    
    utc_date=cd_calendar(field&$dim_field_name$(index),0) ; array returned will be of type float 
                                                          ; and dimensioned dimsizes(time)x6
    year  = tointeger(utc_date(:,0))    ; Convert to integer for
    month = tointeger(utc_date(:,1))    ; use sprinti 
    day   = tointeger(utc_date(:,2))
    hour  = tointeger(utc_date(:,3))

    if ( (arg_name .eq. "date") .and. (strlen(input_arg) .eq. 10) ) \
      .or. ( (arg_name .ne. "date") .and. hour .ne. 0 ) then 
      value = sprinti("%0.4i", year) + "/" + sprinti("%0.2i", month) + "/" + sprinti("%0.2i", day) + "-H" + sprinti("%0.2i", hour) 
    else
      value = sprinti("%0.4i", year) + "/" + sprinti("%0.2i", month) + "/" + sprinti("%0.2i", day) 
    end if

  else
    value=field&$dim_field_name$(index)
  end if

  if isint(arg) then
    if arg_name .eq. "time" then
      print("Selecting index "+arg+" for "+arg_name+", i.e. "+arg_name+" = "+field&$dim_field_name$(arg)+" <=> "+value)
    else
      print("Selecting index "+arg+" for "+arg_name+", i.e. "+arg_name+" = "+value)
    end if

  else
    if isfloat(arg) .or. isstring(arg) then 
      if (arg_name .eq. "date") .or. (arg_name .eq. "time") then
        if arg_name .eq. "date" then arg=input_arg end if
        print("Selecting "+arg_name+" close to "+arg+", i.e. "+arg_name+" = "+field&$dim_field_name$(index)+" <=> "+value)
      else
        print("Selecting "+arg_name+" close to "+arg+", i.e. "+arg_name+" = "+value)
      end if
    end if
  end if
  
  select_list=select_list+" "+arg_name+"="+value

  return(new_fld)
  
end

;--------------------------------------------------------------------------------------------

undef("check_zaxis")
; Check if dimension 'k' of 'field' is a vertical axis
function check_zaxis(field:numeric, k:integer)

local vardims
begin
  
  vardims = getVarDimNames(field)  ; getting dimensions from metadata
  zaxis=False

  if ( .not. ismissing(str_match(vardims(k),"dept")) \
    .or. ( .not. ismissing(vardims(k)) .and. ( (vardims(k) .eq. "sigma") \
         .or. (vardims(k) .eq. "z") .or. (vardims(k) .eq. "Z") \
         .or. (vardims(k) .eq. "plev") .or. (vardims(k) .eq. "lev") .or. (vardims(k) .eq. "level") \
         .or. (vardims(k) .eq. "p") .or. (vardims(k) .eq. "pressure") ) ) \
    .or. ( iscoord(field,vardims(k)) .and. isatt(field&$vardims(k)$,"axis") \
         .and. ((field&$vardims(k)$@axis .eq. "z") .or. (field&$vardims(k)$@axis .eq. "Z")) ) \
    .or. ( iscoord(field,vardims(k)) .and. isatt(field&$vardims(k)$,"standard_name") \
         .and. ( .not. ismissing(str_match(field&$vardims(k)$@standard_name,"depth")) \
         .or. .not. ismissing(str_match(field&$vardims(k)$@standard_name,"level")) \
         .or. .not. ismissing(str_match(field&$vardims(k)$@standard_name,"height")) ) ) ) then
    zaxis=True
  end if
 
  delete(vardims)
  return(zaxis)
  
end

;--------------------------------------------------------------------------------------------

undef("check_map")
; Check if 'field' of rank 2 is a map, 'lat_tab' is the latitude array and the latitude variable 
; name is 'lat_name' (same as for 'lon_tab' and 'lon_name')
function check_map(field:numeric, lat_name:string, lon_name:string, lat_tab:numeric, lon_tab:numeric) 

local vardims, zaxis_exist
begin
  
  vardims = getVarDimNames(field)  ; getting dimensions from metadata
  map=False
  
  ; check if one of dimensions is a vertical axis
  zaxis_exist=False
  do k=0,1
    if check_zaxis(field, k) then
      map=False
      zaxis_exist=True
    end if
  end do
              
  ; if any dimension is a vertical axis, we check if we have a map
  if .not. zaxis_exist then
    if ( isatt(field,"coordinates") .and. (.not. ismissing(str_match(field@coordinates,lon_name)))  \ 
         .and. (.not. ismissing(str_match(field@coordinates,lat_name))) \
         .and. ( (isatt(lat_tab,"standard_name") .and. (lat_tab@standard_name .eq. "latitude") \
               .and. isatt(lon_tab,"standard_name") .and. (lon_tab@standard_name .eq. "longitude")) \ 
         .or. ( isatt(lat_tab,"axis") .and. ((lat_tab@axis .eq. "y") .or. (lat_tab@axis .eq. "Y")) \
               .and. isatt(lon_tab,"axis") .and. ((lon_tab@axis .eq. "x") .or. (lon_tab@axis .eq. "X")) ) ) ) \
      .or. ( (.not. ismissing(str_match(vardims(0),lat_name))) \ 
               .and. (.not. ismissing(str_match(vardims(1),lon_name))) ) \
      .or. ( iscoord(field,vardims(0)) .and. isatt(field&$vardims(0)$,"standard_name") \
           .and. (field&$vardims(0)$@standard_name .eq. "latitude") \
           .and. iscoord(field,vardims(1)) .and. isatt(field&$vardims(1)$,"standard_name") \
           .and. (field&$vardims(1)$@standard_name .eq. "longitude") ) \
      .or. (  iscoord(field,vardims(0)) .and. isatt(field&$vardims(0)$,"axis") \
           .and. ( (field&$vardims(0)$@axis .eq. "y") .or. (field&$vardims(0)$@axis .eq. "Y") ) \
           .and. iscoord(field,vardims(1)) .and. isatt(field&$vardims(1)$,"axis") \
           .and. ( (field&$vardims(1)$@axis .eq. "x") .or. (field&$vardims(1)$@axis .eq. "X") ) ) then
      map =True
    end if
  end if

  delete(vardims)
  return(map)

end

;--------------------------------------------------------------------------------------------

undef("field_reduce")
; Reduce rank of field called 'varname' in file 'filename' by adapting to various cases, output field is 2D or 1D
function field_reduce(filename:string, varname:string, ystyle:string, useXY:logical, horizontal:logical, useLatDim:logical, vprofile:logical, extract_list:string, lat_exist:logical, lon_exist:logical, proj_data:logical)

local ffile, field, Var_DimNames, dime, rank, new_field, fldtmp, index, hor_dim, lat_dim, lon_dim, dimnames, latnames, lonnames, latname, lonname, coord_file, grid_file, extract
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
  new_field=rm_single_dims(field)
  delete(Var_DimNames)
  Var_DimNames=getVarDimNames(new_field)
  delete(dime)
  dime=dimsizes(new_field)
  delete(rank)
  rank=dimsizes(dime)
  delete(field)
  field=new_field
  delete(new_field)
  
  ; Assume first dimension is time. Select first time slice before further processing
  if (rank .eq. 4) then
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
; NOTE : this should be done only if at least two other dimensions have size > 1, otherwise we
; should plot some Hovmoeller diagram
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ; case where (t,z,y,x) are not degenerated
    if (isvar("date") .or. isvar("time")) .and. ( (.not. ismissing(str_match(Var_DimNames(0),"time"))) \
      .or. ( iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
      .and. (field&$Var_DimNames(0)$@standard_name .eq. "time") ) ) then
    
      if isvar("date") .and. .not. isvar("time") then
        fldtmp=data_select("date", date, field, Var_DimNames(0), extract_list)
      else
        if isvar("time") .and. .not. isvar("date") then 
          fldtmp=data_select("time", time, field, Var_DimNames(0), extract_list) 
        else
          print("'date' and 'time' are incompatible. You only have to supply one of these arguments.")
          status_exit(1) 
        end if
      end if

      if isvar("level") .and. check_zaxis(field,1) then
        delete(field)
        field=fldtmp
        delete(fldtmp)
        fldtmp=data_select("level", level, field, Var_DimNames(1), extract_list)
      end if

    else
      ; case where no time argument or 'bad' files
      print("Selecting first time step")
      fldtmp=field(0,:,:,:)
    end if

    delete(field)
    field=fldtmp
    delete(fldtmp)
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(field) 
    delete(dime)
    dime=dimsizes(field)
    rank=dimsizes(dime)
  end if
 
  ; Assume second dimension is depth. Select first level before further processing
  if (rank .eq. 3) then 

    ; case where (t,y,x) or (t,z,y) or (t,z,x) are not degenerated
    if (.not. ismissing(str_match(Var_DimNames(0),"time"))) \
      .or. ( iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
      .and. (field&$Var_DimNames(0)$@standard_name .eq. "time") ) then

      if isvar("date") .or. isvar("time") then 

        if isvar("date") .and. .not. isvar("time") then
          fldtmp=data_select("date", date, field, Var_DimNames(0), extract_list) 
        else
          if isvar("time") .and. .not. isvar("date") then 
            fldtmp=data_select("time", time, field, Var_DimNames(0), extract_list) 
          else
            print("'date' and 'time' are incompatible. You only have to supply one of these arguments.")
            status_exit(1) 
          end if
        end if

        ; case where (t,z,y) or (t,z,x) are not degenerated
        if isvar("level") .and. check_zaxis(field,1) then
          delete(field)
          field=fldtmp
          delete(fldtmp)
          fldtmp=data_select("level", level, field, Var_DimNames(1), extract_list)
        end if  

      else
        if isvar("level") .and. check_zaxis(field,1) then
          fldtmp=data_select("level", level, field, Var_DimNames(1), extract_list)
      
        else
          ; case where no time argument or 'bad' files
          print("Selecting first time step")
          fldtmp=field(0,:,:)
        end if
      end if

    else
      ; case where (z,y,x) are not degenerated
      if isvar("level") .and. check_zaxis(field,0) then
        fldtmp=data_select("level", level, field, Var_DimNames(0), extract_list)
      else
        ; case where no level argument or 'bad' files
        print("Selecting first level step")
        fldtmp=field(0,:,:)
      end if ; level

    end if ; time

    delete(field)
    field=fldtmp
    delete(fldtmp)
    delete(Var_DimNames)
    Var_DimNames = getVarDimNames(field) 
    delete(dime)
    dime=dimsizes(field)
    rank=dimsizes(dime)
  end if ; rk eq 3 

  ; field is now 2D, with one or two horizontal dimension(s). Last dim is assumed to be horizontal
  ; We have a true cross-section, a horizontal map or a profile (t,z)
  if (rank .eq. 2) then

    extract=False
    ; cases (t,*) or (z,*) with an extraction in time or level
    if (.not. ismissing(str_match(Var_DimNames(0),"time"))) \
      .or. ( iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
             .and. (field&$Var_DimNames(0)$@standard_name .eq. "time") ) then

      if isvar("date") .or. isvar("time") then
        if isvar("date") .and. .not. isvar("time") then
          fldtmp=data_select("date", date, field, Var_DimNames(0), extract_list) 
        else
          if isvar("time") .and. .not. isvar("date") then
            fldtmp=data_select("time", time, field, Var_DimNames(0), extract_list) 
          else
            print("'date' and 'time' are incompatible. You only have to supply one of these arguments.")
            status_exit(1) 
          end if
        end if
        extract=True

      else
        if isvar("level") .and. check_zaxis(field,1) then
          fldtmp=data_select("level", level, field, Var_DimNames(1), extract_list) 
          extract=True
        end if
      end if        
    
    else
      if isvar("level") .and. check_zaxis(field,0) then 
        fldtmp=data_select("level", level, field, Var_DimNames(0), extract_list)
        extract=True
      end if
    end if

    if extract then
      delete(field)
      field=fldtmp
      delete(fldtmp)
      delete(dime)
      dime=dimsizes(field)
      rank=dimsizes(dime)
    end if
  
    if .not. extract then

      if (ystyle .eq. "log") then useXY=False end if
   
      ; get latitude and/or longitude name
      latnames=(/"lat", "LAT", "latitude", "nav_lat"/)     ; dimnames(0,:)
      lonnames=(/"lon", "LON", "longitude", "nav_lon"/)    ; dimnames(1,:)
      dimnames=(/latnames, lonnames/)

      do k=0,1 
        do i=0, dimsizes(dimnames(k,:))-1
          if ( .not. ismissing(str_match(Var_DimNames,dimnames(k,i))) \
            .or. (isatt(field,"coordinates") .and. .not. ismissing(str_match(field@coordinates,dimnames(k,i)))) ) then
            if (k .eq. 0) then latname=latnames(i) end if
            if (k .eq. 1) then lonname=lonnames(i) end if
          end if
        end do
      end do

      ; for curvilinear grid  
      if isvar("latname") .and. ismissing(str_match(Var_DimNames,latname)) then
        useLatDim=True
      else
        if .not. isvar("latname") then
          if ( iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"standard_name") \
               .and. (field&$Var_DimNames(0)$@standard_name .eq. "latitude") ) \
             .or. (  iscoord(field,Var_DimNames(0)) .and. isatt(field&$Var_DimNames(0)$,"axis") \
               .and. ( (field&$Var_DimNames(0)$@axis .eq. "y") .or. (field&$Var_DimNames(0)$@axis .eq. "Y") ) ) then
            useLatDim=True
          end if
        end if
      end if

      if useLatDim then ; curvilinear grid
      
        if isfilevar(ffile,"nav_lat") then
          if (isfilepresent("coordinates.nc") .or. isfilepresent("mesh_mask.nc")) then
            
            if isfilepresent("coordinates.nc") then
              coord_file=addfile("coordinates.nc","r")
              
              if isfilevar(coord_file,"gphit") then 
                lat_dim=coord_file->gphit
                lat_dim_tmp=rm_single_dims(lat_dim)
                delete(lat_dim)
                lat_dim=lat_dim_tmp
                delete(lat_dim_tmp)
                lat_dim@standard_name="latitude"
              end if
              if isfilevar(coord_file,"glamt") then 	
                lon_dim=coord_file->glamt
                lon_dim_tmp=rm_single_dims(lon_dim)
                delete(lon_dim)
                lon_dim=lon_dim_tmp
                delete(lon_dim_tmp)
                lon_dim@standard_name="longitude"
              end if
            else

              if isfilepresent("mesh_mask.nc") then
                coord_file=addfile("mesh_mask.nc","r")
                if isfilevar(ffile,"nav_lat") then lat_dim=coord_file->nav_lat end if
                if isfilevar(ffile,"nav_lon") then lon_dim=coord_file->nav_lon end if
                lat_dim@standard_name="latitude"
                lon_dim@standard_name="longitude"
              end if
          
            end if

          else  ; files 'coordinates.nc' and 'mesh_mask.nc' not present
            print("File coordinates.nc or mesh_mask.nc cannot be accessed. We will use data file values.")
            if isvar("latname") then lat_dim=ffile->$latname$ end if
            if isvar("lonname") then lon_dim=ffile->$lonname$ end if	
          end if
        
        else ; curvilinear grid but not with nav_lat/nav_lon
        
          if ( .not. isvar("proj") .and. isfilepresent("climaf_plot_grid.nc") ) then
            grid_file=addfile("climaf_plot_grid.nc","r")
            if isfilevar(grid_file,"Lambert_Conformal") then 
              proj_data=True ; contains map projection information
              proj_data@projection_type="Lambert_Conformal"
              proj_data@latitude_of_projection_origin=grid_file->Lambert_Conformal@latitude_of_projection_origin
              ;proj_data@standard_parallel=grid_file->Lambert_Conformal@standard_parallel
              proj_data@longitude_of_central_meridian=grid_file->Lambert_Conformal@longitude_of_central_meridian
            end if
          end if
          if isvar("latname") then lat_dim=ffile->$latname$ end if
          if isvar("lonname") then lon_dim=ffile->$lonname$ end if
       
        end if

      else ; it is not a curvilinear grid
        if isvar("latname") then lat_dim=ffile->$latname$ end if
        if isvar("lonname") then lon_dim=ffile->$lonname$ end if	
      end if

      ; correction for data with 'units' attribute equal to "degrees" for latitude and longitude
      if isvar("lat_dim") .and. isatt(lat_dim,"units") .and. (lat_dim@units .eq. "degrees") then
        lat_dim@units = "degrees_north"
        field&$latname$@units = "degrees_north"
      end if
      if isvar("lon_dim") .and. isatt(lon_dim,"units") .and. (lon_dim@units .eq. "degrees") then
        lon_dim@units = "degrees_east"
        field&$lonname$@units = "degrees_east"
      end if

      ; check if we have a horizontal map
      if isvar("latname") .and. isvar("lonname") then 
        horizontal=check_map(field, latname, lonname, lat_dim, lon_dim) 
      else
        horizontal=False
      end if
    
    end if ; extract is False
  end if ; rk eq 2

  if (rank .eq. 1) then 
    delete(Var_DimNames)
    Var_DimNames=getVarDimNames(field)  ; getting dimensions from metadata
    hor_dim=field&$Var_DimNames(0)$
    vprofile=False
    useXY=True
    if check_zaxis(field,0) then
      print("We have a vertical profile")
      vprofile=True
    end if
  end if

  lat_exist=True
  lon_exist=True
  ; Return depending on rank=1 or rank=2 (and depend on existence of lat and lon variables)
  if (rank .eq. 1) then 
    return([/field, hor_dim/])
  else ;rk eq 2
    if isvar("lon_dim") .and. isvar("lat_dim") then  return([/field, lat_dim, lon_dim, proj_data/]) end if
    if isvar("lon_dim") .and. .not. isvar("lat_dim") then  
       lat_exist=False
       return([/field, lon_dim, proj_data/]) 
    end if
    if .not. isvar("lon_dim") .and. isvar("lat_dim") then  
       lon_exist=False
       return([/field, lat_dim, proj_data/]) 
    end if	 
    if .not. isvar("lon_dim") .and. .not. isvar("lat_dim") then  
      lat_exist=False
      lon_exist=False
      return([/field, proj_data/])
    end if
  end if
  
end

;--------------------------------------------------------------------------------------------

undef("field_transpose")
; Transpose 'field' of rank 2
function field_transpose(field:numeric)

local VarDim, tr_fld
begin
  
  VarDim=getVarDimNames(field) 
  if .not. any(ismissing(VarDim)) then  
    tr_fld=field($VarDim(1)$|:,$VarDim(0)$|:)
  else
    print("Field contains missing dimension names for the given variable " \
    + "so 'invXY' will not invert X and Y axis")
    tr_fld=field
  end if
  delete(VarDim)  
  return(tr_fld)
  
end  

;--------------------------------------------------------------------------------------------

undef("time_labels")
; If 'field' contains a time dimension, add additional resources to 'fct_res' to produce 
; nicely-formatted time labels on time axis (xaxis or yaxis depend on 'inv_axis'). This 
; function only works if you have a time 'units' recognized by the cd_calendar function.
procedure time_labels(field:numeric, fct_res:logical, inv_axis:logical)

local VarDim, rnk, restick
begin

  VarDim=getVarDimNames(field)
  rnk=dimsizes(dimsizes(field))
 
  do k=0, dimsizes(VarDim)-1
    if ( .not. ismissing(str_match(VarDim(k),"time")) \
      .or. (isatt(field,"coordinates") .and. .not. ismissing(str_match(field@coordinates,"time"))) \
      .or.  ( iscoord(field,VarDim(k)) .and. isatt(field&$VarDim(k)$,"standard_name") \
      .and. (field&$VarDim(k)$@standard_name .eq. "time") )) then
      
      restick=True

      if ( (rnk .eq. 2) .and. .not. inv_axis ) \
        .or. ( (rnk .eq. 1) .and. inv_axis ) then 
        restick@ttmAxis="YL"  ; "XB" by default 
      end if 

      if (isvar("fmt")) then restick@ttmFormat=fmt end if
      time_axis_labels(field&$VarDim(k)$,fct_res,restick)           
    end if
  end do

  return
end

;--------------------------------------------------------------------------------------------

undef("time_position")
; Return position of time dimension for 'field'
function time_position(field:numeric)

local VarDim
begin
  
  VarDim=getVarDimNames(field) 
 
  it=-1
  do k=0, dimsizes(VarDim)-1
    if ( .not. ismissing(str_match(VarDim(k),"time")) \
      .or. (isatt(field,"coordinates") .and. .not. ismissing(str_match(field@coordinates,"time"))) \
      .or.  ( iscoord(field,VarDim(k)) .and. isatt(field&$VarDim(k)$,"standard_name") \
      .and. (field&$VarDim(k)$@standard_name .eq. "time") )) then
      it=it+k+1
    end if
  end do

  delete(VarDim)  
  return(it)

end

;--------------------------------------------------------------------------------------------


begin

  if (.not. isvar("colormap")) then colormap="BlueDarkRed18" end if
  if isvar("colormap") .and. .not. ismissing(str_match(colormap,",")) then 
    colornames=str_split(colormap,",")
    delete(colormap)
    colormap=colornames
    delete(colornames)  
  end if
  
  if (.not. isvar("myscale")) then myscale=1.0 end if
  if (.not. isvar("myoffset")) then myoffset=0.0 end if
  if (.not. isvar("myscale_aux")) then myscale_aux=1.0 end if
  if (.not. isvar("myoffset_aux")) then myoffset_aux=0.0 end if
  if (.not. isvar("type")) then type="png" end if
  if (.not. isvar("trim")) then trim=True end if
  if (.not. isvar("invXY")) then invXY=False end if
  
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

  if isvar("shade2_options") then
    if (.not. ( isvar("shade2_below") .and. isvar("shade2_above")  )) then
      print("Must provide args shade2_below and shade2_above when using arg shade2_options  !")
      status_exit(1) 
    end if
    ;if (.not. isvar("shade2_file") ) then
    ;  print("Must provide a shade2 field when using arg shade2_options !")
    ;  status_exit(1) 
    ;end if
  end if
  if isvar("shade2_file") then
    if (.not. isvar("shade2_options") ) then
      print("Must provide shade2_options when providing a shade2_file !")
      status_exit(1)
    else
      print("---------------------")
      print("   STIPPLING FIELD   ")
      print("---------------------")
      useLatDim2=False
      useXY_dummy=False
      horizontal_dummy=False
      vprofile_dummy=False
      lat_exist2=True  
      lon_exist2=True
      proj_data_dummy=False
      shade2_field_select=""
      array_shade2=field_reduce(shade2_file, shade2_var, "lin", useXY_dummy, horizontal_dummy, \
          useLatDim2, vprofile_dummy, shade2_field_select, lat_exist2, lon_exist2, proj_data_dummy)
      fld_shade2=array_shade2[0]
    end if
  end if
  
  
  ;-----------------
  ; Main field: fld
  ;-----------------
  
  ; Setting variables depending on optional arguments
  if .not. isvar("y") then y="lin" end if ; by default, vertical cross-sections (and profiles) in pressure coordinates will have a data-linear scale

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
  lat_exist=True  
  lon_exist=True
  proj_data=False ; for Lambert projection

  ; Reading main field and reduction if necessary
  main_field_select=""
  array=field_reduce(main_file, main_var, y, useXY, horizontal, useLatDim, vprofile, main_field_select, lat_exist, lon_exist, proj_data)

  fld=array[0]
  if (ListCount(array) .eq. 2) .and. useXY then ; rk eq 1
    hdim=array[1]
  else 
    if (ListCount(array) .ge. 2) then ; ListCount eq 3 or 4 <=> rk eq 2
      if lat_exist .and. lon_exist then 
        latdim=array[1]
        londim=array[2]
        proj_data=array[3]
      end if
      if (lat_exist .and. .not. lon_exist) then 
        latdim=array[1] 
        proj_data=array[2]
      end if
      if (lon_exist .and. .not. lat_exist) then 
        londim=array[1] 
        proj_data=array[2]
      end if
    end if
  end if

  ; Reading main field unit, scaling the field and setting REDU
  if (.not. isvar("units")) then 
    if (isatt(fld,"units")) then units=fld@units else units="None" end if
  end if
  
  units=units 
  tmpfld=fld*tofloat(myscale)+tofloat(myoffset)
  copy_VarMeta(fld,tmpfld)
  delete(fld)
  fld=tmpfld
  delete(tmpfld)

  controlMinMax= isvar("vmin") .and. isvar("vmax") .and. isvar("vdelta")
  if ( controlMinMax ) then      
    power10=floattoint(log10(abs(vmax-vmin)))
    if power10.ge.4 then
      vmin=tofloat(vmin/10^power10)
      vmax=tofloat(vmax/10^power10)
      vdelta=tofloat(vdelta/10^power10)

    end if
  else
    power10=floattoint(log10(dim_max(ndtooned(tofloat(fld)))))
    if ismissing(power10) then 
      print("Field has only missing values" )
      power10=1
    end if
  end if

  
  if power10.ge.4 then
    fld=fld/10^power10
  end if
  
  ;-----------------------
  ; Auxiliary field: fld2
  ;-----------------------

  if (AUX_FIELD) then
    
    print("---------------------")
    print("   AUXILIARY FIELD   ")
    print("---------------------")

    useLatDim2=False
    useXY_dummy=False
    horizontal_dummy=False
    vprofile_dummy=False
    lat_exist2=True  
    lon_exist2=True
    proj_data_dummy=False

    ; Reading auxiliary field and reduction if necessary
    aux_field_select=""
    array2=field_reduce(aux_file, aux_var, y, useXY_dummy, horizontal_dummy, useLatDim2, vprofile_dummy, aux_field_select, lat_exist2, lon_exist2, proj_data_dummy)
 
    fld2=array2[0]
    if (ListCount(array2) .eq. 2) .and. useXY_dummy then
      hdim2=array2[1]
    else 
      if (ListCount(array2) .ge. 2) then ; ListCount eq 3 or 4 <=> rk eq 2
        if lat_exist2 .and. lon_exist2 then	
          latdim2=array2[1]	    
          londim2=array2[2]
        end if
        if (lat_exist2 .and. .not. lon_exist2) then latdim2=array2[1] end if
        if (lon_exist2 .and. .not. lat_exist2) then londim2=array2[1] end if
      end if
    end if

    tmpfld=fld2*tofloat(myscale_aux)+tofloat(myoffset_aux)
    copy_VarMeta(fld2,tmpfld)
    delete(fld2)
    fld2=tmpfld
    delete(tmpfld)
  
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
    useXY_dummy=False
    horizontal_dummy=False
    vprofile_dummy=False
    lat_exist3=True
    lon_exist3=True
    proj_data_dummy=False

    useLatDimv=False
    uselect=""
    array3=field_reduce(u_file, u_var, y, useXY_dummy, horizontal_dummy, useLatDimv, vprofile_dummy, uselect, lat_exist3, lon_exist3, proj_data_dummy)
 
    fld3=array3[0]
    if (ListCount(array3) .eq. 2) .and. useXY_dummy then
      print("Rank data for vector u is 1 !!! Vectors fields must have a rank >= 2 !")
      status_exit(1)
    else 
      if (ListCount(array3) .ge. 2) then ; ListCount eq 3 or 4 <=> rk eq 2
        ;latdimv=array3[1]
        if (lat_exist3 .and. lon_exist3) then londimv=array3[2] end if
        if (lon_exist3 .and. .not. lat_exist3) then londimv=array3[1] end if
      end if
    end if

    print("-----> Vector v ")
    
    ; Reading vector v and reduction if necessary
    lat_exist4=True
    lon_exist4=True
    useLatDimv=False
    vselect=""
    array4=field_reduce(v_file, v_var, y, useXY_dummy, horizontal_dummy, useLatDimv, vprofile_dummy, vselect, lat_exist4, lon_exist4, proj_data_dummy)

    fld4=array4[0]
    if (ListCount(array4) .eq. 2) .and. useXY_dummy then
      print("Rank data for vector v is 1 !!! Vectors fields must have a rank >= 2 !")
      status_exit(1)
    else 
      if (ListCount(array4) .ge. 2) then ; ListCount eq 3 or 4 <=> rk eq 2
        ;londimv=array4[2]
        if lat_exist4 then latdimv=array4[1] end if
      end if
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
        vx=fld3
        vy=fld4
        fld3 = vx * new_gcosu - vy * new_gsinu
        fld4 = vx * new_gsinv + vy * new_gcosv
      else
        print("File angles.nc cannot be accessed")
        status_exit(2)
      end if
    end if 
      
  end if ; VECT

  ;-----------------
  ; Open workstation
  ;-----------------

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
  gsn_define_colormap(wks,colormap)

  i = NhlNewColor(wks,0.8,0.8,0.8)
  ; reverse colormap
  if (isvar("reverse") .and. reverse) then gsn_reverse_colormap(wks) end if

  ; main field resources
  res=True
  res@gsnFrame= False
  res@gsnDraw= False
  res@gsnMaximize = True
  res@gsnPaperOrientation="portrait" 

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ; ContourPlot resources
  if (.not. useXY  ) then 
    res@gsnSpreadColors     = True
    res@gsnSpreadColorEnd   = -2

    ; Main title
    if isvar("title") then res@tiMainString  = title end if

    if isvar("tiMainFont") then
      res@tiMainFont = tiMainFont ;22 <=> "helvetica-bold"
    end if
    if isvar("tiMainFontHeightF") then
      res@tiMainFontHeightF  = tiMainFontHeightF ;.030       
    end if
    if isvar("tiMainPosition") then
      res@tiMainPosition = tiMainPosition
      res@tiMainJust = "Center"+tiMainPosition
    end if

    ; 3 sub-titles (label, font, height)
    if isvar("gsnLeftString") then
      res@gsnLeftString = gsnLeftString
    end if
    
    if .not. isvar("gsnRightString") then
      if power10.ge.4 then
        res@gsnRightString = units+" x10~S~"+sprinti("%0.1i", power10)+""
      else
        res@gsnRightString = units ; ncl default
      end if
    else
      res@gsnRightString = gsnRightString
    end if

    if .not. isvar("gsnCenterString") then
      if ( isvar("date") .or. isvar("time") .or. isvar("level") ) then
        main_field_select=str_left_strip(main_field_select) ; strips leading spaces from the input strings
        main_field_select=str_sub_str(main_field_select," ",", ") 
        main_field_select=str_sub_str(main_field_select,"time","t")
        main_field_select=str_sub_str(main_field_select,"date","t")
        main_field_select=str_sub_str(main_field_select,"level","l")
        res@gsnCenterString = main_field_select     
      end if
    else 
      res@gsnCenterString = gsnCenterString
    end if
    
    if isvar("gsnStringFont") then
      res@gsnStringFont = gsnStringFont ; "helvetica-bold"
    end if
    if isvar("gsnStringFontHeightF") then
      res@gsnStringFontHeightF = gsnStringFontHeightF
    else 
      res@gsnStringFontHeightF = 0.012
    end if

    ; Label Bar
    res@lbLabelBarOn = True
    res@lbTitleOn    = False
    ;res@lbTitleFontHeightF=0.012
    
    if isvar("lbLabelFontHeightF") then
      res@lbLabelFontHeightF=lbLabelFontHeightF ;0.012
    end if
    res@lbLabelFontThicknessF= 3.0
    res@lbTitleFontThicknessF= 3.0
    res@lbLabelAutoStride = True
    if ( .not. isvar("vcb") .or. (isvar("vcb") .and. vcb) ) then
      res@lbOrientation     = "vertical"
    else
      if ( isvar("vcb") .and. (.not. vcb) ) then
        res@lbOrientation     = "horizontal"
      end if
    end if

    ; Axis Label 
    if (.not. isvar("proj")) then 
      if isvar("tmYLLabelFontHeightF") then
        res@tmYLLabelFontHeightF = tmYLLabelFontHeightF ;0.015
      end if
      if isvar("tmXBLabelFontHeightF") then
        res@tmXBLabelFontHeightF = tmXBLabelFontHeightF ;0.015
      end if
      
      if type.eq."png" then
        res@tmYLLabelFontThicknessF=2.0
        res@tmXBLabelFontThicknessF=2.0
      end if
     
    else ; proj
      if isvar("gsnPolarLabelFontHeightF") then
        res@gsnPolarLabelFontHeightF=gsnPolarLabelFontHeightF
      end if
    end if

    if (.not. horizontal) then ; cross-section
      if isvar("tmYRLabelFontHeightF") then
        res@tmYRLabelFontHeightF=tmYRLabelFontHeightF
      end if
    end if
    
    if isvar("tiYAxisFontHeightF") then
      res@tiYAxisFontHeightF=tiYAxisFontHeightF
    else
      if (.not. horizontal) then ; cross-section
        res@tiYAxisFontHeightF=0.024
      end if
    end if
    
    if isvar("tiXAxisFontHeightF") then
      res@tiXAxisFontHeightF=tiXAxisFontHeightF
    end if
      
    ; Levels
    res@cnFillOn=True 
    if (controlMinMax) then 
      res@cnLevelSelectionMode = "ManualLevels" 
      res@cnMinLevelValF = vmin
      res@cnMaxLevelValF = vmax
      res@cnLevelSpacingF = vdelta
    end if
    if ( isvar("ccolors") ) then
      res@cnLevelSelectionMode = "ExplicitLevels"
      res@cnLevels=tofloat(str_split(ccolors," "))
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
                if isvar("londim") then res2@sfXArray = londim end if          
                if isvar("latdim") then res2@sfYArray = latdim end if
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
      res2@cnLineLabelBackgroundColor = -1
      res2@cnInfoLabelString = ""
    
      res2@cnLinesOn=True
      if ( isvar("shade_below") .or. isvar("shade_above") ) then 
        res2@cnLinesOn=False
      end if

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
          if isvar("londim2") then res2@sfXArray = londim2 end if
          if isvar("latdim2") then res2@sfYArray = latdim2 end if
          res2@gsnAddCyclic = False
        end if
      end if
     
      if ( isvar("shade_below") .or. isvar("shade_above") ) then 
        ; without low or high values, for shading all the field
        ;res2@cnMonoFillPattern = True
        ;res2@cnMonoFillColor   = True   ; Use same fill color
        ;res2@cnFillPattern = 3

        res2@lbLabelBarOn = False
        res2@cnFillOn=True
        ;res2@cnFillColor    = "black"   ; foreground by default
        opt = True
        opt@gsnShadeFillType = "pattern" ; "color" or "pattern"
      end if
      
    end if ; NOT AUX_FIELD

    if (LABELON) then 
      res@cnLineLabelsOn=True
    end if   
    if (RASTER) then
      if (.not. LINEON) then 
        res@cnLinesOn=False
        res@cnLineLabelsOn=False
      end if
      ;res@cnRasterModeOn=True
      res@cnFillMode = "RasterFill" 
      res@cnRasterSmoothingOn=True 
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
      
      if (isvar("proj") .and. proj .ne. "") then 
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
        else
          res@mpProjection=proj
          if (isvar("mpCenterLonF")) then
            do while ((mpCenterLonF .gt. 180) .and. (mpCenterLonF .le. 360))
              mpCenterLonF=mpCenterLonF-360
            end do
            if mpCenterLonF .gt. (max(londim)-180) then
              print("out of data range: mpCenterLonF + 180 > max(londim)")
            end if
            if .not. useLatDim .and. ( mpCenterLonF .lt. (max(londim)-180) ) then ; for only rectilinear grids
                                ; pivots about a user-specified longitude (rectilinear grids only)
              fld_flip=lonPivot(fld,mpCenterLonF+180) 
              delete(fld)
              fld=fld_flip
              delete(fld_flip)
            end if
            res@mpCenterLonF=mpCenterLonF
          end if
        end if
        
      else
        if isvar("latdim") then
          res@mpMinLatF                = min(latdim)
          res@mpMaxLatF                = max(latdim)
        end if
        if (isvar("mpCenterLonF")) then
          do while ((mpCenterLonF .gt. 180) .and. (mpCenterLonF .le. 360))
            mpCenterLonF=mpCenterLonF-360
          end do
          if mpCenterLonF .gt. (max(londim)-180) then
            print("out of data range: mpCenterLonF + 180 > max(londim)")
          end if
          if .not. useLatDim .and. ( mpCenterLonF .lt. (max(londim)-180) ) then ; for only rectilinear grids
            ; pivots about a user-specified longitude (rectilinear grids only)
            fld_flip=lonPivot(fld,mpCenterLonF+180) 
            delete(fld)
            fld=fld_flip
            delete(fld_flip)
          end if
          res@mpCenterLonF=mpCenterLonF
                    
        else
          if isvar("londim") then
            res@mpMinLonF                = min(londim)
            res@mpMaxLonF                = max(londim)
            res@mpCenterLonF=(min(londim)+max(londim))/2
          end if
        end if

      end if
      
      if proj_data then ; Lambert projection
        
        if (proj_data@projection_type .eq. "Lambert_Conformal") then 
          
          nlat=dimsizes(latdim(:,0))
          nlon=dimsizes(londim(0,:))
          
          res@mpProjection = "LambertConformal"     ; Change map projection

          ; Not sure why these values work for the parallels. Normally 
          ; we would use the 'standard_parallel' attribute attached
          ; to this variable.
      
          res@mpLambertParallel1F   = proj_data@latitude_of_projection_origin
          res@mpLambertParallel2F   = proj_data@latitude_of_projection_origin
          res@mpLambertMeridianF    = proj_data@longitude_of_central_meridian
          
          res@mpLimitMode           ="Corners"      
          res@mpLeftCornerLatF      = latdim(0,0)           ;latdim(nlat-1,0)
          res@mpLeftCornerLonF      = londim(0,0)           ;londim(nlat-1,0)
          res@mpRightCornerLatF     = latdim(nlat-1,nlon-1) ;latdim(0,nlon-1)
          res@mpRightCornerLonF     = londim(nlat-1,nlon-1) ;londim(0,nlon-1)
       
          ; usually, when data is placed onto a map, it is TRANSFORMED to the specified
          ; projection. Since this model is already on a native lambert conformal grid,
          ; we want to turn OFF the tranformation.
        
          res@tfDoNDCOverlay        = False         ; plot is smoother if True
          res@mpDataBaseVersion     = "MediumRes"   ; Better map outlines
          res@pmTickMarkDisplayMode = "Always"      ; Turn on tickmarks
            
        else
          print("Cannot describe grid to Ncl due to lack of auxiliary field. Let Ncl decide.")
        end if
        
      end if

    end if ;end horizontal

    if VECT then 
      if (isvar("vcRefMagnitudeF")) then                ; define vector ref magnitude
        res@vcRefMagnitudeF=vcRefMagnitudeF
      end if
    
      if (isvar("vcRefLengthF")) then         	        ; define size of ref vector
        res@vcRefLengthF=vcRefLengthF
      end if
      
      if (isvar("vcMinDistanceF")) then                 ; define density of vectors
        res@vcMinDistanceF        = vcMinDistanceF
      else
        res@vcMinDistanceF        = 0.017               ; thins arrows near pole
      end if
      
      if (isvar("vcGlyphStyle")) then                   ; style of vectors: "LineArrow" (default), "CurlyVector", ...
        res@vcGlyphStyle          = vcGlyphStyle
      end if
      
      res@vcRefAnnoOrthogonalPosF = -1.                 ; move ref vector  
      res@vcRefAnnoParallelPosF = 1.                    ; move ref vector  
      res@vcRefAnnoFontHeightF = 0.01

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
        res@gsnAddCyclic = False
        if useLatDimv then
          if isvar("londimv") then res@vfXArray = londimv end if
          if isvar("latdimv") then res@vfYArray = latdimv end if
          res@gsnAddCyclic        = False
        end if
      end if
    end if ; VECT
    
  end if  ; not useXY
  
  ; Viewport resources
  res@vpWidthF  =0.8
  res@vpHeightF = 0.8

  res@vpXF      =0.1
  res@vpYF      =0.96

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 
  ; Profile
  if useXY then 
    xyres = True
    xyres@gsnDraw = False
    xyres@gsnFrame = False
    xyres@gsnMaximize = True
    xyres@gsnPaperOrientation = "portrait"
    xyres@vpXF = 0.5
    xyres@vpWidthF = 0.45
    xyres@vpHeightF = 0.45
    xyres@txFontHeightF = 0.010
    xyres@xyLineThicknesses = 3.0 ;(/ 2.0, 3.0/)
    xyres@xyLineColor = "black"
    if isvar("title") then xyres@tiMainString = title end if

    if isvar("gsnLeftString") then
      xyres@gsnLeftString = gsnLeftString
    else
      if isatt(fld,"long_name") then xyres@gsnLeftString=fld@long_name end if
    end if

    if isvar("gsnRightString") then
      xyres@gsnRightString=gsnRightString
    else
      if isatt(fld,"units") then xyres@gsnRightString=units end if
    end if

    if .not. isvar("gsnCenterString") then
      if ( isvar("date") .or. isvar("time") .or. isvar("level") ) then
        main_field_select=str_left_strip(main_field_select) ; strips leading spaces from the input strings
        main_field_select=str_sub_str(main_field_select," ",", ") 
        main_field_select=str_sub_str(main_field_select,"time","t")
        main_field_select=str_sub_str(main_field_select,"date","t")
        main_field_select=str_sub_str(main_field_select,"level","l")
        xyres@gsnCenterString = main_field_select     
      end if
    else 
      xyres@gsnCenterString = gsnCenterString
    end if
 
    if isvar("tiMainFontHeightF") then
      xyres@tiMainFontHeightF=tiMainFontHeightF
    end if
    if isvar("tmXBLabelFontHeightF") then
      xyres@tmXBLabelFontHeightF=tmXBLabelFontHeightF 
    else
      xyres@tmXBLabelFontHeightF=0.008
    end if
    if isvar("tmYLLabelFontHeightF") then
      xyres@tmYLLabelFontHeightF=tmYLLabelFontHeightF 
    else
      xyres@tmYLLabelFontHeightF=0.008
    end if
    if isvar("tiXAxisFontHeightF") then
      xyres@tiXAxisFontHeightF=tiXAxisFontHeightF
    end if
    if isvar("tiYAxisFontHeightF") then
      xyres@tiYAxisFontHeightF=tiYAxisFontHeightF
    end if

    ; auxiliary field
    if AUX_FIELD then
      xyres2 = True
      xyres2@gsnDraw = False
      xyres2@gsnFrame = False
      xyres2@xyLineThicknesses = 3.0
    end if
    
    if type.eq."png" then
      xyres@tmXBLabelFontThicknessF = 3.0
      xyres@tmYLLabelFontThicknessF = 3.0
      xyres@txFontThicknessF = 3.0
    end if
    
    if vprofile then ; case fld(z)
      if invXY then
        xyres@trXReverse = True ; reverse X-axis
        xaxis=hdim
        yaxis=fld
        if (y .eq. "log") then
          xyres@xyXStyle = "Log" 
        else
          if (y .eq. "index") then  ; index linear 
            xyres@xyXStyle = "Irregular"
            xyres@xyXIrregularPoints = hdim
          end if
        end if
        if isvar("vmin") then xyres@trYMinF=vmin end if
        if isvar("vmax") then xyres@trYMaxF=vmax end if
      else
        xyres@trYReverse = True ; reverse Y-axis
        xaxis=fld
        yaxis=hdim
        if (y .eq. "log") then
          xyres@xyYStyle = "Log" 
          set_pres_hgt_axes(hdim,xyres,True)
        else
          if (y .eq. "index") then  ; index linear 
            xyres@xyYStyle = "Irregular"
            xyres@xyYIrregularPoints = hdim
          end if
        end if
        if isvar("vmin") then xyres@trXMinF=vmin end if
        if isvar("vmax") then xyres@trXMaxF=vmax end if
      end if      
      if isvar("options") then res_list(options, xyres) end if
      plot0=gsn_csm_xy(wks,xaxis,yaxis,xyres)
      if AUX_FIELD then
        if invXY then
          xaxis2=hdim2
          yaxis2=fld2
        else
          xaxis2=fld2
          yaxis2=hdim2
        end if
        if isvar("aux_options") then res_list(aux_options, xyres2) end if 
        plot1=gsn_csm_xy(wks,xaxis2,yaxis2,xyres2)
      end if

    else ; case fld(t), fld(x) or fld(y)
      if invXY then
        xaxis=fld
        yaxis=hdim
        if isvar("vmin") then xyres@trXMinF=vmin end if
        if isvar("vmax") then xyres@trXMaxF=vmax end if
      else
        xaxis=hdim
        yaxis=fld
        if isvar("vmin") then xyres@trYMinF=vmin end if
        if isvar("vmax") then xyres@trYMaxF=vmax end if
      end if
      ; if 'fld' has a time dimension (i.e. fld(t)), produce nicely-formatted time labels on time axis
      time_labels(fld, xyres, invXY) 
      if isvar("options") then res_list(options, xyres) end if 
      plot0=gsn_csm_xy(wks,xaxis,yaxis,xyres)
      if AUX_FIELD then
        if invXY then
          xaxis2=fld2
          yaxis2=hdim2
        else
          xaxis2=hdim2
          yaxis2=fld2
        end if
        if isvar("aux_options") then res_list(aux_options, xyres2) end if 
        plot1=gsn_csm_xy(wks,xaxis2,yaxis2,xyres2)
      end if
      
    end if
  else
    if (horizontal) then 
      res@gsnAddCyclic = False
      if useLatDim then 
        ;res@trGridType          = "TriangularMesh"
        if isvar("londim") then res@sfXArray = londim end if
        if isvar("latdim") then res@sfYArray = latdim end if
        res@gsnAddCyclic        = False
      end if
 
      print("using gsn_csm_contour_map")
      if isvar("options") then res_list(options, res) end if 
      if VECT then
        plot0=gsn_csm_vector_scalar_map(wks,fld3,fld4,fld,res)
      else
        plot0=gsn_csm_contour_map(wks,fld,res)
      end if
        
      if .not. AUX_FIELD then
        if (LEVELS_CONTOURS) then
          if isvar("options") then res_list(options, res2) end if 
          plot1=gsn_csm_contour(wks,fld,res2)
        end if
      else
        if isvar("aux_options") then res_list(aux_options, res2) end if
        plot1=gsn_csm_contour(wks,fld2,res2)
        if ( isvar("shade_below") .or. isvar("shade_above") ) then plot1 = shading(plot1,fld2,opt) end if
      end if
        
      if isvar("shade2_options") .and. isvar("shade2_file") then
        res_shade2=True
        res_shade2@gsnFrame= False
        res_shade2@gsnDraw=False
        res_shade2@gsnMaximize = True
       
        res_shade2@gsnLeftString     = ""
        res_shade2@gsnRightString    = ""
        res_shade2@gsnCenterString   = ""
       
        res_shade2@cnFillOn=True
        res_shade2@cnLineLabelsOn = False
        res_shade2@cnLineLabelBackgroundColor = -1
        res_shade2@cnInfoLabelString = ""
        
        res_shade2@cnLinesOn=False
        ;res_shade2@gsnContourNegLineDashPattern = 1
        ;res_shade2@gsnContourZeroLineThicknessF = 0
        res_shade2@lbLabelBarOn = False ;
        ;res_shade2@cnFillOn=True
        ;res_shade2@cnFillColor    = "black"   ; foreground by default
                                ;res_shade2@cnFillScaleF        = 0.6         ; add extra density
        plot_shade2=gsn_csm_contour(wks,fld_shade2,res_shade2)
                                ;
        opt_shade2=True
        ;opt_shade2@gsnShadeFillScales=(/1.,0.66, 0.45/)
        opt_shade2@gsnShadeFillType = "pattern" ; "color" or "pattern"
        ;opt_shade2@gsnShadeLow = 17 
        res_list(shade2_options, opt_shade2)
        plot_shade2 = gsn_contour_shade(plot_shade2,str_convert(shade2_below),str_convert(shade2_above),opt_shade2)
      end if
      
      ;if VECT then
      ;  plot2=gsn_csm_vector(wks,fld3,fld4,res)
      ;end if
        
    else ; cross-section or (t,z) profile
      
      time_pos=time_position(fld)

      if (y .eq. "index") then
        print("using gsn_csm_contour; y with index-linear spacing")
        
        if ( (invXY .and. ( (time_pos .eq. -1) .or. (time_pos .eq. 1) )) \
          .or. (.not. invXY .and. (time_pos .eq. 0)) ) then
          res@trXReverse        = True ; reverse X-axis
        else
          res@trYReverse        = True ; reverse Y-axis
        end if
      end if
          
      if (y .eq. "lin") then
        print("using gsn_csm_contour; y with data-linear spacing")
        
        if ( (invXY .and. ( (time_pos .eq. -1) .or. (time_pos .eq. 1) )) \
          .or. (.not. invXY .and. (time_pos .eq. 0)) ) then
          res@trXReverse        = True ; reverse X-axis
          res@gsnXAxisIrregular2Linear= True
          if ( (.not. AUX_FIELD .and. LEVELS_CONTOURS) .or. AUX_FIELD ) then res2@gsnXAxisIrregular2Linear= True end if
        else
          res@trYReverse        = True ; reverse Y-axis
          res@gsnYAxisIrregular2Linear= True
          if ( (.not. AUX_FIELD .and. LEVELS_CONTOURS) .or. AUX_FIELD ) then res2@gsnYAxisIrregular2Linear= True end if
        end if
      end if

      if (y .eq. "log") then
        print("using gsn_csm_pres_hgt")
        
        if .not. ( (invXY .and. ( (time_pos .eq. -1) .or. (time_pos .eq. 1) )) \
          .or. (.not. invXY .and. (time_pos .eq. 0)) ) then

          ; turn off special labels on right axis
          if ( (.not. AUX_FIELD .and. LEVELS_CONTOURS) .or. AUX_FIELD ) then res2@tmYRMode = "Automatic" end if
        end if
      end if

      if invXY then
        fld_tr=field_transpose(fld)
        delete(fld)
        fld=fld_tr
        delete(fld_tr)
        if AUX_FIELD then
          fld2_tr=field_transpose(fld2)
          delete(fld2)
          fld2=fld2_tr
          delete(fld2_tr)
        end if
      end if

      time_labels(fld, res, invXY) ; if 'fld' has a time dimension, produce nicely-formatted time labels on time axis
      
      if isvar("options") then res_list(options, res) end if 
      if (y .eq. "lin") .or. (y .eq. "index") then 
        plot0=gsn_csm_contour(wks,fld,res)
      else
        if (y .eq. "log") then plot0=gsn_csm_pres_hgt(wks,fld,res) end if
      end if
      if .not. AUX_FIELD then
        if (LEVELS_CONTOURS) then
          if isvar("options") then res_list(options, res2) end if 
          if (y .eq. "lin") .or. (y .eq. "index") then 
            plot1=gsn_csm_contour(wks,fld,res2)
          else
            if (y .eq. "log") then plot1=gsn_csm_pres_hgt(wks,fld,res2) end if
          end if
        end if
      else
        if isvar("aux_options") then res_list(aux_options, res2) end if 
        if (y .eq. "lin") .or. (y .eq. "index") then 
          plot1=gsn_csm_contour(wks,fld2,res2)
        else
          if (y .eq. "log") then plot1=gsn_csm_pres_hgt(wks,fld2,res2) end if
        end if
        if ( isvar("shade_below") .or. isvar("shade_above") ) then plot1 = shading(plot1,fld2,opt) end if
      end if

    end if ; cross-section or (t,z) profile
    
  end if

  if LEVELS_CONTOURS .or. AUX_FIELD then
    overlay(plot0,plot1)   
  end if

  if isvar("shade2_options") .and. isvar("shade2_file") then
    overlay(plot0,plot_shade2)   
  end if
  
  ;if VECT then
  ;  overlay(plot0,plot2)  
  ;end if

  ;
  ; Attach a polyline to the plot
  ;
  if isvar("xpolyline") .and. isvar("ypolyline") then
    if dimsizes(str_split(xpolyline,",")) .eq. dimsizes(str_split(ypolyline,",")) then
      polysize=dimsizes(str_split(xpolyline,","))
    else
      print("X and Y coordinates of the polyline must have the same length.")
      status_exit(2)
    end if
  
    xpts=(/tofloat(str_split(xpolyline,","))/)
    ypts=(/tofloat(str_split(ypolyline,","))/)
 
    resp                  = True            
    resp@gsLineColor      = "red"                    ; color of lines
    resp@gsLineThicknessF = 3.0                      ; thickness of lines

    if isvar("polyline_options") then res_list(polyline_options, resp) end if
 
    ; create array of dummy graphic variables
    dum = new(polysize-1,graphic)

    ; draw each line separately, each line must contain two points
    do i = 0, polysize-2
      dum(i)=gsn_add_polyline(wks,plot0,xpts(i:i+1),ypts(i:i+1),resp)      
    end do
  end if
  ; end polyline
  
  draw(plot0)
  
  frame(wks)

  if ( type .eq. "png" .and. trim ) then
      system("convert "+plotname+" -trim "+plotname)
  end if

  status_exit(0)
  
end
