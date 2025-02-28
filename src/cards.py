from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt

# Read the data
df = pd.read_csv('data/processed/processed_data.csv')

# Ensure 'InvoiceDate' is converted to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create Month-Year column
df['MonthYear'] = df['InvoiceDate'].dt.strftime('%b-%Y')


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get unique countries from the dataframe
country_columns = [{'label': country, 'value': country} for country in df['Country'].unique()]

# Create the cards (initially empty, they will be updated dynamically)
card_loyal_customer_ratio = dbc.Card(id='card-loyal-customer-ratio')
card_loyal_customer_sales = dbc.Card(id='card-loyal-customer-sales')
card_net_sales = dbc.Card(id='card-net-sales')
card_total_returns = dbc.Card(id='card-total-returns')


# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1('RetaiLense'))),
    
    # Row for the dropdown and the cards
    dbc.Row([
        dbc.Col(dbc.Row([
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
        ]), md=3),  # Country dropdown on the left (adjust width)
        dbc.Col([
            # Cards in a grid layout
            dbc.Row([
                dbc.Col(card_loyal_customer_ratio, md=3),  # Each card takes up 3 columns (out of 12)
                dbc.Col(card_loyal_customer_sales, md=3),
                dbc.Col(card_net_sales, md=3),
                dbc.Col(card_total_returns, md=3)
            ])
        ], md=9)  # This column takes up 9 columns (rest of the row)
    ])

    
])



# Callback to update the cards dynamically based on the selected country
@callback(
    Output('card-loyal-customer-ratio', 'children'),
    Output('card-loyal-customer-sales', 'children'),
    Output('card-net-sales', 'children'),
    Output('card-total-returns', 'children'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def update_cards(start_date, end_date, selected_countries):

    # Filter the data based on selected date range and countries
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                     (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                     (df['Country'].isin(selected_countries))]

    # Calculate the loyal customer ratio
    loyal_customers = filtered_df['CustomerID'].nunique()
    non_loyal_customers = filtered_df[filtered_df['CustomerID'].isna()]
    total_non_loyal_customers = non_loyal_customers['InvoiceNo'].nunique()  # Count unique InvoiceNo for non-loyal customers
    total_unique_customers = loyal_customers + total_non_loyal_customers
    loyal_customers_ratio = loyal_customers / total_unique_customers
    loyal_customer_ratio_value = f"{round(loyal_customers_ratio * 100, 2)}%"

    # Calculate the loyal customer sales
    non_blank_customer_ids = filtered_df[filtered_df['CustomerID'].notna()]
    total_sales = non_blank_customer_ids['Revenue'].sum()
    loyal_customer_sales_value = f"${total_sales:,.2f}"

    # Calculate net sales
    net_sales_value = f"${filtered_df['Revenue'].sum():,.2f}"

    # Calculate total returns
    returns = filtered_df[filtered_df['Revenue'] < 0]
    total_returns_value = f"${returns['Revenue'].sum():,.2f}"

    # Create the content for each card
    card_loyal_customer_ratio_content = [
        dbc.CardHeader('Loyal Customer Ratio'),
        dbc.CardBody(loyal_customer_ratio_value)
    ]
    card_loyal_customer_sales_content = [
        dbc.CardHeader('Loyal Customer Sales'),
        dbc.CardBody(loyal_customer_sales_value)
    ]
    card_net_sales_content = [
        dbc.CardHeader('Net Sales'),
        dbc.CardBody(net_sales_value)
    ]
    card_total_returns_content = [
        dbc.CardHeader('Total Returns'),
        dbc.CardBody(total_returns_value)
    ]
    
    return card_loyal_customer_ratio_content, card_loyal_customer_sales_content, card_net_sales_content, card_total_returns_content



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)