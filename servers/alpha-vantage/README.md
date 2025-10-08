# Alpha Vantage MCP Server

MCP server for accessing comprehensive financial market data from Alpha Vantage. Get real-time stock quotes, forex rates, cryptocurrency prices, technical indicators, and fundamental company data.

## Features

- **Stock Market Data**: Real-time quotes, intraday, daily, weekly, and monthly time series
- **Technical Indicators**: 50+ indicators including SMA, EMA, RSI, MACD, Bollinger Bands, and more
- **Forex**: Foreign exchange rates for 150+ currencies
- **Cryptocurrency**: Bitcoin, Ethereum, and major crypto prices
- **Fundamental Data**: Company overviews, earnings, financial metrics
- **News Sentiment**: AI-powered news sentiment analysis for stocks
- **Symbol Search**: Search for stock tickers by company name

## Setup

### Prerequisites

- Alpha Vantage account
- API key from [alphavantage.co](https://www.alphavantage.co/support/#api-key)

### Environment Variables

- `ALPHAVANTAGE_API_KEY` (required): Your Alpha Vantage API key

**How to get an API key:**
1. Go to [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)
2. Click "Get Your Free API Key Today"
3. Fill out the form and submit
4. Receive your API key via email immediately
5. Free tier includes 25 requests/day

## Available Tools

### Stock Quote & Time Series Tools

#### `get_stock_quote`
Get real-time stock quote with latest price and trading data.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')

**Example:**
```python
quote = await get_stock_quote(symbol="AAPL")
```

**Response includes:**
- Current price
- Opening price
- Previous close
- High and low
- Volume
- Latest trading day
- Change and change percent

#### `get_intraday_data`
Get intraday time series data with specified intervals.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol
- `interval` (string, optional): Time interval ('1min', '5min', '15min', '30min', '60min', default: '5min')
- `outputsize` (string, optional): 'compact' (last 100 points) or 'full' (full history), default: 'compact'

**Example:**
```python
intraday = await get_intraday_data(
    symbol="MSFT",
    interval="15min",
    outputsize="compact"
)
```

#### `get_daily_data`
Get daily time series data.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol
- `outputsize` (string, optional): 'compact' (last 100 days) or 'full' (20+ years), default: 'compact'

**Example:**
```python
daily = await get_daily_data(
    symbol="GOOGL",
    outputsize="full"
)
```

#### `get_weekly_data`
Get weekly aggregated time series data (20+ years of history).

**Parameters:**
- `symbol` (string, required): Stock ticker symbol

**Example:**
```python
weekly = await get_weekly_data(symbol="TSLA")
```

#### `get_monthly_data`
Get monthly aggregated time series data (20+ years of history).

**Parameters:**
- `symbol` (string, required): Stock ticker symbol

**Example:**
```python
monthly = await get_monthly_data(symbol="AMZN")
```

### Symbol Search Tool

#### `search_symbol`
Search for stock symbols by company name or keywords.

**Parameters:**
- `keywords` (string, required): Search keywords

**Example:**
```python
results = await search_symbol(keywords="Apple")
```

**Response includes:**
- Symbol
- Name
- Type (Equity, ETF, etc.)
- Region
- Market open/close times
- Currency

### Technical Indicators Tool

#### `get_technical_indicator`
Get technical indicator data for analysis.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol
- `indicator` (string, required): Indicator type
- `interval` (string, optional): Time interval (default: 'daily')
- `time_period` (int, optional): Number of data points (default: 14)
- `series_type` (string, optional): Price type ('close', 'open', 'high', 'low', default: 'close')

**Supported Indicators:**
- **Moving Averages**: SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA, T3
- **Momentum**: RSI, STOCH, STOCHF, STOCHRSI, WILLR, ADX, ADXR, APO, PPO, MOM, BOP, CCI, CMO, ROC, ROCR, AROON, AROONOSC, MFI, TRIX, ULTOSC, DX, MINUS_DI, PLUS_DI, MINUS_DM, PLUS_DM, MIDPOINT, MIDPRICE
- **Volatility**: BBANDS, NATR, ATR
- **Volume**: OBV, AD, ADOSC
- **Others**: MACD, MACDEXT, HT_TRENDLINE, HT_SINE, HT_TRENDMODE, HT_DCPERIOD, HT_DCPHASE, HT_PHASOR

**Example:**
```python
# Simple Moving Average
sma = await get_technical_indicator(
    symbol="AAPL",
    indicator="SMA",
    interval="daily",
    time_period=50,
    series_type="close"
)

# Relative Strength Index
rsi = await get_technical_indicator(
    symbol="TSLA",
    indicator="RSI",
    interval="60min",
    time_period=14,
    series_type="close"
)

# MACD
macd = await get_technical_indicator(
    symbol="MSFT",
    indicator="MACD",
    interval="daily",
    series_type="close"
)

# Bollinger Bands
bbands = await get_technical_indicator(
    symbol="GOOGL",
    indicator="BBANDS",
    interval="15min",
    time_period=20,
    series_type="close"
)
```

### Forex Tools

#### `get_forex_rate`
Get real-time foreign exchange rate.

**Parameters:**
- `from_currency` (string, required): Source currency code (e.g., 'USD', 'EUR', 'GBP')
- `to_currency` (string, required): Target currency code

**Example:**
```python
rate = await get_forex_rate(
    from_currency="USD",
    to_currency="EUR"
)
```

**Supported Currencies:**
- Major: USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD
- 150+ total currencies including emerging markets
- Cryptocurrencies: BTC, ETH, etc.

### Cryptocurrency Tools

#### `get_crypto_price`
Get real-time cryptocurrency price.

**Parameters:**
- `symbol` (string, required): Crypto symbol (e.g., 'BTC', 'ETH', 'LTC', 'XRP', 'DOGE')
- `market` (string, optional): Market currency (default: 'USD')

**Example:**
```python
btc = await get_crypto_price(
    symbol="BTC",
    market="USD"
)

eth = await get_crypto_price(
    symbol="ETH",
    market="EUR"
)
```

**Supported Cryptocurrencies:**
- Bitcoin (BTC)
- Ethereum (ETH)
- Litecoin (LTC)
- Ripple (XRP)
- Bitcoin Cash (BCH)
- Cardano (ADA)
- Dogecoin (DOGE)
- And many more

### Fundamental Data Tools

#### `get_company_overview`
Get comprehensive company information and fundamental data.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol

**Example:**
```python
overview = await get_company_overview(symbol="AAPL")
```

**Response includes:**
- Company name, description, sector, industry
- Market capitalization
- P/E ratio, PEG ratio
- Book value, dividend yield
- EPS, profit margin, ROE, ROA
- Revenue, EBITDA
- 52-week high/low
- 50-day and 200-day moving averages
- Analyst target price
- Beta, shares outstanding

#### `get_earnings`
Get earnings reports and estimates.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol

**Example:**
```python
earnings = await get_earnings(symbol="MSFT")
```

**Response includes:**
- Quarterly earnings history
- Annual earnings history
- Reported EPS vs estimated EPS
- Surprise percentage
- Fiscal date ending

### News Sentiment Tool

#### `get_market_sentiment`
Get AI-powered news sentiment analysis for stocks.

**Parameters:**
- `tickers` (string, required): Comma-separated stock symbols
- `topics` (string, optional): Filter by topics
- `time_from` (string, optional): Start time (YYYYMMDDTHHMM)
- `time_to` (string, optional): End time (YYYYMMDDTHHMM)
- `sort` (string, optional): Sort order ('LATEST', 'EARLIEST', 'RELEVANCE', default: 'LATEST')
- `limit` (int, optional): Number of results (max: 1000, default: 50)

**Example:**
```python
sentiment = await get_market_sentiment(
    tickers="AAPL,MSFT,GOOGL",
    topics="technology",
    sort="RELEVANCE",
    limit=20
)
```

**Response includes:**
- News articles with titles, URLs, sources
- Overall sentiment score (-1 to 1)
- Sentiment label (Bearish, Neutral, Bullish)
- Relevance score
- Ticker-specific sentiment
- Publication time

## Time Intervals

### Intraday Intervals
- `1min` - 1-minute bars
- `5min` - 5-minute bars
- `15min` - 15-minute bars
- `30min` - 30-minute bars
- `60min` - 60-minute bars (1-hour)

### Long-term Intervals
- `daily` - Daily bars
- `weekly` - Weekly aggregated
- `monthly` - Monthly aggregated

## Output Size Options

### Compact
- Returns last 100 data points
- Faster response time
- Recommended for recent data

### Full
- Returns full available history
- Up to 20+ years for daily/weekly/monthly
- Larger response size
- Recommended for historical analysis

## Rate Limits and Pricing

### Free Tier
- **25 API requests per day**
- All basic features included
- Real-time data
- Technical indicators
- No credit card required

### Premium Plans

**Basic ($49.99/month)**
- 120 requests/minute
- 43,200 requests/day
- Email support

**Standard ($249.99/month)**
- 300 requests/minute
- 108,000 requests/day
- Priority email support

**Professional ($499.99/month)**
- 600 requests/minute
- 216,000 requests/day
- Priority support
- Historical intraday data

**Ultimate ($1,199.99/month)**
- 1,200 requests/minute
- 432,000 requests/day
- Dedicated support
- Full historical data
- Premium endpoints

Visit [alphavantage.co/premium](https://www.alphavantage.co/premium/) for current rates.

## Data Coverage

### Stock Markets
- **US Stocks**: NYSE, NASDAQ
- **International**: London, Toronto, Frankfurt, and more
- **ETFs**: Major exchange-traded funds
- **Mutual Funds**: Available for many funds

### Historical Data
- **Intraday**: Last 1-2 months (compact), extended history (premium)
- **Daily**: 20+ years
- **Weekly**: 20+ years
- **Monthly**: 20+ years

## Best Practices

1. **Cache responses**: Market data doesn't change every second
2. **Use appropriate intervals**: Match your use case
3. **Monitor rate limits**: Track your daily usage
4. **Handle errors gracefully**: API may return errors during market closures
5. **Use outputsize wisely**: 'compact' for recent data, 'full' for historical analysis
6. **Batch symbol searches**: Search once, cache results
7. **Choose right indicators**: Different indicators for different strategies

## Error Handling

Common error messages:
- **"Invalid API call"**: Check function name and parameters
- **"Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute"**: Rate limit exceeded
- **"Error Message: the parameter apikey is invalid or missing"**: Invalid API key
- **"Note"**: API note about premium features or rate limits

## Response Format

All responses are JSON format with the following structure:

**Time Series Example:**
```json
{
  "Meta Data": {
    "1. Information": "Daily Prices",
    "2. Symbol": "AAPL",
    "3. Last Refreshed": "2024-01-15",
    "4. Output Size": "Compact",
    "5. Time Zone": "US/Eastern"
  },
  "Time Series (Daily)": {
    "2024-01-15": {
      "1. open": "182.00",
      "2. high": "185.50",
      "3. low": "181.50",
      "4. close": "184.25",
      "5. volume": "50000000"
    }
  }
}
```

## API Documentation

For detailed information about Alpha Vantage API:
- [Documentation](https://www.alphavantage.co/documentation/)
- [Stock Time Series](https://www.alphavantage.co/documentation/#time-series-data)
- [Technical Indicators](https://www.alphavantage.co/documentation/#technical-indicators)
- [Forex](https://www.alphavantage.co/documentation/#fx)
- [Cryptocurrency](https://www.alphavantage.co/documentation/#digital-currency)
- [Fundamental Data](https://www.alphavantage.co/documentation/#company-overview)

## Use Cases

- **Trading Bots**: Algorithmic trading systems
- **Portfolio Management**: Track investments and analyze performance
- **Technical Analysis**: Chart patterns and indicator signals
- **Market Research**: Analyze trends and correlations
- **Financial Dashboards**: Real-time market data displays
- **Academic Research**: Historical data analysis
- **Risk Management**: Monitor volatility and exposure
- **Robo-Advisors**: Automated investment recommendations

## Common Technical Analysis Patterns

### Trend Indicators
- **SMA/EMA**: Identify trend direction
- **MACD**: Momentum and trend changes
- **ADX**: Trend strength

### Momentum Oscillators
- **RSI**: Overbought/oversold conditions (0-100)
- **STOCH**: Stochastic oscillator for momentum
- **CCI**: Commodity Channel Index

### Volatility Indicators
- **BBANDS**: Bollinger Bands for volatility
- **ATR**: Average True Range

### Volume Indicators
- **OBV**: On-Balance Volume
- **AD**: Accumulation/Distribution

## Support

- [Alpha Vantage Support](https://www.alphavantage.co/support/)
- [Community Forum](https://www.alphavantage.co/support/#community)
- [FAQ](https://www.alphavantage.co/support/#support)
- [Contact](https://www.alphavantage.co/support/#contact)
