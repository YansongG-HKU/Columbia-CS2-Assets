from low_tri_plan import *
all_rows={}
for f in [source,*sorted((d/'low-source').glob('*.fbx'))]:
 gg,VV,FF=load(f); normal=item(gg,b'LayerElementNormal'); uv=item(gg,b'LayerElementUV')
 un=prop(uv,b'UV');ui=prop(uv,b'UVIndex');ut=[tuple(un[k:k+2]) for k in range(0,len(un),2)]
 assert prop(uv,b'MappingInformationType')==b'ByPolygonVertex' and len(ui)==sum(map(len,FF))
 print(f.name,list((n.id, prop(n,b'MappingInformationType') if b'MappingInformationType' in {e.id for e in n.elems} else '') for n in gg.elems if n.id.startswith(b'LayerElement')))
 rows=[]; c=0
 for j,ff in enumerate(FF):
  pp=[VV[k] for k in ff]; y0,y1=min(p[1] for p in pp),max(p[1] for p in pp)
  up=area([(p[0],p[2]+9) for p in pp])
  details=f==source and (j in planar or j in range(539,547) or any(k in outer|inner for k in ff)) or f!=source and abs(y0-Y)<1e-5 and abs(y1-Y)<1e-5 and up<-10
  if details:
   rows.append(dict(face=j,xyz=pp,uv=[ut[k] for k in ui[c:c+len(ff)]],sign=-up))
  c+=len(ff)
 all_rows[f.name]=rows
(d/'low-uv-donors.json').write_text(json.dumps(all_rows,indent=2)+'\n')
