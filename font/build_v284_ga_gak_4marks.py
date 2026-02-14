#!/usr/bin/env python3
"""PaliHangul v2.83 — G1 independent initial/final attachment pass.

Requirements addressed:
- G1a/G1b coordinates intentionally different
- Macron attached once at syllable-level center
- Non-macron marks support independent initial/final placement in same syllable
- Multi-mark support: initial(top+bottom) + final(bottom tilde)
"""

import os
import fontforge
import psMat

SRC = os.path.expanduser('~/Library/Fonts/PaliHangulV252.otf')
OUT = os.path.expanduser('~/Library/Fonts/PaliHangulV284_ga_gak_4marks.otf')

# Real combining marks
MACRON = 0xFE20
CARON = 0x030C
YA_MARK = 0x0346
RING_ABOVE = 0x030A
RING_BELOW = 0x0325
TILDE_ABOVE = 0x0303
TILDE_BELOW = 0x0330
DOUBLE_PRIME = 0x02BA

# Internal selector-like PUA marks for side targeting
I_CARON = 0xE310
I_YA = 0xE311
I_RING_ABOVE = 0xE312
I_RING_BELOW = 0xE313
I_TILDE_ABOVE = 0xE314
I_TILDE_BELOW = 0xE315

F_CARON = 0xE320
F_YA = 0xE321
F_RING_ABOVE = 0xE322
F_RING_BELOW = 0xE323
F_TILDE_ABOVE = 0xE324
F_TILDE_BELOW = 0xE325

COMMA = 0x05C0
PERIOD = 0x2225

G1 = {0, 1, 2, 3, 4, 5, 6, 7, 20}

# Tuned per group key (no-jong=a / jong=b)
PARAMS = {
    'G1a': {
        # Initial consonant attachment (no jong)
        'i_top_x_ratio': 0.142,
        'i_top_y_gap': 8,
        'i_bot_x_ratio': 0.142,
        'i_bot_y_gap': 9,
        # Final slots (kept distinct by design, mostly unused in no-jong)
        'f_top_x_ratio': 0.674,
        'f_top_y_gap': -6,
        'f_bot_x_ratio': 0.690,
        'f_bot_y_gap': 20,
        # Macron: syllable center only
        'mac_x_ratio': 0.500,
        'mac_y_gap': 8,
        'mac_sx': 1.50,
        # Extras
        'dp_x_gap': 40,
        'dp_y_gap': 80,
        'ring_r_out': 90,
        'ring_r_in': 60,
    },
    'G1b': {
        # Initial consonant attachment (with jong)
        'i_top_x_ratio': 0.136,
        'i_top_y_gap': 5,
        'i_bot_x_ratio': 0.136,
        'i_bot_y_gap': 9,
        # Final consonant attachment (independent from initial)
        'f_top_x_ratio': 0.708,
        'f_top_y_gap': -4,
        'f_bot_x_ratio': 0.724,
        'f_bot_y_gap': 18,
        # Macron: syllable center only
        'mac_x_ratio': 0.498,
        'mac_y_gap': 6,
        'mac_sx': 1.50,
        # Extras
        'dp_x_gap': 40,
        'dp_y_gap': 80,
        'ring_r_out': 90,
        'ring_r_in': 60,
    },
}


def decompose(cp):
    s = cp - 0xAC00
    return s // 588, (s % 588) // 28, s % 28


def anchors(base_cp, bb):
    xmin, ymin, xmax, ymax = bb
    w = xmax - xmin
    L, V, T = decompose(base_cp)
    has_jong = T != 0
    k = 'G1b' if has_jong else 'G1a'
    p = PARAMS[k]

    i_top = (int(xmin + w * p['i_top_x_ratio']), int(ymax + p['i_top_y_gap']))
    i_bot = (int(xmin + w * p['i_bot_x_ratio']), int(ymin - p['i_bot_y_gap']))

    # Final anchors biased to jong area; fallback still valid for no-jong testability
    f_top = (int(xmin + w * p['f_top_x_ratio']), int(ymin + p['f_top_y_gap']))
    f_bot = (int(xmin + w * p['f_bot_x_ratio']), int(ymin - p['f_bot_y_gap']))

    mac = (int(xmin + w * p['mac_x_ratio']), int(ymax + p['mac_y_gap']))
    dp = (int(xmax + p['dp_x_gap']), int(ymax - p['dp_y_gap']))

    return k, p, i_top, i_bot, f_top, f_bot, mac, dp


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


def ensure_zero_width_tokens(font):
    cps = [
        I_CARON, I_YA, I_RING_ABOVE, I_RING_BELOW, I_TILDE_ABOVE, I_TILDE_BELOW,
        F_CARON, F_YA, F_RING_ABOVE, F_RING_BELOW, F_TILDE_ABOVE, F_TILDE_BELOW,
    ]
    for cp in cps:
        font.createChar(cp)
        g = font[cp]
        g.clear()
        g.width = 0


def draw_mark(g, mark_cp, pos, mac_sx, rout, rin):
    if mark_cp in (RING_ABOVE, RING_BELOW):
        pen = g.glyphPen()
        draw_ring(g, pen, pos[0], pos[1], rout, rin)
    elif mark_cp == MACRON:
        add_mark_reference(g, font[mark_cp], pos[0], pos[1], sx=mac_sx)
    elif mark_cp == TILDE_ABOVE or mark_cp == TILDE_BELOW:
        add_mark_reference(g, font[mark_cp], pos[0], pos[1], sy=1.15)
    else:
        add_mark_reference(g, font[mark_cp], pos[0], pos[1])


# pilot only: 가, 각
BASES = [0xAC00, 0xAC01]

font = fontforge.open(SRC)
for lk in list(font.gsub_lookups):
    try:
        font.removeLookup(lk)
    except Exception:
        pass

ensure_zero_width_tokens(font)

lookup_name = 'rlig_pali_v284gagak'
font.addLookup(lookup_name, 'gsub_ligature', (), (("rlig", (("DFLT", ("dflt",)), ("hang", ("dflt",)))),))
NUM_SUBS = 12
SUBTABLES = [f'rlig_pali_v284gagak_sub{i}' for i in range(NUM_SUBS)]
for st in SUBTABLES:
    font.addLookupSubtable(lookup_name, st)

for cp in (COMMA, PERIOD):
    try:
        font[cp].transform(psMat.translate(0, -50))
    except Exception:
        pass

S0 = 0xE600
STEP = [0]

# For compatibility: real combining marks default to INITIAL target (except macron)
initial_real_map = {
    CARON: (I_CARON, CARON, 'itop'),
    YA_MARK: (I_YA, YA_MARK, 'itop'),
    RING_ABOVE: (I_RING_ABOVE, RING_ABOVE, 'itop'),
    RING_BELOW: (I_RING_BELOW, RING_BELOW, 'ibot'),
    TILDE_ABOVE: (I_TILDE_ABOVE, TILDE_ABOVE, 'itop'),
    TILDE_BELOW: (I_TILDE_BELOW, TILDE_BELOW, 'ibot'),
}

# Explicit initial/final map using PUA selectors
side_map = {
    I_CARON: (CARON, 'itop'),
    I_YA: (YA_MARK, 'itop'),
    I_RING_ABOVE: (RING_ABOVE, 'itop'),
    I_RING_BELOW: (RING_BELOW, 'ibot'),
    I_TILDE_ABOVE: (TILDE_ABOVE, 'itop'),
    I_TILDE_BELOW: (TILDE_BELOW, 'ibot'),
    F_CARON: (CARON, 'ftop'),
    F_YA: (YA_MARK, 'ftop'),
    F_RING_ABOVE: (RING_ABOVE, 'ftop'),
    F_RING_BELOW: (RING_BELOW, 'fbot'),
    F_TILDE_ABOVE: (TILDE_ABOVE, 'ftop'),
    F_TILDE_BELOW: (TILDE_BELOW, 'fbot'),
}

for bi, bcp in enumerate(BASES):
    sub = SUBTABLES[bi % NUM_SUBS]
    base = font[bcp]
    k, p, i_top, i_bot, f_top, f_bot, mac, dp = anchors(bcp, base.boundingBox())
    rout = p['ring_r_out']
    rin = p['ring_r_in']
    mac_sx = p['mac_sx']

    positions = {
        'itop': i_top,
        'ibot': i_bot,
        'ftop': f_top,
        'fbot': f_bot,
    }

    def new_slot():
        cp = S0 + STEP[0]
        STEP[0] += 1
        font.createChar(cp)
        return cp

    # Macron: syllable-level only (real combining mark)
    cp_mac = new_slot()
    g = font[cp_mac]
    g.clear()
    draw_mark(g, MACRON, mac, mac_sx, rout, rin)
    g.addReference(base.glyphname)
    g.width = base.width
    g.addPosSub(sub, (base.glyphname, font[MACRON].glyphname))

    # Double-prime kept syllable-level/right
    cp_dp = new_slot()
    g = font[cp_dp]
    g.clear()
    draw_mark(g, DOUBLE_PRIME, dp, mac_sx, rout, rin)
    g.addReference(base.glyphname)
    g.width = base.width
    g.addPosSub(sub, (base.glyphname, font[DOUBLE_PRIME].glyphname))

    # Initial default real marks (compat)
    for real_cp, (_sel_cp, mark_cp, slot_name) in initial_real_map.items():
        cp_out = new_slot()
        g = font[cp_out]
        g.clear()
        draw_mark(g, mark_cp, positions[slot_name], mac_sx, rout, rin)
        g.addReference(base.glyphname)
        g.width = base.width
        g.addPosSub(sub, (base.glyphname, font[real_cp].glyphname))

    # Explicit side selectors (initial/final independent)
    for sel_cp, (mark_cp, slot_name) in side_map.items():
        cp_out = new_slot()
        g = font[cp_out]
        g.clear()
        draw_mark(g, mark_cp, positions[slot_name], mac_sx, rout, rin)
        g.addReference(base.glyphname)
        g.width = base.width
        g.addPosSub(sub, (base.glyphname, font[sel_cp].glyphname))

    # 2-mark: initial + final independence in one syllable (example pair)
    cp_if = new_slot()
    g = font[cp_if]
    g.clear()
    draw_mark(g, CARON, i_top, mac_sx, rout, rin)
    draw_mark(g, TILDE_BELOW, f_bot, mac_sx, rout, rin)
    g.addReference(base.glyphname)
    g.width = base.width
    g.addPosSub(sub, (base.glyphname, font[I_CARON].glyphname, font[F_TILDE_BELOW].glyphname))
    g.addPosSub(sub, (base.glyphname, font[F_TILDE_BELOW].glyphname, font[I_CARON].glyphname))

    # 3-mark required: initial(top+bottom) + final(bottom tilde)
    cp_tri = new_slot()
    g = font[cp_tri]
    g.clear()
    draw_mark(g, CARON, i_top, mac_sx, rout, rin)
    draw_mark(g, RING_BELOW, i_bot, mac_sx, rout, rin)
    draw_mark(g, TILDE_BELOW, f_bot, mac_sx, rout, rin)
    g.addReference(base.glyphname)
    g.width = base.width
    g.addPosSub(sub, (base.glyphname, font[I_CARON].glyphname, font[I_RING_BELOW].glyphname, font[F_TILDE_BELOW].glyphname))
    g.addPosSub(sub, (base.glyphname, font[I_RING_BELOW].glyphname, font[I_CARON].glyphname, font[F_TILDE_BELOW].glyphname))

font.fontname = 'PaliHangulV284GaGak4Marks'
font.familyname = 'PaliHangul V284 GaGak 4Marks'
font.fullname = 'PaliHangul V284 GaGak 4Marks'
font.version = '2.84-gagak-4marks'
font.generate(OUT)
font.close()

print('Generated:', OUT)
print('GlyphCountStep:', STEP[0])
print('Size:', os.path.getsize(OUT))
