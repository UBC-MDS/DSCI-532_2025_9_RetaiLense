from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt


# Read your CSV file
df = pd.read_csv('data/processed/processed_data.csv')

# Ensure 'InvoiceDate' is converted to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create Month-Year column
df['MonthYear'] = df['InvoiceDate'].dt.strftime('%b-%Y')


# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "RetaiLense Dashboard"


app.layout = html.Div([
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
    
    # Create a div for the pie chart using dash_vega_components
    dvc.Vega(
        id='waterfall-chart',
        spec={}  # Pass the Altair chart spec (dict format)
    ),
])



# Server side callbacks (reactivity)
@callback(
    Output('waterfall-chart', 'spec'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('country-dropdown', 'value')
)
# Define the function to create the pie chart (as you already have it)
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)