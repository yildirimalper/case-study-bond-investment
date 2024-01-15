import pycountry
import pandas as pd

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