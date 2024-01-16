import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from pathlib import Path

PROJECT_DIR = Path().resolve()

# =============================================================================
# PIE CHARTS FOR THE "PORTFOLIO DISTRIBUTION"
# =============================================================================

# Create an arbitrary DataFrame
data = {
    'Issuer_Name': ['BondA', 'BondB', 'BondC', 'BondD'],
    'ExpRet': [3.5, 4.2, 3.8, 5.1],
    'Rating': ['AAA', 'AA', 'BBB', 'A'],
    'Country': ['USA', 'UK', 'Germany', 'Japan']
}

bonds_df = pd.DataFrame(data)

# Custom color for the pie charts
base_color = '#3AEFCC'

# Generate a color palette with different shades
country_palette = sns.light_palette(base_color, n_colors=len(bonds_df['Country'].unique()))
rating_palette = sns.light_palette(base_color, n_colors=len(bonds_df['Rating'].unique()))

# Create a pie chart for Country distribution
country_counts = bonds_df['Country'].value_counts()
fig, ax = plt.subplots()
ax.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', startangle=90, colors=country_palette)
ax.set_title('Distribution of Bonds Across Countries')

# Add legend
ax.legend(country_counts.index, loc='upper left', bbox_to_anchor=(1, 1))
plt.show()

# Create a pie chart for Rating distribution
rating_counts = bonds_df['Rating'].value_counts()
fig, ax = plt.subplots()
ax.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=90, colors=rating_palette)
ax.set_title('Distribution of Bonds Across Ratings')

# Add legend
ax.legend(rating_counts.index, loc='upper left', bbox_to_anchor=(1, 1))
plt.show()

# =============================================================================
# INFLATION FORECASTS USING OECD DATA
# =============================================================================

oecd = pd.read_excel(PROJECT_DIR / 'original_data/oecd_inflation_forecasts.xlsx')

# Filter the dataframe for the selected countries
selected_countries = ["United States", "G20", "Russia", "Brazil", "South Africa"]
filtered_oecd = oecd[oecd['Country'].isin(['United States', 'G20', 'Russia', 'Brazil', 'South Africa'])]

# Create a new colormap instance
cmap = cm.get_cmap('winter')

# Create a new figure
plt.figure(figsize=(10, 6))

# Plot the data for each country
for i, country in enumerate(selected_countries):
    country_data = filtered_oecd[filtered_oecd['Country'] == country]
    
    # Get a color from the colormap
    color = cmap(i / len(selected_countries))
    
    # Plot solid line for 2018-2023
    plt.plot(country_data.columns[1:7], country_data.values[0][1:7], label=country, color=color, linewidth=1.5)
    
    # Plot dashed line for 2023-2025
    plt.plot(country_data.columns[6:9], country_data.values[0][6:9], linestyle='dashed', color=color, linewidth=1.5)

# Add a legend
plt.legend()

# Add title and labels
plt.title('Inflation Forecasts (%, YoY)', fontsize=16)

# Add gridlines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Set x-ticks and labels
plt.xticks(ticks=range(2018, 2026), labels=range(2018, 2026))
# Set y-ticks and labels with % sign
y_ticks = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:.0f}%'.format(y) for y in y_ticks])

# Show the plot
plt.show()