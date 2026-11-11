#!/usr/bin/env python3
"""Generate the hand-designed, theme-aware SVG artwork for the profile.

No external dependencies: python scripts/build_art.py
"""
from pathlib import Path
import math, random

OUT=Path(__file__).resolve().parents[1]/'assets'
OUT.mkdir(exist_ok=True)

def shape_nodes(c):
    rng=random.Random(81)
    ss=[]
    for i in range(17):
        x=685+i*30
        y=42+(i%5)*52
        if x>1172: break
        col=c['cyan'] if i%3 else c['mint']
        ss.append(f'<path d="M{x} {y}h{15+i%4*7}v{12+(i%3)*7}" stroke="{col}" stroke-width="1.1" opacity=".30" fill="none"/>')
        ss.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{col}" opacity=".75"/>')
    return '\n'.join(ss)

def banner(theme):
    dark=theme=='dark'
    c={
    'bg':'#0A1220' if dark else '#F4F9FF','bg2':'#152437' if dark else '#E3F1FB',
    'border':'#2D4560' if dark else '#B9D5E6','text':'#ECF7FF' if dark else '#183146',
    'sub':'#A3B7CC' if dark else '#4E7188','dim':'#637C97' if dark else '#7A98AA',
    'cyan':'#73DCEE' if dark else '#087D9D','blue':'#83B6FF' if dark else '#2162B1',
    'mint':'#83E7BA' if dark else '#1E9274','violet':'#C5B4FF' if dark else '#7251C3',
    'chip':'#102234' if dark else '#FFFFFF','chipedge':'#365771' if dark else '#9DC4D9',
    'grid':'#5D8AA4' if dark else '#B1CCD9',
    }
    lines=[]
    for x in range(28,1200,32): lines.append(f'<path d="M{x} 0V364"/>')
    for y in range(20,364,32): lines.append(f'<path d="M0 {y}H1198"/>')
    grid=''.join(lines)
    # Branching PCB traces are intentionally reproducible across themes
    wires=[]
    for i in range(9):
        startx=775+(i%3)*22; sy=48+i*35
        endx=1150; dy=sy+(-10 if i%2 else 16)
        color=[c['cyan'],c['mint'],c['violet']][i%3]
        wires.append(f'<path d="M{startx} {sy}h{65+i%4*12}l{24} {dy-sy}H{endx}" stroke="{color}" stroke-width="{1.4 if i%3 else 1.7}" fill="none" opacity=".38" stroke-linejoin="round"/>')
        wires.append(f'<circle cx="{endx}" cy="{dy}" r="3" fill="{color}" opacity=".68"/>')
    pins=[]
    for i in range(9):
        yy=105+i*18
        pins.append(f'<path d="M865 {yy}h-16 M1068 {yy}h16" stroke="{c["mint"] if i%2 else c["cyan"]}" stroke-width="3" stroke-linecap="round" opacity=".65"/>')
    for i in range(9):
        xx=890+i*19
        pins.append(f'<path d="M{xx} 84v-15 M{xx} 266v15" stroke="{c["mint"] if i%2 else c["cyan"]}" stroke-width="3" stroke-linecap="round" opacity=".65"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="365" viewBox="0 0 1200 365" role="img" aria-labelledby="title description">
<title id="title">Hassan — The Systems Lab</title>
<desc id="description">An original circuit-board themed header: Hassan, building applications and exploring the systems beneath them.</desc>
<defs>
  <linearGradient id="bg" x2="1" y2="1"><stop stop-color="{c['bg']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
  <linearGradient id="signal" x2="1" y2="0"><stop stop-color="{c['cyan']}"/><stop offset=".58" stop-color="{c['blue']}"/><stop offset="1" stop-color="{c['violet']}"/></linearGradient>
  <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" fill="{c['grid']}" opacity=".14"/></pattern>
  <clipPath id="clip"><rect width="1200" height="365" rx="16"/></clipPath>
</defs>
<style>
 @keyframes glow {{0%,100%{{opacity:.32}} 50%{{opacity:.8}}}}
 @keyframes trace {{to{{stroke-dashoffset:-50}}}}
 .pulse {{animation:glow 3.8s ease-in-out infinite}}
 .active {{stroke-dasharray:5 15; animation:trace 4.5s linear infinite}}
 @media(prefers-reduced-motion:reduce){{.pulse,.active{{animation:none}}}}
</style>
<g clip-path="url(#clip)">
<rect width="1200" height="365" fill="url(#bg)"/>
<rect width="1200" height="365" fill="url(#dots)"/>
<g stroke="{c['grid']}" stroke-width=".5" opacity=".07">{grid}</g>
<path d="M0 334H1199" stroke="{c['border']}"/>
<rect x="1" y="1" width="1198" height="363" rx="15" fill="none" stroke="{c['border']}" stroke-width="1.5"/>
<!-- identification / nameplate -->
<circle cx="49" cy="51" r="6" fill="{c['mint']}" class="pulse"/>
<text x="67" y="56" fill="{c['mint']}" font-size="14" font-family="Consolas,monospace" letter-spacing="2.2">PERSONAL ENGINEERING NOTEBOOK</text>
<text x="46" y="158" fill="{c['text']}" font-size="94" font-weight="750" font-family="Segoe UI,Arial,sans-serif" letter-spacing="-5">Hassan<tspan fill="{c['cyan']}">.</tspan></text>
<rect x="49" y="184" width="82" height="4" rx="2" fill="{c['cyan']}"/>
<rect x="139" y="184" width="30" height="4" rx="2" fill="{c['mint']}"/>
<rect x="175" y="184" width="14" height="4" rx="2" fill="{c['violet']}"/>
<text x="49" y="230" fill="{c['sub']}" font-family="Segoe UI,Arial,sans-serif" font-size="22">Building applications. Studying systems.</text>
<text x="49" y="260" fill="{c['sub']}" font-family="Segoe UI,Arial,sans-serif" font-size="22">Looking beneath the abstractions.</text>
<text x="48" y="311" fill="{c['dim']}" font-family="Consolas,monospace" font-size="13" letter-spacing="1.2">SOFTWARE / SYSTEMS / THE SPACE BETWEEN</text>
<!-- circuit cluster -->
{''.join(wires)}
{shape_nodes(c)}
<rect x="863" y="83" width="207" height="185" rx="17" fill="{c['chip']}" stroke="{c['chipedge']}" stroke-width="2"/>
{''.join(pins)}
<rect x="881" y="103" width="170" height="147" rx="9" fill="none" stroke="{c['mint']}" stroke-width="1" opacity=".4"/>
<path d="M908 131h112M908 216h112" stroke="{c['chipedge']}" opacity=".6"/>
<text x="965" y="165" fill="{c['text']}" text-anchor="middle" font-family="Consolas,monospace" font-size="33" font-weight="bold">H/S</text>
<text x="965" y="190" fill="{c['mint']}" text-anchor="middle" font-family="Consolas,monospace" font-size="13" letter-spacing="2">SYSTEMS LAB</text>
<text x="965" y="235" fill="{c['dim']}" text-anchor="middle" font-family="Consolas,monospace" font-size="12">v1.0 / curious</text>
<path d="M840 304H1138" stroke="url(#signal)" stroke-width="2" stroke-dasharray="5 15" class="active"/>
<text x="854" y="326" fill="{c['dim']}" font-family="Consolas,monospace" font-size="11">SIG 0x01</text>
<text x="1117" y="326" fill="{c['dim']}" font-family="Consolas,monospace" font-size="11" text-anchor="end">READY</text>
</g></svg>'''

def explorer(theme):
    dark=theme=='dark'
    p={
    'bg':'#0A1220' if dark else '#F4F9FF','surface':'#132438' if dark else '#FFFFFF',
    'border':'#30435A' if dark else '#C1D8EA','text':'#F0F8FF' if dark else '#1C364C',
    'muted':'#8EA5BE' if dark else '#57738D','dim':'#66849D' if dark else '#7D98AD',
    'cyan':'#73DCEE' if dark else '#0987A3','blue':'#83B6FF' if dark else '#2369B4',
    'mint':'#83E7BA' if dark else '#228F72','violet':'#C5B4FF' if dark else '#7956C4',
    'amber':'#F4CB89' if dark else '#B57B25','grid':'#42627A' if dark else '#C2D6E8',
    }
    layers=[
    ('01','INTERFACE','React · TypeScript','Memory Sequence',p['cyan'],'<rect x="0" y="0" width="35" height="23" rx="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M0 6H35M8 15h19" stroke="currentColor" stroke-width="1.6"/>'),
    ('02','APPLICATION / NETWORK','REST · HTTP · Express','Phonebook API',p['blue'],'<rect width="35" height="23" rx="4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M7 11h21M22 5l6 6-6 6" stroke="currentColor" fill="none" stroke-width="1.6"/>'),
    ('03','OPERATING SYSTEM','Linux · syscalls · I/O','x86-64 Web Server',p['mint'],'<path d="M0 2h35v22H0zM5 9l6 4-6 4M14 18h10" fill="none" stroke="currentColor" stroke-width="1.6"/>'),
    ('04','MACHINE INSTRUCTIONS','Assembly · RISC-V · x86-64','RISC-V Neural Network',p['violet'],'<path d="M1 4h33v20H1zM10 10h17M10 15h12M10 20h8" fill="none" stroke="currentColor" stroke-width="1.6"/>'),
    ('05','DIGITAL LOGIC','ALU · registers · pipelines','RISC-V CPU',p['amber'],'<rect x="7" y="3" width="21" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M2 7h5M2 13h5M2 19h5M28 7h5M28 13h5M28 19h5M12 8h11v10H12z" fill="none" stroke="currentColor" stroke-width="1.5"/>'),
    ]
    rows=[]
    for i,(num,title,tech,project,color,ico) in enumerate(layers):
        y=108+i*104
        rows.append(f'''<g>
<rect x="72" y="{y}" width="1056" height="84" rx="12" fill="{p['surface']}" stroke="{p['border']}" stroke-width="1"/>
<path d="M84 {y+16}v52" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
<circle cx="52" cy="{y+42}" r="14" fill="{p['bg']}" stroke="{color}" stroke-width="2"/>
<text x="52" y="{y+46}" text-anchor="middle" font-size="11" font-family="Consolas,monospace" fill="{color}">{num}</text>
<g transform="translate(113,{y+31})" style="color:{color}">{ico}</g>
<text x="170" y="{y+36}" fill="{p['text']}" font-size="20" font-weight="700" letter-spacing=".7" font-family="Segoe UI,Arial,sans-serif">{title}</text>
<text x="170" y="{y+62}" fill="{p['muted']}" font-size="17" font-family="Segoe UI,Arial,sans-serif">{tech}</text>
<text x="1090" y="{y+33}" text-anchor="end" fill="{p['dim']}" font-size="13" font-family="Consolas,monospace">EXPLORE PROJECT</text>
<text x="1090" y="{y+61}" text-anchor="end" fill="{color}" font-size="18" font-family="Segoe UI,Arial,sans-serif" font-weight="650">{project}</text>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="655" viewBox="0 0 1200 655" role="img" aria-labelledby="title desc">
<title id="title">Beneath the abstractions: five layers of computing</title>
<desc id="desc">An illustration of the layers Hassan explores, from React interfaces and HTTP through operating systems, assembly languages and CPU logic, with associated projects. A conceptual learning map, not a deployed system architecture.</desc>
<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" fill="{p['grid']}" opacity=".22"/></pattern></defs>
<style>@keyframes drift{{0%{{stroke-dashoffset:0}}100%{{stroke-dashoffset:-32}}}} .flow{{animation:drift 2.3s linear infinite}} @media(prefers-reduced-motion:reduce){{.flow{{animation:none}}}}</style>
<rect x="1" y="1" width="1198" height="653" rx="17" fill="{p['bg']}" stroke="{p['border']}" stroke-width="1.5"/>
<rect x="2" y="2" width="1196" height="650" rx="17" fill="url(#grid)"/>
<text x="72" y="48" fill="{p['text']}" font-size="29" font-family="Segoe UI,Arial,sans-serif" font-weight="750">Beneath the abstractions</text>
<text x="73" y="75" fill="{p['muted']}" font-size="15" font-family="Consolas,monospace">FIVE LAYERS / FIVE WAYS TO LEARN BY BUILDING</text>
<path d="M52 99V{108+4*104+84}" stroke="{p['grid']}" stroke-width="3"/>
<path d="M52 99V{108+4*104+84}" stroke="{p['cyan']}" stroke-width="3" stroke-dasharray="4 12" opacity=".7" class="flow"/>
{''.join(rows)}
<text x="75" y="632" fill="{p['dim']}" font-size="13" font-family="Consolas,monospace">CONCEPTUAL MAP — individual projects, not one deployed software stack</text>
<text x="1125" y="632" text-anchor="end" fill="{p['dim']}" font-size="13" font-family="Consolas,monospace">READ THE CODE BELOW ↓</text>
</svg>'''

if __name__=='__main__':
    for th in ('dark','light'):
        (OUT/f'hero.{th}.svg').write_text(banner(th),encoding='utf-8')
        (OUT/f'architecture.{th}.svg').write_text(explorer(th),encoding='utf-8')
    print('Generated four SVG assets')
