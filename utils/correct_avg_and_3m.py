import pandas as pd

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