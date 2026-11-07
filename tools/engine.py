from PIL import Image, ImageDraw, ImageFont
import textwrap
W,H=1080,1350
BG=(6,6,6);INK=(243,243,241);MUTED=(143,143,140);FAINT=(74,74,72);NUM=(16,16,15)
F='/home/claude/fonts/'
def font(name,size): return ImageFont.truetype(F+name,size)
def track(d,xy,text,fnt,fill,sp,anchor='l'):
    x,y=xy
    widths=[d.textlength(c,font=fnt)+sp for c in text]
    total=sum(widths)-sp
    if anchor=='r': x-=total
    for c,w in zip(text,widths):
        d.text((x,y),c,font=fnt,fill=fill); x+=w
def wrap(d,text,fnt,maxw):
    words=text.split();lines=[];cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=fnt)<=maxw: cur=t
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
STY={'H':('Fraunces-500.ttf',76,INK,1.16,40),'h':('Fraunces-500.ttf',58,INK,1.18,34),
     'M':('Inter-Regular.otf',54,MUTED,1.32,34),'B':('Inter-Regular.otf',36,MUTED,1.45,26),
     'W':('Inter-Medium.otf',38,INK,1.42,26)}
def render(slide,kinds,idx,total,path,closing):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.rectangle([44,44,W-44,H-44],outline=(28,28,27),width=2)
    if total>1:
        nf=font('Fraunces-600.ttf',760);s=str(idx)
        bb=d.textbbox((0,0),s,font=nf);d.text((1030-bb[2],1215-bb[3]),s,font=nf,fill=NUM)
    d.line([100,128,145,128],fill=FAINT,width=2)
    ef=font('Inter-Medium.otf',26);track(d,(163,114),slide['eyebrow'].upper(),ef,MUTED,4)
    if total>1: track(d,(980,114),f'{idx:02d} / {total:02d}',ef,MUTED,4,'r')
    limit=1070 if closing else 1180
    for scale in (1.0,.94,.88,.82,.76,.7):
        items=[];y=310
        for k,t in zip(kinds,slide['blocks']):
            fn,sz,col,ld,gap=STY[k];fnt=font(fn,int(sz*scale))
            lines=wrap(d,t,fnt,880);items.append((lines,fnt,col,ld,gap,k))
            y+=len(lines)*int(fnt.size*ld)+gap
        if y-STY['B'][4]<=limit: break
    y=310
    for lines,fnt,col,ld,gap,k in items:
        for ln in lines:
            d.text((100,y),ln,font=fnt,fill=col);y+=int(fnt.size*ld)
        y+=gap
    if closing:
        d.line([100,1182,145,1182],fill=FAINT,width=2)
        track(d,(100,1204),'THE TOP PICK',font('Fraunces-600.ttf',36),INK,7)
    im.save(path,quality=93,subsampling=0)
    return y
def kinds_for(pillar,si,n,slide):
    b=slide['blocks'];first='H' if si==0 else 'h'
    if len(b[0])>90: first='W'
    if pillar=='answer_comparison':
        if si==1: return ['M']+['B']*(len(b)-1)
        if si==2: return ['h']+['W']*(len(b)-1)
        if si==0: return ['H']+['B']*(len(b)-1)
    return [first]+['B']*(len(b)-1)
