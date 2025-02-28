from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt

# read data
df = pd.read_csv('data/processed/processed_data.csv')

# create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "RetaiLense Dashboard"

def plot_top_products_revenue(data, n_products=10):
    """
    Create a bar chart of top products by revenue using Altair.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Input DataFrame containing 'Description' and 'Revenue' columns
    n_products : int, optional
        Number of top products to display (default: 10)
        
    Returns:
    --------
    dict
        Vega-Lite specification for the bar chart
    """
    
    # group description by revenue then get the top 10 products
    product_revenue = (data
        .groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(n_products)
        .reset_index())
    
    # plot the bar chart
    bar_chart = alt.Chart(product_revenue).mark_bar().encode(
        x=alt.X('Revenue:Q', title='Revenue'),
        y=alt.Y('Description:N', sort='-x', title='Product Description'),
        color=alt.Color('Description:N', scale=alt.Scale(scheme='pastel2')),
        tooltip=['Description', 'Revenue']
    ).properties(
        title=f'Top {n_products} Products by Revenue',
        width=600,
        height=300
    )
    
    return bar_chart.to_dict()

app.layout = html.Div([
    html.H1("RetaiLense Dashboard"),
    
    # create div for bar chart using dash_vega_components
    dvc.Vega(
        id='product-bar-chart',
        spec=plot_top_products_revenue(df)
    ),
])

# run the app
if __name__ == '__main__':
    app.server.run(debug=True)