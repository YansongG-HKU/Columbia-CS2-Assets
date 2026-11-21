from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
D=Path(__file__).parent
I=Image.new('RGB',(1320,958),'#eef4f7'); d=ImageDraw.Draw(I)
reg='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; bold=reg.replace('Regular','Bold')
def tx(x,y,s,n=25,c='#213745',heavy=False):
 d.text((x,y),s,font=ImageFont.truetype(bold if heavy else reg,n,index=2),fill=c)
tx(48,24,'哥大 Pupin Hall',52,heavy=True)
tx(49,102,'中景 LOD1  ·  修复 50 处丢面，并补合西侧灯饰接缝',28,'#3e6577')
for x,s,c in [(247,'修复前','#935521'),(817,'修复后','#136a63')]:tx(x,158,s,27,c,True)
for y,key,label in [(218,'roof','高层窗框竖条'),(519,'entry','入口灯饰与灯帽')]:
 d.rounded_rectangle((44,y,1276,y+275),radius=15,fill='white')
 tx(68,y+17,label,23,'#4f7384',True)
 for x,k in [(248,'before'),(794,'after')]:
  A=Image.open(D/f'{key}-{k}.png').convert('RGBA')
  A.thumbnail((410,249));I.paste(A,(x,y+13),A)
d.rounded_rectangle((45,815,1275,890),radius=15,fill='#123b50')
tx(69,833,'42 根窗框竖条 + 8 根灯饰细柱',26,'white',True);tx(682,833,'37,286 面，FBX 导出和回读一致',25,'#e0f1f1')
tx(48,915,'示意颜色标出修复区域。远景形体和场地标高未修改，未做游戏内验收。',22,'#496678')
I.save(D/'Pupin-Hall-LOD1-repair-comparison.webp',quality=94)
I.thumbnail((880,760));I.save(D/'proof.png')
