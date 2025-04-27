import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
df = pd.read_excel("aligned_risk_personal_loans.xlsx")

# Ensure required columns exist
required_cols = ['PD', 'LGD', 'EAD']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

# Extract relevant vectors
pd_array = df['PD'].values.reshape(-1, 1)  # Shape (n_loans, 1)
lgd_array = df['LGD'].values.reshape(-1, 1)
ead_array = df['EAD'].values.reshape(-1, 1)

num_loans = len(df)
num_simulations = 10000

# Generate random numbers for default simulation
random_matrix = np.random.rand(num_loans, num_simulations)  # Shape (n_loans, num_simulations)

# Simulate default (1 if rand < PD, else 0)
default_matrix = (random_matrix < pd_array).astype(int)

# Loss per loan = default * LGD * EAD
loss_matrix = default_matrix * lgd_array * ead_array  # Element-wise multiplication

# Sum across loans for each simulation
total_loss_per_simulation = loss_matrix.sum(axis=0)

# Risk Metrics
mean_loss = np.mean(total_loss_per_simulation)
std_loss = np.std(total_loss_per_simulation)
VaR_95 = np.percentile(total_loss_per_simulation, 5)
VaR_99 = np.percentile(total_loss_per_simulation, 1)

# Output results
print(f"Mean Loss: {mean_loss:.2f}")
print(f"Standard Deviation of Loss: {std_loss:.2f}")
print(f"95% VaR: {VaR_95:.2f}")
print(f"99% VaR: {VaR_99:.2f}")

# Plotting
plt.figure(figsize=(10, 6))
plt.hist(total_loss_per_simulation, bins=50, color='skyblue', edgecolor='black')

# Add lines for VaR at 95% and 99%
plt.axvline(VaR_95, color='red', linestyle='--', label=f"95% VaR = {VaR_95:.2f}")
plt.axvline(VaR_99, color='green', linestyle='--', label=f"99% VaR = {VaR_99:.2f}")

# Title and labels
plt.title("Monte Carlo Simulation of Portfolio Loss")
plt.xlabel("Total Loss")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


