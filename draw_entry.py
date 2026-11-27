# draw_entry.py — draws entry.png for news-image-20261127 (Friday 27 November 2026).
# One-page newspaper: masthead, lead story with schematic Gulf map, two second
# stories, a markets strip, a 3x4 grid of the day's other stories, footer.
# Deterministic: no randomness, no network, no timestamps in the image.
# Run: python3 draw_entry.py  (writes entry.png next to this file)

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (26, 26, 26)           # near-black
RED = (178, 38, 30)          # masthead red
NAVY = (31, 58, 95)          # markets band
GREY = (90, 86, 78)          # secondary text
LINE = (26, 26, 26)
CARD = (255, 255, 255)
SEA = (196, 216, 228)
SAND = (232, 214, 178)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SERIF = F + "DejaVuSerif.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, max_lines, fill=INK, leading=None):
    """Draw wrapped text, at most max_lines; returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    lines = wrap(draw, text, fnt, max_w)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=LINE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24                      # side margin
CW = W - 2 * MX              # content width

# ---- top bar ---------------------------------------------------------------
d.rectangle([0, 0, W, 26], fill=INK)
f_top = font(SANS_B, 13)
d.text((MX, 5), "FRIDAY, 27 NOVEMBER 2026", font=f_top, fill=(247, 243, 234))
right = "ONE DAY  •  ONE PAGE  •  No. 27"
d.text((W - MX - d.textlength(right, font=f_top), 5), right,
       font=f_top, fill=(247, 243, 234))

# ---- masthead --------------------------------------------------------------
f_mast = font(SERIF_B, 66)
title = "THE WORLD TODAY"
d.text(((W - d.textlength(title, font=f_mast)) / 2, 32), title,
       font=f_mast, fill=INK)
f_sub = font(SERIF, 16)
sub = "The world's news of Friday, 27 November 2026 — summed up in one image"
d.text(((W - d.textlength(sub, font=f_sub)) / 2, 106), sub,
       font=f_sub, fill=INK)
rule(d, MX, 128, W - MX, 3)
rule(d, MX, 133, W - MX, 1)

# ---- lead story + schematic map -------------------------------------------
LY = 146
f_kick = font(SANS_B, 14)
f_lead = font(SERIF_B, 29)
f_body = font(SANS, 15)
lead_x, lead_w = MX, 596
d.text((lead_x, LY), "LEAD  —  THE GULF", font=f_kick, fill=RED)
y = para(d, lead_x, LY + 24,
         "Iranian drone strike in Kuwait kills two Italians; Tehran denies role",
         f_lead, lead_w, 3, leading=36)
y = para(d, lead_x, y + 8,
         "Kuwait says an Iranian drone killed two Italian workers at a site in "
         "the Gulf state. Iran denies responsibility, as the strike raises fears "
         "of a wider regional escalation.",
         f_body, lead_w, 4, leading=20, fill=(52, 52, 52))

# schematic map panel (right of the lead)
map_x, map_y, map_w, map_h = 648, LY, 352, 188
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA,
            outline=INK, width=2)
# sand landmass: Arabian peninsula, simplified
d.polygon([(map_x + 150, map_y + 10), (map_x + 340, map_y + 10),
           (map_x + 340, map_y + 178), (map_x + 250, map_y + 178),
           (map_x + 210, map_y + 120), (map_x + 150, map_y + 90)],
          fill=SAND, outline=INK)
d.polygon([(map_x + 10, map_y + 10), (map_x + 140, map_y + 10),
           (map_x + 140, map_y + 80), (map_x + 10, map_y + 60)],
          fill=SAND, outline=INK)
f_map = font(SANS_B, 12)
d.text((map_x + 18, map_y + 16), "IRAN", font=f_map, fill=INK)
d.text((map_x + 252, map_y + 140), "SAUDI ARABIA", font=font(SANS_B, 10),
       fill=INK)
d.text((map_x + 22, map_y + 128), "THE GULF", font=font(SANS, 11), fill=NAVY)
# dashed flight path from Iran toward Kuwait, with a blast star at Kuwait
x0, y0, x1, y1 = map_x + 120, map_y + 42, map_x + 205, map_y + 108
steps = 14
for i in range(steps):
    if i % 2 == 0:
        t0, t1 = i / steps, (i + 1) / steps
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
               fill=RED, width=3)
# blast star at Kuwait
kx, ky = map_x + 208, map_y + 112
for ang in range(0, 360, 45):
    import math
    r1, r2 = 4, 13
    a = math.radians(ang)
    d.line([(kx + r1 * math.cos(a), ky + r1 * math.sin(a)),
            (kx + r2 * math.cos(a), ky + r2 * math.sin(a))],
           fill=RED, width=3)
d.ellipse([kx - 4, ky - 4, kx + 4, ky + 4], fill=RED)
d.text((kx + 14, ky - 6), "KUWAIT", font=f_map, fill=RED)
d.text((map_x + 10, map_y + map_h - 18), "SCHEMATIC MAP — NOT TO SCALE",
       font=font(SANS, 9), fill=GREY)

# ---- second row: storm + Gaza ----------------------------------------------
SY = 352
BOX_H = 108
half_w = (CW - 12) // 2


def story_box(x, y, w, h, kicker, headline, body):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=1)
    d.text((x + 12, y + 8), kicker, font=font(SANS_B, 12), fill=RED)
    yy = para(d, x + 12, y + 28, headline, font(SANS_B, 18), w - 24, 2,
              leading=22)
    para(d, x + 12, yy + 4, body, font(SANS, 13), w - 24, 2, leading=17,
         fill=(52, 52, 52))


story_box(MX, SY, half_w, BOX_H, "UNITED STATES  —  THANKSGIVING STORM",
          "Storm leaves 800,000 in the dark; Macy's postpones its 100th parade",
          "More than 1,000 flights cancelled as a massive storm disrupts the "
          "Thanksgiving holiday across the US.")
story_box(MX + half_w + 12, SY, half_w, BOX_H, "MIDDLE EAST  —  GAZA",
          "Hamas weighs reply after Israel kills 10 in Gaza",
          "Mediators wait on Hamas as strikes kill ten and strain the ceasefire.")

# ---- markets strip ---------------------------------------------------------
MY = 472
d.rectangle([MX, MY, W - MX, MY + 52], fill=NAVY)
f_mkt = font(SANS_B, 15)
m1 = "MARKETS — Bitcoin $60,840, up 3.8% on Thanksgiving  •  US markets shut for the holiday, short session Friday"
d.text(((W - d.textlength(m1, font=f_mkt)) / 2, MY + 7), m1,
       font=f_mkt, fill=(247, 243, 234))
f_mkt2 = font(SANS, 13)
m2 = "Black Friday today: $12.9bn of US online sales forecast (Adobe)"
d.text(((W - d.textlength(m2, font=f_mkt2)) / 2, MY + 30), m2,
       font=f_mkt2, fill=(210, 220, 235))

# ---- grid of the day's other stories ---------------------------------------
GY = 540
COLS, ROWS = 3, 4
gap_x, gap_y = 11, 9
card_w = (CW - gap_x * (COLS - 1)) // COLS
card_h = 100
cards = [
    ("UKRAINE", "Trump tells Putin: pull back aggression in Europe",
     "The US president and NATO's chief urge Moscow not to widen the war."),
    ("TRADE", "US plans new tariffs on the EU and China",
     "Trump also seeks a probe into 'fake' GDP figures after growth was revised to 4.3%."),
    ("BRITAIN", "Net migration to the UK falls to lowest since 1997",
     "Excluding the pandemic years, the sharpest drop on record."),
    ("CHESS", "Gukesh, Sindarov draw marathon Game 3",
     "The world title match stays level after three games."),
    ("FRANCE", "Depardieu to stand trial over alleged 2018 rape",
     "A Paris court orders the trial of the 77-year-old actor."),
    ("SPAIN", "Tanker capsizes off Ibiza; one dead",
     "The vessel carried up to 7,000 tonnes of diesel."),
    ("TECH", "Musk: every US child to get two SpaceX shares",
     "The pledge, made on Thanksgiving, is short on detail."),
    ("HEALTH", "Ebola in DR Congo passes 12,000 cases",
     "Unrest forces responders to pull out of affected areas."),
    ("NEPAL", "Nepal declares 4,000 missing landslide victims dead",
     "The toll is formally recorded after the disaster."),
    ("THAILAND", "Blast at Bangkok oil refinery injures nine",
     "Three are in critical condition; an evacuation alert is issued."),
    ("LIBYA", "Zelensky: Ukraine hit a Russian warship in Libya",
     "Kyiv confirms a drone strike on the vessel at Benghazi."),
    ("WORLD", "UN: 47,000 women killed by relatives in 2025",
     "About five an hour, the United Nations reports."),
]
f_ck = font(SANS_B, 11)
f_ch = font(SANS_B, 15)
f_cb = font(SANS, 12)
for i, (kick, head, body) in enumerate(cards):
    r, c = divmod(i, COLS)
    x = MX + c * (card_w + gap_x)
    y = GY + r * (card_h + gap_y)
    d.rectangle([x, y, x + card_w, y + card_h], fill=CARD, outline=INK,
                width=1)
    d.text((x + 10, y + 7), kick, font=f_ck, fill=RED)
    yy = para(d, x + 10, y + 24, head, f_ch, card_w - 20, 2, leading=18)
    para(d, x + 10, yy + 3, body, f_cb, card_w - 20, 2, leading=15,
         fill=(52, 52, 52))

# ---- footer ----------------------------------------------------------------
FY = GY + ROWS * card_h + (ROWS - 1) * gap_y + 10
rule(d, MX, FY, W - MX, 1)
f_ft = font(SANS, 11)
foot = ("Sources: The New York Times  •  BBC  •  Reuters  •  KuCoin / CoinTelegraph  •  "
        "All events first reported on Friday 27 November 2026.")
d.text((MX, FY + 8), foot, font=f_ft, fill=GREY)
f_sign = font(SERIF_B, 12)
sign = "THE WORLD TODAY"
d.text((W - MX - d.textlength(sign, font=f_sign), FY + 8), sign,
       font=f_sign, fill=INK)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
