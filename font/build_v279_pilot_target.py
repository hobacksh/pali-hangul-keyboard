#!/usr/bin/env python3
"""PaliHangul v2.77 — Tight placement engine with explicit tunable values per group.

원칙: 자음의 상단/하단 중앙에 거의 붙을 정도로(1px 미만). 겹침 금지.
수치: x_offset, y_offset, mark_height_scale, mark_width_scale
"""
import os
import fontforge
import psMat

SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV252.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV279pilot.otf')

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

DOUBLE_CHO = {1, 4, 8, 10, 13}

# ============================================================
# 모음 그룹 분류
# ============================================================
G1 = {0, 1, 2, 3, 4, 5, 6, 7, 20}      # 세로형: ㅏㅐㅑㅒㅓㅔㅕㅖㅣ
G2 = {8, 12, 13, 17, 18}                 # 가로형: ㅗㅛㅜㅠㅡ
G3 = {9, 10, 11, 19}                     # 복합A: ㅘㅙㅚㅢ
G4 = {14, 15, 16}                        # 복합B: ㅝㅞㅟ

# ============================================================
# ★★★ 그룹별 수치 테이블 (조정용) ★★★
#
# 각 그룹 × 받침유무별로 수치를 지정합니다.
#
# top_x_ratio : 상단 기호(caron/ya/ringup/tilde) X 위치 (글리프 너비 대비 비율, 0.0=왼쪽, 1.0=오른쪽)
# top_y_gap   : 상단 기호 Y (글리프 ymax 위로 몇 유닛 띄울지, 양수=위)
# bot_x_ratio : 하단 기호(ringdn/tildedn) X 위치 (글리프 너비 대비 비율)
# bot_y_gap   : 하단 기호 Y (글리프 ymin 아래로 몇 유닛, 양수=아래로)
# mac_x_ratio : macron X 위치 (글리프 너비 대비 비율)
# mac_y_gap   : macron Y (글리프 ymax 위로 몇 유닛)
# mac_sx      : macron 가로 스케일
# dp_x_gap    : double prime X (xmax 오른쪽으로 몇 유닛)
# dp_y_gap    : double prime Y (ymax 아래로 몇 유닛)
# comp_gap    : macron↔caron/ya 복합 간격 (유닛)
# comp_up     : 복합 그룹 전체 상향 (유닛)
# ring_r_out  : ring 외경
# ring_r_in   : ring 내경
# ============================================================

PARAMS = {
    # ──────────────────────────────────
    # G1a: 세로형 무받침 (ㅏㅐㅑㅒㅓㅔㅕㅖㅣ)
    # ──────────────────────────────────
    'G1a': {
        'top_x_ratio': 0.58,   'top_y_gap': 1,
        'bot_x_ratio': 0.53,   'bot_y_gap': 0,
        'mac_x_ratio': 0.58,   'mac_y_gap': 1,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 20,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
    # ──────────────────────────────────
    # G1b: 세로형 받침 (ㅏㅐㅑㅒㅓㅔㅕㅖㅣ + 종성)
    # ──────────────────────────────────
    'G1b': {
        'top_x_ratio': 0.58,   'top_y_gap': 1,
        'bot_x_ratio': 0.53,   'bot_y_gap': 0,
        'mac_x_ratio': 0.58,   'mac_y_gap': 1,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 15,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
    # ──────────────────────────────────
    # G2a: 가로형 무받침 (ㅗㅛㅜㅠㅡ)
    # ──────────────────────────────────
    'G2a': {
        'top_x_ratio': 0.50,   'top_y_gap': 8,
        'bot_x_ratio': 0.50,   'bot_y_gap': 8,
        'mac_x_ratio': 0.62,   'mac_y_gap': 8,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 20,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
    # ──────────────────────────────────
    # G2b: 가로형 받침 (ㅗㅛㅜㅠㅡ + 종성)
    #   받침 시 자음이 왼쪽 위로 압축됨 → x를 왼쪽으로 이동
    # ──────────────────────────────────
    'G2b': {
        'top_x_ratio': 0.35,   'top_y_gap': 5,
        'bot_x_ratio': 0.35,   'bot_y_gap': 8,
        'mac_x_ratio': 0.45,   'mac_y_gap': 5,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 15,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
    # ──────────────────────────────────
    # G3a: 복합A 무받침 (ㅘㅙㅚㅢ)
    # ──────────────────────────────────
    'G3a': {
        'top_x_ratio': 0.15,   'top_y_gap': 8,
        'bot_x_ratio': 0.18,   'bot_y_gap': 8,
        'mac_x_ratio': 0.38,   'mac_y_gap': 8,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 20,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
    # ──────────────────────────────────
    # G3b: 복합A 받침 (ㅘㅙㅚㅢ + 종성)
    # ──────────────────────────────────
    'G3b': {
        'top_x_ratio': 0.12,   'top_y_gap': 5,
        'bot_x_ratio': 0.15,   'bot_y_gap': 8,
        'mac_x_ratio': 0.35,   'mac_y_gap': 5,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 15,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
    # ──────────────────────────────────
    # G4a: 복합B 무받침 (ㅝㅞㅟ)
    # ──────────────────────────────────
    'G4a': {
        'top_x_ratio': 0.15,   'top_y_gap': 8,
        'bot_x_ratio': 0.18,   'bot_y_gap': 8,
        'mac_x_ratio': 0.35,   'mac_y_gap': 8,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 20,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
    # ──────────────────────────────────
    # G4b: 복합B 받침 (ㅝㅞㅟ + 종성)
    #   받침 시 자음이 왼쪽 위로 더 압축 → x 추가 왼쪽 이동
    # ──────────────────────────────────
    'G4b': {
        'top_x_ratio': 0.12,   'top_y_gap': 5,
        'bot_x_ratio': 0.15,   'bot_y_gap': 8,
        'mac_x_ratio': 0.30,   'mac_y_gap': 5,   'mac_sx': 1.5,
        'dp_x_gap': 40,        'dp_y_gap': 80,
        'comp_gap': 85,         'comp_up': 15,
        'ring_r_out': 90,       'ring_r_in': 60,
    },
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
    """자음 상단/하단 중앙에 거의 붙도록 배치. 겹침 금지."""
    xmin, ymin, xmax, ymax = bb
    w = xmax - xmin
    h = ymax - ymin
    L, V, T = decompose(base_cp)
    has_jong = T != 0
    grp = get_group(V)
    grp_key = grp + ('b' if has_jong else 'a')
    p = PARAMS[grp_key]

    # 상단 기호: 자음 상단 중앙 바로 위
    top_x = int(xmin + w * p['top_x_ratio'])
    top_y = int(ymax + p['top_y_gap'])

    # 하단 기호: 자음 하단 중앙 바로 아래
    bot_x = int(xmin + w * p['bot_x_ratio'])
    bot_y = int(ymin - p['bot_y_gap'])

    # macron
    mac_x = int(xmin + w * p['mac_x_ratio'])
    mac_y = int(ymax + p['mac_y_gap'])

    # double prime
    dp_x = int(xmax + p['dp_x_gap'])
    dp_y = int(ymax - p['dp_y_gap'])

    return top_x, top_y, bot_x, bot_y, mac_x, mac_y, dp_x, dp_y, grp_key, has_jong


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
    pen = None
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


# ======= Build all bases =======
# Pilot only: 가/다/따/감
BASES = [0xAC00, 0xB2E4, 0xB530, 0xAC10]

font = fontforge.open(SRC)
for lk in font.gsub_lookups:
    try: font.removeLookup(lk)
    except Exception: pass

lookup_name = 'rlig_pali_v279pilot'
font.addLookup(lookup_name, 'gsub_ligature', (), (("rlig", (("DFLT", ("dflt",)), ("hang", ("dflt",)))),))
NUM_SUBS = 12
SUBTABLES = [f'rlig_pali_v279pilot_sub{i}' for i in range(NUM_SUBS)]
for st in SUBTABLES:
    font.addLookupSubtable(lookup_name, st)

for cp in (COMMA, PERIOD):
    try: font[cp].transform(psMat.translate(0, -50))
    except Exception: pass

S0 = 0xE600
step = 0

for bi, bcp in enumerate(BASES):
    sub = SUBTABLES[bi % NUM_SUBS]
    base = font[bcp]
    bb = base.boundingBox()
    top_x, top_y, bot_x, bot_y, mac_x, mac_y, dp_x, dp_y, grp_key, has_jong = anchors(bcp, bb)
    p = PARAMS[grp_key]

    rout = p['ring_r_out']
    rin = p['ring_r_in']
    mac_sx = p['mac_sx']

    # Allocate PUA slots
    slots = []
    for i in range(14):
        cp = S0 + step; step += 1
        font.createChar(cp)
        slots.append(cp)
    cp_mac, cp_car, cp_dpr, cp_ya, cp_ru, cp_rd, cp_tu, cp_td = slots[:8]
    cp_mc, cp_my, cp_mr, cp_md, cp_rdpr, cp_rudpr = slots[8:]

    # === Single marks ===
    g = font[cp_mac]; g.clear(); add_mark_reference(g, font[MACRON], mac_x, mac_y, sx=mac_sx); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[MACRON].glyphname))
    g = font[cp_car]; g.clear(); add_mark_reference(g, font[CARON], top_x, top_y); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[CARON].glyphname))
    g = font[cp_dpr]; g.clear(); add_mark_reference(g, font[DOUBLE_PRIME], dp_x, dp_y); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[DOUBLE_PRIME].glyphname))
    g = font[cp_ya];  g.clear(); add_mark_reference(g, font[YA_MARK], top_x, top_y); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[YA_MARK].glyphname))
    g = font[cp_ru]; g.clear(); pen = g.glyphPen(); draw_ring(g, pen, top_x, top_y, rout, rin); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[RING_ABOVE].glyphname))
    g = font[cp_rd]; g.clear(); pen = g.glyphPen(); draw_ring(g, pen, bot_x, bot_y, rout, rin); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[RING_BELOW].glyphname))
    g = font[cp_tu]; g.clear(); add_mark_reference(g, font[TILDE_ABOVE], top_x, top_y, sy=1.15); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[TILDE_ABOVE].glyphname))
    g = font[cp_td]; g.clear(); add_mark_reference(g, font[TILDE_BELOW], bot_x, bot_y, sy=1.15); g.addReference(base.glyphname); g.width=base.width; g.addPosSub(sub,(base.glyphname,font[TILDE_BELOW].glyphname))

    # === Compound marks ===
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

font.fontname = 'PaliHangulV279pilot'
font.familyname = 'PaliHangul V279 Pilot'
font.fullname = 'PaliHangul V279 Pilot'
font.version = '2.79-pilot'
font.generate(OUT)
font.close()
print('Generated:', OUT)
print('GlyphCountStep:', step)
print('Size:', os.path.getsize(OUT))
