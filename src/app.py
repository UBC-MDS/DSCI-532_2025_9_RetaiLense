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
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Monthly Revenue Dashboard"



# Create the cards (initially empty, they will be updated dynamically).
card_loyal_customer_ratio = dbc.Card(id='card-loyal-customer-ratio')
card_loyal_customer_sales = dbc.Card(id='card-loyal-customer-sales')
card_net_sales = dbc.Card(id='card-net-sales')
card_total_returns = dbc.Card(id='card-total-returns')


# Server side callbacks (reactivity)
@callback(
    Output('monthly-revenue', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_monthly_revenue_chart(start_date, end_date, selected_countries):
    """
    Generates a monthly revenue line chart using Altair.

    Parameters:
    - start_date (str): The start date selected in the date picker.
    - end_date (str): The end date selected in the date picker.
    - selected_countries (list): List of selected countries for filtering.

    Returns:
    - dict: Altair chart specification (JSON format).
    """
    # Filter the data based on selected date range and countries
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                     (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                     (df['Country'].isin(selected_countries))]
    
    # Create the Altair chart
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
        width=400
    )
    
    return monthly_revenue_chart.to_dict()

# Define the function to create the pie chart (as you already have it)
@callback(
    Output('waterfall-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_waterfall_chart(start_date, end_date, selected_countries):
    """
    Creates a waterfall chart showing Gross Revenue, Refunds, and Net Revenue.

    Parameters:
    - start_date (str): The start date selected in the date picker.
    - end_date (str): The end date selected in the date picker.
    - selected_countries (list): List of selected countries for filtering.

    Returns:
    - dict: Altair chart specification (JSON format).
    """
    # Filter the data based on selected date range and countries
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                       (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                       (df['Country'].isin(selected_countries))]
    
    # Compute Gross Revenue (sum of revenue where quantity > 0)
    gross_revenue = filtered_df.loc[filtered_df['Quantity'] > 0, 'Revenue'].sum()

    # Compute Refund (sum of revenue where quantity < 0)
    refund = filtered_df.loc[filtered_df['Quantity'] < 0, 'Revenue'].sum()

    # Compute Net Revenue (Gross Revenue + Refund)
    net_revenue = gross_revenue + refund

    # Create the final DataFrame
    working_df = pd.DataFrame({
        'Category': ['Gross Revenue', 'Refund', 'Net Revenue'],
        'Value': [gross_revenue, refund, net_revenue]
    })


    # Define explicit category order
    category_order = working_df['Category'].tolist()
    
    # Add an index column to enforce order
    working_df['Index'] = range(len(working_df))  # Assign numerical order explicitly

    # Convert Category column to categorical with correct order
    working_df['Category'] = pd.Categorical(working_df['Category'], categories=category_order, ordered=True)

    # Compute cumulative values properly
    working_df['Start'] = working_df['Value'].cumsum().shift(1).fillna(0)
    working_df['End'] = working_df['Start'] + working_df['Value']

    # Force Net Revenue to start from zero
    working_df.loc[working_df['Category'] == 'Net Revenue', 'Start'] = 0
    working_df.loc[working_df['Category'] == 'Net Revenue', 'End'] = working_df['Value']

    # Define colors
    working_df['Color'] = working_df['Value'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')

    # Create a mapping of Index to Category labels
    category_labels = {i: cat for i, cat in enumerate(working_df['Category'])}

    # Create the waterfall chart
    bars = alt.Chart(working_df).mark_bar().encode(
        x=alt.X('Index:O', title='Category', sort=list(working_df['Index']),  
                axis=alt.Axis(labelExpr=f"datum.value == 0 ? '{category_labels[0]}' : " +
                                       f"datum.value == 1 ? '{category_labels[1]}' : " +
                                       f"datum.value == 2 ? '{category_labels[2]}' : ''",
                              labelAngle=-45)),  # Replaces 0,1,2 with actual labels
        y=alt.Y('Start:Q', title='Revenue'),
        y2='End:Q',
        color=alt.Color('Color:N', scale=alt.Scale(domain=['Increase', 'Decrease'], range=['green', 'red']), legend=None),
        tooltip=['Category', 'Value']
    )

    # Add text labels
    text = alt.Chart(working_df).mark_text(dy=-10, size=12).encode(
        x='Index:O',
        y='End:Q',
        text=alt.Text('Value:Q', format=',.0f')
    )

    # Combine bars and labels
    waterfall_chart = (bars + text).properties( width=300,
                                            #    height=300, 
                                               title="Revenue Waterfall Chart" 
    )

    return waterfall_chart.to_dict()

@callback(
    Output('product-bar-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_top_products_revenue(start_date, end_date, selected_countries, n_products=10):
    """
    Generates a bar chart for top products by revenue.

    Parameters:
    - start_date (str): The start date selected in the date picker.
    - end_date (str): The end date selected in the date picker.
    - selected_countries (list): List of selected countries for filtering.
    - n_products (int): Number of top products to display (default: 10).

    Returns:
    - dict: Altair chart specification (JSON format).
    """
    # Filter the data based on selected date range and countries
    filtered_df = df[
        (df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
        (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
        (df['Country'].isin(selected_countries))
    ]
    
    # group description by revenue then get the top products
    product_revenue = (filtered_df
        .groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(n_products)
        .reset_index())
    
    # plot the bar chart
    bar_chart = alt.Chart(product_revenue).mark_bar().encode(
        x=alt.X('Revenue:Q', title='Revenue (£)'),
        y=alt.Y('Description:N', sort='-x', title='Product Description'),
        color=alt.Color('Description:N', scale=alt.Scale(scheme='pastel2'), legend=None),
        tooltip=['Description', 'Revenue']
    ).properties(
        title=f'Top {n_products} Products by Revenue',
        width=400,
        height=300
    )
    
    return bar_chart.to_dict()

# Define the function to create the pie chart
def plot_top_countries_pie_chart():
    """
    Creates a pie chart showing the top 5 countries (excluding the UK) by sales.

    Returns:
    - dict: Altair chart specification (JSON format).
    """
    # Exclude the United Kingdom
    df_no_uk = df[df['Country'] != 'United Kingdom']
    
    # Count the occurrences of each country and reset index
    country_counts = df_no_uk['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']
    
    # Calculate percentage
    country_counts['Percentage'] = round((country_counts['Count'] / country_counts['Count'].sum()) * 100, 0)
    
    # Get top 5 countries
    country_counts = country_counts.head(5)
    
    # Create the Altair pie chart with percentages
    pie_chart = alt.Chart(country_counts).mark_arc().encode(
        theta=alt.Theta(field="Percentage", type="quantitative"),  # Use Percentage for the arc size
        color=alt.Color(field="Country", type="nominal", 
                        scale=alt.Scale(scheme='pastel1')),  # Use a categorical color scheme
        tooltip=['Country', 'Percentage']  # Show Percentage in the tooltip
    ).properties(
        title="Top 5 Countries Outside of the UK",
        width=400,  # Allow width to scale dynamically
    )
    
    return pie_chart.to_dict()



# Callback to update the cards dynamically based on the selected country
@callback(
    Output('card-loyal-customer-ratio', 'children'),
    Output('card-loyal-customer-sales', 'children'),
    Output('card-net-sales', 'children'),
    Output('card-total-returns', 'children'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def update_cards(start_date, end_date, selected_countries):
    """
    Updates the key financial metric cards based on the selected date range and countries.

    Parameters:
    - start_date (str): The start date selected in the date picker.
    - end_date (str): The end date selected in the date picker.
    - selected_countries (list): List of selected countries for filtering.

    Returns:
    - tuple: A tuple containing the updated contents for four dashboard cards:
        1. Loyal Customer Ratio (percentage)
        2. Loyal Customer Sales (total revenue from known customers)
        3. Net Sales (total revenue including refunds)
        4. Total Returns (negative revenue from refunds)
    """
    # Filter the data based on selected date range and countries
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                     (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                     (df['Country'].isin(selected_countries))]

    # Calculate the loyal customer ratio
    loyal_customers = filtered_df['CustomerID'].nunique()
    non_loyal_customers = filtered_df[filtered_df['CustomerID'].isna()]
    total_non_loyal_customers = non_loyal_customers['InvoiceNo'].nunique()  # Count unique InvoiceNo for non-loyal customers
    total_unique_customers = loyal_customers + total_non_loyal_customers
    
    if total_unique_customers == 0:
        loyal_customers_ratio = 0
    else:
        loyal_customers_ratio = loyal_customers / total_unique_customers
    loyal_customer_ratio_value = f"{round(loyal_customers_ratio * 100, 2)}%"

    # Calculate the loyal customer sales
    non_blank_customer_ids = filtered_df[filtered_df['CustomerID'].notna()]
    total_sales = non_blank_customer_ids['Revenue'].sum()
    loyal_customer_sales_value = f"${total_sales:,.2f}"

    # Calculate net sales
    net_sales_value = f"${filtered_df['Revenue'].sum():,.2f}"

    # Calculate total returns
    returns = filtered_df[filtered_df['Revenue'] < 0]
    total_returns_value = f"${returns['Revenue'].sum():,.2f}"

    # Create the content for each card
    card_loyal_customer_ratio_content = [
        dbc.CardHeader('Loyal Customer Ratio'),
        dbc.CardBody(loyal_customer_ratio_value)
    ]
    card_loyal_customer_sales_content = [
        dbc.CardHeader('Loyal Customer Sales'),
        dbc.CardBody(loyal_customer_sales_value)
    ]
    card_net_sales_content = [
        dbc.CardHeader('Net Sales'),
        dbc.CardBody(net_sales_value)
    ]
    card_total_returns_content = [
        dbc.CardHeader('Total Returns'),
        dbc.CardBody(total_returns_value)
    ]
    
    return card_loyal_customer_ratio_content, card_loyal_customer_sales_content, card_net_sales_content, card_total_returns_content


# Layout with Date Range Picker and Country Dropdown.
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1('RetaiLense'))),

    dbc.Row([
        dbc.Col(dbc.Row([
            html.Label('Date Range:'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df['InvoiceDate'].min().strftime('%Y-%m-%d'),
                end_date=df['InvoiceDate'].max().strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
                style={'padding': '20px'}
            ),
            
            html.Label('Select Countries:'),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in df['Country'].unique()],
                value=['United Kingdom'],  # Default to the UK as a list
                multi=True,
                placeholder="Select Country",
                style={ 'padding': '20px'}
            ),
        ]), md=3),  # Country dropdown on the left (adjust width)
        dbc.Col([
            # Cards in a grid layout
            dbc.Row([
                dbc.Col(card_loyal_customer_ratio, md=3), 
                dbc.Col(card_loyal_customer_sales, md=3),
                dbc.Col(card_net_sales, md=3),
                dbc.Col(card_total_returns, md=3)
            ]),
            dbc.Row([
                        dbc.Col(dbc.Container([dvc.Vega(
                            id='monthly-revenue', 
                            spec={}
                        )]), md=6),  
                        dbc.Col(dbc.Container([dvc.Vega(
                            id='country-pie-chart',
                            spec=plot_top_countries_pie_chart() 
                        )]), md=6)
            ]),
            dbc.Row([ dbc.Col(dbc.Container([dvc.Vega(
                            id='product-bar-chart',
                            spec={}  
                        )]), md=8), 
                        dbc.Col(dbc.Container([dvc.Vega(
                            id='waterfall-chart',
                            spec={}
                        )]), md=4)
            ]),
        ], md=9) 
    ]),

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
                html.P("Last updated on Feb 28, 2025",
                       style={"font-size": "12px"}),
            ])
        ], md=12),
    ]),
])

# Run the app
if __name__ == '__main__':
    app.run()