from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from .data import df

# Date Picker Range
date_picker_range = dcc.DatePickerRange(
    id='date-picker-range',
    start_date=df['InvoiceDate'].min().strftime('%Y-%m-%d'),
    end_date=df['InvoiceDate'].max().strftime('%Y-%m-%d'),
    display_format='YYYY-MM-DD',
    style={'padding': '20px'}
)

# Country Dropdown
country_dropdown = dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in df['Country'].unique()],
    value=['United Kingdom'],  # Default to the UK as a list
    multi=True,
    placeholder="Select Country",
    style={ 'padding': '20px'}
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

# Layout
# layout = dbc.Container(
#     fluid=True,  # Make the container fluid to span the full width
#     style={'padding': '0', 'margin': '0'},  # Remove default padding 
#     children=[
#         dcc.Store(id='selected-country-store', data=None),
#         dcc.Store(id='other-countries-store', data=[]),  # Stores list of "Others" countries
#         dbc.Row(dbc.Col(html.H1(
#             'RetaiLense',
#             style={
#                 'backgroundColor': '#1E3A4C',
#                 'color': 'white',             
#                 'padding': '5px',
#                 'textAlign': 'center',
#                 'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
#                 'marginBottom': '0' 
#             }
#         ))),
#         dbc.Row([
#             dbc.Col(dbc.Row([
#                 html.Label('   Filters',
#                            style={
#                                'color': 'white',
#                                'marginTop': '30px',
#                                'marginLeft': '10px',
#                                'fontSize': '22px', 
#                                'fontWeight': 'bold', 
#                                'fontFamily': 'inherit' # to match header font
#                                 }),
#                 html.Label('   Date Range',
#                            style={
#                                'color': 'white',
#                                'marginTop': '30px',
#                                'marginLeft': '10px',
#                                'fontSize': '18px', 
#                                'fontFamily': 'inherit' # to match header font
#                                 }),
#                 date_picker_range,
#                 html.Label('  Country', 
#                            style={
#                                'color': 'white',
#                                'marginTop': '20px',
#                                'marginLeft': '10px',
#                                'fontSize': '18px', 
#                                'fontFamily': 'inherit' # to match header font
#                                }),
#                 country_dropdown,
#             ]), md=2, # Country dropdown on the left (adjust width)
#             style={
#                 'backgroundColor': '#809DAF', 
#                 'padding': '10px',
#                 'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)'
#                 }
#             ),  
#             dbc.Col([
#                 # Cards in a grid layout
#                 cards_layout,
#                 dbc.Row([
#                     dbc.Col(dbc.Container([monthly_revenue_chart], fluid=True), md=8), 
#                     dbc.Col(dbc.Container([stacked_chart], fluid=True), md=4)
#                 ],
#                 style={'marginRight': '0', 'paddingRight': '0'}
#                 ),
#                 dbc.Row([
#                     dbc.Col(dbc.Container([product_bar_chart], fluid=True), md=8),
#                     dbc.Col(dbc.Container([country_pie_chart], fluid=True), md=4)
#                 ],
#                 style={'marginRight': '0', 'paddingRight': '0'}
#                 ),
#             ], md=10,
#             style={'marginRight': '0', 'paddingRight': '0'}
#             )],
#         style={'marginRight': '0', 'paddingRight': '0'}
#         ),
#         dbc.Row([
#             dbc.Col([
#                 html.Div([
#                     html.P(" ", style={"font-size": "12px"}),
#                     html.P("RetaiLense is an interactive dashboard designed to monitor and optimize eCommerce sales across international markets for a UK-based online retail company.",
#                            style={"font-size": "12px"}),
#                     html.P("Authors: Ashita Diwan @diwanashita, Gurmehak Kaur @gurmehak, Meagan Gardner @meagangardner, and Wai Ming Wong @waiming",
#                            style={"font-size": "12px"}),
#                     html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2025_9_RetaiLense",
#                            target="_blank", style={"font-size": "12px"}),
#                     html.P("Last updated on Feb 28, 2025",
#                            style={"font-size": "12px"}),
#                 ])
#             ], md=12),
#         ]),
#     ]
# )