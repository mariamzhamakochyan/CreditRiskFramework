# correlation_covariance.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def load_data(filepath="aligned_risk_personal_loans.xlsx"):
    df = pd.read_excel(filepath)
    return df

def compute_matrices(df):
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    covariance_matrix = numeric_df.cov()
    return correlation_matrix, covariance_matrix

def plot_heatmap(matrix, title, figsize=(12, 10), cmap="coolwarm"):
    plt.figure(figsize=figsize)
    sns.heatmap(matrix, annot=True, fmt=".2f", cmap=cmap, center=0, linewidths=0.5)
    plt.title(title, fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

  
    plt.show()

def main():
    df = load_data()
    corr_matrix, cov_matrix = compute_matrices(df)

    print("🔍 Correlation Matrix:")
    print(corr_matrix.round(2))

    print("\n📦 Covariance Matrix:")
    print(cov_matrix.round(2))

    # Visualizations
    plot_heatmap(corr_matrix, "📊 Correlation Matrix Heatmap")
    plot_heatmap(cov_matrix, "📦 Covariance Matrix Heatmap", cmap="YlGnBu")

if __name__ == "__main__":
    main()

