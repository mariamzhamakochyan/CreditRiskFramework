import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("aligned_risk_personal_loans.xlsx")

# Monte Carlo Simulation Parameters
n_simulations = 1000
total_portfolio = df["Outstanding Amount"].sum()
loss_distributions = []

# Run Monte Carlo Simulations
for _ in range(n_simulations):
    simulated_losses = []
    for _, row in df.iterrows():
        ead = row["EAD"]
        lgd = row["LGD"]
        pd_sim = np.random.binomial(1, row["PD"])
        loss = ead * lgd * pd_sim
        simulated_losses.append(loss)
    loss_distributions.append(np.sum(simulated_losses))

# Convert to NumPy array
loss_distributions = np.array(loss_distributions)

# Calculate VaR and CVaR
var_95 = np.percentile(loss_distributions, 95)
var_99 = np.percentile(loss_distributions, 99)
cvar_95 = loss_distributions[loss_distributions >= var_95].mean()
cvar_99 = loss_distributions[loss_distributions >= var_99].mean()

# Print Results
print(f"VaR at 95%: {var_95:,.0f} AMD")
print(f"VaR at 99%: {var_99:,.0f} AMD")
print(f"CVaR at 95%: {cvar_95:,.0f} AMD")
print(f"CVaR at 99%: {cvar_99:,.0f} AMD")

# Plot Loss Distribution
plt.figure(figsize=(12, 6))
sns.histplot(loss_distributions, bins=100, kde=True, color='skyblue')
plt.axvline(var_95, color='orange', linestyle='--', label=f'VaR 95% = {var_95:,.0f} AMD')
plt.axvline(var_99, color='red', linestyle='--', label=f'VaR 99% = {var_99:,.0f} AMD')
plt.title("Simulated Loss Distribution - Monte Carlo", fontsize=16)
plt.xlabel("Total Portfolio Loss (AMD)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
