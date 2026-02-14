#!/usr/bin/env python3
import json, os
import fontforge, psMat

ROOT = os.path.dirname(__file__)
PARAMS_PATH = os.path.join(ROOT, 'ga10_editor_params.json')
SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV275.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV289_Ga10Editor.otf')

MACRON = 0xFE20
RING_ABOVE = 0x030A
RING_BELOW = 0x0325
TILDE_BELOW = 0x0330
TRI_BELOW = 0x02D1

CP = {
    'ga': 0xAC00, 'gan': 0xAC04, 'gang': 0xAC15,
    'kka': 0xAE4C, 'kkan': 0xAE50, 'kkang': 0xAE61, 'kkin': 0xB080,
}

with open(PARAMS_PATH, 'r', encoding='utf-8') as f:
    P = json.load(f)

font = fontforge.open(SRC)
for lk in list(font.gsub_lookups):
    try: font.removeLookup(lk)
    except: pass

# Ensure filled triangle at U+02D1
if TRI_BELOW not in font:
    srcg = None
    for c in (0x25BE, 0x25BC, 0x25BF):
        if c in font: srcg = font[c]; break
    if srcg is None:
        nf = fontforge.open(os.path.expanduser('~/Library/Fonts/NanumMyeongjo-Regular.ttf'))
        for c in (0x25BE, 0x25BC, 0x25BF):
            if c in nf:
                nf.selection.select(c); nf.copy(); font.selection.select(c); font.paste(); srcg=font[c]; break
        nf.close()
    if srcg is not None:
        font.createChar(TRI_BELOW, 'uni02D1')
        g = font[TRI_BELOW]; g.clear()
        bb = srcg.boundingBox(); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
        m = psMat.compose(psMat.translate(-cx,-cy), psMat.scale(0.43))
        m = psMat.compose(m, psMat.translate(180, 390))
        g.addReference(srcg.glyphname, m); g.width = 360

lookup='rlig_v289_ga10'
font.addLookup(lookup,'gsub_ligature',(),(("rlig",(("DFLT",("dflt",)),("hang",("dflt",)))),))
font.addLookupSubtable(lookup,'rlig_v289_ga10_sub')
sub='rlig_v289_ga10_sub'

S0=0xF100
step=0

def pct(v): return max(0.2, v/100.0)

def add_ref(g, mark, tx, ty, sx=1.0, sy=1.0):
    mg=font[mark]; bb=mg.boundingBox(); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
    mat=psMat.compose(psMat.translate(-cx,-cy), psMat.scale(sx,sy))
    mat=psMat.compose(mat, psMat.translate(tx,ty))
    g.addReference(mg.glyphname, mat)

def draw_ring_scaled(g,cx,cy,sw=1.0,sh=1.0,r_out=90,r_in=60):
    pen=g.glyphPen(); k=0.5522
    rox,roy=r_out*sw,r_out*sh; rix,riy=r_in*sw,r_in*sh
    pen.moveTo((cx-rox,cy)); pen.curveTo((cx-rox,cy+roy*k),(cx-rox*k,cy+roy),(cx,cy+roy)); pen.curveTo((cx+rox*k,cy+roy),(cx+rox,cy+roy*k),(cx+rox,cy)); pen.curveTo((cx+rox,cy-roy*k),(cx+rox*k,cy-roy),(cx,cy-roy)); pen.curveTo((cx-rox*k,cy-roy),(cx-rox,cy-roy*k),(cx-rox,cy)); pen.closePath()
    pen.moveTo((cx+rix,cy)); pen.curveTo((cx+rix,cy+riy*k),(cx+rix*k,cy+riy),(cx,cy+riy)); pen.curveTo((cx-rix*k,cy+riy),(cx-rix,cy+riy*k),(cx-rix,cy)); pen.curveTo((cx-rix,cy-riy*k),(cx-rix*k,cy-riy),(cx,cy-riy)); pen.curveTo((cx+rix*k,cy-riy),(cx+rix,cy-riy*k),(cx+rix,cy)); pen.closePath(); g.correctDirection()

def newg():
    global step
    c=S0+step; step+=1; font.createChar(c); g=font[c]; g.clear(); return g

def lig_single(base_cp, mark_cp, pos):
    b=font[base_cp]
    g=newg()
    if mark_cp in (RING_ABOVE, RING_BELOW):
        draw_ring_scaled(g, pos['x'], pos['y'], pct(pos['width']), pct(pos['height']))
    elif mark_cp==TILDE_BELOW:
        add_ref(g, mark_cp, pos['x'], pos['y'], sx=pct(pos['width']), sy=pct(pos['height'])*1.15)
    else:
        add_ref(g, mark_cp, pos['x'], pos['y'], sx=pct(pos['width']), sy=pct(pos['height']))
    g.addReference(b.glyphname); g.width=b.width
    g.addPosSub(sub,(b.glyphname,font[mark_cp].glyphname))

def lig_combo(base_cp, p_top, p_mac):
    b=font[base_cp]
    g=newg()
    draw_ring_scaled(g, p_top['x'], p_top['y'], pct(p_top['width']), pct(p_top['height']))
    add_ref(g, MACRON, p_mac['x'], p_mac['y'], sx=pct(p_mac['width'])*1.5, sy=pct(p_mac['height']))
    g.addReference(b.glyphname); g.width=b.width
    g.addPosSub(sub,(b.glyphname,font[RING_ABOVE].glyphname,font[MACRON].glyphname))
    g.addPosSub(sub,(b.glyphname,font[MACRON].glyphname,font[RING_ABOVE].glyphname))

# 1) 가+장음
lig_single(CP['ga'], MACRON, P['id1_mac'])
# 2) 가+윗점+장음
lig_combo(CP['ga'], P['id2_top'], P['id2_mac'])
# 3) 가+윗점
lig_single(CP['ga'], RING_ABOVE, P['id3_top'])
# 4) 간+아랫점
lig_single(CP['gan'], RING_BELOW, P['id4_bot'])
# 5) 강+윗점
lig_single(CP['gang'], RING_ABOVE, P['id5_top'])
# 6) 강+아랫역삼각형
lig_single(CP['gang'], TRI_BELOW, P['id6_tri'])
# 7) 까+장음
lig_single(CP['kka'], MACRON, P['id7_mac'])
# 8) 깐+아랫물결
lig_single(CP['kkan'], TILDE_BELOW, P['id8_tilde'])
# 9) 깡+아랫역삼각형
lig_single(CP['kkang'], TRI_BELOW, P['id9_tri'])
# 10) 낀+아랫물결
lig_single(CP['kkin'], TILDE_BELOW, P['id10_tilde'])

font.fontname='PaliHangulV289Ga10Editor'
font.familyname='PaliHangul V289 Ga10 Editor'
font.fullname='PaliHangul V289 Ga10 Editor'
font.version='2.89-ga10-editor'
font.generate(OUT)
font.close()
print('Generated', OUT)
