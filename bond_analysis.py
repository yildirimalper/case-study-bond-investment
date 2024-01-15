import pandas as pd
import numpy as np
from pathlib import Path
from utils.bond_math import calculate_bond_price, calculate_macaulay_duration, calculate_modified_duration, calculate_bond_convexity, calculate_dv01

# set the project directory for easy access to the data
PROJECT_DIR = Path().resolve()

# load the data
data = pd.read_excel(PROJECT_DIR / "processed_data" / "bonds-data.xlsx")

# Convert Maturity column to datetime, and find the years to maturity
data["Maturity"] = pd.to_datetime(data["Maturity"])
data["Years to Maturity"] = (data["Maturity"] - pd.to_datetime('2023-11-24')).dt.days / 365
