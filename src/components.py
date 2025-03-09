import dash_vega_components as dvc
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

from .datadata import df
import .callbacks 


#Component
date_picker_range = dcc.DatePickerRange(
    id='date-picker-range',
    start_date=df['InvoiceDate'].min().strftime('%Y-%m-%d'),
    end_date=df['InvoiceDate'].max().strftime('%Y-%m-%d'),
    display_format='YYYY-MM-DD',
    style={'padding': '20px'}
    )

country_dropdown = dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in df['Country'].unique()],
    value=['United Kingdom'],  # Default to the UK as a list
    multi=True,
    placeholder="Select Country",
    style={ 'padding': '20px'}
    )


# Cards with styling
card_loyal_customer_ratio = dbc.Card(
    id='card-loyal-customer-ratio',
    style={
        # 'backgroundColor': '#9CB4C3',  
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
        # 'backgroundColor': '#9CB4C3',  
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
        # 'backgroundColor': '#9CB4C3',  
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
        # 'backgroundColor': '#fbb4ae',  
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