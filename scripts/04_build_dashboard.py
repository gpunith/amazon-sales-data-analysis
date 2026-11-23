
"""
Sales Performance Overview - single-page dashboard (matplotlib)
Run:  python sales_dashboard.py
Output: sales_dashboard.png  (+ shows window)

If you have the real file (amazon_sales_clean.csv) you can replace the
DATA section with values computed from it. The numbers below are taken
from your screenshot; the monthly / quarterly splits are generated so
that they add up to those totals.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Wedge, Polygon, Circle
from matplotlib.colors import LinearSegmentedColormap

# ----------------------------------------------------------------- THEME
PINK, TEAL, LTEAL = "#e0457b", "#1f8a9e", "#b8dfe3"
GREEN, RED, GRAY, AMBER = "#2e9e5b", "#d9534f", "#9aa5b1", "#e8a838"
NAVY, BG, CARD, INK, MUTED = "#0f3d4a", "#eaf0f2", "#ffffff", "#1d2b33", "#7b8790"
plt.rcParams["font.family"] = "DejaVu Sans"

# ------------------------------------------------------------------ DATA (computed from amazon_sales_clean.csv)
import os
import pandas as pd

try:
    _HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:                      # Jupyter
    _HERE = os.getcwd()
_CANDIDATES = [os.path.join(_HERE, "amazon_sales_clean.csv"),
               os.path.join(_HERE, "data", "amazon_sales_clean.csv"),
               os.path.join(_HERE, "..", "data", "amazon_sales_clean.csv"),
               os.path.join(os.getcwd(), "amazon_sales_clean.csv")]
CSV = next((p for p in _CANDIDATES if os.path.exists(p)), None)
if CSV is None:
    raise FileNotFoundError("amazon_sales_clean.csv not found. Looked in:\n" + "\n".join(_CANDIDATES))
df = pd.read_csv(CSV, parse_dates=["Order_Date"])

LAKH = 1e5
total_orders = len(df)
net_rev_cr = df["Net_Revenue"].sum() / 1e7
aov = df["Net_Revenue"].mean()
buyers = df["Customer_ID"].nunique()

_cat = (df.groupby("Category")
          .agg(rev=("Net_Revenue", lambda s: s.sum() / LAKH), orders=("Order_ID", "count"),
               rating=("Rating", "mean"))
          .sort_values("rev", ascending=False))
categories = list(_cat.index)
cat_rev = [round(v, 2) for v in _cat["rev"]]
cat_orders = [int(v) for v in _cat["orders"]]
cat_rating = [round(v, 1) for v in _cat["rating"]]

_st = df["Order_Status"].value_counts(normalize=True) * 100
status = [(s, round(_st[s], 1), c) for s, c in
          [("Delivered", GREEN), ("Returned", RED), ("Cancelled", GRAY), ("Pending", AMBER)]]
completion = status[0][1]
returned_pct = status[1][1]

_mon = (df.groupby(["Year", "Month"])
          .agg(o=("Order_ID", "count"), r=("Net_Revenue", lambda s: s.sum() / LAKH))
          .reindex([(y, m) for y in (2023, 2024) for m in range(1, 13)]))
months = [f"{m}-{y}" for y in ("23", "24")
          for m in ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")]
m_orders = _mon["o"].fillna(0).to_numpy()
m_rev = _mon["r"].fillna(0).to_numpy()

_yr = df.groupby("Year")["Net_Revenue"].sum()
rev_yoy = (_yr[2024] / _yr[2023] - 1) * 100
ord_yoy = (len(df[df.Year == 2024]) / len(df[df.Year == 2023]) - 1) * 100

_q = (df.pivot_table(index="Category", columns=["Year", "Quarter"], values="Net_Revenue", aggfunc="sum")
        .reindex(categories).fillna(0) / LAKH)
heat = _q.to_numpy()

_pay = (df.groupby("Payment_Mode")["Net_Revenue"].sum() / LAKH).sort_values(ascending=False)
pay = [(k, round(v, 2)) for k, v in _pay.items()]

_coords = {"Delhi": (77.2, 28.6), "Chandigarh": (76.8, 30.7), "Lucknow": (80.9, 26.8),
           "Bengaluru": (77.6, 12.97), "Chennai": (80.3, 13.1), "Hyderabad": (78.5, 17.4),
           "Kolkata": (88.4, 22.6), "Patna": (85.1, 25.6), "Bhubaneswar": (85.8, 20.3),
           "Mumbai": (72.9, 19.1), "Pune": (73.9, 18.5), "Ahmedabad": (72.6, 23.0),
           "Bhopal": (77.4, 23.3), "Nagpur": (79.1, 21.1), "Raipur": (81.6, 21.25)}
_city_rev = (df[df.City != "Unknown"].groupby("City")["Net_Revenue"].sum() / LAKH)
_city_reg = df.groupby("City")["Region"].agg(lambda s: s.mode().iloc[0])
cities = sorted([(c, _city_reg[c], round(v, 2), *_coords[c]) for c, v in _city_rev.items()],
                key=lambda t: -t[2])
n_cities = len(cities)

def _badge(p):
    return (f"▲ {abs(p):.1f}%", GREEN, "#e3f4ea") if p >= 0 else (f"▼ {abs(p):.1f}%", RED, "#fde8e8")

# very rough India outline (lon, lat)
india = [(68.2, 23.7), (70.0, 24.5), (71.0, 27.5), (74.0, 31.0), (74.5, 34.5), (77.0, 35.5),
         (79.0, 33.0), (79.0, 30.5), (81.0, 30.0), (84.0, 28.5), (88.0, 27.5), (88.5, 28.0),
         (92.0, 27.8), (96.0, 29.0), (95.0, 26.5), (93.5, 24.0), (92.5, 22.5), (90.0, 22.0),
         (87.0, 21.5), (85.0, 19.5), (82.0, 16.5), (80.3, 13.5), (80.0, 10.0), (77.5, 8.0),
         (76.0, 10.5), (74.5, 14.0), (73.0, 17.5), (72.8, 20.5), (72.5, 21.5), (70.0, 21.0),
         (69.0, 22.5)]

# ----------------------------------------------------------------- CANVAS
fig = plt.figure(figsize=(12, 15.6), facecolor=BG)
bg = fig.add_axes([0, 0, 1, 1])
bg.set_xlim(0, 1)
bg.set_ylim(0, 1)
bg.axis("off")


def card(x, y, w, h, title=None, sub=None, color=CARD, r=0.006):
    bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=color, ec="#d9e2e6", lw=0.8, mutation_aspect=1.25))
    if title:
        bg.text(x + 0.014, y + h - 0.017, title, fontsize=9.5, weight="bold", color=INK, va="top")
    if sub:
        bg.text(x + 0.014, y + h - 0.033, sub, fontsize=6.5, color=MUTED, va="top")


def ax_at(x, y, w, h):
    a = fig.add_axes([x, y, w, h])
    a.set_facecolor("none")
    for s in a.spines.values():
        s.set_visible(False)
    return a


# ---------------------------------------------------------------- SIDEBAR
bg.add_patch(plt.Rectangle((0, 0), 0.147, 1, fc=NAVY, ec="none"))
bg.add_patch(FancyBboxPatch((0.013, 0.935), 0.03, 0.026, boxstyle="round,pad=0,rounding_size=0.005",
                            fc=PINK, ec="none", mutation_aspect=1.25))
bg.text(0.028, 0.948, "S", color="white", fontsize=13, weight="bold", ha="center", va="center")
bg.text(0.052, 0.954, "Sales Overview", color="white", fontsize=9, weight="bold", va="center")
bg.text(0.052, 0.940, "Amazon Marketplace · India", color="#9fb8bf", fontsize=5.8, va="center")
bg.plot([0.013, 0.134], [0.915, 0.915], color="#2c5663", lw=0.8)
bg.text(0.013, 0.893, "PERIOD", color="#9fb8bf", fontsize=6)
bg.add_patch(FancyBboxPatch((0.013, 0.858), 0.121, 0.026, boxstyle="round,pad=0,rounding_size=0.004",
                            fc="#16505f", ec="#2c5663", mutation_aspect=1.25))
bg.text(0.022, 0.871, "Jan 2023 - Dec 2024", color="white", fontsize=6.5, va="center")
bg.text(0.126, 0.871, "▾", color="white", fontsize=7, va="center", ha="center")
bg.plot([0.013, 0.134], [0.835, 0.835], color="#2c5663", lw=0.8)
bg.text(0.013, 0.815, "AT A GLANCE", color="#9fb8bf", fontsize=6)

for i, (v, l) in enumerate([(f"{total_orders:,}", "total orders"), (str(n_cities), "cities covered"), (f"{buyers:,}", "unique buyers")]):
    yy = 0.785 - i * 0.045
    bg.text(0.013, yy, v, color="white", fontsize=12, weight="bold", va="center")
    bg.text(0.013, yy - 0.016, l, color="#9fb8bf", fontsize=6, va="center")

bg.add_patch(FancyBboxPatch((0.013, 0.025), 0.121, 0.045, boxstyle="round,pad=0,rounding_size=0.004",
                            fc="none", ec="#2c5663", mutation_aspect=1.25))
bg.text(0.0735, 0.0475, f"Data compiled from order-level\nrecords, {total_orders:,} rows.", color="#9fb8bf",
        fontsize=5.5, ha="center", va="center")

# ----------------------------------------------------------------- HEADER
bg.text(0.165, 0.968, "Sales Performance Overview", fontsize=13, weight="bold", color=INK, va="center")
bg.text(0.165, 0.952, "Revenue, fulfillment & geographic performance across the marketplace",
        fontsize=6.5, color=MUTED, va="center")
bg.add_patch(FancyBboxPatch((0.70, 0.945), 0.285, 0.027, boxstyle="round,pad=0,rounding_size=0.005",
                            fc=CARD, ec="#d9e2e6", mutation_aspect=1.25))
bg.text(0.842, 0.9585, "Currency: INR (₹)  ·  Jan 2023 - Dec 2024", fontsize=6.3,
        color=MUTED, ha="center", va="center")

# --------------------------------------------------------------- KPI CARDS
kx = [0.16, 0.358, 0.556, 0.754]
kw, ky, kh = 0.19, 0.835, 0.092
kpis = [("Net revenue", f"₹{net_rev_cr:.2f}Cr", _badge(rev_yoy), PINK, "rev"),
        ("Total orders", f"{total_orders:,}", _badge(ord_yoy), TEAL, "ord"),
        ("Avg order value", f"₹{aov:,.0f}", ("per order", MUTED, "none"), PINK, "rev"),
        ("Completion rate", f"{completion}%", (f"{returned_pct:.0f}% returned", MUTED, "none"), None, "")]

for x, (t, v, (btxt, bcol, bfc), col, kind) in zip(kx, kpis):
    card(x, ky, kw, kh)
    bg.text(x + 0.012, ky + kh - 0.014, t, fontsize=6.8, color=INK, va="top")
    bg.text(x + 0.012, ky + kh - 0.036, v, fontsize=15, weight="bold", color=INK, va="top")
    bg.text(x + kw - 0.012, ky + kh - 0.014, btxt, fontsize=5.8, color=bcol, ha="right", va="top",
            bbox=dict(fc=bfc, ec="none", pad=2.2) if bfc != "none" else None)
    if col:
        a = ax_at(x + 0.012, ky + 0.008, kw - 0.024, 0.032)
        data = m_rev if kind == "rev" else m_orders
        a.bar(range(24), data - data.min() * 0.85, color=col, width=0.55)
        a.axis("off")
    else:
        a = ax_at(x + 0.08, ky + 0.008, 0.095, 0.036)
        a.axis("off")
        for i, (lab, val, c) in enumerate([("Done", status[0][1], GREEN), ("Returned", status[1][1], RED),
                                           ("Cancelled", status[2][1], GRAY)]):
            a.barh(2 - i, val, color=c, height=0.55)
            bg.text(x + 0.076, ky + 0.008 + 0.036 * (2 - i + 0.5) / 3, lab, fontsize=4.8,
                    color=MUTED, ha="right", va="center")
        a.set_xlim(0, 60)
        a.set_ylim(-0.5, 2.5)

# -------------------------------------------------- 1. CATEGORY PERFORMANCE
cx, cy, cw, ch = 0.16, 0.612, 0.372, 0.205
card(cx, cy, cw, ch, "Category performance", "Revenue, orders and rating by category")
a = ax_at(cx + 0.014, cy + 0.01, cw - 0.028, 0.14)
a.axis("off")
a.set_xlim(0, 1)
a.set_ylim(-0.5, 8.4)
hx = dict(fontsize=5.8, color=MUTED, va="center")
a.text(0, 8.1, "Category", **hx)
a.text(0.73, 8.1, "Revenue", ha="right", **hx)
a.text(0.87, 8.1, "Orders", ha="right", **hx)
a.text(1.0, 8.1, "Rating", ha="right", **hx)

for i, (c, r, o, g) in enumerate(zip(categories, cat_rev, cat_orders, cat_rating)):
    y = 7 - i
    a.text(0, y, c, fontsize=6.3, color=INK, va="center")
    a.add_patch(plt.Rectangle((0.25, y - 0.12), 0.30, 0.24, fc="#e6ecef", ec="none"))
    a.add_patch(plt.Rectangle((0.25, y - 0.12), 0.30 * r / max(cat_rev), 0.24, fc=PINK, ec="none"))
    a.text(0.73, y, f"₹{r:.2f}L", fontsize=6.3, color=INK, ha="right", va="center")
    a.text(0.87, y, f"{o:,}", fontsize=6.3, color=INK, ha="right", va="center")
    a.text(1.0, y, f"{g}", fontsize=6.3, color=INK, ha="right", va="center")

# --------------------------------------------------------- 2. ORDER STATUS
sx, sw = 0.548, 0.437
card(sx, cy, sw, ch, "Order status", f"Share of {total_orders:,} total orders")
a = ax_at(sx + 0.09, cy + 0.035, 0.26, 0.135)
a.set_aspect("equal")
a.axis("off")
a.set_xlim(-1.1, 1.1)
a.set_ylim(-1.1, 1.1)
ang = 90

for lab, val, c in status:
    span = val / sum(s[1] for s in status) * 360
    a.add_patch(Wedge((0, 0), 1, ang - span, ang, width=0.33, fc=c, ec="white", lw=1.5))
    ang -= span

a.text(0, 0.1, f"{completion}%", ha="center", va="center", fontsize=13, weight="bold", color=INK)
a.text(0, -0.2, "delivered", ha="center", va="center", fontsize=6, color=MUTED)

for i, (lab, val, c) in enumerate(status):
    lx = sx + 0.014 + i * 0.1
    bg.add_patch(plt.Rectangle((lx, cy + 0.016), 0.006, 0.01, fc=c, ec="none"))
    bg.text(lx + 0.009, cy + 0.021, f"{lab} {val}%", fontsize=5.5, color=MUTED, va="center")

# ------------------------------------------------ 3. MONTHLY VOLUME/REVENUE
mx, my, mw, mh = 0.16, 0.388, 0.825, 0.207
card(mx, my, mw, mh, "Monthly order volume & revenue", "Jan 2023 through Dec 2024")

for i, (lab, c) in enumerate([("Net revenue", PINK), ("Orders", LTEAL)]):
    lx = 0.855 + i * 0.07
    bg.add_patch(plt.Rectangle((lx, my + mh - 0.024), 0.007, 0.01, fc=c, ec="none"))
    bg.text(lx + 0.01, my + mh - 0.019, lab, fontsize=6, color=MUTED, va="center")

a = ax_at(mx + 0.045, my + 0.045, mw - 0.06, 0.115)
a.bar(range(24), m_orders, color=LTEAL, width=0.6)
a.set_ylim(0, m_orders.max() * 1.1)
a.set_yticks([])

a2 = a.twinx()
a2.spines[:].set_visible(False)
a2.plot(range(24), m_rev, color=PINK, lw=1.4, marker="o", ms=3)
_lo, _hi = np.floor(m_rev.min() * 2) / 2, np.ceil(m_rev.max() * 2) / 2
a2.set_ylim(_lo - 0.2, _hi + 0.2)
a2.yaxis.set_label_position("left")
a2.yaxis.tick_left()
_ticks = np.arange(_lo, _hi + 0.1, 0.5)
a2.set_yticks(_ticks)
a2.set_yticklabels([f"₹{v:.1f}L" for v in _ticks],
                   fontsize=5.5, color=MUTED)
a2.tick_params(length=0)

a.set_xticks(range(24))
a.set_xticklabels(months, rotation=90, fontsize=5, color=MUTED)
a.tick_params(length=0)
a.set_xlim(-0.6, 23.6)

# ------------------------------------------- 4. CATEGORY REVENUE BY QUARTER
hx0, hy, hw, hh = 0.16, 0.167, 0.372, 0.207
card(hx0, hy, hw, hh, "Category revenue by quarter", "Darker = higher revenue")
a = ax_at(hx0 + 0.11, hy + 0.012, hw - 0.12, 0.15)
cmap = LinearSegmentedColormap.from_list("h", [LTEAL, "#b9a9c4", PINK])
a.imshow(heat, cmap=cmap, aspect="auto")
a.set_xticks(range(8))
a.xaxis.tick_top()
a.set_xticklabels(["Q1 '23", "Q2 '23", "Q3 '23", "Q4 '23", "Q1 '24", "Q2 '24", "Q3 '24", "Q4 '24"],
                  fontsize=5, color=MUTED)
a.set_yticks(range(8))
a.set_yticklabels(categories, fontsize=5.8, color=INK)
a.tick_params(length=0)

for i in range(8):
    for j in range(8):
        a.text(j, i, f"₹{heat[i, j]:.1f}L", ha="center", va="center", fontsize=4.8,
               color="white" if heat[i, j] > 5.5 else INK)

for k in range(9):
    a.axhline(k - 0.5, color="white", lw=1)
    a.axvline(k - 0.5, color="white", lw=1)

# ------------------------------------------------------ 5. PAYMENT MODE SHARE
px = 0.548
card(px, hy, sw, hh, "Payment mode share", "By net revenue")
a = ax_at(px + 0.12, hy + 0.03, 0.27, 0.13)
names = [p[0] for p in pay][::-1]
vals = [p[1] for p in pay][::-1]
cols = [GRAY if n == "Unknown" else "#f4b6cf" for n in names]
a.barh(names, vals, color=cols, height=0.6)

for i, v in enumerate(vals):
    a.text(v + 0.8, i, f"₹{v:.2f}L", fontsize=5.8, color=INK, va="center")

a.set_xlim(0, 55)
a.set_xticks([])
a.tick_params(length=0, labelsize=5.8, labelcolor=MUTED)
a.spines["left"].set_visible(True)
a.spines["left"].set_color("#d9e2e6")

# ------------------------------------------------------- 6. REVENUE BY CITY
rx, ry, rw, rh = 0.16, 0.012, 0.825, 0.147
card(rx, ry, rw, rh, "Revenue by city — India", f"Bubble size & colour scale with net revenue · {n_cities} cities plotted")
a = ax_at(rx + 0.012, ry + 0.022, 0.16, 0.088)
a.set_aspect("equal")
a.axis("off")
a.add_patch(Polygon(india, closed=True, fc="#f1f3f4", ec="#d5dadd", lw=0.8))
a.set_xlim(66, 98)
a.set_ylim(6, 37)

cm = LinearSegmentedColormap.from_list("c", ["#dcc9d2", PINK])
rvals = np.array([c[2] for c in cities])
nrm = (rvals - rvals.min()) / np.ptp(rvals)

for c, n in zip(cities, nrm):
    a.scatter(c[3], c[4], s=25 + 140 * n, color=cm(n), alpha=0.85, ec="white", lw=0.6)

bg.add_patch(Circle((rx + 0.016, ry + 0.012), 0.003, fc="#dcc9d2", ec="none"))
bg.text(rx + 0.022, ry + 0.012, "lower revenue", fontsize=5, color=MUTED, va="center")
bg.add_patch(Circle((rx + 0.075, ry + 0.012), 0.003, fc=PINK, ec="none"))
bg.text(rx + 0.081, ry + 0.012, "higher revenue", fontsize=5, color=MUTED, va="center")

order = sorted(cities, key=lambda c: -c[2])

for k, c in enumerate(order):
    col = k // 8
    row = k % 8
    x0 = rx + 0.20 + col * 0.31
    y0 = ry + rh - 0.055 - row * 0.0128
    n = (c[2] - rvals.min()) / np.ptp(rvals)
    bg.add_patch(Circle((x0, y0), 0.0035, fc=cm(n), ec="none"))
    bg.text(x0 + 0.012, y0, c[0], fontsize=6.3, weight="bold", color=INK, va="center")
    bg.text(x0 + 0.075, y0, c[1], fontsize=5.3, color=MUTED, va="center")
    bg.text(x0 + 0.29 - 0.02, y0, f"₹{c[2]:.2f}L", fontsize=6.3, color=INK, ha="right", va="center")

bg.text(0.985, 0.004, "Source: amazon_sales_clean.csv",
        fontsize=5, color=MUTED, ha="right", va="bottom")

# ---------------------------------------------------------------- SAVE
plt.savefig(os.path.join(_HERE, "sales_dashboard.png"), dpi=170, facecolor=BG)
print("Saved sales_dashboard.png")
plt.show()
