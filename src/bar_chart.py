from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt

# read data
df = pd.read_csv('data/processed/processed_data.csv')

# Ensure 'InvoiceDate' is converted to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create Month-Year column
df['MonthYear'] = df['InvoiceDate'].dt.strftime('%b-%Y')

# create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "RetaiLense Dashboard"

app.layout = html.Div([
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
    
    # create div for bar chart using dash_vega_components
    dvc.Vega(
        id='product-bar-chart',
        spec={}  # Empty spec that will be filled by callback
    ),
])

@callback(
    Output('product-bar-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_top_products_revenue(start_date, end_date, selected_countries, n_products=10):
    """
    Create a bar chart of top products by revenue using Altair.
    
    Parameters:
    -----------
    start_date : str
        Start date for filtering
    end_date : str
        End date for filtering
    selected_countries : list
        List of selected countries for filtering
    n_products : int, optional
        Number of top products to display (default: 10)
        
    Returns:
    --------
    dict
        Vega-Lite specification for the bar chart
    """
    
    # Filter the data based on selected date range and countries
    filtered_df = df[
        (df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
        (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
        (df['Country'].isin(selected_countries))
    ]
    
    # group description by revenue then get the top products
    product_revenue = (filtered_df
        .groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(n_products)
        .reset_index())
    
    # plot the bar chart
    bar_chart = alt.Chart(product_revenue).mark_bar().encode(
        x=alt.X('Revenue:Q', title='Revenue (£)'),
        y=alt.Y('Description:N', sort='-x', title='Product Description'),
        color=alt.Color('Description:N', scale=alt.Scale(scheme='pastel2')),
        tooltip=['Description', 'Revenue']
    ).properties(
        title=f'Top {n_products} Products by Revenue',
        width=600,
        height=300
    )
    
    return bar_chart.to_dict()

# run the app
if __name__ == '__main__':
    app.run(debug=True)