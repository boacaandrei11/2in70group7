# Run from the repository root: python tools/diagrams/gen_dashboard_concept.py
o=[]
def a(s): o.append(s)
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 800" width="1300" height="800">')
a('''<style>
text{font-family:"Segoe UI",-apple-system,"Helvetica Neue",Arial,sans-serif;fill:#e2e8f0}
.t{font-size:11px;font-weight:700;letter-spacing:.08em;fill:#94a3b8}
.h{font-size:14px;font-weight:700;fill:#f1f5f9}.s{font-size:12.5px;fill:#cbd5e1}.xs{font-size:11.5px;fill:#94a3b8}
.v{font-size:13px;font-weight:700;fill:#f8fafc}.big{font-size:26px;font-weight:700;fill:#f8fafc}
.mono{font-family:Consolas,"Cascadia Mono",Menlo,monospace;font-size:11.5px;fill:#cbd5e1}
</style>''')
a('<rect x="0" y="0" width="1300" height="800" rx="14" fill="#0b1220"/>')
# title bar
a('<rect x="0" y="0" width="1300" height="44" rx="14" fill="#111a2e"/><rect x="0" y="30" width="1300" height="14" fill="#111a2e"/>')
for i,c in enumerate(["#ef4444","#f59e0b","#22c55e"]): a(f'<circle cx="{24+i*20}" cy="22" r="6" fill="{c}"/>')
a('<text x="96" y="27" class="h" style="font-size:13.5px">Smart Intersection — Operator Dashboard</text>')
a('<rect x="1010" y="12" width="270" height="22" rx="11" fill="#1e293b"/><circle cx="1026" cy="23" r="4.5" fill="#22c55e"/><text x="1038" y="27" class="xs" style="fill:#cbd5e1">connected to Rhapsody model · 20 Hz</text>')
def panel(x,w,title,sub):
    a(f'<rect x="{x}" y="58" width="{w}" height="694" rx="12" fill="#111a2e" stroke="#1f2a44"/>')
    a(f'<text x="{x+18}" y="84" class="t">{title}</text><text x="{x+w-18}" y="84" text-anchor="end" class="xs">{sub}</text>')
def card(x,y,w,h): a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#17223a"/>')
def pill(x,y,txt,bg,fg="#0b1220",w=None):
    w=w or 9*len(txt)+16
    a(f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="11" fill="{bg}"/><text x="{x+w/2}" y="{y+15}" text-anchor="middle" style="font-size:11.5px;font-weight:700;fill:{fg}">{txt}</text>'); return w
# ---------- telemetry ----------
X=16; W=330
panel(X,W,"TELEMETRY","explains decisions")
card(X+14,98,W-28,78)
a(f'<text x="{X+30}" y="122" class="xs">simulation time</text><text x="{X+30}" y="156" class="big">00:42.3</text>')
pill(X+176,112,"RUNNING","#22c55e",w=86); a(f'<text x="{X+176}" y="152" class="xs">s02_red_light · seed 42</text>')
card(X+14,186,W-28,112)
a(f'<text x="{X+30}" y="210" class="xs">active phase</text>'); pill(X+30,218,"NS_GREEN","#22c55e",w=96)
a(f'<text x="{X+140}" y="234" class="s">6.2 s to NS_AMBER</text>')
a(f'<rect x="{X+30}" y="252" width="270" height="6" rx="3" fill="#1e293b"/><rect x="{X+30}" y="252" width="160" height="6" rx="3" fill="#22c55e"/>')
a(f'<rect x="{X+30}" y="266" width="270" height="22" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-dasharray="4 3"/><text x="{X+40}" y="281" class="xs" style="fill:#fcd34d">pending: EW green 20 s · from next all-red</text>')
card(X+14,308,W-28,196)
a(f'<text x="{X+30}" y="332" class="xs">selected vehicle</text><rect x="{X+132}" y="320" width="34" height="18" rx="4" fill="#0f766e" stroke="#99f6e4"/><text x="{X+149}" y="333" text-anchor="middle" style="font-size:11px;font-weight:700;fill:#fff">S1</text><text x="{X+174}" y="333" class="xs">smart · northbound</text>')
rows=[("speed","7.9 m/s  (desired 8.0)"),("state","APPROACHING"),("accel","−0.4 m/s²"),("to stop line","24.6 m")]
for i,(k,v) in enumerate(rows):
    a(f'<text x="{X+30}" y="{362+i*22}" class="xs">{k}</text><text x="{X+130}" y="{362+i*22}" class="v" style="font-size:12.5px">{v}</text>')
a(f'<text x="{X+30}" y="460" class="xs">commanded</text>'); pill(X+100,447,"GREEN","#22c55e",w=58)
a(f'<text x="{X+172}" y="460" class="xs">observed</text>'); pill(X+228,447,"GREEN","#22c55e",w=58)
a(f'<text x="{X+30}" y="490" class="xs">detects</text><text x="{X+82}" y="490" class="s">P1 21.4 m · C3 64 m</text>')
card(X+14,514,W-28,68)
for i,(k,v) in enumerate([("queue N/E/S/W","0 / 1 / 1 / 1"),("mean wait","6.8 s"),("stops","3")]):
    a(f'<text x="{X+30+ (0 if i==0 else (150 if i==1 else 236))}" y="538" class="xs">{k}</text><text x="{X+30+(0 if i==0 else (150 if i==1 else 236))}" y="564" class="v">{v}</text>')
card(X+14,592,W-28,146)
a(f'<text x="{X+30}" y="614" class="xs">event log</text>')
ev=[("36.0","SIG","ALL_RED → NS_GREEN","#cbd5e1"),("37.5","PED","P1 requests crossing (E)","#cbd5e1"),("38.9","VEH","C4 stopped at stop line","#cbd5e1"),("41.0","CMD","green_ew=20 accepted·pending","#86efac"),("42.1","CMD","amber=0.5 rejected (min 2 s)","#fca5a5")]
for i,(t,k,m,c) in enumerate(ev):
    a(f'<text x="{X+30}" y="{638+i*20}" class="mono" style="fill:#64748b">{t}</text><text x="{X+70}" y="{638+i*20}" class="mono" style="fill:#93c5fd">{k}</text><text x="{X+104}" y="{638+i*20}" class="mono" style="fill:{c}">{m}</text>')
# ---------- map ----------
MX=358; MW=560
panel(MX,MW,"TOP-DOWN MAP","renders model state only")
mx0=MX+14; my0=98; S=532
a(f'<rect x="{mx0}" y="{my0}" width="{S}" height="{S}" rx="8" fill="#1c2b22"/>')
cx=mx0+S/2; cy=my0+S/2; h=44
a(f'<rect x="{cx-h}" y="{my0}" width="{2*h}" height="{S}" fill="#334155"/><rect x="{mx0}" y="{cy-h}" width="{S}" height="{2*h}" fill="#334155"/>')
a(f'<line x1="{cx}" y1="{my0}" x2="{cx}" y2="{cy-h-34}" stroke="#fbbf24" stroke-width="2" stroke-dasharray="12 9"/><line x1="{cx}" y1="{cy+h+34}" x2="{cx}" y2="{my0+S}" stroke="#fbbf24" stroke-width="2" stroke-dasharray="12 9"/>')
a(f'<line x1="{mx0}" y1="{cy}" x2="{cx-h-34}" y2="{cy}" stroke="#fbbf24" stroke-width="2" stroke-dasharray="12 9"/><line x1="{cx+h+34}" y1="{cy}" x2="{mx0+S}" y2="{cy}" stroke="#fbbf24" stroke-width="2" stroke-dasharray="12 9"/>')
for k in range(6):
    a(f'<rect x="{cx-h+4+k*14}" y="{cy+h+6}" width="7" height="18" fill="#e2e8f0"/><rect x="{cx-h+4+k*14}" y="{cy-h-24}" width="7" height="18" fill="#e2e8f0"/>')
    a(f'<rect x="{cx+h+6}" y="{cy-h+4+k*14}" width="18" height="7" fill="#e2e8f0"/><rect x="{cx-h-24}" y="{cy-h+4+k*14}" width="18" height="7" fill="#e2e8f0"/>')
a(f'<rect x="{cx}" y="{cy+h+30}" width="{h}" height="4" fill="#fff"/><rect x="{cx-h}" y="{cy-h-34}" width="{h}" height="4" fill="#fff"/><rect x="{cx+h+30}" y="{cy-h}" width="4" height="{h}" fill="#fff"/><rect x="{cx-h-34}" y="{cy}" width="4" height="{h}" fill="#fff"/>')
def lamp(x,y,c): a(f'<rect x="{x}" y="{y}" width="14" height="14" rx="4" fill="#0b1220"/><circle cx="{x+7}" cy="{y+7}" r="4.5" fill="{c}"/>')
lamp(cx+h+4,cy+h+32,"#22c55e"); lamp(cx-h-18,cy-h-46,"#22c55e"); lamp(cx+h+32,cy-h-18,"#ef4444"); lamp(cx-h-46,cy+h+4,"#ef4444")
def car(x,y,w,hh,fill,lab,sel=False):
    if sel: a(f'<rect x="{x-5}" y="{y-5}" width="{w+10}" height="{hh+10}" rx="7" fill="none" stroke="#5eead4" stroke-width="2" stroke-dasharray="4 3"/>')
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="4" fill="{fill}" stroke="#e2e8f0" stroke-width="1.2"/><text x="{x+w/2}" y="{y+hh/2+4}" text-anchor="middle" style="font-size:10.5px;font-weight:700;fill:#fff">{lab}</text>')
car(cx+11,cy+h+60,22,36,"#0f766e","S1",True)
a(f'<rect x="{cx+46}" y="{cy+h+64}" width="96" height="40" rx="6" fill="#0b1220" opacity=".9"/><text x="{cx+54}" y="{cy+h+80}" class="xs" style="fill:#5eead4;font-weight:700">S1 · 7.9 m/s</text><text x="{cx+54}" y="{cy+h+96}" class="xs">APPROACHING</text>')
car(cx+11,cy+h+120,22,36,"#64748b","C2")
car(cx-33,my0+40,22,36,"#64748b","C3")
car(cx+h+40,cy-33,36,22,"#64748b","C4")
car(cx-h-76,cy+11,36,22,"#64748b","C5")
def X(x,y): a(f'<path d="M{x-6} {y-6} L{x+6} {y+6} M{x+6} {y-6} L{x-6} {y+6}" stroke="#f87171" stroke-width="3" stroke-linecap="round"/>')
X(cx+h+15,cy-22); X(cx-h-14,cy+h+16)

a(f'<text x="{mx0+14}" y="{my0+S-14}" class="xs">N ↑ · world metres scaled to pixels · positions from model snapshot #4231</text>')
# overlay toggles
yy=my0+S+14
for i,t in enumerate(["IDs","speeds","states","perception range","warnings"]):
    on = i<3 or i==4
    w=12+7.2*len(t)+20
    xx=mx0+sum(12+7.2*len(u)+20+8 for u in ["IDs","speeds","states","perception range","warnings"][:i])
    a(f'<rect x="{xx}" y="{yy}" width="{w}" height="24" rx="12" fill="{"#1e3a5f" if on else "#17223a"}" stroke="{"#3b82f6" if on else "#334155"}"/><text x="{xx+w/2}" y="{yy+16}" text-anchor="middle" class="xs" style="fill:{"#bfdbfe" if on else "#64748b"}">{t}</text>')
a(f'<text x="{mx0}" y="{yy+52}" class="xs">click an agent to select it in Telemetry · editing happens only in Configuration</text>')
# ---------- config ----------
CX=932; CW=352
panel(CX,CW,"CONFIGURATION","requests → validated by model")
card(CX+14,98,CW-28,268)
a(f'<text x="{CX+30}" y="122" class="xs">signal timing plan</text>')
sl=[("Green N/S",15,5,60,"s"),("Green E/W",20,5,60,"s"),("Amber",3,2,5,"s"),("All-red",2,1,3,"s"),("Pedestrian walk",10,5,30,"s")]
for i,(n,v,lo,hi,u) in enumerate(sl):
    y=148+i*40
    a(f'<text x="{CX+30}" y="{y}" class="s">{n}</text><text x="{CX+CW-30}" y="{y}" text-anchor="end" class="v">{v} {u}</text>')
    f=(v-lo)/(hi-lo); tw=CW-60
    a(f'<rect x="{CX+30}" y="{y+10}" width="{tw}" height="5" rx="2.5" fill="#1e293b"/><rect x="{CX+30}" y="{y+10}" width="{tw*f:.0f}" height="5" rx="2.5" fill="#3b82f6"/><circle cx="{CX+30+tw*f:.0f}" cy="{y+12.5}" r="7" fill="#e2e8f0"/>')
    a(f'<text x="{CX+150}" y="{y}" class="xs" style="font-size:10.5px">{lo}–{hi} {u}</text>')
a(f'<rect x="{CX+30}" y="{336}" width="130" height="24" rx="6" fill="#2563eb"/><text x="{CX+95}" y="{352}" text-anchor="middle" style="font-size:12px;font-weight:700;fill:#fff">Request plan</text>')
a(f'<text x="{CX+172}" y="{352}" class="xs" style="fill:#86efac">✓ accepted · pending</text>')
card(CX+14,376,CW-28,150)
a(f'<text x="{CX+30}" y="400" class="xs">traffic demand</text>')
for i,(n,v) in enumerate([("Vehicles","4"),("of which smart","1"),("S1 initial speed","8.0 m/s"),("Pedestrians","3")]):
    y=428+i*26
    a(f'<text x="{CX+30}" y="{y}" class="s">{n}</text><rect x="{CX+CW-140}" y="{y-15}" width="110" height="22" rx="6" fill="#0b1220" stroke="#334155"/><text x="{CX+CW-40}" y="{y}" text-anchor="end" class="v" style="font-size:12.5px">{v}</text><text x="{CX+CW-132}" y="{y}" class="xs">−  +</text>')
card(CX+14,536,CW-28,86)
a(f'<text x="{CX+30}" y="560" class="xs">scenario</text><rect x="{CX+30}" y="570" width="200" height="28" rx="6" fill="#0b1220" stroke="#334155"/><text x="{CX+42}" y="589" class="s">s02_red_light</text><text x="{CX+214}" y="589" class="xs">▾</text>')
a(f'<text x="{CX+246}" y="560" class="xs">seed</text><rect x="{CX+246}" y="570" width="76" height="28" rx="6" fill="#0b1220" stroke="#334155"/><text x="{CX+258}" y="589" class="s">42</text>')
card(CX+14,632,CW-28,106)
a(f'<text x="{CX+30}" y="656" class="xs">run control</text>')
for i,(t,c) in enumerate([("Start","#16a34a"),("Pause","#334155"),("Step","#334155"),("Reset","#7f1d1d")]):
    a(f'<rect x="{CX+30+i*76}" y="668" width="68" height="30" rx="7" fill="{c}"/><text x="{CX+64+i*76}" y="688" text-anchor="middle" style="font-size:12.5px;font-weight:700;fill:#fff">{t}</text>')
a(f'<text x="{CX+30}" y="722" class="xs">unsafe or out-of-range requests are rejected with a reason</text>')
a('<text x="650" y="783" text-anchor="middle" class="xs">Concept wireframe — values are illustrative; not implemented yet. Every control is a request that the Rhapsody model validates.</text>')
a('</svg>')
open('docs/diagrams/dashboard-concept.svg','w').write("\n".join(o))
