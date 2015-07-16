; Plotting any series of data vectors from A SERIES of NetCDF file, 
; for the same variable (indicated by arg "var")

; Check on first file that only one dimension is not a singleton.

; Do not assume that all datasets have the same dimensions set

; But assume that all data vectors have the same size and coordinate
;   array (take the first one as ref.)

; Usage:
;;;;;;;;;;
; ncl lineplot.ncl infile=.. plotname=.. var=.. title=.. labels=.. colors=.. thickness=.. linp=1 realXaxis=1 fmt=...

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
  ;read data
  filesLV=addfiles(files,"r")

  ; just for extraction of min and max x-range (so for case where realXaxis is on)
  fldLV=filesLV[:]->$var$
  print(fldLV)

  Var_DimNamesLV = getvardims(fldLV)  ; getting dimensions from metadata
  dime=dimsizes(fldLV)
  coordLV=""
  do dim=0,dimsizes(dime)-1
    if dime(dim) .gt. 1 then
      coordLV=Var_DimNamesLV(dim)
      print(coordLV)
      ;inutile (addfiles convertit si les unites en temps sont differentes)
      ;if (all(filesLV[:]&$coordLV$@standard_name .eq. "time")) then  
        ;  print("tous les axes des x sont des temps")
        ;  fldLV&$coordLV$ = cd_convert(fldLV&$coordLV$, filesLV[0]->$var$&$coordLV$@units)

      if (.not. all(filesLV[:]&$coordLV$@standard_name .eq. "time")) then
        first_file_axis_name=filesLV[0]->$var$&$coordLV$@standard_name
        ;si on ne met pas ce test, il fixe les attribut du 1er file a ts les autres
        if (.not. all(filesLV[:]&$coordLV$@standard_name .eq. first_file_axis_name)) then
          print("Files have not same axis (different 'standard_name') for variable "+coordLV)
          status_exit(1)
        end if        
      end if
     
      ;tester si l option realXaxis is on
      if realXaxis .eq. 1 then
        all_Xaxis=fldLV&$coordLV$
      end if
      
    end if
  end do

   ; else
   ;   print("You must provide argument 'realXaxis'")
    ;end if
  ;end if

  res=True
  res@gsnDraw          = False 
  res@gsnFrame         = False 

  ;tester si l option realXaxis is on
  if realXaxis .eq. 1 then
    res@trXMinF=min(all_Xaxis); 1800 
    res@trXMaxF=max(all_Xaxis);2600
  end if

  res@trYMinF=min(fldLV) 
  res@trYMaxF=max(fldLV)
  
  ;les options suivantes n ont pas d impact pr le moment - a tester legend //overlay_7.ncl & xy_32.ncl (plus semblable)
  ;si ds les arguments, le titre est apres l argument realXaxis, les thicks posent un pb... a voir
  ; voir aussi pour l axe des y car les courbes ne sont pas completement contenues dans le plot alors qu avant, c etait le cas et il n y avait pas de min/max pr y. Voir ce qui a change.

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
 
  if .not. isvar("title") then title="title" end if
  res@tiMainString     = title                    ; add title
  
  ;---Resources for legend
  res@pmLegendDisplayMode    = "Always"              ; turn on legend
  res@pmLegendWidthF         = 0.12                  ; Change width and
  res@pmLegendHeightF        = 0.15                  ; height of legend.
  ;res@pmLegendOrthogonalPosF = -0.08                 ; move up slightly 
  res@lgLabelFontHeightF     = .011                  ; change font height
  res@lgPerimOn              = False                ; no box around
  ;res@lgItemOrder            = (/1,0/)               ; reverse legend

  ;ne fonctionne pas car il faut les mettre avant chaque trace de courbe, juste apres xyLineColors => creation de tab_labels: ok mais les positions sont pas encore au point
 
  if ( isvar("labels")) then
    tab_labels=str_split(labels,"$")
  end if

  logp=True
  if (isvar("linp")) then if linp .eq. 1 then logp=False end if end if

  res@vpWidthF    = 0.7        ; Make plots wider
  res@vpHeightF   = 0.5
  
  ;fin des options a tester
  
  restick = True
  ;restick@ttmFormat="%N/%y" ; ou %c %Y pour le mois abrege puis l annee
  ;;restick@ttmValues
  ;;restick@ttmNumTicks=2
  ;restick@ttmMajorStride=1 ;nbre de pas de temps (ex: mois ici) entre lesquels il y a un label 
  ;;restick@ttmMinorStride=0
  if realXaxis .eq. 1 then
    ;rajouter un argument pour le formatage
    if ( isvar("fmt")) then
      print(fmt)
      restick@ttmFormat=fmt  
    else
      ymdhms0 = cd_calendar(all_Xaxis,0)
      ;testlv=cd_calendar(ax,1) ;YYYYMM - opt=2 <=> YYYYMMDD
      ymdhms0dim = dimsizes(ymdhms0)
      nt = ymdhms0dim(0)
      print(ymdhms0)
      print(ymdhms0dim)
      print(nt)
      if ymdhms0(nt-1,0) .ne. ymdhms0(0,0) then ;year changes
        print(abs(ymdhms0(nt-1,0)-ymdhms0(0,0)))
        if (abs(ymdhms0(nt-1,0)-ymdhms0(0,0)) .lt. 1) then
          restick@ttmFormat="%c";"%N/%y" 
        else
          restick@ttmFormat="%N/%y" 
        end if
      else  ;same year
        if ymdhms0(nt-1,1) .ne. ymdhms0(0,1) then ; month changes
          restick@ttmFormat="%c/%y" 
        end if
      end if

      ;restick@ttmFormat="%N/%y" ;par defaut
    end if

    restick@ttmMajorStride=4
    time_axis_labels(all_Xaxis,res,restick) ;plot doit etre apres...et res doit etre deja defini...
  else
    restick@ttmFormat="%c" ;par defaut
    restick@ttmMajorStride=1 
    time_axis_labels(filesLV[0]->$var$&$coordLV$,res,restick) 
    print(filesLV[0]->$var$&$coordLV$)
  end if
 
  wks = gsn_open_wks ("png",plotname)             ; open workstation

  do i=0, n-1 

    ; Read variable
    ;ffile=addfile(files(i),"r") ;ffile=filesLV(i) [i] a voir
    ffile=filesLV[i]
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
      
        ;printVarSummary(fld)
        print(i)
        
        coord:=Var_DimNames(dim)
        print(coord)
        ;ici tester si l option axisXreal is on
        if realXaxis .eq. 1 then
          ax:=fld&$coord$
        else
          ;si non prendre l axe des temps du 1er file
          ; if processing first line/file : store coordinate in 'ax'
          if (i .eq. 0 ) then 
            ax=fld&$coord$
          end if
        end if
        ;create plot
        res@xyLineColor = colornames(i)
        res@xyExplicitLegendLabels = tab_labels(i)
        if (i .eq. 0 ) then 
          print(ax)
          print(fld)
          res@pmLegendParallelPosF   = 0.5;0.15
          res@pmLegendOrthogonalPosF = -0.1    
          if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
            if (ax@positive .eq. "down") then 
              res@trYReverse = True ; reverse Y-axis
            end if
            if logp then 
              res@xyYStyle = "Log" 
              set_pres_hgt_axes(ax,res,True)
            end if
            plot = gsn_csm_xy(wks,ndtooned(fld),ax,res)
          else
            
            plot = gsn_csm_xy(wks,ax,ndtooned(fld),res)
          
          end if

        else
          print(ax)
          print(fld)
          res@pmLegendParallelPosF   = 0.85;0.5;0.15 ;0.81
          res@pmLegendOrthogonalPosF = -0.1;tmp: 0.
          
          ;ici iterer iter_lg
          ; si >4 changer res@pmLegendParallelPosF a 0.15 + ..*i

          if (isatt(ax,"axis") .and. (ax@axis .eq. "Z")) then
            if (ax@positive .eq. "down") then 
              res@trYReverse = True ; reverse Y-axis
            end if
            if logp then 
              res@xyYStyle = "Log" 
              set_pres_hgt_axes(ax,res,True)
            end if
            over = gsn_csm_xy(wks,ndtooned(fld),ax,res)
          else

            over = gsn_csm_xy(wks,ax,ndtooned(fld),res)

          end if

          overlay(plot,over)
        end if
       
      end if
    end do ; loop on dimensions

    if .not. found then 
      print("There is no non-sigleton dim for file "+f)
      status_exit(1)
    end if 
    
  end do ; loop on files  



  draw(plot)
  frame(wks)

  ;-------------
  ;testlv=cd_calendar(ax,0) ;return array dimsizes(time)x6
  ;year=tointeger(testlv(:,0)) ;tointeger utile pr utiliser sprinti
  ;month=tointeger(testlv(:,1))
  ;day=tointeger(testlv(:,2))
  ;hour=tointeger(testlv(:,3))
  ;mn=tointeger(testlv(:,4))
  ;sec=testlv(:,5)
  ;print("year"+year+"month"+month+"day"+day+"hour"+hour+"mn"+mn+"sec"+sec)

  ;res@tmXBMode        = "Manual"	
  ;;res@tmXBTickStartF  = 
  ;;res@tmXBTickEndF    = 2005
  ;res@tmXBTickSpacingF= 1.

  ;;res@tmXBMode        = "Explicit"	
  ;;res@tmXBValues      = (/1950,1960,1970,1980,1990,2000,2005/)
  ;;res@tmXBLabels      = "" + res@tmXBValues 
  ;;res@tmXBMinorValues = ispan(1949,2006,1)

end



