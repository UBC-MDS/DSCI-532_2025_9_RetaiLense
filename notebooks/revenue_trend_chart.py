from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt

# Read CSV file 
df = pd.read_csv('data/processed/processed_data.csv')

# Ensure 'InvoiceDate' is converted to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create Month-Year column
df['MonthYear'] = df['InvoiceDate'].dt.strftime('%b-%Y')

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Monthly Revenue Dashboard"

# Layout with Date Range Picker and Country Dropdown
app.layout = dbc.Container([
    html.H1("RetaiLense Dashboard"),
    
    # Global filters
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['InvoiceDate'].min().strftime('%Y-%m-%d'),
            end_date=df['InvoiceDate'].max().strftime('%Y-%m-%d'),
            display_format='YYYY-MM-DD',
            style={'padding': '20px'}
        ),
        
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Country'].unique()],
            value=['United Kingdom'],  # Default to the UK as a list
            multi=True,
            placeholder="Select Country",
            style={'width': '50%', 'padding': '20px'}
        ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'}),
    
    # Monthly Revenue Chart
    dvc.Vega(id='monthly-revenue', spec={}),  # Empty chart initially
])

# Server side callbacks (reactivity)
@callback(
    Output('monthly-revenue', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_monthly_revenue_chart(start_date, end_date, selected_countries):
    # Filter the data based on selected date range and countries
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                     (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                     (df['Country'].isin(selected_countries))]
    
    # Create the Altair chart
    monthly_revenue_chart = alt.Chart(
        filtered_df.groupby('MonthYear')['Revenue'].sum().reset_index()
    ).mark_line(point=True).encode(
        x=alt.X('MonthYear:N', 
                sort=pd.to_datetime(filtered_df['MonthYear'].unique(), format='%b-%Y').sort_values().strftime('%b-%Y').tolist(), 
                title='Month-Year'),
        y=alt.Y('Revenue:Q', title='Total Revenue'),
        tooltip=['MonthYear:N', 'Revenue:Q']
    ).properties(
        title='Monthly Revenue Trend'
    )
    
    return monthly_revenue_chart.to_dict()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
