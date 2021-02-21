## Stock screener by querying from finviz.com

## OVERVIEW
This tool will populate top stocks to pick by querying information from www.finviz.com

## Methodology

### Fundamental and Descriptive
Query all the stocks with following criteria:

URL: https://finviz.com/screener.ashx?v=111&ft=2 (to check fundamentals below)

1. EPS growth next 5 years > 10%
2. Return on Equity > 10%
3. EPS growth past 5 years > 10%
4. Sales growth past 5 years > 10%, and
5. Debt/Equity < 0.5

URL: https://finviz.com/screener.ashx?v=111&f=fa_debteq_u0.5,fa_eps5years_o10,fa_estltgrowth_o10,fa_roe_o10,fa_sales5years_o10&ft=2
(after filtering above 5 criteria)

Also, put filters on stock descriptions:

URL: https://finviz.com/screener.ashx?v=111 (to check descriptive information below)

1. Country: USA
2. Option/Short: optionable

URL: https://finviz.com/screener.ashx?v=111&f=geo_usa,sh_opt_option (after filtering above)

Choose "custom" columns: Ticker, Sector, Industry, Market Cap, P/E, EPS, EPS next 5Y, ROE, Price, Volume

Read all the pages after making choices above (dataframe)
skip tickers with missing data for any of the 5 fundamental criteria

### Method

Calculate the following:

Rule_1_growth = min(ROE, EPS next 5Y)
Rule_1_PE = min(P/E, 2 x Rule_1_growth x 100)
Future_EPS = EPS*(1 + Rule_1_PE)^10
Future_Price = Future_EPS x Rule_1_PE
Future_Price_Est = Future_Price/4
MoS_Price = 0.5 x Future_Price_Est

list of good stocks:
Good_Stocks = if MoS_Price < Price

Sort list of Good_stocks by MoS_Price/Price

### Additional

#TODO: When to sell