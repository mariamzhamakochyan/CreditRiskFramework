import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load your previously generated Excel file
df = pd.read_excel("aligned_risk_personal_loans.xlsx")

# Assuming df is already defined as in your previous steps

# Calculate the Credit Spread and Break-Even PD for analysis
risk_free_rate = 0.085  # Example risk-free rate (8.5%)
df["Fair Spread"] = (df["LGD"] * df["PD"]) / (1 - df["PD"]) * (1 + risk_free_rate)
df["Credit Spread"] = df["PD"] * (1 - df["Recovery Rate"])  # Credit Spread calculation
df["Break-Even PD"] = df["Fair Spread"] / (1 - df["Recovery Rate"])  # Break-Even PD

# 1. Line Plot for Credit Spread vs Fair Spread across Risk Class
# plt.figure(figsize=(10, 6))
# sns.lineplot(data=df, x='Risk Class', y='Credit Spread', label="Credit Spread", marker='o', color='blue', linewidth=2)
# sns.lineplot(data=df, x='Risk Class', y='Fair Spread', label="Fair Spread", marker='o', color='red', linewidth=2)
# plt.title("Credit Spread and Fair Spread by Risk Class", fontsize=16)
# plt.xlabel("Risk Class", fontsize=12)
# plt.ylabel("Spread (%)", fontsize=12)
# plt.legend(title="Spread Type")
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# 2. Bar Plot for Credit Spread by Risk Class
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Risk Class', y='Credit Spread', palette='Blues')
plt.title("Average Credit Spread by Risk Class", fontsize=16)
plt.xlabel("Risk Class", fontsize=12)
plt.ylabel("Credit Spread (%)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Histogram of Credit Spread Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Credit Spread'], bins=20, kde=True, color='blue', edgecolor='black')
plt.title("Distribution of Credit Spread", fontsize=16)
plt.xlabel("Credit Spread (%)", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.tight_layout()
plt.show()

# 4. Correlation Heatmap between key variables
correlation_matrix = df[['PD', 'LGD', 'Credit Spread', 'Fair Spread', 'Break-Even PD']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True, linewidths=1, linecolor='black')
plt.title("Correlation Heatmap of Key Risk Metrics", fontsize=16)
plt.tight_layout()
plt.show()

