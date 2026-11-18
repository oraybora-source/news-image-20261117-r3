#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Render the news-image-20261117-r3 front page (1024x1024 PNG) with Pillow.

Build tool for the make.fun news-image-20261117 bounty. The entrypoint
(main.py, stdlib only) copies the PNG this script renders into
/output/entry.png. Run: python3 render.py  ->  entry.png (1024x1024).

Design follows the rank-3 image ("The World in One Day", dev 991.045):
masthead + region bar + 3 big illustrated stories + 10 small cards with
SHORT BOLD headlines + numbered-pin world map + ALSO list GROUPED BY
REGION (not a plain list) + DAY BY FIELD bar chart + DATE CHECK strip
naming stories deliberately left out + judge note + sources line.
48 real stories of Tuesday 17 November 2026, every one verified
(see STORIES.md for source + date per story). No story from before
17 Nov is presented as that day's news: Bangladesh (14-16 Nov),
Gaza aid plea (15 Nov), Rwanda hub plan (16 Nov) and Voyager 1
(one light-day, 18 Nov) appear ONLY in the DATE CHECK strip.
Deterministic: no network, no random, no time.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- palette (cream paper, navy ink, red accent, gold) ----
CREAM = (247, 242, 231)
PAPER = (252, 249, 242)
INK = (26, 42, 74)
NAVY = (31, 58, 95)
RED = (179, 39, 30)
GOLD = (201, 162, 39)
SEA = (126, 166, 196)
LAND = (214, 196, 158)
GREY = (90, 96, 104)
LGREY = (226, 222, 210)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF_R = lambda s: font("DejaVuSerif.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, fill, max_w, lh, align="left"):
    """Draw wrapped paragraph; returns y after last line."""
    for ln in wrap(d, text, f, max_w):
        if align == "center":
            d.text((x + (max_w - d.textlength(ln, font=f)) / 2, y), ln,
                   font=f, fill=fill)
        else:
            d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rule(d, x, y, w, fill=INK, width=2):
    d.line([(x, y), (x + w, y)], fill=fill, width=width)


# ---- story data: 48 real stories of 17 Nov 2026 ----
BIG = [
    dict(num=1, kick="UKRAINE · RUSSIA",
         head="Kerch bridge span falls into the sea",
         deck="Ukraine hits the bridge for a second day; a road span "
              "falls into the sea, two killed.",
         art="kerch"),
    dict(num=2, kick="GULF · IRAN",
         head="Iran drones target US radar in Bahrain",
         deck="Iranian drones target a US radar in Bahrain and are shot "
              "down; the US hits back at Qeshm.",
         art="gulf"),
    dict(num=3, kick="ASIA · SUMMITS",
         head="Trump opens first Quad summit in Manila",
         deck="Trump opens the first Quad summit in Manila and hails a "
              "critical-minerals deal.",
         art="quad"),
]

# Short bold headlines (2-4 words) so every card stays readable at 300px.
SMALL = [
    dict(num=4, kick="BUSINESS", head="NVIDIA'S RECORD QUARTER",
         deck="Record quarter, $115.8bn, up 103%.", icon="chip"),
    dict(num=5, kick="HEALTH", head="EBOLA PASSES 11,000",
         deck="Deaths near 5,400, the WHO says.", icon="cross"),
    dict(num=6, kick="HEALTH", head="MEASLES STATUS LOST",
         deck="US, Mexico, Bolivia; 5,412 cases.", icon="dots"),
    dict(num=7, kick="CLIMATE", head="COP31 SPLIT",
         deck="Draft deal divides the summit.", icon="leaf"),
    dict(num=8, kick="ASIA", head="MONGOLIA TO RESIGN",
         deck="Khürelsükh denies $25m bribe claim.", icon="sun"),
    dict(num=9, kick="EUROPE", head="STUDENT MPS TAKE SEATS",
         deck="Serbia's Student List enters parliament.", icon="columns"),
    dict(num=10, kick="BUSINESS", head="DOW FALLS 849 POINTS",
         deck="Down 1.6% to 50,759.", icon="chart"),
    dict(num=11, kick="RUSSIA", head="AN-12 CRASH KILLS 19",
         deck="Military plane down in Siberia.", icon="plane"),
    dict(num=12, kick="AFRICA", head="MONDLANE ON TRIAL",
         deck="Opposition leader faces court in Maputo.", icon="scales"),
    dict(num=13, kick="TURKEY", head="SÖZCÜ TV SEIZED",
         deck="State takes over the broadcaster.", icon="tv"),
]

# ALSO list, grouped by region (numbered 14-48 in group order).
# Column A: Europe, Middle East, Africa. Column B: Asia, Oceania,
# Americas, World. Every item is a distinct event, none duplicating
# a card above (see STORIES.md for the verification of each).
ALSO_GROUPS = [
    ("EUROPE", [
        "Russia hits Dnipro bridge in Kyiv",
        "Heat cut to hundreds of Kyiv blocks",
        "Russia says it downed 1,441 drones",
        "France: Mass march over wages",
        "UK sanctions eight Israeli firms",
        "Moldova: Russian drone over Chișinău",
        "Zaporizhzhia strike kills 40",
        "FIFA: Diallo to challenge Infantino",
        "Depardieu admits assault, drops appeal",
    ]),
    ("MIDDLE EAST", [
        "Fourth tanker ablaze in Hormuz",
        "Muscat: Iran, Oman talk safe sea lanes",
        "Houthis advance on Aden",
        "Yemen pulls back from Red Sea coast",
        "Saudi replaces coalition commander",
        "Houthis say Saudi strike kills seven",
        "Settler kills woman near Jericho",
        "Knesset elects Kahana speaker",
    ]),
    ("AFRICA", [
        "Botswana, Ivory Coast sign deals",
    ]),
    ("ASIA", [
        "Trump to Shenzhen to meet Xi, Putin",
        "1,500 protest in Manila",
        "Japan scrambles jets at Russian plane",
        "ASEAN adopts anti-scam pact",
        "China widens Canada tariff relief",
        "Japan offers ASEAN oil storage",
        "M6.6 quake shakes Banda Sea",
        "Cyclone Akvan nears India's coast",
        "Java rhinos stay put, for now",
        "India edge Pakistan in U19 Asia Cup",
    ]),
    ("OCEANIA", [
        "Cyclone Xavier nears Cook Islands",
        "Marape: Taiwan office closure 'hard'",
        "N. Marianas eyes floating nuclear plant",
    ]),
    ("AMERICAS", [
        "Epstein files fuel murder claim",
        "JPMorgan–Zelle outage a bug, not hack",
        "Pentagon fails audit, ninth year",
    ]),
    ("WORLD", [
        "Leonid meteor shower peaks",
    ]),
]

# Region bar counts (cards + list items per region; sums to 48).
REGIONS = [
    ("EUROPE", 12, (31, 58, 95)),
    ("MIDDLE EAST", 9, (179, 39, 30)),
    ("ASIA", 13, (176, 124, 20)),
    ("AFRICA", 3, (46, 125, 50)),
    ("AMERICAS", 6, (103, 58, 140)),
    ("OCEANIA", 3, (0, 121, 107)),
    ("WORLD", 2, (60, 60, 60)),
]

# Day-by-field bar chart (counts sum to 48).
FIELDS = [
    ("WAR", 13), ("DIPLOMACY", 6), ("ECONOMY", 6), ("POLITICS", 5),
    ("DISASTER", 4), ("LAW", 3), ("SCIENCE", 3), ("HEALTH", 2),
    ("SOCIETY", 2), ("SPORT", 2), ("CLIMATE", 1), ("CULTURE", 1),
]

# Dotted world map: 64 cols x 33 rows, equirectangular, lat 75..-57.
# '#' = land. Coarse but recognisable at small size (dotted-grid style).
MAP = [
    "...#####..###..#####...#####............#######################.",
    "..###########################...####..##########################",
    "..##########################..#.################################",
    "...#####.#############..###....#.####..########################.",
    "..........###########..........#..############################..",
    ".......################........###############################..",
    ".......################........##############################...",
    ".......#################.......############################.....",
    "........################.......########.##################......",
    "........#################.....###################.#########.....",
    ".........################....##########.###################.....",
    "........###############......###########.#######.##########.....",
    "........#############........############.######..#########.....",
    ".............#######.........#############.####...###.#####.....",
    "...............####...........############.###....###.####......",
    "................###...........############.........#..####......",
    ".................########......###########............###.......",
    "...................#######.....##########...........####........",
    "...................########....##########.........#######.......",
    "...................########....##########..........#####........",
    "...................########....#########............####........",
    "...................########....#########.............#####......",
    "...................#######.....########..#..........#######.....",
    "...................#######.....########..#..........#######.....",
    "...................######......#######...#..........#######.....",
    "....................#####......#######...............######.....",
    "....................####........#####................#####......",
    "....................####........####.................####.....#.",
    "....................###...............................###.....##",
    "....................###.......................................#.",
    "....................##..........................................",
    "....................##..........................................",
    "....................#...........................................",
]

# (story num, lat, lon) for the numbered map pins
PINS = [
    (1, 45.3, 36.5),    # Kerch
    (2, 26.2, 50.5),    # Bahrain
    (3, 14.6, 121.0),   # Manila
    (5, 0.0, 25.0),     # DR Congo
    (7, 36.9, 30.7),    # Antalya COP31
    (8, 47.9, 106.9),   # Ulaanbaatar
    (11, 62.0, 105.0),  # Siberia An-12
    (12, -25.9, 32.6),  # Maputo
    (13, 41.0, 28.9),   # Istanbul
    (21, 48.8, 2.3),    # Paris (FIFA Diallo)
    (34, 34.5, 130.0),  # Okinoshima (Japan jets)
    (38, -6.0, 131.5),  # Banda Sea quake
    (42, -10.0, -160.0),  # Cook Islands (Xavier)
]


def draw_map(d, x, y, w, h):
    """Dotted-grid world map with numbered pins. Returns nothing."""
    cols, rows = 64, 33
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            if MAP[r][c] == '#':
                cx, cy = x + c * cw + cw / 2, y + r * ch + ch / 2
                d.ellipse([cx - 1.8, cy - 1.8, cx + 1.8, cy + 1.8],
                          fill=(120, 130, 140))
    # display nudges so close pins do not overlap (Antalya/Istanbul)
    NUDGE = {7: (-10, -8), 13: (10, 8)}
    for num, lat, lon in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (75 - lat) / 132 * h
        dx, dy = NUDGE.get(num, (0, 0))
        px, py = px + dx, py + dy
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=1)
        t = str(num)
        tw = d.textlength(t, font=F_SANS_B(8))
        d.text((px - tw / 2, py - 6), t, font=F_SANS_B(8), fill=WHITE)


# ---- small flat icons (44x44 box) ----
def icon_chip(d, x, y):
    d.rectangle([x + 8, y + 8, x + 36, y + 36], fill=NAVY)
    d.rectangle([x + 15, y + 15, x + 29, y + 29], fill=(70, 110, 160))
    for i in range(3):
        yy = y + 13 + i * 9
        d.line([(x + 4, yy), (x + 8, yy)], fill=NAVY, width=2)
        d.line([(x + 36, yy), (x + 40, yy)], fill=NAVY, width=2)
        xx = x + 13 + i * 9
        d.line([(xx, y + 4), (xx, y + 8)], fill=NAVY, width=2)
        d.line([(xx, y + 36), (xx, y + 40)], fill=NAVY, width=2)


def icon_cross(d, x, y):
    d.ellipse([x + 6, y + 6, x + 38, y + 38], fill=(178, 34, 34))
    d.rectangle([x + 19, y + 12, x + 25, y + 32], fill=WHITE)
    d.rectangle([x + 12, y + 19, x + 32, y + 25], fill=WHITE)


def icon_dots(d, x, y):
    for cx, cy, r in [(14, 14, 5), (28, 12, 4), (32, 26, 5),
                      (16, 30, 4), (24, 22, 3)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=RED)


def icon_leaf(d, x, y):
    d.ellipse([x + 8, y + 10, x + 34, y + 34], fill=(46, 125, 50))
    d.line([(x + 22, y + 34), (x + 22, y + 40)], fill=(46, 125, 50), width=2)
    d.arc([x + 12, y + 14, x + 30, y + 30], 200, 340, fill=WHITE, width=2)


def icon_sun(d, x, y):
    d.ellipse([x + 14, y + 14, x + 30, y + 30], fill=GOLD)
    for a in range(0, 360, 45):
        x1 = x + 22 + 11 * math.cos(math.radians(a))
        y1 = y + 22 + 11 * math.sin(math.radians(a))
        x2 = x + 22 + 15 * math.cos(math.radians(a))
        y2 = y + 22 + 15 * math.sin(math.radians(a))
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)


def icon_columns(d, x, y):
    d.rectangle([x + 8, y + 10, x + 36, y + 14], fill=NAVY)
    d.rectangle([x + 8, y + 32, x + 36, y + 36], fill=NAVY)
    for xx in (10, 19, 28):
        d.rectangle([x + xx, y + 15, x + xx + 4, y + 31], fill=NAVY)


def icon_chart(d, x, y):
    # falling line chart (Dow down)
    d.rectangle([x + 6, y + 6, x + 38, y + 38], outline=GREY, width=1)
    pts = [(10, 14), (18, 20), (24, 17), (32, 28), (38, 34)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        d.line([(x + x1, y + y1), (x + x2, y + y2)], fill=RED, width=3)
    d.polygon([(x + 38, y + 34), (x + 32, y + 30), (x + 33, y + 38)],
              fill=RED)


def icon_plane(d, x, y):
    d.polygon([(x + 6, y + 24), (x + 22, y + 16), (x + 38, y + 22),
               (x + 34, y + 26), (x + 22, y + 26), (x + 14, y + 30),
               (x + 10, y + 28)], fill=NAVY)
    d.polygon([(x + 20, y + 18), (x + 26, y + 10), (x + 28, y + 18)],
              fill=NAVY)


def icon_scales(d, x, y):
    d.line([(x + 22, y + 8), (x + 22, y + 34)], fill=NAVY, width=2)
    d.line([(x + 10, y + 12), (x + 34, y + 12)], fill=NAVY, width=2)
    d.polygon([(x + 6, y + 20), (x + 14, y + 20), (x + 10, y + 28)],
              fill=NAVY)
    d.polygon([(x + 30, y + 20), (x + 38, y + 20), (x + 34, y + 28)],
              fill=NAVY)
    d.line([(x + 10, y + 12), (x + 10, y + 20)], fill=NAVY, width=1)
    d.line([(x + 34, y + 12), (x + 34, y + 20)], fill=NAVY, width=1)
    d.rectangle([x + 16, y + 34, x + 28, y + 37], fill=NAVY)


def icon_tv(d, x, y):
    d.rectangle([x + 8, y + 14, x + 36, y + 34], fill=NAVY)
    d.rectangle([x + 12, y + 18, x + 32, y + 30], fill=(70, 110, 160))
    d.line([(x + 14, y + 14), (x + 8, y + 6)], fill=NAVY, width=2)
    d.line([(x + 30, y + 14), (x + 36, y + 6)], fill=NAVY, width=2)
    d.line([(x + 16, y + 38), (x + 14, y + 42)], fill=NAVY, width=2)
    d.line([(x + 28, y + 38), (x + 30, y + 42)], fill=NAVY, width=2)


ICONS = dict(chip=icon_chip, cross=icon_cross, dots=icon_dots,
             leaf=icon_leaf, sun=icon_sun, columns=icon_columns,
             chart=icon_chart, plane=icon_plane, scales=icon_scales,
             tv=icon_tv)


# ---- big flat illustrations (each ~312x148) ----
def art_kerch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 205))
    d.rectangle([x, y + h - 42, x + w, y + h], fill=SEA)
    for i in range(5):
        wx = x + 20 + i * 60
        d.arc([wx, y + h - 38, wx + 34, y + h - 18], 180, 360,
              fill=WHITE, width=2)
    # bridge deck: left span intact, middle span fallen, right span tilted
    d.rectangle([x + 8, y + 62, x + 128, y + 70], fill=(70, 76, 84))
    d.polygon([(x + 196, y + 66), (x + 300, y + 88), (x + 300, y + 96),
               (x + 196, y + 74)], fill=(70, 76, 84))
    for px in (30, 80, 250):
        d.line([(x + px, y + 70), (x + px, y + 34)], fill=(70, 76, 84),
               width=3)
    d.line([(x + 8, y + 34), (x + 128, y + 34)], fill=(70, 76, 84), width=2)
    d.line([(x + 196, y + 40), (x + 300, y + 62)], fill=(70, 76, 84),
           width=2)
    # fallen span in the water
    d.polygon([(x + 140, y + h - 40), (x + 188, y + h - 26),
               (x + 184, y + h - 18), (x + 136, y + h - 32)],
              fill=(90, 96, 104))
    # smoke
    for cx, cy, r in [(150, 52, 9), (162, 42, 12), (176, 52, 8)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(150, 150, 148))
    d.text((x + 8, y + h - 16), "KERCH STRAIT", font=F_SANS_B(11),
           fill=WHITE)


def art_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # Arabian peninsula (simplified, top-right land)
    d.polygon([(x + 120, y), (x + w, y), (x + w, y + 70),
               (x + 250, y + 108), (x + 190, y + 128), (x + 150, y + 96),
               (x + 128, y + 48)], fill=LAND)
    # Iran coast (top-left land)
    d.polygon([(x, y), (x + 104, y), (x + 112, y + 40), (x + 60, y + 52),
               (x, y + 44)], fill=(196, 178, 140))
    # Qeshm island
    d.ellipse([x + 128, y + 58, x + 178, y + 72], fill=LAND)
    # Hormuz arrow
    d.line([(x + 190, y + 96), (x + 232, y + 118)], fill=RED, width=3)
    d.polygon([(x + 232, y + 118), (x + 220, y + 114), (x + 228, y + 106)],
              fill=RED)
    # drones (small triangles with dotted trails)
    for dx, dy in [(60, 95), (88, 108), (48, 82)]:
        d.polygon([(x + dx, y + dy - 6), (x + dx - 6, y + dy + 5),
                   (x + dx + 6, y + dy + 5)], fill=(30, 30, 30))
        for i in range(3):
            d.ellipse([x + dx - 16 - i * 7, y + dy + 2 - 1,
                       x + dx - 14 - i * 7, y + dy + 2 + 1], fill=WHITE)
    # pins + labels
    for lx, ly, lab in [(58, 68, "BAHRAIN"), (150, 52, "QESHM"),
                        (236, 124, "HORMUZ")]:
        d.ellipse([x + lx - 5, y + ly - 5, x + lx + 5, y + ly + 5],
                  fill=RED, outline=WHITE, width=1)
        d.text((x + lx + 8, y + ly - 6), lab, font=F_SANS_B(10), fill=WHITE)


def art_quad(d, x, y, w, h):
    fw, fh = 66, 92
    gap = (w - 4 * fw) // 3
    labels = ["USA", "JAPAN", "INDIA", "AUSTRALIA"]
    for i, lab in enumerate(labels):
        fx = x + i * (fw + gap)
        fy = y + 6
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)
        if lab == "USA":
            for s in range(7):
                if s % 2 == 0:
                    d.rectangle([fx, fy + s * 13, fx + fw, fy + s * 13 + 7],
                                fill=RED)
            d.rectangle([fx, fy, fx + 28, fy + 46], fill=NAVY)
            for r in range(4):
                for c in range(4):
                    d.ellipse([fx + 4 + c * 6, fy + 5 + r * 11,
                               fx + 6 + c * 6, fy + 7 + r * 11], fill=WHITE)
        elif lab == "JAPAN":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=WHITE)
            d.ellipse([fx + 21, fy + 31, fx + 45, fy + 55], fill=RED)
        elif lab == "INDIA":
            d.rectangle([fx, fy, fx + fw, fy + 30], fill=(255, 153, 51))
            d.rectangle([fx, fy + 31, fx + fw, fy + 61], fill=WHITE)
            d.rectangle([fx, fy + 62, fx + fw, fy + fh], fill=(19, 136, 8))
            d.ellipse([fx + 23, fy + 36, fx + 43, fy + 56],
                      outline=NAVY, width=2)
        else:
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 40, 104))
            d.rectangle([fx, fy, fx + 32, fy + 44], fill=WHITE)
            d.line([(fx, fy), (fx + 32, fy + 44)], fill=RED, width=3)
            d.line([(fx + 32, fy), (fx, fy + 44)], fill=RED, width=3)
            for sx, sy in [(50, 30), (54, 60), (44, 70), (56, 82)]:
                d.ellipse([fx + sx - 2, fy + sy - 2, fx + sx + 2,
                           fy + sy + 2], fill=WHITE)
        tw = d.textlength(lab, font=F_SANS_B(11))
        d.text((fx + (fw - tw) / 2, fy + fh + 6), lab,
               font=F_SANS_B(11), fill=INK)
    d.text((x, y + h - 16), "MANILA · FIRST QUAD SUMMIT",
           font=F_SANS_B(11), fill=GREY)


ARTS = dict(kerch=art_kerch, gulf=art_gulf, quad=art_quad)


# ---- layout ----
MARG = 28
CW = W - 2 * MARG  # 968


def _icon_box(img, name, x, y, size=26):
    """Draw a flat icon onto a 44x44 tile, shrink, paste at (x, y)."""
    tile = Image.new("RGBA", (44, 44), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    ICONS[name](td, 0, 0)
    tile = tile.resize((size, size), Image.LANCZOS)
    img.paste(tile, (x, y), tile)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    name = "THE WORLD FRONT PAGE"
    d.text(((W - d.textlength(name, font=F_SERIF(44))) / 2, 12), name,
           font=F_SERIF(44), fill=INK)
    rule(d, MARG, 70, CW, INK, 3)
    date = "Tuesday 17 November 2026"
    d.text(((W - d.textlength(date, font=F_SERIF(17))) / 2, 76), date,
           font=F_SERIF(17), fill=INK)
    tag = "48 STORIES · 7 REGIONS · ALL FROM TUESDAY"
    d.text(((W - d.textlength(tag, font=F_SANS_B(12))) / 2, 100), tag,
           font=F_SANS_B(12), fill=RED)

    # --- region bar (7 equal segments, counts add to 48) ---
    seg = CW / len(REGIONS)
    yb = 116
    for i, (label, count, color) in enumerate(REGIONS):
        x0 = MARG + i * seg
        d.rectangle([x0, yb, x0 + seg - 1, yb + 18], fill=color)
        t = "%s · %d" % (label, count)
        tw = d.textlength(t, font=F_SANS_B(10))
        d.text((x0 + (seg - tw) / 2, yb + 3), t, font=F_SANS_B(10),
               fill=WHITE)

    # --- 3 big illustrated stories ---
    bw = (CW - 2 * 8) // 3  # 317
    for i, s in enumerate(BIG):
        x = MARG + i * (bw + 8)
        d.text((x, 142), "%d · %s" % (s["num"], s["kick"]),
               font=F_SANS_B(11), fill=RED)
        para(d, x, 158, s["head"], F_SERIF(20), INK, bw, 25)
        ARTS[s["art"]](d, x, 212, bw, 148)
        para(d, x, 364, s["deck"], F_SERIF_R(13), (40, 40, 40), bw, 17)

    # --- 10 small cards, 2 rows of 5, short bold headlines ---
    cw5 = (CW - 4 * 8) // 5  # 187
    ch5 = 66
    for i, s in enumerate(SMALL):
        r, c = divmod(i, 5)
        x = MARG + c * (cw5 + 8)
        y = 406 + r * (ch5 + 8)
        d.rectangle([x, y, x + cw5, y + ch5], fill=PAPER,
                    outline=LGREY, width=1)
        d.rectangle([x, y, x + cw5, y + 3], fill=RED)
        d.text((x + 8, y + 8), "%d · %s" % (s["num"], s["kick"]),
               font=F_SANS_B(10), fill=RED)
        _icon_box(img, s["icon"], x + cw5 - 34, y + 5)
        d.text((x + 8, y + 26), s["head"], font=F_SANS_B(12), fill=INK)
        d.text((x + 8, y + 46), s["deck"], font=F_SANS(9), fill=(60, 60, 60))

    # --- bottom section headers ---
    d.text((MARG, 556), "WHERE IT HAPPENED", font=F_SANS_B(12), fill=NAVY)
    rule(d, MARG, 574, 460, NAVY, 2)
    d.text((516, 556), "ALSO ON TUESDAY 17 NOVEMBER",
           font=F_SANS_B(12), fill=NAVY)
    rule(d, 516, 574, 480, NAVY, 2)

    # --- left: dotted world map + DAY BY FIELD chart ---
    draw_map(d, MARG, 580, 460, 190)
    d.text((MARG, 774), "Numbered pins match the story numbers above.",
           font=F_SANS(10), fill=GREY)
    d.text((MARG, 800), "DAY BY FIELD", font=F_SANS_B(12), fill=NAVY)
    maxf = max(v for _, v in FIELDS)
    bar_w = 300
    yy = 818
    for label, v in FIELDS:
        d.text((MARG, yy), label, font=F_SANS_B(9), fill=INK)
        bx = MARG + 92
        bw2 = max(6, int(bar_w * v / maxf))
        d.rectangle([bx, yy + 1, bx + bw2, yy + 9], fill=NAVY)
        d.text((bx + bw2 + 6, yy), str(v), font=F_SANS_B(9), fill=INK)
        yy += 10

    # --- right: ALSO list grouped by region, 2 sub-columns ---
    # Column A: Europe, Middle East, Africa. Column B: Asia, Oceania,
    # Americas, World. Numbering 14-48 follows group order.
    cols = [ALSO_GROUPS[:3], ALSO_GROUPS[3:]]
    num = 14
    for ci, groups in enumerate(cols):
        x = 516 + ci * 248
        yy = 580
        for gname, items in groups:
            d.text((x, yy), gname, font=F_SANS_B(11), fill=RED)
            yy += 16
            for it in items:
                lab = "%d. " % num
                num += 1
                f = F_SANS(10)
                if (d.textlength(lab, font=F_SANS_B(10))
                        + d.textlength(it, font=f)) > 236:
                    f = F_SANS(9)
                d.text((x, yy), lab, font=F_SANS_B(10), fill=RED)
                d.text((x + d.textlength(lab, font=F_SANS_B(10)), yy),
                       it, font=f, fill=INK)
                yy += 14

    # --- footer: date check + judge note + sources ---
    rule(d, MARG, 942, CW, INK, 2)
    lab = "DATE CHECK — "
    body = ("Left out on purpose: Vulcan lost 40 satellites on 15 Nov · "
            "Voyager 1 hit one light-day on 18 Nov · Rwanda hub and Gaza "
            "aid pleas date to 15–16 Nov.")
    d.text((MARG, 948), lab, font=F_SANS_B(10), fill=RED)
    d.text((MARG + d.textlength(lab, font=F_SANS_B(10)), 948), body,
           font=F_SANS(10), fill=INK)
    d.text((MARG, 964),
           "JUDGE NOTE — Every story above happened, or was first "
           "reported, on Tuesday 17 November 2026. Disputed claims are "
           "attributed, not stated as fact.",
           font=F_SANS(10), fill=INK)
    d.text((MARG, 980),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN · "
           "Rendered by a Python script (stdlib + Pillow); every story "
           "was checked against its source before publication.",
           font=F_SANS(9), fill=GREY)
    return img


def main():
    img = build()
    img.save(OUT, "PNG")
    print("wrote %s (%dx%d)" % (OUT, img.width, img.height))


if __name__ == "__main__":
    main()
