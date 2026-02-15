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
DOUBLE = 0x02BA       # 자음중복
CARON = 0x030C        # 캐론
YA = 0x0346           # 야(꺽쇠)
TOP_TILDE = 0x0303    # 윗물결

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


# ensure marks from Nanum when missing
for code in (DOUBLE, CARON, YA, TOP_TILDE):
    if code not in font:
        try:
            nf = fontforge.open(os.path.expanduser('~/Library/Fonts/NanumMyeongjo-Regular.ttf'))
            if code in nf:
                nf.selection.select(code); nf.copy(); font.selection.select(code); font.paste()
            nf.close()
        except Exception:
            pass

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
    g.addReference(b.glyphname); g.width=b.width
    draw_mark(g, mark, P[pos_key])
    g.addPosSub(sub,(b.glyphname,font[mark].glyphname))

def lig_combo2(base_char, markA, keyA, markB, keyB):
    if keyA not in P or keyB not in P: return
    b = font[ord(base_char)]
    g = newg()
    g.addReference(b.glyphname); g.width=b.width
    draw_mark(g, markA, P[keyA])
    draw_mark(g, markB, P[keyB])
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
lig_single('나', BOT_DOT, 'na2_bot')
lig_combo2('나', BOT_DOT, 'na3_bot', MACRON, 'na3_mac')
lig_single('낙', MACRON, 'na4_mac')
lig_combo2('난', BOT_DOT, 'na5_bot', BOT_TILDE, 'na5_tilde')
lig_single('난', BOT_DOT, 'na6_bot')
lig_single('난', BOT_TILDE, 'na7_tilde')
lig_combo2('난', MACRON, 'na8_mac', BOT_TILDE, 'na8_tilde')
lig_single('낫', BOT_DOT, 'na9_bot')
lig_single('낭', BOT_DOT, 'na10_bot')
lig_single('낭', BOT_TRI, 'na11_tri')
lig_single('냐', BOT_DOT, 'na12_bot')
lig_combo2('냐', BOT_DOT, 'na13_bot', MACRON, 'na13_mac')
lig_single('냣', BOT_TILDE, 'na14_tilde')
lig_single('냥', BOT_TILDE, 'na15_tilde')
lig_combo2('누', BOT_DOT, 'na16_bot', MACRON, 'na16_mac')
lig_single('니', BOT_DOT, 'na17_bot')
lig_single('네', BOT_DOT, 'na18_bot')

# --- 다계열 ---
lig_single('다', MACRON, 'da1_mac')
lig_single('다', TOP, 'da2_top')
lig_combo2('다', TOP, 'da3_top', MACRON, 'da3_mac')
lig_single('담', TOP, 'da4_top')
lig_single('닷', TOP, 'da5_top')
lig_single('당', TOP, 'da6_top')
lig_single('도', TOP, 'da7_top')
lig_single('둣', BOT_DOT, 'da8_bot')
lig_single('디', MACRON, 'da9_mac')
lig_single('디', BOT_DOT, 'da10_bot')
lig_single('디', TOP, 'da11_top')
lig_single('딕', TOP, 'da12_top')
lig_single('딧', BOT_DOT, 'da13_bot')
lig_single('딩', TOP, 'da14_top')
lig_single('데', TOP, 'da15_top')
lig_single('따', MACRON, 'da16_mac')
lig_single('땃', BOT_DOT, 'da17_bot')
lig_single('뚯', BOT_DOT, 'da18_bot')
lig_single('띠', MACRON, 'da19_mac')
lig_single('띠', BOT_DOT, 'da20_bot')
lig_single('띳', BOT_DOT, 'da21_bot')
lig_single('띤', BOT_DOT, 'da22_bot')

# --- 라계열 ---
lig_single('라', MACRON, 'ra1_mac')
lig_combo2('라', MACRON, 'ra2_mac', BOT_DOT, 'ra2_bot')
lig_single('랏', DOUBLE, 'ra3_double')
lig_single('로', TOP_TILDE, 'ra4_tilde_top')
lig_single('로', DOUBLE, 'ra5_double')
lig_single('루', MACRON, 'ra6_mac')
lig_combo2('리', MACRON, 'ra7_mac', BOT_DOT, 'ra7_bot')

# --- 마계열 ---
lig_single('마', MACRON, 'ma1_mac')
lig_single('만', BOT_TILDE, 'ma2_tilde')
lig_single('망', BOT_TRI, 'ma3_tri')
lig_single('뭇', BOT_DOT, 'ma4_bot')
lig_single('무', MACRON, 'ma5_mac')
lig_single('물', MACRON, 'ma6_mac')

# --- 바계열 ---
lig_single('바', MACRON, 'ba1_mac')
lig_single('바', TOP, 'ba2_top')
lig_combo2('바', TOP, 'ba3_top', MACRON, 'ba3_mac')
lig_single('뱌', MACRON, 'ba4_mac')
lig_single('발', MACRON, 'ba5_mac')
lig_combo2('발', MACRON, 'ba6_mac', BOT_DOT, 'ba6_bot')
lig_single('보', TOP, 'ba7_top')
lig_single('붕', TOP, 'ba8_top')
lig_single('부', TOP, 'ba9_top')
lig_combo2('부', TOP, 'ba10_top', MACRON, 'ba10_mac')
lig_single('비', TOP, 'ba11_top')
lig_single('빅', TOP, 'ba12_top')
lig_combo2('빈', TOP, 'ba13_top', BOT_TILDE, 'ba13_tilde')
lig_single('빈', TOP, 'ba14_top')
lig_single('빗', TOP, 'ba15_top')
lig_single('빠', MACRON, 'ba16_mac')
lig_single('빤', BOT_DOT, 'ba17_bot')
lig_single('빤', BOT_TILDE, 'ba18_tilde')
lig_single('빳', BOT_DOT, 'ba19_bot')
lig_single('뿌', MACRON, 'ba20_mac')
lig_single('뿐', BOT_TILDE, 'ba21_tilde')
lig_single('붓', TOP, 'ba22_top')
lig_single('베', TOP, 'ba23_top')

# --- 사계열 ---
lig_single('사', MACRON, 'sa1_mac')
lig_single('산', BOT_TILDE, 'sa2_tilde')
lig_single('상', BOT_TRI, 'sa3_tri')
lig_single('실', MACRON, 'sa4_mac')

# --- 아계열 ---
lig_single('아', MACRON, 'a1_mac')
lig_single('안', BOT_TILDE, 'a2_tilde')
lig_single('앗', BOT_DOT, 'a3_bot')
lig_single('야', DOUBLE, 'a4_double')
lig_single('야', MACRON, 'a5_mac')
lig_combo2('야', MACRON, 'a6_mac', DOUBLE, 'a6_double')
lig_single('얀', BOT_TILDE, 'a7_tilde')
lig_single('오', CARON, 'a8_caron')
lig_single('와', TOP, 'a9_top')
lig_combo2('와', TOP, 'a10_top', MACRON, 'a10_mac')
lig_single('완', BOT_DOT, 'a11_bot')
lig_single('왕', TOP, 'a12_top')
lig_single('왕', BOT_TRI, 'a13_tri')
lig_single('웃', BOT_DOT, 'a14_bot')
lig_combo2('웃', CARON, 'a15_caron', BOT_DOT, 'a15_bot')
lig_single('윈', BOT_TILDE, 'a16_tilde')
lig_single('이', YA, 'a17_ya')
lig_single('잉', YA, 'a18_ya')
lig_combo2('잇', YA, 'a19_ya', BOT_DOT, 'a19_bot')
lig_single('윈', TOP, 'a20_top')

# --- 자계열 ---
lig_single('자', MACRON, 'ja1_mac')
lig_combo2('자', TOP, 'ja2_top', MACRON, 'ja2_mac')
lig_single('짜', MACRON, 'ja3_mac')
lig_single('짠', BOT_TILDE, 'ja4_tilde')
lig_single('찐', BOT_TILDE, 'ja5_tilde')
lig_single('찐', BOT_DOT, 'ja6_bot')
lig_single('지', MACRON, 'ja7_mac')

# --- 차계열 ---
lig_single('차', MACRON, 'cha1_mac')

# --- 카계열 ---
lig_single('카', MACRON, 'ka1_mac')

# --- 타계열 ---
lig_single('타', MACRON, 'ta1_mac')
lig_combo2('타', MACRON, 'ta2_mac', BOT_DOT, 'ta2_bot')
lig_single('탑', BOT_DOT, 'ta3_bot')
lig_combo2('티', MACRON, 'ta4_mac', BOT_DOT, 'ta4_bot')
lig_single('티', BOT_DOT, 'ta5_bot')
lig_single('팅', BOT_DOT, 'ta6_bot')
lig_single('타', BOT_DOT, 'ta7_bot')
lig_single('테', BOT_DOT, 'ta8_bot')

# --- 파계열 ---
lig_single('폿', BOT_DOT, 'pa1_bot')

# --- 하계열 ---
lig_single('후', MACRON, 'ha1_mac')
lig_single('히', MACRON, 'ha2_mac')
lig_single('하', MACRON, 'ha3_mac')

tag = os.environ.get('OC_BUILD_TAG', 'base')
font.fontname=f'PaliHangulV289Ga10Editor_{tag}'
font.familyname=f'PaliHangul V289 Ga10 Editor {tag}'
font.fullname=f'PaliHangul V289 Ga10 Editor {tag}'
font.version=f'2.89-ga10-editor-{tag}'
font.generate(OUT)
font.close()
print('Generated', OUT)
