
#  Import appropriate libraries
import pandas as pd
import matplotlib.pyplot as plt

#  Save overdose data and GINI data file paths.
gini_data_path = "../data/nys_gini_coefficient_by_county.csv"
overdose_data_path = "../data/nys_overdose_deaths_involving_opioids_by_county.csv"

#  Write data to dataframes
gini_df = pd.read_csv(gini_data_path)
overdose_df = pd.read_csv(overdose_data_path)

# Merge dataframes
merged_df = pd.merge(
    left=overdose_df,
    right=gini_df,
    left_on='name',
    right_on='name'
)

# Remove " County" from 'name' column
merged_df['name'] = merged_df['name'].replace(' County', '', regex=True)

# Clean commas from population column
merged_df["population"] = merged_df["population"].replace(',', '', regex=True)

# Convert population from str to int
merged_df = merged_df.astype({'population': 'int'})

# Calculates overdose rate percent (for visualization)
merged_df['od rate percent'] = (merged_df['overdoses'] / merged_df['population']) * 100

# Plots the Scatterplot
plt.scatter(merged_df['gini index'], merged_df['od rate percent'])
plt.xlabel('GINI Coefficient')
plt.ylabel('Overdose Rate (%)')
plt.title('Scatterplot of Overdose Rates to GINI Coefficient Indices per County')
plt.show()
