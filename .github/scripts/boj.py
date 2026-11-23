"""stdin: mazassumnida v2 badge SVG -> assets/boj-{dark,light}.svg

solved.ac's own API sits behind a Cloudflare challenge, so the numbers are read from the badge instead.
"""
import re
import sys
from bisect import bisect_right

FLOORS = [30, 60, 90, 120, 150, 200, 300, 400, 500, 650, 800, 950, 1100, 1250, 1400,
          1600, 1750, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2850, 2900, 2950, 3000]
NAMES = [f"{m} {r}" for m in ("Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby")
         for r in ("V", "IV", "III", "II", "I")] + ["Master"]
CELLS = 53  # same columns and pitch as the contribution graph above it


def tier(rating):
    """-> (tier name, next tier name or None, next tier's floor or None, percent of the way there)"""
    i = bisect_right(FLOORS, rating) - 1
    if i < 0:
        return "Unrated", NAMES[0], FLOORS[0], 100 * rating // FLOORS[0]
    if i == len(NAMES) - 1:
        return NAMES[i], None, None, 100
    return NAMES[i], NAMES[i + 1], FLOORS[i + 1], 100 * (rating - FLOORS[i]) // (FLOORS[i + 1] - FLOORS[i])


assert tier(1771) == ("Platinum IV", "Platinum III", 1900, 14)
assert tier(3100) == ("Master", None, None, 100)

texts = [t.strip() for t in re.findall(r"<text[^>]*>([^<]+)</text>", sys.stdin.read())]
value = lambda label: texts[texts.index(label) + 1]  # raises if the badge layout changed
rating = int(value("rate").replace(",", ""))
name, nxt, nxt_floor, pct = tier(rating)

filled = round(pct * CELLS / 100)
bar = "".join(
    f'<rect class="c" x="{51 + i * 14}" y="48" width="10" height="10" rx="2" '
    f'fill="{"#6b8afd" if i < filled else "#30363d"}" style="animation-delay:{.2 + i * .03:.2f}s"/>'
    for i in range(CELLS))
goal = f'<text x="789" y="86" text-anchor="end">{pct}% → {nxt.upper()} · {nxt_floor:,}</text>' if nxt else ""

dark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 110" width="840" height="110" role="img" aria-label="Baekjoon: {name}, rating {rating}, {value("solved")} solved">
  <style>
    text {{ font: 500 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 3px; fill: #8b949e; }}
    .now {{ fill: #e6edf3; }}
    .c {{ animation: rise .5s backwards; }}
    @keyframes rise {{ from {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <text x="420" y="24" text-anchor="middle">BAEKJOON · {value("solved")} SOLVED · CLASS {value("class")}</text>
  {bar}
  <text class="now" x="51" y="86">{name.upper()} · {rating:,}</text>
  {goal}
</svg>
'''

# same palette swap as the header: fg / muted / accent / line
light = dark
for a, b in (("#e6edf3", "#17191d"), ("#8b949e", "#656a75"), ("#6b8afd", "#3457d5"), ("#30363d", "#d8dae0")):
    light = light.replace(a, b)
open("assets/boj-dark.svg", "w").write(dark)
open("assets/boj-light.svg", "w").write(light)
print(name, rating, f"{pct}%")
