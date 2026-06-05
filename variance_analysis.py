"""
variance_analysis.py
--------------------
Automates Budget vs Actual variance analysis with waterfall charts
and plain-English commentary generation.

Built by: Arjun D | Finance Head | ACCA DipIFR
Use case: Replaces manual monthly CFO-pack variance commentary in Excel
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from io import StringIO


SAMPLE_DATA = """
Category,Budget,Actual
Revenue,5000000,5350000
Cost of Goods Sold,-3000000,-3100000
Gross Profit,2000000,2250000
Salaries,-600000,-650000
Rent,-120000,-120000
Marketing,-200000,-180000
Professional Fees,-80000,-95000
Technology,-100000,-115000
Travel,-50000,-30000
EBITDA,850000,1060000
Depreciation,-150000,-155000
EBIT,700000,905000
Interest Expense,-80000,-75000
PBT,620000,830000
Tax,-186000,-249000
PAT,434000,581000
"""


def load_data(csv_string=None, filepath=None):
    if filepath:
        return pd.read_csv(filepath)
    return pd.read_csv(StringIO(csv_string))


def calculate_variances(df):
    df = df.copy()
    df["Variance"] = df["Actual"] - df["Budget"]
    df["Variance_%"] = ((df["Actual"] - df["Budget"]) / df["Budget"].abs()) * 100
    df["Favourable"] = __import__('numpy').where(
        df["Budget"] >= 0,
        df["Variance"] >= 0,
        df["Variance"] <= 0,
    )
    return df


def generate_commentary(df, threshold_pct=5.0):
    lines = ["=== VARIANCE COMMENTARY ==="]
    material = df[df["Variance_%"].abs() >= threshold_pct].copy()
    for _, row in material.iterrows():
        direction = "favourable" if row["Favourable"] else "adverse"
        sign = "+" if row["Variance"] > 0 else ""
        lines.append(f"  {row['Category']:30s} | {sign}{row['Variance']:>12,.0f} ({sign}{row['Variance_%']:.1f}%) - {direction.upper()}")
    return "\n".join(lines)


def waterfall_chart(df, save_path=None):
    import matplotlib.pyplot as plt
    import numpy as np
    colors = ["#27AE60" if f else "#E74C3C" for f in df["Favourable"]]
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    x = np.arange(len(df))
    axes[0].bar(x - 0.175, df["Budget"], 0.35, label="Budget", color="#2C3E50", alpha=0.8)
    axes[0].bar(x + 0.175, df["Actual"], 0.35, label="Actual", color="#3498DB", alpha=0.8)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(df["Category"], rotation=45, ha="right", fontsize=8)
    axes[0].legend()
    axes[1].barh(df["Category"], df["Variance"], color=colors)
    axes[1].axvline(0, color="black", linewidth=1)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.close()


if __name__ == "__main__":
    df = load_data(csv_string=SAMPLE_DATA)
    df = calculate_variances(df)
    print(generate_commentary(df))
    waterfall_chart(df, save_path="variance_chart.png")
    print("Chart saved: variance_chart.png")
