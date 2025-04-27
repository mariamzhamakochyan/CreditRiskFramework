import pandas as pd

# Բեռնում ենք տվյալները
df = pd.read_excel('aligned_risk_personal_loans.xlsx')

# Կարգավորիչ կապիտալ (կմուտքագրես քո բանկի կապիտալի չափը՝ օրինակ 10 մլրդ)
K = 250_000_000  # օրինակ 10 մլրդ դրամ

# Քանի որ բոլոր վարկերը ունեն 100% ռիսկային կշիռ
df['Risk Weight'] = 1.00
df['Risk Weighted Asset'] = df['Outstanding Amount'] * df['Risk Weight']

# Վարկային ռիսկով կշռված ակտիվների գումար
VR = df['Risk Weighted Asset'].sum()

# Շուկայի ու Գործառնական ռիսկեր չենք հաշվում հիմա
SR = 0
GR = 0

# Ռիսկով Կշռված Ակտիվներ (ՌԿԱ)
RKA = VR + (100/11) * (SR + GR)

# Ն1 կապիտալի ադեկվատության նորմատիվ
N1 = K / RKA if RKA > 0 else 0

print(f"✅ ՌԿԱ = {RKA:,.2f} դրամ")
print(f"✅ Կապիտալի ընդհանուր չափը = {K:,.2f} դրամ")
print(f"📊 Ն1 (կապիտալի ադեկվատություն) = {N1:.2%}")
import pandas as pd

# Բեռնում ենք տվյալները
df = pd.read_excel('aligned_risk_personal_loans.xlsx')

# Կարգավորիչ կապիտալ (կմուտքագրես քո բանկի կապիտալի չափը՝ օրինակ 10 մլրդ)
K = 250_000_000  # օրինակ 10 մլրդ դրամ

# Քանի որ բոլոր վարկերը ունեն 100% ռիսկային կշիռ
df['Risk Weight'] = 1.00
df['Risk Weighted Asset'] = df['Outstanding Amount'] * df['Risk Weight']

# Վարկային ռիսկով կշռված ակտիվների գումար
VR = df['Risk Weighted Asset'].sum()

# Շուկայի ու Գործառնական ռիսկեր չենք հաշվում հիմա
SR = 0
GR = 0

# Ռիսկով Կշռված Ակտիվներ (ՌԿԱ)
RKA = VR + (100/11) * (SR + GR)

# Ն1 կապիտալի ադեկվատության նորմատիվ
N1 = K / RKA if RKA > 0 else 0

print(f"✅ ՌԿԱ = {RKA:,.2f} դրամ")
print(f"✅ Կապիտալի ընդհանուր չափը = {K:,.2f} դրամ")
print(f"📊 Ն1 (կապիտալի ադեկվատություն) = {N1:.2%}")
import matplotlib.pyplot as plt
import numpy as np

# Constants
capital = 250000000  # 10 billion AMD
RKA_values = np.linspace(500000000, 3000000000 , 100)  # Simulating different RKA values from 1 billion to 5 billion

# Calculate N1 (Capital Adequacy Ratio) for each RKA value
N1_values = (capital / RKA_values) * 100

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(RKA_values, N1_values, label="N1 (Capital Adequacy)", color="b", lw=2)
plt.axhline(y=12, color='r', linestyle='--', label="Regulatory Minimum (12%)")
plt.title("Capital Adequacy Ratio (N1) vs RWA (Risk-Weighted Assets)", fontsize=14)
plt.xlabel("Risk-Weighted Assets (RWA)", fontsize=12)
plt.ylabel("Capital Adequacy Ratio (N1) [%]", fontsize=12)
plt.legend()
plt.grid(True)
plt.show()
