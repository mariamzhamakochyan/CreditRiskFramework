import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Parameters
num_loans = 250
years = list(range(2020, 2026))
months_options = [12, 24, 36, 48, 60]
risk_class_distribution = ['01'] * 170 + ['02'] * 40 + random.choices(['03', '04', '05'], k=40)
random.shuffle(risk_class_distribution)

# Helper Functions
def generate_loan_number(existing_numbers):
    while True:
        year = random.choice(years)
        suffix = f"{random.randint(0, 999999):06d}"
        loan_number = f"V2{year % 10}-{suffix}"
        if loan_number not in existing_numbers:
            return loan_number

def generate_customer_number(existing_customers):
    customer_id = f"C{random.randint(100000, 999999)}"
    if customer_id not in existing_customers or random.random() < 0.85:
        existing_customers.add(customer_id)
        return customer_id
    return random.choice(list(existing_customers))

def generate_dates(year, months):
    start_date = datetime(year, random.randint(1, 12), random.randint(1, 28))
    end_date = start_date + timedelta(days=30 * months)
    return start_date.date(), end_date.date()

def generate_overdue(risk_class):
    if risk_class == '01':
        return 0, 0, 0, 0
    elif risk_class == '02':
        days = random.randint(1, 60)
    elif risk_class == '03':
        days = random.randint(61, 90)
    elif risk_class == '04':
        days = random.randint(91, 180)
    else:  # '05'
        days = random.randint(181, 365)

    principal_amt = random.randint(1000, 1000000)
    interest_amt = random.randint(500, 500000)
    return days, principal_amt, interest_amt, days

def get_credit_score(risk_class):
    ranges = {
        '01': (700, 850), '02': (600, 699),
        '03': (500, 599), '04': (400, 499), '05': (300, 399)
    }
    return random.randint(*ranges[risk_class])

def get_recovery_rate(risk_class):
    ranges = {
        '01': (0.6, 0.8), '02': (0.4, 0.6),
        '03': (0.3, 0.5), '04': (0.2, 0.4), '05': (0.1, 0.3)
    }
    return round(random.uniform(*ranges[risk_class]), 2)

def simulate_credit_limit(outstanding):
    return round(outstanding * random.uniform(1.0, 1.5))

def simulate_employment():
    return random.choice(["Employed", "Self-employed", "Unemployed", "Retired", "Student"])

def simulate_macroeconomic_factors():
    # Simulate interest rate change and unemployment rate change (randomized)
    interest_rate_change = random.uniform(-0.02, 0.02)  # +/- 2% change
    unemployment_rate_change = random.uniform(-0.03, 0.03)  # +/- 3% change
    return interest_rate_change, unemployment_rate_change

def calculate_risk_metrics(amount, recovery_rate, risk_class, loan_term, interest_rate_change, unemployment_rate_change):
    # Adjust PD based on risk class, loan term, and macroeconomic factors
    base_PD_dict = {'01': 0.01, '02': 0.03, '03': 0.08, '04': 0.2, '05': 0.5}
    PD = base_PD_dict[risk_class]
    
    # Adjust PD based on loan term
    PD += (loan_term - 12) * 0.005  # Increase PD for longer terms
    
    # Adjust PD based on macroeconomic conditions
    PD += interest_rate_change * 0.1  # Interest rate change increases PD
    PD += unemployment_rate_change * 0.2  # Unemployment rate change significantly affects PD
    
    # Clip PD to a reasonable range [0, 1]
    PD = min(max(PD, 0), 1)
    
    LGD = 1 - recovery_rate  # LGD is 1 - recovery rate
    
    # Adjust LGD based on loan term
    LGD += (loan_term - 12) * 0.01  # Longer terms increase LGD
    
    # UL Calculation based on adjusted PD and LGD
    UL = amount * np.sqrt(PD * (1 - PD)) * LGD  # Unexpected Loss formula
    
    # Calculate Expected Loss (EL)
    EL = amount * PD * LGD  # Expected Loss formula
    
    # Calculate Exposure at Default (EAD)
    EAD = amount  # This is the outstanding amount
    
    return EAD, LGD, PD, EL, UL

# Generate Dataset
loan_numbers = set()
customer_numbers = set()
records = []

for i in range(num_loans):
    risk_class = risk_class_distribution[i]
    loan_number = generate_loan_number(loan_numbers)
    loan_numbers.add(loan_number)

    customer_number = generate_customer_number(customer_numbers)
    amount = random.randint(100000, 10000000)
    interest_rate = round(random.uniform(13, 21), 1)
    if interest_rate % 1 == 0:
        interest_rate = int(interest_rate)
    
    year = int(loan_number[2]) + 2020
    term = random.choice(months_options)
    provided, maturity = generate_dates(year, term)
    pr_days, pr_amt, int_amt, int_days = generate_overdue(risk_class)

    credit_score = get_credit_score(risk_class)
    recovery_rate = get_recovery_rate(risk_class)
    employment = simulate_employment()
    credit_limit = simulate_credit_limit(amount)
    
    # Simulate macroeconomic factors
    interest_rate_change, unemployment_rate_change = simulate_macroeconomic_factors()
    
    # Calculate risk metrics with macroeconomic adjustments
    EAD, LGD, PD, EL, UL = calculate_risk_metrics(amount, recovery_rate, risk_class, term, interest_rate_change, unemployment_rate_change)

    records.append([
        loan_number, customer_number, "AMD", amount, interest_rate, risk_class,
        provided, maturity, term,
        pr_days, pr_amt, int_amt, int_days,
        credit_score, recovery_rate, credit_limit, employment, "Personal",
        interest_rate_change, unemployment_rate_change, EAD, LGD, PD, EL, UL
    ])

# Create and Export DataFrame
columns = [
    "Loan Number", "Customer Number", "Currency", "Outstanding Amount", "Interest Rate", "Risk Class",
    "Provided Date", "Maturity Date", "Term (Months)",
    "Principal Overdue Days", "Principal Overdue Amount",
    "Interest Overdue Amount", "Interest Overdue Days",
    "Credit Score", "Recovery Rate", "Credit Limit", "Employment Status", "Loan Purpose",
    "Interest Rate Change", "Unemployment Rate Change", "EAD", "LGD", "PD", "EL", "UL"
]

df = pd.DataFrame(records, columns=columns)
df.to_excel("aligned_risk_personal_loans.xlsx", index=False)
print("✅ Excel file 'aligned_risk_personal_loans.xlsx' generated.")

