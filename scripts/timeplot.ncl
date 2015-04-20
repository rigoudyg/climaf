; Plotting a time series from a NetCDF file. SSelect the varibale form argument 'var'. 
; Check that dimensions other than time are de-generated. 

; call it as 
; ncl plot1d.ncl infile=.. outfile=.. var=.. title=.. 

; First version : S.Sénési - april 2015

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"

begin
  type="png"
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

  ; select the time series as a 1D array, by analyzing the dimensions 
  ; and checking that dimensions other than 'time' are degenerated
  Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
  dime=dimsizes(fld)
  rank=dimsizes(dime)
  do i=0,rank-1
    print("analyzing "+Var_DimNames(i))
    if Var_DimNames(i) .eq. "time" then
      timedimnum=i
    else
      if dime(i) .gt. 1 then
        print("dimension "+Var_DimNames(i)+" is not a singleton")
        status_exit(2)
      end if
    end if
  end do

  ; A bit heavy style, but I am not expert enough with NCL scripting language ... : 
  if rank .eq. 1 then
    series=fld
  else 
    if rank .eq. 2 then
      if (timedimnum .eq. 0) then 
        series=fld(:,0)
      else
        series=fld(0,:)
      end if
    else 
      if rank .eq. 3 then
        if (timedimnum .eq. 0) then 
          series=fld(:,0,0)
        else
          if (timedimnum .eq. 1) then 
            series=fld(0,:,0)
          else
            series=fld(0,0,:)
          end if
        end if
      else
        print("Cannot process more than 3 dimensions yet")
        status_exit(1)
      end if
    end if
  end if
    


  ; Just plot
  wks   = gsn_open_wks (type,outfile)             ; open workstation
  res                  = True                     ; plot mods desired
  res@tiMainString     = title                    ; add title

 plot  = gsn_csm_xy (wks,fld&time,series,res) ; create plot
end
