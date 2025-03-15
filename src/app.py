from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from flask_caching import Cache

from .data import df
from .components import date_picker_range, country_dropdown, cards_layout, product_bar_chart, country_pie_chart, stacked_chart, monthly_revenue_chart

# Initialization
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='RetaiLense Dashboard'
)
server = app.server

cache = Cache(
    app.server,
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'tmp'
    }
)

from . import callbacks # import callbacks after caching is initialized 

# Layout
app.layout = dbc.Container(
    fluid=True,  # Make the container fluid to span the full width
    style={'padding': '0', 'margin': '0'},  # Remove default padding 
    children=[
        dcc.Store(id='selected-country-store', data=None),
        dcc.Store(id='other-countries-store', data=[]),  # Stores list of "Others" countries
        dbc.Row(dbc.Col(html.H1(
            'RetaiLense',
            style={
                'backgroundColor': '#1E3A4C',
                'color': 'white',             
                'padding': '5px',
                'textAlign': 'center',
                'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
                'marginBottom': '0' 
            }
        ))),
        dbc.Row([
            dbc.Col(dbc.Row([
                html.Label('   Filters',
                           style={
                               'color': 'white',
                               'marginTop': '30px',
                               'marginLeft': '10px',
                               'fontSize': '22px', 
                               'fontWeight': 'bold', 
                               'fontFamily': 'inherit' # to match header font
                                }),
                                html.Hr(style={'borderBottom': '2px solid white', 'margin': '9px auto', 'width': '80%'}), # horizontal line 

                html.Label('   Date Range',
                           style={
                               'color': 'white',
                               'marginTop': '30px',
                               'marginLeft': '10px',
                               'fontSize': '18px', 
                               'fontFamily': 'inherit' # to match header font
                                }),
                html.Div(date_picker_range,
                                  style={'justifyContent': 'center', 'width': '100%', 'padding': '20px'}),
                html.Hr(style={'borderBottom': '2px solid white', 'margin': '9px auto', 'width': '80%'}), # horizontal line 
                html.Label('  Country', 
                           style={
                               'color': 'white',
                               'marginTop': '20px',
                               'marginLeft': '10px',
                               'fontSize': '18px', 
                               'fontFamily': 'inherit' # to match header font
                               }),
                html.Div(country_dropdown,
                                  style={'justifyContent': 'center', 'width': '100%', 'padding': '10px'}),
                html.Hr(style={'borderBottom': '2px solid white', 'margin': '9px auto', 'width': '80%'}), # horizontal line 
            ]), md=2, # Country dropdown on the left (adjust width)
            style={
                'backgroundColor': '#809DAF', 
                'padding': '10px',
                'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)'
                }
            ),  
            dbc.Col([
                # Cards in a grid layout
                cards_layout,
                dbc.Row([
                    dbc.Col(dbc.Container([monthly_revenue_chart], fluid=True), md=8), 
                    dbc.Col(dbc.Container([stacked_chart], fluid=True), md=4)
                ],
                style={'marginRight': '0', 'paddingRight': '0'}
                ),
                dbc.Row([
                    dbc.Col(dbc.Container([product_bar_chart], fluid=True), md=8),
                    dbc.Col(dbc.Container([country_pie_chart], fluid=True), md=4)
                ],
                style={'marginRight': '0', 'paddingRight': '0'}
                ),
            ], md=10,
            style={'marginRight': '0', 'paddingRight': '0'}
            )],
        style={'marginRight': '0', 'paddingRight': '0'}
        ),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P(" ", style={"font-size": "12px"}),
                    html.P("RetaiLense is an interactive dashboard designed to monitor and optimize eCommerce sales across international markets for a UK-based online retail company.",
                           style={"font-size": "12px"}),
                    html.P("Authors: Ashita Diwan @diwanashita, Gurmehak Kaur @gurmehak, Meagan Gardner @meagangardner, and Wai Ming Wong @waiming",
                           style={"font-size": "12px"}),
                    html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2025_9_RetaiLense",
                           target="_blank", style={"font-size": "12px"}),
                ],
                style={
                    'textAlign': 'center',  # Center-align text horizontally
                    'alignItems': 'center',  # Center-align children horizontally
                    'justifyContent': 'center',  # Center-align children vertically
                    'margin': '0 auto',  # Center the div itself horizontally
                    'paddingLeft': '20x'
                })
            ], md=12),
        ],
        style={'marginTop': '20px'} 
        ),
    ]
)

# Run the app
if __name__ == '__main__':
    app.run()