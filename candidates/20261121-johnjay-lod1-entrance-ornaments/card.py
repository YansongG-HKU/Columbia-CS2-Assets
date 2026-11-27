from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).parent
s='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; b='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
f=lambda n,w:ImageFont.truetype(n,w,index=2)
im=Image.new('RGB',(1280,760),'#edf2f6'); g=ImageDraw.Draw(im)
g.text((43,19),'哥大 John Jay Hall',font=f(b,43),fill='#192e3b')
g.text((45,86),'LOD1 中景 · 解决导出后丢面',font=f(s,26),fill='#3b5b6e')
for x,key,lab,col in [(41,'before','修复前：重叠薄片','#9c542a'),(653,'after','修复后：恢复实体细柱','#14665f')]:
 g.rounded_rectangle((x,140,x+586,554),radius=18,fill='white')
 g.text((x+16,151),lab,font=f(b,25),fill=col)
 a=Image.open(p/(key+'-ornament.png')).convert('RGBA'); a=a.crop((116,9,556,471));a.thumbnail((553,337)); im.paste(a,(x+(586-a.width)//2,200),a)
g.rounded_rectangle((41,575,1239,687),radius=18,fill='#0f374d')
g.text((62,587),'8 处局部恢复',font=f(b,28),fill='white')
g.text((64,638),'按近景原模型恢复，并保留原 UV',font=f(s,20),fill='#c9e8ed')
g.text((612,588),'43,934 面，FBX 导出与回读一致',font=f(b,25),fill='white')
g.text((616,635),'其他 43,774 面的几何、UV 和法线保持不变',font=f(s,20),fill='#d2eaf2')
g.text((42,710),'示意颜色只标出修改部位。尚未做 CS2 Editor 实测。',font=f(s,21),fill='#446574')
im.save(p/'John-Jay-Hall-LOD1-repaired-with-local-readback.webp',quality=94)
