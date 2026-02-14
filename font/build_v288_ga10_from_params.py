#!/usr/bin/env python3
import json, os
import fontforge, psMat

ROOT = os.path.dirname(__file__)
PARAMS_PATH = os.path.join(ROOT, 'ga10_editor_params.json')
SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV275.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV288_Ga10Editor.otf')

MACRON = 0xFE20
RING_ABOVE = 0x030A
RING_BELOW = 0x0325
TILDE_BELOW = 0x0330
TRI_BELOW = 0x02D1

BASES = {
    'ga': 0xAC00, 'gan': 0xAC04, 'gang': 0xAC15,
    'kka': 0xAE4C, 'kkan': 0xAE50, 'kkang': 0xAE61, 'kkin': 0xB080,
}

with open(PARAMS_PATH, 'r', encoding='utf-8') as f:
    U = json.load(f)

font = fontforge.open(SRC)
for lk in list(font.gsub_lookups):
    try: font.removeLookup(lk)
    except: pass

# ensure filled triangle for U+02D1
if TRI_BELOW not in font:
    srcg = None
    for c in (0x25BE, 0x25BC, 0x25BF):
        if c in font:
            srcg = font[c]; break
    if srcg is None:
        nf = fontforge.open(os.path.expanduser('~/Library/Fonts/NanumMyeongjo-Regular.ttf'))
        for c in (0x25BE, 0x25BC, 0x25BF):
            if c in nf:
                nf.selection.select(c); nf.copy(); font.selection.select(c); font.paste(); srcg = font[c]; break
        nf.close()
    if srcg is not None:
        font.createChar(TRI_BELOW, 'uni02D1')
        g = font[TRI_BELOW]; g.clear()
        bb = srcg.boundingBox(); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
        m = psMat.compose(psMat.translate(-cx,-cy), psMat.scale(0.43))
        m = psMat.compose(m, psMat.translate(180, 390))
        g.addReference(srcg.glyphname, m); g.width = 360

lookup='rlig_v288_ga10'
font.addLookup(lookup,'gsub_ligature',(),(("rlig",(("DFLT",("dflt",)),("hang",("dflt",)))),))
font.addLookupSubtable(lookup,'rlig_v288_ga10_sub')
sub='rlig_v288_ga10_sub'

S0=0xEF00
step=[0]

def add_ref(g, mark, tx, ty, sx=1.0, sy=1.0):
    mg = font[mark]; bb=mg.boundingBox(); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
    mat = psMat.compose(psMat.translate(-cx,-cy), psMat.scale(sx,sy))
    mat = psMat.compose(mat, psMat.translate(tx,ty))
    g.addReference(mg.glyphname, mat)

def draw_ring_scaled(g,cx,cy,scale_w=1.0,scale_h=1.0,r_out=90,r_in=60):
    pen=g.glyphPen(); k=0.5522
    rox,roy=r_out*scale_w,r_out*scale_h
    rix,riy=r_in*scale_w,r_in*scale_h
    pen.moveTo((cx-rox,cy)); pen.curveTo((cx-rox,cy+roy*k),(cx-rox*k,cy+roy),(cx,cy+roy)); pen.curveTo((cx+rox*k,cy+roy),(cx+rox,cy+roy*k),(cx+rox,cy)); pen.curveTo((cx+rox,cy-roy*k),(cx+rox*k,cy-roy),(cx,cy-roy)); pen.curveTo((cx-rox*k,cy-roy),(cx-rox,cy-roy*k),(cx-rox,cy)); pen.closePath()
    pen.moveTo((cx+rix,cy)); pen.curveTo((cx+rix,cy+riy*k),(cx+rix*k,cy+riy),(cx,cy+riy)); pen.curveTo((cx-rix*k,cy+riy),(cx-rix,cy+riy*k),(cx-rix,cy)); pen.curveTo((cx-rix,cy-riy*k),(cx-rix*k,cy-riy),(cx,cy-riy)); pen.curveTo((cx+rix*k,cy-riy),(cx+rix,cy-riy*k),(cx+rix,cy)); pen.closePath(); g.correctDirection()

def pct(v):
    return max(0.2, v/100.0)

# helpers to use id params
ID = U

# build target glyphs only
for name,cp in BASES.items():
    base=font[cp]

    # ids mapping
    p1=ID['id1']; p2=ID['id2']; p3=ID['id3']; p4=ID['id4']; p5=ID['id5']; p6=ID['id6']; p7=ID['id7']; p8=ID['id8']; p9=ID['id9']; p10=ID['id10']

    # choose per base anchors from ids
    if name=='ga': top=p3; bot=p4; mac=p1
    elif name=='gan': top=p3; bot=p4; mac=p1
    elif name=='gang': top=p5; bot=p6; mac=p1
    elif name=='kka': top=p5; bot=p8; mac=p7
    elif name=='kkan': top=p5; bot=p8; mac=p7
    elif name=='kkang': top=p5; bot=p9; mac=p7
    elif name=='kkin': top=p5; bot=p10; mac=p7

    def newg():
        c=S0+step[0]; step[0]+=1; font.createChar(c); g=font[c]; g.clear(); return g

    # macron
    g=newg(); add_ref(g, MACRON, mac['x'], mac['y'], sx=pct(mac['width'])*1.5, sy=pct(mac['height'])); g.addReference(base.glyphname); g.width=base.width
    g.addPosSub(sub,(base.glyphname,font[MACRON].glyphname))

    # top ring
    g=newg(); draw_ring_scaled(g, top['x'], top['y'], pct(top['width']), pct(top['height'])); g.addReference(base.glyphname); g.width=base.width
    g.addPosSub(sub,(base.glyphname,font[RING_ABOVE].glyphname))

    # bottom ring
    g=newg(); draw_ring_scaled(g, bot['x'], bot['y'], pct(bot['width']), pct(bot['height'])); g.addReference(base.glyphname); g.width=base.width
    g.addPosSub(sub,(base.glyphname,font[RING_BELOW].glyphname))

    # bottom tilde
    g=newg(); add_ref(g, TILDE_BELOW, bot['x'], bot['y'], sx=pct(bot['width']), sy=pct(bot['height'])*1.15); g.addReference(base.glyphname); g.width=base.width
    g.addPosSub(sub,(base.glyphname,font[TILDE_BELOW].glyphname))

    # bottom triangle
    g=newg(); add_ref(g, TRI_BELOW, bot['x'], bot['y'], sx=pct(bot['width']), sy=pct(bot['height'])); g.addReference(base.glyphname); g.width=base.width
    g.addPosSub(sub,(base.glyphname,font[TRI_BELOW].glyphname))

    # top ring + macron combo
    g=newg(); draw_ring_scaled(g, p2['x'], p2['y'], pct(p2['width']), pct(p2['height'])); add_ref(g, MACRON, p2['x']+216, p2['y']+30, sx=pct(p2['width'])*1.5, sy=pct(p2['height']))
    g.addReference(base.glyphname); g.width=base.width
    g.addPosSub(sub,(base.glyphname,font[RING_ABOVE].glyphname,font[MACRON].glyphname))
    g.addPosSub(sub,(base.glyphname,font[MACRON].glyphname,font[RING_ABOVE].glyphname))

font.fontname='PaliHangulV288Ga10Editor'
font.familyname='PaliHangul V288 Ga10 Editor'
font.fullname='PaliHangul V288 Ga10 Editor'
font.version='2.88-ga10-editor'
font.generate(OUT)
font.close()
print('Generated', OUT)
