from dash import dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc


def create_date_picker(df):
    return dcc.DatePickerRange(
    id='date-picker-range',
    start_date=df['InvoiceDate'].min().strftime('%Y-%m-%d'),
    end_date=df['InvoiceDate'].max().strftime('%Y-%m-%d'),
    display_format='YYYY-MM-DD',
    style={'padding': '20px'}
    )

def create_country_dropdown(df):
    return dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in df['Country'].unique()],
    value=['United Kingdom'],  # Default to the UK as a list
    multi=True,
    placeholder="Select Country",
    style={ 'padding': '20px'}
    )

def create_cards(card_id, title):
    dbc.Card(
        id=card_id,
        children=[dbc.CardHeader(title), dbc.CardBody()],
        style={
            'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
            'textAlign': 'center',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'height': '100%'
        }
    )

def create_charts():
    return {
        "product_bar_chart": dvc.Vega(
            id='product-bar-chart', 
            spec={}, 
            style={'width': '100%', 'marginTop': '20px'}
            ),
        "country_pie_chart": dvc.Vega(
            id='country-pie-chart', 
            signalsToObserve=["selected_country"], 
            spec={}, style={'width': '100%', 'marginTop': '20px'}
            ),
        "stacked_chart": dvc.Vega(
            id='stacked-chart', 
            spec={}, 
            style={'width': '100%', 'marginTop': '20px'}
            ),
        "monthly_revenue_chart": dvc.Vega(
            id='monthly-revenue', 
            spec={}, 
            style={'width': '100%', 'marginTop': '20px'}
            )
    }