#!/usr/bin/env python3
import json, os
import fontforge, psMat

ROOT = os.path.dirname(__file__)
PARAMS_PATH = os.path.join(ROOT, 'ga10_editor_params.json')
SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV275.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV289_Ga10Editor.otf')

MACRON = 0xFE20
TOP = 0x030A          # 윗점
BOT_DOT = 0x0325      # 아랫점
BOT_TILDE = 0x0330    # 아랫물결
BOT_TRI = 0x02D1      # 아랫 역삼각형

with open(PARAMS_PATH, 'r', encoding='utf-8') as f:
    P = json.load(f)

font = fontforge.open(SRC)
for lk in list(font.gsub_lookups):
    try: font.removeLookup(lk)
    except: pass

# ensure filled triangle at U+02D1
if BOT_TRI not in font:
    srcg = None
    for c in (0x25BE, 0x25BC, 0x25BF):
        if c in font:
            srcg = font[c]
            break
    if srcg is None:
        nf = fontforge.open(os.path.expanduser('~/Library/Fonts/NanumMyeongjo-Regular.ttf'))
        for c in (0x25BE, 0x25BC, 0x25BF):
            if c in nf:
                nf.selection.select(c); nf.copy(); font.selection.select(c); font.paste(); srcg = font[c]; break
        nf.close()
    if srcg is not None:
        font.createChar(BOT_TRI, 'uni02D1')
        g = font[BOT_TRI]; g.clear()
        bb = srcg.boundingBox(); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
        m = psMat.compose(psMat.translate(-cx,-cy), psMat.scale(0.43))
        m = psMat.compose(m, psMat.translate(180, 390))
        g.addReference(srcg.glyphname, m); g.width = 360

lookup='rlig_v289_editor'
font.addLookup(lookup,'gsub_ligature',(),(("rlig",(("DFLT",("dflt",)),("hang",("dflt",)))),))
font.addLookupSubtable(lookup,'rlig_v289_editor_sub')
sub='rlig_v289_editor_sub'

S0=0xF100
step=0

def _dim(v, fallback=100):
    try: n=float(v)
    except: n=float(fallback)
    return max(1.0, n)

def newg():
    global step
    cp=S0+step; step+=1
    font.createChar(cp)
    g=font[cp]; g.clear()
    return g

def add_ref_abs(g, mark, tx, ty, target_w, target_h):
    mg = font[mark]
    bb = mg.boundingBox()
    src_w = max(1.0, bb[2]-bb[0])
    src_h = max(1.0, bb[3]-bb[1])
    cx = (bb[0]+bb[2])/2.0
    cy = (bb[1]+bb[3])/2.0
    sx = _dim(target_w)/src_w
    sy = _dim(target_h)/src_h
    mat = psMat.compose(psMat.translate(-cx,-cy), psMat.scale(sx,sy))
    mat = psMat.compose(mat, psMat.translate(tx,ty))
    g.addReference(mg.glyphname, mat)

def draw_ring_abs(g, cx, cy, outer_w, outer_h):
    pen=g.glyphPen(); k=0.5522
    rox=_dim(outer_w)/2.0; roy=_dim(outer_h)/2.0
    rix=rox*0.66; riy=roy*0.66
    pen.moveTo((cx-rox,cy)); pen.curveTo((cx-rox,cy+roy*k),(cx-rox*k,cy+roy),(cx,cy+roy)); pen.curveTo((cx+rox*k,cy+roy),(cx+rox,cy+roy*k),(cx+rox,cy)); pen.curveTo((cx+rox,cy-roy*k),(cx+rox*k,cy-roy),(cx,cy-roy)); pen.curveTo((cx-rox*k,cy-roy),(cx-rox,cy-roy*k),(cx-rox,cy)); pen.closePath()
    pen.moveTo((cx+rix,cy)); pen.curveTo((cx+rix,cy+riy*k),(cx+rix*k,cy+riy),(cx,cy+riy)); pen.curveTo((cx-rix*k,cy+riy),(cx-rix,cy+riy*k),(cx-rix,cy)); pen.curveTo((cx-rix,cy-riy*k),(cx-rix*k,cy-riy),(cx,cy-riy)); pen.curveTo((cx+rix*k,cy-riy),(cx+rix,cy-riy*k),(cx+rix,cy)); pen.closePath()
    g.correctDirection()

def draw_mark(g, mark, pos):
    if mark in (TOP, BOT_DOT):
        draw_ring_abs(g, pos['x'], pos['y'], pos['width'], pos['height'])
    else:
        add_ref_abs(g, mark, pos['x'], pos['y'], pos['width'], pos['height'])

def lig_single(base_char, mark, pos_key):
    if pos_key not in P: return
    b = font[ord(base_char)]
    g = newg()
    draw_mark(g, mark, P[pos_key])
    g.addReference(b.glyphname); g.width=b.width
    g.addPosSub(sub,(b.glyphname,font[mark].glyphname))

def lig_combo2(base_char, markA, keyA, markB, keyB):
    if keyA not in P or keyB not in P: return
    b = font[ord(base_char)]
    g = newg()
    draw_mark(g, markA, P[keyA])
    draw_mark(g, markB, P[keyB])
    g.addReference(b.glyphname); g.width=b.width
    g.addPosSub(sub,(b.glyphname,font[markA].glyphname,font[markB].glyphname))
    g.addPosSub(sub,(b.glyphname,font[markB].glyphname,font[markA].glyphname))

# --- 가계열 ---
lig_single('가', MACRON, 'id1_mac')
lig_combo2('가', TOP, 'id2_top', MACRON, 'id2_mac')
lig_single('가', TOP, 'id3_top')
lig_single('간', BOT_DOT, 'id4_bot')
lig_single('강', TOP, 'id5_top')
lig_single('강', BOT_TRI, 'id6_tri')
lig_single('까', MACRON, 'id7_mac')
lig_single('깐', BOT_TILDE, 'id8_tilde')
lig_single('깡', BOT_TRI, 'id9_tri')
lig_single('낀', BOT_TILDE, 'id10_tilde')

# --- 나계열 ---
lig_single('나', MACRON, 'na1_mac')
lig_single('나', BOT_DOT, 'na2_top')          # 윗점 -> 아랫점 변경
lig_combo2('나', BOT_DOT, 'na3_top', MACRON, 'na3_mac')
lig_single('낙', MACRON, 'na4_mac')
lig_combo2('난', BOT_DOT, 'na5_top', BOT_TILDE, 'na5_tilde')
lig_single('난', BOT_DOT, 'na6_top')
lig_single('난', BOT_TILDE, 'na7_tilde')
lig_combo2('난', MACRON, 'na8_mac', BOT_TILDE, 'na8_tilde')
lig_single('낫', BOT_DOT, 'na9_top')
lig_single('낭', BOT_DOT, 'na10_top')
lig_single('낭', BOT_TRI, 'na11_tri')
lig_single('냐', BOT_DOT, 'na12_top')
lig_combo2('냐', BOT_DOT, 'na13_top', MACRON, 'na13_mac')
lig_single('냣', BOT_TILDE, 'na14_tilde')
lig_single('냥', BOT_TILDE, 'na15_tilde')
lig_combo2('누', BOT_DOT, 'na16_top', MACRON, 'na16_mac')
lig_single('니', BOT_DOT, 'na17_top')
lig_single('네', TOP, 'na18_top')             # 18번만 윗점 유지

tag = os.environ.get('OC_BUILD_TAG', 'base')
font.fontname=f'PaliHangulV289Ga10Editor_{tag}'
font.familyname=f'PaliHangul V289 Ga10 Editor {tag}'
font.fullname=f'PaliHangul V289 Ga10 Editor {tag}'
font.version=f'2.89-ga10-editor-{tag}'
font.generate(OUT)
font.close()
print('Generated', OUT)
