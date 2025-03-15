from dash import Output, Input, callback, State, html
import pandas as pd
import altair as alt
import dash_bootstrap_components as dbc
from textwrap import wrap

from .data import df
from .app import cache


@callback(
    Output('monthly-revenue', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
@cache.memoize()
def plot_monthly_revenue_chart(start_date, end_date, selected_countries):
    """
    Generates an interactive line chart showing the monthly revenue trend 
    for the selected countries within the specified date range.

    Parameters:
    ----------
    start_date : str
        The selected start date from the date picker (in YYYY-MM-DD format).
    end_date : str
        The selected end date from the date picker (in YYYY-MM-DD format).
    selected_countries : list
        A list of selected countries used to filter the data.

    Returns:
    -------
    dict
        A JSON-encoded Altair chart specification representing the monthly 
        revenue trend.
    """
    # Filter the data based on selected date range and countries
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                     (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                     (df['Country'].isin(selected_countries))]
    
    # Create the Altair chart
    monthly_revenue_chart = alt.Chart(
        filtered_df.groupby('MonthYear')['Revenue'].sum().reset_index()
    ).mark_line(point=True, color='#361162').encode(
        x=alt.X('MonthYear:N', 
                sort=pd.to_datetime(filtered_df['MonthYear'].unique(), format='%b-%Y').sort_values().strftime('%b-%Y').tolist(), 
                title='Month-Year'),
        y=alt.Y('Revenue:Q', title='Total Revenue (£)'),
        tooltip=[  # Format tooltip values with commas
            alt.Tooltip('MonthYear:N', title='Month-Year'),
            alt.Tooltip('Revenue:Q', title='Total Revenue (£)', format=",.0f")
        ]
    ).properties(
        title='Monthly Revenue Trend',
        width='container',
        height = 300
    )
    
    return monthly_revenue_chart.to_dict()

@callback(
    Output('stacked-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
@cache.memoize()
def plot_stacked_chart(start_date, end_date, selected_countries):
    """
    Generates a stacked bar chart displaying Gross Revenue, Refunds, and Net Revenue 
    for the selected countries within the specified date range.

    Parameters:
    ----------
    start_date : str
        The selected start date from the date picker (in YYYY-MM-DD format).
    end_date : str
        The selected end date from the date picker (in YYYY-MM-DD format).
    selected_countries : list
        A list of selected countries used to filter the data.

    Returns:
    -------
    dict
        A JSON-encoded Altair chart specification representing the stacked bar 
        chart of revenue components.
    """
    # Filter the data based on selected date range and countries
    filtered_df = df[(df['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                       (df['InvoiceDate'] <= pd.to_datetime(end_date)) & 
                       (df['Country'].isin(selected_countries))]
    
    # Compute Gross Revenue (sum of revenue where quantity > 0)
    gross_revenue = filtered_df.loc[filtered_df['Quantity'] > 0, 'Revenue'].sum()
    
    # Compute Refund (sum of revenue where quantity < 0, taking absolute value)
    refund = abs(filtered_df.loc[filtered_df['Quantity'] < 0, 'Revenue'].sum())
    
    # Compute Net Revenue (Gross Revenue - Refund)
    net_revenue = gross_revenue - refund
    
    # Data for stacked bar (ensuring total height is Gross Revenue)
    working_df = pd.DataFrame({
        'Component': ['Net Revenue', 'Refunds'],
        'Value': [net_revenue, refund]
    })
    working_df['Total'] = working_df['Value'].sum()
    
    chart = alt.Chart(working_df).mark_bar(size=40).encode(  # Adjust size here
        x=alt.X('Total:Q', title='Total Gross Revenue'),
        y=alt.Y('Value:Q', title='Amount (£)'),
        color=alt.Color('Component:N', scale=alt.Scale(domain=['Refunds', 'Net Revenue'], range=['#9A2A2A', '#ffcc87']),
                        legend=alt.Legend(title='Category')
                       ),
        order=alt.Order('Component:N', sort='ascending'),  # Ensure correct stacking order,
    tooltip=[
        alt.Tooltip('Component:N', title='Category'),
        alt.Tooltip('Value:Q', title='Amount (£)', format=",.2f")  # Format with pound symbol and commas
    ]
    ).properties(
        title='Revenue Stacked Chart',
        width=200,
        height=300
    )

    return chart.to_dict()

@callback(
    Output('product-bar-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
@cache.memoize()
def plot_top_products_revenue(start_date, end_date, selected_countries, n_products=10):
    """
    Generates a horizontal bar chart displaying the top products by revenue 
    within the selected date range and countries.

    Parameters:
    ----------
    start_date : str
        The selected start date from the date picker (in YYYY-MM-DD format).
    end_date : str
        The selected end date from the date picker (in YYYY-MM-DD format).
    selected_countries : list
        A list of selected countries used for data filtering.
    n_products : int, optional
        The number of top products to display, default is 10.

    Returns:
    -------
    dict
        A JSON-encoded Altair chart specification representing the 
        top products by revenue.
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
    
    # Wrap on whitespace with a max line length of 30 chars
    product_revenue['Product'] = product_revenue['Description'].apply(wrap, args=[30])

    # Assign a rank to each product based on its position in the top 10
    product_revenue['Rank'] = range(1, len(product_revenue) + 1)

    # Define a consistent color scheme for the top 10 positions
    top_colors = [
        '#150e37', '#3b0f70', '#651a80', '#8c2a81', '#b6377a',
        '#de4968', '#f76f5c', '#fe9f6d', '#fece91', '#e8d3bd'
    ]

    # Map the rank to the corresponding color
    product_revenue['Color'] = product_revenue['Rank'].apply(lambda x: top_colors[x - 1])

    # Plot the bar chart with consistent colors for the top 10 positions
    bar_chart = alt.Chart(product_revenue).mark_bar().encode(
        x=alt.X('Revenue:Q', title='Revenue (£)'),
        y=alt.Y('Product:N', sort='-x', title='Product Name'),
        color=alt.Color('Color:N', scale=None, legend=None),  # Use consistent colors
        tooltip=[  
            alt.Tooltip('Description:N', title='Description'),
            alt.Tooltip('Revenue:Q', title='Revenue (£)', format=",.0f")
        ]
    ).properties(
        title=f'Top {n_products} Products by Revenue',
        width='container',
        height=300
    )
    
    return bar_chart.to_dict()

@callback(
    Output('country-pie-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
@cache.memoize()
def plot_top_countries_pie_chart(start_date, end_date):
    """
    Generates an interactive pie chart displaying the top 5 countries by sales, 
    excluding the United Kingdom. The chart also groups all other countries into 
    an "Others" category.

    Parameters:
    ----------
    start_date : str
        The selected start date from the date picker (in YYYY-MM-DD format).
    end_date : str
        The selected end date from the date picker (in YYYY-MM-DD format).

    Returns:
    -------
    dict
        A JSON-encoded Altair chart specification representing the pie chart 
        of the top 5 countries (excluding the UK) by sales.
    """
    # Exclude the United Kingdom
    df_no_uk = df[df['Country'] != 'United Kingdom']

    df_no_uk = df_no_uk[(df_no_uk['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                        (df_no_uk['InvoiceDate'] <= pd.to_datetime(end_date))]
    
    # Count the occurrences of each country and reset index
    country_counts = df_no_uk['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']
    
    # Calculate percentage
    total_count = country_counts['Count'].sum()
    country_counts['Percentage'] = round((country_counts['Count'] / total_count) * 100, 1)
    
    # Get top 5 countries
    top_countries = country_counts.head(5)

    # Calculate the "Others" percentage
    others_percentage = 100 - top_countries['Percentage'].sum()

    # Append "Others" to the DataFrame
    others_row = pd.DataFrame({'Country': ['Others'], 'Count': [total_count - top_countries['Count'].sum()], 'Percentage': [others_percentage]})
    final_data = pd.concat([top_countries, others_row], ignore_index=True)
    


    # Create an Altair selection object for clicking on the pie slices
    selection = alt.selection_point(fields=['Country'], 
                                    nearest= False, 
                                    empty=False,
                                    name="selected_country")

    # Create the Altair pie chart with percentages
    pie_chart = alt.Chart(final_data).mark_arc().encode(
        theta=alt.Theta(field="Percentage", type="quantitative").stack(True),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.5)), 
        tooltip=['Country', 'Percentage']
    )
    
    chart = pie_chart.mark_arc(outerRadius=120).encode(
         color=alt.Color(field="Country", type="nominal", scale=alt.Scale(scheme='magma'), legend=None)
    ).add_params(selection).properties(
        title="Top 5 Countries Outside of the UK",
        width='container',
        height = 300
    )

    text = pie_chart.mark_text(
        size=10, fontWeight='bold', color='black', radius=140
    ).encode(
        text=alt.Text('Country:N'),  # Show country names
    )

    pie_chart = (chart + text)

    return pie_chart.to_dict()



@callback(
    Output('card-loyal-customer-ratio', 'children'),
    Output('card-loyal-customer-sales', 'children'),
    Output('card-net-sales', 'children'),
    Output('card-total-returns', 'children'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
#@cache.memoize()
def update_cards(start_date, end_date, selected_countries):
    """
    Updates key financial metric cards based on the selected date range and countries.

    Parameters:
    ----------
    start_date : str
        The selected start date from the date picker (in YYYY-MM-DD format).
    end_date : str
        The selected end date from the date picker (in YYYY-MM-DD format).
    selected_countries : list
        A list of selected countries used for filtering data.

    Returns:
    -------
    tuple
        A tuple containing the updated content for four dashboard cards:
        1. **Loyal Customer Ratio** (percentage of transactions from known customers).
        2. **Loyal Customer Sales** (total revenue from identified customers).
        3. **Net Sales** (total revenue, including refunds).
        4. **Total Returns** (negative revenue due to refunds).
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
    loyal_customer_ratio_value = html.Span(
        f"{round(loyal_customers_ratio * 100, 2)}%",
        style={'color': '#034168', 'fontWeight': 'bold'}  
    )

    # Calculate the loyal customer sales
    non_blank_customer_ids = filtered_df[filtered_df['CustomerID'].notna()]
    total_sales = non_blank_customer_ids['Revenue'].sum()
    loyal_customer_sales_value = html.Span(
        f"£{total_sales:,.2f}",
        style={'color': '#034168', 'fontWeight': 'bold'}  
    )

    # Calculate net sales
    net_sales_value = html.Span(
        f"£{filtered_df['Revenue'].sum():,.2f}",
        style={'color': '#034168', 'fontWeight': 'bold'}  
    )

    # Calculate total returns
    returns = filtered_df[filtered_df['Revenue'] < 0]
    total_returns_value = html.Span(
        f"-£{-1*returns['Revenue'].sum():,.2f}",
        style={'color': '#9A2A2A', 'fontWeight': 'bold'}  
    )

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



@callback(
    Output('other-countries-store', 'data'),  # Store list of "Others" countries
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('other-countries-store', 'data')
)

def compute_other_countries(start_date, end_date, store):
    """
    Identifies and returns a list of countries classified under the "Others" category. 
    The "Others" category includes all countries except for the top 5 based on sales 
    within the specified date range.

    Parameters:
    ----------
    start_date : str
        The selected start date from the date picker (in YYYY-MM-DD format).
    end_date : str
        The selected end date from the date picker (in YYYY-MM-DD format).
    store : list or None
        Previously stored list of "Others" countries (not used in the computation).

    Returns:
    -------
    list
        A list of country names that are outside the top 5 in sales, excluding the United Kingdom.
    """
    # Exclude the United Kingdom
    df_no_uk = df[df['Country'] != 'United Kingdom']

    df_no_uk = df_no_uk[(df_no_uk['InvoiceDate'] >= pd.to_datetime(start_date)) & 
                        (df_no_uk['InvoiceDate'] <= pd.to_datetime(end_date))]
    
    # Count occurrences of each country and reset index
    country_counts = df_no_uk['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']
    
    # Get the list of "Others" countries
    other_countries = country_counts.iloc[5:]['Country'].tolist()

    return other_countries  # Return only the list

@callback(
    Output('selected-country-store', 'data'),  # Store selected country
    Input('country-pie-chart', 'signalData')  # Capture Vega selection
)
@cache.memoize()
def store_selected_country(signalData):
    """
    Extracts and stores the selected country from the pie chart interaction. 
    If "Others" is selected, it stores "Others" instead of an individual country.

    Parameters:
    ----------
    signalData : dict or None
        Data received from the Vega chart selection, containing details about the 
        chosen country. If no selection is made, this may be None.

    Returns:
    -------
    str or None
        The name of the selected country if a valid selection was made. 
        Returns None if no selection is detected.
    """
    print(f'store_selected_country {signalData}')  # Debugging output
    
    if signalData and "selected_country" in signalData:
        selected_data = signalData["selected_country"]
        
        if "Country" in selected_data and isinstance(selected_data["Country"], list):
            selected_country = selected_data["Country"][0]  # Extract first country in the list
            print(f"Extracted Country: {selected_country}")  # Debugging output
            
            return selected_country  # Store only the name (not the full list)
        
    return None  # Default to None if nothing is clicked

@callback(
    Output('country-dropdown', 'value'),
    Input('selected-country-store', 'data'),  # Read from stored selection
    Input('other-countries-store', 'data'),  # Read from stored "Others" countries
    State('country-dropdown', 'value')
)
@cache.memoize()
def update_country_dropdown(selected_country, other_countries, dropdown_value):
    """
    Updates the country dropdown based on the selected country from the pie chart. 
    If "Others" is selected, the dropdown is updated with all non-top-5 countries.

    Parameters:
    ----------
    selected_country : str or None
        The country selected from the pie chart. If "Others" is selected, this will be "Others".
    other_countries : list
        A list of countries classified as "Others" (i.e., all non-top-5 countries).
    dropdown_value : list
        The current value(s) in the country dropdown before updating.

    Returns:
    -------
    list
        A list of selected countries to update the dropdown. If "Others" is selected, 
        the dropdown will be set to contain all non-top-5 countries. If no selection is 
        made, the dropdown retains its previous value.
    """
    print(f"Dropdown Updated - selected_country: {selected_country}")  # Debugging output
    print(f"Dropdown Updated - other_countries: {other_countries}")  # Debugging output
    print(f"Dropdown Updated - dropdown_value: {dropdown_value}")  # Debugging output

    if selected_country is None:
        selected_country = None
        return dropdown_value

    if selected_country == "Others":
        selected_country = None
        return other_countries  # Set dropdown to all "Others" countries
    
    return [selected_country] # Ensure it's a list (Dropdown expects a list)

