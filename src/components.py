from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd

from .data import df

# Date Picker Range
date_picker_range = dcc.DatePickerRange(
    id='date-picker-range',
    start_date=df['InvoiceDate'].min().strftime('%Y-%m-%d'),
    end_date=df['InvoiceDate'].max().strftime('%Y-%m-%d'),
    min_date_allowed=pd.to_datetime('2010-12-01'), 
    max_date_allowed=pd.to_datetime('2011-12-31'),
    display_format='YYYY-MM-DD',
    style={'width': '100%'},  # Set width to match the parent
)

# Country Dropdown
country_dropdown = dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in df['Country'].unique()],
    value=['United Kingdom'],  # Default to the UK as a list
    multi=True,
    placeholder="Select Country",
    style={'padding': '10px', 'font-size': '12px'}
)

# Cards
card_loyal_customer_ratio = dbc.Card(
    id='card-loyal-customer-ratio',
    style={
        'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
        'textAlign': 'center',        
        'display': 'flex',           
        'alignItems': 'center',       
        'justifyContent': 'center',  
        'height': '100%'      
    }
)

card_loyal_customer_sales = dbc.Card(
    id='card-loyal-customer-sales',
    style={
        'textAlign': 'center',  
        'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
        'display': 'flex',     
        'alignItems': 'center', 
        'justifyContent': 'center', 
        'height': '100%'               
    }
)

card_net_sales = dbc.Card(
    id='card-net-sales',
    style={
        'textAlign': 'center',
        'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
        'display': 'flex',  
        'alignItems': 'center',  
        'justifyContent': 'center',   
        'height': '100%'          
    }
)

card_total_returns = dbc.Card(
    id='card-total-returns',
    style={
        'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
        'textAlign': 'center',      
        'display': 'flex',           
        'alignItems': 'center',    
        'justifyContent': 'center',  
        'height': '100%'       
    }
)

# Layout for the cards
cards_layout = dbc.Row(
    [
        dbc.Col(card_loyal_customer_ratio, md=3),
        dbc.Col(card_loyal_customer_sales, md=3),
        dbc.Col(card_net_sales, md=3),
        dbc.Col(card_total_returns, md=3)
    ],
    style={'marginTop': '20px'}  # Add 20px space above the cards
)

# Charts
product_bar_chart = dvc.Vega(
    id='product-bar-chart',
    spec={},
    style={'width': '100%', 'marginTop': '20px'}
)

country_pie_chart = dvc.Vega(
    id='country-pie-chart',
    signalsToObserve=["selected_country"],
    spec={},
    style={'width': '100%', 'marginTop': '20px'}
)

stacked_chart = dvc.Vega(
    id='stacked-chart',
    spec={},
    style={'width': '100%', 'marginTop': '20px'}
)

monthly_revenue_chart = dvc.Vega(
    id='monthly-revenue', 
    spec={},
    style={'width': '100%', 'marginTop': '20px'}
)
