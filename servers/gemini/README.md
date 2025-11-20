# Google Gemini MCP Server

MCP server for accessing Google's Gemini multimodal AI models. Generate text, analyze images and videos, process PDFs, create embeddings, and leverage function calling with models that support up to 2 million token context windows.

## Features

- **Text Generation**: Advanced LLMs with up to 2M token context
- **Multimodal Analysis**: Images, videos, audio, and PDFs
- **Chat**: Multi-turn conversations with context
- **Function Calling**: Tool use and structured outputs
- **Embeddings**: High-quality text embeddings
- **Streaming**: Real-time response streaming
- **JSON Mode**: Structured JSON output generation
- **Token Counting**: Estimate costs before generation

## Setup

### Prerequisites

- Google Cloud account or Google AI Studio access
- Gemini API key

### Environment Variables

- `GEMINI_API_KEY` (required): Your Google Gemini API key

**How to get an API key:**
1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click "Create API key"
3. Select a Google Cloud project or create new one
4. Copy the API key (starts with `AIza...`)
5. Store as `GEMINI_API_KEY`

## Available Models

### Text Models
- **gemini-1.5-pro-latest** - Best quality, 2M token context, multimodal
- **gemini-1.5-flash-latest** - Fast and efficient, 1M token context
- **gemini-2.0-flash-exp** - Experimental with latest features

### Embedding Models
- **text-embedding-004** - 768-dimension text embeddings

## Available Tools

### Text Generation

#### `generate_text`
Generate text with Gemini models.

**Parameters:**
- `prompt` (string, required): Input text prompt
- `model` (string, optional): Model name (default: 'gemini-1.5-flash-latest')
- `temperature` (float, optional): Sampling temperature 0-2
- `top_p` (float, optional): Nucleus sampling 0-1
- `top_k` (int, optional): Top-k sampling
- `max_output_tokens` (int, optional): Maximum tokens to generate
- `system_instruction` (string, optional): System instruction for behavior

**Example:**
```python
result = await generate_text(
    prompt="Explain quantum computing in simple terms",
    model="gemini-1.5-pro-latest",
    temperature=0.7,
    max_output_tokens=500,
    system_instruction="You are a helpful science educator"
)
```

### Conversation

#### `chat`
Multi-turn conversation with context.

**Parameters:**
- `messages` (list, required): List of messages with 'role' ('user'/'model') and 'text'
- `model` (string, optional): Model name
- `temperature` (float, optional): Sampling temperature
- `system_instruction` (string, optional): System instruction

**Example:**
```python
result = await chat(
    messages=[
        {"role": "user", "text": "What is machine learning?"},
        {"role": "model", "text": "Machine learning is..."},
        {"role": "user", "text": "Can you give an example?"}
    ],
    model="gemini-1.5-flash-latest"
)
```

### Multimodal Analysis

#### `analyze_image`
Analyze images with vision capabilities.

**Parameters:**
- `prompt` (string, required): Question about the image
- `image_base64` (string, required): Base64 encoded image
- `mime_type` (string, optional): Image MIME type (default: 'image/jpeg')
- `model` (string, optional): Model name

**Example:**
```python
result = await analyze_image(
    prompt="What objects are in this image?",
    image_base64="base64_encoded_image_data",
    mime_type="image/jpeg"
)
```

#### `analyze_video`
Analyze video content including frames, audio, and transcription.

**Parameters:**
- `prompt` (string, required): Question about the video
- `video_base64` (string, required): Base64 encoded video
- `mime_type` (string, optional): Video MIME type (default: 'video/mp4')
- `model` (string, optional): Model name (use gemini-1.5-pro-latest)

**Example:**
```python
result = await analyze_video(
    prompt="Summarize the key events in this video",
    video_base64="base64_encoded_video_data",
    model="gemini-1.5-pro-latest"
)
```

#### `analyze_pdf`
Extract and analyze PDF documents.

**Parameters:**
- `prompt` (string, required): Question about the PDF
- `pdf_base64` (string, required): Base64 encoded PDF
- `model` (string, optional): Model name

**Example:**
```python
result = await analyze_pdf(
    prompt="Extract all financial data from this document",
    pdf_base64="base64_encoded_pdf_data"
)
```

### Utility Tools

#### `count_tokens`
Estimate token usage before generation.

**Parameters:**
- `text` (string, required): Input text
- `model` (string, optional): Model name

**Example:**
```python
result = await count_tokens(
    text="Long document text here...",
    model="gemini-1.5-flash-latest"
)
# Returns: {'totalTokens': 1234}
```

#### `list_models`
List available Gemini models.

**Example:**
```python
models = await list_models()
```

### Advanced Features

#### `generate_with_tools`
Function calling and tool use.

**Parameters:**
- `prompt` (string, required): Input prompt
- `tools` (list, required): List of tool definitions
- `model` (string, optional): Model name

**Example:**
```python
tools = [{
    "function_declarations": [{
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }]
}]

result = await generate_with_tools(
    prompt="What's the weather in Paris?",
    tools=tools
)
```

#### `stream_generate`
Stream text generation responses.

**Parameters:**
- `prompt` (string, required): Input prompt
- `model` (string, optional): Model name
- `temperature` (float, optional): Sampling temperature

**Example:**
```python
result = await stream_generate(
    prompt="Write a long story about...",
    model="gemini-1.5-flash-latest"
)
```

#### `generate_json`
Generate structured JSON output.

**Parameters:**
- `prompt` (string, required): Input prompt
- `json_schema` (dict, required): JSON schema for response
- `model` (string, optional): Model name

**Example:**
```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
        "skills": {"type": "array", "items": {"type": "string"}}
    }
}

result = await generate_json(
    prompt="Extract person details: John is 30 and knows Python and SQL",
    json_schema=schema
)
```

#### `embed_text`
Generate text embeddings.

**Parameters:**
- `text` (string, required): Input text
- `model` (string, optional): Embedding model (default: 'text-embedding-004')
- `task_type` (string, optional): Task type

**Task types:**
- `RETRIEVAL_DOCUMENT` - For documents in retrieval
- `RETRIEVAL_QUERY` - For search queries
- `SEMANTIC_SIMILARITY` - For similarity comparison
- `CLASSIFICATION` - For classification tasks
- `CLUSTERING` - For clustering tasks

**Example:**
```python
result = await embed_text(
    text="This is a sample document",
    task_type="RETRIEVAL_DOCUMENT"
)
# Returns 768-dimensional vector
```

#### `batch_generate`
Generate multiple responses in parallel.

**Parameters:**
- `prompts` (list, required): List of prompts
- `model` (string, optional): Model name
- `temperature` (float, optional): Sampling temperature

**Example:**
```python
result = await batch_generate(
    prompts=[
        "Translate 'hello' to Spanish",
        "Translate 'goodbye' to French",
        "Translate 'thank you' to German"
    ]
)
```

## Context Windows

- **gemini-1.5-pro**: Up to 2 million tokens
- **gemini-1.5-flash**: Up to 1 million tokens
- **gemini-2.0-flash-exp**: Up to 1 million tokens

## Rate Limits

### Free Tier
- **15 requests per minute (RPM)**
- **1 million tokens per minute (TPM)**
- **1,500 requests per day (RPD)**

### Paid Tier (Pay-as-you-go)
- **360 RPM** (gemini-1.5-pro)
- **2000 RPM** (gemini-1.5-flash)
- **10 million TPM**

### Pricing (as of 2025)
- **gemini-1.5-pro**: $0.00125 per 1K characters input, $0.00375 per 1K characters output
- **gemini-1.5-flash**: $0.000125 per 1K characters input, $0.000375 per 1K characters output
- **text-embedding-004**: $0.00001 per 1K characters

Visit [ai.google.dev/pricing](https://ai.google.dev/pricing) for current rates.

## Safety Settings

Gemini includes built-in safety filters. You can configure safety settings:

```python
# Add to payload
"safetySettings": [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]
```

**Categories:**
- `HARM_CATEGORY_HARASSMENT`
- `HARM_CATEGORY_HATE_SPEECH`
- `HARM_CATEGORY_SEXUALLY_EXPLICIT`
- `HARM_CATEGORY_DANGEROUS_CONTENT`

**Thresholds:**
- `BLOCK_NONE` - No blocking
- `BLOCK_LOW_AND_ABOVE` - Block low and above
- `BLOCK_MEDIUM_AND_ABOVE` - Block medium and above (default)
- `BLOCK_ONLY_HIGH` - Block only high

## Best Practices

1. **Use appropriate models**: Flash for speed, Pro for quality
2. **Leverage long context**: Process entire documents
3. **Token counting**: Estimate costs with count_tokens
4. **System instructions**: Guide model behavior
5. **Streaming**: Use for long responses
6. **Function calling**: Enable tool use
7. **JSON mode**: Get structured outputs
8. **Batch processing**: Process multiple prompts efficiently

## Multimodal Capabilities

### Supported Formats

**Images:**
- JPEG, PNG, WebP, HEIC, HEIF
- Max size: 4MB per image
- Up to 16 images per request

**Videos:**
- MP4, MPEG, MOV, AVI, FLV, MPG, WebM
- Max duration: 2 hours
- Max size: 2GB

**Audio:**
- WAV, MP3, AIFF, AAC, OGG, FLAC
- Max duration: 9.5 hours

**PDFs:**
- Up to 3,000 pages
- Text and images extracted

## Error Handling

Common errors:

- **400 Bad Request**: Invalid parameters or content
- **403 Forbidden**: Invalid API key or insufficient permissions
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Gemini service issue

## Use Cases

- **Content Creation**: Blog posts, articles, creative writing
- **Code Generation**: Programming assistance and debugging
- **Document Analysis**: Extract insights from PDFs and documents
- **Visual Understanding**: Image and video analysis
- **Chatbots**: Conversational AI with context
- **Data Extraction**: Structured data from unstructured content
- **Embeddings**: Semantic search and similarity
- **Tool Integration**: Function calling for external APIs

## API Documentation

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Quickstart Guide](https://ai.google.dev/gemini-api/docs/quickstart)
- [Model Comparison](https://ai.google.dev/gemini-api/docs/models/gemini)
- [Safety Settings](https://ai.google.dev/gemini-api/docs/safety-settings)
- [Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)

## Support

- [Google AI Studio](https://aistudio.google.com/)
- [Issue Tracker](https://issuetracker.google.com/issues?q=componentid:1202013)
- [Community Forum](https://discuss.ai.google.dev/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-gemini-api)
