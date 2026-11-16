"""Visual narratives for the implementation-backed security work in profile.json."""
from svg_primitives import theme, text, start, icon


def label(x, y, value, size, p, color=None, extra=''):
    return text(x, y, value, size, color or p['muted'], 'class="mono" '+extra)


def box(x, y, w, h, p, fill=None, stroke=None, radius=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill or p["card"]}" stroke="{stroke or p["line"]}"/>'


def line(points, p, color=None, extra=''):
    return f'<path d="{points}" fill="none" stroke="{color or p["line"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def arrow(x1, y, x2, p, color=None):
    return line(f'M{x1} {y}H{x2}m-6-5 6 5-6 5', p, color)


def node(x, y, w, title, p, color, size=17, height=48):
    return box(x,y,w,height,p,stroke=color) + text(x+w/2,y+height/2+6,title,size,p['ink'],'text-anchor="middle"')


def header_emblem(p):
    a,v,g = p['amber'],p['violet'],p['green']
    parts = [line('M48 48H126Q153 48 153 75V133H190M48 133H190M48 218H126Q153 218 153 191V133',p,v),
             line('M308 133H346V48H405M346 133H405M346 133V218H405',p,a),
             f'<circle cx="249" cy="133" r="73" fill="{p["wash"]}"/>',
             f'<circle cx="249" cy="133" r="58" fill="{p["bg"]}" stroke="{v}"/>',
             text(249,142,'AI',36,p['ink'],'text-anchor="middle" font-weight="650"'),
             label(249,170,'AGENTS',12,p,v,'text-anchor="middle"')]
    for kind,x,y,color in [('browser',16,17,v),('database',16,102,g),('certificate',16,187,a),('search',414,17,a),('shield',414,102,g),('plug',414,187,v)]:
        parts += [box(x-7,y-7,68,68,p),icon(kind,x+3,y+3,48,color,p)]
    parts += [label(48,276,'CONTEXT',13,p,None,'text-anchor="middle"'),label(249,276,'REASONING',13,p,None,'text-anchor="middle"'),label(441,276,'ACTION',13,p,None,'text-anchor="middle"')]
    return ''.join(parts)


def hero_svg(data, light=False, mobile=False, static=False):
    p=theme(light)
    width,height=(600,610) if mobile else (1100,390)
    parts=start(width,height,data['name']+' / Agentic AI for security',data['bio'],p)
    if not static:
        parts.append('<style>.signal{animation:signal 4s ease-out 1}@keyframes signal{0%{opacity:.2}50%{opacity:1}75%{opacity:.6}100%{opacity:1}}@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>')
    parts.append(label(32,43,data['name'].upper()+' / MIDNIGHT WORKSHOP',16 if mobile else 13,p,p['amber'], 'letter-spacing="1.5"'))
    if mobile:
        parts += [text(32,119,'I build AI',58,p['ink'],'font-weight="650" letter-spacing="-2"'),text(32,181,'for security work.',49,p['ink'],'font-weight="650" letter-spacing="-2"'),
                  text(34,224,'Evidence. Decisions. Operational tools.',21,p['muted']),
                  '<g transform="translate(54 270)" class="signal">'+header_emblem(p)+'</g>',
                  label(32,583,'INVESTIGATE / PROTECT / MANAGE',18,p,p['amber'])]
    else:
        parts += [text(38,136,'I build AI',66,p['ink'],'font-weight="650" letter-spacing="-2"'),text(38,207,'for security work.',56,p['ink'],'font-weight="650" letter-spacing="-2"'),
                  text(40,254,'Evidence. Decisions. Operational tools.',21,p['muted']),
                  '<g transform="translate(588 46) scale(.91)" class="signal">'+header_emblem(p)+'</g>',
                  line('M36 325H1064',p),label(40,358,'SECURITY OPERATIONS',14,p,p['amber']),label(398,358,'DATA PROTECTION',14,p,p['violet']),label(753,358,'CERTIFICATES + CRYPTO',14,p,p['green'])]
    return ''.join(parts)+'</svg>\n'


def security_scene(p):
    a,v,g=p['amber'],p['violet'],p['green']
    parts=[box(145,7,245,44,p),text(268,36,'A security question',21,p['ink'],'text-anchor="middle"'),
           line('M268 51V78',p,a),node(185,80,165,'Intent router',p,a,22,53),
           line('M268 133V155H87V179M268 155V179M268 155H450V179',p,v)]
    for x,kind,title in [(15,'database','LOGS / CASES'),(196,'lock','IAM / APPSEC'),(377,'shield','OT / FIREWALL')]:
        parts.extend([box(x,180,145,76,p),icon(kind,x+53,190,36,v,p),label(x+72,247,title,13,p,None,'text-anchor="middle"')])
    parts += [text(268,294,'Evidence → analysis → playbooks',20,p['ink'],'text-anchor="middle"')]
    return ''.join(parts)


def protection_scene(p):
    a,v,g=p['amber'],p['violet'],p['green']
    parts=[box(8,40,140,172,p),line('M8 71H148',p),label(25,61,'BROWSER',13,p,v),
           box(23,89,109,23,p,fill=p['wash'],radius=4),box(23,125,109,23,p,fill=p['wash'],radius=4),box(23,161,109,23,p,fill=p['wash'],radius=4),
           line('M33 100H96M33 136H78M33 172H108',p,v),arrow(151,126,188,p,v),
           box(194,40,144,172,p),label(210,66,'POLICY PLAN',13,p,a),line('M208 79H324M208 117H324M208 155H324M250 79V194M290 79V194',p),
           label(218,105,'R1',12,p),label(218,143,'R2',12,p),label(218,181,'R3',12,p)]
    for x,y,color in [(263,98,g),(302,98,a),(263,136,a),(302,136,v),(263,174,v),(302,174,g)]:
        parts.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="3" fill="{color}"/>')
    parts += [arrow(342,126,384,p,a),f'<path d="M411 95 442 126 411 157 380 126Z" fill="{p["wash"]}" stroke="{a}"/>',
              icon('team',395,109,32,a,p),label(411,84,'APPROVAL',13,p,a,'text-anchor="middle"'),arrow(446,126,479,p,g),
              icon('shield',481,95,65,g,p),label(513,187,'APPLY',13,p,g,'text-anchor="middle"'),
              text(268,260,'Discover → review → apply → verify',19,p['ink'],'text-anchor="middle"'),
              label(268,290,'POLICY ENFORCEMENT + RUNTIME CHECKS',12,p,None,'text-anchor="middle"')]
    return ''.join(parts)


def crypto_scene(p):
    a,v,g=p['amber'],p['violet'],p['green']
    parts=[label(10,24,'CERTIFICATE LIFECYCLE',14,p,a),icon('certificate',5,49,57,a,p),
           arrow(69,79,102,p,a),node(106,55,110,'Request',p,a),arrow(220,79,242,p,a),node(246,55,110,'Approve',p,a),arrow(360,79,382,p,a),node(386,55,154,'Issue / renew',p,a),
           label(10,168,'CRYPTOGRAPHIC POSTURE',14,p,v),icon('database',5,192,57,v,p),
           arrow(69,222,102,p,v),node(106,198,110,'Inventory',p,v),arrow(220,222,242,p,v),node(246,198,110,'Correlate',p,v),arrow(360,222,382,p,v),node(386,198,154,'PQC assess',p,v),
           label(268,294,'DISCOVERY / APPROVALS / READINESS',13,p,None,'text-anchor="middle"')]
    return ''.join(parts)


def projects_svg(data, light=False, mobile=False):
    p=theme(light)
    width,height=(600,1875) if mobile else (1100,1220)
    parts=start(width,height,'What I build',' '.join(x['summary'] for x in data['projects']),p)
    parts.append(label(32,43,'WHAT I BUILD',16 if mobile else 14,p,p['amber'],'letter-spacing="2"'))
    if not mobile:
        parts.append(label(1068,43,'WORKFLOW ILLUSTRATIONS',12,p,None,'text-anchor="end"'))
    stories=[('SECURITY OPERATIONS',('A question becomes','an investigation.'),'SIEM / SOAR / IAM / APPSEC / OT / FIREWALL',security_scene),
             ('DATA PROTECTION',('Discover the data.','Control the exposure.'),'BROWSER EVIDENCE / REVIEWED POLICIES',protection_scene),
             ('CERTIFICATES + CRYPTO',('Manage the lifecycle.','Understand the risk.'),'LIFECYCLE TOOLS / CRYPTO POSTURE',crypto_scene)]
    for i,(kicker,title,caption,scene) in enumerate(stories):
        y=70+i*(599 if mobile else 380)
        x,w,h=(20,560,579) if mobile else (22,1056,356)
        accent=[p['amber'],p['violet'],p['green']][i]
        parts += [box(x,y,w,h,p,radius=18),f'<rect x="{x}" y="{y+22}" width="3" height="54" rx="1.5" fill="{accent}"/>',
                  label(x+22,y+36,f'0{i+1} / {kicker}',17 if mobile else 13,p,accent)]
        parts.extend([text(x+22,y+91,title[0],35 if mobile else 34,p['ink'],'font-weight="650" letter-spacing="-.6"'),text(x+22,y+133,title[1],35 if mobile else 34,p['ink'],'font-weight="650" letter-spacing="-.6"')])
        if mobile:
            parts.append('<g transform="translate(30 '+str(y+161)+')">'+scene(p)+'</g>')
            parts.append(label(x+22,y+509,caption,15,p,accent))
            parts.append(text(x+22,y+549,' / '.join(data['projects'][i]['technologies']),18,p['muted']))
        else:
            parts.append(label(x+22,y+185,caption,12,p,accent))
            parts.append(text(x+22,y+267,' / '.join(data['projects'][i]['technologies'][:2]),18,p['muted']))
            parts.append(text(x+22,y+296,' / '.join(data['projects'][i]['technologies'][2:]),18,p['muted']))
            parts.append(line(f'M{x+435} {y+25}V{y+h-25}',p))
            parts.append('<g transform="translate(505 '+str(y+25)+')">'+scene(p)+'</g>')
    return ''.join(parts)+'</svg>\n'


def languages_svg(data, rows, light=False, mobile=False):
    p=theme(light);width,height=(600,345) if mobile else (1100,204)
    parts=start(width,height,'Languages in the work','Language byte shares: '+', '.join(f'{n} {s:.1f}%' for n,s,_ in rows),p)
    parts.extend([label(32,43,'CODE MIX',17 if mobile else 14,p,p['amber'],'letter-spacing="2"'),label(width-32,43,f'{data["snapshot"]["repository_count"]} PRIVATE REPOS',14 if mobile else 12,p,None,'text-anchor="end"')])
    x=32
    for _,share,color in rows:
        segment=(width-64)*share/100
        parts.append(f'<rect x="{x:.3f}" y="69" width="{segment:.3f}" height="18" fill="{color}"/>');x+=segment
    for i,(name,share,color) in enumerate(rows):
        x=32+(i%3)*185 if mobile else 32+i*177
        y=127+(i//3)*78 if mobile else 127
        parts += [f'<circle cx="{x+4}" cy="{y-7}" r="4" fill="{color}"/>',text(x+17,y,name,20 if mobile else 17,p['ink']),text(x+17,y+30,f'{share:.1f}%',25 if mobile else 22,p['ink'],'font-weight="600"')]
    parts.append(label(32,height-24,f'BYTE SHARE / {data["snapshot"]["date"]} / NOT A SKILL SCORE',14 if mobile else 12,p))
    return ''.join(parts)+'</svg>\n'


def toolkit_svg(data, light=False, mobile=False):
    p=theme(light);width,height=(600,586) if mobile else (1100,223)
    parts=start(width,height,'The engineering stack',', '.join(data['stack']),p)
    parts.append(label(32,43,'THE ENGINEERING STACK',17 if mobile else 14,p,p['amber'],'letter-spacing="1.5"'))
    groups=[('ORCHESTRATE','agent',['LangGraph','CrewAI']),('RETRIEVE','search',['LangChain','Pinecone']),('CONNECT','plug',['MCP','FastAPI']),('INTERACT','browser',['Playwright','React']),('CONTROL + STORE','shield',['Casbin','Supabase'])]
    for i,(heading,kind,names) in enumerate(groups):
        x,y,w,h=(22+(i%2)*283,70+(i//2)*164,273,146) if mobile else (22+i*216,70,202,130)
        color=[p['violet'],p['amber'],p['green'],p['blue'],p['violet']][i]
        parts += [box(x,y,w,h,p),icon(kind,x+16,y+16,31,color,p),label(x+57,y+35,heading,12 if mobile else 10,p,color),
                  text(x+18,y+83,names[0],27 if mobile else 23,p['ink'],'font-weight="600"'),text(x+18,y+114,names[1],23 if mobile else 20,p['muted'])]
    return ''.join(parts)+'</svg>\n'


def experiments_svg(data, light=False, mobile=False):
    p=theme(light);width,height=(600,359) if mobile else (1100,168)
    parts=start(width,height,'Supporting tools',' '.join(data['notes']),p)
    parts.append(label(32,43,'SUPPORTING TOOLS',17 if mobile else 14,p,p['amber'],'letter-spacing="1.5"'))
    for i,(kind,name) in enumerate([('document','Reports & workbooks'),('search','Regulatory retrieval'),('memory','Agent memory')]):
        x,y,w=(24,68+i*89,552) if mobile else (24+i*360,68,332)
        color=[p['amber'],p['violet'],p['green']][i]
        parts += [box(x,y,w,72,p),icon(kind,x+16,y+14,42,color,p),text(x+78,y+45,name,26 if mobile else 20,p['ink'])]
    return ''.join(parts)+'</svg>\n'
