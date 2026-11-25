"""Build the two original figures for the SDG 14 essay.

Run from anywhere:  python3 latex/figures/make_figures.py
Outputs (next to this script):
  bigdata_workflow.pdf  - Big Earth data sources -> indicators -> SDG 14 targets
  mpa_coverage.pdf      - Marine protected-area coverage by country vs targets

Every number in the chart comes from a source the essay already cites.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10,
    "pdf.fonttype": 42,  # embed real fonts so text stays selectable
    "axes.spines.top": False,
    "axes.spines.right": False,
})

INK = "#222222"
BLUE = "#1f5a8a"
LIGHT = "#dbe8f3"
GREY = "#9a9a9a"


# --------------------------------------------------------------------------
# Figure A: Big Earth data workflow
# --------------------------------------------------------------------------
def box(ax, x, y, w, h, title, body, face="white", edge=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.008,rounding_size=0.015",
                                linewidth=0.9, edgecolor=edge, facecolor=face))
    ax.text(x + w / 2, y + h - 0.022, title, ha="center", va="top",
            fontsize=9.5, fontweight="bold", color=INK)
    if body:
        ax.text(x + w / 2, y + h - 0.068, body, ha="center", va="top",
                fontsize=8.3, color=INK, linespacing=1.25)


def arrow(ax, x0, y0, x1, y1, color=INK, style="-|>", ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color, lw=0.9,
                                linestyle=ls, shrinkA=0, shrinkB=0))


def workflow():
    fig, ax = plt.subplots(figsize=(6.5, 4.3))
    ax.set_xlim(-0.015, 1.015)
    ax.set_ylim(0, 1)
    ax.axis("off")

    cols = [0.0, 0.355, 0.71]
    w = 0.29
    for x, head in zip(cols, ["Data sources", "Derived indicators",
                              "SDG 14 targets"]):
        ax.text(x + w / 2, 0.985, head, ha="center", va="top",
                fontsize=10.5, fontweight="bold", color=BLUE)

    h, gap, top = 0.175, 0.03, 0.915
    ys = [top - h - i * (h + gap) for i in range(4)]

    sources = [
        ("Satellite imagery", "Sea-surface temperature,\nchlorophyll-a, coastline\nand habitat extent"),
        ("Vessel tracking (AIS)", "Ship positions, speed\nand fishing behaviour"),
        ("Ocean sensors & buoys", "Water chemistry, pH,\ntemperature profiles"),
        ("Models & ML", "Combine sources into\ngap-filled time series\nand forecasts"),
    ]
    indicators = [
        ("Eutrophication & debris", "Algal-bloom index,\nfloating-plastic estimates"),
        ("Habitat condition", "Reef heat stress & bleaching,\nmangrove and seagrass change"),
        ("Ocean acidification", "Mean seawater pH\nat sampling stations"),
        ("Fishing pressure", "Fishing effort maps,\nlikely IUU activity"),
    ]
    targets = [
        ("14.1  Marine pollution", ""),
        ("14.2 / 14.5  Protect\necosystems & areas", ""),
        ("14.3  Acidification", ""),
        ("14.4  Sustainable fishing", ""),
    ]

    for y, (t, b) in zip(ys, sources):
        box(ax, cols[0], y, w, h, t, b)
    for y, (t, b) in zip(ys, indicators):
        box(ax, cols[1], y, w, h, t, b, face=LIGHT, edge=BLUE)
    for y, (t, _) in zip(ys, targets):
        ax.add_patch(FancyBboxPatch((cols[2], y), w, h,
                                    boxstyle="round,pad=0.008,rounding_size=0.015",
                                    linewidth=0.9, edgecolor=BLUE, facecolor="white"))
        ax.text(cols[2] + w / 2, y + h / 2, t, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=BLUE, linespacing=1.2)

    mid = lambda y: y + h / 2
    x_out, x_in = cols[0] + w + 0.008, cols[1] - 0.008
    # source -> indicator links (which sources feed which indicator)
    links = [(0, 0), (0, 1), (2, 2), (1, 3), (3, 0), (3, 1), (3, 3)]
    for s, i in links:
        same = s == i
        arrow(ax, x_out, mid(ys[s]), x_in, mid(ys[i]),
              color=INK if same else GREY)
    # indicator -> target, one to one
    for y in ys:
        arrow(ax, cols[1] + w + 0.008, mid(y), cols[2] - 0.008, mid(y), color=BLUE)

    # field validation feeds back into the indicators
    ax.text(0.5, 0.012,
            "Field surveys, catch records and in situ sampling validate every indicator "
            "before it is used as evidence",
            ha="center", va="bottom", fontsize=8.3, style="italic", color=INK)

    fig.savefig(OUT / "bigdata_workflow.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / "bigdata_workflow.png", dpi=200, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure B: MPA coverage by country
# --------------------------------------------------------------------------
def mpa_chart():
    # (country, % of national waters protected, year, note)
    data = [
        ("Australia", 48.9, "2024"),
        ("Brazil", 26.49, "2023"),
        ("United States", 24.0, "2024"),
        ("China", None, "9.33 Mha reported;\nno comparable %"),
        ("Japan", None, "no comparable %\npublished"),
        ("India", None, "130 MPAs;\nno comparable %"),
    ]
    planned_au = 52.0
    global_mpa = 8.12

    fig, ax = plt.subplots(figsize=(6.5, 3.3))
    names = [d[0] for d in data]
    x = range(len(data))

    for i, (name, val, note) in enumerate(data):
        if val is None:
            ax.bar(i, 2.2, width=0.6, color="white", edgecolor=GREY,
                   hatch="///", linewidth=0.8)
            ax.text(i, 2.9, note, ha="center", va="bottom", fontsize=7.5,
                    color="#555555", style="italic", linespacing=1.15)
        else:
            ax.bar(i, val, width=0.6, color=BLUE, edgecolor=BLUE)
            ax.text(i, val - 1.5, f"{val:g}%", ha="center", va="top",
                    fontsize=9, fontweight="bold", color="white")
            ax.text(i, 1.2, note, ha="center", va="bottom", fontsize=7.5,
                    color="white")

    # Australia's announced expansion to 52 %
    ax.bar(0, planned_au - 48.9, bottom=48.9, width=0.6, color="white",
           edgecolor=BLUE, hatch="....", linewidth=0.8)
    ax.text(0.34, planned_au, f"{planned_au:g}% after\nexpansion", ha="left",
            va="center", fontsize=7.5, color=BLUE)

    lines = [(30, "30% target\n(2030)", "--", "center"),
             (10, "10% target (2020)", ":", "bottom"),
             (global_mpa, f"Global ocean\n{global_mpa}% (2024)", "-", "top")]
    for yv, txt, ls, va in lines:
        col = GREY if ls == "-" else INK
        ax.axhline(yv, color=col, lw=0.9, ls=ls, zorder=0)
        ax.text(1.01, yv + (0.3 if va == "bottom" else -0.3 if va == "top" else 0),
                txt, transform=ax.get_yaxis_transform(), ha="left", va=va,
                fontsize=8, color=col, clip_on=False, linespacing=1.1)

    ax.set_xticks(list(x))
    ax.set_xticklabels(names)
    ax.set_ylabel("Marine area protected (%)")
    ax.set_ylim(0, 58)
    ax.set_xlim(-0.5, len(data) - 0.5)
    ax.tick_params(axis="x", length=0)

    fig.tight_layout()
    fig.savefig(OUT / "mpa_coverage.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / "mpa_coverage.png", dpi=200, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


if __name__ == "__main__":
    workflow()
    mpa_chart()
    print("wrote", *(p.name for p in sorted(OUT.glob("*.pdf"))))
