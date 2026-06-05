"""
cash_flow_forecast.py
----------------------
13-week rolling direct cash flow forecast.
Built by: Arjun D
Deployed at Ciel Et Terre Solar to give France CFO real-time INR visibility.
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta


def build_forecast(opening_cash, inflows, outflows, weeks=13, start_date=None):
    if start_date is None:
        start_date = date.today()
    records = []
    cash = opening_cash
    for i in range(weeks):
        win = inflows[i] if i < len(inflows) else 0
        wout = outflows[i] if i < len(outflows) else 0
        net = win - wout
        cash += net
        records.append({"Week": i+1, "Date": str(start_date + timedelta(weeks=i)),
                         "Inflows": win, "Outflows": wout, "Net": net, "Cash": cash})
    return pd.DataFrame(records)


def plot_forecast(df, opening, save_path=None):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    x = df["Week"]
    axes[0].bar(x-0.2, df["Inflows"]/1e6, 0.4, label="Inflows", color="#27AE60")
    axes[0].bar(x+0.2, df["Outflows"]/1e6, 0.4, label="Outflows", color="#E74C3C")
    axes[0].set_title("13-Week Cash Flow: Inflows vs Outflows", fontweight="bold")
    axes[0].legend()
    axes[1].plot(x, df["Cash"]/1e6, marker="o", color="#2C3E50", linewidth=2)
    axes[1].axhline(0, color="#E74C3C", linewidth=0.8)
    axes[1].axhline(opening/1e6, color="#95A5A6", linestyle="--", label="Opening")
    axes[1].set_title("Cumulative Cash Position (13 Weeks)", fontweight="bold")
    axes[1].legend()
    plt.tight_layout()
    if save_path: plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.close()


if __name__ == "__main__":
    opening = 25_000_000
    inflows  = [8.5e6,9.2e6,7.8e6,10.5e6,8e6,9.8e6,11.2e6,7.5e6,9e6,10.8e6,8.2e6,9.5e6,11e6]
    outflows = [7.2e6,8.1e6,9.5e6,7.8e6,8.5e6,7.2e6,8.8e6,9.2e6,7.5e6,8.1e6,9e6,7.8e6,8.2e6]
    df = build_forecast(opening, inflows, outflows)
    print(df.to_string(index=False))
    print(f"Min cash: {df[\"Cash\"].min():,.0f}")
    plot_forecast(df, opening, save_path="cash_flow_forecast.png")
    print("Chart saved.")
