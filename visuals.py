# visualizer.py
import matplotlib.pyplot as plt
import numpy as np

PLANET_SYMBOLS = {
    "Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀", "Mars": "♂",
    "Jupiter": "♃", "Saturn": "♄", "Uranus": "♅", "Neptune": "♆", "Pluto": "♇",
    "Ascendant": "As", "Midheaven": "Mc"
}
SIGN_SYMBOLS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
ASPECT_COLORS = {
    "Conjunction": "gray",
    "Sextile": "green",
    "Square": "red",
    "Trine": "blue",
    "Opposition": "purple"
}

def draw_natal_chart(chart_data, aspects=None):
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('W')
    ax.set_theta_direction(-1)
    ax.set_xticks(np.radians(np.arange(0, 360, 30)))
    ax.set_xticklabels(SIGN_SYMBOLS, fontsize=16)
    ax.set_yticklabels([])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.spines['polar'].set_visible(False)
    ax.set_facecolor('#f8f5ec')
    fig.patch.set_facecolor('#f8f5ec')

    # Draw house axes
    asc_deg = chart_data['Ascendant']['degree_val']
    mc_deg = chart_data['Midheaven']['degree_val']
    ax.plot([np.radians(asc_deg), np.radians(asc_deg + 180)], [0, 1], 'k-', lw=2, alpha=0.7)
    ax.text(np.radians(asc_deg), 1.05, "ASC", ha='center', fontsize=12, weight='bold')
    ax.plot([np.radians(mc_deg), np.radians(mc_deg + 180)], [0, 1], 'k-', lw=1.5, alpha=0.7)
    ax.text(np.radians(mc_deg), 1.05, "MC", ha='center', fontsize=12, weight='bold')

    # Plot aspects
    if aspects:
        for aspect in aspects:
            p1, p2 = aspect["planets"]
            if p1 in chart_data and p2 in chart_data:
                deg1 = np.radians(chart_data[p1]["degree_val"])
                deg2 = np.radians(chart_data[p2]["degree_val"])
                color = ASPECT_COLORS.get(aspect["type"], "gray")
                ax.plot([deg1, deg2], [0.8, 0.8], color=color, lw=1.5, alpha=0.6, zorder=1)

    # Plot planets
    radii = {name: 0.85 - (i * 0.04) for i, name in enumerate(PLANET_SYMBOLS)}
    for name, data in chart_data.items():
        if name in PLANET_SYMBOLS:
            angle = np.radians(data['degree_val'])
            radius = radii.get(name, 0.6)
            ax.text(angle, radius, PLANET_SYMBOLS[name],
                    ha='center', va='center', fontsize=16, color='darkblue',
                    bbox=dict(boxstyle='circle,pad=0.1', fc='white', ec='darkblue', lw=1.2))
            ax.text(angle, radius - 0.07, data['degree_str'],
                    ha='center', va='center', fontsize=8, color='black', alpha=0.8)

    ax.set_rmax(1.1)
    ax.set_title("Sidereal Natal Chart (Lahiri)", pad=30, fontsize=18, weight='bold')
    plt.tight_layout()
    return fig