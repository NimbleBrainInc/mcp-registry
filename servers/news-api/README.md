# News API MCP Server

MCP server for accessing news articles, breaking headlines, and sources from News API. Search through 80,000+ news sources worldwide with advanced filtering options.

## Features

- **Article Search**: Search all articles with keywords, dates, and filters
- **Top Headlines**: Get breaking news and top headlines by country/category
- **Source Discovery**: List and filter from 80,000+ news sources
- **Multi-language**: Access news in 14 different languages
- **Country-specific**: Get news from 150+ countries
- **Category Filtering**: Browse news by 7 major categories

## Setup

### Prerequisites

- News API account (free or paid)
- API key from [newsapi.org](https://newsapi.org/register)

### Environment Variables

- `NEWS_API_KEY` (required): Your News API key

**How to get an API key:**
1. Go to [newsapi.org/register](https://newsapi.org/register)
2. Sign up for a free or paid account
3. Find your API key in the dashboard
4. Free tier includes 100 requests/day

## Available Tools

### Article Search Tools

#### `search_everything`
Search through all articles with advanced filtering.

**Parameters:**
- `q` (string, required): Keywords or phrases to search for
- `from_date` (string, optional): Oldest date (ISO 8601: YYYY-MM-DD)
- `to_date` (string, optional): Newest date (ISO 8601: YYYY-MM-DD)
- `sources` (string, optional): Comma-separated source IDs (e.g., 'bbc-news,cnn')
- `domains` (string, optional): Comma-separated domains (e.g., 'bbc.co.uk,techcrunch.com')
- `language` (string, optional): Language code ('en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ar', 'zh', etc.)
- `sort_by` (string, optional): Sort order ('relevancy', 'popularity', 'publishedAt', default: 'publishedAt')
- `page_size` (int, optional): Results per page (max: 100, default: 20)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
articles = await search_everything(
    q="artificial intelligence",
    from_date="2024-01-01",
    to_date="2024-12-31",
    language="en",
    sort_by="relevancy",
    page_size=50
)
```

#### `get_top_headlines`
Get breaking news and top headlines.

**Parameters:**
- `country` (string, optional): 2-letter ISO country code ('us', 'gb', 'ca', 'au', 'de', 'fr', etc.)
- `category` (string, optional): Category ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
- `sources` (string, optional): Comma-separated source IDs
- `q` (string, optional): Keywords to search for
- `page_size` (int, optional): Results per page (max: 100, default: 20)
- `page` (int, optional): Page number (default: 1)

**Note:** Cannot mix 'sources' with 'country' or 'category' parameters.

**Example:**
```python
headlines = await get_top_headlines(
    country="us",
    category="technology",
    page_size=10
)
```

#### `search_by_source`
Search articles from specific news sources.

**Parameters:**
- `sources` (string, required): Comma-separated source IDs
- `q` (string, optional): Keywords to search for
- `from_date` (string, optional): Oldest date (ISO 8601: YYYY-MM-DD)
- `to_date` (string, optional): Newest date (ISO 8601: YYYY-MM-DD)
- `sort_by` (string, optional): Sort order (default: 'publishedAt')
- `page_size` (int, optional): Results per page (max: 100, default: 20)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
articles = await search_by_source(
    sources="bbc-news,cnn,techcrunch",
    q="climate change",
    page_size=20
)
```

### Source Discovery Tools

#### `get_sources`
Get all available news sources with optional filters.

**Parameters:**
- `category` (string, optional): Filter by category
- `language` (string, optional): Filter by language code
- `country` (string, optional): Filter by country code

**Example:**
```python
sources = await get_sources(
    category="technology",
    language="en",
    country="us"
)
```

### Category & Country Tools

#### `search_by_category`
Get news articles by category.

**Parameters:**
- `category` (string, required): News category
- `country` (string, optional): Country code
- `q` (string, optional): Keywords to search for
- `page_size` (int, optional): Results per page (max: 100, default: 20)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
tech_news = await search_by_category(
    category="technology",
    country="us",
    page_size=25
)
```

#### `search_by_country`
Get news articles by country.

**Parameters:**
- `country` (string, required): 2-letter ISO country code
- `category` (string, optional): News category
- `q` (string, optional): Keywords to search for
- `page_size` (int, optional): Results per page (max: 100, default: 20)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
uk_news = await search_by_country(
    country="gb",
    category="business",
    page_size=15
)
```

#### `search_by_language`
Get news articles in a specific language.

**Parameters:**
- `language` (string, required): 2-letter ISO language code
- `q` (string, required): Keywords to search for
- `from_date` (string, optional): Oldest date (ISO 8601: YYYY-MM-DD)
- `to_date` (string, optional): Newest date (ISO 8601: YYYY-MM-DD)
- `sort_by` (string, optional): Sort order (default: 'publishedAt')
- `page_size` (int, optional): Results per page (max: 100, default: 20)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
french_articles = await search_by_language(
    language="fr",
    q="économie",
    page_size=30
)
```

### Trending Tools

#### `get_trending_topics`
Get currently trending news topics and headlines.

**Parameters:**
- `country` (string, optional): Country code (default: 'us')
- `category` (string, optional): News category (default: 'general')
- `page_size` (int, optional): Results per page (max: 100, default: 20)

**Example:**
```python
trending = await get_trending_topics(
    country="us",
    category="general",
    page_size=20
)
```

## Supported Options

### Categories (7 available)
- `business` - Business news and finance
- `entertainment` - Entertainment and celebrity news
- `general` - General news (default)
- `health` - Health and medical news
- `science` - Science and research news
- `sports` - Sports news and scores
- `technology` - Technology and gadget news

### Languages (14 available)
- `ar` - Arabic
- `de` - German
- `en` - English
- `es` - Spanish
- `fr` - French
- `he` - Hebrew
- `it` - Italian
- `nl` - Dutch
- `no` - Norwegian
- `pt` - Portuguese
- `ru` - Russian
- `sv` - Swedish
- `ud` - Urdu
- `zh` - Chinese

### Countries (150+ available)
Popular country codes:
- `us` - United States
- `gb` - United Kingdom
- `ca` - Canada
- `au` - Australia
- `de` - Germany
- `fr` - France
- `in` - India
- `jp` - Japan
- `cn` - China
- `br` - Brazil
- `mx` - Mexico
- `za` - South Africa

[Full list of country codes](https://newsapi.org/docs/endpoints/sources)

## Rate Limits and Pricing

### Free Tier
- **100 requests/day**
- Historical articles up to 1 month old
- Top headlines and sources
- Development use only

### Paid Tiers

**Developer Plan ($449/month)**
- 250,000 requests/month
- Historical articles up to 2 years
- Commercial use allowed
- Email support

**Business Plan ($999/month)**
- 1,000,000 requests/month
- Full historical archive
- Commercial use allowed
- Priority support

**Enterprise (Custom pricing)**
- Unlimited requests
- Full historical archive
- Dedicated support
- SLA guarantees

Visit [newsapi.org/pricing](https://newsapi.org/pricing) for current rates.

### Rate Limit Headers
All responses include rate limit information:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets

## Search Tips

### Keywords and Phrases
- Use quotes for exact phrases: `"climate change"`
- Use AND/OR/NOT operators: `tesla AND "electric cars"`
- Use parentheses for complex queries: `(bitcoin OR cryptocurrency) AND regulation`

### Date Ranges
- Dates must be in ISO 8601 format: `YYYY-MM-DD`
- Example: `from_date="2024-01-01"`, `to_date="2024-12-31"`
- Free tier limited to last 30 days

### Sorting Options
- `relevancy` - Most relevant articles first
- `popularity` - Most popular/shared articles
- `publishedAt` - Most recent articles (default)

### Pagination
- Maximum `page_size` is 100
- Results are paginated, use `page` parameter to navigate
- `totalResults` field shows total articles available

## Response Format

All successful responses include:
```json
{
  "status": "ok",
  "totalResults": 12345,
  "articles": [
    {
      "source": {
        "id": "bbc-news",
        "name": "BBC News"
      },
      "author": "John Doe",
      "title": "Article Title",
      "description": "Article description...",
      "url": "https://example.com/article",
      "urlToImage": "https://example.com/image.jpg",
      "publishedAt": "2024-01-15T10:30:00Z",
      "content": "Article content..."
    }
  ]
}
```

## Error Handling

Common error codes:
- **400 Bad Request** - Invalid parameters
- **401 Unauthorized** - Invalid or missing API key
- **429 Too Many Requests** - Rate limit exceeded
- **500 Server Error** - News API service issue

## Security Best Practices

1. **Never commit API keys**: Store in environment variables
2. **Use HTTPS only**: All API calls use HTTPS
3. **Monitor usage**: Check rate limits regularly
4. **Rotate keys**: Change API keys periodically
5. **Restrict domains**: Configure allowed domains in News API dashboard
6. **Use proxies**: Consider caching responses to reduce API calls

## API Documentation

For detailed information about News API:
- [News API Documentation](https://newsapi.org/docs)
- [API Endpoints Reference](https://newsapi.org/docs/endpoints)
- [Sources List](https://newsapi.org/docs/endpoints/sources)
- [Error Codes](https://newsapi.org/docs/errors)

## Use Cases

- **News Aggregation**: Build custom news dashboards
- **Market Research**: Monitor industry trends and competitors
- **Content Curation**: Discover trending topics and stories
- **Sentiment Analysis**: Analyze news sentiment for brands
- **Breaking News Alerts**: Get real-time notifications
- **Research Tools**: Access historical news archives
- **Media Monitoring**: Track brand mentions and coverage

## Limitations

1. Free tier limited to 100 requests/day
2. Historical data restricted based on plan
3. Cannot mix 'sources' with 'country/category' in top-headlines
4. Maximum 100 articles per request
5. Some sources may require attribution
6. Real-time news has 15-minute delay on free tier

## Support

- [News API Support](https://newsapi.org/support)
- [FAQs](https://newsapi.org/faq)
- [Status Page](https://newsapi.org/status)
