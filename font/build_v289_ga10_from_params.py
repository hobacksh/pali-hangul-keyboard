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

def _dim(v, fallback=100):
    try:
        n = float(v)
    except Exception:
        n = float(fallback)
    return max(1.0, n)

def add_ref_abs(g, mark, tx, ty, target_w, target_h):
    mg = font[mark]
    bb = mg.boundingBox()
    src_w = max(1.0, bb[2] - bb[0])
    src_h = max(1.0, bb[3] - bb[1])
    cx = (bb[0] + bb[2]) / 2.0
    cy = (bb[1] + bb[3]) / 2.0
    sx = _dim(target_w) / src_w
    sy = _dim(target_h) / src_h
    mat = psMat.compose(psMat.translate(-cx, -cy), psMat.scale(sx, sy))
    mat = psMat.compose(mat, psMat.translate(tx, ty))
    g.addReference(mg.glyphname, mat)

def draw_ring_abs(g, cx, cy, outer_w, outer_h):
    pen = g.glyphPen(); k = 0.5522
    rox = _dim(outer_w) / 2.0
    roy = _dim(outer_h) / 2.0
    # inner ring keeps fixed proportion
    rix = rox * 0.66
    riy = roy * 0.66
    pen.moveTo((cx-rox,cy)); pen.curveTo((cx-rox,cy+roy*k),(cx-rox*k,cy+roy),(cx,cy+roy)); pen.curveTo((cx+rox*k,cy+roy),(cx+rox,cy+roy*k),(cx+rox,cy)); pen.curveTo((cx+rox,cy-roy*k),(cx+rox*k,cy-roy),(cx,cy-roy)); pen.curveTo((cx-rox*k,cy-roy),(cx-rox,cy-roy*k),(cx-rox,cy)); pen.closePath()
    pen.moveTo((cx+rix,cy)); pen.curveTo((cx+rix,cy+riy*k),(cx+rix*k,cy+riy),(cx,cy+riy)); pen.curveTo((cx-rix*k,cy+riy),(cx-rix,cy+riy*k),(cx-rix,cy)); pen.curveTo((cx-rix,cy-riy*k),(cx-rix*k,cy-riy),(cx,cy-riy)); pen.curveTo((cx+rix*k,cy-riy),(cx+rix,cy-riy*k),(cx+rix,cy)); pen.closePath(); g.correctDirection()

def newg():
    global step
    c=S0+step; step+=1; font.createChar(c); g=font[c]; g.clear(); return g

def lig_single(base_cp, mark_cp, pos):
    b=font[base_cp]
    g=newg()
    w = _dim(pos.get('width', 100))
    h = _dim(pos.get('height', 100))
    if mark_cp in (RING_ABOVE, RING_BELOW):
        draw_ring_abs(g, pos['x'], pos['y'], w, h)
    elif mark_cp==TILDE_BELOW:
        add_ref_abs(g, mark_cp, pos['x'], pos['y'], w, h)
    else:
        add_ref_abs(g, mark_cp, pos['x'], pos['y'], w, h)
    g.addReference(b.glyphname); g.width=b.width
    g.addPosSub(sub,(b.glyphname,font[mark_cp].glyphname))

def lig_combo(base_cp, p_top, p_mac):
    b=font[base_cp]
    g=newg()
    draw_ring_abs(g, p_top['x'], p_top['y'], _dim(p_top.get('width', 100)), _dim(p_top.get('height', 100)))
    # macron width is absolute; apply legacy 1.5x feel by defaulting larger base width in params if needed
    add_ref_abs(g, MACRON, p_mac['x'], p_mac['y'], _dim(p_mac.get('width', 100))*1.5, _dim(p_mac.get('height', 100)))
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

tag = os.environ.get('OC_BUILD_TAG', 'base')
font.fontname=f'PaliHangulV289Ga10Editor_{tag}'
font.familyname=f'PaliHangul V289 Ga10 Editor {tag}'
font.fullname=f'PaliHangul V289 Ga10 Editor {tag}'
font.version=f'2.89-ga10-editor-{tag}'
font.generate(OUT)
font.close()
print('Generated', OUT)
