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
  - Measures the net revenue useful for assessing the company's performance and creae trends on the basis of revenue growth. 


## Research Questions
Daniella is the Global Head of Sales for a UK-based online retail company that specializes in unique gifts for all occasions. She is focused on gaining deeper insights into the company’s monthly sales, losses, and top-performing products. While the business is strong in the UK, Daniella is eager to identify opportunities for expansion into the other countries where they currently operate, aiming to boost international growth and company profits.

When Daniella opens up our “RetaiLense Executive Dashboard” she is presented with an overview of key sales metrics, including total revenue, losses due to returned orders, top-selling products, and the top 10 sales countries outside of the UK. Using the dashboard, she can filter the data by country to compare sales trends across different regions, drill down into product performance, and identify areas for potential growth. She can also filter by date to narrow down the data to specific months or quarters, allowing her to analyze sales performance over time and detect seasonal trends or spikes in sales.



## App sketch and description

