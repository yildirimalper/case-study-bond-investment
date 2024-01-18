import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import FuncFormatter

PROJECT_DIR = Path().resolve()

# Assuming df is your DataFrame with bond data
data = pd.read_excel(PROJECT_DIR / "processed_data/bonds-data.xlsx")

# Convert Maturity column to datetime
data["Maturity"] = pd.to_datetime(data["Maturity"])

# Calculate time to maturity in years using a specific date
data["Years to Maturity"] = round((data["Maturity"] - pd.to_datetime('2023-11-24')).dt.days / 365)
data["Years to Maturity (Unrounded)"] = (data["Maturity"] - pd.to_datetime('2023-11-24')).dt.days / 365

# Subset data for Country=="United States"
data_us = data[data["Country"] == "United States"]

# Group by maturity year and calculate the mean of yields
data_mean = data_us.groupby("Years to Maturity").agg({"YTM - Ask": "mean", "YTM - Bid": "mean"}).reset_index()
data_mean = data_mean.sort_values(by='Years to Maturity')

# Apply spline interpolation
x_smooth = np.linspace(data_mean['Years to Maturity'].min(), data_mean['Years to Maturity'].max(), 300)
spl_ask = make_interp_spline(data_mean['Years to Maturity'], data_mean['YTM - Ask'], k=3)
spl_bid = make_interp_spline(data_mean['Years to Maturity'], data_mean['YTM - Bid'], k=3)
y_smooth_ask = spl_ask(x_smooth)
y_smooth_bid = spl_bid(x_smooth)

# Plot the smoothed curve with specified line colors
plt.plot(x_smooth, y_smooth_ask, color='blue', label='YTM Ask')
plt.plot(x_smooth, y_smooth_bid, color='black', label='YTM Bid')

filtered_ytm = data_us[(data_us['YTM - Ask'] > 0) & (data_us['YTM - Ask'] < 8)]
plt.scatter(filtered_ytm['Years to Maturity (Unrounded)'], filtered_ytm['YTM - Ask'], color='deepskyblue', alpha=0.4, s=25)

plt.rcParams['figure.figsize'] = (10, 6)  # Set the figure size
plt.xticks(fontsize=12)  # Customize font size for x-axis ticks
plt.yticks(fontsize=12)  # Customize font size for y-axis ticks
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0f}%'))
plt.title('Bond Yields with November 24, 2023 Sample', fontsize=16)
plt.xlabel('Time to Maturity', fontsize=14)
plt.ylabel('Yield to Maturity', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)

# Save the figure for inclusion in your presentation
# plt.savefig('figures/yield_curve.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()