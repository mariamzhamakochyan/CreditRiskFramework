import pandas as pd
import random

# Define a simple Risk Class to PD mapping
def get_pd(risk_class):
    """
    Return the Probability of Default (PD) based on risk class.
    """
    if risk_class == '01':
        return 0.01  # 1% default probability
    elif risk_class == '02':
        return 0.03  # 3% default probability
    elif risk_class == '03':
        return 0.08  # 8% default probability
    elif risk_class == '04':
        return 0.20  # 20% default probability
    elif risk_class == '05':
        return 0.50  # 50% default probability
    else:
        return 0.1  # Default to 10% if unknown risk class

def calculate_credit_spread(risk_class, base_spread=0.02, risk_free_rate=0.03):
    """
    Calculate the credit spread based on the loan's risk class.
    """
    # Get the PD based on the risk class
    pd = get_pd(risk_class)
    
    # The higher the PD, the higher the risk premium
    risk_premium = pd * 0.05  # Arbitrary risk premium factor for demonstration
    
    # The total credit spread is the base spread plus the risk premium
    credit_spread = base_spread + risk_premium
    return credit_spread

# Simulate loan portfolio data (replace this with actual loan data)
loan_data = {
    'Loan_ID': [f'Loan_{i}' for i in range(1, 251)],
    'Risk_Class': [random.choice(['01', '02', '03', '04', '05']) for _ in range(250)],
    'Outstanding_Amount': [random.randint(1000000, 5000000) for _ in range(250)],  # Random loan amounts
}

# Create a DataFrame to represent the loan portfolio
loan_df = pd.DataFrame(loan_data)

# Calculate credit spread for each loan based on its risk class
loan_df['Credit_Spread'] = loan_df['Risk_Class'].apply(lambda x: calculate_credit_spread(x))

# Display the first few rows of the data with calculated credit spreads
print(loan_df[['Loan_ID', 'Risk_Class', 'Credit_Spread']].head())

# Visualize the distribution of credit spreads
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.hist(loan_df['Credit_Spread'], bins=10, edgecolor='black', color='skyblue')
plt.title('Distribution of Credit Spreads')
plt.xlabel('Credit Spread')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

