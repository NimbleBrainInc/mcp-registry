# Pinecone MCP Server

MCP server for Pinecone vector database. Store and search embeddings for similarity search, semantic search, and RAG (Retrieval Augmented Generation) applications.

## Features

- **Index Management**: Create, list, describe, and delete vector indexes
- **Vector Operations**: Upsert, query, fetch, update, and delete vectors
- **Similarity Search**: Find similar vectors with cosine, euclidean, or dot product metrics
- **Metadata Filtering**: Hybrid search with metadata filters
- **Namespaces**: Data isolation for multi-tenancy
- **Collections**: Create backups from indexes
- **Statistics**: Get vector counts and index stats

## Setup

### Prerequisites

- Pinecone account
- API key and environment name

### Environment Variables

- `PINECONE_API_KEY` (required): Your Pinecone API key
- `PINECONE_ENVIRONMENT` (required): Your Pinecone environment

**How to get credentials:**
1. Go to [app.pinecone.io](https://app.pinecone.io)
2. Sign up or log in
3. Navigate to API Keys section
4. Copy your API key
5. Note your environment (e.g., `us-west1-gcp`, `us-east-1-aws`)
6. Store as `PINECONE_API_KEY` and `PINECONE_ENVIRONMENT`

## Index Types

### Serverless (Recommended)
- Pay per usage
- Auto-scaling
- No infrastructure management
- Available regions: AWS (us-east-1, us-west-2), GCP (us-central1, us-west1), Azure (eastus)

### Pod-based
- Fixed capacity
- Dedicated resources
- More control over performance
- Higher cost

## Vector Dimensions

Match your embedding model:
- **OpenAI text-embedding-ada-002**: 1536 dimensions
- **OpenAI text-embedding-3-small**: 1536 dimensions
- **OpenAI text-embedding-3-large**: 3072 dimensions
- **sentence-transformers/all-MiniLM-L6-v2**: 384 dimensions
- **sentence-transformers/all-mpnet-base-v2**: 768 dimensions

## Distance Metrics

- **cosine** - Cosine similarity (recommended for most use cases)
- **euclidean** - Euclidean distance
- **dotproduct** - Dot product similarity

## Available Tools

### Index Management

#### `list_indexes`
List all indexes in the project.

**Example:**
```python
indexes = await list_indexes()
```

#### `create_index`
Create a new vector index.

**Parameters:**
- `name` (string, required): Index name
- `dimension` (int, required): Vector dimension
- `metric` (string, optional): Distance metric (default: 'cosine')
- `spec_type` (string, optional): 'serverless' or 'pod' (default: 'serverless')
- `cloud` (string, optional): 'aws', 'gcp', or 'azure' (default: 'aws')
- `region` (string, optional): Region (default: 'us-east-1')

**Example:**
```python
index = await create_index(
    name="my-index",
    dimension=1536,  # OpenAI embeddings
    metric="cosine",
    spec_type="serverless",
    cloud="aws",
    region="us-east-1"
)
```

#### `describe_index`
Get index configuration and status.

**Example:**
```python
info = await describe_index(index_name="my-index")
```

#### `delete_index`
Delete an index.

**Example:**
```python
result = await delete_index(index_name="my-index")
```

### Vector Operations

#### `upsert_vectors`
Insert or update vectors with metadata.

**Parameters:**
- `index_name` (string, required): Index name
- `vectors` (list, required): List of vector objects
- `namespace` (string, optional): Namespace (default: "")

**Vector format:**
```python
{
    "id": "vec1",
    "values": [0.1, 0.2, 0.3, ...],  # Must match index dimension
    "metadata": {"key": "value"}  # Optional
}
```

**Example:**
```python
result = await upsert_vectors(
    index_name="my-index",
    vectors=[
        {
            "id": "doc1",
            "values": [0.1, 0.2, ...],  # 1536 dimensions
            "metadata": {
                "title": "Document 1",
                "category": "tech",
                "year": 2024
            }
        },
        {
            "id": "doc2",
            "values": [0.3, 0.4, ...],
            "metadata": {
                "title": "Document 2",
                "category": "science"
            }
        }
    ],
    namespace="production"
)
```

#### `query_vectors`
Query similar vectors.

**Parameters:**
- `index_name` (string, required): Index name
- `vector` (list, optional): Query vector (use this OR id)
- `id` (string, optional): Vector ID to use as query (use this OR vector)
- `top_k` (int, optional): Number of results (default: 10)
- `namespace` (string, optional): Namespace (default: "")
- `include_values` (bool, optional): Include vectors (default: False)
- `include_metadata` (bool, optional): Include metadata (default: True)
- `filter` (dict, optional): Metadata filter

**Example:**
```python
# Query by vector
results = await query_vectors(
    index_name="my-index",
    vector=[0.1, 0.2, ...],  # Your query embedding
    top_k=5,
    filter={"category": {"$eq": "tech"}, "year": {"$gte": 2023}},
    include_metadata=True
)

# Query by existing vector ID
results = await query_vectors(
    index_name="my-index",
    id="doc1",
    top_k=5
)
```

**Response:**
```json
{
  "matches": [
    {
      "id": "doc1",
      "score": 0.95,
      "metadata": {"title": "Document 1", "category": "tech"}
    }
  ]
}
```

#### `fetch_vectors`
Fetch vectors by IDs.

**Example:**
```python
vectors = await fetch_vectors(
    index_name="my-index",
    ids=["doc1", "doc2", "doc3"],
    namespace="production"
)
```

#### `update_vector`
Update vector values or metadata.

**Example:**
```python
# Update values
result = await update_vector(
    index_name="my-index",
    id="doc1",
    values=[0.5, 0.6, ...]
)

# Update metadata
result = await update_vector(
    index_name="my-index",
    id="doc1",
    set_metadata={"category": "updated", "year": 2025}
)
```

#### `delete_vectors`
Delete vectors.

**Example:**
```python
# Delete by IDs
result = await delete_vectors(
    index_name="my-index",
    ids=["doc1", "doc2"]
)

# Delete by filter
result = await delete_vectors(
    index_name="my-index",
    filter={"year": {"$lt": 2020}}
)

# Delete all in namespace
result = await delete_vectors(
    index_name="my-index",
    delete_all=True,
    namespace="test"
)
```

### Statistics & Utility

#### `describe_index_stats`
Get index statistics.

**Example:**
```python
stats = await describe_index_stats(index_name="my-index")
# Returns: dimension, totalVectorCount, indexFullness, namespaces
```

#### `list_vector_ids`
List all vector IDs.

**Example:**
```python
ids = await list_vector_ids(
    index_name="my-index",
    namespace="production",
    prefix="doc",
    limit=100
)
```

#### `create_collection`
Create a collection (backup) from an index.

**Example:**
```python
collection = await create_collection(
    name="my-backup",
    source_index="my-index"
)
```

## Namespaces

Namespaces provide data isolation within an index:

```python
# Production data
await upsert_vectors(index_name="my-index", vectors=[...], namespace="prod")

# Test data
await upsert_vectors(index_name="my-index", vectors=[...], namespace="test")

# Query only production
results = await query_vectors(index_name="my-index", vector=[...], namespace="prod")
```

## Metadata Filtering

Filter vectors during queries using metadata:

**Operators:**
- `$eq` - Equal
- `$ne` - Not equal
- `$gt` - Greater than
- `$gte` - Greater than or equal
- `$lt` - Less than
- `$lte` - Less than or equal
- `$in` - In array
- `$nin` - Not in array

**Examples:**
```python
# Simple filter
filter={"category": {"$eq": "tech"}}

# Range filter
filter={"year": {"$gte": 2020, "$lte": 2024}}

# Multiple conditions
filter={
    "$and": [
        {"category": {"$eq": "tech"}},
        {"year": {"$gte": 2020}}
    ]
}

# OR condition
filter={
    "$or": [
        {"category": {"$eq": "tech"}},
        {"category": {"$eq": "science"}}
    ]
}

# In array
filter={"category": {"$in": ["tech", "science", "engineering"]}}
```

## RAG Example with OpenAI

```python
import openai

# 1. Generate embedding
response = openai.Embedding.create(
    input="What is machine learning?",
    model="text-embedding-ada-002"
)
query_embedding = response['data'][0]['embedding']

# 2. Query Pinecone
results = await query_vectors(
    index_name="knowledge-base",
    vector=query_embedding,
    top_k=3,
    include_metadata=True
)

# 3. Get context from results
context = "\n".join([match['metadata']['text'] for match in results['matches']])

# 4. Generate answer with context
answer = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"Answer based on this context:\n{context}"},
        {"role": "user", "content": "What is machine learning?"}
    ]
)
```

## Rate Limits

### Free Tier (Starter)
- **100,000 operations/month**
- 1 pod/index
- 100 indexes max

### Paid Tiers
- **Standard**: $70/month, unlimited operations
- **Enterprise**: Custom pricing, dedicated support

## Best Practices

1. **Match dimensions**: Ensure vector dimensions match index
2. **Use namespaces**: Separate prod/test/dev data
3. **Add metadata**: Enable hybrid search and filtering
4. **Batch upserts**: Insert multiple vectors per request
5. **Use serverless**: For most applications (cost-effective)
6. **Monitor usage**: Track vector count and operations
7. **Create backups**: Use collections for important data
8. **Optimize queries**: Use appropriate top_k values

## Common Use Cases

- **Semantic Search**: Find similar documents or products
- **RAG**: Retrieval for LLM context
- **Recommendation Systems**: Similar item recommendations
- **Duplicate Detection**: Find near-duplicate content
- **Anomaly Detection**: Identify outliers
- **Image Search**: Visual similarity search
- **Chatbot Memory**: Store conversation context

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Index or vector not found
- **400 Bad Request**: Invalid dimensions or parameters
- **429 Too Many Requests**: Rate limit exceeded
- **503 Service Unavailable**: Pinecone service issue

## API Documentation

- [Pinecone Documentation](https://docs.pinecone.io/)
- [API Reference](https://docs.pinecone.io/reference/api/introduction)
- [Python SDK](https://docs.pinecone.io/docs/python-client)
- [Serverless Indexes](https://docs.pinecone.io/docs/serverless-indexes)
- [Metadata Filtering](https://docs.pinecone.io/docs/metadata-filtering)

## Support

- [Pinecone Community](https://community.pinecone.io/)
- [Discord](https://discord.gg/pinecone)
- [Support](https://support.pinecone.io/)
- [Status Page](https://status.pinecone.io/)
