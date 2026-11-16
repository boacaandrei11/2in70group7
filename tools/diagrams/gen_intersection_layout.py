# Run from the repository root: python tools/diagrams/gen_intersection_layout.py
# generates docs/diagrams/intersection-layout.svg
O=20; C=370; H=60; L=C-H; R=C+H   # map offset, centre, half road width
def T(x,y): return x+O,y+O
out=[]
def a(s): out.append(s)
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1220 800" width="1220" height="800">')
a('''<style>
text{font-family:"Segoe UI",-apple-system,"Helvetica Neue",Arial,sans-serif;fill:#1e293b}
.h{font-size:19px;font-weight:700}.h2{font-size:14px;font-weight:700}.s{font-size:13px;fill:#475569}
.tag{font-size:11px;font-weight:700;letter-spacing:.08em;fill:#64748b}.m{font-size:12px;fill:#ffffff;font-weight:700}
.ml{font-size:13px;font-weight:700;fill:#334155}
</style>
<defs><marker id="ax" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker>
<radialGradient id="fan" cx="0.5" cy="1" r="1"><stop offset="0" stop-color="#14b8a6" stop-opacity=".35"/><stop offset="1" stop-color="#14b8a6" stop-opacity="0"/></radialGradient></defs>''')
a('<rect x="1" y="1" width="1218" height="798" rx="14" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>')
# map
a(f'<g transform="translate({O},{O})">')
a('<rect x="0" y="0" width="740" height="740" rx="10" fill="#e3ecdf"/>')
# sidewalks
a(f'<rect x="{L-14}" y="0" width="{2*H+28}" height="740" fill="#cfd8dc"/><rect x="0" y="{L-14}" width="740" height="{2*H+28}" fill="#cfd8dc"/>')
# roads
a(f'<rect x="{L}" y="0" width="{2*H}" height="740" fill="#3f4b59"/><rect x="0" y="{L}" width="740" height="{2*H}" fill="#3f4b59"/>')
# centre dashes
a(f'<line x1="{C}" y1="0" x2="{C}" y2="262" stroke="#fbbf24" stroke-width="2.5" stroke-dasharray="16 12"/>')
a(f'<line x1="{C}" y1="478" x2="{C}" y2="740" stroke="#fbbf24" stroke-width="2.5" stroke-dasharray="16 12"/>')
a(f'<line x1="0" y1="{C}" x2="262" y2="{C}" stroke="#fbbf24" stroke-width="2.5" stroke-dasharray="16 12"/>')
a(f'<line x1="478" y1="{C}" x2="740" y2="{C}" stroke="#fbbf24" stroke-width="2.5" stroke-dasharray="16 12"/>')
# crossings: south (y438-464), north (276-302): stripes vertical across x L..R
def zebra_h(y0):  # crossing across a vertical arm
    for x in range(L+4,R-4,14): a(f'<rect x="{x}" y="{y0}" width="8" height="26" fill="#f8fafc"/>')
def zebra_v(x0):
    for y in range(L+4,R-4,14): a(f'<rect x="{x0}" y="{y}" width="26" height="8" fill="#f8fafc"/>')
zebra_h(438); zebra_h(276); zebra_v(438); zebra_v(276)
# stop lines (approach lane only)
a(f'<rect x="{C}" y="472" width="{H}" height="5" fill="#ffffff"/>')      # northbound
a(f'<rect x="{L}" y="263" width="{H}" height="5" fill="#ffffff"/>')      # southbound
a(f'<rect x="472" y="{L}" width="5" height="{H}" fill="#ffffff"/>')      # westbound
a(f'<rect x="263" y="{C}" width="5" height="{H}" fill="#ffffff"/>')      # eastbound
# signals
def sig_v(x,y,lit):  # vertical housing: red, amber, green top->bottom
    a(f'<rect x="{x}" y="{y}" width="14" height="38" rx="3" fill="#111827"/>')
    for i,c in enumerate(["#ef4444","#f59e0b","#22c55e"]):
        on = (["red","amber","green"][i]==lit)
        a(f'<circle cx="{x+7}" cy="{y+7+i*12}" r="4.3" fill="{c if on else "#374151"}"/>')
def sig_h(x,y,lit):
    a(f'<rect x="{x}" y="{y}" width="38" height="14" rx="3" fill="#111827"/>')
    for i,c in enumerate(["#ef4444","#f59e0b","#22c55e"]):
        on = (["red","amber","green"][i]==lit)
        a(f'<circle cx="{x+7+i*12}" cy="{y+7}" r="4.3" fill="{c if on else "#374151"}"/>')
sig_v(R+4,478,"green")   # northbound, right side
sig_v(L-18,224,"green")  # southbound
sig_h(478,L-18,"red")    # westbound (north side)
sig_h(224,R+4,"red")     # eastbound (south side)
# perception fan for smart vehicle (northbound, x centre 400)
a('<path d="M400 520 L340 330 A200 200 0 0 1 460 330 Z" fill="url(#fan)"/>')
# vehicles
def car_v(cx,y,fill,stroke,label,txt="#fff"):
    a(f'<rect x="{cx-13}" y="{y}" width="26" height="44" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    a(f'<text x="{cx}" y="{y+27}" text-anchor="middle" style="font-size:12px;font-weight:700;fill:{txt}">{label}</text>')
def car_h(x,cy,fill,stroke,label):
    a(f'<rect x="{x}" y="{cy-13}" width="44" height="26" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    a(f'<text x="{x+22}" y="{cy+4}" text-anchor="middle" style="font-size:12px;font-weight:700;fill:#fff">{label}</text>')
car_v(400,520,"#0f766e","#99f6e4","S1")
car_v(400,600,"#64748b","#cbd5e1","C2")
car_v(340,150,"#64748b","#cbd5e1","C3")
car_h(484,340,"#64748b","#cbd5e1","C4")
car_h(212,400,"#64748b","#cbd5e1","C5")
# heading ticks
a('<path d="M400 512 l-6 8 h12 z" fill="#99f6e4"/>')
# pedestrians
def X(x,y,lab,dx=11):
    a(f'<path d="M{x-7} {y-7} L{x+7} {y+7} M{x+7} {y-7} L{x-7} {y+7}" stroke="#dc2626" stroke-width="3.5" stroke-linecap="round"/>')
    a(f'<text x="{x+dx}" y="{y+5}" style="font-size:12px;font-weight:700;fill:#991b1b;paint-order:stroke;stroke:#ffffff;stroke-width:3px">{lab}</text>')
X(451,328,"P1",-30); X(292,486,"P2"); X(452,256,"P3")
# coordinate frame
a(f'<circle cx="{C}" cy="{C}" r="3.5" fill="#fbbf24"/>')
a(f'<line x1="{C}" y1="{C}" x2="{C+40}" y2="{C}" stroke="#fbbf24" stroke-width="2" marker-end="url(#ax)"/>')
a(f'<line x1="{C}" y1="{C}" x2="{C}" y2="{C-40}" stroke="#fbbf24" stroke-width="2" marker-end="url(#ax)"/>')
a(f'<text x="{C+44}" y="{C+5}" style="font-size:12px;font-weight:700;fill:#fbbf24">x</text>')
a(f'<text x="{C-4}" y="{C-46}" style="font-size:12px;font-weight:700;fill:#fbbf24">y</text>')
a(f'<text x="{C+6}" y="{C+18}" style="font-size:11px;fill:#fde68a">(0, 0) m</text>')
# arm labels
for (x,y,t) in [(C+150,40,"NORTH ARM"),(C+150,722,"SOUTH ARM"),(70,C-84,"WEST ARM"),(670,C-84,"EAST ARM")]:
    a(f'<text x="{x}" y="{y}" text-anchor="middle" class="ml" style="letter-spacing:.06em">{t}</text>')
a('</g>')
# right panel
X0=800
a(f'<text x="{X0}" y="54" class="tag">INTERSECTION LAYOUT  ·  ODD BASELINE  ·  MAP CONCEPT</text>')
a(f'<text x="{X0}" y="84" class="h">Four-arm signalised junction</text>')
a(f'<text x="{X0}" y="108" class="s">Shown at phase <tspan style="font-weight:700;fill:#15803d">NS_GREEN</tspan> (EW red).</text>')
y=150
def leg(svg,title,sub):
    global y
    a(svg.replace("Y",str(y)))
    a(f'<text x="{X0+50}" y="{y+5}" class="h2">{title}</text>')
    a(f'<text x="{X0+50}" y="{y+23}" class="s">{sub}</text>')
    y+=56
leg(f'<rect x="{X0+6}" y="Y" width="26" height="18" rx="4" transform="translate(0,-12)" fill="#0f766e" stroke="#99f6e4" stroke-width="2"/>',"Smart vehicle","perception → decision, distinct marker")
leg(f'<rect x="{X0+6}" y="Y" width="26" height="18" rx="4" transform="translate(0,-12)" fill="#64748b" stroke="#cbd5e1" stroke-width="2"/>',"Conventional vehicle","obeys signals and right-of-way")
leg(f'<path d="M{X0+12} Y l14 14 m0 -14 l-14 14" transform="translate(0,-9)" stroke="#dc2626" stroke-width="3.5" stroke-linecap="round"/>',"Pedestrian (X)","uses the zebra crossings")
leg(f'<g transform="translate(0,-10)"><rect x="{X0+4}" y="Y" width="38" height="14" rx="3" fill="#111827"/><circle cx="{X0+11}" cy="0" r="4" fill="#ef4444" transform="translate(0,Y) translate(0,7)"/><circle cx="{X0+23}" cy="0" r="4" fill="#374151" transform="translate(0,Y) translate(0,7)"/><circle cx="{X0+35}" cy="0" r="4" fill="#374151" transform="translate(0,Y) translate(0,7)"/></g>',"Signal head","state comes from the model, not a UI timer")
leg(f'<g transform="translate(0,-10)"><rect x="{X0+4}" y="Y" width="38" height="16" fill="#3f4b59"/><rect x="{X0+20}" y="Y" width="5" height="16" fill="#fff"/></g>',"Stop line","vehicles must not cross it on red")
leg(f'<path d="M{X0+23} Y l-16 -14 a 22 22 0 0 1 32 0 z" transform="translate(0,6)" fill="#14b8a6" fill-opacity=".35"/>',"Perception range","smart vehicle observes, not the ground truth")
# ODD box
yb=y+6
a(f'<rect x="{X0-4}" y="{yb}" width="400" height="196" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>')
a(f'<text x="{X0+14}" y="{yb+28}" class="tag">ODD ASSUMPTIONS (MILESTONE 1)</text>')
lines=["One lane in / out per arm, right-hand traffic","Straight-through movements only (no turns)","≤ 4 vehicles · 2–6 pedestrians at once","Vehicles 0–8.5 m/s · pedestrians 0.8–1.8 m/s","World frame in metres, origin at the centre,","x east, y north — Python only scales to pixels"]
for i,t in enumerate(lines):
    a(f'<text x="{X0+14}" y="{yb+54+i*21}" class="s">{"• " if i!=5 else "   "}{t}</text>')
a('</svg>')
open('docs/diagrams/intersection-layout.svg','w').write("\n".join(out))
