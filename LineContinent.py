import pandas as pd
import lightningchart as lc
import time

# Read the license key for LightningChart
lc.set_license(my_license_key)

# Load the dataset
file_path = 'owid-co2-data.csv'
data = pd.read_csv(file_path)

# List of countries and regions to include in the chart, including Americas
entities = ['Oceania', 'Americas', 'Africa', 'Europe', 'Asia', 'World']

# Create the chart
chart = lc.ChartXY(
    theme=lc.Themes.White,
    title='CO2 emissions over the years by continent'
)

# Define colors for each entity
colors = [
    lc.Color(0, 0, 255),     # Blue for Oceania
    lc.Color(255, 165, 0),   # Orange for Americas
    lc.Color(255, 255, 0),   # Yellow for Africa
    lc.Color(0, 255, 0),     # Green for Europe
    lc.Color(255, 0, 0),     # Red for Asia
    lc.Color(0, 0, 0)        # Black for World
]

# Create a line series for each entity
line_series_dict = {}
for i, entity in enumerate(entities):
    line_series = chart.add_line_series()
    line_series.set_name(entity)
    line_series.set_line_color(colors[i])
    line_series.set_line_thickness(2)
    line_series_dict[entity] = line_series

# Customize x-axis
x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')

# Customize y-axis
y_axis = chart.get_default_y_axis()
y_axis.set_title('CO2 Emissions (Million Metric Tons)')

# Add a legend to the chart
chart.add_legend(
    horizontal=False,
    title='Regions',
    x=12 , y=42,
    data=chart
)

# Function to add data points
def add_data(entity, year, emission):
    if pd.notna(year) and pd.notna(emission):
        emission_million = emission / 1e6  # Convert to million metric tons
        line_series_dict[entity].add(year, emission_million)

# Aggregate data for North America and South America
north_america_data = data[(data['country'] == 'North America') & (data['year'].notna())]
south_america_data = data[(data['country'] == 'South America') & (data['year'].notna())]

# Combine North and South America data
combined_america_data = pd.concat([north_america_data, south_america_data])
americas_data = combined_america_data.groupby('year')['co2'].sum().reset_index()

# Open the chart
chart.open(live=True)

# Add data points for the rest of the entities
for index, row in data.iterrows():
    if row['country'] in entities and row['country'] != 'Americas':
        add_data(row['country'], row['year'], row['co2'])

# Add data points for Americas
for index, row in americas_data.iterrows():
    add_data('Americas', row['year'], row['co2'])

# Close the chart
chart.close()
