import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("aligned_risk_personal_loans.xlsx")

# Parameters for Monte Carlo Simulation
num_simulations = 10000
confidence_level_99 = 0.99
confidence_level_95 = 0.95

# Simulate Portfolio Losses using Monte Carlo Simulation
simulated_losses = []

for _ in range(num_simulations):
    total_loss = 0
    # For each loan in the portfolio, simulate whether it defaults or not
    for _, row in df.iterrows():
        # Simulate the default occurrence using the loan's Probability of Default (PD)
        default_simulation = np.random.rand() < row['PD']
        if default_simulation:
            # If default happens, the loss is EAD * LGD
            total_loss += row['EAD'] * row['LGD']
    
    simulated_losses.append(total_loss)

# Convert the simulated losses into a numpy array
simulated_losses = np.array(simulated_losses)

# Calculate the VaR at 99% and 95% confidence levels using percentiles
VaR_99 = np.percentile(simulated_losses, (1 - confidence_level_99) * 100)
VaR_95 = np.percentile(simulated_losses, (1 - confidence_level_95) * 100)

# Plot the simulated losses to visualize the VaR
plt.figure(figsize=(10, 6))
plt.hist(simulated_losses, bins=100, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(VaR_99, color='red', linestyle='dashed', linewidth=2, label=f'VaR 99%: {VaR_99:,.2f}')
plt.axvline(VaR_95, color='orange', linestyle='dashed', linewidth=2, label=f'VaR 95%: {VaR_95:,.2f}')
plt.title("Monte Carlo Simulation: Portfolio Loss Distribution", fontsize=14)
plt.xlabel("Portfolio Loss", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Output the calculated VaR values
print(f"Value at Risk (VaR) at 99% confidence level: {VaR_99:,.2f}")
print(f"Value at Risk (VaR) at 95% confidence level: {VaR_95:,.2f}")
