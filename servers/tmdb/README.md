# TMDB MCP Server

MCP server for The Movie Database (TMDB) API. Search and discover movies, TV shows, cast information, ratings, and streaming availability from over 1 million titles.

## Features

- **Search**: Find movies, TV shows, and people
- **Details**: Get comprehensive information about titles and cast
- **Discovery**: Filter and discover content by genre, year, rating, and more
- **Trending & Popular**: Access trending and popular lists
- **Recommendations**: Find similar content
- **Streaming**: Check where content is available to stream
- **Credits**: Get cast and crew information
- **Genres**: Browse content by genre

## Setup

### Prerequisites

- TMDB account and API key
- 1 million+ movies and TV shows available

### Environment Variables

- `TMDB_API_KEY` (required): Your TMDB API key

**How to get credentials:**
1. Go to [themoviedb.org](https://www.themoviedb.org/)
2. Create an account or log in
3. Go to Settings → API
4. Request an API key (free for non-commercial use)
5. Choose "Developer" API key type
6. Fill in the application details
7. Copy your API key and store as `TMDB_API_KEY`

## Rate Limits

- **Free Tier**: 40 requests per 10 seconds
- **Rate limit headers** included in responses
- Consider implementing caching for frequently accessed data

## Image URLs

TMDB returns image paths that need to be combined with a base URL:

**Base URL**: `https://image.tmdb.org/t/p/`

**Available sizes:**
- **Posters**: w92, w154, w185, w342, w500, w780, original
- **Backdrops**: w300, w780, w1280, original
- **Profiles**: w45, w185, h632, original
- **Logos**: w45, w92, w154, w185, w300, w500, original

**Example:**
```
Path: /nBNZadXqJSdt05SHLqgT0HuC5Gm.jpg
Full URL: https://image.tmdb.org/t/p/w500/nBNZadXqJSdt05SHLqgT0HuC5Gm.jpg
```

## Available Tools

### Search Tools

#### `search_movies`
Search for movies by title.

**Parameters:**
- `query` (string, required): Movie title to search
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)
- `include_adult` (bool, optional): Include adult content (default: false)
- `year` (int, optional): Filter by release year

**Example:**
```python
results = await search_movies(
    query="The Matrix",
    year=1999,
    language="en-US"
)
```

#### `search_tv_shows`
Search for TV shows by title.

**Parameters:**
- `query` (string, required): TV show title
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)
- `include_adult` (bool, optional): Include adult content (default: false)
- `first_air_date_year` (int, optional): Filter by first air date year

**Example:**
```python
results = await search_tv_shows(
    query="Breaking Bad",
    first_air_date_year=2008
)
```

#### `search_people`
Search for actors, directors, and crew members.

**Parameters:**
- `query` (string, required): Person name
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)
- `include_adult` (bool, optional): Include adult content (default: false)

**Example:**
```python
results = await search_people(query="Tom Hanks")
```

### Details Tools

#### `get_movie_details`
Get detailed movie information including runtime, budget, revenue, ratings, and more.

**Parameters:**
- `movie_id` (int, required): TMDB movie ID
- `language` (string, optional): Language code (default: en-US)
- `append_to_response` (string, optional): Additional data (credits, videos, images, similar, recommendations)

**Example:**
```python
movie = await get_movie_details(
    movie_id=603,  # The Matrix
    append_to_response="credits,videos,recommendations"
)

# Returns:
# - title, overview, tagline
# - runtime, budget, revenue
# - release_date, status
# - vote_average, vote_count, popularity
# - genres, production_companies, production_countries
# - spoken_languages
# - credits (cast and crew)
# - videos (trailers, teasers)
# - recommendations
```

#### `get_tv_details`
Get TV show details including seasons, episodes, networks, and more.

**Parameters:**
- `tv_id` (int, required): TMDB TV show ID
- `language` (string, optional): Language code (default: en-US)
- `append_to_response` (string, optional): Additional data (credits, videos, images, similar, recommendations)

**Example:**
```python
show = await get_tv_details(
    tv_id=1396,  # Breaking Bad
    append_to_response="credits,videos"
)

# Returns:
# - name, overview, tagline
# - number_of_seasons, number_of_episodes
# - first_air_date, last_air_date, status
# - networks, production_companies
# - seasons (season number, episode count, air date, poster)
# - episode_run_time
# - vote_average, vote_count, popularity
# - genres
```

#### `get_person_details`
Get person biography, filmography, and credits.

**Parameters:**
- `person_id` (int, required): TMDB person ID
- `language` (string, optional): Language code (default: en-US)
- `append_to_response` (string, optional): Additional data (movie_credits, tv_credits, combined_credits, images)

**Example:**
```python
person = await get_person_details(
    person_id=31,  # Tom Hanks
    append_to_response="movie_credits,tv_credits"
)

# Returns:
# - name, biography
# - birthday, place_of_birth
# - known_for_department (Acting, Directing, etc.)
# - popularity
# - profile_path (profile image)
# - movie_credits (cast and crew roles)
# - tv_credits (cast and crew roles)
```

### Discovery Tools

#### `get_trending`
Get trending movies or TV shows.

**Parameters:**
- `media_type` (string, optional): movie, tv, or all (default: movie)
- `time_window` (string, optional): day or week (default: day)
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
# Trending movies today
trending = await get_trending(
    media_type="movie",
    time_window="day"
)

# Trending TV shows this week
trending_tv = await get_trending(
    media_type="tv",
    time_window="week"
)
```

#### `get_popular`
Get popular movies or TV shows.

**Parameters:**
- `media_type` (string, optional): movie or tv (default: movie)
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)
- `region` (string, optional): ISO 3166-1 code (US, GB, etc.)

**Example:**
```python
popular = await get_popular(
    media_type="movie",
    region="US"
)
```

#### `get_top_rated`
Get top rated movies or TV shows.

**Parameters:**
- `media_type` (string, optional): movie or tv (default: movie)
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)
- `region` (string, optional): ISO 3166-1 code

**Example:**
```python
top_rated = await get_top_rated(media_type="movie")
```

#### `discover_movies`
Discover movies with advanced filters.

**Parameters:**
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)
- `sort_by` (string, optional): Sort results (default: popularity.desc)
  - popularity.desc, popularity.asc
  - vote_average.desc, vote_average.asc
  - release_date.desc, release_date.asc
  - revenue.desc, revenue.asc
  - primary_release_date.desc, primary_release_date.asc
- `with_genres` (string, optional): Comma-separated genre IDs
- `year` (int, optional): Filter by release year
- `primary_release_year` (int, optional): Filter by primary release year
- `vote_average_gte` (float, optional): Minimum rating (0-10)
- `vote_average_lte` (float, optional): Maximum rating (0-10)
- `with_runtime_gte` (int, optional): Minimum runtime in minutes
- `with_runtime_lte` (int, optional): Maximum runtime in minutes
- `region` (string, optional): ISO 3166-1 code

**Example:**
```python
# Find highly-rated sci-fi movies from 2020-2024
movies = await discover_movies(
    with_genres="878",  # Sci-Fi
    primary_release_year=2023,
    vote_average_gte=7.0,
    sort_by="vote_average.desc"
)

# Find short comedies (under 90 minutes)
comedies = await discover_movies(
    with_genres="35",  # Comedy
    with_runtime_lte=90,
    sort_by="popularity.desc"
)
```

#### `discover_tv`
Discover TV shows with advanced filters.

**Parameters:**
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)
- `sort_by` (string, optional): Sort results (default: popularity.desc)
- `with_genres` (string, optional): Comma-separated genre IDs
- `first_air_date_year` (int, optional): Filter by first air date year
- `vote_average_gte` (float, optional): Minimum rating (0-10)
- `vote_average_lte` (float, optional): Maximum rating (0-10)
- `with_runtime_gte` (int, optional): Minimum episode runtime in minutes
- `with_runtime_lte` (int, optional): Maximum episode runtime in minutes
- `with_networks` (string, optional): Comma-separated network IDs (Netflix: 213, HBO: 49, etc.)

**Example:**
```python
# Find Netflix dramas
shows = await discover_tv(
    with_networks="213",  # Netflix
    with_genres="18",  # Drama
    sort_by="vote_average.desc",
    vote_average_gte=7.5
)
```

### Genre Tools

#### `get_genres`
Get list of all genres for movies or TV shows.

**Parameters:**
- `media_type` (string, optional): movie or tv (default: movie)
- `language` (string, optional): Language code (default: en-US)

**Example:**
```python
genres = await get_genres(media_type="movie")

# Returns:
# {
#   "genres": [
#     {"id": 28, "name": "Action"},
#     {"id": 12, "name": "Adventure"},
#     {"id": 16, "name": "Animation"},
#     {"id": 35, "name": "Comedy"},
#     {"id": 80, "name": "Crime"},
#     {"id": 99, "name": "Documentary"},
#     {"id": 18, "name": "Drama"},
#     {"id": 10751, "name": "Family"},
#     {"id": 14, "name": "Fantasy"},
#     {"id": 36, "name": "History"},
#     {"id": 27, "name": "Horror"},
#     {"id": 10402, "name": "Music"},
#     {"id": 9648, "name": "Mystery"},
#     {"id": 10749, "name": "Romance"},
#     {"id": 878, "name": "Science Fiction"},
#     {"id": 10770, "name": "TV Movie"},
#     {"id": 53, "name": "Thriller"},
#     {"id": 10752, "name": "War"},
#     {"id": 37, "name": "Western"}
#   ]
# }
```

### Credits Tools

#### `get_movie_credits`
Get cast and crew for a movie.

**Parameters:**
- `movie_id` (int, required): TMDB movie ID
- `language` (string, optional): Language code (default: en-US)

**Example:**
```python
credits = await get_movie_credits(movie_id=603)  # The Matrix

# Returns:
# {
#   "cast": [
#     {
#       "name": "Keanu Reeves",
#       "character": "Neo",
#       "order": 0,
#       "profile_path": "/path.jpg"
#     }
#   ],
#   "crew": [
#     {
#       "name": "Lana Wachowski",
#       "job": "Director",
#       "department": "Directing"
#     }
#   ]
# }
```

#### `get_tv_credits`
Get cast and crew for a TV show.

**Parameters:**
- `tv_id` (int, required): TMDB TV show ID
- `language` (string, optional): Language code (default: en-US)

**Example:**
```python
credits = await get_tv_credits(tv_id=1396)  # Breaking Bad
```

### Recommendation Tools

#### `get_recommendations`
Get similar movies or TV shows based on a title.

**Parameters:**
- `media_type` (string, required): movie or tv
- `media_id` (int, required): TMDB media ID
- `language` (string, optional): Language code (default: en-US)
- `page` (int, optional): Page number (default: 1)

**Example:**
```python
# Movies similar to The Matrix
similar = await get_recommendations(
    media_type="movie",
    media_id=603
)
```

#### `get_streaming_providers`
Get streaming availability for a movie or TV show by region.

**Parameters:**
- `media_type` (string, required): movie or tv
- `media_id` (int, required): TMDB media ID

**Example:**
```python
providers = await get_streaming_providers(
    media_type="movie",
    media_id=603
)

# Returns providers by region:
# {
#   "results": {
#     "US": {
#       "link": "https://www.themoviedb.org/movie/603/watch?locale=US",
#       "flatrate": [  # Streaming (subscription)
#         {"provider_id": 8, "provider_name": "Netflix", "logo_path": "/path.jpg"}
#       ],
#       "rent": [  # Rent
#         {"provider_id": 2, "provider_name": "Apple TV", "logo_path": "/path.jpg"}
#       ],
#       "buy": [  # Buy
#         {"provider_id": 3, "provider_name": "Google Play Movies"}
#       ]
#     },
#     "GB": {...},
#     "CA": {...}
#   }
# }
```

## Genre IDs

**Movie Genres:**
- 28: Action
- 12: Adventure
- 16: Animation
- 35: Comedy
- 80: Crime
- 99: Documentary
- 18: Drama
- 10751: Family
- 14: Fantasy
- 36: History
- 27: Horror
- 10402: Music
- 9648: Mystery
- 10749: Romance
- 878: Science Fiction
- 10770: TV Movie
- 53: Thriller
- 10752: War
- 37: Western

**TV Genres:**
- 10759: Action & Adventure
- 16: Animation
- 35: Comedy
- 80: Crime
- 99: Documentary
- 18: Drama
- 10751: Family
- 10762: Kids
- 9648: Mystery
- 10763: News
- 10764: Reality
- 10765: Sci-Fi & Fantasy
- 10766: Soap
- 10767: Talk
- 10768: War & Politics
- 37: Western

## Network IDs

Common streaming networks:
- **213**: Netflix
- **49**: HBO
- **2739**: Disney+
- **1024**: Amazon Prime Video
- **453**: Hulu
- **2552**: Apple TV+
- **2697**: Peacock
- **1899**: Max
- **389**: Showtime
- **67**: Paramount+

## Language Codes

Common language codes (ISO 639-1):
- `en-US`: English (United States)
- `es-ES`: Spanish (Spain)
- `fr-FR`: French (France)
- `de-DE`: German (Germany)
- `it-IT`: Italian (Italy)
- `ja-JP`: Japanese (Japan)
- `ko-KR`: Korean (South Korea)
- `pt-BR`: Portuguese (Brazil)
- `zh-CN`: Chinese (Simplified)

## Region Codes

Common region codes (ISO 3166-1):
- `US`: United States
- `GB`: United Kingdom
- `CA`: Canada
- `AU`: Australia
- `DE`: Germany
- `FR`: France
- `ES`: Spain
- `IT`: Italy
- `JP`: Japan
- `KR`: South Korea
- `BR`: Brazil
- `MX`: Mexico

## Pagination

Most list endpoints support pagination:

```python
# Page 1
results_page1 = await search_movies(query="action", page=1)

# Page 2
results_page2 = await search_movies(query="action", page=2)

# Response includes:
# - page: Current page number
# - total_pages: Total number of pages
# - total_results: Total number of results
# - results: Array of items (usually 20 per page)
```

## Common Use Cases

### Find a Movie and Get Full Details
```python
# Search for the movie
search_results = await search_movies(query="Inception")
movie_id = search_results["results"][0]["id"]

# Get full details with credits and videos
details = await get_movie_details(
    movie_id=movie_id,
    append_to_response="credits,videos,recommendations"
)

# Get streaming availability
streaming = await get_streaming_providers(
    media_type="movie",
    media_id=movie_id
)
```

### Discover New Content
```python
# Find popular sci-fi movies from 2023
movies = await discover_movies(
    with_genres="878",
    primary_release_year=2023,
    sort_by="popularity.desc",
    vote_average_gte=6.0
)

# Find Netflix original series
shows = await discover_tv(
    with_networks="213",
    first_air_date_year=2023,
    sort_by="vote_average.desc"
)
```

### Get Trending Content
```python
# What's trending today?
trending_today = await get_trending(
    media_type="all",
    time_window="day"
)

# Popular movies in the US
popular_us = await get_popular(
    media_type="movie",
    region="US"
)
```

### Research Actors and Filmography
```python
# Search for an actor
search = await search_people(query="Leonardo DiCaprio")
person_id = search["results"][0]["id"]

# Get full filmography
person = await get_person_details(
    person_id=person_id,
    append_to_response="movie_credits,tv_credits"
)

# Returns all movies and TV shows they appeared in
```

## Best Practices

1. **Cache frequently accessed data**: Genre lists, popular content, and trending lists
2. **Use append_to_response**: Combine multiple requests into one
3. **Respect rate limits**: 40 requests per 10 seconds
4. **Store image sizes appropriately**: Use smaller sizes for thumbnails
5. **Filter by region**: Get relevant streaming providers for your users
6. **Use language codes**: Provide localized content
7. **Implement pagination**: Handle large result sets properly
8. **Check vote_count**: High ratings with few votes may not be reliable

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Movie, show, or person not found
- **429 Too Many Requests**: Rate limit exceeded (wait and retry)
- **500 Internal Server Error**: TMDB service issue (retry later)

## Data Freshness

- **Daily updates**: New releases, trending content, popularity scores
- **Real-time streaming data**: Provider availability updates
- **User ratings**: Vote averages update continuously
- **Content metadata**: Updated as information becomes available

## API Documentation

- [TMDB API Documentation](https://developer.themoviedb.org/docs)
- [API Reference](https://developer.themoviedb.org/reference/intro/getting-started)
- [Image Documentation](https://developer.themoviedb.org/docs/image-basics)
- [API Terms of Use](https://www.themoviedb.org/terms-of-use)

## Support

- [TMDB Support](https://www.themoviedb.org/talk)
- [API Forums](https://www.themoviedb.org/talk/category/5047958519c29526b50017d6)
- [Status Page](https://status.themoviedb.org/)
- [Contact](https://www.themoviedb.org/about/staying-in-touch)
