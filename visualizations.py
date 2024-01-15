import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
