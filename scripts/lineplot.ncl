; Plotting any series of data vectors from A SERIES of NetCDF file, 
; for the same variable (indicated by arg "var")

; Check on first file that only one dimension is not a singleton.

; Do not assume that all datasets have the same dimensions set

; But assume that all data vectors have the same size and coordinate
;   array (take the first one as ref.)

; Usage:
;;;;;;;;;;
; ncl lineplot.ncl infile=.. plotname=.. var=.. title=.. labels=.. colors=.. thickness=.. linp=1

; infile, plotname and var are mandatory
; infile : a string holding the series of filenames, separated by whitespaces
; colors : a string holding a series of color NCL names, separated by whitespaces
; thickness : the common thickness (defaults to 2.0)
; If argument linp=1 and data is a vertical profile, do not plot it in log(p) 

; First version : S.Sénési - may 2015

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl" ;LV

begin
  files=str_split(infile," ")
  n=dimsizes(files)
  if .not. all(isfilepresent(files)) then
    print("Some file cannot be accessed")
    status_exit(2)
  end if
  ;
  
  ;LV
  filesLV=addfiles(files,"r")
  print(filesLV)
  
  fldLV=filesLV[:]->$var$
  print(fldLV)
  
  tmpLV=new(n,integer)
 
  Var_DimNamesLV = getvardims(fldLV)  ; getting dimensions from metadata
  dime=dimsizes(fldLV)

  print(dime)
  coordLV=Var_DimNamesLV(0)
  timeLV=fldLV&$coordLV$

  print(timeLV)
  print(coordLV)
  timeLV_ut=cd_calendar(timeLV,3)
  timeLVmin=min(timeLV_ut)
  timeLVmax=max(timeLV_ut)

  print(timeLVmin)
  print(timeLVmax)
  do i=0, n-1 
    fld = filesLV[i]->$var$
    print(filesLV[i])
    dime=dimsizes(fld)
    print(dime)
    do dim=0,dimsizes(dime)-1
      if dime(dim) .gt. 1 then
        tmpLV(i)=dime(dim)
      end if
    end do
  end do
  print(tmpLV)
  maxLV=max(tmpLV)
  vec=new((/n,maxLV/),float)
  print("ICI"+maxLV)
  ;ax=new(n,float)
  tab=new((/n,maxLV/),double)

  do i=0, n-1 

    ; Read variable
    ffile=addfile(files(i),"r") ;ffile=filesLV(i) [i] a voir
    if isfilevar(ffile,var) then 
      fld = ffile->$var$
    else
      print("File "+infile+" does not include variable "+var)
      status_exit(1)
    end if

     ; Search and extract relevant vector
    Var_DimNames = getvardims(fld)  ; getting dimensions from metadata
    dime=dimsizes(fld)
    rank=dimsizes(dime)
    found=False
    coord=""
   
    do dim=0,rank-1
      ;print("analyzing "+Var_DimNames(dim))
      if dime(dim) .gt. 1 then 
        if found then
          print("There is more than one non-singleton dim for file "+f+ " :"+coord+ Var_DimNames(dim))
          status_exit(1)
        end if 
        found=True
        
        ;LV
        ;tmpLV(i)=dime(dim)

        ; if processing first line/file : allocate multi-line array, and store coordinate array in 'ax'
        ;tmp comment
        ;if (i .eq. 0 ) then 
        ;  vec=new((/n,dime(dim)/),float)
          ;coord=Var_DimNames(dim)
          ;ax=fld&$coord$
	  
	;  ;choix 1: affiche 198100 au 1er tick => decaler l affichage
	;  ;au 2eme tick ou changer de solution
	;  testlv=cd_calendar(ax,1) ;YYYYMM - opt=2 <=> YYYYMMDD
	;  print(testlv)
	  
        ;end if
        ;printVarSummary(fld)
        ;printVarSummary(ndtooned(fld))
        ;printVarSummary(vec)
        ;vec(i,:)=ndtooned(fld);avant
        coord=Var_DimNames(dim)
        ax=fld&$coord$
        tab(i,:)=ax
        vec(i,0:dime(dim)-1)=ndtooned(fld) ;LV
      end if
    end do ; loop on dimensions

    if .not. found then 
      print("There is no non-sigleton dim for file "+f)
      status_exit(1)
    end if 
    
  end do ; loop on files  
  
  print("tmpLV"+tmpLV)
  print(tab)

  res=True

  ;res@gsnDraw          = False ;LV
  ;res@gsnFrame         = False ;LV
  ;res@trXMinF= min(timeLV_ut) non pb
  ;res@trXMaxF=max(timeLV_ut)

  if isvar("thickness") then 
    res@xyLineThicknessF       = thickness 
  else
    res@xyLineThicknessF       = 2.0      ; default is 1
  end if
  res@xyMonoDashPattern      = True     ; force all solid lines
  
  colornames=new(n, string)
  stdcolors=(/"black","red","blue","yellow","green","orange","purple","violet","grey"/)
  do i=0,n-1 colornames(i)=stdcolors(i) end do
  if isvar("colors") then 
    tab=str_split(colors," ")
    do i=0,dimsizes(tab)-1 
      colornames(i)=tab(i) 
    end do
  end if 
  res@xyLineColors=colornames
  
  if .not. isvar("title") then title="title" end if
  res@tiMainString     = title                    ; add title
  
;---Resources for legend
  res@pmLegendDisplayMode    = "Always"              ; turn on legend
  res@pmLegendWidthF         = 0.12                  ; Change width and
  res@pmLegendHeightF        = 0.15                  ; height of legend.
  ;res@pmLegendOrthogonalPosF = -0.08                 ; move up slightly 
  res@lgLabelFontHeightF     = .011                  ; change font height
  res@lgPerimOn              = True                 ; no box around
  ;res@lgItemOrder            = (/1,0/)               ; reverse legend
  if ( isvar("labels")) then 
    res@xyExplicitLegendLabels=str_split(labels,"$")
  end if

  logp=True
  if (isvar("linp")) then if linp .eq. 1 then logp=False end if end if

  res@vpWidthF    = 0.7        ; Make plots wider
  res@vpHeightF   = 0.5

  ;LV choix 1
  ;res@trXMinF=testlv(0)
  
  res@tmXBMode        = "Manual"	
;  res@tmXBTickStartF  = 
;  res@tmXBTickEndF    = 2005
  res@tmXBTickSpacingF= 1.

;  res@tmXBMode        = "Explicit"	
;  res@tmXBValues      = (/1950,1960,1970,1980,1990,2000,2005/)
;  res@tmXBLabels      = "" + res@tmXBValues 
;  res@tmXBMinorValues = ispan(1949,2006,1)

  ;time axis labels LV choix 2
  restick = True
  restick@ttmFormat="%c" ;"%N/%Y" ; ou %c %Y pour le mois abrege puis l annee
  ;restick@ttmValues
  ;restick@ttmNumTicks=2
  restick@ttmMajorStride=1 ;nbre de pas de temps (ex: mois ici) entre lesquels il y a un label 
  ;restick@ttmMinorStride=0
  ;time_axis_labels(ax,res,restick)
  time_axis_labels(tab(0,:),res,restick)
  ; Just plot
  wks   = gsn_open_wks ("png",plotname)             ; open workstation
  
  ;
  tabtest1=tab(0,:)
  tabtest2=tab(1,:)

  vectest1=vec(0,:)
  vectest2=vec(1,:)

  if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
    if (ax@positive .eq. "down") then 
      res@trYReverse = True ; reverse Y-axis
    end if
    if logp then 
      res@xyYStyle = "Log" 
      set_pres_hgt_axes(ax,res,True)
    end if
    plot = gsn_csm_xy(wks,vec,ax,res)
  else
    ;plot = gsn_csm_xy (wks,ax,vec,res) ; create plot 
    ;plot = gsn_csm_xy (wks,ax,vec,res) ; create plot choix 2 (unchanged)
    ;plot = gsn_csm_xy (wks,testlv,vec,res) ; create plot choix 1

    ;plot = gsn_csm_xy (wks,ax,vec(1,:),res)
    plot = gsn_csm_xy (wks,tab(0,:),vec,res) ;ok
    ;plot = gsn_csm_xy (wks,tab(0,:),vec(0,:),res)
    ;plot = gsn_csm_xy (wks,tabtest1,vectest1,res)
  end if
  
  print(vec(0,:))
  print(tab(0,:))
  ;plot2 = gsn_csm_xy (wks,tab(1,:),vec(1,:),res)
  ;plot2 = gsn_csm_xy (wks,tabtest2,vectest2,res)
  ;overlay(plot,plot2)
  ;draw(plot)
  ;frame(wks)

 ;ou
	  ;testlv=cd_calendar(ax,0) ;return array dimsizes(time)x6
	  ;year=tointeger(testlv(:,0)) ;tointeger utile pr utiliser sprinti
	  ;month=tointeger(testlv(:,1))
	  ;day=tointeger(testlv(:,2))
	  ;hour=tointeger(testlv(:,3))
	  ;mn=tointeger(testlv(:,4))
	  ;sec=testlv(:,5)
	  ;print("year"+year+"month"+month+"day"+day+"hour"+hour+"mn"+mn+"sec"+sec)
                                               
	  ;time_test=(/2207, 2237, 2267, 2297, 2328, 2358, 2389, 2420, \
	  ;2450, 2481, 2511, 2542/)
	  ;time_test@units="days since 1975-01-01 00:00:00"
	  ;utc_date=cd_calendar(time_test, 0)
	  ;year=utc_date(:,0)
	  ;month=utc_date(:,1)	  
	  ;day=utc_date(:,2)
	  ;hour=utc_date(:,3)
	  ;mn=utc_date(:,4)
	  ;sec=utc_date(:,5)
	  ;print("year"+year+"month"+month+"day"+day+"hour"+hour+"mn"+mn+"sec"+sec)
	  ;ou	  
	  ;year:=tointeger(utc_date(:,0)) 	
	  ;month:=tointeger(utc_date(:,1))
	  ;day:=tointeger(utc_date(:,2))    
	  ;date_str=sprinti("%0.4i ",year) + sprinti("%0.2i ",month) + sprinti("%0.2i ",day)  
	  ;print(date_str)     
	  ;ou YYYYMMDD
	  ;utc_date:=cd_calendar(time_test, 2) 
	  ;print(utc_date)                     

end



