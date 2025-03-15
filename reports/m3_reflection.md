# Milestone 3 Reflection

## What We Have Implemented So Far

Our dashboard still follows our app's original design, however with a few modifications. We still have followed the general layout of our sketch, with four main charts and supporting widgets that provide insights from our data:

-   Net revenue sales by month through a trend-line chart.
-   Monthly revenue by product through a bar chart.
-   Updated stacked bar chart to record sales and returns.
-   Updated interactive pie chart of top-performing international markets (outside the UK).
-   Interactive cards summarizing important business insights like the company's net sales and loyal customer ratio.
-   Updated title and sidebar styling
-   Updated chart colours to align with each other
-   Updated formatting on display cards
  
   **Challenging question attempt:**
-   [DSCI-532_2025_17_pharma_spend_dashboard](https://github.com/UBC-MDS/DSCI-532_2025_17_pharma_spend_dashboard): We really liked the horizontal bar/lines between filters in this dashboard. It provides a structured look to the dashboard and helps better distinguish between filters. We have incorporated this in our dashboard.
-   [DSCI-532_2025_27_CA_Wildfire-Dashboard](https://github.com/UBC-MDS/DSCI-532_2025_27_CA_Wildfire-Dashboard): We have center aligned the "About" section in our dashboard. Our dashboard looks cleaner this way. 


## Deviations from the Original Sketch

Our biggest deviation was transitioning from a static pie chart to an interactive one. The pie chart still highlights the top-performing international markets outside of the UK, however, it is now also linked to the global filters. Users can click on a country within the pie chart, which updates the country filter and refreshes the dashboard accordingly. All other non-UK countries are aggregated into an "Others" category, which also updates the dashboard when selected. Clicking outside the pie chart resets the global filter to its default, displaying data for the United Kingdom.

Based on feedback, we also replaced the waterfall chart with a more intuitive stacked bar chart. While still conveying key insights into sales and returns, this format enhances readability and user experience.

Lastly, we rearranged the order of our charts to create a more logical flow and improve usability. The top charts focus on revenue and overall sales, while the lower charts provide deeper insights into top products and customer distribution. This adjustment aligns with our original sketch, reversing last week's decision to reorder the layout.


## Best Practices

We have stuck to best practices for designing dashboards and visualizations. We replaced the waterfall chart with a stacked chart, to make the data more digestible for users. Additionally, we modularized our code for better maintainability and added docstrings to all functions for clarity. As a further improvement, we can enhance the readability of our layout components by improving their indentation in the code.

## Strengths

The strength of our dashboard lies in its clear presentation of key insights and logical flow. Users can easily analyze product and sales patterns across all operating countries. The interactive pie chart is now one of the dashboard's standout features, providing a quick view of the top five international markets while also allowing users to explore data for all other regions.

## Issues and Future Improvements

We are continuously working on enhancing the dashboard to make it as visually appealing and user-friendly as possible:
 
-   Continue to improve dashboard aesthetics. Specifically, we need to decide if we want to keep the pastel theme for our charts or change it to a more vibrant colour scheme.
-   Discuss appropriate chart names and title formats
-   Due to the arrangement of our containers, the sidebar currently only spans the length of the charts. We can expand its length to fit the whole dashboard for a more balanced look. 
-   Ensure axis ticks are either horizontal or vertical
-   Address peer-review feedback 
