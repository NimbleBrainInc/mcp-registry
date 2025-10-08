# Brave Search MCP Server

MCP server providing access to Brave Search API for privacy-focused web search.

## Features

### Core Capabilities
- **Web Search** - Fast, private web search with no tracking
- **News Search** - Latest news articles from trusted sources
- **Image Search** - Find images with safe search controls
- **Video Search** - Discover video content
- **Local Search** - Find nearby businesses and places
- **Search Suggestions** - Autocomplete and query suggestions
- **AI Summaries** - Get AI-powered search result summaries

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your Brave Search API key
```

## Configuration

### Get Your Brave Search API Key
1. Go to https://brave.com/search/api/
2. Sign up for free tier (2,000 queries/month) or paid plans
3. Generate an API key
4. Copy the key and add it to your `.env` file

### NimbleBrain Configuration

Deploy via NimbleBrain platform with your Brave Search API key.

## Available Tools

### web_search
Perform a web search with ranking and relevance.

**Parameters:**
- `query` (required): Search query
- `count`: Results to return (1-20, default: 10)
- `offset`: Pagination offset
- `country`: Country code (US, GB, FR, etc.)
- `search_lang`: Language code (en, es, fr, etc.)
- `safesearch`: "off", "moderate", or "strict"
- `freshness`: "pd" (day), "pw" (week), "pm" (month), "py" (year)
- `text_decorations`: Include text formatting (default: true)
- `spellcheck`: Enable spell checking (default: true)

**Example:**
```json
{
  "query": "machine learning tutorials",
  "count": 10,
  "freshness": "pm"
}
```

### news_search
Search for recent news articles.

**Parameters:**
- `query` (required): Search query
- `count`: Results (1-20, default: 10)
- `offset`: Pagination offset
- `country`: Country code
- `search_lang`: Language code
- `freshness`: Time filter
- `spellcheck`: Enable spell checking

**Example:**
```json
{
  "query": "AI breakthroughs 2024",
  "count": 10,
  "freshness": "pw"
}
```

### image_search
Search for images.

**Parameters:**
- `query` (required): Search query
- `count`: Results (1-20, default: 10)
- `offset`: Pagination offset
- `country`: Country code
- `search_lang`: Language code
- `safesearch`: Safety level
- `spellcheck`: Enable spell checking

**Example:**
```json
{
  "query": "mountain landscapes",
  "count": 20,
  "safesearch": "strict"
}
```

### video_search
Search for videos.

**Parameters:**
- `query` (required): Search query
- `count`: Results (1-20, default: 10)
- `offset`: Pagination offset
- `country`: Country code
- `search_lang`: Language code
- `safesearch`: Safety level
- `spellcheck`: Enable spell checking

**Example:**
```json
{
  "query": "python programming tutorials",
  "count": 10
}
```

### suggest
Get search suggestions/autocomplete.

**Parameters:**
- `query` (required): Partial query
- `country`: Country code
- `search_lang`: Language code

**Example:**
```json
{
  "query": "how to learn"
}
```

### local_search
Find local businesses and places.

**Parameters:**
- `query` (required): Search query with location
- `count`: Results (1-20, default: 10)
- `offset`: Pagination offset
- `country`: Country code
- `search_lang`: Language code

**Example:**
```json
{
  "query": "coffee shops near San Francisco",
  "count": 10
}
```

### summarize_search
Get AI-powered summary of search results.

**Parameters:**
- `query` (required): Search query
- `count`: Source results for summary (1-20, default: 5)
- `entity_info`: Include entity information (default: true)

**Example:**
```json
{
  "query": "quantum computing applications",
  "count": 5
}
```

## Usage Examples

### Basic Web Search
```json
{
  "tool": "web_search",
  "query": "best practices for REST APIs"
}
```

### Recent News
```json
{
  "tool": "news_search",
  "query": "artificial intelligence",
  "freshness": "pd",
  "count": 10
}
```

### Image Search with Safe Search
```json
{
  "tool": "image_search",
  "query": "data visualization examples",
  "safesearch": "strict"
}
```

### Local Business Search
```json
{
  "tool": "local_search",
  "query": "restaurants in Paris"
}
```

### Get Search Suggestions
```json
{
  "tool": "suggest",
  "query": "what is"
}
```

### AI-Powered Summary
```json
{
  "tool": "summarize_search",
  "query": "climate change solutions",
  "count": 5
}
```

## Rate Limits & Pricing

### Free Tier
- 2,000 queries/month
- All search types included
- No credit card required

### Paid Plans
- **Basic**: $5/month - 15,000 queries
- **Pro**: $15/month - 50,000 queries  
- **Enterprise**: Custom pricing

Check current pricing: https://brave.com/search/api/

## Why Brave Search?

### Privacy-First
- No user tracking or profiling
- No stored search history
- Independent index (not Google/Bing)

### Quality Results
- Built on Brave's independent index
- AI-powered summaries
- Fast response times

### Developer-Friendly
- Simple API key authentication
- Generous free tier
- Comprehensive documentation

## Supported Countries & Languages

### Countries (Sample)
- US, GB, CA, AU, DE, FR, ES, IT, JP, BR, IN, and 100+ more

### Languages
- English, Spanish, French, German, Japanese, Chinese, Portuguese, Russian, and 50+ more

## Use Cases

### For Developers
- Add search to applications
- Research and information gathering
- Content discovery
- Real-time data retrieval

### For AI Agents
- Web research capabilities
- Fact-checking and verification
- Current event awareness
- Multi-source information synthesis

## Error Handling

The server handles:
- Invalid API keys
- Rate limiting (429 errors)
- Network timeouts
- Invalid parameters
- No results scenarios

## Best Practices

1. **Cache Results**: Store frequent searches to reduce API calls
2. **Use Freshness Filters**: Narrow results by time for better relevance
3. **Implement Pagination**: Use offset for large result sets
4. **Safe Search**: Enable for user-facing applications
5. **Country/Language**: Specify for localized results
6. **Rate Limiting**: Monitor usage to stay within limits

## Security Notes

- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly
- Monitor usage in Brave dashboard
- Set up usage alerts

## Troubleshooting

### "Invalid API Key" Error
- Verify key in `.env` file
- Check key is active at brave.com/search/api
- Ensure no extra spaces

### Rate Limit Errors
- Check monthly usage in dashboard
- Upgrade plan if needed
- Implement result caching

### No Results
- Try broader search terms
- Remove overly specific filters
- Check spelling

## Resources

- [Brave Search API](https://brave.com/search/api/)
- [API Documentation](https://api.search.brave.com/app/documentation/web-search/get-started)
- [Pricing](https://brave.com/search/api/#pricing)
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT License - feel free to use in your projects!