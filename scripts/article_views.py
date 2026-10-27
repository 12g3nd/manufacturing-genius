"""Presentation only: all estimates and intervals come from saved study outputs."""
from html import escape
import re

POLICIES = {'equilibrium': 'Equilibrium choice', 'safe': 'Both safe (prescribed)', 'risky': 'Both risky (prescribed)'}


def article_contents(source):
    """A static mobile counterpart to Quarto's desktop contents, including subsections."""
    items = re.findall(r'^(#{2,3}) (.+?) \{#([\w-]+)[^}]*\}', source, re.MULTILINE)
    out = ['<details class="mobile-contents" id="reader-contents"><summary>Contents</summary><nav aria-label="Article contents"><ul>']
    for marks, title, target in items:
        cls = ' class="contents-subsection"' if len(marks) == 3 else ''
        out.append(f'<li{cls}><a href="#{target}">{escape(title)}</a></li>')
    out.append('<li><a href="#quarto-bibliography">References</a></li></ul></nav></details>')
    return '\n'.join(out)


def signed(text):
    """Typographic minus signs for displayed numbers."""
    return re.sub(r'-(?=\d)', '−', text)


def pct(x):
    return f'{100*x:.1f}%'


def interval(stat, scale=100, places=2):
    return signed(f"{stat['mean']*scale:.{places}f} [{stat['low']*scale:.{places}f}, {stat['high']*scale:.{places}f}]")


def comparison_panels(cells):
    chosen = [next(c for c in cells if c['delta'] == .75 and c['risk_size'] == 1.5 and c['correlation'] == rho) for rho in (0, 1)]
    out = ['<figure id="reversal-example" class="focus-evidence"><p class="figure-key">How often the better player wins. Open diamonds: exact probability. Markers and bars: simulation and 95% intervals.</p><div class="comparison-panels">']
    for c, name, suffix in zip(chosen, ('Independent shocks', 'One shared shock'), (0, 2)):
        exact, paired = c['exact_accuracy'], c['paired']['equilibrium-risky']['accuracy']
        diff = 100*(exact['equilibrium']-exact['risky'])
        out.append(f'<section class="comparison-panel" data-rho="{c["correlation"]:g}" aria-label="{name}">'
                   f'<h4>{name}</h4><p class="measurement">Correlation ρ = {c["correlation"]:g}</p>'
                   f'<img src="data/generated/selection-focus-{suffix}.svg" alt="{name}: exact accuracy is {pct(exact["safe"])} for both safe, '
                   f'{pct(exact["equilibrium"])} in equilibrium, and {pct(exact["risky"])} for both risky. Circles and bars show simulation estimates and Wilson intervals.">'
                   f'<p class="comparison-verdict">Letting players choose picks the better player '
                   f'{"more" if diff > 0 else "less"} often than forcing everyone to gamble.</p>'
                   f'<p class="paired-interval">Equilibrium minus both-risky: {signed(f"{diff:+.2f}")} percentage points exact; '
                   f'paired simulation {interval(paired)} pp (95% Monte Carlo interval).</p>'
                   '</section>')
    out.append('</div><figcaption>One example, picked before running anything: ability gap δ = '
               f'{chosen[0]["delta"]:g}; risk magnitude a = {chosen[0]["risk_size"]:g}. '
               'Open diamonds and the percentages give exact model probabilities. Filled circle: equilibrium; open square: both safe; triangle: both risky, each with its pointwise 95% Wilson interval. '
               'The line under each panel compares equilibrium with both-risky. Both-safe is a separate benchmark.</figcaption></figure>')
    return '\n'.join(out)


def assumption_explorer(cells, config):
    out = ['<details id="assumption-explorer"><summary>Pick a setting</summary>',
           '<div class="assumption-controls" hidden>']
    for key, label in (('delta', 'Ability gap <i class="sym">δ</i>'), ('risk_size', 'Risk magnitude <i class="sym">a</i>'), ('correlation', 'Correlation <i class="sym">ρ</i>')):
        default = {'delta': .75, 'risk_size': 1.5, 'correlation': 0}[key]
        options = ''.join(f'<option value="{x:g}"'+(' selected' if x == default else '')+f'>{x:g}</option>' for x in config[key])
        out.append(f'<div><label for="study-{key}">{label}</label><select id="study-{key}">{options}</select></div>')
    out.append('</div><p id="study-announcement" class="game-note" role="status"></p><div id="study-views">')
    for c in cells:
        initial = c['delta'] == .75 and c['risk_size'] == 1.5 and c['correlation'] == 0
        attrs = ' '.join(f'data-{k.replace("_", "-")}="{c[k]:g}"' for k in ('delta', 'risk_size', 'correlation'))
        out.append(f'<div class="study-view" {attrs}'+('' if initial else ' hidden')+'>')
        if c['delta'] == 0:
            out.append('<p>Accuracy is undefined at equal ability: neither player is more able. Other outcomes remain in the complete ledger.</p>')
        else:
            out.append('<dl class="accuracy-list">')
            for p, name in POLICIES.items():
                out.append(f'<div><dt>{name}</dt><dd><strong>{pct(c["exact_accuracy"][p])}</strong> exact'
                           f'<span>Simulation: {interval(c["policies"][p]["accuracy"])}%</span></dd></div>')
            out.append('</dl><p class="game-note">Simulation brackets are pointwise 95% Wilson intervals.</p>')
            for p in ('safe', 'risky'):
                diff = 100*(c['exact_accuracy']['equilibrium']-c['exact_accuracy'][p])
                out.append(f'<p class="explorer-difference">Equilibrium − both {p}: <strong>{signed(f"{diff:+.2f}")} pp exact</strong>; '
                           f'paired simulation {interval(c["paired"]["equilibrium-"+p]["accuracy"])} pp (95% Monte Carlo interval).</p>')
        out.append('</div>')
    out.append('</div><noscript><p>The selector needs JavaScript. The example above and the full charts and results below work without it.</p></noscript></details>')
    return '\n'.join(out)


def fresh_panels(cells):
    out = ['<figure id="fresh-example" class="focus-evidence"><div class="figure-key metric-key" aria-label="Figure legend">'
           '<span><svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="4" fill="#1c1712"/></svg>Reported score</span>'
           '<span><svg width="12" height="12" aria-hidden="true"><rect x="2.5" y="2.5" width="7" height="7" fill="none" stroke="#1c1712" stroke-width="1.5"/></svg>Selected ability</span>'
           '<span><svg width="12" height="12" aria-hidden="true"><path d="M6 1 L11 11 L1 11 Z" fill="#6e604d"/></svg>Fresh performance</span>'
           '</div><div class="comparison-panels">']
    for rho, name, suffix in ((0, 'Independent shocks', 0), (1, 'One shared shock', 2)):
        c = next(c for c in cells if c['delta'] == .75 and c['risk_size'] == 1.5 and c['correlation'] == rho)
        stats = c['policies']['equilibrium']
        alt = (f'{name}. Equilibrium selected ability {stats["selected_ability"]["mean"]:.3f}, '
               f'reported score {stats["reported_score"]["mean"]:.3f}, fresh performance {stats["fresh"]["mean"]:.3f} points per round. '
               'The plot compares all three rules with pointwise Monte Carlo intervals.')
        out.append(f'<section class="comparison-panel"><h3>{name}</h3><p class="measurement">Correlation ρ = {rho:g}</p>'
                   f'<img src="data/generated/fresh-focus-{suffix}.svg" alt="{escape(alt, quote=True)}"></section>')
    out.append('</div><figcaption>Same ability gap and gamble size as above. Filled circles: winning score per round; '
               'open squares: the winner’s actual ability; grey triangles: their score on the fresh test. '
               'Bars are pointwise 95% Monte Carlo intervals. Both panels share axes so the rules line up.</figcaption></figure>')
    return '\n'.join(out)
