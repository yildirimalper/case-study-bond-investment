import pandas as pd
import numpy as np
from pathlib import Path
import pycountry
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
from difflib import get_close_matches
# pip install blpapi --index-url=https://bcms.bloomberg.com/pip/simple/
# pip install xbbg
# pip install pycountry
# pip install scapy
# pip install googlesearch-python beautifulsoup4 requests
# !python -m spacy download en_core_web_sm

# set the project directory for easy access to the data
PROJECT_DIR = Path().resolve()

# load the data
bonds   = pd.read_excel(PROJECT_DIR / 'bonds.xlsx')
cds_10y = pd.read_excel(PROJECT_DIR / 'cds_by_countries.xlsx', sheet_name='10 years')
cds_5y  = pd.read_excel(PROJECT_DIR / 'cds_by_countries.xlsx', sheet_name='5 years')
cds_2y  = pd.read_excel(PROJECT_DIR / 'cds_by_countries.xlsx', sheet_name='2 years')

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

cds_10y = correct_avg_and_3m(cds_10y)
cds_5y = correct_avg_and_3m(cds_5y)
cds_2y = correct_avg_and_3m(cds_2y)

# =============================================================================
# BONDS DATA CLEANING
# =============================================================================

# Delete rows with maturity date is older than today
bonds['Maturity'] = pd.to_datetime(bonds['Maturity'], errors='coerce')
today = pd.to_datetime('today')
older_than_today = bonds[bonds['Maturity'] < today]

# drop the empty columns
bonds.drop(columns=['BVAL Ask Yld', 'BVAL Bid Yld'], inplace=True)










# =============================================================================

# initialize the geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

def get_country(issuer_name):
    # Convert the issuer name to lowercase
    issuer_name = issuer_name.lower()
    
    for country in pycountry.countries:
        # Convert the country name to lowercase before checking for a match
        if country.name.lower() in issuer_name:
            return country.name
    return None

# Apply the function to the 'Issuer Name' column
bonds['Country'] = bonds['Issuer Name'].apply(get_country)

# Apply the function to the 'Issuer Name' column
bonds['Country'] = bonds['Issuer Name'].apply(get_country)

# =============================================================================
# Exploratory Data Analysis
# =============================================================================

# Create overlapping histograms
plt.hist(bonds['Yld to Mty (Ask)'], bins=30, alpha=0.5, label='Ask')
plt.hist(bonds['Yld to Mty (Bid)'], bins=30, alpha=0.5, label='Bid')
plt.legend(loc='upper right')
plt.show()

# Count the instances where bid > ask and ask > bid
bid_gt_ask = (bonds['Yld to Mty (gBid)'] > bonds['Yld to Mty (Ask)']).sum()
ask_gt_bid = (bonds['Yld to Mty (Ask)'] > bonds['Yld to Mty (Bid)']).sum()

print(f'Bid > Ask: {bid_gt_ask}')
print(f'Ask > Bid: {ask_gt_bid}')


print(bonds['Issuer Name'].value_counts())
# Federal Home Loan Banks                                        1983
# Federal Farm Credit Banks Funding Corp                         1606
# Federal Home Loan Mortgage Corp                                 414


# Filter the dataframe
bonds_fhlb = bonds[bonds['Issuer Name'] == 'Federal Home Loan Banks']

# Create overlapping histograms
plt.hist(bonds_fhlb['Yld to Mty (Ask)'], bins=30, alpha=0.5, label='Ask')
plt.hist(bonds_fhlb['Yld to Mty (Bid)'], bins=30, alpha=0.5, label='Bid')
plt.legend(loc='upper right')
plt.show()


# Convert the columns to float
bonds['Yld to Mty (Ask)'] = pd.to_numeric(bonds['Yld to Mty (Ask)'], errors='coerce')
bonds['Yld to Mty (Bid)'] = pd.to_numeric(bonds['Yld to Mty (Bid)'], errors='coerce')


# Filter the dataframe
bonds_fhlb = bonds[(bonds['Issuer Name'] == 'Federal Home Loan Banks') & 
                   (bonds['Yld to Mty (Ask)'].between(-10, 10)) & 
                   (bonds['Yld to Mty (Bid)'].between(-10, 10))]

# Create overlapping histograms
plt.hist(bonds_fhlb['Yld to Mty (Ask)'], bins=30, alpha=0.5, label='Ask')
plt.hist(bonds_fhlb['Yld to Mty (Bid)'], bins=30, alpha=0.5, label='Bid')
plt.legend(loc='upper right')
plt.show()

# Convert the 'Maturity' column to datetime
bonds['Maturity'] = pd.to_datetime(bonds['Maturity'], errors='coerce')

# Find the minimum value
min_maturity = bonds['Maturity'].min()

print(min_maturity)

# Get the current date
today = pd.to_datetime('today')

# Find rows where the Maturity date is older than today
older_than_today = bonds[bonds['Maturity'] < today]

print(older_than_today)

# =============================================================================

# Create a list of unique values in the 'Name' column
countries = cds_2y['Name'].unique()

# Function to match issuer names to countries
def get_country(issuer_name):
    for country in pycountry.countries:
        if country in issuer_name:
            return country.name
    return None

def find_country(issuer_name):
    matches = get_close_matches(issuer_name, countries)
    return matches[0] if matches else None

# Apply the function to create the 'Country' column
bonds['Country'] = bonds['Issuer Name'].apply(find_country)

# =============================================================================

nlp = spacy.load("en_core_web_sm")

# Function to extract country using spaCy
def extract_country(issuer_name):
    doc = nlp(issuer_name)
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE stands for Geopolitical Entity
            return ent.text
    return None

# Apply the function to create the 'Country' column
bonds['Country'] = bonds['Issuer Name'].apply(extract_country)

# =============================================================================
from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Sample data
# Replace with your actual data
countries = cds_10y['Name'].unique()  # Replace with your actual list of countries
observations = bonds['Issuer Name'].unique()

# Function to perform Google search and web scraping
def search_and_scrape(issue_name):
    query = issue_name + " Wikipedia"

# Perform Google search and get the first result
    search_results = search(query)
    first_result = next(search_results, None)

    if first_result:
        # Fetch and parse the first search result
        response = requests.get(first_result)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    else:
        return None

# Loop through each observation
for observation in observations:
    # Search and scrape text data from Wikipedia
    scraped_text = search_and_scrape(observation)

    if scraped_text:
        # Check if any country is mentioned in the scraped text
        country_mentioned = next((country for country in countries if country in scraped_text), None)

# Print or use the results as needed
        print(f"Issue: {observation}")
        print(f"Scraped Text: {scraped_text}")
        print(f"Country Mentioned: {country_mentioned}")
        print("\n")
    else:
        print(f"No search result found for '{observation}' on Wikipedia.\n")