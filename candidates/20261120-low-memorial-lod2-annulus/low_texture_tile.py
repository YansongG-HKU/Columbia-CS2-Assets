"""Create a padded LOD2 atlas island from the exact homologous LOD1 cornice donor."""
from low_tri_plan import *
from PIL import Image
import numpy as np
import shutil
D=json.loads((d/'low-uv-donors.json').read_text())['NA_ColumbiaLowLibrary_13x10_LOD1.fbx']
data=[([x[0],x[2]+9,1],uv) for f in D for x,uv in zip(f['xyz'],f['uv'])]
world=np.array([x for x,y in data]); uv=np.array([y for x,y in data])
mat=np.linalg.lstsq(world,uv,rcond=None)[0]; assert (abs(world@mat-uv)).max()<3e-8
outer=out['outer'];ids=outer+out['inner']
outer_uv=np.array([[*xy(k),1.] for k in outer])@mat
umin,vmin=outer_uv.min(0); umax,vmax=outer_uv.max(0)
x,y,w,h=824,604,96,104
pad=16
# Maintain identical positive U/V scale, preserving donor tangent orientation.
scale=min((w-2*pad)/(umax-umin),(h-2*pad)/(vmax-vmin))
uc=(umax+umin)/2; vc=(vmax+vmin)/2
a=np.array([[*xy(k),1.] for k in ids])@mat
pf=np.c_[x+w/2+(a[:,0]-uc)*scale,y+h/2-(a[:,1]-vc)*scale]
assert ((pf[:,0]>=x+pad-1e-7)&(pf[:,0]<=x+w-pad+1e-7)).all()
assert ((pf[:,1]>=y+pad-1e-7)&(pf[:,1]<=y+h-pad+1e-7)).all()
Y,X=np.mgrid[y:y+h,x:x+w]
nearUV=np.stack((uc+(X+.5-x-w/2)/scale,vc-(Y+.5-y-h/2)/scale),axis=-1)
plane=(nearUV-mat[2])@np.linalg.inv(mat[:2])
t=np.arange(8)*np.pi/4
apo=np.max(plane@np.stack((np.cos(t),np.sin(t)),axis=0),axis=2)
# Clip outer unverified strip to interior donor continuity; no sampling across other chart edges.
clipped=plane*np.minimum(1,15.45/np.maximum(1e-6,apo))[...,None]
samples=(clipped@mat[:2])+mat[2]
occ=np.asarray(Image.open(d/'low-far-existing-UV.png'))
assert not occ[y:y+h,x:x+w].any()
Dout=d/'low-tile-candidate';Dout.mkdir(exist_ok=False)
receipts={}
for label in ('BaseColor','ControlMask','Emissive','MaskMap','Normal'):
 near,=list((d/'low-textures').glob('*13x10_'+label+'.png'))
 far,=list((d/'low-textures').glob('*LOD2_'+label+'.png'))
 ni=Image.open(near).convert('RGBA'); orig=Image.open(far); old=orig.convert('RGBA')
 assert ni.size==(4096,4096) and old.size==(1024,1024)
 src=np.asarray(ni); X=samples[:,:,0]*4096-.5; Y=(1-samples[:,:,1])*4096-.5
 ix=X.astype(int);iy=Y.astype(int)
 dx=(X-ix)[...,None];dy=(Y-iy)[...,None]
 tile=np.rint((1-dy)*((1-dx)*src[iy,ix]+dx*src[iy,ix+1])+dy*((1-dx)*src[iy+1,ix]+dx*src[iy+1,ix+1])).astype(np.uint8)
 a=np.array(old);a[y:y+h,x:x+w]=tile
 if np.array_equal(a,np.asarray(old)):shutil.copyfile(far,Dout/far.name)
 else:Image.fromarray(a,mode='RGBA').save(Dout/far.name,optimize=False,**{k:v for k,v in orig.info.items() if k in ('exif','dpi','icc_profile')})
 new=np.asarray(Image.open(Dout/far.name))
 changes=np.any(new!=np.asarray(old),axis=-1);assert changes.sum()==changes[y:y+h,x:x+w].sum()
 receipts[label]={'donor_sha256':hashlib.sha256(near.read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(far.read_bytes()).hexdigest(),
  'candidate_sha256':hashlib.sha256((Dout/far.name).read_bytes()).hexdigest(),'changed_pixels':int(changes.sum()),
  'tile_main_q05_q50_q95':np.quantile(tile[pad:-pad,pad:-pad].reshape(-1,4),[.05,.5,.95],axis=0).tolist()}
 print(label,receipts[label]['changed_pixels'],receipts[label]['tile_main_q05_q50_q95'])
basis=np.linalg.inv(mat[:2]);basis/=np.linalg.norm(basis,axis=1,keepdims=True)
assert abs(float(basis[0]@basis[1]))<1e-6
report=dict(rect=[x,y,w,h],padding_px=pad,near_apothem_clamp_m=15.45,uv_by_vertex={k:[px/1024,1-py/1024] for k,(px,py) in zip(ids,pf)},
            raw_tangent=[basis[0,0],0,basis[0,1]],raw_binormal=[basis[1,0],0,basis[1,1]],maps=receipts,
            note='Outer 0.55 m reuses nearest trusted LOD1 donor strip; geometry held at far source extents. Provisional exterior appearance.')
(d/'low-tile-report.json').write_text(json.dumps(report,indent=2)+'\n')
