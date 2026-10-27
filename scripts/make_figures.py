"""Full-grid and focused static figures; every point comes from the frozen study."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/generated"
# Broadside inks. Red is kept for the reader's own choice on the page, so series differ by
# ink, marker fill and line style: equilibrium heavy solid, both-safe dashed and open, both-risky wash.
INK, WASH, RULE, PAPER = "#1c1712", "#6e604d", "#b9a98a", "#dacfb5"
COLORS = {"equilibrium": INK, "safe": INK, "risky": WASH}
MARKERS = {"equilibrium": "o", "safe": "s", "risky": "^"}
FILLS = {"equilibrium": INK, "safe": PAPER, "risky": WASH}
LINES = {"equilibrium": ("-", 2.2), "safe": ("--", 1.3), "risky": (":", 1.6)}
NAMES = {"equilibrium": "Equilibrium", "safe": "Both safe", "risky": "Both risky"}


def style():
    for name in ("OldStandard-Regular.ttf", "OldStandard-Bold.ttf", "LeagueGothic.ttf"):
        font_manager.fontManager.addfont(str(ROOT / "assets/fonts" / name))
    plt.rcParams.update({"font.family": ["Old Standard TT", "DejaVu Serif"], "font.size": 12.5,
        "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none", "savefig.transparent": True,
        "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": INK, "axes.linewidth": 1.1,
        "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 17, "svg.fonttype": "path", "svg.hashsalt": "manufacturing-genius-broadside-1"})


def title(ax, text):
    upper = "".join(ch.upper() if ch.isascii() else ch for ch in text)
    ax.set_title(upper, pad=14, fontfamily=["League Gothic", "DejaVu Serif"], fontsize=19)


def save(fig, name):
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight", metadata={"Date": None})
    svg = OUT / (name + '.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8', newline='\n')
    fig.savefig(OUT / (name + ".png"), bbox_inches="tight", dpi=150)
    plt.close(fig)


def build():
    style()
    study = json.loads((OUT / "study.json").read_text(encoding="utf-8"))
    cells, config = study["cells"], study["config"]
    deltas = [d for d in config["delta"] if d > 0]
    rhos = config["correlation"]
    def group(delta, rho):
        return [c for c in cells if c["delta"] == delta and c["correlation"] == rho]
    fig, axes = plt.subplots(len(deltas), len(rhos), figsize=(10, 9), sharex=True, sharey=True)
    for i, delta in enumerate(deltas):
        for j, rho in enumerate(rhos):
            ax = axes[i, j]
            cs = group(delta, rho)
            x = np.array([c["risk_size"] for c in cs])
            for k, p in enumerate(NAMES):
                y = [c["policies"][p]["accuracy"] for c in cs]
                ax.plot(x, [c["exact_accuracy"][p] for c in cs], color=COLORS[p], ls=LINES[p][0], lw=LINES[p][1])
                ax.errorbar(x + (k-1)*.035, [v["mean"] for v in y],
                    yerr=[[v["mean"]-v["low"] for v in y], [v["high"]-v["mean"] for v in y]],
                    fmt=MARKERS[p], ms=4.5, mfc=FILLS[p], capsize=2, color=COLORS[p], lw=.9)
            if i == 0:
                title(ax, f"Correlation ρ = {rho:g}")
            if j == 0:
                ax.set_ylabel(f"Ability gap δ = {delta:g}\nSelection accuracy")
            if i == len(deltas)-1:
                ax.set_xlabel("Risk magnitude a (points)")
            ax.set_xticks(config["risk_size"])
            ax.set_ylim(.47, 1.025)
            ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
            ax.grid(axis="y", color=RULE, lw=.7)
    handles = [Line2D([0], [0], color=COLORS[p], marker=MARKERS[p], mfc=FILLS[p], ls=LINES[p][0], lw=LINES[p][1], label=NAMES[p]) for p in NAMES]
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False)
    fig.subplots_adjust(top=.91, hspace=.2, wspace=.12, bottom=.08)
    save(fig, "selection")

    fig, axes = plt.subplots(2, len(rhos), figsize=(10, 7.6), sharex=True, sharey=True)
    palette = [INK, INK, WASH]
    dstyles = [("-", 2.0, INK), ("--", 1.3, PAPER), (":", 1.6, WASH)]
    for i, baseline in enumerate(("safe", "risky")):
        for j, rho in enumerate(rhos):
            ax = axes[i, j]
            ax.axhline(0, color=INK, lw=1.2)
            for k, delta in enumerate(deltas):
                cs = group(delta, rho)
                x = np.array([c["risk_size"] for c in cs])
                y = [c["paired"]["equilibrium-"+baseline]["accuracy"] for c in cs]
                ax.plot(x, [100*(c["exact_accuracy"]["equilibrium"]-c["exact_accuracy"][baseline]) for c in cs], color=palette[k], ls=dstyles[k][0], lw=dstyles[k][1])
                ax.errorbar(x+(k-1)*.035, [100*v["mean"] for v in y],
                    yerr=[196*v["mc_se"] for v in y], fmt=["o", "s", "^"][k], ms=4.5, mfc=dstyles[k][2], color=palette[k], capsize=2, lw=.9)
            if i == 0:
                title(ax, f"Correlation ρ = {rho:g}")
            if j == 0:
                ax.set_ylabel(f"Equilibrium − {NAMES[baseline].lower()}\nAccuracy difference (pp)")
            if i == 1:
                ax.set_xlabel("Risk magnitude a (points)")
            ax.set_xticks(config["risk_size"])
            ax.grid(axis="y", color=RULE, lw=.7)
    fig.legend(handles=[Line2D([0], [0], color=c, marker=m, mfc=st[2], ls=st[0], lw=st[1], label=f"δ = {d:g}") for c, m, d, st in zip(palette, ["o", "s", "^"], deltas, dstyles)], loc="upper center", ncol=3, frameon=False)
    fig.subplots_adjust(top=.89, hspace=.2, wspace=.12, bottom=.1)
    save(fig, "paired")

    # All frozen cells, including equal ability: no undefined accuracy required.
    fig, axes = plt.subplots(len(config['delta']), len(rhos), figsize=(10, 11), sharex=True, sharey=True)
    for i, delta in enumerate(config['delta']):
        for j, rho in enumerate(rhos):
            ax = axes[i, j]
            cs = group(delta, rho)
            x = np.array([c['risk_size'] for c in cs])
            for k, p in enumerate(NAMES):
                stats = [c['policies'][p]['overstatement'] for c in cs]
                ax.errorbar(x+(k-1)*.035, [s['mean'] for s in stats],
                    yerr=[1.96*s['mc_se'] for s in stats], fmt=MARKERS[p], ls=LINES[p][0],
                    ms=4.5, mfc=FILLS[p], lw=LINES[p][1]*.8, capsize=2, color=COLORS[p])
            if i == 0:
                title(ax, f'Correlation ρ = {rho:g}')
            if j == 0:
                ax.set_ylabel(f'δ = {delta:g}'+(' (equal ability)' if delta==0 else ''))
            if i == len(config['delta'])-1:
                ax.set_xlabel('Risk magnitude a (points)')
            ax.set_xticks(config['risk_size'])
            ax.grid(axis='y', color=RULE, lw=.7)
    fig.legend(handles=handles, loc='upper center', ncol=3, frameon=False)
    fig.supylabel('Winner overstatement (points per round)', x=.005)
    fig.subplots_adjust(top=.93, hspace=.18, wspace=.12, bottom=.08)
    save(fig, 'overstatement')

    fig, axes = plt.subplots(1, len(rhos), figsize=(10, 4.8), sharey=True)
    metrics = [("reported_score", INK, "o", "Winning score F/2"),
               ("selected_ability", INK, "s", "Selected ability θ"),
               ("fresh", WASH, "^", "Fresh performance H")]
    mfill = {"reported_score": INK, "selected_ability": PAPER, "fresh": WASH}
    for j, rho in enumerate(rhos):
        ax = axes[j]
        cell = next(c for c in cells if c["delta"] == .75 and c["risk_size"] == 1.5 and c["correlation"] == rho)
        for k, (metric, color, marker, label) in enumerate(metrics):
            stats = [cell["policies"][p][metric] for p in NAMES]
            ax.errorbar(np.arange(3)+(k-1)*.14, [v["mean"] for v in stats], yerr=[1.96*v["mc_se"] for v in stats],
                fmt=marker, ms=6, mfc=mfill[metric], capsize=3, color=color, label=label)
        ax.set_xticks(range(3), list(NAMES.values()), rotation=22, ha="right")
        title(ax, f"Correlation ρ = {rho:g}")
        ax.axhline(0, color=INK, lw=.8)
        ax.grid(axis="y", color=RULE, lw=.7)
    axes[0].set_ylabel("Mean score points per round")
    fig.legend(handles=axes[0].get_legend_handles_labels()[0], labels=[m[3] for m in metrics], loc="upper center", ncol=3, frameon=False)
    fig.subplots_adjust(top=.78, bottom=.24, wspace=.12)
    save(fig, "fresh")
    build_focus(cells, rhos)
    print("Saved selection, overstatement and fresh figures, plus supplementary paired plot (SVG/PNG).")


def build_focus(cells, rhos):
    """Small reading-path panels; presentation only, using unchanged saved results."""
    rows = (('safe', 2), ('equilibrium', 1), ('risky', 0))
    label_font = dict(fontfamily=['League Gothic', 'DejaVu Serif'], fontsize=19)
    def frame(ax, xlim, ticks):
        ax.set(xlim=xlim, ylim=(-.6, 2.6), xticks=ticks)
        ax.set_yticks([y for _, y in rows], [NAMES[p] for p, _ in rows], **label_font)
        ax.tick_params(axis='y', length=0, pad=8)
        ax.tick_params(axis='x', labelsize=13)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color(INK)
        ax.grid(axis='x', color=RULE, lw=.7)
    for j, rho in enumerate(rhos):
        c = next(c for c in cells if c['delta'] == .75 and c['risk_size'] == 1.5 and c['correlation'] == rho)
        fig, ax = plt.subplots(figsize=(3.6, 2.6))
        for p, y in rows:
            s, exact = c['policies'][p]['accuracy'], c['exact_accuracy'][p]
            ax.plot(exact, y, marker='D', ms=13, markerfacecolor='none', color=INK, mew=1.1, zorder=2)
            ax.errorbar(s['mean'], y, xerr=[[s['mean']-s['low']], [s['high']-s['mean']]],
                        fmt=MARKERS[p], ms=6, mfc=FILLS[p], capsize=0, color=COLORS[p], lw=1.5, zorder=3)
            ax.text(1.0, y, f'{exact:.1%}', ha='left', va='center', fontsize=13, transform=ax.get_yaxis_transform())
        frame(ax, (.5, 1.0), [.5, .75, 1])
        ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
        fig.subplots_adjust(left=.3, right=.8, top=.97, bottom=.14)
        save(fig, f'selection-focus-{j}')

        fig, ax = plt.subplots(figsize=(3.6, 2.9))
        metrics = [('reported_score', INK, 'o', INK), ('selected_ability', INK, 's', PAPER), ('fresh', WASH, '^', WASH)]
        for p, y in rows:
            for k, (metric, color, marker, fill) in enumerate(metrics):
                s = c['policies'][p][metric]
                ax.errorbar(s['mean'], y+(1-k)*.2, xerr=1.96*s['mc_se'], fmt=marker,
                            ms=6, mfc=fill, color=color, capsize=0, lw=1.4, zorder=3)
        frame(ax, (-.05, .85), [0, .4, .8])
        ax.axvline(0, color=INK, lw=.8)
        ax.set_xlabel('Score points per round', fontsize=13)
        fig.subplots_adjust(left=.3, right=.97, top=.97, bottom=.2)
        save(fig, f'fresh-focus-{j}')


if __name__ == "__main__":
    build()
