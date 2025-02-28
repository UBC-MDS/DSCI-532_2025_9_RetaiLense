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



# Server side callbacks (reactivity)
@callback(
    Output('monthly-revenue', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_monthly_revenue_chart(start_date, end_date, selected_countries):
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
        title='Monthly Revenue Trend'
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
    waterfall_chart = (bars + text).properties(width=600, height=400, title="Revenue Waterfall Chart" )
    
    return waterfall_chart.to_dict()

@callback(
    Output('product-bar-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
def plot_top_products_revenue(start_date, end_date, selected_countries, n_products=10):
    """
    Create a bar chart of top products by revenue using Altair.
    
    Parameters:
    -----------
    start_date : str
        Start date for filtering
    end_date : str
        End date for filtering
    selected_countries : list
        List of selected countries for filtering
    n_products : int, optional
        Number of top products to display (default: 10)
        
    Returns:
    --------
    dict
        Vega-Lite specification for the bar chart
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
        color=alt.Color('Description:N', scale=alt.Scale(scheme='pastel2')),
        tooltip=['Description', 'Revenue']
    ).properties(
        title=f'Top {n_products} Products by Revenue',
        width=600,
        height=300
    )
    
    return bar_chart.to_dict()

# Define the function to create the pie chart
def plot_top_countries_pie_chart():
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
        title="Top 5 Countries Outside of the UK"
    )
    
    return pie_chart.to_dict()




# Layout with Date Range Picker and Country Dropdown
app.layout = dbc.Container([
    html.H1("RetaiLense Dashboard"),
    
    # Global filters
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['InvoiceDate'].min().strftime('%Y-%m-%d'),
            end_date=df['InvoiceDate'].max().strftime('%Y-%m-%d'),
            display_format='YYYY-MM-DD',
            style={'padding': '20px'}
        ),
        
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Country'].unique()],
            value=['United Kingdom'],  # Default to the UK as a list
            multi=True,
            placeholder="Select Country",
            style={'width': '50%', 'padding': '20px'}
        ),
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'}),
    
    # create div for bar chart using dash_vega_components
    dvc.Vega(
        id='product-bar-chart',
        spec={}  # Empty spec that will be filled by callback
    ),

    # Monthly Revenue Chart
    dvc.Vega(
        id='monthly-revenue', 
        spec={}
    ),  # Empty chart initially

    dvc.Vega(
        id='country-pie-chart',
        spec=plot_top_countries_pie_chart()  # Pass the Altair chart spec (dict format)
    ),

    # Create a div for the pie chart using dash_vega_components
    dvc.Vega(
        id='waterfall-chart',
        spec={}  # Pass the Altair chart spec (dict format)
    ),
])

# Run the app
if __name__ == '__main__':
    app.run()
