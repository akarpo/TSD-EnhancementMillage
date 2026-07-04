#!/usr/bin/env python3
import os, math, matplotlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Troy School District seal palette: black + vegas gold (#b4a269) + cream
BG=(11,11,13); GOLD=(184,165,104); GOLDB=(224,197,120); CREAM=(242,235,216)
GOLDDIM=(120,106,62); RINGS=(34,30,18); GLOW=(48,40,20)

DJ=os.path.join(matplotlib.get_data_path(),'fonts','ttf')
def fp(*c):
    for x in c:
        if os.path.exists(x): return x
REG=fp("/System/Library/Fonts/Supplemental/Arial.ttf",os.path.join(DJ,"DejaVuSans.ttf"))
BLD=fp("/System/Library/Fonts/Supplemental/Arial Bold.ttf",os.path.join(DJ,"DejaVuSans-Bold.ttf"))
def font(sz,bold=True): return ImageFont.truetype(BLD if bold else REG,sz)

W,H=1640,856; cx=W//2
img=Image.new("RGB",(W,H),BG)

# --- background: faint concentric rings (echo the seal) + radial glow ---
bg=Image.new("RGB",(W,H),BG); bd=ImageDraw.Draw(bg)
cyR=300
for r in range(90,760,58):
    bd.ellipse([cx-r,cyR-r,cx+r,cyR-r+2*r],outline=RINGS,width=2)
bg=bg.filter(ImageFilter.GaussianBlur(1.2))
glow=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(glow)
gd.ellipse([cx-470,cyR-190,cx+470,cyR+190],fill=GLOW)
glow=glow.filter(ImageFilter.GaussianBlur(120))
img=Image.blend(bg,glow,0.85)
d=ImageDraw.Draw(img)

# --- seal frame (double gold border) ---
d.rectangle([26,26,W-26,H-26],outline=GOLDDIM,width=3)
d.rectangle([35,35,W-35,H-35],outline=(70,62,36),width=1)

def tlen(t,f): return d.textlength(t,font=f)
def center(y,t,f,fill): d.text((cx-tlen(t,f)/2,y),t,font=f,fill=fill)
def tracked(y,t,f,fill,tr,ox=0):
    tot=sum(tlen(c,f)+tr for c in t)-tr; x=cx-tot/2+ox
    for ch in t: d.text((x,y),ch,font=f,fill=fill); x+=tlen(ch,f)+tr
def diamond(px,py,s,fill):
    d.polygon([(px,py-s),(px+s,py),(px,py+s),(px-s,py)],fill=fill)

# --- kicker with flanking diamonds ---
ky=104; kf=font(23)
ktxt="IF THE ENHANCEMENT MILLAGE PASSES, WE ASK THE DISTRICT TO"
tracked(ky,ktxt,kf,GOLD,4)
kw=sum(tlen(c,kf)+4 for c in ktxt)-4
diamond(cx-kw/2-26,ky+15,5,GOLD); diamond(cx+kw/2+26,ky+15,5,GOLD)

# --- HERO: Dedicate / 100% / to special education ---
center(158,"DEDICATE",font(34),CREAM)
# 100% with a soft drop shadow for weight
big=font(150)
n="100%"; nx=cx-tlen(n,big)/2
d.text((nx+3,205+3),n,font=big,fill=(0,0,0))
d.text((nx,205),n,font=big,fill=GOLDB)
tracked(372,"TO FULLY FUND SPECIAL EDUCATION",font(43),CREAM,3)

# --- accountability line ---
sub=font(31,bold=False)
center(452,"Fund the gap the District itself named. Then track and report, every year,",sub,CREAM)
center(490,"how much general-fund money it frees for classrooms.",sub,CREAM)

# --- divider with center diamond ---
dy=560
d.line([cx-300,dy,cx-26,dy],fill=GOLDDIM,width=2); d.line([cx+26,dy,cx+300,dy],fill=GOLDDIM,width=2)
diamond(cx,dy,7,GOLD)

# --- CTA ---
cta_a="VOTE TUESDAY, AUGUST 4"; cta_b="tsd-enhancementmillage.karpowitsch.org"
fa=font(27); fb2=font(27,bold=False)
gap=44
total=tlen(cta_a,fa)+gap+tlen(cta_b,fb2)
x0=cx-total/2
d.text((x0,600),cta_a,font=fa,fill=GOLDB)
diamond(x0+tlen(cta_a,fa)+gap/2,617,6,GOLD)
d.text((x0+tlen(cta_a,fa)+gap,600),cta_b,font=fb2,fill=CREAM)

out="./tsd_group_banner.png"
img.save(out); img.save(os.path.expanduser("~/Downloads/TSD_group_banner.png"))
print("saved",img.size)
