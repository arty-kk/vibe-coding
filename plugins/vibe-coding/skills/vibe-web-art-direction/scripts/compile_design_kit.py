#!/usr/bin/env python3
"""Compile explicit design decisions into local CSS, SVG materials and a review board."""
import argparse
import html
import json
import math
from pathlib import Path
import random
import re

CORE_COLORS = {'background', 'surface', 'text', 'muted', 'accent', 'on-accent', 'line'}
TYPE_FIELDS = {'family', 'min_rem', 'max_rem', 'fluid_vw', 'line_height', 'weight', 'tracking_em', 'measure_ch'}
LAYOUT_FIELDS = {'container_rem', 'gutter_min_rem', 'gutter_max_rem', 'gutter_vw', 'columns', 'gap_rem', 'section_min_rem', 'section_max_rem', 'header_rem'}


def object_fields(value, label, allowed, required=None):
    if not isinstance(value, dict) or set(value) - allowed or not (required or set()) <= set(value):
        raise ValueError(label + ': missing or unsupported fields')
    return value


def numeric(value, label, low, high, integer=False):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high or integer and int(value) != value:
        raise ValueError(f'{label}: expected {low}..{high}' + (' integer' if integer else ''))
    return value


def token(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,39}', value):
        raise ValueError('Invalid token name')
    return value


def text(value, label, maximum=300):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(label + ': nonempty bounded text required')
    return value


def validate(spec):
    object_fields(spec, 'design kit', {'name', 'colors', 'type', 'layout', 'motion', 'materials', 'effects', 'assets'}, {'name', 'colors', 'type', 'layout', 'motion'})
    text(spec['name'], 'name', 120)
    colors = spec['colors']
    if not isinstance(colors, dict) or not CORE_COLORS <= set(colors) or len(colors) > 32:
        raise ValueError('colors: define semantic core colors, at most 32')
    for name, value in colors.items():
        token(name)
        if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
            raise ValueError('colors: six-digit hex values required')
    def color(name):
        if name not in colors:
            raise ValueError('Unknown color token: ' + str(name))
    typography = object_fields(spec['type'], 'type', {'families', 'roles'}, {'families', 'roles'})
    families, roles = typography['families'], typography['roles']
    if not isinstance(families, dict) or not 1 <= len(families) <= 6:
        raise ValueError('type.families: define 1..6 font stacks')
    for name, stack in families.items():
        token(name)
        if not isinstance(stack, list) or not 1 <= len(stack) <= 8 or any(not isinstance(font, str) or not re.fullmatch(r'[\w -]{1,80}', font) for font in stack):
            raise ValueError('Font stacks must contain plain family names')
    if not isinstance(roles, dict) or not {'display', 'heading', 'body', 'label', 'caption'} <= set(roles) or len(roles) > 12:
        raise ValueError('type.roles: display, heading, body, label and caption required')
    for name, role in roles.items():
        token(name)
        object_fields(role, 'type.' + name, TYPE_FIELDS, TYPE_FIELDS)
        if role['family'] not in families:
            raise ValueError('Unknown font stack: ' + str(role['family']))
        minimum = 1 if name == 'body' else .875 if name == 'label' else .75
        numeric(role['min_rem'], name + '.min_rem', minimum, 12)
        numeric(role['max_rem'], name + '.max_rem', role['min_rem'], 16)
        numeric(role['fluid_vw'], name + '.fluid_vw', 0, 8)
        numeric(role['line_height'], name + '.line_height', .85, 2.5)
        numeric(role['weight'], name + '.weight', 100, 900, True)
        numeric(role['tracking_em'], name + '.tracking_em', -.1, .5)
        numeric(role['measure_ch'], name + '.measure_ch', 4, 120)
    layout = object_fields(spec['layout'], 'layout', LAYOUT_FIELDS, LAYOUT_FIELDS)
    for key, low, high in [('container_rem', 20, 120), ('gutter_min_rem', .5, 6), ('gutter_max_rem', .5, 8), ('gutter_vw', 0, 8), ('columns', 1, 24), ('gap_rem', 0, 8), ('section_min_rem', .5, 16), ('section_max_rem', .5, 20), ('header_rem', 2, 10)]:
        numeric(layout[key], 'layout.' + key, low, high, key == 'columns')
    if layout['gutter_min_rem'] > layout['gutter_max_rem'] or layout['section_min_rem'] > layout['section_max_rem']:
        raise ValueError('Layout minimum exceeds maximum')
    motion = object_fields(spec['motion'], 'motion', {'fast_ms', 'base_ms', 'scene_ms', 'easing'}, {'fast_ms', 'base_ms', 'scene_ms', 'easing'})
    for key in ('fast_ms', 'base_ms', 'scene_ms'):
        numeric(motion[key], 'motion.' + key, 0, 3000, True)
    easing = motion['easing']
    if easing not in ('ease', 'ease-in-out', 'linear'):
        match = re.fullmatch(r'cubic-bezier\(\s*([\d.-]+)\s*,\s*([\d.-]+)\s*,\s*([\d.-]+)\s*,\s*([\d.-]+)\s*\)', str(easing))
        if not match:
            raise ValueError('Unsupported easing')
        for i, raw in enumerate(match.groups()):
            numeric(float(raw), 'easing', 0 if i % 2 == 0 else -3, 1 if i % 2 == 0 else 3)
    materials = object_fields(spec.get('materials', {}), 'materials', {'gradient', 'glass', 'procedural'})
    if 'gradient' in materials:
        gradient = object_fields(materials['gradient'], 'gradient', {'colors', 'angle_deg'}, {'colors', 'angle_deg'})
        if not isinstance(gradient['colors'], list) or not 2 <= len(gradient['colors']) <= 4:
            raise ValueError('gradient.colors: 2..4 color tokens required')
        for name in gradient['colors']: color(name)
        numeric(gradient['angle_deg'], 'gradient.angle_deg', -360, 360)
    if 'glass' in materials:
        glass = object_fields(materials['glass'], 'glass', {'color', 'fallback', 'border', 'alpha', 'blur_px'}, {'color', 'fallback', 'border', 'alpha', 'blur_px'})
        for key in ('color', 'fallback', 'border'): color(glass[key])
        numeric(glass['alpha'], 'glass.alpha', .1, .99)
        numeric(glass['blur_px'], 'glass.blur_px', 0, 24)
    if 'procedural' in materials:
        field = object_fields(materials['procedural'], 'procedural', {'kind', 'seed', 'density', 'opacity', 'stroke_px', 'color', 'quiet'}, {'kind', 'seed', 'density', 'opacity', 'stroke_px', 'color', 'quiet'})
        if field['kind'] not in ('flow', 'contours', 'dots') or field['quiet'] not in ('left', 'right', 'center'):
            raise ValueError('Unsupported procedural kind or quiet region')
        color(field['color'])
        for key, low, high in [('seed', 0, 1000000), ('density', 8, 80), ('opacity', .01, .6), ('stroke_px', .25, 3)]:
            numeric(field[key], 'procedural.' + key, low, high, key in ('seed', 'density'))
    effects = object_fields(spec.get('effects', {}), 'effects', {'tints', 'borders', 'shadows'})
    for family, values in effects.items():
        if not isinstance(values, dict) or len(values) > 16: raise ValueError('effects: bounded named families required')
        for name, value in values.items():
            token(name)
            fields = {'color', 'alpha'} | ({'width_px'} if family == 'borders' else {'x_px', 'y_px', 'blur_px', 'spread_px'} if family == 'shadows' else set())
            object_fields(value, 'effects.' + name, fields, fields)
            color(value['color']); numeric(value['alpha'], 'effects.alpha', 0, 1)
            if family == 'tints' and name in colors: raise ValueError('Tint cannot replace an opaque semantic color')
            if family == 'borders': numeric(value['width_px'], 'border.width_px', 0, 4)
            if family == 'shadows':
                for key, low, high in [('x_px', -40, 40), ('y_px', -40, 40), ('blur_px', 0, 64), ('spread_px', -32, 32)]:
                    numeric(value[key], 'shadow.' + key, low, high)
    assets = spec.get('assets', [])
    if not isinstance(assets, list) or len(assets) > 64:
        raise ValueError('assets: list of at most 64 entries required')
    identities = set()
    for asset in assets:
        object_fields(asset, 'asset', {'id', 'kind', 'status', 'source', 'rights', 'role', 'fallback', 'budget_kb'}, {'id', 'kind', 'status', 'source', 'rights', 'role', 'fallback', 'budget_kb'})
        token(asset['id'])
        if asset['id'] in identities: raise ValueError('Duplicate asset ID')
        identities.add(asset['id'])
        if asset['kind'] not in ('photo', 'icon', '3d', 'video', 'font', 'illustration', 'material') or asset['status'] not in ('available', 'planned'):
            raise ValueError('Unsupported asset kind or status')
        for key in ('source', 'rights', 'role', 'fallback'): text(asset[key], 'asset.' + key, 1200)
        numeric(asset['budget_kb'], 'asset.budget_kb', 0, 100000)
    return spec


def contrast(first, second):
    def luminance(value):
        rgb = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
        return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))
    a, b = sorted((luminance(first), luminance(second)))
    return (b + .05) / (a + .05)


def css_tokens(spec):
    lines = [':root {']
    lines += [f'  --color-{name}: {value};' for name, value in sorted(spec['colors'].items())]
    for family, values in spec.get('effects', {}).items():
        for name, value in values.items():
            raw = spec['colors'][value['color']]
            rgb = ', '.join(str(int(raw[i:i+2], 16)) for i in (1, 3, 5))
            fill = f'rgba({rgb}, {value["alpha"]})'
            if family == 'tints': lines.append(f'  --color-{name}: {fill};')
            elif family == 'borders': lines.append(f'  --border-{name}: {value["width_px"]}px solid {fill};')
            else: lines.append(f'  --shadow-{name}: {value["x_px"]}px {value["y_px"]}px {value["blur_px"]}px {value["spread_px"]}px {fill};')
    for name, stack in spec['type']['families'].items():
        generic = {'serif', 'sans-serif', 'monospace', 'system-ui', 'cursive', 'fantasy'}
        family = ', '.join(font if font in generic else json.dumps(font, ensure_ascii=False) for font in stack)
        lines.append(f'  --font-{name}: {family};')
    for name, value in spec['layout'].items():
        unit = 'rem' if name.endswith('_rem') else 'vw' if name.endswith('_vw') else ''
        lines.append(f'  --layout-{name.replace("_", "-")}: {value}{unit};')
    for key in ('fast_ms', 'base_ms', 'scene_ms'):
        lines.append(f'  --motion-{key[:-3]}: {spec["motion"][key]}ms;')
    lines += [f'  --motion-easing: {spec["motion"]["easing"]};', '}']
    for name, role in spec['type']['roles'].items():
        lines.append(f'.type-{name} {{ font-family: var(--font-{role["family"]}); font-size: clamp({role["min_rem"]}rem, calc({role["min_rem"]}rem + {role["fluid_vw"]}vw), {role["max_rem"]}rem); line-height: {role["line_height"]}; font-weight: {role["weight"]}; letter-spacing: {role["tracking_em"]}em; max-inline-size: {role["measure_ch"]}ch; }}')
    materials = spec.get('materials', {})
    if 'gradient' in materials:
        gradient = materials['gradient']
        values = ', '.join('var(--color-' + color + ')' for color in gradient['colors'])
        lines.append(f'.material-gradient {{ background: linear-gradient({gradient["angle_deg"]}deg, {values}); }}')
    if 'glass' in materials:
        glass = materials['glass']; raw = spec['colors'][glass['color']]
        rgb = ', '.join(str(int(raw[i:i+2], 16)) for i in (1, 3, 5))
        lines += [f'.material-glass {{ background: var(--color-{glass["fallback"]}); border: 1px solid var(--color-{glass["border"]}); }}',
                  f'@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {{ .material-glass {{ background: rgba({rgb}, {glass["alpha"]}); backdrop-filter: blur({glass["blur_px"]}px); -webkit-backdrop-filter: blur({glass["blur_px"]}px); }} }}']
    lines.append('@media (prefers-reduced-motion: reduce) { :root { --motion-fast: 0ms; --motion-base: 0ms; --motion-scene: 0ms; } }')
    return '\n'.join(lines) + '\n'


def field_svg(field, colors):
    rng = random.Random(field['seed']); phase = rng.uniform(0, math.tau)
    paths = []; count = field['density']; color = colors[field['color']]
    if field['kind'] == 'dots':
        for row in range(max(5, count // 2)):
            for col in range(count):
                x = 1200 * (col + .5) / count; y = 720 * (row + .5) / max(5, count // 2)
                radius = 1 + 3 * (.5 + .5 * math.sin(x / 150 + y / 190 + phase))
                paths.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{color}"/>')
    else:
        for index in range(count):
            points = []
            for step in range(97):
                t = step / 96
                if field['kind'] == 'contours':
                    theta = t * math.tau; radius = 30 + index * 11 + 10 * math.sin(theta * 3 + phase + index / 15)
                    x = 770 + radius * math.cos(theta) * 1.2; y = 360 + radius * math.sin(theta) * .8
                else:
                    x = t * 1200; y = index * 820 / max(1, count - 1) - 50 + 65 * math.sin(t * 5 + phase + index / 11) + 26 * math.sin(t * 11 + index / 17)
                points.append(('M' if step == 0 else 'L') + f'{x:.2f},{y:.2f}')
            paths.append(f'<path d="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="{field["stroke_px"]}"/>')
    stops = {'left': [(0, 'black'), (.4, 'black'), (1, 'white')], 'right': [(0, 'white'), (.6, 'black'), (1, 'black')], 'center': [(0, 'white'), (.35, 'black'), (.65, 'black'), (1, 'white')]}[field['quiet']]
    gradient = ''.join(f'<stop offset="{offset * 100}%" stop-color="{color}"/>' for offset, color in stops)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720"><defs><linearGradient id="quiet">{gradient}</linearGradient><mask id="reading"><rect width="1200" height="720" fill="url(#quiet)"/></mask></defs><g opacity="{field["opacity"]}" mask="url(#reading)">{"".join(paths)}</g></svg>\n'


def compile_kit(raw):
    spec = validate(raw); colors = spec['colors']; checks = []
    for foreground, background in [('text', 'background'), ('text', 'surface'), ('muted', 'background'), ('muted', 'surface'), ('on-accent', 'accent')]:
        ratio = contrast(colors[foreground], colors[background])
        checks.append({'foreground': foreground, 'background': background, 'ratio': round(ratio, 3), 'minimum': 4.5, 'passed': ratio >= 4.5})
    required = ['Actual font files, glyph coverage and rendering', 'Responsive page, interaction and visual acceptance']
    if spec.get('materials') or spec.get('effects'): required.append('Rendered text/control contrast over materials in all relevant states')
    report = {'spec': spec, 'solid_text_contrast': checks, 'solid_text_contrast_passed': all(row['passed'] for row in checks), 'render_required': required,
              'limits': 'Local design parameters and opaque text-color checks only. No assets downloaded, fonts verified, 3D scene supplied or website certified.'}
    outputs = {'design-tokens.css': css_tokens(spec)}
    materials = spec.get('materials', {})
    if 'gradient' in materials:
        gradient = materials['gradient']; angle = math.radians(gradient['angle_deg'])
        x, y = math.sin(angle) * 50, -math.cos(angle) * 50
        stops = ''.join(f'<stop offset="{i / (len(gradient["colors"]) - 1) * 100:.2f}%" stop-color="{colors[color]}"/>' for i, color in enumerate(gradient['colors']))
        outputs['gradient.svg'] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720"><defs><linearGradient id="field" x1="{50-x:.2f}%" y1="{50-y:.2f}%" x2="{50+x:.2f}%" y2="{50+y:.2f}%">{stops}</linearGradient></defs><rect width="1200" height="720" fill="url(#field)"/></svg>\n'
    if 'procedural' in materials: outputs['procedural.svg'] = field_svg(materials['procedural'], colors)
    escape = html.escape
    swatches = ''.join(f'<article class="swatch"><div style="background:{value}"></div><strong>{escape(name)}</strong><code>{value}</code></article>' for name, value in colors.items())
    specimens = ''.join(f'<article class="specimen"><small>{escape(name)} · {role["min_rem"]}–{role["max_rem"]} rem</small><p class="type-{name}">A distinct point of view. Выразительный характер.</p></article>' for name, role in spec['type']['roles'].items())
    rows = ''.join(f'<tr><td>{row["foreground"]} / {row["background"]}</td><td>{row["ratio"]}:1</td><td>{"Pass" if row["passed"] else "Fail"}</td></tr>' for row in checks)
    samples = ''.join(f'<figure><img src="{filename}" alt="Generated {filename.split(".")[0]} material sample"/><figcaption>{filename}</figcaption></figure>' for filename in outputs if filename.endswith('.svg'))
    if 'glass' in materials: samples += '<figure class="glass-stage material-gradient"><div class="material-glass">Material / Материал<br/>Rendered contrast still requires inspection.</div><figcaption>Glass with opaque fallback</figcaption></figure>'
    for family, values in spec.get('effects', {}).items():
        for name in values:
            style = f'background:var(--color-{name})' if family == 'tints' else f'border:var(--border-{name})' if family == 'borders' else f'box-shadow:var(--shadow-{name})'
            samples += f'<figure><div class="finish-sample" style="{style}">Accent / Акцент</div><figcaption>{family} · {name}</figcaption></figure>'
    asset_rows = ''.join(f'<tr><td>{escape(asset["id"])}</td><td>{escape(asset["kind"])}</td><td>{escape(asset["status"])}</td><td>{escape(asset["role"])}</td></tr>' for asset in spec.get('assets', []))
    board_css = '*{box-sizing:border-box}body{margin:0;background:var(--color-background);color:var(--color-text);font-family:var(--font-body)}main{max-width:90rem;margin:auto;padding:clamp(1rem,4vw,4rem)}header{padding:2rem 0 4rem;border-bottom:1px solid var(--color-line)}h1{margin:1rem 0}section{padding:2.5rem 0;border-bottom:1px solid var(--color-line)}h2{font:600 1.5rem var(--font-body)}small,figcaption{color:var(--color-muted)}p{overflow-wrap:anywhere}.swatches,.materials{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr));gap:1rem}.swatch{padding:1rem;border:1px solid var(--color-line)}.swatch div{height:7rem;margin-bottom:1rem}.swatch code{display:block;margin-top:.5rem}.specimen{padding:1.5rem 0;overflow:hidden}.specimen p{margin:.8rem 0}figure{margin:0;min-width:0}figure img{display:block;width:100%;aspect-ratio:5/3;object-fit:cover;background:var(--color-surface)}figcaption{padding:.7rem 0}.glass-stage{min-height:15rem;padding:2rem;display:grid;align-content:center}.material-glass{padding:1.5rem;border-radius:1rem;color:var(--color-text)}table{width:100%;border-collapse:collapse}td{padding:.8rem .3rem;border-bottom:1px solid var(--color-line);overflow-wrap:anywhere}footer{padding:2rem 0;max-width:65ch;line-height:1.6}'
    board_css = board_css.replace('var(--font-body)', 'var(--font-' + spec['type']['roles']['body']['family'] + ')')
    board_css += 'h1{overflow-wrap:anywhere}th{text-align:left;padding:.8rem .3rem;border-bottom:1px solid var(--color-line)}'
    board_css += '.finish-sample{min-height:9rem;padding:1.5rem;margin:.8rem 0;display:grid;align-items:center;background:var(--color-surface);color:var(--color-text)}'
    outputs['design-board.html'] = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(spec["name"])} · Design kit</title><link rel="stylesheet" href="design-tokens.css"><style>{board_css}</style></head><body><main><header><p class="type-label">DESIGN SYSTEM STUDY</p><h1 class="type-display">{escape(spec["name"])}</h1><p class="type-body">Typography, color and material decisions for review.</p></header><section><h2>Semantic palette</h2><div class="swatches">{swatches}</div></section><section><h2>Type roles</h2>{specimens}</section><section><h2>Materials</h2><div class="materials">{samples or "No materials selected."}</div></section><section><h2>Opaque text contrast</h2><table><thead><tr><th scope="col">Pair</th><th scope="col">Ratio</th><th scope="col">Result</th></tr></thead><tbody>{rows}</tbody></table></section><section><h2>Asset plan</h2><table><thead><tr><th scope="col">Asset</th><th scope="col">Kind</th><th scope="col">Status</th><th scope="col">Role</th></tr></thead><tbody>{asset_rows or "<tr><td colspan=4>No assets declared.</td></tr>"}</tbody></table></section><footer>{escape(report["limits"])}<p>{escape("; ".join(required))}</p></footer></main></body></html>\n'
    report['generated_files'] = list(outputs) + ['design-kit.json']
    outputs['design-kit.json'] = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    return outputs, report


def unique_pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value: raise ValueError('Duplicate JSON field: ' + key)
        value[key] = item
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--force', action='store_true', help='Replace this compiler’s existing named outputs')
    args = parser.parse_args()
    try:
        if args.input.stat().st_size > 256 * 1024: raise ValueError('Input exceeds 256 KiB')
        spec = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)
        outputs, report = compile_kit(spec)
        output = args.output_dir.expanduser().resolve()
        names = set(outputs) | {'gradient.svg', 'procedural.svg'}
        for name in names:
            target = output/name
            if target.is_symlink() or target.resolve() == args.input.resolve():
                raise ValueError('Output collides with input or symbolic link: ' + name)
        if any((output/name).exists() for name in names) and not args.force: raise ValueError('Named output exists; use a new directory or --force')
        output.mkdir(parents=True, exist_ok=True)
        for name, data in outputs.items(): (output/name).write_text(data, encoding='utf-8', newline='\n')
        if args.force:
            for name in names - set(outputs): (output/name).unlink(missing_ok=True)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    print(f'Wrote {len(outputs)} local kit files to {output}; opaque text contrast: ' + ('passed' if report['solid_text_contrast_passed'] else 'failed'))
    return 0 if report['solid_text_contrast_passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
