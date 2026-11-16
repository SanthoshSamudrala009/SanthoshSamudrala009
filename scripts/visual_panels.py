"""Original SVG panels for the Midnight Workshop profile."""
from html import escape
import math


def theme(light):
    return ({'bg': '#f7f3ed', 'card': '#fffdf9', 'ink': '#302b38', 'muted': '#736579',
             'line': '#d8cbdc', 'amber': '#9b612a', 'violet': '#79609f', 'green': '#5e7e54',
             'wash': '#e8dfed', 'blue': '#537f96'} if light else
            {'bg': '#15171d', 'card': '#1e1e29', 'ink': '#f6ecdf', 'muted': '#b3a7bf',
             'line': '#3b3349', 'amber': '#f2bb79', 'violet': '#b5a0e1', 'green': '#abc998',
             'wash': '#2b2538', 'blue': '#92bdcf'})


def text(x, y, value, size=18, color='currentColor', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'


def start(width, height, title, description, p):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
            '<style>text{font-family:Segoe UI,Arial,sans-serif}.mono{font-family:Consolas,monospace}.outline{fill:none;stroke-linecap:round;stroke-linejoin:round}</style>',
            f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="22" fill="{p["bg"]}" stroke="{p["line"]}"/>']


def section(parts, title, subtitle, width, p, mobile):
    parts.append(text(32, 45, title, 15 if not mobile else 18, p['amber'], 'class="mono" letter-spacing="2"'))
    if subtitle:
        parts.append(text(width-32, 45, subtitle, 12 if not mobile else 15, p['muted'], 'text-anchor="end" class="mono"'))


def icon(kind, x, y, size, color, p):
    """Functional pictograms drawn in a 64-unit box, rather than external logo assets."""
    shapes = {
        'shield': '<path d="M32 5 54 14V31C54 44 42 53 32 59 22 53 10 44 10 31V14Z"/><path d="m22 31 7 8 15-17"/>',
        'certificate': '<rect x="12" y="5" width="39" height="50" rx="4"/><path d="M21 17H42M21 25H40M21 33H32"/><circle cx="40" cy="43" r="8"/><path d="m35 50-2 10 7-4 7 4-2-10"/>',
        'agent': '<rect x="9" y="17" width="46" height="34" rx="11"/><path d="M32 17V8M4 29v10M60 29v10M22 51v7M42 51v7"/><circle cx="32" cy="5" r="3"/><circle cx="23" cy="32" r="3"/><circle cx="41" cy="32" r="3"/><path d="M24 42H40"/>',
        'browser': '<rect x="5" y="9" width="54" height="44" rx="5"/><path d="M5 22H59M13 15h1M20 15h1M27 15h1M13 31h22M13 39h13"/><path d="m40 33 14 9-7 2-3 7Z"/>',
        'database': '<ellipse cx="32" cy="13" rx="22" ry="8"/><path d="M10 13V49C10 60 54 60 54 49V13M10 30c0 11 44 11 44 0M10 46c0 11 44 11 44 0"/>',
        'plug': '<path d="M20 7V23M44 7V23M12 23H52V29C52 40 43 46 32 46V57M20 57H32"/><path d="M23 30h18M32 46v-9"/>',
        'document': '<path d="M13 4H39L52 17V59H13Z M39 4V18H52M22 29H43M22 38H43M22 47H35"/>',
        'sheet': '<path d="M13 4H39L52 17V59H13Z M39 4V18H52M20 28H45V50H20Z M20 36H45M20 43H45M29 28V50M37 28V50"/>',
        'cloud': '<path d="M16 47C-1 47 0 25 16 25 16 7 44 7 47 25 66 24 66 47 49 47H42M32 58V29m-9 10 9-10 9 10"/>',
        'bolt': '<path d="M36 4 10 36H29L25 60 54 25H35Z"/>',
        'atom': '<ellipse cx="32" cy="32" rx="28" ry="11"/><ellipse cx="32" cy="32" rx="28" ry="11" transform="rotate(60 32 32)"/><ellipse cx="32" cy="32" rx="28" ry="11" transform="rotate(120 32 32)"/><circle cx="32" cy="32" r="4"/>',
        'chain': '<path d="m28 42-6 6a12 12 0 0 1-17-17l14-14a12 12 0 0 1 17 0M36 22l6-6a12 12 0 0 1 17 17L45 47a12 12 0 0 1-17 0M21 43l22-22"/>',
        'team': '<circle cx="32" cy="17" r="9"/><circle cx="12" cy="27" r="7"/><circle cx="52" cy="27" r="7"/><path d="M18 55V45c0-17 28-17 28 0V55M2 52V44c0-9 8-13 15-9M62 52V44c0-9-8-13-15-9"/>',
        'tree': '<path d="M32 5 12 25H22L7 43H26V59H38V43H57L42 25H52Z"/>',
        'memory': '<rect x="15" y="15" width="34" height="34" rx="5"/><path d="M23 4V15M32 4V15M41 4V15M23 49V60M32 49V60M41 49V60M4 23H15M4 32H15M4 41H15M49 23H60M49 32H60M49 41H60"/><path d="M24 39V25l8 9 8-9V39"/>',
        'search': '<circle cx="27" cy="27" r="19"/><path d="m41 41 18 18M18 22H36M18 30H30"/>',
        'filter': '<path d="M6 10H58L39 32V51L25 58V32Z"/><path d="m24 19 6 6 12-12"/>',
        'lock': '<rect x="13" y="27" width="38" height="30" rx="5"/><path d="M21 27V17a11 11 0 0 1 22 0v10M32 38v9"/>',
    }
    return f'<g transform="translate({x} {y}) scale({size/64})" class="outline" stroke="{color}" stroke-width="2.7">{shapes[kind]}</g>'


def project_scene(index, x, y, scale, p):
    # A quiet illustration, with no claim of a live system or measured status.
    a, v, g = p['amber'], p['violet'], p['green']
    parts = [f'<g transform="translate({x} {y}) scale({scale})">',
             f'<ellipse cx="145" cy="172" rx="125" ry="20" fill="{p["wash"]}"/>']
    if index == 0:
        parts.extend([f'<path d="M60 100H231" fill="none" stroke="{p["line"]}" stroke-width="2" stroke-dasharray="4 7"/>',
                      icon('certificate', 15, 55, 87, v, p),
                      f'<circle cx="156" cy="107" r="53" fill="{p["bg"]}" stroke="{p["line"]}"/>',
                      icon('shield', 121, 70, 70, a, p),
                      '<g transform="translate(238 95)">',
                      f'<circle r="29" fill="{p["bg"]}" stroke="{p["line"]}"/><path d="M-17 1a17 17 0 0 1 29-13m0-9v11h-11M17-1A17 17 0 0 1-12 12m0 9V10h11" stroke="{g}" stroke-width="2.5" fill="none"/>', '</g>'])
    elif index == 1:
        parts.extend([f'<path d="M47 48 145 109 245 48M145 109 47 164M145 109 245 164" fill="none" stroke="{p["line"]}" stroke-width="2"/>'])
        for kind, sx, sy, color in [('browser', 18, 16, v), ('search', 217, 16, a), ('database', 24, 132, g), ('shield', 222, 132, v)]:
            parts.append(icon(kind, sx, sy, 44, color, p))
        parts.extend([f'<circle cx="145" cy="105" r="52" fill="{p["bg"]}" stroke="{v}" stroke-opacity=".5"/>', icon('agent', 108, 68, 74, v, p)])
    else:
        parts.extend([f'<path d="M61 102H140L235 53M140 102 235 153" fill="none" stroke="{p["line"]}" stroke-width="2"/>',
                      icon('plug', 18, 62, 77, g, p),
                      f'<circle cx="140" cy="102" r="6" fill="{g}"/>',
                      icon('document', 209, 15, 65, a, p), icon('sheet', 209, 120, 65, v, p)])
    return ''.join(parts) + '</g>'


def projects_svg(data, light=False, mobile=False):
    p = theme(light)
    width, height = (600, 1240) if mobile else (1100, 488)
    descriptions = ' '.join(project['title'] + '. ' + project['summary'] for project in data['projects'])
    parts = start(width, height, 'The workbench', descriptions, p)
    section(parts, 'THE WORKBENCH', 'PRIVATE BUILDS', width, p, mobile)
    titles = [('Certificates', '& crypto agility'), ('Security', '& data agents'), ('MCP tools', '& useful outputs')]
    accents = [p['amber'], p['violet'], p['green']]
    for index, project in enumerate(data['projects']):
        x, y, w, h = (24, 72 + index*386, 552, 366) if mobile else (24+index*358, 72, 336, 392)
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="17" fill="{p["card"]}" stroke="{p["line"]}"/>')
        parts.append(text(x+22, y+34, f'{index+1:02d} / {project["label"].upper()}', 16 if mobile else 12, accents[index], 'class="mono" letter-spacing="1"'))
        if mobile:
            parts.extend([text(x+24, y+86, titles[index][0], 31, p['ink'], 'font-weight="650"'), text(x+24, y+124, titles[index][1], 31, p['ink'], 'font-weight="650"'), project_scene(index, x+252, y+123, .95, p)])
            for j, tech in enumerate(project['technologies']):
                parts.append(text(x+24, y+180+j*30, tech, 19, p['muted'], 'class="mono"'))
        else:
            parts.extend([project_scene(index, x+23, y+48, 1, p), text(x+22, y+280, titles[index][0], 27, p['ink'], 'font-weight="650"'), text(x+22, y+313, titles[index][1], 27, p['ink'], 'font-weight="650"')])
            parts.append(text(x+22, y+348, ' / '.join(project['technologies'][:2]), 13, p['muted'], 'class="mono"'))
            parts.append(text(x+22, y+370, ' / '.join(project['technologies'][2:]), 13, p['muted'], 'class="mono"'))
    return ''.join(parts) + '</svg>\n'


def languages_svg(data, rows, light=False, mobile=False):
    p = theme(light)
    width, height = (600, 790) if mobile else (1100, 330)
    desc = ', '.join(f'{name} {share:.1f}%' for name, share, _ in rows) + '. Shares of detected language bytes, not proficiency or time spent.'
    parts = start(width, height, 'The code palette', desc, p)
    section(parts, 'THE CODE PALETTE', f'{data["snapshot"]["repository_count"]} REPOS', width, p, mobile)
    for index, (name, share, color) in enumerate(rows):
        cx = 159+(index%2)*282 if mobile else 102+index*179
        cy = 150+(index//2)*216 if mobile else 157
        radius = 60 if mobile else 58
        circumference = 2*math.pi*radius
        parts.extend([f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{p["wash"]}" stroke-width="12"/>',
                      f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-width="12" stroke-dasharray="{circumference*share/100:.3f} {circumference:.3f}" transform="rotate(-90 {cx} {cy})"/>',
                      text(cx, cy+9, f'{share:.1f}%', 30 if mobile else 27, p['ink'], 'text-anchor="middle" font-weight="600"'),
                      text(cx, cy+98, name, 25 if mobile else 20, p['ink'], 'text-anchor="middle"')])
    parts.append(text(32, height-42, f'BYTE SHARE / {data["snapshot"]["date"]}', 16 if mobile else 13, p['muted'], 'class="mono"'))
    parts.append(text(32, height-18, 'Selected private repositories. Not a skill score.', 16 if mobile else 13, p['muted']))
    return ''.join(parts) + '</svg>\n'


def toolkit_svg(data, light=False, mobile=False):
    p = theme(light)
    width, height = (600, 804) if mobile else (1100, 384)
    parts = start(width, height, 'The tool wall', ', '.join(data['stack']), p)
    section(parts, 'THE TOOL WALL', '', width, p, mobile)
    mapping = {'FastAPI': ('bolt','APIs'), 'React': ('atom','INTERFACES'), 'Playwright': ('browser','AUTOMATION'),
               'MCP': ('plug','CONNECTIONS'), 'LangChain': ('chain','RETRIEVAL'), 'CrewAI': ('team','AGENTS'),
               'Pinecone': ('tree','VECTORS'), 'Supabase': ('database','STORAGE')}
    for index, name in enumerate(data['stack']):
        kind, role = mapping.get(name, ('plug', 'TOOL'))
        x, y, w, h = (24+(index%2)*282, 72+(index//2)*177, 270, 161) if mobile else (24+(index%4)*269, 72+(index//4)*148, 245, 128)
        color = [p['amber'],p['violet'],p['blue'],p['green']][index%4]
        parts.extend([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{p["card"]}" stroke="{p["line"]}"/>'])
        if mobile:
            parts.extend([icon(kind,x+19,y+18,52,color,p),text(x+20,y+105,name,29,p['ink'],'font-weight="600"'),text(x+20,y+135,role,15,p['muted'],'class="mono" letter-spacing="1"')])
        else:
            parts.extend([icon(kind,x+18,y+22,53,color,p),text(x+87,y+52,name,23,p['ink'],'font-weight="600"'),text(x+87,y+79,role,11,p['muted'],'class="mono" letter-spacing="1"')])
    return ''.join(parts) + '</svg>\n'


def experiments_svg(data, light=False, mobile=False):
    p = theme(light)
    width, height = (600, 384) if mobile else (1100, 213)
    parts = start(width, height, 'On the side bench', ' '.join(data['notes']), p)
    section(parts, 'THE SIDE BENCH', '', width, p, mobile)
    for index, (kind, title) in enumerate([('memory','Agent memory'), ('search','Evidence retrieval'), ('filter','LLM guardrails')]):
        x, y = (32, 80+index*96) if mobile else (32+index*360, 83)
        color = [p['violet'],p['amber'],p['green']][index]
        parts.extend([f'<rect x="{x}" y="{y}" width="{536 if mobile else 316}" height="{78 if mobile else 101}" rx="14" fill="{p["card"]}" stroke="{p["line"]}"/>',
                      icon(kind,x+17,y+17,44 if mobile else 48,color,p),
                      text(x+83,y+48 if mobile else y+58,title,25 if mobile else 21,p['ink'])])
    return ''.join(parts) + '</svg>\n'
