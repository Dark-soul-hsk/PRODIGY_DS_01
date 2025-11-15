import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np


POPULATION_FILE = r"C:\Users\Hemant Sri Kumar\Desktop\Prodigy\Task_01\API_SP.POP.TOTL_DS2_en_csv_v2_130083.csv"
LATEST_YEAR = '2024'


def millions_formatter(x, pos):
    if x >= 1e9:
        return f'{x/1e9:.1f}B'
    return f'{x/1e6:.0f}M'


pop_df = (
    pd.read_csv(POPULATION_FILE, skiprows=4)
    .drop(columns=['Unnamed: 69'])
)


year_cols = [col for col in pop_df.columns if col.isdigit() and int(col) >= 2000]


melted_pop_df = pop_df.melt(
    id_vars=['Country Name'], 
    value_vars=year_cols,
    var_name='Year', 
    value_name='Population'
)


melted_pop_df['Population'] = pd.to_numeric(melted_pop_df['Population'], errors='coerce')
melted_pop_df['Year'] = melted_pop_df['Year'].astype(int)


top_10_names = (
    melted_pop_df[melted_pop_df['Year'] == int(LATEST_YEAR)]
    .sort_values(by='Population', ascending=False)
    ['Country Name']
    .head(10)
    .tolist()
) 


plot_data = melted_pop_df[melted_pop_df['Country Name'].isin(top_10_names)].dropna(subset=['Population'])


plt.figure(figsize=(12, 7))


for entity in top_10_names:
    entity_data = plot_data[plot_data['Country Name'] == entity]
    plt.plot(entity_data['Year'], entity_data['Population'], label=entity)


plt.title(f'Population Trend of Top 10 Entities in {LATEST_YEAR} (2000-2024)')
plt.xlabel('Year')
plt.ylabel('Population')
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Entity', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()


plt.show()