import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
df = pd.read_excel('aligned_risk_personal_loans.xlsx')

# 1. Risk Class Distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='Risk Class', data=df, palette='Set2')
plt.title('Distribution of Risk Classes')
plt.xlabel('Risk Class')
plt.ylabel('Count')
plt.show()

# 2. Scatter Plot of Expected Loss vs Unexpected Loss
plt.figure(figsize=(10, 6))
sns.scatterplot(x='EL', y='UL', hue='Risk Class', data=df, palette='Set1', alpha=0.7)
plt.title('Expected Loss vs Unexpected Loss')
plt.xlabel('Expected Loss (EL)')
plt.ylabel('Unexpected Loss (UL)')
plt.legend(title='Risk Class')
plt.show()

# 3. Credit Score Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Credit Score'], bins=20, kde=True, color='blue')
plt.title('Distribution of Credit Scores')
plt.xlabel('Credit Score')
plt.ylabel('Frequency')
plt.show()

# 4. Loan Term vs EAD (Exposure at Default)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Term (Months)', y='EAD', data=df, palette='Set3')
plt.title('Loan Term vs Exposure at Default (EAD)')
plt.xlabel('Loan Term (Months)')
plt.ylabel('Exposure at Default (EAD)')
plt.show()

# 5. Heatmap of Correlation Between Risk Metrics
correlation_matrix = df[['EAD', 'LGD', 'PD', 'EL', 'UL']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Risk Metrics')
plt.show()
