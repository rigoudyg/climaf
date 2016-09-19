;******************************************************************
; Plot Hovmoller diagrams
; Usage and interfacing : see CliMAF doc 
; http://climaf.readthedocs.org/en/latest/scripts/hovm.html

; Second version - may 2016
;******************************************************************

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl"

;-----------------------------------------------------------------------------------------------

undef("str_convert")
; Convert an input string into logical, integer, float or the same string
; Remark: same function as 'str_convert' of 'gplot.py'
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
; Remark: same function as 'res_list' of 'gplot.py'
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

undef("LatLon_names")
; Return names of latitude and longitude dimensions
function LatLon_names(ffile, field)

local latnames, lonnames, dimnames, i, k
begin

  latnames=(/"lat", "LAT", "latitude", "nav_lat"/)     ; dimnames(0,:)
  lonnames=(/"lon", "LON", "longitude", "nav_lon"/)    ; dimnames(1,:)
  dimnames=(/latnames, lonnames/)

  do k=0,1 
    do i=0, dimsizes(dimnames(k,:))-1
      if ( .not. ismissing(str_match(getvardims(field),dimnames(k,i))) \
        .or. (isatt(field,"coordinates") .and. .not. ismissing(str_match(field@coordinates,dimnames(k,i)))) ) then
        if (k .eq. 0) then latname=latnames(i) end if
        if (k .eq. 1) then lonname=lonnames(i) end if
      end if
    end do
  end do
  
  return(/latname, lonname/) 

end

;-----------------------------------------------------------------------------------------------

undef("data_select")
; Select value 'arg' of optional argument 'arg_name' for dimension 'dim_field_name' of 'field'
; and create a list, called 'select_list', of extracted values 
; Remark: this is a simplified function of function 'data_select' of 'gplot.py' (here, time extraction is not
; taken account)
function data_select(arg_name:string, arg:numeric, field:numeric, dim_field_name:string, select_list:string)

local VarDimNames, dim, rk, k, dim_pos, index
begin

  VarDimNames = getvardims(field)
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
    end if
  end if

  ; compute of new field with extraction at 'index'

; first version
;  if rk .eq. 4 then
;    if isvar("xpoint") then 
;      new_fld=field(:,:,:,index)
;    else 
;      if isvar("ypoint") then 
;        new_fld=field(:,:,index,:) 
;      else 
;        if isvar("zpoint") then 
;          new_fld=field(:,index,:,:)     
;        end if
;      end if
;    end if
;  else
;    if rk .eq. 3 then
;      if arg_name .eq. "latitude"  then
;        if ( .not. ismissing(str_match(VarDimNames(1),"dept")) .or. (VarDimNames(1) .eq. "sigma") \
;          .or. (VarDimNames(1) .eq. "z") .or. (VarDimNames(1) .eq. "Z") \
;          .or. (VarDimNames(1) .eq. "plev") .or. (VarDimNames(1) .eq. "lev") .or. (VarDimNames(1) .eq. "level") \
;          .or. (VarDimNames(1) .eq. "p") .or. (VarDimNames(1) .eq. "pressure") \
;          .or. ( iscoord(field,VarDimNames(1)) .and. isatt(field&$VarDimNames(1)$,"axis") .and. ( (field&$VarDimNames(1)$@axis .eq. "z") .or. (field&$VarDimNames(1)$@axis .eq. "Z") ) ) ) then
;          new_fld=field(:,:,index) 
;        else
;          new_fld=field(:,index,:)
;        end if
;      end if
;      if arg_name .eq. "longitude" then new_fld=field(:,:,index) end if
;      if arg_name .eq. "level" then new_fld=field(:,index,:) end if 
;    else 
;      if rk .eq. 2 then
;        new_fld=field(:,index)
;      end if ; rk eq 2
;    end if ; rk eq 3
;  end if ; rk eq 4
;
; second version
  if rk .eq. 4 then
    if dim_pos .eq. 1 then new_fld=field(:,index,:,:) end if
    if dim_pos .eq. 2 then new_fld=field(:,:,index,:) end if
    if dim_pos .eq. 3 then new_fld=field(:,:,:,index) end if
  else 
    if rk .eq. 3 then
      if dim_pos .eq. 1 then new_fld=field(:,index,:) end if
      if dim_pos .eq. 2 then new_fld=field(:,:,index) end if
    else 
      if rk .eq. 2 then
        new_fld=field(:,index)
      end if ;rk eq 2
    end if ; rk eq 3
  end if ; rk eq 4

  ; to print extracted value
  if isint(arg) then
    print("Selecting index "+arg+" for "+arg_name+", i.e. "+arg_name+" = "+field&$dim_field_name$(arg))
  else
    if isfloat(arg) then
      print("Selecting "+arg_name+" close to "+arg+", i.e. "+arg_name+" = "+field&$dim_field_name$(index))
    end if
  end if
  
  if arg_name .eq. "level" then
    select_list=select_list+" "+arg_name+"="+field&$dim_field_name$(index)
  else
    select_list=select_list+" "+arg_name+"="+sprintf("%.2f",field&$dim_field_name$(index)) 
  end if

  return(new_fld)
end

;-----------------------------------------------------------------------------------------------

undef("check_zaxis")
; Check if dimension 'k' of 'field' is a vertical axis
; Remark: same function as 'check_zaxis' of 'gplot.py'
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

;-----------------------------------------------------------------------------------------------

undef("check_lat_axis")
; Check if dimension 'i' of 'field' is a latitude axis, 'lat_tab' is the latitude array 
; and the latitude variable name is 'lat_name'
function check_lat_axis(field:numeric, i:integer, lat_name:string, lat_tab:numeric) 

local vardims, zaxis_exist
begin
  
  vardims = getVarDimNames(field)  ; getting dimensions from metadata
  lat_axis=False
  
  ; check if this dimension is a vertical axis
  zaxis_exist=False
  if check_zaxis(field, i) then
    lat_axis=False
    zaxis_exist=True
  end if
              
  ; if this dimension is not a vertical axis, we check if we have a latitude axis
  if .not. zaxis_exist then  
    if ( isatt(field,"coordinates") .and. (.not. ismissing(str_match(field@coordinates,lat_name))) \
      .and. ( (  isatt(lat_tab,"standard_name") .and. (lat_tab@standard_name .eq. "latitude") ) \ 
           .or. ( isatt(lat_tab,"axis") .and. ((lat_tab@axis .eq. "y") .or. (lat_tab@axis .eq. "Y")) ) ) ) \
      .or. .not. ismissing(str_match(vardims(i),lat_name)) \
      .or. ( iscoord(field,vardims(i)) .and. isatt(field&$vardims(i)$,"standard_name") \
           .and. (field&$vardims(i)$@standard_name .eq. "latitude") ) \
      .or. (  iscoord(field,vardims(i)) .and. isatt(field&$vardims(i)$,"axis") \
           .and. ( (field&$vardims(i)$@axis .eq. "y") .or. (field&$vardims(i)$@axis .eq. "Y") ) ) then
      lat_axis=True
    end if
  end if

  delete(vardims)
  return(lat_axis)

end

;-----------------------------------------------------------------------------------------------

undef("check_lon_axis")
; Check if dimension 'i' of 'field' is a longitude axis, 'lon_tab' is the longitude array
; and the longitude variable name is 'lon_name'
function check_lon_axis(field:numeric, i:integer, lon_name:string, lon_tab:numeric) 

local vardims, zaxis_exist
begin
  
  vardims = getVarDimNames(field)  ; getting dimensions from metadata
  lon_axis=False
  
  ; check if this dimension is a vertical axis
  zaxis_exist=False
  if check_zaxis(field, i) then
    lon_axis=False
    zaxis_exist=True
  end if
              
  ; if this dimension is not a vertical axis, we check if we have a longitude axis
  if .not. zaxis_exist then  
    if ( isatt(field,"coordinates") .and. (.not. ismissing(str_match(field@coordinates,lon_name))) \
      .and. ( (  isatt(lon_tab,"standard_name") .and. (lon_tab@standard_name .eq. "longitude") ) \ 
           .or. ( isatt(lon_tab,"axis") .and. ((lon_tab@axis .eq. "x") .or. (lon_tab@axis .eq. "X")) ) ) ) \
      .or. .not. ismissing(str_match(vardims(i),lon_name)) \
      .or. ( iscoord(field,vardims(i)) .and. isatt(field&$vardims(i)$,"standard_name") \
           .and. (field&$vardims(i)$@standard_name .eq. "longitude") ) \
      .or. (  iscoord(field,vardims(i)) .and. isatt(field&$vardims(i)$,"axis") \
           .and. ( (field&$vardims(i)$@axis .eq. "x") .or. (field&$vardims(i)$@axis .eq. "X") ) ) then
      lon_axis=True
    end if
  end if

  delete(vardims)
  return(lon_axis)

end
   
;-----------------------------------------------------------------------------------------------

undef("data_axavg")
; Computes the average of the variable corresponding to 'mean_axis' for 'field' in file 'ffile' 
; on a given domain ('latS, 'latN', 'lonE', 'lonW'), with 'LatLon' for latitude and longitude names
function data_axavg(ffile, field, mean_axis, latS, latN, lonE, lonW, LatLon)

local Var_DimNames, lat_dim, lon_dim, X, Xmean
begin

  Var_DimNames = getvardims(field)
  lat_dim=ffile->$LatLon(0)$ 
  lon_dim=ffile->$LatLon(1)$ 

  if dimsizes(Var_DimNames) .eq. 3 then

    if (mean_axis .eq. "Lat") then
      if check_zaxis(field,1) then
        ; No reorder: (t,z,y)
        X = field($Var_DimNames(0)$|:,$Var_DimNames(1)$|:,{$LatLon(0)$|latS:latN})
      else if check_lon_axis(field,2,LatLon(1),lon_dim) then
        ; Reorder: (t,y,x) -> (t,x,y)
        field = lonFlip(field)
        X = field($Var_DimNames(0)$|:,{$LatLon(1)$|lonE:lonW},{$LatLon(0)$|latS:latN})
      end if
      end if
    else 
      if (mean_axis .eq. "Lon") then
        ; --> No reorder 
        field = lonFlip(field)
        if check_zaxis(field,1) then
          ; (t,z,x)
          X = field($Var_DimNames(0)$|:,$Var_DimNames(1)$|:,{$LatLon(1)$|lonE:lonW})
        else if check_lon_axis(field,2,LatLon(1),lon_dim) then
          ; (t,y,x)
          X = field($Var_DimNames(0)$|:,{$LatLon(0)$|latS:latN}, {$LatLon(1)$|lonE:lonW})
        end if
        end if

      end if ; mean_axis eq 'Lon'
    end if ; mean_axis eq 'Lat'

    ; compute average of the variable's rightmost dimension 
    Xmean =  dim_avg_Wrap(X)
    return(Xmean)
  end if ; dimsizes

end

;-----------------------------------------------------------------------------------------------

undef("data_reduce")
; Reduce rank of field called 'var' in file 'ffile' on a given domain ('latS, 'latN', 'lonE', 'lonW'), 
; with 'LatLon' for latitude and longitude names, by adapting to various cases, output field is 2D
function data_reduce(ffile, var, latS, latN, lonE, lonW, LatLon, extract_list)

local cr, fld, lat_array, lon_array, tmpfld, vardim, rk, ds, new_fld, tmp, dataONdom
begin

  cr = tochar(10)
  if (getfilevartypes(ffile,var) .eq. "short") then
    fld = short2flt( ffile->$var$ )
  else
    fld = ffile->$var$
  end if
  lat_array=ffile->$LatLon(0)$ 
  lon_array=ffile->$LatLon(1)$ 

  tmpfld= rm_single_dims(fld)
  delete(fld)
  fld=tmpfld
  delete(tmpfld)
  vardim=getvardims(fld)  ; getting dimensions from metadata
  rk=dimsizes(vardim)

  ; Assume dimensions order is anyway t,z,y,x, but that some may be missing 
  ; Checks input data file
  if  (rk .lt. 2) .or. (rk .gt. 4)  then 
    print("This script is not tuned for this rank data for field ( rk ="+rk +")")
    status_exit(1)
  else if ismissing(str_match(vardim(0),"time"))  \
    .and. ( iscoord(fld,vardim(0)) .and. isatt(fld&$vardim(0)$,"standard_name") \
    .and. (fld&$vardim(0)$@standard_name .ne. "time") ) then
    print("Hovmoller diagrams needs time dimension")
    print(vardim)
    status_exit(1)
  end if
  end if
  if (rk .ne. 2) .and. (.not. isvar("mean_axis")) then
    print("You must specify at least argument 'mean_axis' which can be Lat, Lon or Point")
    status_exit(1)
  end if
  if (rk .ne. 2) .and. ( (dimsizes(lat_array) .eq. 1) .or. .not. isvar("lat_array") ) \
    .and. ( isvar("mean_axis") .and. (mean_axis .eq. "Lat") ) then
    print("Error: You want an average on latitude axis but field does not depend on this dimension.")
    status_exit(1)
  end if
  if (rk .ne. 2) .and. ( (dimsizes(lon_array) .eq. 1) .or. .not. isvar("lon_array") ) \
    .and. ( isvar("mean_axis") .and. (mean_axis .eq. "Lon") ) then
    print("Error: You want an average on longitude axis but field does not depend on this dimension.")
    status_exit(1)
  end if

  ; Try to adapt to various cases, using heuristics
  if rk .eq. 4 then
    if mean_axis .eq. "Lat" then
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
      new_fld=data_axavg(ffile, ds, mean_axis, latS, latN, lonE, lonW, LatLon)

    else if mean_axis .eq. "Lon" then
      print("rank= "+rk+"-> mean on x axis")
      if isvar("zpoint") .and. .not.isvar("xpoint") .and. .not.isvar("ypoint") then
        ds=data_select("level", zpoint, fld, vardim(1), extract_list)
      else if isvar("ypoint")  .and. .not.isvar("xpoint") .and. .not.isvar("zpoint") then
        ds=data_select("latitude", ypoint, fld, vardim(2), extract_list)
      else
        print("You must specify zpoint or ypoint"+cr)
        status_exit(1)
      end if
      end if
      new_fld=data_axavg(ffile, ds, mean_axis, latS, latN, lonE, lonW, LatLon)

    else    ; mean_axis= Point
      if isvar("zpoint") .and. isvar("ypoint") .and. isvar("xpoint") then
        print("mean_axis='Point' => you have to select only two points because rank="+rk)
        status_exit(1)
      end if
      print("rank= "+rk+"-> No mean on any axis, mean_axis= "+mean_axis+cr)
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
        ds=data_select("latitude", ypoint, fld, vardim(2), extract_list)
        tmp=data_select("level", zpoint, ds, vardim(1), extract_list)
      else
        print("You must specify two points"+cr)
        status_exit(1)
      end if
      end if

      dimvar=getvardims(tmp)

      if check_lat_axis(tmp,1,LatLon(0),lat_array) then
        new_fld = tmp($dimvar(0)$|:,{$LatLon(0)$|latS:latN})

      else if check_lon_axis(tmp,1,LatLon(1),lon_array) then
        tmp = lonFlip(tmp)
        new_fld = tmp($dimvar(0)$|:,{$LatLon(1)$|lonE:lonW})
      else
        new_fld = tmp
      end if
      end if
      
    end if ; mean_axis eq "Lon" 
    end if ; mean_axis eq "Lat" 
  end if ; rk eq 4

  if rk .eq. 3 then
    if (mean_axis .eq. "Lat") .or. (mean_axis .eq. "Lon") then
      print("rank= "+rk+"-> mean on "+ mean_axis +" axis")
      if isvar("zpoint") .or. isvar("xpoint") .or. isvar("ypoint") then
        print(cr+"Warning: selected points are not considered because rank=3 and a mean on one of axis is done"+cr)
      end if
      new_fld=data_axavg(ffile, fld, mean_axis, latS, latN, lonE, lonW, LatLon)
    else      ; mean_axis= Point
      if ( isvar("zpoint") .and. isvar("ypoint") .and. isvar("xpoint") )\
        .or. (isvar("xpoint") .and. isvar("ypoint" ) ) \
        .or. (isvar("xpoint") .and. isvar("zpoint" ) ) \
        .or. (isvar("zpoint") .and. isvar("ypoint" ) ) \
        .or. ( .not.isvar("zpoint") .and. .not.isvar("ypoint") .and. .not.isvar("xpoint") ) then
        print("mean_axis='Point' => you have to select only one point because rank="+rk)
        status_exit(1)
      end if
      print("rank= "+rk+"-> No mean on any axis, mean_axis= "+mean_axis+cr)

      if isvar("xpoint") \
        .and. check_lon_axis(fld,2,LatLon(1),lon_array) then

        tmp=data_select("longitude", xpoint, fld, vardim(2), extract_list)
      else if isvar("ypoint") then

        if check_lat_axis(fld,1,LatLon(0),lat_array) then
          tmp=data_select("latitude", ypoint, fld, vardim(1), extract_list)
          
        else if check_lat_axis(fld,2,LatLon(0),lat_array) then
          tmp=data_select("latitude", ypoint, fld, vardim(2), extract_list)
        else
          print("The dimension selected is missing.")
          status_exit(1)
        end if
        end if
 
      else if isvar("zpoint") \
        .and. check_zaxis(fld,1) then
        tmp=data_select("level", zpoint, fld, vardim(1), extract_list)
      else
        print("The dimension selected is missing.")
        status_exit(1)
      end if 
      end if
      end if

      dimvar=getvardims(tmp)

      if check_lat_axis(tmp,1,LatLon(0),lat_array) then
        new_fld = tmp($dimvar(0)$|:,{$LatLon(0)$|latS:latN})
      else if check_lon_axis(tmp,1,LatLon(1),lon_array)
        tmp = lonFlip(tmp)
        new_fld = tmp($dimvar(0)$|:,{$LatLon(1)$|lonE:lonW})
      else
        new_fld = tmp
      end if
      end if
    end if ; mean_axis eq "Lat" or "Lon" 
  end if ; rk eq 3

  if rk .eq. 2 then
    if isvar("mean_axis") then 
      print("argument 'mean_axis' is not considered because rank=2 -> plot supplied coordinates"+cr) 
    else
      print("rank= "+rk+"-> plot supplied coordinates")
    end if
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
; Main Program
;-----------------------------------------------------------------------------------------------
begin
  
  setfileoption("nc","MissingToFillValue",False)
  quote = str_get_dq()
  cr = tochar(10)
  carriage = "~C~"       ; A string with a carriage ~C~ return in it
  mean_axis_names=(/"Lat","Lon","Point"/)
  if isvar("mean_axis") .and. ismissing(str_match(mean_axis_names,mean_axis)) then 
    print("argument 'mean_axis' can be only 'Lat', 'Lon' or 'Point' (mean_axis="+mean_axis+")")
    status_exit(1)
  end if

  if (.not.isvar("colormap")) then colormap="amwg256" end if
  if (.not.isvar("reverse")) then reverse=False end if
  if (.not.isvar("myscale")) then myscale=1.0 end if
  if (.not.isvar("myoffset")) then myoffset=0.0 end if
  if (.not.isvar("type")) then type="png" end if
  if (.not. isvar("invXY")) then invXY=False end if
  if (.not.isvar("trim")) then trim=True end if
  ;
  ;---Defining data to plot 
  ;                                            
  if isfilepresent(infile) then
    ffile=addfile(infile,"r")
    
    if isfilevar(ffile,var) then 
      dim_select="" 
      LatLon=LatLon_names(ffile, ffile->$var$)
      if .not. ( isvar("latS") .and. isvar("latN") .and. isvar("lonE") .and. isvar("lonW") ) then
        latS=min(ffile->$LatLon(0)$)
        latN=max(ffile->$LatLon(0)$)
        lonE=max(ffile->$LatLon(1)$)
        lonW=min(ffile->$LatLon(1)$)
      end if
      data_dom = data_reduce(ffile, var, latS, latN, lonE, lonW, LatLon, dim_select)
      Xfld = data_dom[0]*tofloat(myscale)+tofloat(myoffset)
      copy_VarMeta(data_dom[0],Xfld)   ; copy_VarMeta( var_from, var_to) 
      XArray = tofloat(data_dom[1])
      copy_VarMeta(data_dom[1],XArray)
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
      
      if type .eq. "png" then ; image resolution in pixels
        type@wkWidth = width
        type@wkHeight = height
      else 
        if (type .eq. "pdf") .or. (type .eq. "eps") then ; image resolution in inches
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
  gsn_define_colormap(wks,colormap)
  ; reverse colormap
  if (reverse) then gsn_reverse_colormap(wks) end if
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
  ; title and 3 sub-titles
  if (.not. isvar("title")) then
    area = "(Domain: LAT "+latS+":"+latN+", LON "+lonW+":"+lonE+")"
    title =carriage+period+carriage+area+carriage+" "
  end if

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
  res@cnLineLabelFontHeightF  = 0.015  
  res@cnInfoLabelFontHeightF  = 0.01
  ;
  ; Contour
  res@cnFillOn                = True             ; True-> full areas between contour levels
  res@cnLinesOn               = False            ; True-> contour lines
  res@cnLineLabelsOn          = False            ; True-> contour labels
  res@cnMaxLevelCount         = 25               ; default is 16
  ;
  ;--- Smoothing colors
  res@cnRasterSmoothingOn     = True
  res@cnFillOpacityF          = 0.6              ; color contours are partially transparent
  ;res@pmLabelBarOrthogonalPosF = -.001          ; move label bar closer
  res@lbLabelFont = "helvetica"
  res@lbLabelFontHeightF = .02
  ;
  ; Y and X axis 
  if invXY then
    if check_zaxis(Xfld,1) then ; z on y-axis
      res@gsnYAxisIrregular2Log = True       ; set y-axis to log scale
    else ; lat or lon on y-axis
      res@tiYAxisString = XAxisString 
      res@tmYMajorGrid = True
      res@tmYMajorGridThicknessF = 0.5
      res@tmYMinorGrid = True
      res@tmYMinorGridThicknessF = 0.25
    end if
    ; time on x-axis
    res@tiXAxisString = "Time"             
    res@tmXMajorGrid = True
    res@tmXMajorGridThicknessF= 0.5
    res@tmXMinorGrid = False
    res@tmXMinorGridThicknessF= 0.25
  else
    if check_zaxis(Xfld,1) then ; z on x-axis
      res@gsnXAxisIrregular2Log = True       ; set x-axis to log scale
    else ; lat or lon on x-axis
      res@tiXAxisString = XAxisString 
      res@tmXMajorGrid = True
      res@tmXMajorGridThicknessF = 0.5
      res@tmXMinorGrid = True
      res@tmXMinorGridThicknessF = 0.25
    end if
    ; time on y-axis
    res@tiYAxisString = "Time"               
    res@tmYMajorGrid = True
    res@tmYMajorGridThicknessF= 0.5
    res@tmYMinorGrid = False
    res@tmYMinorGridThicknessF= 0.25
  end if
  ;
  ; Set special resources for the time axis
  resTickY = True
  if .not. invXY then resTickY@ttmAxis = "YL" end if  ; Y left axis, "XB" by default
  if (isvar("fmt")) then
    resTickY@ttmFormat=fmt
  else
    resTickY@ttmMajorStride = 12                      ; Number of timesteps desired between major tickmarks. 
    resTickY@ttmFormat      = "%Y"                    ; 4-digit year
  end if
  time_axis_labels( time,  res, resTickY )
  ;
  Xfeatures = nice_mnmxintvl(min(XArray), max(XArray), 4, False)
  Xmin = floattointeger(Xfeatures(0))
  Xmax = floattointeger(Xfeatures(1))
  XlevelSpacing = floattointeger(Xfeatures(2))
  if invXY then
    res@tmYLLabelFontHeightF  = 0.018
    res@tmXBLabelFontHeightF  = 0.02
    res@tmYLTickSpacingF      = XlevelSpacing
  else
    res@tmXBLabelFontHeightF  = 0.018
    res@tmYLLabelFontHeightF  = 0.02
    res@tmXBTickSpacingF      = XlevelSpacing
  end if
  ;
  ;---Set some "nice" contour levels
  mnmxint = nice_mnmxintvl(min(Xfld(:,:)), max(Xfld(:,:)), 21, False)
  if (mnmxint(0).lt.0) then 
    symMinMaxPlt(Xfld, 14, False, res)           
  else
    res@cnLevelSelectionMode  = "ManualLevels"
    res@cnMinLevelValF  = mnmxint(0)
    res@cnMaxLevelValF  = mnmxint(1)
    res@cnLevelSpacingF = mnmxint(2)/2.          ; twice as many
  end if
 
  print("Plotted axis:")
  print(getvardims(Xfld))
  if isvar("options") then res_list(options, res) end if 
 
  if invXY then
    if .not. any(ismissing(var_att)) then  
      tr_Xfld=Xfld($var_att(1)$|:,$var_att(0)$|:)
      delete(Xfld)
      Xfld=tr_Xfld
      delete(tr_Xfld)
    else
      print("Field contains missing dimension names for the given variable " \
      + "so 'invXY' will not invert X and Y axis")
    end if
  end if

  plot = gsn_csm_hov(wks, Xfld, res) 

  if ( type .eq. "png" .and. trim ) then
    system("convert "+plotname+" -trim "+plotname)
  end if
  
  status_exit(0)
  
end