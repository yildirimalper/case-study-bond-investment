import pandas as pd
import numpy as np
from pathlib import Path
from utils.bond_math import calculate_bond_price, calculate_macaulay_duration, calculate_modified_duration, calculate_bond_convexity, calculate_dv01

# Set the project directory for easy access to the data
PROJECT_DIR = Path().resolve()

# load the data
data = pd.read_pickle(PROJECT_DIR / "processed_data" / "bonds-data.pkl")

# Convert Maturity column to datetime, and find the years to maturity
data["Maturity"] = pd.to_datetime(data["Maturity"])
data["Years to Maturity"] = round((data["Maturity"] - pd.to_datetime('2023-11-24')).dt.days / 365).astype(int)
data["Years to Maturity"] = np.where(data["Years to Maturity"] == 0, 1, data["Years to Maturity"])

# Add a new column named "Face Value" with a constant value of 1000
data['Face Value'] = 1000

# =============================================================================
# 1. BOND PRICE
# =============================================================================
# Calculate Buy Price
data['Buy Price'] = data.apply(lambda row: calculate_bond_price(
    face_value=row['Face Value'],
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'],
    buying=True
), axis=1)

# Calculate Sell Price
data['Sell Price'] = data.apply(lambda row: calculate_bond_price(
    face_value=row['Face Value'],
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'], 
    buying=False
), axis=1)

# =============================================================================
# 2. MACAULAY DURATION
# =============================================================================
# Calculate Macaulay Duration for Buying
data['Macaulay Duration (Buy)'] = data.apply(lambda row: calculate_macaulay_duration(
    face_value=row['Face Value'],
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'],
    buying=True
), axis=1)

# Calculate Macaulay Duration for Selling
data['Macaulay Duration (Sell)'] = data.apply(lambda row: calculate_macaulay_duration(
    face_value=row['Face Value'], 
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'],
    buying=False
), axis=1)

# =============================================================================
# 3. MODIFIED DURATION
# =============================================================================
# Calculate Modified Duration for Buying
data['Modified Duration (Buy)'] = data.apply(lambda row: calculate_modified_duration(
    face_value=row['Face Value'],
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'], 
    buying=True
), axis=1)

# Calculate Modified Duration for Selling
data['Modified Duration (Sell)'] = data.apply(lambda row: calculate_modified_duration(
    face_value=row['Face Value'], 
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'], 
    buying=False
), axis=1)

# =============================================================================
# 4. CONVEXITY
# =============================================================================
# Calculate Convexity for Buying
data['Convexity (Buy)'] = data.apply(lambda row: calculate_bond_convexity(
    face_value=row['Face Value'],
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'],  
    buying=True
), axis=1)

# Calculate Convexity for Selling
data['Convexity (Sell)'] = data.apply(lambda row: calculate_bond_convexity(
    face_value=row['Face Value'],
    years_to_maturity=row['Years to Maturity'],
    ytm_bid=row['YTM - Bid'],
    ytm_ask=row['YTM - Ask'],
    coupon_rate=row['Cpn'],
    buying=False
), axis=1)

# =============================================================================
# 5. DV01
# =============================================================================
# Calculate DV01 for each bond
data['DV01'] = data.apply(lambda row: calculate_dv01(
    face_value=row['Face Value'],
    coupon_rate=row['Cpn'], 
    years_to_maturity=row['Years to Maturity'],
    ytm=row['YTM - Bid'] 
), axis=1)

# =============================================================================
# 6. Compute the Bid-Ask Spread
# =============================================================================
data['Buy-Sell Spread'] = data['Buy Price'] - data['Sell Price']
data['Percentage Spread'] = (data['Buy-Sell Spread'] / data['Buy Price']) * 100

# =============================================================================
# 7. Export data
# =============================================================================
# save the data to an Excel and pickle file
data.to_excel(PROJECT_DIR / "processed_data" / "bonds-analyzed.xlsx", index=False)
data.to_pickle(PROJECT_DIR / "processed_data" / "bonds-analyzed.pkl")