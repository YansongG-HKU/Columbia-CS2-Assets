import collections,json,hashlib,sys,xml.etree.ElementTree as XML
from pathlib import Path
import numpy as np
from pyproj import Transformer
from osgeo import ogr
D=Path(__file__).parent
EP=Transformer.from_crs(2263,6347,always_xy=True)
EF=Transformer.from_crs(4326,6347,always_xy=True)
B=XML.parse(D/'lerner-nyc-2014.gml').find('.//{*}Building')
tags={x.attrib['name']:x[0].text for x in B if 'name' in x.attrib}
assert tags['BIN']=='1082166' and tags['DOITT_ID']=='397140'
foot=json.loads((D/'lerner-footprint.geojson').read_text())['features']
assert len(foot)==1 and foot[0]['properties']['doitt_id']==tags['DOITT_ID']
W=np.asarray(foot[0]['geometry']['coordinates'][0][0]); P=np.asarray(EF.transform(*W[:-1].T)).T
O=np.mean(P,axis=0)
v=P[9]-P[4]; v/=np.linalg.norm(v)
ux=np.array([v[0],v[1]])
uy=np.array([-v[1],v[0]])
axis=np.array([ux,uy])
local=lambda p:(p-O) @ axis.T
P=local(P); O=O+((P.min(axis=0)+P.max(axis=0))*.5)@axis; P=local(np.asarray(EF.transform(*W[:-1].T)).T)
groups=collections.defaultdict(list)
for node in B.findall('{*}boundedBy'):
 n,=node[:]; tag=n.tag.split('}')[-1]
 for o in n.findall('.//{*}Polygon'):
  r=np.fromstring(o.find('.//{*}posList').text,sep=' ').reshape(-1,3);assert np.allclose(r[0],r[-1],rtol=0,atol=1e-6)
  xy=np.asarray(EP.transform(*r[:-1,:2].T)).T
  groups[tag].append(np.round(np.c_[local(xy),r[:-1,2]*1200/3937],5))
def flat(a):return float(np.sum(a[:,0]*np.roll(a[:,1],-1)-a[:,1]*np.roll(a[:,0],-1))*.5)
def poly(a):
 r=ogr.Geometry(ogr.wkbLinearRing)
 for x,y,*z in a:r.AddPoint_2D(x,y)
 r.CloseRings(); p=ogr.Geometry(ogr.wkbPolygon);p.AddGeometry(r);return p
g,=groups['GroundSurface']; gp=poly(g); fp=poly(P)
print('origin, axes:',O,axis,'foot span:',np.ptp(P,axis=0),'historic span:',np.ptp(g[:,:2],axis=0),'fp area:',fp.GetArea(),'hist area:',gp.GetArea(),'symdiff m2:',gp.SymDifference(fp).GetArea())
print('foot ring',np.round(P,3));print('city roof tiers')
for r in sorted(groups['RoofSurface'],key=lambda p:p[0,2]):print(r[0,2],flat(r[:,:2]),np.round(r[:,:2].min(axis=0),2),np.round(r[:,:2].max(axis=0),2),poly(r).IsValid())
