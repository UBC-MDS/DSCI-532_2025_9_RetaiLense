from dash import Dash
import dash_bootstrap_components as dbc
from components import layout
import callbacks  # This import is necessary to register the callbacks

# Initialization
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='RetaiLense Dashboard'
)
server = app.server

# Layout
app.layout = layout

# Run the app
if __name__ == '__main__':
    app.run(debug=False)