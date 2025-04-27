import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Load dataset
df = pd.read_excel("aligned_risk_personal_loans.xlsx")

# Constants
T = 1  # Time horizon in years
r = 0.08  # Risk-free rate (8%)

# Estimate Asset Value (V) and Volatility (sigma_V) using assumptions
df['Asset Value'] = df['Outstanding Amount'] * np.random.uniform(1.1, 1.5, size=len(df))
df['Asset Volatility'] = np.random.uniform(0.15, 0.35, size=len(df))  # 15% to 35%

# Merton Model PD Calculation
def calculate_merton_pd(V, D, sigma_V, r, T):
    if V <= 0 or D <= 0 or sigma_V <= 0:
        return np.nan  # handle invalid values
    try:
        d1 = (np.log(V / D) + (r + 0.5 * sigma_V**2) * T) / (sigma_V * np.sqrt(T))
        d2 = d1 - sigma_V * np.sqrt(T)
        pd = stats.norm.cdf(-d2)
        return pd
    except:
        return np.nan

# Apply the Merton Model
df['Merton_PD'] = df.apply(
    lambda row: calculate_merton_pd(
        row['Asset Value'],
        row['Outstanding Amount'],
        row['Asset Volatility'],
        r,
        T
    ),
    axis=1
)

# Save with PDs
df.to_excel("Merton_PD_Portfolio.xlsx", index=False)

# Visualization 1: Merton PD by Risk Class
plt.figure(figsize=(10, 6))
df.boxplot(column='Merton_PD', by='Risk Class', grid=False)
plt.title("Merton PD by Risk Class")
plt.suptitle("")
plt.xlabel("Risk Class")
plt.ylabel("Probability of Default (PD)")
plt.tight_layout()
plt.savefig("merton_pd_by_risk_class.png")
plt.show()
