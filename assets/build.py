"""Builds the animated profile header (light + dark) from one template.

Colours are the portfolio's own (my-react-app/src/style.css, my-vue-movie/src/style.css)
so the GitHub profile, iamilia.ir and the movie site read as one brand.

Run: python assets/build.py
"""

from pathlib import Path

THEMES = {
    "dark": {"fg": "#f5f5f7", "muted": "#a1a1a6", "accent": "#2997ff", "green": "#30d158", "track": "rgba(255,255,255,0.12)", "lua": "#6a7bff"},
    "light": {"fg": "#1d1d1f", "muted": "#6e6e73", "accent": "#0066cc", "green": "#34c759", "track": "rgba(0,0,0,0.1)", "lua": "#000080"},
}

# Primary language of my own public repos (forks and this repo excluded), GitHub's own colours.
# Snapshot: 2026-11-02. Re-count and re-run when it drifts.
LANGS = [("TypeScript", 3, "#3178c6"), ("Lua", 3, "#000080"), ("Go", 1, "#00add8"), ("Python", 1, "#3572a5")]

FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI Variable Display', 'Segoe UI', system-ui, sans-serif"


def bar(c):
    total = sum(n for _, n, _ in LANGS)
    width, gap, x = 640, 4, 0
    usable = width - gap * (len(LANGS) - 1)
    segs, legend, lx = [], [], 0
    for i, (name, n, color) in enumerate(LANGS):
        color = c["lua"] if name == "Lua" else color
        w = usable * n / total
        segs.append(f'<rect class="seg" style="animation-delay:{900 + i * 110}ms" x="{x:.1f}" y="0" width="{w:.1f}" height="10" rx="5" fill="{color}"/>')
        x += w + gap
        legend.append(
            f'<g transform="translate({lx} 40)"><g class="in" style="animation-delay:{1300 + i * 80}ms">'
            f'<circle cx="5" cy="-6" r="5" fill="{color}"/>'
            f'<text x="18" y="0" fill="{c["fg"]}">{name} <tspan fill="{c["muted"]}">{n}</tspan></text></g></g>'
        )
        lx += 44 + len(f"{name} {n}") * 9.2
    return "\n    ".join(segs), "\n    ".join(legend), total


def svg(c):
    segs, legend, total = bar(c)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 440" width="1200" height="440" role="img" aria-labelledby="t d">
  <title id="t">Ilia Lotfi</title>
  <desc id="d">I write FiveM resources in Lua, and the React and TypeScript tools that run alongside them. Open to projects. Tehran.</desc>
  <style>
    text {{ font-family: {FONT}; }}
    .in {{ opacity: 0; animation: up 700ms cubic-bezier(0.22, 1, 0.36, 1) both; }}
    .seg {{ transform-box: fill-box; transform-origin: left center; transform: scaleX(0); animation: grow 900ms cubic-bezier(0.22, 1, 0.36, 1) both; }}
    .ring {{ transform-box: fill-box; transform-origin: center; animation: ping 2.4s cubic-bezier(0, 0, 0.2, 1) 1.2s infinite; }}
    .caret {{ animation: blink 1.1s steps(1) 1s infinite; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    @keyframes ping {{ 0% {{ transform: scale(1); opacity: 0.55; }} 80%, 100% {{ transform: scale(2.8); opacity: 0; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .in, .seg, .ring, .caret {{ animation: none; opacity: 1; transform: none; }}
      .ring {{ opacity: 0; }}
    }}
  </style>

  <g transform="translate(8 56)"><g class="in" style="animation-delay:0ms">
    <circle class="ring" cx="6" cy="-7" r="6" fill="{c["green"]}"/>
    <circle cx="6" cy="-7" r="6" fill="{c["green"]}"/>
    <text x="24" y="0" font-size="22" fill="{c["muted"]}">Open to projects <tspan dx="10">·</tspan><tspan dx="10">Tehran</tspan><tspan dx="10">·</tspan><tspan dx="10" fill="{c["accent"]}">@iamilia</tspan></text>
  </g></g>

  <g class="in" style="animation-delay:120ms">
    <text x="0" y="192" font-size="128" font-weight="700" letter-spacing="-5" fill="{c["fg"]}">Ilia Lotfi<tspan class="caret" fill="{c["accent"]}" dx="8">_</tspan></text>
  </g>

  <g class="in" style="animation-delay:260ms" font-size="34" font-weight="500" letter-spacing="-0.5" fill="{c["muted"]}">
    <text x="4" y="258">I write FiveM resources in <tspan fill="{c["fg"]}">Lua</tspan>, and the <tspan fill="{c["fg"]}">React</tspan> and</text>
    <text x="4" y="302"><tspan fill="{c["fg"]}">TypeScript</tspan> tools that run alongside them.</text>
  </g>

  <g transform="translate(6 352)" font-size="18">
    <rect class="in" style="animation-delay:700ms" x="0" y="0" width="640" height="10" rx="5" fill="{c["track"]}"/>
    {segs}
    {legend}
    <text class="in" style="animation-delay:1700ms" x="0" y="78" font-size="17" fill="{c["muted"]}">Primary language of my {total} own public repositories</text>
  </g>
</svg>
"""


STACK = [
    ("Game servers", ["Lua", "FiveM", "ESX · QBCore", "ox_lib · oxmysql", "Discord.js"]),
    ("Web", ["React", "TypeScript", "JavaScript · HTML · CSS", "Next.js · Vue", "Tailwind CSS · Sass", "Zustand · Vite"]),
    ("Backend", ["Node.js", "Express", "Python · Go", "C++ · Bash", "Socket.io"]),
    ("Data &amp; tools", ["PostgreSQL", "MySQL", "MongoDB · Redis", "Prisma · Drizzle", "Git · HeidiSQL · FFmpeg", "Visual Studio · Figma"]),
]


def stack_svg(c):
    STACK_TITLE = "Stack — " + ". ".join(f"{t}: {', '.join(i)}" for t, i in STACK).replace(" · ", ", ") + "."
    cols = []
    for i, (title, items) in enumerate(STACK):
        base = i * 140
        rows = "".join(
            f'<g transform="translate(0 {96 + j * 40})"><text class="in" style="animation-delay:{base + 300 + j * 70}ms" '
            f'font-size="{26 if j < 2 else 22}" font-weight="{600 if j < 2 else 400}" fill="{c["fg"] if j < 2 else c["muted"]}">{item}</text></g>'
            for j, item in enumerate(items)
        )
        cols.append(
            f'<g transform="translate({6 + i * 300} 0)">'
            f'<rect x="0" y="0" width="260" height="2" rx="1" fill="{c["track"]}"/>'
            f'<rect class="seg" style="animation-delay:{base}ms" x="0" y="0" width="260" height="2" rx="1" fill="{c["accent"]}"/>'
            f'<text class="in" style="animation-delay:{base + 150}ms" y="46" font-size="20" fill="{c["accent"]}">{title}</text>'
            f"{rows}</g>"
        )
    body = "\n  ".join(cols)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="1200" height="320" role="img" aria-labelledby="st">
  <title id="st">{STACK_TITLE}</title>
  <style>
    text {{ font-family: {FONT}; letter-spacing: -0.2px; }}
    .in {{ opacity: 0; animation: up 700ms cubic-bezier(0.22, 1, 0.36, 1) both; }}
    .seg {{ transform-box: fill-box; transform-origin: left center; transform: scaleX(0); animation: grow 1100ms cubic-bezier(0.22, 1, 0.36, 1) both; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .in, .seg {{ animation: none; opacity: 1; transform: none; }} }}
  </style>
  {body}
</svg>
"""


out = Path(__file__).parent
for name, colors in THEMES.items():
    for kind, fn in (("header", svg), ("stack", stack_svg)):
        (out / f"{kind}-{name}.svg").write_text(fn(colors), encoding="utf-8")
        print("wrote", out / f"{kind}-{name}.svg")
