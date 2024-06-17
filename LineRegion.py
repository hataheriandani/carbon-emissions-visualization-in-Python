import pandas as pd
import lightningchart as lc
import time

# Read the license key for LightningChart
lc.set_license(my_license_key)

# Load the dataset
file_path = 'owid-co2-data.csv'
data = pd.read_csv(file_path)

# List of countries and regions to include in the chart
entities = ['World', 'China', 'Europe', 'Oceania', 'United Kingdom', 'United States', 'India', 'Asia', 'Germany', 'France', 'Africa']

# Create the chart
chart = lc.ChartXY(
    theme=lc.Themes.White,
    title='CO2 Emissions Over the Years'
)

colors = [
    lc.Color(0, 0, 0),       # Black for World
    lc.Color(255, 0, 0),     # Red
    lc.Color(0, 255, 0),     # Green
    lc.Color(0, 0, 255),     # Blue
    lc.Color(255, 165, 0),   # Orange
    lc.Color(128, 0, 128),   # Purple
    lc.Color(0, 255, 255),   # Cyan
    lc.Color(75, 0, 130),    # Indigo
    lc.Color(238, 130, 238), # Violet
    lc.Color(139, 69, 19),   # Brown
    lc.Color(128, 128, 128)  # Grey
]

line_series_dict = {}
for i, entity in enumerate(entities):
    line_series = chart.add_line_series()
    line_series.set_name(entity)
    line_series.set_line_color(colors[i])
    line_series.set_line_thickness(2)
    line_series_dict[entity] = line_series

x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')

y_axis = chart.get_default_y_axis()
y_axis.set_title('CO2 Emissions (Million Metric Tons)')

chart.add_legend(x=15, y=35, data=chart)
chart.open(live=True)

# Add data points with a delay to simulate real-time drawing
for index, row in data.iterrows():
    if row['country'] in entities:
        year = row['year']
        emission = row['co2']
        if pd.notna(year) and pd.notna(emission):
            emission_million = emission / 1e6  # Convert to million metric tons
            print(f"Adding data for {row['country']}: Year={year}, Emission={emission_million}")
            line_series_dict[row['country']].add(year, emission_million)
            time.sleep(0.005)  # 0.005 second delay between each data point

chart.close()

