import pandas as pd
import numpy as np
from pathlib import Path
import pycountry
import matplotlib.pyplot as plt
import seaborn as sns
#import pyarrow as pa
#import pyarrow.parquet as pq

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

def correct_avg_and_3m(df):
    """
    This function corrects the 'Avg' and '3M +/-' columns in a dataframe.
    If 'Avg' is not between 'Low' and 'High', but '3M +/-' is   , it swaps 'Avg' and '3M +/-'.

    Parameters:
    df (pandas.DataFrame): The dataframe to correct.

    Returns:
    df (pandas.DataFrame): The corrected dataframe.
    """
    
    # to iterate over the rows
    for i, row in df.iterrows():
        # if everything is correct, continue
        if row['Low'] <= row['Avg'] <= row['High']:
            continue
        # if values are incorrect
        elif row['Low'] <= row['3M +/-'] <= row['High']:
            df.loc[i, 'Avg'], df.loc[i, '3M +/-'] = row['3M +/-'], row['Avg']
    
    return df

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

# delete bonds with maturity date is older than November 24, 2023
bonds['Maturity'] = pd.to_datetime(bonds['Maturity'], format='%d.%m.%Y', errors='coerce')
date = pd.to_datetime('2023-11-24')
bonds = bonds[bonds['Maturity'] >= date]

# drop the empty columns
bonds.drop(columns=['BVAL Ask Yld', 'BVAL Bid Yld'], inplace=True)

def get_country(issuer_name):
    """
    This function takes an issuer name as input and returns the country name if it is found in the issuer name.
    It uses the pycountry module to get a list of all countries.

    Parameters:
    issuer_name (str): The name of the issuer.

    Returns:
    str: The name of the country if found in the issuer name, None otherwise.
    """
    
    # convert the issuer name to lowercase for case insensitive comparison
    issuer_name = issuer_name.lower()
    
    # iterate over all countries provided by the pycountry module
    for country in pycountry.countries:
        # convert the country name to lowercase before checking for a match
        # this ensures that the comparison is case insensitive
        if country.name.lower() in issuer_name:
            # if a match is found, return the name of the country
            return country.name
    
    # if no match is found, return None
    return None

# apply the function to create the 'Country' column
bonds['Country'] = bonds['Issuer Name'].apply(get_country)

# read the missing pairings data to fill the missing values in the 'Country' column
missing_issuers_country_pairings = pd.read_excel('missing_issuers_country_pairings.xlsx', index_col=0)

# set 'Issuer Name' as the index in both dataframes for filling the missing values
bonds.set_index('Issuer Name', inplace=True)
missing_issuers_country_pairings.set_index('Issuer Name', inplace=True)

# now fill the missing values in the 'Country' column and reset the index
bonds['Country'] = bonds['Country'].fillna(missing_issuers_country_pairings['Country'])
bonds.reset_index(inplace=True)

# don't need this dataframe anymore, so delete it to free up memory
del missing_issuers_country_pairings

# finally, merge CDS data and bonds data into a single dataframe
final_df = bonds.merge(merged_cds, left_on='Country', right_on='Name_10y')

# export the data to Excel
final_df.to_excel(PROJECT_DIR / "processed_data" / "bonds-data.xlsx")