import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Parameters
debt_value = 80000
risk_free_rate = 0.03
time_to_maturity = 1
asset_value = 120000
volatilities = [0.2, 0.25, 0.3, 0.35]  # Increasing volatilities

x = np.linspace(0.5, 1.5, 100)

plt.figure(figsize=(10, 6))

for sigma in volatilities:
    d1 = (np.log(x) + (risk_free_rate - 0.5 * sigma**2) * time_to_maturity) / (sigma * np.sqrt(time_to_maturity))
    pd = norm.cdf(-d1)
    plt.plot(x * debt_value, pd, label=f"Volatility = {sigma}")

plt.title("Դեֆոլտի հավանականություն՝ ըստ ակտիվների արժեքի տարբեր անկայունությունների")
plt.xlabel("Ակտիվների արժեք")
plt.ylabel("Դեֆոլտի հավանականություն (PD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

