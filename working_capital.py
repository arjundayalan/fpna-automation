"""
working_capital.py
------------------
Working capital metrics calculator: DSO, DPO, DIO, Cash Conversion Cycle.
Built by: Arjun D
Real-world context: At Cotton World Group drove DSO from 90 to 30 days.
"""

import pandas as pd
import matplotlib.pyplot as plt


def calculate_dso(accounts_receivable, revenue, days=365):
    return (accounts_receivable / revenue) * days

def calculate_dpo(accounts_payable, cogs, days=365):
    return (accounts_payable / cogs) * days

def calculate_dio(inventory, cogs, days=365):
    return (inventory / cogs) * days

def cash_conversion_cycle(dso, dpo, dio):
    """CCC = DIO + DSO - DPO. Lower (or negative) = better."""
    return dio + dso - dpo

def working_capital_ratio(current_assets, current_liabilities):
    return current_assets / current_liabilities

def analyse_trend(periods):
    rows = []
    for p in periods:
        dso = calculate_dso(p['accounts_receivable'], p['revenue'])
        dpo = calculate_dpo(p['accounts_payable'], p['cogs'])
        dio = calculate_dio(p['inventory'], p['cogs'])
        ccc = cash_conversion_cycle(dso, dpo, dio)
        wcr = working_capital_ratio(p['current_assets'], p['current_liabilities'])
        rows.append({'Period': p['period'], 'DSO (days)': round(dso,1),
                     'DPO (days)': round(dpo,1), 'DIO (days)': round(dio,1),
                     'CCC (days)': round(ccc,1), 'WC Ratio': round(wcr,2)})
    return pd.DataFrame(rows)

def plot_wc_trend(df, save_path=None):
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    colors = ['#E74C3C' if v > 0 else '#27AE60' for v in df['CCC (days)']]
    axes[0].bar(df['Period'], df['CCC (days)'], color=colors)
    axes[0].axhline(0, color='black', linewidth=1, linestyle='--')
    axes[0].set_title('Cash Conversion Cycle (lower/negative = better)', fontweight='bold')
    axes[1].plot(df['Period'], df['DSO (days)'], marker='o', label='DSO', color='#E74C3C')
    axes[1].plot(df['Period'], df['DPO (days)'], marker='s', label='DPO', color='#27AE60')
    axes[1].plot(df['Period'], df['DIO (days)'], marker='^', label='DIO', color='#3498DB')
    axes[1].set_title('DSO / DPO / DIO Over Time', fontweight='bold')
    axes[1].legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=150)
    plt.close()

if __name__ == '__main__':
    periods = [
        {'period':'Q1 FY24','revenue':150e6,'cogs':90e6,'accounts_receivable':37.5e6,
         'accounts_payable':12e6,'inventory':22e6,'current_assets':80e6,'current_liabilities':40e6},
        {'period':'Q2 FY24','revenue':160e6,'cogs':95e6,'accounts_receivable':30e6,
         'accounts_payable':14e6,'inventory':20e6,'current_assets':82e6,'current_liabilities':38e6},
        {'period':'Q3 FY24','revenue':165e6,'cogs':98e6,'accounts_receivable':22e6,
         'accounts_payable':16e6,'inventory':18.5e6,'current_assets':85e6,'current_liabilities':36e6},
        {'period':'Q4 FY24','revenue':175e6,'cogs':100e6,'accounts_receivable':14.5e6,
         'accounts_payable':18e6,'inventory':17e6,'current_assets':90e6,'current_liabilities':34e6},
    ]
    df = analyse_trend(periods)
    print(df.to_string(index=False))
    plot_wc_trend(df, save_path='working_capital_trend.png')
    print('Chart saved.')
