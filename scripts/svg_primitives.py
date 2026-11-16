"""Shared SVG drawing primitives for the Midnight Workshop profile."""
from html import escape


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
