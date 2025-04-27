import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

# Function to calculate Merton Model PD
def merton_model_pd(asset_value, debt_value, volatility, risk_free_rate, time_to_maturity):
    """
    Calculate the Probability of Default (PD) using the Merton Model.

    Parameters:
    asset_value (float): The value of the firm's assets.
    debt_value (float): The value of the firm's liabilities.
    volatility (float): The volatility of the firm's asset value.
    risk_free_rate (float): The risk-free rate (annualized).
    time_to_maturity (float): The time to maturity (in years).
    
    Returns:
    pd (float): The probability of default.
    """
    # Calculate the distance to default (DD)
    dd = (asset_value - debt_value) / (volatility * asset_value)
    
    # Calculate the probability of default (PD) using the Merton model formula
    d1 = (np.log(asset_value / debt_value) + (risk_free_rate - 0.5 * volatility**2) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    pd = norm.cdf(-d1)  # Cumulative distribution function of the normal distribution
    return pd

# Example loan portfolio with asset values, debt values, volatility, risk-free rate, and time to maturity
portfolio_data = {
    'Risk Class': [1, 2, 3, 4, 5],
    'Asset_Value': [100000, 120000, 150000, 110000, 95000],  # Example values for the firm's asset value
    'Debt_Value': [70000, 80000, 100000, 90000, 60000],  # Example values for the firm's liabilities
    'Volatility': [0.25, 0.30, 0.22, 0.28, 0.27],  # Volatility of asset value (annualized)
    'Risk_Free_Rate': [0.03, 0.03, 0.03, 0.03, 0.03],  # Risk-free rate (3% per year)
    'Time_to_Maturity': [1, 1, 1, 1, 1]  # Time to maturity in years (1 year)
}

# Convert portfolio data to a DataFrame
df = pd.DataFrame(portfolio_data)

# Calculate Probability of Default (PD) for each loan in the portfolio using Merton Model
df['PD'] = df.apply(lambda row: merton_model_pd(row['Asset_Value'], row['Debt_Value'], row['Volatility'],
                                                row['Risk_Free_Rate'], row['Time_to_Maturity']), axis=1)

# Display the portfolio data with PD values
print(df)

# Visualizing the Probability of Default (PD) for each loan in the portfolio
plt.figure(figsize=(10, 6))
plt.bar(df['Risk Class'], df['PD'], color='blue')
plt.xlabel('Risk Class')
plt.ylabel('Probability of Default (PD)')
plt.title('Probability of Default (PD) for Each Loan in the Portfolio')
plt.show()

