import pandas as pd
import pycountry
import lightningchart as lc
from lightningchart import Color, Dashboard, Themes

# Set the license key
lc.set_license(my_license_key)

# Load the dataset
file_path = 'owid-co2-data.csv'
data = pd.read_csv(file_path)

# Manual mapping for countries with names that don't match pycountry
manual_mapping = {
    'Russia': 'RUS',
    'Iran': 'IRN',
    'Syria': 'SYR',
    'Turkey': 'TUR',
    'Venezuela': 'VEN',
    'Tanzania': 'TZA',
    'Vietnam': 'VNM',
    # Add more mappings if needed
}

# Convert country names to ISO_A3 codes
def get_iso_a3(country_name):
    if country_name in manual_mapping:
        return manual_mapping[country_name]
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_3 if country else None
    except AttributeError:
        return None

def create_map_chart(dashboard, data_year, year, column_index, row_index):
    data_year.loc[:, 'ISO_A3'] = data_year['country'].apply(get_iso_a3)
    data_year = data_year.dropna(subset=['ISO_A3'])

    # Select relevant columns for the chart
    co2_data = data_year[['ISO_A3', 'co2']].rename(columns={'co2': 'value'}).to_dict(orient='records')

    # Create world map chart
    chart = dashboard.MapChart(column_index=column_index, row_index=row_index)

    # Set CO2 data
    chart.invalidate_region_values(co2_data)

    # Set color palette with finer divisions
    chart.set_palette_colors(
        steps=[
            {'value': 0.0001, 'color': Color('#e0f7fa')},  # Light cyan
            {'value': 1, 'color': Color('#80deea')},  # Cyan
            {'value': 10, 'color': Color('#4dd0e1')},  # Light blue
            {'value': 20, 'color': Color('#26c6da')},  # Darker blue
            {'value': 30, 'color': Color('#00bcd4')},  # Even darker blue
            {'value': 40, 'color': Color('#00acc1')},  # Dark cyan
            {'value': 50, 'color': Color('#0097a7')},  # Cyan green
            {'value': 70, 'color': Color('#00838f')},  # Green cyan
            {'value': 100, 'color': Color('#006064')},  # Dark green cyan
            {'value': 200, 'color': Color('#004d40')},  # Dark green
            {'value': 300, 'color': Color('#2e7d32')},  # Dark green
            {'value': 400, 'color': Color('#388e3c')},  # Green
            {'value': 500, 'color': Color('#43a047')},  # Light green
            {'value': 700, 'color': Color('#66bb6a')},  # Light green
            {'value': 900, 'color': Color('#9ccc65')},  # Green yellow
            {'value': 1000, 'color': Color('#d4e157')},  # Yellow
            {'value': 1500, 'color': Color('#fbc02d')},  # Yellow orange
            {'value': 2000, 'color': Color('#ffa000')},  # Dark orange
            {'value': 2500, 'color': Color('#ff8f00')},  # Orange
            {'value': 3000, 'color': Color('#ff6f00')},  # Dark orange red
            {'value': 3500, 'color': Color('#ff5722')},  # Red
            {'value': 4000, 'color': Color('#f4511e')},  # Dark red
            {'value': 4500, 'color': Color('#e64a19')},  # Very dark red
            {'value': 5000, 'color': Color('#d84315')},  # Deep red
            {'value': 6000, 'color': Color('#bf360c')},  # Brown red
            {'value': 7000, 'color': Color('#a3320c')},  # Dark brown red
            {'value': 8000, 'color': Color('#87281e')},  # Dark maroon
            {'value': 9000, 'color': Color('#6d211c')},  # Very dark maroon
            {'value': 11000, 'color': Color('#212121')}  # Black
        ],
        look_up_property='value',
        percentage_values=False
    )

    # Enable hover highlighting
    chart.set_highlight_on_hover(enabled=True)

    return chart

# Create a dashboard to arrange the charts
dashboard = Dashboard(
    rows=2,
    columns=2,
    theme=Themes.White
)

# Create and add map charts to the dashboard
create_map_chart(dashboard, data[data['year'] == 1990].copy(), 1990, column_index=0, row_index=0)
create_map_chart(dashboard, data[data['year'] == 2000].copy(), 2000, column_index=1, row_index=0)
create_map_chart(dashboard, data[data['year'] == 2010].copy(), 2010, column_index=0, row_index=1)
create_map_chart(dashboard, data[data['year'] == 2022].copy(), 2022, column_index=1, row_index=1)

# Open the dashboard
dashboard.open(live=True)
