"""Builds the GitHub profile SVGs (text outlined, since GitHub <img> SVGs can't load fonts)."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = os.path.join(os.path.dirname(__file__), "SchibstedGrotesk.ttf")  # OFL, from google/fonts
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "assets")
_cache = {}

def font(w):
    if w not in _cache:
        _cache[w] = instantiateVariableFont(TTFont(FONT), {"wght": w})
    return _cache[w]

def text_path(s, x, y, size, w=400, track=0.0):
    """Return (path d, advance width) for s with baseline at (x, y)."""
    f = font(w); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    sc = size / upm; pen = SVGPathPen(gs); cx = 0
    for ch in s:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x + cx, y)))
        cx += gs[g].width * sc + track * size
    return pen.getCommands(), cx - track * size

THEMES = {
    "light": dict(bg="#F3F5F7", ink="#1B2230", body="#3A4250", muted="#5B6372", accent="#0E6470", rule="#D6DAE0", bar="#0E6470"),
    "dark":  dict(bg="#161B22", ink="#E6EDF3", body="#C9D1D9", muted="#8B949E", accent="#4FC3CF", rule="#30363D", bar="#4FC3CF"),
}

def banner(t):
    W, H = 1200, 300
    name, nw = text_path("Justin Masiga", 64, 156, 96, 700, -0.02)
    role, _ = text_path("Full Stack Developer and AI Operations Engineer", 66, 216, 34, 500)
    # QuickSight-ish bar motif on the right, nod to the BI years
    heights = [70, 110, 90, 150, 125, 185, 160, 205]
    bars = "".join(
        f'<rect x="{900 + i * 32}" y="{246 - h}" width="20" height="{h}" rx="3" fill="{t["bar"]}" opacity="{0.25 + i * 0.09:.2f}"/>'
        for i, h in enumerate(heights))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Justin Masiga, Full Stack Developer and AI Operations Engineer">
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
<path d="{name}" fill="{t["ink"]}"/>
<path d="{role}" fill="{t["accent"]}"/>
{bars}
<rect x="64" y="246" width="{W - 128}" height="3" fill="{t["ink"]}"/>
</svg>'''

def card(t, title, domain, tag):
    W, H = 1200, 180
    tp, _ = text_path(title, 56, 100, 64, 700, -0.015)
    dp, _ = text_path(domain, 58, 146, 30, 500)
    tg, tw = text_path(tag, 0, 0, 26, 600, 0.04)
    pw = tw + 64; px = W - 56 - pw
    tg, _ = text_path(tag, px + 44, 99, 26, 600, 0.04)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}, {domain}">
<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{t["bg"]}"/>
<rect x="0" y="0" width="12" height="{H}" fill="{t["accent"]}" clip-path="url(#c)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{t["rule"]}" stroke-width="2"/>
<path d="{tp}" fill="{t["ink"]}"/>
<path d="{dp}" fill="{t["muted"]}"/>
<rect x="{px:.1f}" y="66" width="{pw:.1f}" height="46" rx="23" fill="none" stroke="{t["accent"]}" stroke-width="2"/>
<circle cx="{px + 25:.1f}" cy="89" r="7" fill="{t["accent"]}"/>
<path d="{tg}" fill="{t["accent"]}"/>
</svg>'''

CARDS = {
    "thejobstash": ("TheJobStash", "thejobstash.com", "LIVE"),
    "tapndine": ("tapndine", "tapndine.online", "LIVE"),
    "agent-office": ("Agent Office", "github.com/tsujintsujin/agent-office", "OPEN SOURCE"),
}

for mode, t in THEMES.items():
    open(os.path.join(OUT, f"banner-{mode}.svg"), "w").write(banner(t))
    for slug, args in CARDS.items():
        open(os.path.join(OUT, f"{slug}-{mode}.svg"), "w").write(card(t, *args))
print(sorted(os.listdir(OUT)))
