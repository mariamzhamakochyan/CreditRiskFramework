# Stress_Testing.py

import pandas as pd
import matplotlib.pyplot as plt

# Load your Excel file
file_path = "aligned_risk_personal_loans.xlsx"
df = pd.read_excel(file_path)

# Rename columns to standard names if needed
rename_map = {
    'Exposure at Default (EAD)': 'EAD',
    'Probability of Default (PD)': 'PD',
    'Loss Given Default (LGD)': 'LGD',
    'Loan Number': 'Loan Number'
}
df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

# Ensure all required columns exist
required_columns = ['EAD', 'PD', 'LGD']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns in data: {missing_columns}")

# Define stress scenarios as multipliers for PD and LGD
scenarios = {
    'Base': (1.0, 1.0),
    'Mild Stress': (1.2, 1.1),
    'Moderate Stress': (1.5, 1.3),
    'Severe Stress': (2.0, 1.5)
}

# Calculate total expected loss under each scenario
results = {}

for scenario, (pd_mult, lgd_mult) in scenarios.items():
    stressed_PD = df['PD'] * pd_mult
    stressed_LGD = df['LGD'] * lgd_mult

    stressed_EL = df['EAD'] * stressed_PD * stressed_LGD
    total_EL = stressed_EL.sum()

    results[scenario] = total_EL

# Visualization
plt.figure(figsize=(10, 6))
bars = plt.bar(results.keys(), results.values(), color=["green", "gold", "orange", "red"])
plt.title("Stress Testing: Total Expected Loss by Scenario", fontsize=14)
plt.xlabel("Stress Scenario")
plt.ylabel("Total Expected Loss (AMD)")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels to bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f"{height:,.0f}", ha='center', va='bottom')

plt.tight_layout()
plt.show()

