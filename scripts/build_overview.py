#!/usr/bin/env python3
"""Generate assets/overview-{light,dark}.svg.

Pill widths come from real Chromium text metrics (see MEASURED), not guesses,
so the focus row cannot overflow its column. Re-run after editing CONTENT.
"""
from pathlib import Path
from xml.sax.saxutils import escape

W, H = 1280, 500
LEFT_X, RAIL_X, TEXT_X = 76, 94, 124
RIGHT_X, RIGHT_W = 700, 504

SANS = "'Outfit','Segoe UI',-apple-system,Helvetica,Arial,sans-serif"
SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style','Palatino Linotype',serif"

ROLES = [
    ("Aug 2026 · Anna University", "Research Assistant",
     "Autonomous Research Supervision Agent"),
    ("Feb 2026 · IIT Madras", "Undergraduate Researcher",
     "Symbolic Regression for Packed-Bed Transport"),
    ("University of Toronto · remote", "Research Engineer",
     "AI Research Infrastructure"),
    ("Apr 2025 · Anna University, MIT Campus", "Undergraduate Researcher",
     "Sign-Language Translation & Explainable Medical Imaging"),
]

# Chromium canvas measureText @ 500 15px SANS
MEASURED = {
    "Symbolic Regression": 140.9, "Equation Discovery": 129.2,
    "Neuro-Symbolic AI": 125.0, "Explainable AI": 95.9,
    "Computer Vision": 110.6, "Multi-Agent Systems": 137.5,
}
PAD, GAP, PILL_H, ROW_GAP = 18, 12, 38, 14

PUBS = [
    ("IEEE Xplore · ICIETSD 2026",
     "Neural Translation of Tamil to Indian Sign Language"),
    ("Springer (IFIP-endorsed) · ICCCSP 2026 · accepted",
     "From ASL to ISL: Translating Gestures across Sign Languages"),
]

THEMES = {
    "light": dict(bg0="#f2f0ea", bg1="#edeae2", bg2="#e6e2d8", glow="#ccba9c",
                  glow_op="0.34", ink="#141208", body="#4a4436", muted="#716d60",
                  bronze="#9b7b50", rail="#dedad1", pill_fill="#ffffff",
                  pill_op="0.55"),
    "dark": dict(bg0="#141208", bg1="#1a1710", bg2="#241e14", glow="#9b7b50",
                 glow_op="0.24", ink="#f2f0ea", body="#ccba9c", muted="#8d8677",
                 bronze="#9b7b50", rail="#2e2718", pill_fill="#9b7b50",
                 pill_op="0.10"),
}


def tracked(s: str) -> str:
    """Letter-spaced small caps label, e.g. 'R E S E A R C H'."""
    return escape(" ".join(s.upper()))


def pill_rows():
    """Pack focus pills into rows that fit RIGHT_W."""
    rows, row, used = [], [], 0.0
    for label, tw in MEASURED.items():
        w = tw + 2 * PAD
        if row and used + GAP + w > RIGHT_W:
            rows.append(row)
            row, used = [], 0.0
        row.append((label, w))
        used += (GAP if used else 0) + w
    if row:
        rows.append(row)
    return rows


def build(t: dict) -> str:
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="Overview: research '
        f'timeline, focus areas and 2026 publications for Ruparagunath G">',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["bg0"]}"/>'
        f'<stop offset="0.6" stop-color="{t["bg1"]}"/>'
        f'<stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>',
        f'<radialGradient id="gl" cx="0.78" cy="0.15" r="0.6">'
        f'<stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glow_op"]}"/>'
        f'<stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#gl)"/>',
        f'<rect width="{W}" height="3" fill="{t["bronze"]}"/>',
    ]

    def label(x, y, text):
        o.append(f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="12.5" '
                 f'letter-spacing="4.2" font-weight="500" fill="{t["bronze"]}">'
                 f'{tracked(text)}</text>')

    # ---- left: research timeline -------------------------------------
    label(LEFT_X, 74, "Research")
    o.append(f'<line x1="{RAIL_X}" y1="102" x2="{RAIL_X}" y2="478" '
             f'stroke="{t["rail"]}" stroke-width="2"/>')
    for i, (where, role, detail) in enumerate(ROLES):
        y = 132 + i * 94
        r, op = (7, "1") if i == 0 else (5, "0.75")
        o.append(f'<circle cx="{RAIL_X}" cy="{y - 5}" r="{r}" '
                 f'fill="{t["bronze"]}" fill-opacity="{op}"/>')
        o.append(f'<text x="{TEXT_X}" y="{y}" font-family="{SANS}" font-size="12.5" '
                 f'letter-spacing="0.7" fill="{t["bronze"]}">{escape(where)}</text>')
        o.append(f'<text x="{TEXT_X}" y="{y + 27}" font-family="{SERIF}" '
                 f'font-size="24" fill="{t["ink"]}">{escape(role)}</text>')
        o.append(f'<text x="{TEXT_X}" y="{y + 50}" font-family="{SANS}" '
                 f'font-size="14" fill="{t["muted"]}">{escape(detail)}</text>')

    # ---- right: focus pills ------------------------------------------
    label(RIGHT_X, 74, "Focus")
    y = 100
    for row in pill_rows():
        x = RIGHT_X
        for text, w in row:
            o.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{PILL_H}" '
                     f'rx="{PILL_H/2}" fill="{t["pill_fill"]}" '
                     f'fill-opacity="{t["pill_op"]}" stroke="{t["bronze"]}" '
                     f'stroke-opacity="0.45" stroke-width="1"/>')
            o.append(f'<text x="{x + w/2:.1f}" y="{y + 25}" text-anchor="middle" '
                     f'font-family="{SANS}" font-size="15" font-weight="500" '
                     f'fill="{t["body"]}">{escape(text)}</text>')
            x += w + GAP
        y += PILL_H + ROW_GAP

    # ---- right: publications -----------------------------------------
    div = y + 22
    o.append(f'<line x1="{RIGHT_X}" y1="{div}" x2="{RIGHT_X + RIGHT_W}" y2="{div}" '
             f'stroke="{t["rail"]}" stroke-width="1.5"/>')
    label(RIGHT_X, div + 42, "Publications")
    py = div + 78
    for venue, title in PUBS:
        o.append(f'<text x="{RIGHT_X}" y="{py}" font-family="{SANS}" font-size="12.5" '
                 f'letter-spacing="0.5" fill="{t["bronze"]}">{escape(venue)}</text>')
        o.append(f'<text x="{RIGHT_X}" y="{py + 26}" font-family="{SERIF}" '
                 f'font-size="18" fill="{t["ink"]}">{escape(title)}</text>')
        py += 62
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        p = out / f"overview-{name}.svg"
        p.write_text(build(theme), encoding="utf-8")
        print("wrote", p.name)
