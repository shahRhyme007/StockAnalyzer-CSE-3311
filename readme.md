![image](https://github.com/user-attachments/assets/f978f4f9-ad5f-480a-bc4e-3abbc987f35a)


![image](https://github.com/user-attachments/assets/ec5c97a7-ce39-4f9a-8325-2d9be15c244b)

![image](https://github.com/user-attachments/assets/06ee24c9-4314-47c5-8db0-a92fa55257c1)

![image](https://github.com/user-attachments/assets/60a5584d-9300-4135-9a90-d57d970552c6)

![image](https://github.com/user-attachments/assets/4c686281-55e7-4e6f-ab34-83cf017da36f)



https://github.com/user-attachments/assets/ac39501c-9f95-4789-af2d-605d75a6490c




The `stockanalyzer.py` file is a Streamlit-based web application designed to provide stock analysis tools, including stock price visualization, financial data, comparison among different stocks, news updates, educational videos, and investment tips. Here's a detailed breakdown of its contents:

### Imports:
- **Libraries**: Streamlit (for UI), Pandas/Numpy (data handling), yFinance (fetching stock data), Plotly (visualizations), StockNews (news fetching), and other utility libraries like requests, random, and math.

### Custom Classes:
- **StockTips**: Contains a list of investment tips and methods to shuffle and retrieve a specific number of tips.
- **VideoArray**: Manages a list of educational video URLs with methods to shuffle and retrieve a specified number of videos.

### Initialization:
- Instances of `StockTips` and `VideoArray` are created, shuffled, and a few items are selected for display.

### Functions:
- **fetch_stock_news**: Fetches stock-related news from the Polygon API, parsing and returning the news items.

### Streamlit Setup:
- Sidebar inputs allow users to specify the stock ticker, start date, end date, and graph color.
- Stock data is downloaded using yFinance, and a line chart is created with Plotly to visualize stock prices.

### Tabs:
1. **Stock Comparison**:
   - Allows users to select multiple stocks for comparison.
   - Downloads and plots adjusted close prices for the selected stocks.
   - Calculates and displays annual return, standard deviation, and risk-adjusted return for each stock.
   
2. **Financial Data**:
   - Displays historical stock price data, calculates annual returns, standard deviation, and risk-adjusted returns.
   - Fetches and shows financial statements (balance sheet, cash flow) for the selected stock using yFinance.

3. **Selected News**:
   - Uses the StockNews module to fetch and display recent news articles, including sentiment analysis scores.
   - Calculates and displays average sentiment scores based on the articles.

4. **Videos**:
   - Displays selected educational videos on stock investment.

5. **Articles**:
   - Fetches and displays trending articles about the selected stock using the `fetch_stock_news` function.

6. **Tips**:
   - Lists several investment tips randomly selected from the `StockTips` class.

This app offers a comprehensive toolset for stock analysis, combining real-time data fetching, financial metrics, news updates, educational resources, and practical tips.
