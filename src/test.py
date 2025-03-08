from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from data import load_data
from callbacks import register_callbacks

df = load_data()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Monthly Revenue Dashboard"

app.layout = create_layout(df)

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run()