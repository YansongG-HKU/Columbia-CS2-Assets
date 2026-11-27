import sys,numpy as np
from scipy.optimize import least_squares
d=np.load(sys.argv[1]);a=d['a']; p=d['pixel']; R=np.array([[.887,.462],[.462,-.887]])
uv=(p-[590,218])@R.T; hold=np.isin(a[:,4],[1135,1136]); z=(a[:,2]>=54.90)&(a[:,2]<=55.18)&(a[:,3]==1)&(a[:,5]==1)&(uv[:,1]>25)&(uv[:,1]<122)
def points(mark):
 rows=[]
 for x in range(-88,89,4):
  k=mark&z&(abs(uv[:,0]-x)<=2)
  if k.sum()>=8:
   vv=np.percentile(uv[k,1],97)
   idx=np.flatnonzero(k)[np.argmin(abs(uv[k,1]-vv))]
   rows.append(np.r_[a[idx,:2]-[587623.1421979353,4518097.006500896],uv[idx],k.sum()])
 return np.asarray(rows)
p0=points(~hold);p1=points(hold)
def circ(q,xy):return np.linalg.norm(xy-q[:2],axis=1)-q[2]
def ell(q,uv): return (np.sqrt(((uv[:,0]-q[0])/q[2])**2 +((uv[:,1]-q[1])/q[3])**2)-1)*np.mean(q[2:])*0.226
C=least_squares(circ,[2,0,24],args=(p0[:,:2],),loss='soft_l1',f_scale=.35).x
E=least_squares(ell,[0,1,108,115],args=(p0[:,2:4],),bounds=([-30,-35,70,90],[30,25,140,170]),loss='soft_l1',f_scale=.35).x
for name,X,fn,ix in [('circle',C,circ,[0,1]),('ellipse',E,ell,[2,3])]:
 print(name,X,'train',len(p0),np.percentile(np.abs(fn(X,p0[:,ix])),[50,90,100]),'hold',len(p1),np.percentile(np.abs(fn(X,p1[:,ix])),[50,90,100]))
print(p0[::7])
