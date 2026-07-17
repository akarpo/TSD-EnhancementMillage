#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib

NAVY=(31,42,68); RED=(178,34,34); GRAY=(90,90,90); LGRAY=(120,120,120)
PINK=(251,233,231); WHITE=(255,255,255); INK=(17,17,17); LINE=(210,210,214); GREEN=(27,94,32); LNAVY=(233,238,248)

DJ=os.path.join(matplotlib.get_data_path(),'fonts','ttf')
def fp(*cands):
    for c in cands:
        if os.path.exists(c): return c
    return None
REG=fp("/System/Library/Fonts/Supplemental/Arial.ttf","/Library/Fonts/Arial.ttf",os.path.join(DJ,"DejaVuSans.ttf"))
BLD=fp("/System/Library/Fonts/Supplemental/Arial Bold.ttf","/Library/Fonts/Arial Bold.ttf",os.path.join(DJ,"DejaVuSans-Bold.ttf"))
def font(sz,bold=False): return ImageFont.truetype(BLD if bold else REG, sz)

def tw(d,t,f): return d.textlength(t,font=f)
def wrap(d,t,f,maxw):
    words=t.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f)<=maxw: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

# ---------------- IMAGE 1: comparison table ----------------
def make_table():
    W=1320; M=54
    img=Image.new("RGB",(W,1000),WHITE); d=ImageDraw.Draw(img)
    y=M
    f_title=font(46,True); f_sub=font(25); f_h=font(25,True); f_cell=font(28,True); f_lbl=font(24); f_foot=font(20); f_src=font(19)
    d.text((M,y),"Local school funding, per pupil (2024-25)",font=f_title,fill=NAVY); y+=58
    for ln in wrap(d,"Local property-tax funding. Oakland already leads Macomb, with no enhancement millage of its own.",f_sub,W-2*M):
        d.text((M,y),ln,font=f_sub,fill=GRAY); y+=32
    y+=16
    # table geometry
    x0=M; x1=W-M; tw_all=x1-x0
    c0=int(tw_all*0.42); cw=(tw_all-c0)/3
    cols=[x0, x0+c0, x0+c0+cw, x0+c0+2*cw, x1]
    rows=[
        ("h","Local school funding","Oakland today","Oakland if it passes","Macomb*"),
        ("d","Member districts' own local revenue","$7,402","$7,402","$5,273"),
        ("d","County ISD's own levies (incl. enhancement)","$1,781","$2,562","$1,973"),
        ("t","TOTAL LOCAL, PER PUPIL","$9,184","$9,965","$7,247"),
    ]
    rh=104
    for kind,lbl,a,b,c in rows:
        if kind=="h": bg=NAVY
        elif kind=="t": bg=PINK
        else: bg=WHITE
        d.rectangle([x0,y,x1,y+rh],fill=bg,outline=LINE,width=2)
        # vertical separators
        for cx in cols[1:-1]:
            d.line([cx,y,cx,y+rh],fill=LINE,width=2)
        # label
        lcol = WHITE if kind=="h" else (NAVY if kind=="t" else INK)
        lf = f_h if kind=="h" else (font(24,True) if kind=="t" else f_lbl)
        lbl_lines=wrap(d,lbl,lf,c0-28)
        ly=y+(rh-len(lbl_lines)*30)//2
        for ln in lbl_lines:
            d.text((x0+16,ly),ln,font=lf,fill=lcol); ly+=30
        # values
        vals=[a,b,c]
        for i,v in enumerate(vals):
            cx0=cols[1+i]; cx1=cols[2+i]
            if kind=="h":
                vf=f_h; vcol=WHITE
                vlines=wrap(d,v,vf,cw-16)
                vy=y+(rh-len(vlines)*30)//2
                for ln in vlines:
                    d.text((cx0+(cw-tw(d,ln,vf))/2,vy),ln,font=vf,fill=vcol); vy+=30
            else:
                # highlight the "if it passes" column (i==1) and total row in red
                vcol = RED if (i==1 or kind=="t") else INK
                vf = font(30,True) if kind=="t" else f_cell
                d.text((cx0+(cw-tw(d,v,vf))/2, y+(rh-34)//2), v, font=vf, fill=vcol)
        y+=rh
    y+=18
    for ln in wrap(d,"*Local funding only (property taxes). Macomb already levies a 1.82-mill enhancement (2020); Oakland, with none, still raises 27% more per pupil. Total funding, counting state and federal aid, is much closer: about $17,100 per pupil in Oakland vs about $16,100 in Macomb.",f_foot,W-2*M):
        d.text((M,y),ln,font=f_foot,fill=GRAY); y+=27
    y+=10
    bl=wrap(d,"Bigger picture: Oakland pays more into Michigan's school property tax base than it draws back per pupil. Its districts hold about 16% of that base but enroll about 12% of the state's students. Through the 6-mill State Education Tax alone that is a net contribution of at least $85 million a year.",f_foot,W-2*M-40)
    bh=len(bl)*28+26
    d.rectangle([M,y,W-M,y+bh],fill=LNAVY)
    yy=y+14
    for ln in bl:
        d.text((M+20,yy),ln,font=f_foot,fill=NAVY); yy+=28
    y+=bh+16
    d.text((M,y),"Sources: MDE (Bulletin 1014/1011 & Financial Information Database) and Michigan Senate Fiscal Agency, 2024-25.",font=f_src,fill=LGRAY); y+=34
    img=img.crop((0,0,W,y+M-20))
    return img

# ---------------- IMAGE 2: problem vs plan ----------------
def make_juxta():
    W=1320; M=54
    img=Image.new("RGB",(W,1200),WHITE); d=ImageDraw.Draw(img)
    f_title=font(46,True); f_h=font(26,True); f_body=font(26); f_bul=font(26,True); f_foot=font(24,True)
    y=M
    d.text((M,y),"The District's own email: problem vs. plan",font=f_title,fill=NAVY); y+=70
    colgap=30; colw=(W-2*M-colgap)/2
    lx=M; rx=M+colw+colgap
    top=y; hh=64
    # headers
    d.rectangle([lx,top,lx+colw,top+hh],fill=NAVY)
    d.rectangle([rx,top,rx+colw,top+hh],fill=NAVY)
    d.text((lx+20,top+18),"THE PROBLEM THEY NAME (p.3)",font=f_h,fill=WHITE)
    d.text((rx+20,top+18),"THE PLAN THEY OFFER (p.5)",font=f_h,fill=WHITE)
    by=top+hh+22
    # left body (quote)
    quote='"Special education funding is underfunded by approximately 40%... districts must use dollars from their general fund to support students with special needs to close this gap."'
    ly=by
    for ln in wrap(d,quote,f_body,colw-40):
        d.text((lx+20,ly),ln,font=f_body,fill=NAVY); ly+=36
    # right body (tiles)
    ry=by
    d.text((rx+20,ry),"Six broad budget categories:",font=font(24),fill=GRAY); ry+=44
    for tile in ["Staff Retention & Raises","Enhance Student Wellness Supports","Stabilize the General Fund Budget",
                 "Enhance & Maintain Safety Measures","Maintain Staff to Student Ratios","Maintain & Strengthen District Programming"]:
        for k,ln in enumerate(wrap(d,tile,f_bul,colw-70)):
            pre="•  " if k==0 else "    "
            d.text((rx+24,ry),pre+ln,font=f_bul,fill=RED); ry+=38
        ry+=6
    boxbot=max(ly,ry)+16
    # column borders
    d.rectangle([lx,top,lx+colw,boxbot],outline=LINE,width=2)
    d.rectangle([rx,top,rx+colw,boxbot],outline=LINE,width=2)
    y=boxbot+30
    # bottom strip
    d.rectangle([M,y,W-M,y+70],fill=PINK)
    msg="Not one of the six names special education, the need the District itself cites."
    d.text((M+20,y+20),msg,font=f_foot,fill=RED)
    y+=70+M-16
    img=img.crop((0,0,W,y))
    return img

out_dir="."
t=make_table(); t.save(f"{out_dir}/funding-chart.png")
j=make_juxta(); j.save(f"{out_dir}/problem-vs-plan.png")
print("table size:", t.size, "| juxta size:", j.size)
print("wrote funding-chart.png and problem-vs-plan.png to", os.path.abspath(out_dir))
