from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
from itertools import pairwise
from sys import argv
import json
r,o,dest=map(Path,argv[1:])
lods=('LOD0','LOD1','LOD2'); views=('front','aerial'); images={}
sheet=Image.new('RGB',(1536,760),(36,42,50));d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for c,lod in enumerate(lods):
 d.text((c*512+20,9),lod+'  /  Base Color',font=font,fill=(242,244,246))
 for v,key in enumerate(views):
  full=Image.open(r/f'{lod}-{key}.png').convert('RGBA')
  x0,y0,x1,y1=full.getchannel('A').getbbox()
  if not (0<x0<x1<full.width and 0<y0<y1<full.height):raise ValueError((lod,key,x0,y0,x1,y1))
  images[lod,key]=full.getchannel('A').point(lambda p:255 if p>=128 else 0)
  im=full.copy();im.thumbnail((512,344));sheet.paste(im,(c*512,42+v*355),im)
report={}
for v in views:
 rm={}
 for a,b in pairwise(lods):
  A,B=images[a,v],images[b,v]
  rm[f'{a}-{b}']={'different_silhouette_pixels':int(ImageChops.difference(A,B).histogram()[-1]),'baseline_shape_pixels':int(A.histogram()[-1])}
 report[v]=rm
sheet.save(o,quality=88)
dest.write_text(json.dumps(report,indent=2)+'\n')
print(report)
