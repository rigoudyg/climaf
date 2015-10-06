;Step 1. Load the necessary NCL scripts
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;
;
; FONCTION AUXILIAIRE.
;
function cl_recouvrement(field,psg)
local ntot,jpj2m,ll1,ll2,dimse,dimll1,dimll2,l1tmp,l2tmp,l3tmp,l4tmp
begin
 dimse=dimsizes(field)
 ntot=dimse(2)
 jpj2m=ntot/2
 ll1=field(0,dimse(1)-1-1,:)
 ll2=field(0,dimse(1)-1-1,:)
 dimll1=dimsizes(ll1)
 dimll2=dimsizes(ll2)
 l2tmp=ll2(jpj2m-1:dimll2-1-1)
 l1tmp=ll1(jpj2m-1:dimll1-1-1)
 l3tmp=ll2(0:jpj2m-1)
 l4tmp=ll1(0:jpj2m-1)
 field(0,dimse(1)-1-1,:jpj2m-1)=psg*l2tmp(::-1)
 field(0,dimse(1)-2-1,:jpj2m-1)=psg*l1tmp(::-1)
 field(0,dimse(1)-1-1,jpj2m:)=psg*l3tmp(::-1)
 field(0,dimse(1)-2-1,jpj2m:)=psg*l4tmp(::-1)
 return(field)
;#
end
;
; ===========================================================
;
begin
  ; ========================================================
  conf="ORCA1"
  if conf.eq."ORCA12" then
   repfile="/dataref/rd/INITIALISATION/ORCA12/T321/ORCA12-T321.mesh_hgr.nc"
   nx=3059
   ny=4322
  else
  if conf.eq."ORCA025" then
   repfile="/dataref/rd/INITIALISATION/ORCA025_LIM/ORCA025_LIM-T322/ORCA025_LIM-T322_mesh_hgr.nc"
   nx=1021
   ny=1442
  end if
  end if
  if conf.eq."ORCA1" then
   repfile="/cnrm/aster/data1/UTILS/CDAT5/Data/mesh_mask_NEMO1.2.nc"
   nx=292
   ny=362
  end if 
  ;  
  ;fmesh= addfile("/sxaster1/data1/UTILS/CDAT5/Data/mesh_mask_NEMO1.2.nc","r")
  fmesh= addfile(repfile,"r")
  glamf = fmesh->glamf
  ;printVarSummary(glamf)
  ;ax=glamf&x
  ;at=glamf&t
  ;ay=glamf&y
  ;print(top)
  gphif = fmesh->gphif
  glamu = fmesh->glamu
  glamv = fmesh->glamv
  gphiu = fmesh->gphiu
  gphiv = fmesh->gphiv
  ;
  print("Champs charges... en avant!")
  ;
  ; Les champs sont sur la grille du modele.
  ; On les tourne.
  ; Ces operations sont extraites de rot_rep (NEMO).
  ;
  pi=4*atan(1)
  rad=pi/180.
  ;
  ;(xnpu,ynpu,nnpu) = np_dir_mod(glamu,gphiu)
  ; 
  glamu0=glamu(0,:,:)
  gphiu0=gphiu(0,:,:)
  xnpu = 0. - 2.*cos(rad*glamu0)*tan(pi/4 - rad*gphiu0/2)
  ynpu = 0. - 2.*sin(rad*glamu0)*tan(pi/4 - rad*gphiu0/2)
  nnpu = xnpu*xnpu + ynpu*ynpu
  ;
  ;(xnpv,ynpv,nnpv) = np_dir_mod(glamv,gphiv)
  ;
  glamv0=glamv(0,:,:)
  gphiv0=gphiv(0,:,:)
  xnpv = 0. - 2.*cos(rad*glamv0)*tan(pi/4 - rad*gphiv0/2)
  ynpv = 0. - 2.*sin(rad*glamv0)*tan(pi/4 - rad*gphiv0/2)
  nnpv = xnpv*xnpv + ynpv*ynpv
  ;
  ;(xffu,yffu,nffu) = dir_func(glamf,gphif,nnpu,0,1)
  ; 
  ;
  ;delete(dime)
  dime=dimsizes(glamf)
  xffu=new((/dime(1),dime(2)/),float,-9999.)
  yffu=new((/dime(1),dime(2)/),float,-9999.)
  nffu=new((/dime(1),dime(2)/),float,-9999.)
  glam=glamf(0,1:,   :)
  glan=glamf(0,0:dime(1)-1-1,:)
  gphi=gphif(0,1:,   :)
  gphh=gphif(0,0:dime(1)-1-1,:)
  xffu(1:,:) = 2.*cos(rad*glam)*tan(pi/4 - rad*gphi/2) \
		- 2.*cos(rad*glan)*tan(pi/4 - rad*gphh/2)
  yffu(1:,:) = 2.*sin(rad*glam)*tan(pi/4 - rad*gphi/2) \
		- 2.*sin(rad*glan)*tan(pi/4 - rad*gphh/2)
  nffu = sqrt(nnpu * (xffu*xffu + yffu*yffu))
  nffu=where(nffu.le.1e-14,1e-14,nffu)
  ;
  ; (xffv,yffv,nffv) = dir_func(glamf,gphif,nnpv,1,0)
  ;
  delete(glam)
  delete(glan)
  delete(gphi)
  delete(gphh)
  glam=glamf(0,:,   1:)
  glan=glamf(0,:,0:dime(2)-1-1)
  gphi=gphif(0,:,   1:)
  gphh=gphif(0,:,0:dime(2)-1-1)
  ;
  xffv=new((/dime(1),dime(2)/),float,-9999.)
  yffv=new((/dime(1),dime(2)/),float,-9999.)
  nffv=new((/dime(1),dime(2)/),float,-9999.)
  xffv(:,1:) = 2.*cos(rad*glam)*tan(pi/4 - rad*gphi/2) \
		- 2.*cos(rad*glan)*tan(pi/4 - rad*gphh/2)
  yffv(:,1:) = 2.*sin(rad*glam)*tan(pi/4 - rad*gphi/2) \
		- 2.*sin(rad*glan)*tan(pi/4 - rad*gphh/2)
  ;
  nffv = sqrt(nnpv * (xffv*xffv + yffv*yffv))
  nffv=where(nffv.le.1e-14,1e-14,nffv)
  ;
  ;# cosinus and sinus using scalar and vectorial products
  gsinu = ( xnpu*yffu - ynpu*xffu ) / nffu
  gcosu = ( xnpu*xffu + ynpu*yffu ) / nffu
  gsinv =   ( xnpv*xffv + ynpv*yffv ) / nffv
  gcosv = - ( xnpv*yffv - ynpv*xffv ) / nffv
  ;  
  ;#GEOGRAPHICAL MESH
  ;#COSU - SINU
  ; (gsinu,gcosu,gdgla) = geo_mesh(glamf,gsinu,gcosu,0,1) 
  delete(dime)
  delete(glam)
  delete(glan)
  dime=dimsizes(glamf)
  dgla = new((/dime(1),dime(2)/),float,-9999.)
  glam = glamf(0,1:,   :)
  glan = glamf(0,0:dime(1)-1-1,:)
  dgla(1:,:) = mod(abs(glam-glan),360)
  gsinu = where(dgla.lt.1e-3,0., gsinu)
  gcosu = where(dgla.lt.1e-3,1., gcosv)
  ;
  ;gsinu = mask(gsinu,abs(gsinu).gt.2,False)
  ;gcosu = mask(gcosu,abs(gcosu).gt.2,False)
  ;gsinu = where(gsinu.ge.1,1.,gsinu)
  ;gcosu = where(gcosu.ge.1,1.,gcosu)
  ;gsinu = where(gsinu.le.-1,-1.,gsinu)
  ;gcosu = where(gcosu.le.-1,-1.,gcosu)
  gsinu@_FillValue = -9999. 
  gcosu@_FillValue = -9999.
  ;
  gsinur=reshape(gsinu,(/1,nx,ny/))
  gcosur=reshape(gcosu,(/1,nx,ny/))
  ;
  ;gsinur=cl_recouvrement(gsinur,1)
  ;gcosur=cl_recouvrement(gcosur,1)  
  print("OK COSU et SINU!")
  ;#COSV - SINV
  ;
  dimphif=dimsizes(gphif)
  gphim = gphif(0,:,1:)
  gphin = gphif(0,:,0:dimphif(2)-1-1)
  gladiffmod=new((/dimphif(1),dimphif(2)/),float,-9999.)
  gladiffmod(:,1:)=abs(gphim - gphin)
  ;#gladiffmod = abs(gphim - gphin)
  gsinv = where(gladiffmod.lt.1e-3,0., gsinv)
  gcosv = where(gladiffmod.lt.1e-3,1., gcosv)
  ;
  ;gsinv = mask(gsinv,abs(gsinv).gt.2,False)
  ;gcosv = mask(gcosv,abs(gcosv).gt.2,False)
  ;gsinv = where(gsinv.ge.1,1.,gsinv)
  ;gcosv = where(gcosv.ge.1,1.,gcosv)
  ;gsinv = where(gsinv.le.-1,-1.,gsinv)
  ;gcosv = where(gcosv.le.-1,-1.,gcosv)
  gsinv@_FillValue = -9999. 
  gcosv@_FillValue = -9999.
  ;
  gsinvr=reshape(gsinv,(/1,nx,ny/))
  gcosvr=reshape(gcosv,(/1,nx,ny/))
  ;gsinvr=cl_recouvrement(gsinvr,1)
  ;gcosvr=cl_recouvrement(gcosvr,1)  
  ;
  gsinvr@short_name="GSINV"
  gcosvr@short_name="GCOSV"
  gsinur@short_name="GSINU"
  gcosur@short_name="GCOSU"
  ;
  gsinvr@long_name="GSINV"
  gcosvr@long_name="GCOSV"
  gsinur@long_name="GSINU"
  gcosur@long_name="GCOSU"
  ;
  gsinvr@missing_value=-9999.
  gcosvr@missing_value=-9999.
  gsinur@missing_value=-9999.
  gcosur@missing_value=-9999.
  ;
  gsinvr@valid_min=-1.
  gcosvr@valid_min=-1.
  gsinur@valid_min=-1.
  gcosur@valid_min=-1.
  ;
  gsinvr@valid_max=1.
  gcosvr@valid_max=1.
  gsinur@valid_max=1.
  gcosur@valid_max=1.
  ;
  gsinvr@axis="TYX"
  gcosvr@axis="TYX"
  gsinur@axis="TYX"
  gcosur@axis="TYX"


  printVarSummary(gcosur)
  printVarSummary(glamf)
  print("OK COSV et SINV!")  
  ; ========================================================
  print("ON ECRIT.")
  fon="angle_"+conf+".nc"
  fo = addfile(fon,"c")
  setfileoption(fo,"DefineMode",True)
  
  dimNames = (/"t","y", "x"/)
  dimSizes = (/1, nx, ny/)
  dimUnlim=(/True,False,False/)
  filedimdef(fo,dimNames,dimSizes,dimUnlim)
  
  print("Var GCOSU")
  filevardef(fo,"GCOSU",typeof(glamf),getvardims(glamf))  
  print("Att GCOSU")
  filevarattdef(fo,"GCOSU",gcosur)
  print("Wri GCOSU")
  fo->GCOSU   = (/gcosur/)
  
  filevardef(fo,"GCOSV",typeof(glamf),getvardims(glamf))  
  filevarattdef(fo,"GCOSV",gcosvr)
  fo->GCOSV   = (/gcosvr/)

  filevardef(fo,"GSINU",typeof(glamf),getvardims(glamf))  
  filevarattdef(fo,"GSINU",gsinur)
  fo->GSINU   = (/gsinur/)
 
  filevardef(fo,"GSINV",typeof(glamf),getvardims(glamf))  
  filevarattdef(fo,"GSINV",gsinvr)
  fo->GSINV   = (/gsinvr/)
  ;
end
