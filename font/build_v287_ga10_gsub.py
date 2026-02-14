#!/usr/bin/env python3
"""v2.85 - ga-series 10 items, GSUB-internal positioning only (no CSS overlay)."""
import os
import fontforge
import psMat

SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV275.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV287_Ga10.otf')

MACRON = 0xFE20
RING_ABOVE = 0x030A   # 윗점
RING_BELOW = 0x0325   # 아랫점
TILDE_BELOW = 0x0330  # 아랫물결
TRI_BELOW = 0x02D1    # 아랫 역삼각형

BASES = {
    'ga': 0xAC00, 'gan': 0xAC04, 'gang': 0xAC15,
    'kka': 0xAE4C, 'kkan': 0xAE50, 'kkang': 0xAE61,
    'kkin': 0xB080,
}

# per-base tuned anchors (from JB feedback)
P = {
    'ga':   {'top_x':0.14, 'top_gap':-12, 'bot_x':0.14, 'bot_gap':10, 'mac_x':0.378, 'mac_gap':18},
    'gan':  {'top_x':0.14, 'top_gap':6, 'bot_x':0.63, 'bot_gap':22, 'mac_x':0.40, 'mac_gap':7},
    'gang': {'top_x':0.14, 'top_gap':8, 'bot_x':0.86, 'bot_gap':10, 'mac_x':0.40, 'mac_gap':7},
    'kka':  {'top_x':0.16, 'top_gap':8, 'bot_x':0.16, 'bot_gap':10, 'mac_x':0.382, 'mac_gap':8},
    'kkan': {'top_x':0.16, 'top_gap':6, 'bot_x':0.66, 'bot_gap':22, 'mac_x':0.41, 'mac_gap':7},
    'kkang':{'top_x':0.16, 'top_gap':8, 'bot_x':0.86, 'bot_gap':10, 'mac_x':0.41, 'mac_gap':7},
    'kkin': {'top_x':0.16, 'top_gap':8, 'bot_x':0.70, 'bot_gap':22, 'mac_x':0.41, 'mac_gap':7},
}

font = fontforge.open(SRC)
for lk in list(font.gsub_lookups):
    try: font.removeLookup(lk)
    except: pass

# ensure triangle glyph exists
if TRI_BELOW not in font:
    srcg = None
    # prefer FILLED down-triangle glyphs: U+25BE, fallback U+25BC, then white U+25BF
    for c in (0x25BE, 0x25BC, 0x25BF):
        if c in font:
            srcg = font[c]
            break
    if srcg is None:
        try:
            nf = fontforge.open(os.path.expanduser('~/Library/Fonts/NanumMyeongjo-Regular.ttf'))
            for c in (0x25BE, 0x25BC, 0x25BF):
                if c in nf:
                    nf.selection.select(c); nf.copy(); font.selection.select(c); font.paste()
                    srcg = font[c]
                    break
            nf.close()
        except Exception:
            pass
    if srcg is not None:
        font.createChar(TRI_BELOW, 'uni02D1')
        g = font[TRI_BELOW]; g.clear()
        bb = srcg.boundingBox(); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
        m = psMat.compose(psMat.translate(-cx,-cy), psMat.scale(0.43))
        m = psMat.compose(m, psMat.translate(180, 390))
        g.addReference(srcg.glyphname, m); g.width = 360

lookup='rlig_v287_ga10'
font.addLookup(lookup,'gsub_ligature',(),(("rlig",(("DFLT",("dflt",)),("hang",("dflt",)))),))
font.addLookupSubtable(lookup,'rlig_v285_ga10_sub')
sub='rlig_v285_ga10_sub'

S0=0xEE00
step=0

def add_ref(g, mark, tx, ty, sx=1.0, sy=1.0):
    mg = font[mark]; bb=mg.boundingBox(); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
    if sx!=1.0 or sy!=1.0:
        mat=psMat.compose(psMat.translate(-cx,-cy), psMat.scale(sx,sy)); mat=psMat.compose(mat, psMat.translate(tx,ty))
    else:
        mat=psMat.translate(tx-cx, ty-cy)
    g.addReference(mg.glyphname, mat)

def draw_ring(g,cx,cy,r_out=90,r_in=60):
    pen=g.glyphPen(); k=0.5522
    pen.moveTo((cx-r_out,cy)); pen.curveTo((cx-r_out,cy+r_out*k),(cx-r_out*k,cy+r_out),(cx,cy+r_out)); pen.curveTo((cx+r_out*k,cy+r_out),(cx+r_out,cy+r_out*k),(cx+r_out,cy)); pen.curveTo((cx+r_out,cy-r_out*k),(cx+r_out*k,cy-r_out),(cx,cy-r_out)); pen.curveTo((cx-r_out*k,cy-r_out),(cx-r_out,cy-r_out*k),(cx-r_out,cy)); pen.closePath()
    pen.moveTo((cx+r_in,cy)); pen.curveTo((cx+r_in,cy+r_in*k),(cx+r_in*k,cy+r_in),(cx,cy+r_in)); pen.curveTo((cx-r_in*k,cy+r_in),(cx-r_in,cy+r_in*k),(cx-r_in,cy)); pen.curveTo((cx-r_in,cy-r_in*k),(cx-r_in*k,cy-r_in),(cx,cy-r_in)); pen.curveTo((cx+r_in*k,cy-r_in),(cx+r_in,cy-r_in*k),(cx+r_in,cy)); pen.closePath(); g.correctDirection()

for name,cp in BASES.items():
    base=font[cp]; xmin,ymin,xmax,ymax=base.boundingBox(); w=xmax-xmin
    p=P[name]
    top=(int(xmin+w*p['top_x']), int(ymax+p['top_gap']))
    bot=(int(xmin+w*p['bot_x']), int(ymin-p['bot_gap']))
    mac=(int(xmin+w*p['mac_x']), int(ymax+p['mac_gap']))

    def mk_single(mark, key='top', use_ring=False, is_tilde=False, sx=1.0):
        global step
        c=S0+step; step+=1; font.createChar(c); g=font[c]; g.clear()
        pos = top if key=='top' else bot
        if use_ring:
            draw_ring(g,pos[0],pos[1])
        else:
            add_ref(g, mark, pos[0], pos[1], sx=sx, sy=(1.15 if is_tilde else 1.0))
        g.addReference(base.glyphname); g.width=base.width; return g, c

    # macron
    c=S0+step; step+=1; font.createChar(c); g=font[c]; g.clear()
    add_ref(g, MACRON, mac[0], mac[1], sx=1.5); g.addReference(base.glyphname); g.width=base.width
    g.addPosSub(sub,(base.glyphname,font[MACRON].glyphname))

    # ring above/below
    g1,c1 = mk_single(RING_ABOVE,'top',use_ring=True)
    g1.addPosSub(sub,(base.glyphname,font[RING_ABOVE].glyphname))
    g2,c2 = mk_single(RING_BELOW,'bot',use_ring=True)
    g2.addPosSub(sub,(base.glyphname,font[RING_BELOW].glyphname))

    # tilde below
    g3,c3 = mk_single(TILDE_BELOW,'bot',is_tilde=True)
    g3.addPosSub(sub,(base.glyphname,font[TILDE_BELOW].glyphname))

    # triangle below
    c=S0+step; step+=1; font.createChar(c); gt=font[c]; gt.clear()
    add_ref(gt, TRI_BELOW, bot[0], bot[1]); gt.addReference(base.glyphname); gt.width=base.width
    gt.addPosSub(sub,(base.glyphname,font[TRI_BELOW].glyphname))

    # ring above + macron (2번)
    c=S0+step; step+=1; font.createChar(c); gc=font[c]; gc.clear()
    draw_ring(gc, top[0], top[1]); add_ref(gc, MACRON, mac[0], mac[1], sx=1.5)
    gc.addReference(base.glyphname); gc.width=base.width
    gc.addPosSub(sub,(base.glyphname,font[RING_ABOVE].glyphname,font[MACRON].glyphname))
    gc.addPosSub(sub,(base.glyphname,font[MACRON].glyphname,font[RING_ABOVE].glyphname))

font.fontname='PaliHangulV287Ga10'
font.familyname='PaliHangul V287 Ga10'
font.fullname='PaliHangul V287 Ga10'
font.version='2.87-ga10'
font.generate(OUT)
font.close()
print('Generated',OUT)
