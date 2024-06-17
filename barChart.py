import pandas as pd
import lightningchart as lc
import pycountry
from lightningchart import Dashboard, Themes

# Set the license key
lc.set_license(my_license_key)

# Load data from CSV file
file_path = 'owid-co2-data.csv'
data = pd.read_csv(file_path)

# Dictionary for country names to abbreviations
def get_country_code(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        # Manual check for countries that may not be in pycountry
        manual_codes = {
            'Russia': 'RUS',
            'Turkey': 'TUR',
            'United Arab Emirates': 'ARE',
            'South Africa': 'ZAF',
            'South Korea': 'KOR',
            'Brunei': 'BRN',
            'Greenland': 'GRL',
            'Libya': 'LBY',
            'Singapore': 'SGP'
        }
        return manual_codes.get(country_name, country_name[:3].upper())

# Filter data for the year 2022
data_2022 = data[data['year'] == 2022]

# Complete list of non-country regions to remove
non_countries = [
    'World', 'Asia', 'Asia (GCP)', 'Europe', 'Europe (GCP)', 'European Union (27)', 'North America', 'North America (GCP)', 'South America',
    'Africa', 'Africa (GCP)', 'Oceania', 'Upper-middle-income countries', 'High-income countries', 'South America (GCP)',
    'Lower-middle-income countries', 'Low-income countries', 'International transport', 'North America (excl. USA)', 'International shipping',
    'Non-OECD (GCP)', 'OECD (GCP)', 'Asia (excl. China and India)', 'European Union (28)', 'International aviation',
    'Europe (excl. EU-28)', 'South America (GCP)', 'Oceania (GCP)', 'Africa (excl. South Africa)',
    'Asia (excl. China and India)', 'Europe (excl. EU-27)', 'International transport',
    'Lower-middle-income economies', 'Low-income economies', 'Non-OECD members', 'OECD members',
    'Other Africa', 'Other Asia', 'Other Europe', 'Rest of world', 'Upper-middle-income economies',
    'Middle East', 'Middle East (GCP)', 'Other non-OECD'
]

# Remove non-country regions from the data
data_countries_2022 = data_2022[~data_2022['country'].isin(non_countries)]

# Select top 30 countries by CO2 emissions
top_30_countries = data_countries_2022.nlargest(30, 'co2')

# Select top 30 countries by CO2 emissions per capita
top_30_countries_per_capita = data_countries_2022.nlargest(30, 'co2_per_capita')

# Prepare data for the first chart
chart_data_total = [{'category': get_country_code(row['country']), 'value': row['co2']} for _, row in top_30_countries.iterrows()]

# Prepare data for the second chart
chart_data_per_capita = [{'category': get_country_code(row['country']), 'value': row['co2_per_capita']} for _, row in top_30_countries_per_capita.iterrows()]

# Create dashboard
dashboard = Dashboard(
    rows=2,
    columns=1,
    theme=Themes.White
)

# Create bar chart for the first chart
chart_total = dashboard.BarChart(
    column_index=0,
    row_index=0,
    column_span=1,
    row_span=1
)
chart_total.set_title('Top 30 CO2 Emitting Countries - Year 2022')
chart_total.set_sorting('disabled')
chart_total.set_data(chart_data_total)

# Create bar chart for the second chart
chart_per_capita = dashboard.BarChart(
    column_index=0,
    row_index=1,
    column_span=1,
    row_span=1
)
chart_per_capita.set_title('Top 30 CO2 Emitting Countries per Capita - Year 2022')
chart_per_capita.set_sorting('disabled')
chart_per_capita.set_data(chart_data_per_capita)

# Open the dashboard
dashboard.open()
