# RetaiLens Proposal
### By Ashita, Meagan, Gurmehak, WaiMing

## Motivation and purpose

Target: Head of Sales

Global Head of Sales is responsible for monitoring and optimizing eCommerce sales performance across different markets. The company has a strong domestic market in the UK and growing international penetration. Sales leaders face challenges in:

* Detecting seasonal trends and opportunities to optimize sales strategies
* Understanding customer purchase behavior and product demand across regions
* The company started the UK but needs help Identifying which international markets show the most growth potential.

Our dashboard provides a comprehensive view of sales trends and customer distribution, helping decision-makers:
* Monitor global revenue and regional performance 
* Analyze customer segments 
* Track product demand and returns

## Description of the data

The dataset contains ~0.5M rows and 8 columns, representing transactional data from an online retail business. The transactions span from December 1, 2010, to December 9, 2011 covering purchases made by both individual customers and wholesalers across 38 countries.  

#### Key Data Insights  
- Observations: 541,909
- Total Products: 4,223 unique products
- Geographical Distribution: 91.43% of transactions originate from the UK
- Returns: 10,624 transactions involve negative quantities, representing product returns

#### Variable Overview & Usefulness  

| **Variable**    | **Type**       | **Use in Analysis** |
|---------------|--------------|----------------|
| **InvoiceNo**  | Categorical (ID) | Identifies each transaction; cancellations marked with ‘C’ can help track returns |
| **StockCode**  | Categorical (ID) | Used to determine most in-demand products |
| **Description** | Categorical | Product description |
| **Quantity**   | Integer | Sales quantity|
| **InvoiceDate** | Date | Global filter for date range and for tracking monthly trends  |
| **UnitPrice**  | Continuous | Unit price for the product |
| **CustomerID** | Categorical | Used to determine top customers |
| **Country**    | Categorical | Used as a global filter to monitor regional performance |

#### Engineered Variable  
To enhance our analysis, we introduce:  
- Revenue = `Quantity × UnitPrice`  
  - Measures the net revenue useful for assessing the company's performance and create trends on the basis of revenue growth. 


## Research Questions
Daniella is the Global Head of Sales for a UK-based online retail company that specializes in unique gifts for all occasions. She is responsible for overseeing the company’s sales performance across different countries and ensuring sustainable growth. While the company has a strong presence in the UK, Daniella is eager to identify opportunities for expansion and boost sales in other countries where they currently operate. To do this, she needs to identify key areas for growth, top-performing products, and the sales dynamics across different regions.

When Daniella opens up our “RetaiLense Executive Dashboard” she will be presented with an overview of key sales metrics, including total revenue, losses due to returned orders, top-selling products, and the top 10 sales countries outside of the UK. Using the dashboard, she can filter the data by country, enabling her to compare sales trends across different regions and spot key differences in product performance and identify areas for potential growth. Using the date filter, Daniella can analyze sales performance over specific periods = such as monthly or quarterly – to help detect seasonal trends or spikes in sales. For example, she may find that certain products perform well around specific holidays in different countries.

As a result of her findings from our dashboard, Daniella can determine which countries present the most promising opportunities for expansion. She can identify top-selling products and target regions where these products are underrepresented. Additionally, she can pinpoint peak sales periods in order to optimize inventory levels. With this strategic insight, Daniella can confidently recommend actions to support international growth, such as tailoring marketing campaigns for specific regions or adjusting inventory to meet customer demands.

## App sketch and description
Here is our app sketch:

<img src="https://github.com/UBC-MDS/DSCI-532_2025_9_RetaiLense/blob/main/img/sketch.png?raw=true" width="800" />

The app features a landing page that visualizes key dataset factors such as revenue, gross and net sales, quantity sold, and top-performing countries using various chart types (e.g., bar charts, waterfall charts, and pie charts, depending on the data type).

For filtering options, we plan to implement:

- A time frame slider to allow users to zoom in on specific periods.
- A dropdown menu to toggle between Product and Sales views, enabling users to analyze either quantity sold or dollar amount sold.
- Global filters, including:
  - A country filter that adjusts all charts except for the "Top Countries Outside the UK" visualization.
  - Start and end date selectors to provide a more focused view of the data.

