from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt

# Read CSV file 
df = pd.read_csv('data/processed/processed_data.csv')

# Create Month-Year column
df['MonthYear'] = pd.to_datetime(df['InvoiceDate']).dt.strftime('%b-%Y')

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Monthly Revenue Dashboard"

# Define function to create the line chart
def plot_monthly_revenue_chart(df):
    monthly_revenue_chart = alt.Chart(
    df.groupby('MonthYear')['Revenue'].sum().reset_index()
    ).mark_line(point=True).encode(
        x=alt.X('MonthYear:N', 
        sort=pd.to_datetime(df['MonthYear'].unique(), format='%b-%Y').sort_values().strftime('%b-%Y').tolist(), title='Month-Year'),
        y=alt.Y('Revenue:Q', title='Total Revenue'),
    tooltip=['MonthYear:N', 'Revenue:Q']
    ).properties(
        title='Monthly Revenue Trend'
)
    
    return monthly_revenue_chart.to_dict(format="vega")  

app.layout = html.Div([
    html.H1("RetaiLense Dashboard"),
    
    # Monthly Revenue Chart
    dvc.Vega(
        id='monthly-revenue',
        spec=plot_monthly_revenue_chart(df)  # Pass Altair chart spec as a dictionary
    ),
])

# Run the app
if __name__ == '__main__':
    app.server.run(debug=True)
