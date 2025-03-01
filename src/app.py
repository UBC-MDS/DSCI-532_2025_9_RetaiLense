from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt

# Read CSV file 
df = pd.read_csv('data/processed/processed_data.csv')

# Ensure 'InvoiceDate' is converted to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create Month-Year column
df['MonthYear'] = df['InvoiceDate'].dt.strftime('%b-%Y')

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Monthly Revenue Dashboard"

# Create the cards (initially empty, they will be updated dynamically).
card_loyal_customer_ratio = dbc.Card(id='card-loyal-customer-ratio')
card_loyal_customer_sales = dbc.Card(id='card-loyal-customer-sales')
card_net_sales = dbc.Card(id='card-net-sales')
card_total_returns = dbc.Card(id='card-total-returns')


@callback(
    Output('monthly-revenue', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_monthly_revenue_chart(start_date, end_date, selected_countries):
    """
    Generates an Altair line chart showing monthly revenue trends over time.

    Parameters:
    start_date (str): The start date selected in the date picker.
    end_date (str): The end date selected in the date picker.
    selected_countries (list): List of selected countries for filtering.

    Returns:
    dict: Vega-Lite specification of the Altair chart.
    """
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                     (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                     (df['Country'].isin(selected_countries))]
    
    monthly_revenue_chart = alt.Chart(
        filtered_df.groupby('MonthYear')['Revenue'].sum().reset_index()
    ).mark_line(point=True).encode(
        x=alt.X('MonthYear:N', 
                sort=pd.to_datetime(filtered_df['MonthYear'].unique(), format='%b-%Y').sort_values().strftime('%b-%Y').tolist(), 
                title='Month-Year'),
        y=alt.Y('Revenue:Q', title='Total Revenue'),
        tooltip=['MonthYear:N', 'Revenue:Q']
    ).properties(
        title='Monthly Revenue Trend',
    )
    
    return monthly_revenue_chart.to_dict()


@callback(
    Output('waterfall-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_waterfall_chart(start_date, end_date, selected_countries):
    """
    Generates a waterfall chart to visualize gross revenue, refunds, and net revenue.

    Parameters:
    start_date (str): The start date selected in the date picker.
    end_date (str): The end date selected in the date picker.
    selected_countries (list): List of selected countries for filtering.

    Returns:
    dict: Vega-Lite specification of the Altair chart.
    """
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                     (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                     (df['Country'].isin(selected_countries))]
    
    gross_revenue = filtered_df.loc[filtered_df['Quantity'] > 0, 'Revenue'].sum()
    refund = filtered_df.loc[filtered_df['Quantity'] < 0, 'Revenue'].sum()
    net_revenue = gross_revenue + refund

    working_df = pd.DataFrame({
        'Category': ['Gross Revenue', 'Refund', 'Net Revenue'],
        'Value': [gross_revenue, refund, net_revenue]
    })

    working_df['Start'] = working_df['Value'].cumsum().shift(1).fillna(0)
    working_df['End'] = working_df['Start'] + working_df['Value']
    
    bars = alt.Chart(working_df).mark_bar().encode(
        x=alt.X('Category:N', title='Category'),
        y=alt.Y('Start:Q', title='Revenue'),
        y2='End:Q',
        color=alt.Color('Value:Q', scale=alt.Scale(scheme='redblue')),
        tooltip=['Category', 'Value']
    )

    return bars.to_dict()


@callback(
    Output('product-bar-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_top_products_revenue(start_date, end_date, selected_countries, n_products=10):
    """
    Generates a bar chart of the top products by revenue.

    Parameters:
    start_date (str): The start date selected in the date picker.
    end_date (str): The end date selected in the date picker.
    selected_countries (list): List of selected countries for filtering.
    n_products (int, optional): Number of top products to display. Defaults to 10.

    Returns:
    dict: Vega-Lite specification of the Altair chart.
    """
    filtered_df = df[
        (df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
        (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
        (df['Country'].isin(selected_countries))
    ]
    
    product_revenue = (filtered_df
        .groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(n_products)
        .reset_index())
    
    bar_chart = alt.Chart(product_revenue).mark_bar().encode(
        x=alt.X('Revenue:Q', title='Revenue (£)')
    ).properties(
        title=f'Top {n_products} Products by Revenue'
    )
    
    return bar_chart.to_dict()


if __name__ == '__main__':
    app.run()
