import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample DataFrame (Replace this with your actual data)
df = pd.read_excel('aligned_risk_personal_loans.xlsx')  # Replace with your file path

# Calculate Break-Even Default if not done yet
df['Break_Even_Default'] = df['EL'] / df['EAD']  # Example calculation

# Define colors for each Risk Class
risk_class_colors = {1: 'blue', 2: 'green', 3: 'yellow', 4: 'orange', 5: 'red'}

# Initialize the plot
plt.figure(figsize=(10, 6))

# Set the style for better visual appeal
sns.set(style="whitegrid")

# Plot a scatter plot with color based on Risk Class
scatter = plt.scatter(df['Break_Even_Default'], df['PD'], c=df['Risk Class'].map(risk_class_colors), s=100, edgecolors='k', alpha=0.7)

# Add a legend for the Risk Classes
import matplotlib.patches as mpatches
legend_labels = [mpatches.Patch(color=color, label=f'Risk Class {risk_class}') for risk_class, color in risk_class_colors.items()]
plt.legend(handles=legend_labels, title="Risk Class", fontsize=12)

# Fit a linear regression model to add a trend line
X = df[['Break_Even_Default']]
y = df['PD']
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Plot the trend line
plt.plot(df['Break_Even_Default'], y_pred, color='black', linestyle='--', label='Trend Line')

# Add labels and title
plt.title('Break-Even Default vs Probability of Default (PD)', fontsize=16)
plt.xlabel('Break-Even Default', fontsize=14)
plt.ylabel('Probability of Default (PD)', fontsize=14)

# Customize ticks and grid
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

