import pandas as pd

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

    # Construct the result dictionary
    portfolio_metrics = {
        'YTM': weighted_ytm,
        'Duration': weighted_duration,
        'Modified Duration': weighted_modified_duration,
        'Convexity': weighted_convexity,
        'DV01': total_dv01
    }

    return portfolio_metrics