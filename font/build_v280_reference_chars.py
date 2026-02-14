#!/usr/bin/env python3
"""PaliHangul v2.80 - reference-character pilot

목표: 저장된 reference 타겟 글자( key_mapping.py ROWS ) 전체만 대상으로
기호 위치를 기준 이미지 통계값(top/bot)으로 맞춘 파일럿 폰트 생성.
"""
import os
import fontforge
import psMat
import importlib.util

KM_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reference', 'key_mapping.py')
spec = importlib.util.spec_from_file_location('key_mapping', KM_PATH)
km = importlib.util.module_from_spec(spec)
spec.loader.exec_module(km)
ROWS = km.ROWS

SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV252.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV280refpilot.otf')

MACRON = 0xFE20
CARON = 0x030C
DOUBLE_PRIME = 0x02BA
YA_MARK = 0x0346
RING_ABOVE = 0x030A
RING_BELOW = 0x0325
TILDE_ABOVE = 0x0303
TILDE_BELOW = 0x0330
COMMA = 0x05C0
PERIOD = 0x2225

G1 = {0, 1, 2, 3, 4, 5, 6, 7, 20}
G2 = {8, 12, 13, 17, 18}
G3 = {9, 10, 11, 19}
G4 = {14, 15, 16}

# 기준 이미지 1차 목표값(REFERENCE_POSITION_VALUES.md)
REF_TOP_X = 0.58
REF_BOT_X = 0.53
REF_TOP_GAP = 1
REF_BOT_GAP = 0

PARAMS = {
    'G1a': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 20, 'ring_r_out': 90, 'ring_r_in': 60},
    'G1b': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 15, 'ring_r_out': 90, 'ring_r_in': 60},
    'G2a': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 20, 'ring_r_out': 90, 'ring_r_in': 60},
    'G2b': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 15, 'ring_r_out': 90, 'ring_r_in': 60},
    'G3a': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 20, 'ring_r_out': 90, 'ring_r_in': 60},
    'G3b': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 15, 'ring_r_out': 90, 'ring_r_in': 60},
    'G4a': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 20, 'ring_r_out': 90, 'ring_r_in': 60},
    'G4b': {'top_x_ratio': REF_TOP_X, 'top_y_gap': REF_TOP_GAP, 'bot_x_ratio': REF_BOT_X, 'bot_y_gap': REF_BOT_GAP, 'mac_x_ratio': 0.58, 'mac_y_gap': 1, 'mac_sx': 1.5, 'dp_x_gap': 40, 'dp_y_gap': 80, 'comp_gap': 85, 'comp_up': 15, 'ring_r_out': 90, 'ring_r_in': 60},
}


def decompose(cp):
    s = cp - 0xAC00
    return s // 588, (s % 588) // 28, s % 28


def get_group(V):
    if V in G1: return 'G1'
    if V in G2: return 'G2'
    if V in G3: return 'G3'
    if V in G4: return 'G4'
    return 'G1'


def anchors(base_cp, bb):
    xmin, ymin, xmax, ymax = bb
    w = xmax - xmin
    L, V, T = decompose(base_cp)
    has_jong = T != 0
    grp = get_group(V)
    grp_key = grp + ('b' if has_jong else 'a')
    p = PARAMS[grp_key]

    top_x = int(xmin + w * p['top_x_ratio'])
    top_y = int(ymax + p['top_y_gap'])
    bot_x = int(xmin + w * p['bot_x_ratio'])
    bot_y = int(ymin - p['bot_y_gap'])
    mac_x = int(xmin + w * p['mac_x_ratio'])
    mac_y = int(ymax + p['mac_y_gap'])
    dp_x = int(xmax + p['dp_x_gap'])
    dp_y = int(ymax - p['dp_y_gap'])
    return top_x, top_y, bot_x, bot_y, mac_x, mac_y, dp_x, dp_y, grp_key


def draw_ring(glyph, pen, cx, cy, r_out=90, r_in=60):
    k = 0.5522
    pen.moveTo((cx - r_out, cy))
    pen.curveTo((cx - r_out, cy + r_out * k), (cx - r_out * k, cy + r_out), (cx, cy + r_out))
    pen.curveTo((cx + r_out * k, cy + r_out), (cx + r_out, cy + r_out * k), (cx + r_out, cy))
    pen.curveTo((cx + r_out, cy - r_out * k), (cx + r_out * k, cy - r_out), (cx, cy - r_out))
    pen.curveTo((cx - r_out * k, cy - r_out), (cx - r_out, cy - r_out * k), (cx - r_out, cy))
    pen.closePath()
    pen.moveTo((cx + r_in, cy))
    pen.curveTo((cx + r_in, cy + r_in * k), (cx + r_in * k, cy + r_in), (cx, cy + r_in))
    pen.curveTo((cx - r_in * k, cy + r_in), (cx - r_in, cy + r_in * k), (cx - r_in, cy))
    pen.curveTo((cx - r_in, cy - r_in * k), (cx - r_in * k, cy - r_in), (cx, cy - r_in))
    pen.curveTo((cx + r_in * k, cy - r_in), (cx + r_in, cy - r_in * k), (cx + r_in, cy))
    pen.closePath()
    glyph.correctDirection()


def add_mark_reference(g, mark_glyph, tx, ty, sx=1.0, sy=1.0):
    bb = mark_glyph.boundingBox()
    cx = (bb[0] + bb[2]) / 2.0
    cy = (bb[1] + bb[3]) / 2.0
    if sx != 1.0 or sy != 1.0:
        mat = psMat.compose(psMat.translate(-cx, -cy), psMat.scale(sx, sy))
        mat = psMat.compose(mat, psMat.translate(tx, ty))
    else:
        mat = psMat.translate(tx - cx, ty - cy)
    g.addReference(mark_glyph.glyphname, mat)


# reference 타겟 글자 전체(중복 제거)
BASES = sorted({ord(ch) for row in ROWS for ch in row if 0xAC00 <= ord(ch) <= 0xD7A3})

font = fontforge.open(SRC)
for lk in font.gsub_lookups:
    try:
        font.removeLookup(lk)
    except Exception:
        pass

lookup_name = 'rlig_pali_v280ref'
font.addLookup(lookup_name, 'gsub_ligature', (), (("rlig", (("DFLT", ("dflt",)), ("hang", ("dflt",)))),))
NUM_SUBS = 6
SUBTABLES = [f'rlig_pali_v280ref_sub{i}' for i in range(NUM_SUBS)]
for st in SUBTABLES:
    font.addLookupSubtable(lookup_name, st)

for cp in (COMMA, PERIOD):
    try:
        font[cp].transform(psMat.translate(0, -50))
    except Exception:
        pass

S0 = 0xE900
step = 0
for bi, bcp in enumerate(BASES):
    sub = SUBTABLES[bi % NUM_SUBS]
    base = font[bcp]
    bb = base.boundingBox()
    top_x, top_y, bot_x, bot_y, mac_x, mac_y, dp_x, dp_y, grp_key = anchors(bcp, bb)
    p = PARAMS[grp_key]
    rout, rin, mac_sx = p['ring_r_out'], p['ring_r_in'], p['mac_sx']

    slots = []
    for _ in range(14):
        cp = S0 + step
        step += 1
        font.createChar(cp)
        slots.append(cp)

    cp_mac, cp_car, cp_dpr, cp_ya, cp_ru, cp_rd, cp_tu, cp_td = slots[:8]
    cp_mc, cp_my, cp_mr, cp_md, cp_rdpr, cp_rudpr = slots[8:]

    g = font[cp_mac]; g.clear(); add_mark_reference(g, font[MACRON], mac_x, mac_y, sx=mac_sx); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[MACRON].glyphname))
    g = font[cp_car]; g.clear(); add_mark_reference(g, font[CARON], top_x, top_y); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[CARON].glyphname))
    g = font[cp_dpr]; g.clear(); add_mark_reference(g, font[DOUBLE_PRIME], dp_x, dp_y); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[DOUBLE_PRIME].glyphname))
    g = font[cp_ya];  g.clear(); add_mark_reference(g, font[YA_MARK], top_x, top_y); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[YA_MARK].glyphname))
    g = font[cp_ru]; g.clear(); pen = g.glyphPen(); draw_ring(g, pen, top_x, top_y, rout, rin); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[RING_ABOVE].glyphname))
    g = font[cp_rd]; g.clear(); pen = g.glyphPen(); draw_ring(g, pen, bot_x, bot_y, rout, rin); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[RING_BELOW].glyphname))
    g = font[cp_tu]; g.clear(); add_mark_reference(g, font[TILDE_ABOVE], top_x, top_y, sy=1.15); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[TILDE_ABOVE].glyphname))
    g = font[cp_td]; g.clear(); add_mark_reference(g, font[TILDE_BELOW], bot_x, bot_y, sy=1.15); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[TILDE_BELOW].glyphname))

    comp_gap = p['comp_gap']
    comp_up = p['comp_up']
    mac_comp_y = mac_y + comp_up + (comp_gap // 2)
    sec_comp_y = mac_y + comp_up - (comp_gap // 2)

    def make_compound(cp, m1, m2, p1, p2):
        font.createChar(cp)
        g = font[cp]; g.clear()
        if m1 in (RING_ABOVE, RING_BELOW):
            pen = g.glyphPen(); draw_ring(g, pen, p1[0], p1[1], rout, rin)
        elif m1 == MACRON:
            add_mark_reference(g, font[m1], p1[0], p1[1], sx=mac_sx)
        else:
            add_mark_reference(g, font[m1], p1[0], p1[1])
        if m2 in (RING_ABOVE, RING_BELOW):
            pen = g.glyphPen(); draw_ring(g, pen, p2[0], p2[1], rout, rin)
        elif m2 == MACRON:
            add_mark_reference(g, font[m2], p2[0], p2[1], sx=mac_sx)
        else:
            add_mark_reference(g, font[m2], p2[0], p2[1])
        g.addReference(base.glyphname); g.width = base.width
        g.addPosSub(sub, (base.glyphname, font[m1].glyphname, font[m2].glyphname))
        g.addPosSub(sub, (base.glyphname, font[m2].glyphname, font[m1].glyphname))

    make_compound(cp_mc, MACRON, CARON, (mac_x, mac_comp_y), (top_x, sec_comp_y))
    make_compound(cp_my, MACRON, YA_MARK, (mac_x, mac_comp_y), (top_x, sec_comp_y))
    make_compound(cp_mr, MACRON, RING_ABOVE, (mac_x, mac_y), (top_x, top_y))
    make_compound(cp_md, MACRON, RING_BELOW, (mac_x, mac_y), (bot_x, bot_y))
    make_compound(cp_rudpr, RING_ABOVE, DOUBLE_PRIME, (top_x, top_y), (dp_x, dp_y))
    make_compound(cp_rdpr, RING_BELOW, DOUBLE_PRIME, (bot_x, bot_y), (dp_x, dp_y))

font.fontname = 'PaliHangulV280refpilot'
font.familyname = 'PaliHangul V280 Reference Pilot'
font.fullname = 'PaliHangul V280 Reference Pilot'
font.version = '2.80-refpilot'
font.generate(OUT)
font.close()
print('Generated:', OUT)
print('BaseCount:', len(BASES))
print('GlyphCountStep:', step)
print('Size:', os.path.getsize(OUT))
