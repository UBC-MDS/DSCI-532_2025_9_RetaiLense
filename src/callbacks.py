from dash import Output, Input, callback, html
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd

from data import df
from components import date_picker_range, country_dropdown, card_loyal_customer_ratio, card_loyal_customer_sales
from components import card_net_sales,cards_layout,product_bar_chart,country_pie_chart,stacked_chart,monthly_revenue_chart

