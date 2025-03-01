# Milestone 2 Reflection

## What We Have Implemented So Far

Our dashboard closely follows our app design and implements all the components we had planned. We have created four main charts and supporting widgets that provide insights from our data:

* Net revenue sales by month through a trend-line chart.
* Monthly revenue by product through a bar chart.
* A waterfall chart to record sales and returns.
* A pie chart of top-performing international markets (countries outside the UK).
* Interactive cards summarizing important business insights like the company's net sales and loyal customer ratio.
* All charts except the pie chart are bound by two global filters—date range and country dropdown.
* **Challenging question attempt** We added an additional interactive card, 'Loyal Customer Sales,' to make the app more informative at first glance. This feature helps the business understand how much of the net revenue comes from loyal customers and whether they should invest in building a more loyal customer base. Despite only 52% of customers being loyal, they account for 82% of the company's total sales.


## Deviations from the Original Sketch

At this time, we have implemented all our originally planned features. We changed our monthly revenue chart from a bar chart to a trend-line chart as it is more intuitive for a continuous variable like revenue. We have also added a footer section to provide a quick summary of the dashboard's functionality and included a link to our GitHub repository in it. 

In our original sketch, we did not have any global filters on our cards, as we thought a holistic overview of the entire dataset would be more suitable when first opening the app. However, we realized that this could cause confusion since the cards and charts would not be in sync, so we decided to add global filters to our cards as well.

Additionally, we experimented with the placement of the cards and global filters and arrived at a more visually appealing template for now, which includes filters on the left, cards at the top, and charts in the center.

## Current Issues with the Dashboard

We are continuously working on improving the aesthetics and layout of the dashboard. Since different group members created various app elements, the dashboard lacks consistency and alignment. Some charts are overlapping (including overlapping headings) with other charts, and some appear larger than we intended. The dashboard extends beyond the screen, forcing us to scroll to see the whole picture at once, which is not ideal.

## Deviations from Best Practices

Our dashboard does not clearly indicate which filter interacts with which chart. Currently, our country filter defaults to the UK, and selecting all countries at once is tedious. We will consider adding an option to select all countries with a single click. Moreover, all our scripts are in the same Python file, and we plan to modularize our code next week.

## Strengths

Our dashboard effectively covers important business insights. The cards provide key statistics at a glance, and the choice of charts for each use case is intuitive. The global filters also work well for generating insights. This dashboard serves as a strong foundation for a more comprehensive version we may develop in the future.

## Future Improvements and Additions

As mentioned earlier, we are working on enhancing the dashboard's aesthetics to make it more visually appealing and user-friendly:

* Reorder the charts to improve storytelling—place total revenue charts at the top, followed by top products, and then top countries. We created an issue to attempt to resolve this in the coming milestones: https://github.com/UBC-MDS/DSCI-532_2025_9_RetaiLense/issues/89
* We ran into an issue with the graphs resizing poorly when the screen size changes. For example, when you zoom in on the dashboard, the graphs do not dynamically adjust to the new sizing and instead overlap each other. We created an issue to attempt to resolve this in the coming milestones: https://github.com/UBC-MDS/DSCI-532_2025_9_RetaiLense/issues/66
* Make the color scheme consistent across all the app elements. We created an issue to attempt to resolve this in the coming milestones: https://github.com/UBC-MDS/DSCI-532_2025_9_RetaiLense/issues/90
* Explore options to add an interactive feature to the pie chart, possibly by incorporating the date range filter. We would like to get some feedback on this next week for suggestions.
* Center align dashboard name, RetaiLense
* The "Total Returns" card displays the "$" sign before the negative returns value. Since returns inherently represent negative revenue, we will remove the negative sign from the displayed value.