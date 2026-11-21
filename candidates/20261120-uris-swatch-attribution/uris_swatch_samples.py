from pathlib import Path
from PIL import Image
import argparse,json,math,statistics
p=argparse.ArgumentParser()
p.add_argument('directory',type=Path);p.add_argument('output',type=Path)
a=p.parse_args()
anchors={'A':(0.7842459082603455,0.44651466608047485),'B':(0.7022064328193665,0.21046608686447144)}
channels=('BaseColor','Normal','MaskMap','ControlMask','Emissive')
result={k:{} for k in anchors}
for c in channels:
    with Image.open(a.directory/f'NA_UrisHall_6x9_{c}.png') as im:
        im.load()
        for k,(u,v) in anchors.items():
            x,y=u*im.width,(1-v)*im.height
            left,top=math.floor(x-.5),math.floor(y-.5)
            s,t=x-.5-left,y-.5-top
            pixel=lambda x,y: im.getpixel((x,y)) if im.mode not in ('L','I') else (im.getpixel((x,y)),)
            near=[pixel(left+i,top+j) for j in range(2) for i in range(2)]
            weights=[(1-s)*(1-t),s*(1-t),(1-s)*t,s*t]
            bilateral=[sum(z[j]*w for z,w in zip(near,weights)) for j in range(len(near[0]))]
            x0,y0=math.floor(x),math.floor(y)
            measured={}
            for r in (1,4,16,64):
                samples=[pixel(i,j) for j in range(y0-r,y0+r+1) for i in range(x0-r,x0+r+1)]
                measured[r]={'min':list(map(min,zip(*samples))),'max':list(map(max,zip(*samples))),
                             'distinct_values':len(set(samples))}
            result[k][c]={'mode':im.mode,'size':list(im.size),'pixel_xy':[x0,y0],
                          'encoded_bilinear_value':bilateral,'bilinear_support_pixels':near,'neighborhoods':measured}
a.output.write_text(json.dumps(result,indent=2)+'\n')
for k,v in result.items():
    for channel,row in v.items():
        print(k,channel,row['pixel_xy'],row['encoded_bilinear_value'],[(n,s['distinct_values']) for n,s in row['neighborhoods'].items()])
