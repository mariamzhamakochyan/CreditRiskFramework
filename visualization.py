import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load dataset
df = pd.read_excel("aligned_risk_personal_loans.xlsx")

# Create folder for plots
os.makedirs("plots", exist_ok=True)

# 1. Loan Distribution by Risk Class
plt.figure(figsize=(8, 5))
sns.countplot(x='Risk Class', data=df, palette='Set2')
plt.title('Loan Count by Risk Class')
plt.xlabel('Risk Class')
plt.ylabel('Number of Loans')
plt.savefig('plots/loan_distribution_by_risk_class.png')
plt.clf()

# 2. Credit Score Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['Credit Score'], bins=20, kde=True, color='skyblue')
plt.title('Credit Score Distribution')
plt.xlabel('Credit Score')
plt.ylabel('Count')
plt.savefig('plots/credit_score_distribution.png')
plt.clf()

# 3. EL vs UL Scatter Plot
plt.figure(figsize=(10, 6))
plt.scatter(df['EL'], df['UL'], c=df['PD'], cmap='coolwarm', alpha=0.6)
plt.title('Expected Loss vs. Unexpected Loss')
plt.xlabel('Expected Loss (EL)')
plt.ylabel('Unexpected Loss (UL)')
plt.colorbar(label='Probability of Default (PD)')
plt.grid(True)
plt.savefig('plots/el_vs_ul_scatter.png')
plt.clf()

# 4. PD vs LGD Heatmap
pivot = pd.pivot_table(df, values='Outstanding Amount', index='PD', columns='LGD', aggfunc='count', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(pivot, cmap='YlGnBu')
plt.title('PD vs LGD Heatmap (Loan Count)')
plt.xlabel('LGD')
plt.ylabel('PD')
plt.savefig('plots/pd_vs_lgd_heatmap.png')
plt.clf()

# 5. Loan Amount by Risk Class (Boxplot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Risk Class', y='Outstanding Amount', data=df, palette='Pastel1')
plt.title('Loan Amount Distribution by Risk Class')
plt.xlabel('Risk Class')
plt.ylabel('Loan Amount')
plt.yscale('log')  # Log scale for better readability with large ranges
plt.savefig('plots/loan_amount_by_risk_class.png')
plt.clf()

print("✅ All visualizations saved to 'plots' folder.")
print(f"✅ Loaded {df.shape[0]} loans into visualization")  # Should say 250

