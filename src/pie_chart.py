from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt


# Read your CSV file
df = pd.read_csv('data/processed/processed_data.csv')

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "RetaiLense Dashboard"

# Define the function to create the pie chart
def plot_top_countries_pie_chart(df):
    # Exclude the United Kingdom
    df_no_uk = df[df['Country'] != 'United Kingdom']
    
    # Count the occurrences of each country and reset index
    country_counts = df_no_uk['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']
    
    # Calculate percentage
    country_counts['Percentage'] = round((country_counts['Count'] / country_counts['Count'].sum()) * 100, 0)
    
    # Get top 5 countries
    country_counts = country_counts.head(5)
    
    # Create the Altair pie chart with percentages
    pie_chart = alt.Chart(country_counts).mark_arc().encode(
        theta=alt.Theta(field="Percentage", type="quantitative"),  # Use Percentage for the arc size
        color=alt.Color(field="Country", type="nominal", 
                        scale=alt.Scale(scheme='pastel1')),  # Use a categorical color scheme
        tooltip=['Country', 'Percentage']  # Show Percentage in the tooltip
    ).properties(
        title="Top 5 Countries Outside of the UK"
    )
    
    return pie_chart.to_dict()

app.layout = html.Div([
    html.H1("RetaiLense Dashboard"),
    
    # Create a div for the pie chart using dash_vega_components
    dvc.Vega(
        id='country-pie-chart',
        spec=plot_top_countries_pie_chart(df)  # Pass the Altair chart spec (dict format)
    ),
])

# Run the app
if __name__ == '__main__':
    app.server.run(debug=True)