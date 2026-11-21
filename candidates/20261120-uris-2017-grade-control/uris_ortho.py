import json,math
from pathlib import Path
from urllib.request import urlretrieve
from PIL import Image,ImageDraw
lon,lat=-73.9613538,40.8089617
z=19;n=2**z
cx=int((lon+180)/360*n);cy=int((1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n)
out=Image.new('RGB',(768,768))
for j,y in enumerate(range(cy-1,cy+2)):
 for i,x in enumerate(range(cx-1,cx+2)):
  f=f'ortho-{z}-{x}-{y}.jpg'
  url=f'https://tiles.arcgis.com/tiles/yG5s3afENB5iO9fj/arcgis/rest/services/NYC_Orthos_2024/MapServer/tile/{z}/{y}/{x}'
  if not Path(f).exists(): urlretrieve(url,f)
  with Image.open(f) as im:out.paste(im,(i*256,j*256))
out.save('uris-ortho-2024.png')
Path('uris-ortho-reference.json').write_text(json.dumps(dict(zoom=z,tile_min_x=cx-1,tile_min_y=cy-1,resolution_web_mercator=40075016.68557849/(n*256),tile_size=256),indent=2)+'\n')
