from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
D=Path(__file__).parent
I=Image.new('RGB',(1200,1110),'#eef4f7'); d=ImageDraw.Draw(I)
reg='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; bold=reg.replace('Regular','Bold')
def font(n,heavy=False):return ImageFont.truetype(bold if heavy else reg,n,index=2)
def tx(x,y,s,n=25,c='#213745',heavy=False):d.text((x,y),s,font=font(n,heavy),fill=c)
tx(48,27,'哥大 Lerner Hall',53,heavy=True)
tx(49,107,'中景 LOD1  ·  3 处导出丢面修复',29,'#3e6577')
for x,s,c in [(304,'修复前：相反重合薄片','#955222'),(762,'修复后：恢复原构件','#1a6b64')]:tx(x,169,s,25,c,True)
for y,j,lab in [(216,0,['01','中庭框条 A']),(460,1,['02','南侧门片']),(704,2,['03','中庭框条 B'])]:
 d.rounded_rectangle((46,y,1153,y+224),radius=15,fill='white')
 tx(70,y+48,lab[0],33,'#587786',True);tx(70,y+103,lab[1],25)
 for x,k in [(258,'old'),(716,'new')]:
  A=Image.open(D/f'{j}-{k}.png').convert('RGBA')
  A.thumbnail((399,212)); I.paste(A,(x,y+6),A)
d.rounded_rectangle((46,952,1153,1030),radius=16,fill='#123b50')
tx(73,969,'15,304 面，FBX 导出和回读一致',25,'white',True);tx(628,970,'其他 15,268 面逐角保持不变',24,'#d7e9f0')
tx(49,1058,'构件单独着色展示，不代表实际游戏材质或游戏内验收。',22,'#466575')
I.save(D/'Lerner-Hall-LOD1-local-repair.webp',quality=93)
