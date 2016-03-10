;******************************************************************
; Plot Hovmoller diagrams
; Usage and interfacing : see CliMAF doc 
; http://climaf.readthedocs.org/en/latest/scripts/timesection.html
;
; First version - march 2016
;******************************************************************

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl"

;-----------------------------------------------------------------------------------------------
undef("LatLon_names")
; Return names of latitude and longitude dimensions
function LatLon_names(ffile, field)
begin
  latname="lat"
  lonname="lon"
  if .not.ismissing(str_match(getvardims(field),"latitude")) then
    latname="latitude"
    lonname="longitude"
  end if
  if .not. ismissing(str_match(getvardims(field),"LAT")) then
    latname="LAT"
    lonname="LON"
  end if
  if (ismissing(str_match(getvardims(field),"lat"))) .and. (ismissing(str_match(getvardims(field),"LAT"))) then
    if ( isatt(field,"coordinates") .and. ( (.not. ismissing(str_match(field@coordinates,"lat"))) .or. (.not. ismissing(str_match(field@coordinates,"LAT"))) ) ) then
      if isfilevar(ffile,"nav_lat") then 
        latname="nav_lat" 
        lonname="nav_lon"
      end if
    end if
  end if
  return(/latname, lonname/)
end
;-----------------------------------------------------------------------------------------------
undef("data_select")
; Select value 'arg' of optional argument 'arg_name' for dimension 'dim_field_name' of 'field'
; and create a list, called 'select_list', of extracted values 
function data_select(arg_name:string, arg:numeric, field:numeric, dim_field_name:string, select_list:string)
local VarDimNames, dim, rk, index
begin
;  print(dim_field_name)
;  if ismissing(dim_field_name) then 
;    print("The dimension selected is missing !")
;    status_exit(1)
;  end if
  VarDimNames = getvardims(field)
  dim=dimsizes(field)
  rk=dimsizes(dim)
  
  if isint(arg) then
    print("Selecting index "+arg+" for "+arg_name+", i.e. "+arg_name+" = "+field&$dim_field_name$(arg))
    select_list=select_list+" "+arg_name+"="+field&$dim_field_name$(arg)
    if rk .eq. 4 then
      if isvar("xpoint") then 
        new_fld=field(:,:,:,arg)
      else if isvar("ypoint") then 
        new_fld=field(:,:,arg,:) 
      else if isvar("zpoint") then 
        new_fld=field(:,arg,:,:)     
      end if
      end if
      end if
    else 
      if rk .eq. 3 then
        if arg_name .eq. "latitude"  then
;          if VarDimNames(1) .eq. "level"  then 
          if ( .not. ismissing(str_match(VarDimNames(1),"depth")) .or. (VarDimNames(1) .eq. "sigma") \
            .or. (VarDimNames(1) .eq. "z") .or. (VarDimNames(1) .eq. "Z") \
            .or. (VarDimNames(1) .eq. "plev") .or. (VarDimNames(1) .eq. "lev") .or. (VarDimNames(1) .eq. "level") \
            .or. (VarDimNames(1) .eq. "p") .or. (VarDimNames(1) .eq. "pressure") \
            .or. ( iscoord(field,VarDimNames(1)) .and. isatt(field&$VarDimNames(1)$,"axis") .and. ( (field&$VarDimNames(1)$@axis .eq. "z") .or. (field&$VarDimNames(1)$@axis .eq. "Z") ) ) ) then
            new_fld=field(:,:,arg) 
          else
            new_fld=field(:,arg,:)
          end if
        end if
        if arg_name .eq. "longitude"   then new_fld=field(:,:,arg) end if
        if arg_name .eq. "level" then new_fld=field(:,arg,:) end if  
      else 
        if rk .eq. 2 then
          new_fld=field(:,arg)
        end if ; rk eq 2
      end if ; rk eq 3
    end if ; rk eq 4
 
  else
    if isfloat(arg) then 
      index=closest_val(arg,field&$dim_field_name$)
      print("Selecting "+arg_name+" closed to "+arg+", i.e. "+arg_name+" = "+field&$dim_field_name$(index))
      select_list=select_list+" "+arg_name+"="+field&$dim_field_name$(index)
      if rk .eq. 4 then
        if isvar("xpoint") then 
          new_fld=field(:,:,:,index)
        else if isvar("ypoint") then 
          new_fld=field(:,:,index,:) 
        else if isvar("zpoint") then 
          new_fld=field(:,index,:,:)     
        end if
        end if
        end if
      else 
        if rk .eq. 3 then
          if arg_name .eq. "latitude"  then
;            if VarDimNames(1) .eq. "level"  then 
            if ( .not. ismissing(str_match(VarDimNames(1),"depth")) .or. (VarDimNames(1) .eq. "sigma") \
              .or. (VarDimNames(1) .eq. "z") .or. (VarDimNames(1) .eq. "Z") \
              .or. (VarDimNames(1) .eq. "plev") .or. (VarDimNames(1) .eq. "lev") .or. (VarDimNames(1) .eq. "level") \
              .or. (VarDimNames(1) .eq. "p") .or. (VarDimNames(1) .eq. "pressure") \
              .or. ( iscoord(field,VarDimNames(1)) .and. isatt(field&$VarDimNames(1)$,"axis") .and. ( (field&$VarDimNames(1)$@axis .eq. "z") .or. (field&$VarDimNames(1)$@axis .eq. "Z") ) ) ) then
              new_fld=field(:,:,index) 
            else
              new_fld=field(:,index,:)
            end if
          end if
          if arg_name .eq. "longitude"   then new_fld=field(:,:,index) end if
          if arg_name .eq. "level" then new_fld=field(:,index,:) end if 
        else 
          if rk .eq. 2 then
            new_fld=field(:,index)
          end if ; rk eq 2
        end if ; rk eq 3
      end if ; rk eq 4
   
    end if ; arg is float
  end if ; arg is integer

  return(new_fld)
end
;-----------------------------------------------------------------------------------------------
undef("data_axavg")
; Computes the average of the variable corresponding to 'axmean' for 'field' in file 'ffile' 
; on a given domain ('latS, 'latN', 'lonE', 'lonW')
function data_axavg(ffile, field, axmean, latS, latN, lonE, lonW)
local X, Xmean, Var_DimNames, LatLon
begin
  Var_DimNames = getvardims(field)
  if dimsizes(Var_DimNames) .eq. 3 then
    LatLon= LatLon_names(ffile, field)
    if (axmean .eq. "Lat") then
;      if .not.ismissing(str_match(Var_DimNames(1),"level")) then
      if ( .not. ismissing(str_match(Var_DimNames(1),"depth")) .or. (Var_DimNames(1) .eq. "sigma") \
        .or. (Var_DimNames(1) .eq. "z") .or. (Var_DimNames(1) .eq. "Z") \
        .or. (Var_DimNames(1) .eq. "plev") .or. (Var_DimNames(1) .eq. "lev") .or. (Var_DimNames(1) .eq. "level") \
        .or. (Var_DimNames(1) .eq. "p") .or. (Var_DimNames(1) .eq. "pressure") \
        .or. ( iscoord(field,Var_DimNames(1)) .and. isatt(field&$Var_DimNames(1)$,"axis") .and. ( (field&$Var_DimNames(1)$@axis .eq. "z") .or. (field&$Var_DimNames(1)$@axis .eq. "Z") ) ) ) then
        ;print("--> No reorder ")
        X = field($Var_DimNames(0)$|:,$Var_DimNames(1)$|:,{$LatLon(0)$|latS:latN})
;      else if .not.ismissing(str_match(Var_DimNames(2),"lon")) then
      else if .not.ismissing(str_match(Var_DimNames(2),"lon")) .or. .not.ismissing(str_match(Var_DimNames(2),"LON")) \
        .or. ( iscoord(field,Var_DimNames(2)) .and. isatt(field&$Var_DimNames(2)$,"standard_name") \
        .and. (field&$Var_DimNames(2)$@standard_name .eq. "longitude") ) \
        .or. ( iscoord(field,Var_DimNames(2)) .and. isatt(field&$Var_DimNames(2)$,"axis") \
        .and. ( (field&$Var_DimNames(2)$@axis .eq. "x") .or. (field&$Var_DimNames(2)$@axis .eq. "X") ) ) then
        ;print("--> Reorder ")
        ;print("-->  (t,x,y)")
        field = lonFlip(field)
        X = field($Var_DimNames(0)$|:,{$LatLon(1)$|lonE:lonW},{$LatLon(0)$|latS:latN})
      end if
      end if
    else 
      if (axmean .eq. "Lon") then
        ;print("--> No reorder ")
        field = lonFlip(field)
;        if .not.ismissing(str_match(Var_DimNames(1),"level")) then
        if ( .not. ismissing(str_match(Var_DimNames(1),"depth")) .or. (Var_DimNames(1) .eq. "sigma") \
          .or. (Var_DimNames(1) .eq. "z") .or. (Var_DimNames(1) .eq. "Z") \
          .or. (Var_DimNames(1) .eq. "plev") .or. (Var_DimNames(1) .eq. "lev") .or. (Var_DimNames(1) .eq. "level") \
          .or. (Var_DimNames(1) .eq. "p") .or. (Var_DimNames(1) .eq. "pressure") \
          .or. ( iscoord(field,Var_DimNames(1)) .and. isatt(field&$Var_DimNames(1)$,"axis") .and. ( (field&$Var_DimNames(1)$@axis .eq. "z") .or. (field&$Var_DimNames(1)$@axis .eq. "Z") ) ) ) then
          ;print("-->  (t,z,x)")
          X = field($Var_DimNames(0)$|:,$Var_DimNames(1)$|:,{$LatLon(1)$|lonE:lonW})
;        else if .not.ismissing(str_match(Var_DimNames(2),"lon")) then
        else if .not.ismissing(str_match(Var_DimNames(2),"lon")) .or. .not.ismissing(str_match(Var_DimNames(2),"LON")) \
          .or. ( iscoord(field,Var_DimNames(2)) .and. isatt(field&$Var_DimNames(2)$,"standard_name") \
          .and. (field&$Var_DimNames(2)$@standard_name .eq. "longitude") ) \
          .or. ( iscoord(field,Var_DimNames(2)) .and. isatt(field&$Var_DimNames(2)$,"axis") \
          .and. ( (field&$Var_DimNames(2)$@axis .eq. "x") .or. (field&$Var_DimNames(2)$@axis .eq. "X") ) ) then
          ;print("-->  (t,y,x)")
          X = field($Var_DimNames(0)$|:,{$LatLon(0)$|latS:latN}, {$LatLon(1)$|lonE:lonW})
        end if
        end if
;      else
;        if .not.ismissing(str_match(Var_DimNames,"lat"))
;          print("  field -->  min = "+ min(field) + "  max = " + max(field) )
;          X = field(time|:,level|:,{$LatLon(0)$|latS:latN})
;          print("  X -->  min = "+ min(X) + "  max = " + max(X) )
;        end if
      end if ; axmean eq "Lon"
    end if ; axmean eq "Lat"
  
    Xmean =  dim_avg_Wrap(X)
    return(Xmean)
  end if ; dimsizes
  
end
;-----------------------------------------------------------------------------------------------
undef("data_fmt")
; Reduce rank of field called 'var' in file 'ffile' on a given domain ('latS, 'latN', 'lonE', 'lonW') 
; by adapting to various cases, output field is 2D
function data_fmt(ffile, var, latS, latN, lonE, lonW, extract_list)
local fld, tmpfld, new_fld, vardim, rk, LatLon, ds, tmp, dataONdom
begin
  ;print("(1) ############    data_fmt")
  cr = tochar(10)
  if (getfilevartypes(ffile,var) .eq. "short") then
    fld = short2flt( ffile->$var$ )
  else
    fld = ffile->$var$
  end if
  tmpfld= rm_single_dims(fld)
  delete(fld)
  fld=tmpfld
  delete(tmpfld)
  vardim=getvardims(fld)  ; getting dimensions from metadata
  rk=dimsizes(vardim)

  ; Try to adapt to various cases, using heuristics ! 
  ; Assume dimensions order is anyway t,z,y,x, but that some may be missing 
  if  (rk .lt. 2) .or. (rk .gt. 4)  then 
    print("This script is not tuned for this rank data for field ( rk ="+rk +")")
    status_exit(1)
;  else if ismissing(str_match(vardim,"time")) then
  else if ismissing(str_match(vardim(0),"time"))  \
    .and. ( iscoord(fld,vardim(0)) .and. isatt(fld&$vardim(0)$,"standard_name") \
    .and. (fld&$vardim(0)$@standard_name .ne. "time") ) then
    print("Hovmoller diagrams needs time dimension")
    print(vardim)
    status_exit(1)
  end if
  end if

  LatLon= LatLon_names(ffile, fld)
  if rk .eq. 4 then
    if axmean .eq. "Lat" then
      print("rank= "+rk+"-> mean on y axis")
      if isvar("zpoint") .and. .not.isvar("xpoint") .and. .not.isvar("ypoint") then
        ds=data_select("level", zpoint, fld, vardim(1), extract_list)
      else if isvar("xpoint") .and. .not.isvar("zpoint") .and. .not.isvar("ypoint") then
        ds=data_select("longitude", xpoint, fld, vardim(3), extract_list)
      else
        print("You must specify zpoint or xpoint"+cr)
        status_exit(1)
      end if
      end if 
      new_fld= data_axavg(ffile, ds, axmean, latS, latN, lonE, lonW)

    else if axmean .eq. "Lon" then
      print("rank= "+rk+"-> mean on x axis")
      if isvar("zpoint") .and. .not.isvar("xpoint") .and. .not.isvar("ypoint") then
        ds= data_select("level", zpoint, fld, vardim(1), extract_list)
      else if isvar("ypoint")  .and. .not.isvar("xpoint") .and. .not.isvar("zpoint") then
        ds= data_select("latitude", ypoint, fld, vardim(3), extract_list)
      else
        print("You must specify zpoint or ypoint"+cr)
        status_exit(1)
      end if
      end if
      new_fld= data_axavg(ffile, ds, axmean, latS, latN, lonE, lonW)

    else    ; axmean= Point
      if isvar("zpoint") .and. isvar("ypoint") .and. isvar("xpoint") then
        print("axmean='Point' => you have to select only two points because rank="+rk)
        status_exit(1)
      end if
      print("rank= "+rk+"-> No mean on any axis, axmean= "+axmean+cr)
      if isvar("xpoint") then
        ds=data_select("longitude", xpoint, fld, vardim(3), extract_list)
        if isvar("ypoint") then
          tmp=data_select("latitude", ypoint, ds, vardim(2), extract_list)
        else if isvar("zpoint") then
          tmp=data_select("level", zpoint, ds, vardim(1), extract_list)
        else
          print("You must specify two points"+cr)
          status_exit(1)
        end if
        end if
      else if isvar("ypoint") .and.  isvar("zpoint") then
        ;print("ypoint and zpoint")
        ds=data_select("latitude", ypoint, fld, vardim(2), extract_list)
        tmp=data_select("level", zpoint, ds, vardim(1), extract_list)
      else
        print("You must specify two points"+cr)
        status_exit(1)
      end if
      end if
;      if .not.ismissing(str_match(getvardims(tmp),"lat")) then
      dimvar=getvardims(tmp)
      if .not.ismissing(str_match(dimvar(1),"lat")) .or. .not.ismissing(str_match(dimvar(1),"LAT")) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"standard_name") \
        .and. (tmp&$dimvar(1)$@standard_name .eq. "latitude") ) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"axis") \
        .and. ( (tmp&$dimvar(1)$@axis .eq. "y") .or. (tmp&$dimvar(1)$@axis .eq. "Y") ) ) then
        new_fld = tmp($dimvar(0)$|:,{$LatLon(0)$|latS:latN})
;      else if .not.ismissing(str_match(getvardims(tmp),"lon")) then
      else if .not.ismissing(str_match(dimvar(1),"lon")) .or. .not.ismissing(str_match(dimvar(1),"LON")) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"standard_name") \
        .and. (tmp&$dimvar(1)$@standard_name .eq. "longitude") ) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"axis") \
        .and. ( (tmp&$dimvar(1)$@axis .eq. "x") .or. (tmp&$dimvar(1)$@axis .eq. "X") ) ) then
        tmp = lonFlip(tmp)
        new_fld = tmp($dimvar(0)$|:,{$LatLon(1)$|lonE:lonW})
      else
        new_fld = tmp
      end if
      end if
      
    end if ; axmean eq "Lon" 
    end if ; axmean eq "Lat" 
  end if ; rk eq 4

  if rk .eq. 3 then
    if (axmean .eq. "Lat") .or. (axmean .eq. "Lon") then
      print("rank= "+rk+"-> mean on "+ axmean +" axis")
      if isvar("zpoint") .or. isvar("xpoint") .or. isvar("ypoint") then
        print(cr+"Warning: selected points are not considered because rank=3 and a mean on one of axis is done"+cr)
      end if
      new_fld= data_axavg(ffile, fld, axmean, latS, latN, lonE, lonW)
    else      ; axmean= Point
      if ( isvar("zpoint") .and. isvar("ypoint") .and. isvar("xpoint") )\
        .or. (isvar("xpoint") .and. isvar("ypoint" ) ) \
        .or. (isvar("xpoint") .and. isvar("zpoint" ) ) \
        .or. (isvar("zpoint") .and. isvar("ypoint" ) ) \
        .or. ( .not.isvar("zpoint") .and. .not.isvar("ypoint") .and. .not.isvar("xpoint") ) then
        print("axmean='Point' => you have to select only one point because rank="+rk)
        status_exit(1)
      end if
      print("rank= "+rk+"-> No mean on any axis, axmean= "+axmean+cr)
      if isvar("xpoint") \
        .and. ( .not.ismissing(str_match(vardim(2),"lon")) .or. .not.ismissing(str_match(vardim(2),"LON")) \
        .or. ( iscoord(fld,vardim(2)) .and. isatt(fld&$vardim(2)$,"standard_name") \
        .and. (fld&$vardim(2)$@standard_name .eq. "longitude") ) \
        .or. ( iscoord(fld,vardim(2)) .and. isatt(fld&$vardim(2)$,"axis") \
        .and. ( (fld&$vardim(2)$@axis .eq. "x") .or. (fld&$vardim(2)$@axis .eq. "X") ) ) ) then
        tmp=data_select("longitude", xpoint, fld, vardim(2), extract_list)
      else if isvar("ypoint") then
;        print(fld&$"lon"$(10))
;        print(fld&$"lat"$(10))
;        tmp=data_select("lat", ypoint, fld, vardim(2))
;        if vardim(1) .eq. "level" then
;          tmp=data_select("latitude", ypoint, fld, vardim(2), extract_list)
;        else
;          tmp=data_select("latitude", ypoint, fld, vardim(1), extract_list)
;        end if
        if .not.ismissing(str_match(vardim(1),"lat")) .or. .not.ismissing(str_match(vardim(1),"LAT")) \
          .or. ( iscoord(fld,vardim(1)) .and. isatt(fld&$vardim(1)$,"standard_name") \
          .and. (fld&$vardim(1)$@standard_name .eq. "latitude") ) \
          .or. ( iscoord(fld,vardim(1)) .and. isatt(fld&$vardim(1)$,"axis") \
          .and. ( (fld&$vardim(1)$@axis .eq. "y") .or. (fld&$vardim(1)$@axis .eq. "Y") ) ) then
          tmp=data_select("latitude", ypoint, fld, vardim(1), extract_list)
          
        else if .not.ismissing(str_match(vardim(2),"lat")) .or. .not.ismissing(str_match(vardim(2),"LAT")) \
          .or. ( iscoord(fld,vardim(2)) .and. isatt(fld&$vardim(2)$,"standard_name") \
          .and. (fld&$vardim(2)$@standard_name .eq. "latitude") ) \
          .or. ( iscoord(fld,vardim(2)) .and. isatt(fld&$vardim(2)$,"axis") \
          .and. ( (fld&$vardim(2)$@axis .eq. "y") .or. (fld&$vardim(2)$@axis .eq. "Y") ) ) then
          tmp=data_select("latitude", ypoint, fld, vardim(2), extract_list)
        end if
        end if
 
      else if isvar("zpoint") \
        .and. ( .not. ismissing(str_match(vardim(1),"depth")) .or. (vardim(1) .eq. "sigma") \
        .or. (vardim(1) .eq. "z") .or. (vardim(1) .eq. "Z") \
        .or. (vardim(1) .eq. "plev") .or. (vardim(1) .eq. "lev") .or. (vardim(1) .eq. "level") \
        .or. (vardim(1) .eq. "p") .or. (vardim(1) .eq. "pressure") \
        .or. ( iscoord(fld,vardim(1)) .and. isatt(fld&$vardim(1)$,"axis") .and. ( (fld&$vardim(1)$@axis .eq. "z") .or. (fld&$vardim(1)$@axis .eq. "Z") ) ) ) then
        tmp=data_select("level", zpoint, fld, vardim(1), extract_list)
      else
        print("The dimension selected is missing !")
; replace log data_select
        status_exit(1)
      end if 
      end if
      end if
;      if .not.ismissing(str_match(getvardims(tmp),"lat")) then
      dimvar=getvardims(tmp)
      if .not.ismissing(str_match(dimvar(1),"lat")) .or. .not.ismissing(str_match(dimvar(1),"LAT")) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"standard_name") \
        .and. (tmp&$dimvar(1)$@standard_name .eq. "latitude") ) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"axis") \
        .and. ( (tmp&$dimvar(1)$@axis .eq. "y") .or. (tmp&$dimvar(1)$@axis .eq. "Y") ) ) then
        new_fld = tmp($dimvar(0)$|:,{$LatLon(0)$|latS:latN})
;      else if .not.ismissing(str_match(getvardims(tmp),"lon")) then
      else if .not.ismissing(str_match(dimvar(1),"lon")) .or. .not.ismissing(str_match(dimvar(1),"LON")) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"standard_name") \
        .and. (tmp&$dimvar(1)$@standard_name .eq. "longitude") ) \
        .or. ( iscoord(tmp,dimvar(1)) .and. isatt(tmp&$dimvar(1)$,"axis") \
        .and. ( (tmp&$dimvar(1)$@axis .eq. "x") .or. (tmp&$dimvar(1)$@axis .eq. "X") ) ) then
        tmp = lonFlip(tmp)
        new_fld = tmp($dimvar(0)$|:,{$LatLon(1)$|lonE:lonW})
      else
        new_fld = tmp
      end if
      end if
    end if ; axmean eq "Lat" or "Lon" 
  end if ; rk eq 3

  if rk .eq. 2 then
    print("rank= "+rk+"-> plot supplied coordinates")
    if .not.ismissing(str_match(getvardims(fld),"lat")) then
      new_fld = fld($vardim(0)$|:,{$LatLon(0)$|latS:latN})
    else if .not.ismissing(str_match(getvardims(fld),"lon")) then
      tmp = lonFlip(fld)
      new_fld = tmp($vardim(0)$|:,{$LatLon(1)$|lonE:lonW})
    else
      new_fld = fld
    end if
    end if
  end if ; rk eq 2
   
  dataONdom = ([/ new_fld, new_fld&$new_fld!1$ /])
  return(dataONdom)
end 
;-----------------------------------------------------------------------------------------------
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
;-----------------------------------------------------------------------------------------------
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
;-----------------------------------------------------------------------------------------------
; Main Program
;-----------------------------------------------------------------------------------------------
begin
  ;print("############    MAIN")
  setfileoption("nc","MissingToFillValue",False)
  quote = str_get_dq()
  cr = tochar(10)
  carriage = "~C~"       ; A string with a carriage ~C~ return in it
  axmean_names=(/"Lat","Lon","Point"/)
  if (.not.isvar("axmean"))  then
    print("You must specify at least 'axmean' argument which can be Lat, Lon or Point"+cr)
    status_exit(1)
  else if ismissing(str_match(axmean_names,axmean)) then 
    print("'axmean' argument can be only 'Lat', 'Lon' or 'Point' (axmean="+axmean+")")
    status_exit(1)
  end if
  end if

  if (.not.isvar("cmap")) then cmap="amwg256" end if
  if (.not.isvar("reverse")) then reverse=False end if
  if (.not.isvar("myscale")) then myscale=1.0 end if
  if (.not.isvar("myoffset")) then myoffset=0.0 end if
  if (.not.isvar("type")) then type="png" end if
  if (.not.isvar("trim")) then trim=True end if
  ;
  ;---Defining data to plot 
  ;                                            
  if isfilepresent(infile) then
    ffile=addfile(infile,"r")
    varNames =getfilevarnames(ffile)
    if isfilevar(ffile,var) then 
      dim_select=""
      if .not. ( isvar("latS") .and. isvar("latN") .and. isvar("lonE") .and. isvar("lonW") ) then
        latlon=LatLon_names(ffile, var)
        latS=min(ffile->$latlon(0)$)
        latN=max(ffile->$latlon(0)$)
        lonE=max(ffile->$latlon(1)$)
        lonW=min(ffile->$latlon(1)$)
      end if
      data_dom = data_fmt(ffile, var, latS, latN, lonE, lonW, dim_select)
      Xfld = data_dom[0]*tofloat(myscale)+tofloat(myoffset)
      copy_VarCoords(data_dom[0],Xfld)   ;  copy_VarCoords( var_from, var_to)
      XArray = tofloat(data_dom[1])
      copy_VarCoords(data_dom[1],XArray)
      XAxisString = getvardims(XArray)
    else
      print("File "+infile+" does not include variable "+var)
      status_exit(1)
    end if
  else
    print("File "+infile+" cannot be accessed")
    status_exit(2)
  end if
  ;
  ;--- Defining "units"
  if (.not. isvar("units")) then 
    if (isatt(Xfld,"units")) then units=Xfld@units else units="None" end if
  end if
  units=units 
  ;
  ;--- Defining the Time
  var_att = getvardims(Xfld)
  timname  = var_att(0)
  time = ffile->$timname$
  utc_date = cd_calendar(time, 0)
  year  = floattointeger(utc_date(:,0))
  period   = "(" + year(0) + "-" + year(dimsizes(year)-1) + ") "

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

  wks = gsn_open_wks ( type, plotname )  ; open workstation 
  gsn_define_colormap(wks,cmap)
  if (reverse) then
    gsn_reverse_colormap(wks)
  end if
  ;
  ; resources
  ;
  res                      = True               ; plot mods desired
  res@gsnDraw              = True               ; draw yet
  res@gsnFrame             = True               ; advance frame yet
  res@gsnMaximize          = True               ; use full page
  res@gsnSpreadColors      = True               ; use full range of color map
  res@vpWidthF             = .35
  res@vpHeightF            = .95
  ; title
;  if (.not.isvar("title")) then
  area = "(Domain: LAT "+latS+":"+latN+", LON "+lonW+":"+lonE+")"
  title = carriage+period+carriage+area+carriage+" "
;  end if
  res@tiMainString            = title   
  res@gsnLeftString           = var
  res@gsnRightString          = "("+units+")"
  if ( isvar("xpoint") .or. isvar("ypoint") .or. isvar("zpoint") ) then
    dim_select=str_left_strip(dim_select)       ; strips leading spaces from the input strings
    dim_select=str_sub_str(dim_select," ",", ") 
    dim_select=str_sub_str(dim_select,"latitude","y")
    dim_select=str_sub_str(dim_select,"longitude","x")
    dim_select=str_sub_str(dim_select,"level","l")
    res@gsnCenterString = dim_select     
  end if
  ;
  res@txFontHeightF           = 0.015
  res@lbLabelStride           = 1               ; every other label
  res@lbOrientation           = "Vertical"      ; vertical label bar
  ; Change the size of the left and center string labels
  res@cnLineLabelFontHeightF   = 0.015  
  res@cnInfoLabelFontHeightF   = 0.01
  ;
  ; Contour
  res@cnFillOn               = True             ; True-> full areas between contour levels
  res@cnLinesOn              = False            ; True-> contour lines
  res@cnLineLabelsOn         = False            ; True-> contour labels
  res@cnMaxLevelCount        = 25               ; default is 16
  ;
  ;--- Smoothing colors
  res@cnRasterSmoothingOn    = True
  res@cnFillOpacityF         = 0.6              ; color contours are partially transparent
  ;res@pmLabelBarOrthogonalPosF = -.001         ; move label bar closer
  res@lbLabelFont = "helvetica"
  res@lbLabelFontHeightF = .02
;  if .not.ismissing(str_match(getvardims(Xfld),"lev"))then 
  dimv= getvardims(Xfld)
  if ( .not. ismissing(str_match(dimv(1),"depth")) .or. (dimv(1) .eq. "sigma") \
    .or. (dimv(1) .eq. "z") .or. (dimv(1) .eq. "Z") \
    .or. (dimv(1) .eq. "plev") .or. (dimv(1) .eq. "lev") .or. (dimv(1) .eq. "level") \
    .or. (dimv(1) .eq. "p") .or. (dimv(1) .eq. "pressure") \
    .or. ( iscoord(Xfld,dimv(1)) .and. isatt(Xfld&$dimv(1)$,"axis") .and. ( (Xfld&$dimv(1)$@axis .eq. "z") .or. (Xfld&$dimv(1)$@axis .eq. "Z") ) ) ) then
    res@gsnXAxisIrregular2Log = True            ; set y-axis to log scale
  else
    res@tiXAxisString =  XAxisString 
    res@tmXMajorGrid = True
    res@tmXMajorGridThicknessF = 0.5
    res@tmXMinorGrid = True
    res@tmXMinorGridThicknessF = 0.25
  end if
  res@tiYAxisString = "Time"                    ; y axis title
  res@tmYMajorGrid = True
  res@tmYMajorGridThicknessF= 0.5
  res@tmYMinorGrid = False
  res@tmYMinorGridThicknessF= 0.25
  ;
  ; Y and X axis 
  ; Set special resources for the time axis
  resTickY                = True
  resTickY@ttmFormat      = "%Y"                ; 4-digit year
  resTickY@ttmAxis        = "YL"                ; Y left axis
  resTickY@ttmMajorStride = 12                  ; Number of timesteps desired between major tickmarks. 
  time_axis_labels( time,  res, resTickY )
  ;
  Xfeatures = nice_mnmxintvl( min(XArray), max(XArray), 4, False)
  Xmin = floattointeger(Xfeatures(0))
  Xmax = floattointeger(Xfeatures(1))
  XlevelSpacing = floattointeger(Xfeatures(2))
  res@tmXBLabelFontHeightF  = 0.018
  res@tmYLLabelFontHeightF  = 0.02
  res@tmXBTickSpacingF      = XlevelSpacing
  ;
  ;---Set some "nice" contour levels
  mnmxint = nice_mnmxintvl( min(Xfld(:,:)), max(Xfld(:,:)), 21, False)
  if (mnmxint(0).lt.0) then 
    symMinMaxPlt(Xfld, 14, False, res)           
  else
    res@cnLevelSelectionMode  = "ManualLevels"
    res@cnMinLevelValF  = mnmxint(0)
    res@cnMaxLevelValF  = mnmxint(1)
    res@cnLevelSpacingF = mnmxint(2)/2.         ; twice as many
  end if
  print("Plotted axis:")
  print(getvardims(Xfld))
  if isvar("options") then res_list(options, res) end if 
  plot = gsn_csm_hov(wks, Xfld, res) 

  if ( type .eq. "png" .and. trim ) then
    system("convert "+plotname+" -trim "+plotname)
  end if
  
  status_exit(0)
  
end