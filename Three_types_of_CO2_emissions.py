import pandas as pd
import lightningchart as lc

# Read the license key for LightningChart
lc.set_license(my_license_key)

# Load the dataset
file_path = 'owid-co2-data.csv'
data = pd.read_csv(file_path)

# Filter data for the world
world_data = data[data['country'] == 'World']

# Ensure 'year' and CO2 columns are in the correct format
world_data['year'] = pd.to_numeric(world_data['year'], errors='coerce')
world_data['co2'] = pd.to_numeric(world_data['co2'], errors='coerce')
world_data['co2_including_luc'] = pd.to_numeric(world_data['co2_including_luc'], errors='coerce')
world_data['land_use_change_co2'] = pd.to_numeric(world_data['land_use_change_co2'], errors='coerce')

# Drop rows with NaN values
world_data = world_data.dropna(subset=['year', 'co2', 'co2_including_luc', 'land_use_change_co2'])

# Extract the relevant columns
years = world_data['year'].tolist()
total_emissions = world_data['co2_including_luc'].tolist()
fossil_fuel_emissions = world_data['co2'].tolist()
land_use_change_emissions = world_data['land_use_change_co2'].tolist()

# Convert emissions to billion metric tons
total_emissions = [e / 1e9 for e in total_emissions]
fossil_fuel_emissions = [e / 1e9 for e in fossil_fuel_emissions]
land_use_change_emissions = [e / 1e9 for e in land_use_change_emissions]

# Create the chart
chart = lc.ChartXY(
    theme=lc.Themes.White,
    title='Global CO2 Emissions Over the Years (Fossil Fuels Land-Use Change and Total Emissions)'
)
# Add the total emissions series
total_series = chart.add_line_series()
total_series.add(years, total_emissions)
total_series.set_name('Total (fossil fuels and land-use change)')
total_series.set_line_color(lc.Color(255, 0, 128))  # Pink color
total_series.set_line_thickness(2)  # Set line width
# Add the fossil fuel emissions series
fossil_fuel_series = chart.add_line_series()
fossil_fuel_series.add(years, fossil_fuel_emissions)
fossil_fuel_series.set_name('Fossil fuels')
fossil_fuel_series.set_line_color(lc.Color(255, 165, 0))  # Orange color
fossil_fuel_series.set_line_thickness(2)  # Set line width
# Add the land-use change emissions series
land_use_series = chart.add_line_series()
land_use_series.add(years, land_use_change_emissions)
land_use_series.set_name('Land-use change')
land_use_series.set_line_color(lc.Color(0, 128, 0))  # Green color
land_use_series.set_line_thickness(2)  # Set line width
# Customize x-axis
x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_interval(min(world_data['year']), max(world_data['year']))
# Customize y-axis
y_axis = chart.get_default_y_axis()
y_axis.set_title('CO2 Emissions (Billion Metric Tons)')

chart.add_legend(x=25, y=40, data=chart)

chart.open()
