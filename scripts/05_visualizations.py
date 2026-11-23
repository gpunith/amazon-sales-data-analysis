"""
Six dashboard charts - every value is computed from amazon_sales_clean.csv.
Run:  python 05_visualizations.py   (also works in Jupyter)
Each chart is saved as its own PNG next to this script.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Polygon, Circle
from matplotlib.colors import LinearSegmentedColormap

PINK, LTEAL, INK, MUTED = "#e0457b", "#b8dfe3", "#1d2b33", "#7b8790"
GREEN, RED, GRAY, AMBER = "#2e9e5b", "#d9534f", "#9aa5b1", "#e8a838"

# =====================================================
# LOAD DATA + COMPUTE EVERYTHING
# =====================================================
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:                      # Jupyter
    HERE = os.getcwd()
CANDIDATES = [os.path.join(HERE, "amazon_sales_clean.csv"),
              os.path.join(HERE, "data", "amazon_sales_clean.csv"),
              os.path.join(HERE, "..", "data", "amazon_sales_clean.csv"),
              os.path.join(os.getcwd(), "amazon_sales_clean.csv")]
CSV = next((p for p in CANDIDATES if os.path.exists(p)), None)
if CSV is None:
    raise FileNotFoundError("amazon_sales_clean.csv not found. Looked in:\n" + "\n".join(CANDIDATES))
df = pd.read_csv(CSV, parse_dates=["Order_Date"])
LAKH = 1e5

def save(name):
    plt.savefig(os.path.join(HERE, name), dpi=170)

# 1 category performance
_cat = (df.groupby("Category")
          .agg(rev=("Net_Revenue", lambda s: s.sum() / LAKH), orders=("Order_ID", "count"),
               rating=("Rating", "mean"))
          .sort_values("rev", ascending=False))
categories = list(_cat.index)
revenue = [round(v, 2) for v in _cat["rev"]]
orders_by_cat = [int(v) for v in _cat["orders"]]
rating = [round(v, 1) for v in _cat["rating"]]

# 2 order status
_st = df["Order_Status"].value_counts(normalize=True) * 100
status = [(s, round(_st[s], 1), c) for s, c in
          [("Delivered", GREEN), ("Returned", RED), ("Cancelled", GRAY), ("Pending", AMBER)]]
total_orders = len(df)

# 3 monthly
_mon = (df.groupby(["Year", "Month"])
          .agg(o=("Order_ID", "count"), r=("Net_Revenue", lambda s: s.sum() / LAKH))
          .reindex([(y, m) for y in (2023, 2024) for m in range(1, 13)]))
months = [f"{m}-{y}" for y in ("23", "24") for m in
          ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")]
m_orders = _mon["o"].fillna(0).to_numpy()
m_rev = _mon["r"].fillna(0).to_numpy()

# 4 heatmap (category x quarter)
quarters = ["Q1 '23", "Q2 '23", "Q3 '23", "Q4 '23", "Q1 '24", "Q2 '24", "Q3 '24", "Q4 '24"]
heat = (df.pivot_table(index="Category", columns=["Year", "Quarter"], values="Net_Revenue", aggfunc="sum")
          .reindex(categories).fillna(0) / LAKH).to_numpy()

# 5 payment
_pay = (df.groupby("Payment_Mode")["Net_Revenue"].sum() / LAKH).sort_values(ascending=False)
pay = [(k, round(v, 2)) for k, v in _pay.items()]

# 6 cities (lon, lat are fixed map coordinates)
_coords = {"Delhi": (77.2, 28.6), "Chandigarh": (76.8, 30.7), "Lucknow": (80.9, 26.8),
           "Bengaluru": (77.6, 12.97), "Chennai": (80.3, 13.1), "Hyderabad": (78.5, 17.4),
           "Kolkata": (88.4, 22.6), "Patna": (85.1, 25.6), "Bhubaneswar": (85.8, 20.3),
           "Mumbai": (72.9, 19.1), "Pune": (73.9, 18.5), "Ahmedabad": (72.6, 23.0),
           "Bhopal": (77.4, 23.3), "Nagpur": (79.1, 21.1), "Raipur": (81.6, 21.25)}
_city_rev = df[df.City != "Unknown"].groupby("City")["Net_Revenue"].sum() / LAKH
_city_reg = df.groupby("City")["Region"].agg(lambda s: s.mode().iloc[0])
cities = sorted([(c, _city_reg[c], round(v, 2), *_coords[c]) for c, v in _city_rev.items()],
                key=lambda t: -t[2])
india = [(68.2, 23.7), (70.0, 24.5), (71.0, 27.5), (74.0, 31.0), (74.5, 34.5), (77.0, 35.5),
         (79.0, 33.0), (79.0, 30.5), (81.0, 30.0), (84.0, 28.5), (88.0, 27.5), (88.5, 28.0),
         (92.0, 27.8), (96.0, 29.0), (95.0, 26.5), (93.5, 24.0), (92.5, 22.5), (90.0, 22.0),
         (87.0, 21.5), (85.0, 19.5), (82.0, 16.5), (80.3, 13.5), (80.0, 10.0), (77.5, 8.0),
         (76.0, 10.5), (74.5, 14.0), (73.0, 17.5), (72.8, 20.5), (72.5, 21.5), (70.0, 21.0),
         (69.0, 22.5)]   # rough outline


# =====================================================
# 1. CATEGORY PERFORMANCE
# =====================================================
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.set_xlim(0, 1); ax.set_ylim(-0.5, 8.4); ax.axis("off")
ax.set_title("Category performance", loc="left", fontsize=12, weight="bold", color=INK)
for x, t, ha in [(0, "Category", "left"), (0.73, "Revenue", "right"),
                 (0.87, "Orders", "right"), (1.0, "Rating", "right")]:
    ax.text(x, 8.1, t, fontsize=8, color=MUTED, ha=ha, va="center")
for i, (c, r, o, g) in enumerate(zip(categories, revenue, orders_by_cat, rating)):
    y = 7 - i
    ax.text(0, y, c, fontsize=9, color=INK, va="center")
    ax.add_patch(plt.Rectangle((0.25, y - 0.12), 0.30, 0.24, fc="#e6ecef", ec="none"))
    ax.add_patch(plt.Rectangle((0.25, y - 0.12), 0.30 * r / max(revenue), 0.24, fc=PINK, ec="none"))
    ax.text(0.73, y, f"₹{r:.2f}L", fontsize=9, ha="right", va="center", color=INK)
    ax.text(0.87, y, f"{o:,}", fontsize=9, ha="right", va="center", color=INK)
    ax.text(1.0, y, f"{g}", fontsize=9, ha="right", va="center", color=INK)
plt.tight_layout(); save("1_category_performance.png")

# =====================================================
# 2. ORDER STATUS
# =====================================================
fig, ax = plt.subplots(figsize=(5.5, 5))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.4, 1.1)
ax.set_title(f"Order status\nShare of {total_orders:,} total orders", loc="left",
             fontsize=11, weight="bold", color=INK)
angle, total = 90, sum(s[1] for s in status)
for _, val, col in status:
    span = val / total * 360
    ax.add_patch(Wedge((0, 0), 1, angle - span, angle, width=0.33, fc=col, ec="white", lw=2))
    angle -= span
ax.text(0, 0.08, f"{status[0][1]}%", ha="center", va="center", fontsize=20, weight="bold", color=INK)
ax.text(0, -0.2, "delivered", ha="center", va="center", fontsize=9, color=MUTED)
for i, (lab, val, col) in enumerate(status):
    x = -1.05 + (i % 2) * 1.1; y = -1.2 - (i // 2) * 0.15
    ax.add_patch(plt.Rectangle((x, y - 0.04), 0.07, 0.08, fc=col, ec="none"))
    ax.text(x + 0.1, y, f"{lab} {val}%", fontsize=8, color=MUTED, va="center")
plt.tight_layout(); save("2_order_status.png")

# =====================================================
# 3. MONTHLY ORDER VOLUME & REVENUE
# =====================================================
fig, ax = plt.subplots(figsize=(12, 4.2))
ax.bar(range(24), m_orders, color=LTEAL, width=0.6, label="Orders")
ax.set_ylim(0, m_orders.max() * 1.1); ax.set_yticks([])
ax2 = ax.twinx()
ax2.plot(range(24), m_rev, color=PINK, lw=1.8, marker="o", ms=4, label="Net revenue")
lo, hi = np.floor(m_rev.min() * 2) / 2, np.ceil(m_rev.max() * 2) / 2
ax2.set_ylim(lo - 0.2, hi + 0.2)
ax2.yaxis.tick_left(); ax2.yaxis.set_label_position("left")
ticks = np.arange(lo, hi + 0.1, 0.5)
ax2.set_yticks(ticks); ax2.set_yticklabels([f"₹{t:.1f}L" for t in ticks], fontsize=8, color=MUTED)
for a in (ax, ax2):
    a.spines[:].set_visible(False); a.tick_params(length=0)
ax.set_xticks(range(24)); ax.set_xticklabels(months, rotation=90, fontsize=8, color=MUTED)
ax.set_title("Monthly order volume & revenue\nJan 2023 through Dec 2024", loc="left",
             fontsize=12, weight="bold", color=INK)
h1, l1 = ax2.get_legend_handles_labels(); h2, l2 = ax.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper right", frameon=False, ncol=2, fontsize=8)
plt.tight_layout(); save("3_monthly_volume_revenue.png")

# =====================================================
# 4. CATEGORY REVENUE BY QUARTER
# =====================================================
cmap = LinearSegmentedColormap.from_list("h", ["#b8dfe3", "#b9a9c4", "#e0457b"])
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.imshow(heat, cmap=cmap, aspect="auto")
ax.xaxis.tick_top()
ax.set_xticks(range(8)); ax.set_xticklabels(quarters, fontsize=8, color=MUTED)
ax.set_yticks(range(8)); ax.set_yticklabels(categories, fontsize=9, color=INK)
ax.tick_params(length=0)
_mid = (heat.min() + heat.max()) / 2.6
for i in range(8):
    for j in range(8):
        ax.text(j, i, f"₹{heat[i, j]:.1f}L", ha="center", va="center", fontsize=7,
                color="white" if heat[i, j] > _mid else INK)
for k in range(9):
    ax.axhline(k - 0.5, color="white", lw=1.5); ax.axvline(k - 0.5, color="white", lw=1.5)
for s in ax.spines.values(): s.set_visible(False)
fig.suptitle("Category revenue by quarter  (darker = higher revenue)", x=0.02, ha="left",
             fontsize=12, weight="bold", color=INK)
plt.tight_layout(); save("4_category_revenue_by_quarter.png")

# =====================================================
# 5. PAYMENT MODE SHARE
# =====================================================
names = [p[0] for p in pay][::-1]; vals = [p[1] for p in pay][::-1]
colors = ["#9aa5b1" if n == "Unknown" else "#f4b6cf" for n in names]
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(names, vals, color=colors, height=0.6)
for i, v in enumerate(vals):
    ax.text(v + 0.8, i, f"₹{v:.2f}L", fontsize=9, color=INK, va="center")
ax.set_xlim(0, max(vals) * 1.2); ax.set_xticks([])
ax.tick_params(length=0, labelsize=9, labelcolor=MUTED)
for s in ("top", "right", "bottom"): ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#d9e2e6")
ax.set_title("Payment mode share\nBy net revenue", loc="left", fontsize=12, weight="bold", color=INK)
plt.tight_layout(); save("5_payment_mode_share.png")

# =====================================================
# 6. REVENUE BY CITY
# =====================================================
cmap_c = LinearSegmentedColormap.from_list("c", ["#dcc9d2", PINK])
rev = np.array([c[2] for c in cities]); nrm = (rev - rev.min()) / np.ptp(rev)
fig, (axm, axl) = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={"width_ratios": [1, 1.6]})
axm.add_patch(Polygon(india, closed=True, fc="#f1f3f4", ec="#d5dadd", lw=1))
for c, n in zip(cities, nrm):
    axm.scatter(c[3], c[4], s=60 + 300 * n, color=cmap_c(n), alpha=0.85, ec="white", lw=0.8)
axm.set_xlim(66, 98); axm.set_ylim(6, 37); axm.set_aspect("equal"); axm.axis("off")
axl.axis("off"); axl.set_xlim(0, 2); axl.set_ylim(0, 8.5)
for k, c in enumerate(cities):
    col, row = k // 8, k % 8
    x0, y = col * 1.0, 7.8 - row
    n = nrm[k]
    axl.add_patch(Circle((x0 + 0.04, y), 0.07, fc=cmap_c(n), ec="none"))
    axl.text(x0 + 0.12, y, c[0], fontsize=9, weight="bold", color=INK, va="center")
    axl.text(x0 + 0.48, y, c[1], fontsize=7, color=MUTED, va="center")
    axl.text(x0 + 0.92, y, f"₹{c[2]:.2f}L", fontsize=9, color=INK, ha="right", va="center")
fig.suptitle(f"Revenue by city — India\nBubble size & colour scale with net revenue · {len(cities)} cities plotted",
             x=0.02, ha="left", fontsize=12, weight="bold", color=INK)
plt.tight_layout(); save("6_revenue_by_city.png")

plt.show()
