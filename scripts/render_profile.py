"""Render a curated public snapshot; no network access or credentials required."""
from __future__ import annotations
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COLORS = {'Python': '#efbd72', 'TypeScript': '#ad9adb', 'JavaScript': '#a9c690',
          'CSS': '#d490a9', 'HTML': '#90b9ca', 'PowerShell': '#8dadd6',
          'C#': '#a8c7ba', 'SCSS': '#c99ab9', 'Other': '#84909b'}


def plain(value, label, maximum=500):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f'Invalid {label}.')
    if any(ord(c) < 32 for c in value) or any(c in value for c in '<>[]`\\'):
        raise ValueError(f'Unsafe formatting in {label}.')
    if re.search(r'https?://|www\.|@', value, re.I):
        raise ValueError(f'Links and contact addresses are not allowed in {label}.')
    return value


def exact_keys(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(f'Unexpected or missing fields in {label}.')


def text_list(values, label, limit, maximum=50):
    if not isinstance(values, list) or not 1 <= len(values) <= limit:
        raise ValueError(f'Invalid {label} list.')
    for item in values:
        plain(item, label, maximum)


def validate(data):
    exact_keys(data, ('schema_version', 'name', 'handle', 'headline', 'bio',
                     'projects', 'notes', 'stack', 'snapshot'), 'profile')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('Unsupported schema version.')
    plain(data['name'], 'name', 30)
    handle = data['handle']
    if not isinstance(handle, str) or not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', handle):
        raise ValueError('Invalid GitHub handle.')
    plain(data['headline'], 'headline', 100)
    plain(data['bio'], 'biography', 500)
    if not isinstance(data['projects'], list) or len(data['projects']) != 3:
        raise ValueError('Exactly three curated project summaries are required.')
    for project in data['projects']:
        exact_keys(project, ('label', 'title', 'summary', 'technologies'), 'project')
        plain(project['label'], 'project label', 28)
        plain(project['title'], 'project title', 90)
        plain(project['summary'], 'project summary', 400)
        text_list(project['technologies'], 'technologies', 10)
    text_list(data['notes'], 'notes', 6, maximum=250)
    text_list(data['stack'], 'stack', 20)
    snapshot = data['snapshot']
    exact_keys(snapshot, ('date', 'repository_count', 'languages'), 'snapshot')
    if not isinstance(snapshot['date'], str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', snapshot['date']):
        raise ValueError('Snapshot date must be YYYY-MM-DD.')
    date.fromisoformat(snapshot['date'])
    if type(snapshot['repository_count']) is not int or snapshot['repository_count'] < 1:
        raise ValueError('Snapshot needs at least one repository with language data.')
    languages = snapshot['languages']
    if not isinstance(languages, dict) or not languages or len(languages) > 50:
        raise ValueError('Invalid language map.')
    for language, count in languages.items():
        plain(language, 'language', 30)
        if type(count) is not int or count <= 0 or count > 10**13:
            raise ValueError('Language bytes must be positive bounded integers.')
    return data


def language_rows(data):
    counts = sorted(data['snapshot']['languages'].items(), key=lambda p: (-p[1], p[0]))
    total = sum(count for _, count in counts)
    rows = counts[:5]
    if len(counts) > 5:
        rows.append(('Other', sum(count for _, count in counts[5:])))
    return [(name, count / total * 100, COLORS.get(name, '#84909b')) for name, count in rows]


def text(x, y, value, size=14, fill='#b9aebf', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" {extra}>{escape(str(value))}</text>'


def palette(light):
    return ('#f7f3ed', '#302b38', '#6d6071', '#d9cdd8') if light else ('#15171d', '#f5ede4', '#b9aebf', '#3d3447')


def hero(data, light=False, static=False):
    svg = (ROOT / 'templates/workshop.svg').read_text(encoding='utf-8')
    svg = svg.replace('{{NAME}}', escape(data['name']))
    if light:
        for old, new in [('#15171d', '#f7f3ed'), ('#443044', '#e6d4e0'),
                         ('#f6ecdf', '#302b38'), ('#b9aebd', '#6d6071'),
                         ('#b3a8b7', '#6d6071'), ('#ddd3db', '#473a50'),
                         ('#9b929f', '#6d6071'), ('#c3a8b5', '#6d6071')]:
            svg = svg.replace(old, new)
        svg = svg.replace('fill="#f8bb79"', 'fill="#925b2a"')
    if static:
        svg = re.sub(r'<style>.*?</style>', '', svg, flags=re.S)
    return '\n'.join(line.rstrip() for line in svg.splitlines()) + '\n'


def language_svg(data, light=False):
    bg, ink, muted, border = palette(light)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="220" viewBox="0 0 1100 220" role="img" aria-labelledby="title desc"><title id="title">Languages on the workbench</title><desc id="desc">Language shares by GitHub-detected bytes. Exact values are also available in the README table.</desc><style>text {{font-family:Segoe UI,Arial,sans-serif;}}</style><rect x="1" y="1" width="1098" height="218" rx="18" fill="{bg}" stroke="{border}"/>', text(32, 42, 'THE MATERIALS', 12, muted, 'letter-spacing="2"'), text(1068, 42, data['snapshot']['date'] + ' / SNAPSHOT', 12, muted, 'text-anchor="end"')]
    x = 32.0
    for _, share, color in language_rows(data):
        width = 1036 * share / 100
        parts.append(f'<rect x="{x:.3f}" y="65" width="{width:.3f}" height="18" fill="{color}"/>')
        x += width
    for index, (name, share, color) in enumerate(language_rows(data)):
        x = 32 + index * 173
        parts.extend([f'<circle cx="{x+5}" cy="118" r="5" fill="{color}"/>', text(x+18, 123, name, 15, ink), text(x, 158, f'{share:.1f}%', 28, ink, 'font-weight="600"')])
    parts.append(text(32, 198, f"GitHub-detected bytes · {data['snapshot']['repository_count']} selected private repositories · not time spent or proficiency", 13, muted))
    return ''.join(parts) + '</svg>\n'


def md(value):
    return escape(value, quote=False).replace('|', '\\|').replace('*', '\\*').replace('_', '\\_')


def picture(stem, alt):
    return f'<picture>\n  <source media="(prefers-color-scheme: light)" srcset="assets/{stem}-light.svg">\n  <img src="assets/{stem}-dark.svg" alt="{escape(alt, quote=True)}" width="1100">\n</picture>'


def readme(data):
    parts = ['<!-- Generated from profile.json by scripts/render_profile.py. -->',
             picture('workshop', "Santhosh's Midnight Workshop: AI agents, security systems, and developer tools."),
             f"# {md(data['headline'])}", md(data['bio']),
             '[Explore the workbench](#on-the-workbench) · [See the materials](#languages-on-the-workbench) · [Static artwork](assets/workshop-static-dark.svg)',
             '## On the workbench',
             'Most of my work lives in private repositories. Here is a window into what I build.']
    for index, project in enumerate(data['projects'], 1):
        parts.extend([f"### {index:02d} / {md(project['label'])}", f"**{md(project['title'])}**", md(project['summary']),
                      ' · '.join(f'`{tech}`' for tech in project['technologies'])])
    parts.extend(['## Languages on the workbench', picture('languages', 'Language shares by detected bytes; values and scope are listed below.'),
                  '<details>\n<summary>Read the numbers and how they are measured</summary>',
                  '| Language | Share of detected bytes |\n| --- | ---: |\n' + '\n'.join(f'| {md(name)} | {share:.1f}% |' for name, share, _ in language_rows(data)),
                  f"Snapshot: **{data['snapshot']['date']}** · **{data['snapshot']['repository_count']} selected private repositories**. Shares use GitHub's detected language bytes. They do not measure proficiency or time spent. Similar code in different repositories can be counted more than once. Small languages are grouped as Other. Percentages are rounded.",
                  '</details>', '## Tools I work with', ' · '.join(f'`{tool}`' for tool in data['stack']),
                  '<details>\n<summary>Elsewhere in the workshop</summary>', '\n'.join('- ' + md(note) for note in data['notes']), '</details>',
                  '---', '**The thread through it all:** turning complex systems into tools people can use.',
                  '<sub>Hand-drawn in SVG. Built from a curated snapshot of my work. ' + f'<a href="https://github.com/{data["handle"]}">Find me on GitHub</a>.</sub>'])
    return '\n\n'.join(parts) + '\n'


def preview(data):
    template = (ROOT / 'templates/preview.html').read_text(encoding='utf-8')
    cards = ''.join(f'<article><span class="eyebrow">{i:02d} / {escape(p["label"])}</span><h3>{escape(p["title"])}</h3><p>{escape(p["summary"])}</p><div class="tags">' + ''.join(f'<span>{escape(t)}</span>' for t in p['technologies']) + '</div></article>' for i, p in enumerate(data['projects'], 1))
    replacements = {'NAME': escape(data['name']), 'HEADLINE': escape(data['headline']), 'BIO': escape(data['bio']), 'HANDLE': data['handle'], 'CARDS': cards,
                    'ROWS': ''.join(f'<tr><td>{escape(n)}</td><td>{v:.1f}%</td></tr>' for n, v, _ in language_rows(data)),
                    'NOTES': ''.join(f'<li>{escape(n)}</li>' for n in data['notes']),
                    'STACK': ''.join(f'<span>{escape(t)}</span>' for t in data['stack']),
                    'DATE': data['snapshot']['date'], 'COUNT': str(data['snapshot']['repository_count'])}
    return re.sub(r'\{\{([A-Z]+)\}\}', lambda m: replacements[m[1]], template)


def outputs(data):
    validate(data)
    result = {'README.md': readme(data), 'preview/index.html': preview(data)}
    for light in (False, True):
        tone = 'light' if light else 'dark'
        result[f'assets/workshop-{tone}.svg'] = hero(data, light)
        result[f'assets/workshop-static-{tone}.svg'] = hero(data, light, static=True)
        result[f'assets/languages-{tone}.svg'] = language_svg(data, light)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, default=ROOT / 'profile.json')
    parser.add_argument('--output-dir', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rendered = outputs(json.loads(args.snapshot.read_text(encoding='utf-8')))
    stale = []
    for relative, content in rendered.items():
        target = args.output_dir / relative
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8') != content:
                stale.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8', newline='\n')
    if stale:
        sys.exit('Generated files need refreshing: ' + ', '.join(stale))
    print(f'{"Checked" if args.check else "Rendered"} {len(rendered)} profile files.')


if __name__ == '__main__':
    main()
