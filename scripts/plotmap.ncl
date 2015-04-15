 ; Basic map plot using NCL, for use in CliMAF. 
; Derived from CAMI's plot_map_atmo.ncl
;
; Should be declared to CliMAF as :
;   script('plotmap', "ncl plotmap.ncl infile=${in} plotname=${out} cmap=${color} vmin=${min} vmax=${max} vdelta=${delta} var=${var} title=${crs} scale=${scale} offset=${offset} units=${units}",format="png")
;
; and called through CliMAF as e.g :
;   plotmap(some_dataset, color="DarkBlue", min=0.0, max=50.0, delta=5.)
;
; or called directly as in :
;   ncl plotmap.ncl infile=\"$f\" outfile=\"es.png\" cmap=\"BlueDarkRed18\" vmin=260 vmax=300 vdelta=4 plotname=\"plotname\" var=\"tas\" title=\"some_title\ scale=1. offset=0. units=\"unit\""

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

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
  print("plotting map "+plotname+" from :"+vmin+" to: "+vmax+" by: "+vdelta+" with cmap: "+cmap  )

  type="png"
  LINEON=False
  LABELON=False
  RASTER=True 
  plotOn="global"
  
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
  Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
  dime=dimsizes(fld)
  rank=dimsizes(dime)
  if (rank.gt.3) then
    print("This script is not tuned for high rank data ("+rank+")")
    print(Var_DimNames)
    status_exit(1)
  end if
  if ( rank .eq. 3) then
    ; use first time-step only
    fldtmp=fld(0,:,:)
    delete(fld)
    delete(Var_DimNames)
    delete(dime)
    fld=fldtmp
    Var_DimNames = getVarDimNames(fld)  ; getting dimensions from metadata
    dime=dimsizes(fld)
    rank=dimsizes(dime)
    end if

  ; we now have a 1 or 2d field
  if (rank.gt.1) then
    REDU=False 
    CURVI=False
    latname = Var_DimNames(0)
    lonname = Var_DimNames(1)
    if (ismissing(str_index_of_substr(latname,"lat",-1))) then
      CURVI=True
      ; search for the variables providing lat and lon
      latname="lat"
      lonname="lon"
      if isfilevar(ffile,"nav_lat") then
        latname="nav_lat"
        lonname="nav_lon"
      end if
    end if
    lat=ffile->$latname$
    lon=ffile->$lonname$
  else

    print("This script is not yet tuned to the reduced grid of "+infile)
    status_exit(1)

    nlat=1 
    nlon=dime(0)
    lonname = Var_DimNames(0)
    REDU=True 
    lat=ffile->$latname$(:)
    lon=ffile->$lonname$(:)  
  end if

  units=units
  fld=fld*scale+offset
  
  power10=floattoint(log10(dim_max(ndtooned(fld))))
  if power10.ge.4 then
    fld=fld/10^power10
    vmin=vmin/10^power10
    vmax=vmax/10^power10
    vdelta=vdelta/10^power10
  end if

  if type.eq."png" then
    type@wkWidth= 1200
    type@wkHeight=1200 
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
  res@gsnRightString    = ""
  res@gsnCenterString   = ""

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ContourPlot resources
  res@cnFillOn=True 
  res@cnLevelSelectionMode = "ManualLevels" 
  res@cnMinLevelValF = vmin
  res@cnMaxLevelValF = vmax
  res@cnLevelSpacingF = vdelta

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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; MapPlot resources
  print("lonmin=")
  print(min(lon))
  res@mpMinLonF                = min(lon)
  res@mpMaxLonF                = max(lon)
  res@mpMinLatF                = min(lat)
  res@mpMaxLatF                = max(lat)
  res@mpCenterLonF=(min(lon)+max(lon))/2

  res@mpFillOn=True
  res@mpFillColors    = (/-1,-1,-1,-1/)
  res@mpPerimOn = False
  res@mpGeophysicalLineThicknessF = 2

  if (plotOn .eq. "ocean") then
    res@mpLandFillColor="grey"
    res@mpFillDrawOrder="PostDraw"
  else 
    if (plotOn .eq. "land") then
      res@mpFillOn=True
      res@mpLandFillColor=-1
      res@mpInlandWaterFillColor = -1 
      res@mpOceanFillColor="grey"
      res@mpFillDrawOrder="PostDraw"
    end if
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
  
  res@tmYLLabelFontHeightF = 0.008
  res@tmXBLabelFontHeightF = 0.008
  
  if type.eq."png" then
    res@lbTitleFontThicknessF= 3.0
    res@lbLabelFontThicknessF= 3.0
    res@tmYLLabelFontThicknessF=2.0
    res@tmXBLabelFontThicknessF=2.0
  end if
  
  res@tiMainFont=22 
  res@tiMainFontHeightF  = .015       
  
  ; Viewport resources
  res@vpWidthF  = 0.7
  res@vpHeightF = 0.8
  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  res@tiMainString       = title
  res@vpXF      = 0.1
  res@vpYF      = 0.96
  if (CURVI) then
    res@trGridType          = "TriangularMesh"
    res@sfXArray            = lon
    res@sfYArray            = lat
    ; Pour REDU ?:
    res@gsnAddCyclic        = False
    ;res@gsnZonalMean = False
  end if  
  plot0=gsn_csm_contour_map_ce(wks,fld(:,:),res)
  draw(plot0)
  
  frame(wks)
  status_exit(0)
  
end
