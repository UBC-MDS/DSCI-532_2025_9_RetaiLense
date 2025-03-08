from dash import html, dcc
import dash_bootstrap_components as dbc
from components import create_date_picker, create_country_dropdown, create_cards, create_charts

def create_layout(df):
    date_picker = create_date_picker(df)
    country_dropdown = create_country_dropdown(df)
    charts = create_charts()

    cards_layout = dbc.Row(
        [
            dbc.Col(create_cards('card-loyal-customer-ratio', 'Loyal Customer Ratio'), md=3),
            dbc.Col(create_cards('card-loyal-customer-sales', 'Loyal Customer Sales'), md=3),
            dbc.Col(create_cards('card-net-sales', 'Net Sales'), md=3),
            dbc.Col(create_cards('card-total-returns', 'Total Returns'), md=3)
        ],
        style={'marginTop': '20px'}
    )

    return dbc.Container(
        fluid=True,
        style={'padding': '0', 'margin': '0'},
        children=[
            dcc.Store(id='selected-country-store', data=None),
            dcc.Store(id='other-countries-store', data=[]),
            dbc.Row(dbc.Col(html.H1('RetaiLense', style={'backgroundColor': '#1E3A4C', 'color': 'white', 'padding': '5px', 'textAlign': 'center', 'marginBottom': '0'}))),
            dbc.Row([
                dbc.Col(dbc.Row([
                    html.Label('Filters', style={'color': 'white', 'marginTop': '30px', 'marginLeft': '10px', 'fontSize': '22px', 'fontWeight': 'bold'}),
                    html.Label('Date Range', style={'color': 'white', 'marginTop': '30px', 'marginLeft': '10px', 'fontSize': '18px'}),
                    date_picker,
                    html.Label('Country', style={'color': 'white', 'marginTop': '20px', 'marginLeft': '10px', 'fontSize': '18px'}),
                    country_dropdown
                ]), md=2, style={'backgroundColor': '#809DAF', 'padding': '10px', 'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)'}),
                dbc.Col([
                    cards_layout,
                    dbc.Row([
                        dbc.Col(dbc.Container([charts["monthly_revenue_chart"]], fluid=True), md=8),
                        dbc.Col(dbc.Container([charts["stacked_chart"]], fluid=True), md=4)
                    ]),
                    dbc.Row([
                        dbc.Col(dbc.Container([charts["product_bar_chart"]], fluid=True), md=8),
                        dbc.Col(dbc.Container([charts["country_pie_chart"]], fluid=True), md=4)
                    ]),
                ], md=10)
            ])
        ]
    )
