import pandas as pd
from utils.bond_math import *

def calculate_portfolio_metrics(portfolio_df, weight_col, num_bonds_col, price_col, ytm_col, maturity_col, coupon_col):
    """
    Calculate portfolio metrics for a bond portfolio.

    Parameters:
    - portfolio_df (DataFrame): DataFrame containing bond portfolio data.
    - weight_col (str): Column name for bond weight (% of invested portfolio).
    - num_bonds_col (str): Column name for number of bonds.
    - price_col (str): Column name for bond price.
    - ytm_col (str): Column name for bond yield to maturity.
    - maturity_col (str): Column name for years to maturity.
    - coupon_col (str): Column name for coupon rate.

    Returns:
    - dict: Dictionary containing portfolio metrics (YTM, duration, modified duration, convexity, dv01).
    """

    # Ensure required columns are present
    required_columns = [weight_col, num_bonds_col, price_col, ytm_col, maturity_col, coupon_col]
    if not set(required_columns).issubset(portfolio_df.columns):
        raise ValueError("Missing required columns in the portfolio DataFrame.")

    # Calculate weighted averages for portfolio metrics
    weighted_ytm = (portfolio_df[weight_col] / 100 * portfolio_df[ytm_col]).sum()
    weighted_duration = (portfolio_df[weight_col] / 100 * portfolio_df[maturity_col]).sum()
    weighted_modified_duration   =  (portfolio_df[weight_col] / 100 * portfolio_df[maturity_col] /
                                    (1 + (portfolio_df[ytm_col] / 100))).sum()
    weighted_convexity = (portfolio_df[weight_col] / 100 * (portfolio_df[maturity_col] * (portfolio_df[maturity_col] + 1) /
                                (1 + (portfolio_df[ytm_col] / 100))**2)).sum()

    # Calculate dv01 for each bond and sum for the portfolio
    portfolio_df['dv01'] = portfolio_df.apply(lambda row:    calculate_dv01(row[price_col], row[coupon_col],
                                                                            row[maturity_col], row[ytm_col]), axis=1)
    total_dv01 = (portfolio_df[weight_col] / 100 * portfolio_df['dv01']).sum()

    # Calculate weighted averages for additional metrics
    weighted_buy_price = (portfolio_df[weight_col] / 100 * portfolio_df['Buy Price']).sum()
    weighted_years_to_maturity = (portfolio_df[weight_col] / 100 * portfolio_df['Years to Maturity']).sum()
    weighted_percentage_spread = (portfolio_df[weight_col] / 100 * portfolio_df['Percentage Spread']).sum()
    weighted_cpn = (portfolio_df[weight_col] / 100 * portfolio_df['Cpn']).sum() 
    weighted_spread_5y = (portfolio_df[weight_col] / 100 * portfolio_df['Spread_5y']).sum()
    weighted_pd_5y_pct = (portfolio_df[weight_col] / 100 * portfolio_df['PD_5y_pct']).sum()

    # Add the new metric to the DataFrame
    portfolio_metrics_df = pd.DataFrame({
        'Metric': ['YTM', 'Price', 'Coupon', 'Time-to-Maturity', 'Duration', 'Modified Duration', 'Convexity', 'DV01', 'Pct Bid-Ask Spread', '5-yr CDS Spread', 'PD_5y_pct'],
        'Value': [weighted_ytm, weighted_buy_price, weighted_cpn, weighted_years_to_maturity, weighted_duration, weighted_modified_duration, weighted_convexity, total_dv01, weighted_percentage_spread, weighted_spread_5y, weighted_pd_5y_pct]
    })
    portfolio_metrics_df['Value'] = portfolio_metrics_df['Value'] * 100

    return portfolio_metrics_df