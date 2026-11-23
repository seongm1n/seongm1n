"""stdin: GitHub GraphQL contributionCalendar JSON -> assets/contrib-{dark,light}.svg"""
import json
import sys

cal = json.load(sys.stdin)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
OPACITY = {"FIRST_QUARTILE": .3, "SECOND_QUARTILE": .55, "THIRD_QUARTILE": .8, "FOURTH_QUARTILE": 1}

cols = []
for c, week in enumerate(cal["weeks"]):
    cells = ""
    for d in week["contributionDays"]:
        op = OPACITY.get(d["contributionLevel"])
        fill = 'fill="#30363d"' if op is None else f'fill="#6b8afd" fill-opacity="{op}"'
        cells += f'<rect y="{48 + d["weekday"] * 14}" width="10" height="10" rx="2" {fill}/>'
    # delays: reveal left to right once, then a ripple every 8s
    cols.append(f'<g class="c" transform="translate({51 + c * 14})" '
                f'style="animation-delay:{.2 + c * .03:.2f}s,{3 + c * .05:.2f}s">{cells}</g>')

dark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 170" width="840" height="170" role="img" aria-label="{cal["totalContributions"]} contributions in the last year">
  <style>
    text {{ font: 500 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 3px; fill: #8b949e; text-anchor: middle; }}
    .c {{ animation: rise .5s backwards, ripple 8s linear infinite; }}
    @keyframes rise {{ from {{ opacity: 0; }} }}
    @keyframes ripple {{ 0%, 12%, 100% {{ opacity: 1; }} 5% {{ opacity: .4; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <text x="420" y="24">{cal["totalContributions"]:,} CONTRIBUTIONS · LAST 12 MONTHS</text>
  {"".join(cols)}
</svg>
'''

# same palette swap as the header: fg / muted / accent / line
light = dark.replace("#8b949e", "#656a75").replace("#6b8afd", "#3457d5").replace("#30363d", "#d8dae0")
open("assets/contrib-dark.svg", "w").write(dark)
open("assets/contrib-light.svg", "w").write(light)
