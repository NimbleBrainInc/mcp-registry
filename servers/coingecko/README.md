# CoinGecko MCP Server

MCP server for accessing comprehensive cryptocurrency market data from CoinGecko. Get real-time prices, market stats, trending coins, historical data, and global market insights for 14,000+ cryptocurrencies.

## Features

- **Real-time Prices**: Current prices in 150+ fiat and crypto currencies
- **Market Data**: Market cap, volume, supply, ATH/ATL, price changes
- **Historical Data**: Price charts from 1 day to maximum available history
- **Trending Coins**: Top trending cryptocurrencies in last 24h
- **Global Stats**: Total market cap, volume, BTC dominance
- **Exchange Data**: Volume rankings and exchange information
- **Categories**: DeFi, NFT, Gaming, Meme, Layer 1, Layer 2, and more
- **NFT Data**: Floor prices and volumes for NFT collections
- **Search**: Find coins by name or symbol

## Setup

### Prerequisites

- CoinGecko account
- API key (Demo or Pro plan)

### Environment Variables

- `COINGECKO_API_KEY` (required): Your CoinGecko API key

**How to get an API key:**
1. Go to [coingecko.com/en/api/pricing](https://www.coingecko.com/en/api/pricing)
2. Choose a plan:
   - **Demo** ($0/month): 30 calls/minute, 10,000 calls/month
   - **Analyst** ($129/month): 500 calls/minute, rate limit info
   - **Professional** ($499/month): 500 calls/minute, priority support
3. Sign up and get your API key
4. Store it as `COINGECKO_API_KEY`

## Available Tools

### Price & Market Data Tools

#### `get_coin_price`
Get current price of coins in multiple currencies.

**Parameters:**
- `ids` (string, required): Comma-separated coin IDs (e.g., 'bitcoin,ethereum,cardano')
- `vs_currencies` (string, optional): Target currencies (e.g., 'usd,eur,btc', default: 'usd')
- `include_market_cap` (bool, optional): Include market cap (default: False)
- `include_24hr_vol` (bool, optional): Include 24h volume (default: False)
- `include_24hr_change` (bool, optional): Include 24h change (default: False)
- `include_last_updated_at` (bool, optional): Include timestamp (default: False)

**Example:**
```python
# Simple price check
price = await get_coin_price(
    ids="bitcoin,ethereum",
    vs_currencies="usd"
)

# With market data
data = await get_coin_price(
    ids="bitcoin,ethereum,cardano",
    vs_currencies="usd,eur,btc",
    include_market_cap=True,
    include_24hr_vol=True,
    include_24hr_change=True
)
```

**Response:**
```json
{
  "bitcoin": {
    "usd": 43250,
    "eur": 39800,
    "btc": 1.0,
    "usd_market_cap": 847000000000,
    "usd_24h_vol": 18500000000,
    "usd_24h_change": 2.5
  }
}
```

#### `get_coin_details`
Get comprehensive information for a coin.

**Parameters:**
- `coin_id` (string, required): Coin ID (e.g., 'bitcoin', 'ethereum')
- `localization` (bool, optional): Include translations (default: False)
- `tickers` (bool, optional): Include ticker data (default: False)
- `market_data` (bool, optional): Include market data (default: True)
- `community_data` (bool, optional): Include community stats (default: False)
- `developer_data` (bool, optional): Include dev stats (default: False)
- `sparkline` (bool, optional): Include 7-day sparkline (default: False)

**Example:**
```python
details = await get_coin_details(
    coin_id="bitcoin",
    market_data=True,
    community_data=True,
    sparkline=True
)
```

**Response includes:**
- Name, symbol, description
- Current price, market cap, volume
- ATH/ATL prices and dates
- Circulating/total/max supply
- Price changes (24h, 7d, 30d, 1y)
- Community stats (Twitter, Reddit)
- Developer stats (GitHub)

### Historical Data Tools

#### `get_coin_market_chart`
Get historical price, market cap, and volume data.

**Parameters:**
- `coin_id` (string, required): Coin ID
- `vs_currency` (string, optional): Target currency (default: 'usd')
- `days` (string, optional): Time range ('1', '7', '14', '30', '90', '180', '365', 'max', default: '7')
- `interval` (string, optional): Data interval ('daily' for 90+ days, auto-selected if not specified)

**Example:**
```python
# Last 7 days (automatic interval)
week_data = await get_coin_market_chart(
    coin_id="ethereum",
    vs_currency="usd",
    days="7"
)

# Last 365 days with daily intervals
year_data = await get_coin_market_chart(
    coin_id="bitcoin",
    vs_currency="usd",
    days="365",
    interval="daily"
)

# All available history
all_data = await get_coin_market_chart(
    coin_id="bitcoin",
    vs_currency="usd",
    days="max"
)
```

**Response:**
```json
{
  "prices": [[1609459200000, 29000], [1609545600000, 30000], ...],
  "market_caps": [[1609459200000, 540000000000], ...],
  "total_volumes": [[1609459200000, 35000000000], ...]
}
```

### Search & Discovery Tools

#### `search_coins`
Search for coins by name or symbol.

**Parameters:**
- `query` (string, required): Search query

**Example:**
```python
results = await search_coins(query="ethereum")
```

**Response includes:**
- Matching coins with IDs, names, symbols
- Matching exchanges
- Matching categories

#### `get_trending_coins`
Get trending coins in the last 24 hours.

**Example:**
```python
trending = await get_trending_coins()
```

**Response includes:**
- Top 7 trending coins
- Trending NFTs
- Trending categories

#### `get_top_coins`
Get top coins by market cap with comprehensive market data.

**Parameters:**
- `vs_currency` (string, optional): Target currency (default: 'usd')
- `order` (string, optional): Sort order ('market_cap_desc', 'volume_desc', 'id_asc', 'id_desc', default: 'market_cap_desc')
- `per_page` (int, optional): Results per page (1-250, default: 100)
- `page` (int, optional): Page number (default: 1)
- `sparkline` (bool, optional): Include 7-day sparkline (default: False)
- `price_change_percentage` (string, optional): Price change timeframes ('1h,24h,7d')

**Example:**
```python
# Top 100 coins by market cap
top100 = await get_top_coins(
    vs_currency="usd",
    per_page=100,
    sparkline=True,
    price_change_percentage="1h,24h,7d"
)

# Top volume leaders
volume_leaders = await get_top_coins(
    vs_currency="usd",
    order="volume_desc",
    per_page=50
)
```

**Response includes per coin:**
- Current price
- Market cap, rank
- 24h volume
- Price changes (1h, 24h, 7d)
- ATH/ATL
- Circulating supply
- 7-day price sparkline (if requested)

### Listing Tools

#### `list_supported_coins`
List all supported coins with IDs and symbols.

**Parameters:**
- `include_platform` (bool, optional): Include platform addresses (default: False)

**Example:**
```python
all_coins = await list_supported_coins(include_platform=True)
```

**Response:**
```json
[
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "platforms": {}
  },
  {
    "id": "ethereum",
    "symbol": "eth",
    "name": "Ethereum",
    "platforms": {
      "": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    }
  }
]
```

### Global Market Tools

#### `get_global_market_data`
Get global cryptocurrency market statistics.

**Example:**
```python
global_stats = await get_global_market_data()
```

**Response includes:**
- Total market cap (all currencies)
- Total 24h volume
- BTC dominance percentage
- ETH dominance percentage
- Market cap change 24h
- Active cryptocurrencies count
- Markets count
- Ongoing ICOs
- Ended ICOs
- Upcoming ICOs

### Exchange Tools

#### `list_exchanges`
List all exchanges with volume rankings.

**Parameters:**
- `per_page` (int, optional): Results per page (1-250, default: 100)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
exchanges = await list_exchanges(per_page=50)
```

**Response includes per exchange:**
- Name, ID, year established
- Country
- Trust score, rank
- 24h BTC volume
- Normalized 24h volume
- URL, image

#### `get_exchange_info`
Get detailed information about a specific exchange.

**Parameters:**
- `exchange_id` (string, required): Exchange ID (e.g., 'binance', 'coinbase_exchange')

**Example:**
```python
binance = await get_exchange_info(exchange_id="binance")
```

**Response includes:**
- Exchange details
- Trust score
- Trade volume
- Tickers
- Status updates

### Category Tools

#### `get_coin_categories`
Get coin categories with market data.

**Parameters:**
- `order` (string, optional): Sort order (default: 'market_cap_desc')

**Example:**
```python
categories = await get_coin_categories(order="market_cap_desc")
```

**Response includes categories like:**
- DeFi (Decentralized Finance)
- NFT (Non-Fungible Tokens)
- Gaming (GameFi)
- Meme Coins
- Layer 1 (L1)
- Layer 2 (L2)
- Smart Contract Platforms
- Exchange-based Tokens
- And 200+ more

**Each category includes:**
- Market cap
- 24h volume
- 24h market cap change
- Top 3 coins

### NFT Tools

#### `get_nft_data`
Get NFT collection data including floor price and volume.

**Parameters:**
- `nft_id` (string, required): NFT collection ID (e.g., 'bored-ape-yacht-club')

**Example:**
```python
bayc = await get_nft_data(nft_id="bored-ape-yacht-club")
cryptopunks = await get_nft_data(nft_id="cryptopunks")
```

**Response includes:**
- Floor price (ETH/USD)
- 24h volume
- Market cap
- Number of unique addresses (holders)
- Description
- Links (homepage, Twitter, Discord)

## Supported Currencies

### Fiat Currencies (150+)
Major: USD, EUR, GBP, JPY, CNY, KRW, INR, AUD, CAD, CHF, HKD, SGD, etc.

### Cryptocurrencies
BTC, ETH, BNB, XRP, ADA, SOL, DOT, DOGE, MATIC, and more

## Time Ranges

- `1` - Last 1 day
- `7` - Last 7 days
- `14` - Last 14 days
- `30` - Last 30 days
- `90` - Last 90 days
- `180` - Last 180 days
- `365` - Last 365 days
- `max` - All available history

**Data granularity:**
- 1 day: 5-minute intervals
- 2-90 days: Hourly intervals
- 90+ days: Daily intervals (00:00 UTC)

## Coin IDs vs Symbols

CoinGecko uses **coin IDs**, not symbols:

✅ Correct: `bitcoin`, `ethereum`, `cardano`
❌ Incorrect: `BTC`, `ETH`, `ADA`

**Find coin IDs:**
- Use `list_supported_coins()` to see all IDs
- Use `search_coins("bitcoin")` to search
- Visit coingecko.com and check the URL

**Examples:**
- Bitcoin → `bitcoin`
- Ethereum → `ethereum`
- Binance Coin → `binancecoin`
- USD Coin → `usd-coin`
- Wrapped Bitcoin → `wrapped-bitcoin`

## Rate Limits and Pricing

### Demo Plan ($0/month)
- **30 calls/minute**
- 10,000 calls/month
- Basic support
- All features included

### Analyst Plan ($129/month)
- **500 calls/minute**
- Rate limit headers
- Historical data
- Priority support

### Professional Plan ($499/month)
- **500 calls/minute**
- Dedicated support
- Custom solutions
- Enterprise SLA

**Rate limit headers in response:**
```
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 499
X-RateLimit-Reset: 1640000000
```

Visit [coingecko.com/en/api/pricing](https://www.coingecko.com/en/api/pricing) for current rates.

## Coverage

- **14,000+ cryptocurrencies** tracked
- **150+ fiat currencies** supported
- **800+ exchanges** monitored
- **200+ categories** organized
- **Real-time data** updates
- **Historical data** back to 2013 for major coins

## Market Data Explained

### Price
Current trading price in specified currency

### Market Cap
Current price × Circulating supply

### Volume
Total trading volume in last 24 hours

### Circulating Supply
Amount of coins currently in circulation

### Total Supply
Amount of coins that have been minted (minus burned)

### Max Supply
Maximum amount of coins that will ever exist

### ATH (All-Time High)
Highest price ever reached

### ATL (All-Time Low)
Lowest price ever reached

### Dominance
Coin's market cap / Total crypto market cap

## Best Practices

1. **Use coin IDs**: Always use coin IDs, not symbols
2. **Cache data**: Prices update every 1-5 minutes
3. **Batch requests**: Get multiple coins in one call
4. **Monitor rate limits**: Track remaining calls
5. **Handle errors**: Implement retry logic
6. **Use appropriate timeframes**: Match data granularity to needs
7. **Leverage categories**: Filter coins by category
8. **Store coin IDs**: Cache coin list locally

## Error Handling

Common error codes:

- **401 Unauthorized**: Invalid or missing API key
- **404 Not Found**: Invalid coin ID or endpoint
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: CoinGecko service issue
- **503 Service Unavailable**: Temporary maintenance

**Rate limit handling:**
```python
try:
    data = await get_coin_price(ids="bitcoin", vs_currencies="usd")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 429:
        # Wait and retry
        pass
```

## Use Cases

- **Portfolio Tracking**: Monitor crypto holdings value
- **Price Alerts**: Trigger notifications on price changes
- **Market Analysis**: Analyze trends and correlations
- **Trading Bots**: Algorithmic trading systems
- **Data Dashboards**: Real-time market displays
- **Research**: Historical data analysis
- **Tax Reporting**: Track cost basis and gains
- **News Aggregation**: Combine with sentiment data

## API Documentation

For detailed information:
- [CoinGecko API Documentation](https://docs.coingecko.com/reference/introduction)
- [API v3 Reference](https://docs.coingecko.com/v3.0.1/reference/introduction)
- [Rate Limits](https://docs.coingecko.com/reference/rate-limits)
- [Pagination](https://docs.coingecko.com/reference/pagination)

## Security Notes

- **Never commit API keys**: Store securely in environment variables
- **Use HTTPS**: All API calls use HTTPS
- **Monitor usage**: Check API call limits regularly
- **Rotate keys**: Change API keys periodically
- **Limit permissions**: Use minimum required access

## Support

- [CoinGecko Support](https://www.coingecko.com/en/about)
- [API Status](https://status.coingecko.com/)
- [Community Forum](https://www.coingecko.com/en/glossary)
- [Twitter](https://twitter.com/coingecko)
