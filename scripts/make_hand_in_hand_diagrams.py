from pathlib import Path
from math import hypot
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'chapters/02-hand-in-hand/assets/diagrams'
OUT.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.truetype('C:/Windows/Fonts/ariali.ttf', 30)
BLACK, BLUE, GRAY = '#20252b', '#326b9c', '#8e969e'


def diagram(name, points, original, auxiliary=(), rights=(), ticks=(), offsets=None):
    offsets = offsets or {}
    xs, ys = zip(*points.values())
    width, height = (760, 680) if max(ys) - min(ys) > max(xs) - min(xs) else (880, 650)
    scale = min((width - 190) / (max(xs) - min(xs)),
                (height - 150) / (max(ys) - min(ys)))
    px = (width - (max(xs) - min(xs)) * scale) / 2
    py = (height - (max(ys) - min(ys)) * scale) / 2
    q = {key: (px + (x - min(xs)) * scale,
               py + (max(ys) - y) * scale) for key, (x, y) in points.items()}
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/>']

    def line(a, b, color=BLACK, dashed=False, weight=3):
        if dashed:
            length = hypot(b[0] - a[0], b[1] - a[1])
            for start in range(0, int(length), 17):
                end = min(start + 10, length)
                draw.line([(a[0] + (b[0] - a[0]) * start / length,
                            a[1] + (b[1] - a[1]) * start / length),
                           (a[0] + (b[0] - a[0]) * end / length,
                            a[1] + (b[1] - a[1]) * end / length)], fill=color, width=weight)
        else:
            draw.line([a, b], fill=color, width=weight)
        dash = ' stroke-dasharray="10 7"' if dashed else ''
        svg.append(f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" stroke="{color}" stroke-width="{weight}"{dash}/>')

    for a, b in original:
        line(q[a], q[b])
    for a, b in auxiliary:
        line(q[a], q[b], BLUE, True)
    for a, v, b in rights:
        u = (q[a][0] - q[v][0], q[a][1] - q[v][1])
        w = (q[b][0] - q[v][0], q[b][1] - q[v][1])
        lu, lw = hypot(*u), hypot(*w)
        u = (u[0] * 17 / lu, u[1] * 17 / lu)
        w = (w[0] * 17 / lw, w[1] * 17 / lw)
        t1 = (q[v][0] + u[0], q[v][1] + u[1])
        t2 = (t1[0] + w[0], t1[1] + w[1])
        t3 = (q[v][0] + w[0], q[v][1] + w[1])
        line(t1, t2, GRAY, weight=2)
        line(t2, t3, GRAY, weight=2)
    for a, b, count in ticks:
        u = (q[b][0] - q[a][0], q[b][1] - q[a][1])
        length = hypot(*u)
        u = (u[0] / length, u[1] / length)
        mid = ((q[a][0] + q[b][0]) / 2, (q[a][1] + q[b][1]) / 2)
        for k in range(count):
            shift = (k - (count - 1) / 2) * 7
            center = (mid[0] + u[0] * shift, mid[1] + u[1] * shift)
            line((center[0] - u[1] * 10.5, center[1] + u[0] * 10.5),
                 (center[0] + u[1] * 10.5, center[1] - u[0] * 10.5), weight=2)
    for label, p in q.items():
        dx, dy = offsets.get(label, (10, -28))
        pos = (p[0] + dx, p[1] + dy)
        box = draw.textbbox(pos, label, font=FONT)
        draw.rectangle((box[0] - 2, box[1] - 1, box[2] + 2, box[3] + 1), fill='white')
        draw.text(pos, label, font=FONT, fill=BLACK)
        svg.append(f'<text x="{pos[0]:.3f}" y="{pos[1]+28:.3f}" font-family="Arial, sans-serif" font-size="30" font-style="italic" fill="{BLACK}">{escape(label)}</text>')
    svg.append('</svg>')
    img.save(OUT / f'{name}.png')
    (OUT / f'{name}.svg').write_text('\n'.join(svg), encoding='utf-8')


p1 = dict(A=(0, 4), B=(0, 0), C=(4, 0), D=(-1, 1), E=(3, 3), F=(1, -1))
edges1 = [('A', 'B'), ('B', 'C'), ('A', 'C'), ('A', 'D'), ('A', 'E'),
          ('D', 'E'), ('D', 'F'), ('C', 'F'), ('C', 'E')]
rights1 = [('D', 'A', 'E'), ('A', 'B', 'C')]
ticks1 = [('A', 'D', 1), ('A', 'E', 1), ('A', 'B', 2), ('B', 'C', 2),
          ('D', 'B', 3), ('B', 'F', 3)]
labels1 = dict(A=(-12, -39), B=(-34, -7), C=(13, -8), D=(-40, -17),
               E=(12, -21), F=(-13, 12))
diagram('example-1', p1, edges1, rights=rights1, ticks=ticks1, offsets=labels1)
diagram('example-1-extend-ab', dict(p1, G=(0, -4)), edges1,
        [('B', 'G'), ('G', 'F'), ('G', 'C')], rights1 + [('A', 'C', 'G')], ticks1,
        dict(labels1, G=(-14, 13)))
diagram('example-1-rotate-ac', dict(p1, G=(-4, 0)), edges1,
        [('B', 'G'), ('G', 'A'), ('G', 'D')], rights1 + [('G', 'A', 'C')], ticks1,
        dict(labels1, G=(-36, -12)))

p2 = dict(B=(0, 0), A=(3, 3), C=(6, 0), D=(4.8, 4.8), E=(0, 3.6))
edges2 = [('B', 'D'), ('A', 'C'), ('B', 'C'), ('D', 'C'), ('D', 'E'),
          ('C', 'E'), ('B', 'E')]
rights2 = [('B', 'A', 'C'), ('C', 'D', 'E')]
ticks2 = [('A', 'B', 1), ('A', 'C', 1), ('D', 'C', 2), ('D', 'E', 2)]
labels2 = dict(B=(-29, 13), A=(-22, 9), C=(8, 13), D=(-13, -40), E=(-36, -9))
diagram('example-2', p2, edges2, rights=rights2, ticks=ticks2, offsets=labels2)
p2g = dict(p2, G=(6, 6), F=(9.6, 6))
aux2 = [('D', 'F'), ('D', 'G'), ('C', 'F'), ('C', 'G'), ('G', 'F')]
diagram('example-2-hand-in-hand', p2g, edges2, aux2,
        rights2 + [('B', 'C', 'G')], ticks2,
        dict(labels2, G=(-12, -40), F=(13, -11)))
diagram('example-2-parallel', dict(p2g, P=(3.6, 3.6)), edges2,
        aux2 + [('E', 'P')], rights2, ticks2,
        dict(labels2, G=(-12, -40), F=(13, -11), P=(8, 6)))
print('Created 6 diagrams, each in PNG and SVG')
