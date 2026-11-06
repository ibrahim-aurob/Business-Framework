# Erzeugt die technischen Zeichnungen als Inline-SVG.
s=2.6; x0=105; cy=232
segs=[(22,24),(4,19.5),(44,40),(30,60),(38,32),(12,26)]  # (Länge mm, Ø mm)
ch=1.0*s
pts=[]; x=x0
xs=[x0]
for L,d in segs:
    xs.append(xs[-1]+L*s)
def up(r): return cy-r*s/2*1  # r here = diameter
# outline upper: step profile with chamfers on outer ends of each shoulder (simple)
path=[]
x=x0
first=True
for i,(L,d) in enumerate(segs):
    y=cy-d*s/2
    xa=xs[i]; xb=xs[i+1]
    if first:
        path.append(f"M{xa:.1f},{cy:.1f} L{xa:.1f},{y+ch:.1f} L{xa+ch:.1f},{y:.1f}")
        first=False
    else:
        path.append(f"L{xa:.1f},{y:.1f}")
    if i==len(segs)-1:
        path.append(f"L{xb-ch:.1f},{y:.1f} L{xb:.1f},{y+ch:.1f} L{xb:.1f},{cy:.1f}")
    else:
        ny=cy-segs[i+1][1]*s/2
        path.append(f"L{xb:.1f},{y:.1f} L{xb:.1f},{ny:.1f}")
upper=" ".join(path)
# mirror
import re
def mirror(p):
    return re.sub(r"(-?\d+\.?\d*),(-?\d+\.?\d*)", lambda m: f"{m.group(1)},{2*cy-float(m.group(2)):.1f}", p)
lower=mirror(upper)
# vertical shoulder lines (full)
vl=[]
for i in range(1,len(segs)):
    d=min(segs[i-1][1],segs[i][1])
    vl.append(f'<line x1="{xs[i]:.1f}" y1="{cy-d*s/2:.1f}" x2="{xs[i]:.1f}" y2="{cy+d*s/2:.1f}"/>')
# thread minor lines on first seg
tr=24*0.85*s/2
thread=f'<line class="thin" x1="{x0+ch:.1f}" y1="{cy-tr:.1f}" x2="{xs[1]:.1f}" y2="{cy-tr:.1f}"/><line class="thin" x1="{x0+ch:.1f}" y1="{cy+tr:.1f}" x2="{xs[1]:.1f}" y2="{cy+tr:.1f}"/>'
# section hatch on lower half of collar (partial section)
xa,xb=xs[3],xs[4]; ya=cy; yb=cy+60*s/2
hatch=[]
k=-200
while k<400:
    hatch.append(f'<line x1="{xa+k:.1f}" y1="{yb:.1f}" x2="{xa+k+ (yb-ya):.1f}" y2="{ya:.1f}"/>')
    k+=7
total=sum(L for L,_ in segs)
xe=xs[-1]
dim_y=cy+60*s/2+46
svg=f'''<svg viewBox="0 0 600 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Technische Zeichnung eines Serien-Drehteils: Gesamtlänge 150 mm, größter Durchmesser 60 mm, Gewinde M24">
<defs>
<clipPath id="hc"><rect x="{xa:.1f}" y="{ya:.1f}" width="{xb-xa:.1f}" height="{yb-ya:.1f}"/></clipPath>
<marker id="ar" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,2 L10,5 L0,8 z" fill="#15171a"/></marker>
</defs>
<g fill="none" stroke="#c9c4ba" stroke-width="0.5">{"".join(f'<line x1="{gx}" y1="0" x2="{gx}" y2="470"/>' for gx in range(0,601,20))}{"".join(f'<line x1="0" y1="{gy}" x2="600" y2="{gy}"/>' for gy in range(10,471,20))}</g>
<g clip-path="url(#hc)" stroke="#15171a" stroke-width="0.7" opacity=".55">{"".join(hatch)}</g>
<g fill="none" stroke="#15171a" stroke-width="2" stroke-linejoin="round"><path d="{upper}"/><path d="{lower}"/></g>
<g stroke="#15171a" stroke-width="1.2">{"".join(vl)}</g>
<g stroke="#15171a" stroke-width="0.8" class="thin">{thread}</g>
<line x1="{x0-28}" y1="{cy}" x2="{xe+28}" y2="{cy}" stroke="#e2520f" stroke-width="1" stroke-dasharray="22 4 3 4"/>
<g stroke="#15171a" stroke-width="0.8" fill="none">
<line x1="{x0}" y1="{cy+12*s+6:.1f}" x2="{x0}" y2="{dim_y+8:.1f}"/>
<line x1="{xe}" y1="{cy+13*s+6:.1f}" x2="{xe}" y2="{dim_y+8:.1f}"/>
<line x1="{x0}" y1="{dim_y:.1f}" x2="{xe}" y2="{dim_y:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/>
<line x1="{xs[3]-6:.1f}" y1="{cy-30*s:.1f}" x2="{xs[3]-6:.1f}" y2="{cy-30*s:.1f}"/>
<line x1="{(xs[3]+xs[4])/2:.1f}" y1="{cy-30*s:.1f}" x2="{(xs[3]+xs[4])/2:.1f}" y2="{cy+30*s:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/>
<line x1="{(xs[2]+xs[3])/2-30:.1f}" y1="{cy-20*s:.1f}" x2="{(xs[2]+xs[3])/2-30:.1f}" y2="{cy+20*s:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/>
<polyline points="{x0+22:.1f},{cy-12*s:.1f} {x0+40:.1f},{cy-12*s-58:.1f} {x0+92:.1f},{cy-12*s-58:.1f}"/>
<line x1="{xs[2]:.1f}" y1="{cy-40*s/2-4:.1f}" x2="{xs[2]:.1f}" y2="{cy-30*s-30:.1f}"/>
<line x1="{xs[3]:.1f}" y1="{cy-30*s-4:.1f}" x2="{xs[3]:.1f}" y2="{cy-30*s-30:.1f}"/>
<line x1="{xs[2]:.1f}" y1="{cy-30*s-22:.1f}" x2="{xs[3]:.1f}" y2="{cy-30*s-22:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/>
</g>
<g font-family="Plex Mono, monospace" font-size="13" fill="#15171a">
<text x="{(x0+xe)/2:.1f}" y="{dim_y-7:.1f}" text-anchor="middle" fill="#15171a" paint-order="stroke" stroke="#f7f6f2" stroke-width="4">150</text>
<text transform="translate({(xs[3]+xs[4])/2-6:.1f},{cy-18:.1f}) rotate(-90)" text-anchor="end" paint-order="stroke" stroke="#f7f6f2" stroke-width="4">Ø60 h9</text>
<text transform="translate({(xs[2]+xs[3])/2-36:.1f},{cy-10:.1f}) rotate(-90)" text-anchor="end" paint-order="stroke" stroke="#f7f6f2" stroke-width="4">Ø40 g6</text>
<text x="{x0+46:.1f}" y="{cy-12*s-64:.1f}">M24×1,5</text>
<text x="{(xs[2]+xs[3])/2:.1f}" y="{cy-30*s-28:.1f}" text-anchor="middle">44</text>
<text x="{x0-28}" y="28" font-size="11" fill="#6b727b">A–A  TEILSCHNITT</text>
<text x="572" y="28" font-size="11" fill="#6b727b" text-anchor="end">Ra 1,6 (√)</text>
</g>
</svg>'''
open(__import__('os').path.join(__import__('os').path.dirname(__file__),'hero.svg'),'w').write(svg)

# Hüllkurven-Diagramm: Länge (x) gegen Durchmesser (y)
W,H=640,420; ml,mr,mt,mb=64,24,28,58
pw=W-ml-mr; ph=H-mt-mb
X=lambda L: ml+L/160*pw
Y=lambda d: mt+ph-(d/70)*ph
grid=""
for L in range(0,161,10):
    grid+=f'<line x1="{X(L):.1f}" y1="{mt}" x2="{X(L):.1f}" y2="{mt+ph}" stroke="#d8d3c9" stroke-width="{0.9 if L%50==0 else 0.5}"/>'
for d in range(0,71,5):
    grid+=f'<line x1="{ml}" y1="{Y(d):.1f}" x2="{ml+pw}" y2="{Y(d):.1f}" stroke="#d8d3c9" stroke-width="{0.9 if d%10==0 else 0.5}"/>'
ticks=""
for L in [0,20,40,60,80,100,120,150]:
    ticks+=f'<text x="{X(L):.1f}" y="{mt+ph+20}" text-anchor="middle">{L}</text>'
for d in [0,6,20,40,60]:
    ticks+=f'<text x="{ml-10}" y="{Y(d)+4:.1f}" text-anchor="end">{d}</text>'
zoneA=f'<rect x="{X(0):.1f}" y="{Y(40):.1f}" width="{X(80)-X(0):.1f}" height="{Y(6)-Y(40):.1f}"/>'
zoneB=f'<rect x="{X(0):.1f}" y="{Y(60):.1f}" width="{X(150)-X(0):.1f}" height="{Y(40)-Y(60):.1f}"/>'
env=f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Leistungsbereich: Durchmesser 6 bis 40 Millimeter bis 80 Millimeter Länge, Durchmesser 40 bis 60 Millimeter bis 150 Millimeter Länge">
<defs>
<pattern id="hA" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#15171a" stroke-width="1"/></pattern>
<pattern id="hB" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#e2520f" stroke-width="1.2"/></pattern>
</defs>
{grid}
<g fill="url(#hA)" stroke="#15171a" stroke-width="1.8" opacity=".9">{zoneA}</g>
<g fill="url(#hB)" stroke="#e2520f" stroke-width="1.8">{zoneB}</g>
<g id="probe" style="display:none"><circle r="7" fill="#fff" stroke="#15171a" stroke-width="2"/><circle r="2.5" fill="#15171a"/></g>
<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="#15171a" stroke-width="1.4"/>
<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="#15171a" stroke-width="1.4"/>
<g font-family="Plex Mono, monospace" font-size="12" fill="#3b4047">{ticks}
<text x="{ml+pw}" y="{H-8}" text-anchor="end" fill="#15171a">LÄNGE [mm] →</text>
<text transform="translate(16,{mt}) rotate(-90)" text-anchor="end" fill="#15171a">↑ DURCHMESSER [mm]</text>
</g>
<g font-family="Plex Mono, monospace" font-size="13" font-weight="500">
<text x="{X(4):.1f}" y="{Y(23)+5:.1f}" fill="#15171a" paint-order="stroke" stroke="#f7f6f2" stroke-width="5">A · Ø6–40 · L ≤ 80</text>
<text x="{X(84):.1f}" y="{Y(50)+5:.1f}" fill="#b63f08" paint-order="stroke" stroke="#f7f6f2" stroke-width="5">B · Ø40–60 · L ≤ 150</text>
</g>
</svg>'''
open(__import__('os').path.join(__import__('os').path.dirname(__file__),'envelope.svg'),'w').write(env)
