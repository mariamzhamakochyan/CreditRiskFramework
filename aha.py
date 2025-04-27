import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the portfolio
df = pd.read_excel('aligned_risk_personal_loans.xlsx')

# Risk Weights for Basel II and III (Armenian bank logic)
risk_weights = {
    '1': 0.5,   # 50%
    '2': 0.75,  # 75%
    '3': 1.0,   # 100%
    '4': 1.5,   # 150%
    '5': 2.0    # 200%
}

def calculate_capital_requirements(df, risk_weights):
    df['Risk Weight'] = df['Risk Class'].map(risk_weights)
    df['Basel II Capital'] = df['Outstanding Amount'] * df['Risk Weight'] * 0.08
    df['Basel III Capital'] = df['Outstanding Amount'] * df['Risk Weight'] * 0.10
    total_basel2 = df['Basel II Capital'].sum()
    total_basel3 = df['Basel III Capital'].sum()
    return total_basel2, total_basel3

# ---- STEP 1: Calculate current (unstressed) requirements ----
total_basel2_before, total_basel3_before = calculate_capital_requirements(df, risk_weights)

# ---- STEP 2: Stress Test ----
def stress_test(df_original):
    df_stressed = df_original.copy()
    
    # 1. Increase PD by +5% (0.05)
    df_stressed['PD'] = np.clip(df_stressed['PD'] + 0.05, 0, 1)

    # 2. Increase LGD by +10% (0.10)
    df_stressed['LGD'] = np.clip(df_stressed['LGD'] + 0.10, 0, 1)

    # 3. Downgrade Risk Class
    downgrade_map = {'1': '2', '2': '3', '3': '4', '4': '5', '5': '5'}
    df_stressed['Risk Class'] = df_stressed['Risk Class'].replace(downgrade_map)

    return df_stressed

# Apply Stress Test
df_stressed = stress_test(df)

# Recalculate after stress
total_basel2_after, total_basel3_after = calculate_capital_requirements(df_stressed, risk_weights)

# ---- STEP 3: Print the Results ----
print(f"✅ Total Basel II Capital Requirement BEFORE Stress: {total_basel2_before:,.0f} AMD")
print(f"✅ Total Basel II Capital Requirement AFTER Stress:  {total_basel2_after:,.0f} AMD\n")
print(f"✅ Total Basel III Capital Requirement BEFORE Stress: {total_basel3_before:,.0f} AMD")
print(f"✅ Total Basel III Capital Requirement AFTER Stress:  {total_basel3_after:,.0f} AMD")

# ---- STEP 4: Visualization ----
labels = ['Basel II', 'Basel III']
before = [total_basel2_before, total_basel3_before]
after = [total_basel2_after, total_basel3_after]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8,6))
bars1 = ax.bar(x - width/2, before, width, label='Before Stress')
bars2 = ax.bar(x + width/2, after, width, label='After Stress')

ax.set_ylabel('Capital Requirement (AMD)')
ax.set_title('Basel II & III Capital Requirements Before and After Stress Test')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:,.0f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=8)

plt.grid(axis='y')
plt.tight_layout()
plt.show()

