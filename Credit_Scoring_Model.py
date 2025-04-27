import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Load the Portfolio Data
df = pd.read_excel('aligned_risk_personal_loans.xlsx')

# Credit Score Ranges based on Risk Class
# Credit Score Ranges based on Risk Class
def get_credit_score(risk_class):
    """
    Get the credit score range based on risk class.
    """
    # Ensure the risk_class is a string (e.g., '01', '02', etc.)
    risk_class = str(risk_class).zfill(2)  # Convert to string and pad with leading zero if needed
    
    ranges = {
        '01': (700, 850),
        '02': (600, 699),
        '03': (500, 599),
        '04': (400, 499),
        '05': (300, 399)
    }
    
    if risk_class in ranges:
        return random.randint(*ranges[risk_class])
    else:
        raise ValueError(f"Invalid risk class: {risk_class}")


# Apply Credit Score Calculation
df['Credit Score'] = df['Risk Class'].apply(get_credit_score)

# Credit Score Distribution
plt.figure(figsize=(10, 6))
plt.hist(df['Credit Score'], bins=20, color='skyblue', edgecolor='black')
plt.title('Credit Score Distribution for Portfolio')
plt.xlabel('Credit Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Analyze Relationship Between Credit Score and Other Risk Metrics
# Correlation Analysis between Credit Score and other metrics like EAD, LGD, PD
correlation_matrix = df[['Credit Score', 'EAD', 'LGD', 'PD', 'EL', 'UL']].corr()

# Print correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# Visualize the Correlation Matrix
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Summary Statistics of the Credit Score
credit_score_summary = df['Credit Score'].describe()
print("Credit Score Summary Statistics:")
print(credit_score_summary)

# Calculate the Average Credit Score per Risk Class
average_credit_scores = df.groupby('Risk Class')['Credit Score'].mean()
print("Average Credit Score per Risk Class:")
print(average_credit_scores)

# Risk Analysis Based on Credit Score
# We can categorize loans into groups based on their Credit Score:
high_credit_score_loans = df[df['Credit Score'] >= 750]
medium_credit_score_loans = df[(df['Credit Score'] >= 650) & (df['Credit Score'] < 750)]
low_credit_score_loans = df[df['Credit Score'] < 650]

print(f"\nNumber of High Credit Score Loans: {len(high_credit_score_loans)}")
print(f"Number of Medium Credit Score Loans: {len(medium_credit_score_loans)}")
print(f"Number of Low Credit Score Loans: {len(low_credit_score_loans)}")

# Calculate the Average EAD, LGD, PD, EL for Each Category of Credit Score
high_credit_score_risk_metrics = high_credit_score_loans[['EAD', 'LGD', 'PD', 'EL']].mean()
medium_credit_score_risk_metrics = medium_credit_score_loans[['EAD', 'LGD', 'PD', 'EL']].mean()
low_credit_score_risk_metrics = low_credit_score_loans[['EAD', 'LGD', 'PD', 'EL']].mean()

print("\nHigh Credit Score Loan Risk Metrics:")
print(high_credit_score_risk_metrics)

print("\nMedium Credit Score Loan Risk Metrics:")
print(medium_credit_score_risk_metrics)

print("\nLow Credit Score Loan Risk Metrics:")
print(low_credit_score_risk_metrics)


