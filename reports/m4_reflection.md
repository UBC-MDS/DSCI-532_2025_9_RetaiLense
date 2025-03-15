# Milestone 4 Reflection

## What We Have Implemented So Far

In Week 4, we focused on enhancing the aesthetics, improving functionality, and optimizing the speed of our dashboard. We would like to acknowledge Daniel and our peers for their valuable feedback, which helped us refine our design and performance.

**Performance Improvement**
- Used binary format for faster data loading.
- Implemented caching for the default view to load quickly and the top 5 countries outside the UK.

**App Refinement**
- Updated the color palette to be color-blind friendly.
- Center-aligned charts to create a more structured and visually appealing layout.
- Improved label visibility in the product chart to ensure product names are clearly displayed. We also reviewed and adjusted text sizes for better readability.
- Finalized the overall design by refining chart titles, colors, element placements, and addressing other minor aesthetic feedback.
  
**Challenging question attempt:**
- Added proper docstrings for all functions.
- Set up tests to validate function performance and accuracy.


## Deviations from the Original Sketch

Our final dashboard has evolved significantly from our initial sketch and we are happy with the final product. Our charts are interactive (e.g., pie chart now allows dynamic country selection that automatically updates the rest of the dashboard through global filters), more intuitive and user-friendly (e.g., waterfall was changed to stacked bar which users are more familiar with) and the placements are updated for better storytelling. 


## Best Practices

We have stuck to best practices for designing dashboards and visualizations. While our chosen color scheme does not include a neutral middle-range color (which prevented us from using green color for sales), this decision was intentional. Our goal was to ensure strong contrast and maintain a visually harmonious design.


## Strengths

Our dashboard loads quickly both locally and on Render. The strength of our dashboard lies in its clear presentation of key insights and logical flow. It is easy to navigate, and the summary cards at the top provide quick insights at a glance. This version serves as a strong foundation for further development, should we choose to expand it in the future.


## Future Improvements

We are happy with our dashboard. Some things to consider for the future:
- Incorporating real-time data through an API would allow the dashboard to provide the most up-to-date insights.
- Adding a map to show global sales could further enhance usability by enabling users to click on a country to dynamically update the rest of the charts.
- Based on peer feedback, we could also create a customizable product chart with options to filter by specific products or display the top N items. 
- Additionally, while we have addressed color-blindness issues, we remain committed to making the dashboard even more inclusive. If we receive further feedback on accessibility concerns, we would love to make updates to ensure a better experience for all users.