from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','assets','logo'); FONTS=os.path.join(HERE,'..','assets','fonts'); os.makedirs(OUT,exist_ok=True)
BROWN='#4A3B30'; IVORY='#FAF7EF'

def text_path(fontfile, text, x0, baseline, cap_px, track_em):
    f=TTFont(fontfile); gs=f.getGlyphSet(); cmap=f.getBestCmap()
    cap=f['OS/2'].sCapHeight; upm=f['head'].unitsPerEm
    s=cap_px/cap; pen=SVGPathPen(gs); x=x0
    for ch in text:
        if ch==' ':
            x+=gs[cmap[32]].width*s + track_em*upm*s; continue
        g=cmap[ord(ch)]
        tp=TransformPen(pen,(s,0,0,-s,x,baseline)); gs[g].draw(tp)
        x+=gs[g].width*s + track_em*upm*s
    return pen.getCommands(), x - track_em*upm*s

# Mark: equilateral pointed arch (each flank is an arc of radius = span, centred on the
# opposite foot), symmetric, with short straight legs. The X is the right flank repeated
# half a span to the left. All three feet stand on one baseline.
import math
SPAN=380.0
R=SPAN                                   # equilateral arch
RISE=math.sqrt(R*R-(SPAN/2)**2)          # = span x 0.866
LEG=0.16*SPAN
K=310.0/(RISE+LEG)                       # fit mark height to the site logo (31 px)
MK_W=SPAN*K; MK_H=(RISE+LEG)*K
MK_X=540-MK_W; MK_Y=190                  # right edge where the site mark ends
def mark(sw, s=1.0, x=MK_X, y=MK_Y):
    s=s*K; h=SPAN/2; r=f'{R:.2f} {R:.2f}'; B=RISE+LEG
    d1=f'M0 {B:.2f} V{RISE:.2f} A{r} 0 0 1 {h:.2f} 0 A{r} 0 0 1 {SPAN:.2f} {RISE:.2f} V{B:.2f}'
    d2=f'M{-h:.2f} 0 A{r} 0 0 1 0 {RISE:.2f}'
    d2=f'M0 {0:.2f}'  # placeholder replaced below
    # diagonal: right flank (apex -> right foot) shifted left by half a span
    d2=f'M0 0 A{r} 0 0 1 {h:.2f} {RISE:.2f} V{B:.2f}'
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.5f})" fill="none" stroke="currentColor" '
            f'stroke-width="{sw/s:.2f}" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="20">'
            f'<path d="{d1}"/><path d="{d2}"/></g>')
PF=os.path.join(FONTS,'PlayfairDisplay-700-normal.ttf'); MR=os.path.join(FONTS,'Manrope-600-normal.ttf')
word,wend=text_path(PF,'XANAKA',730,440,180,0.06)

def svg(w,h,body,color,vb_x=0,vb_y=0,title='Xanaka'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x} {vb_y} {w} {h}" '
            f'width="{w/10:g}" height="{h/10:g}" style="color:{color}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

files={}
# horizontal: mark + wordmark
pad=60; x0=MK_X-pad; y0=MK_Y-pad; x1=wend+pad; y1=MK_Y+MK_H+pad
body_h=mark(11)+f'<path fill="currentColor" d="{word}"/>'
for name,col in [('brown',BROWN),('ivory',IVORY)]:
    files[f'xanaka-logo-horizontal-{name}.svg']=svg(x1-x0,y1-y0,body_h,col,x0,y0)
# stacked: mark centered over wordmark + descriptor
mw=560-140; ww=wend-730
cx=(730+wend)/2
k=0.62; mh=MK_H*k; mtop=260-70-mh
desc,dend=text_path(MR,'TRAVEL · UZBEKISTAN',0,0,46,0.28)
dwidth=dend
desc,_=text_path(MR,'TRAVEL · UZBEKISTAN',cx-dwidth/2,530,46,0.28)
body_s=(mark(11, k, cx-MK_W*k/2, mtop)+
        f'<path fill="currentColor" d="{word}"/><path fill="currentColor" d="{desc}"/>')
sx0=min(730,cx-dwidth/2)-pad; sx1=max(wend,cx+dwidth/2)+pad
dy=mtop-190
for name,col in [('brown',BROWN),('ivory',IVORY)]:
    files[f'xanaka-logo-stacked-{name}.svg']=svg(sx1-sx0,(530+pad)-(mtop-pad),body_s,col,sx0,mtop-pad)
# mark only (fine + bold for small sizes), 1 unit margin of 10%
for name,col in [('brown',BROWN),('ivory',IVORY)]:
    m=0.12*MK_H
    files[f'xanaka-mark-{name}.svg']=svg(MK_W+2*m,MK_H+2*m,mark(11,1,m,m),col)
    files[f'xanaka-mark-bold-{name}.svg']=svg(MK_W+2*m,MK_H+2*m,mark(26,1,m,m),col)
for k,v in files.items(): open(f'{OUT}/{k}','w').write(v)
print(sorted(files))
