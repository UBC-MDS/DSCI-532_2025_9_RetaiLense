from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt


# Read your CSV file
df = pd.read_csv('data/processed/processed_data.csv')

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "RetaiLense Dashboard"

# Define the function to create the pie chart (as you already have it)
def plot_waterfall_chart(data):

    # Compute Gross Revenue (sum of revenue where quantity > 0)
    gross_revenue = data.loc[data['Quantity'] > 0, 'Revenue'].sum()

    # Compute Refund (sum of revenue where quantity < 0)
    refund = data.loc[data['Quantity'] < 0, 'Revenue'].sum()

    # Compute Net Revenue (Gross Revenue + Refund)
    net_revenue = gross_revenue + refund

    # Create the final DataFrame
    df = pd.DataFrame({
        'Category': ['Gross Revenue', 'Refund', 'Net Revenue'],
        'Value': [gross_revenue, refund, net_revenue]
    })


    # Define explicit category order
    category_order = df['Category'].tolist()
    
    # Add an index column to enforce order
    df['Index'] = range(len(df))  # Assign numerical order explicitly

    # Convert Category column to categorical with correct order
    df['Category'] = pd.Categorical(df['Category'], categories=category_order, ordered=True)

    # Compute cumulative values properly
    df['Start'] = df['Value'].cumsum().shift(1).fillna(0)
    df['End'] = df['Start'] + df['Value']

    # Force Net Revenue to start from zero
    df.loc[df['Category'] == 'Net Revenue', 'Start'] = 0
    df.loc[df['Category'] == 'Net Revenue', 'End'] = df['Value']

    # Define colors
    df['Color'] = df['Value'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')

    # Create a mapping of Index to Category labels
    category_labels = {i: cat for i, cat in enumerate(df['Category'])}

    # Create the waterfall chart
    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X('Index:O', title='Category', sort=list(df['Index']),  
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
    text = alt.Chart(df).mark_text(dy=-10, size=12).encode(
        x='Index:O',
        y='End:Q',
        text=alt.Text('Value:Q', format=',.0f')
    )

    # Combine bars and labels
    waterfall_chart = (bars + text).properties(width=600, height=400, title="Revenue Waterfall Chart" )
    
    return waterfall_chart.to_dict()


app.layout = html.Div([
    html.H1("RetaiLense Dashboard"),
    
    # Create a div for the pie chart using dash_vega_components
    dvc.Vega(
        id='waterfall-chart',
        spec=plot_waterfall_chart(df)  # Pass the Altair chart spec (dict format)
    ),
])

# Run the app
if __name__ == '__main__':
    app.server.run(debug=True)