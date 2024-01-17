import pandas as pd
import numpy as np
from pathlib import Path
import pycountry
import matplotlib.pyplot as plt
import seaborn as sns
from utils.get_country import get_country
from utils.correct_avg_and_3m import correct_avg_and_3m

# set the project directory for easy access to the data
PROJECT_DIR = Path().resolve()

# load the data
bonds   = pd.read_excel(PROJECT_DIR / 'original_data/bonds.xlsx')
cds_10y = pd.read_excel(PROJECT_DIR / 'original_data/cds_by_countries.xlsx', sheet_name='10 years')
cds_5y  = pd.read_excel(PROJECT_DIR / 'original_data/cds_by_countries.xlsx', sheet_name='5 years')
cds_2y  = pd.read_excel(PROJECT_DIR / 'original_data/cds_by_countries.xlsx', sheet_name='2 years')

# =============================================================================
# CREDIT DEFAULT SWAPS SPREAD DATA CLEANING
# =============================================================================

# apply the function to fix the mistaken 'Avg' and '3M +/-' values
cds_10y = correct_avg_and_3m(cds_10y)
cds_5y = correct_avg_and_3m(cds_5y)
cds_2y = correct_avg_and_3m(cds_2y)

# add relevant suffixes to the column names to make merged dataframe more readable
cds_10y = cds_10y.add_suffix('_10y')
cds_5y = cds_5y.add_suffix('_5y')
cds_2y = cds_2y.add_suffix('_2y')

# merge the CDS dataframes
merged_cds = cds_10y.merge(cds_5y, left_on='Name_10y', right_on='Name_5y').merge(cds_2y, left_on='Name_10y', right_on='Name_2y')

# =============================================================================
# BONDS DATA CLEANING
# =============================================================================

## Issues with Maturity:
# delete bonds with maturity date is older than November 24, 2023
bonds['Maturity'] = pd.to_datetime(bonds['Maturity'], format='%d.%m.%Y', errors='coerce')
date = pd.to_datetime('2023-11-24')
bonds = bonds[bonds['Maturity'] >= date]

# Drop rows where the 'Maturity' year is greater than 2054
# otherwise, it even extends to year 2122
bonds = bonds[bonds['Maturity'].dt.year <= 2054]

## Issues with Empty Columns:
# drop the empty columns
bonds.drop(columns=['BVAL Ask Yld', 'BVAL Bid Yld'], inplace=True)

## Issues with Yld to Mty (Ask) and Yld to Mty (Bid):
# Drop rows where either 'Yld to Mty (Ask)' or 'Yld to Mty (Bid)' is missing
bonds = bonds.dropna(subset=['Yld to Mty (Ask)', 'Yld to Mty (Bid)'])

# Drop the rows where 'Yld to Mty (Ask)' or 'Yld to Mty (Bid)' is "#N/A Field Not Applicable"
values_to_drop = ['#N/A Field Not Applicable']
bonds = bonds[~bonds[["Yld to Mty (Ask)", "Yld to Mty (Bid)"]].isin(values_to_drop).any(axis=1)]

## Add Country Pairings to Merge with CDS Data:
# apply the function to create the 'Country' column
bonds['Country'] = bonds['Issuer Name'].apply(get_country)

# read the missing pairings data to fill the missing values in the 'Country' column
missing_issuers_country_pairings = pd.read_excel('original_data/missing_issuers_country_pairings.xlsx', index_col=0)

# set 'Issuer Name' as the index in both dataframes for filling the missing values
bonds.set_index('Issuer Name', inplace=True)
missing_issuers_country_pairings.set_index('Issuer Name', inplace=True)

# now fill the missing values in the 'Country' column and reset the index
bonds['Country'] = bonds['Country'].fillna(missing_issuers_country_pairings['Country'])
bonds.reset_index(inplace=True)

# don't need this dataframe anymore, so delete it to free up memory
del missing_issuers_country_pairings

# finally, merge CDS data and bonds data into a single dataframe
final_df = bonds.merge(merged_cds, left_on='Country', right_on='Name_10y', how='left')

# to check if there any trouble with the merge or data in general
final_df.info()

## final cleaning
# remove the '*' character and convert to numeric
for col in ['Spread_10y', 'Spread_5y', 'Spread_2y']:
    final_df[col] = pd.to_numeric(final_df[col].str.replace('*', ''), errors='coerce')

# remove the '+' character and convert to numeric
final_df['Change_5y'] = pd.to_numeric(final_df['Change_5y'].str.replace('+', ''), errors='coerce')

# replace "not rated" and "NaN" to None
final_df['BBG Composite'] = final_df['BBG Composite'].replace('NR', np.nan)
final_df['Series'] = final_df['Series'].replace('#N/A Field Not Applicable', np.nan)

# export the data to Excel and pickle files
final_df.to_excel(PROJECT_DIR / "processed_data" / "bonds-data.xlsx", index=False)
final_df.to_pickle(PROJECT_DIR / "processed_data" / "bonds-data.pkl")