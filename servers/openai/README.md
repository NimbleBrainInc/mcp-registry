# OpenAI MCP Server

MCP server providing comprehensive access to OpenAI's API capabilities.

## Features

### Core Capabilities
- **Chat Completions** - Generate responses using GPT-4o, GPT-4, and GPT-3.5 models
- **Embeddings** - Create vector embeddings for semantic search and similarity
- **Image Generation** - Generate images with DALL-E 3 and DALL-E 2
- **Text-to-Speech** - Convert text to natural-sounding speech
- **Speech-to-Text** - Transcribe audio using Whisper
- **Vision Analysis** - Analyze images with GPT-4 Vision
- **Content Moderation** - Check content against usage policies
- **Model Management** - List and explore available models

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Configuration

### Get Your OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and add it to your `.env` file

## Running the Server

### HTTP Mode (Recommended for NimbleBrain)

Start the server:
```bash
# Set your API key
export OPENAI_API_KEY=your_api_key_here

# Run the server (default port 8000)
fastmcp run openai_server.py

# Or specify a custom port
fastmcp run openai_server.py --port 8080
```

The server will be available at `http://localhost:8000`

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

**HTTP Configuration:**
```json
{
  "mcpServers": {
    "openai": {
      "url": "http://localhost:8000"
    }
  }
}
```

**Alternative - Direct Python (stdio):**

If you need stdio mode instead of HTTP, you can run directly:

**Windows** (`%APPDATA%\Claude\claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "openai": {
      "command": "python",
      "args": ["-m", "fastmcp", "run", "openai_server.py"],
      "env": {
        "OPENAI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**macOS** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "openai": {
      "command": "python3",
      "args": ["-m", "fastmcp", "run", "openai_server.py"],
      "env": {
        "OPENAI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### chat_completion
Generate conversational responses using OpenAI's chat models.

**Parameters:**
- `messages` (required): List of message objects with 'role' and 'content'
- `model`: Model name (default: "gpt-4o-mini")
- `temperature`: Creativity level 0-2 (default: 1.0)
- `max_tokens`: Maximum response length
- `response_format`: Optional "json_object" for JSON responses

**Example:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain quantum computing in simple terms."}
]
```

### create_embedding
Generate vector embeddings for text.

**Parameters:**
- `text` (required): Text to embed
- `model`: Embedding model (default: "text-embedding-3-small")

**Use Cases:**
- Semantic search
- Document similarity
- Clustering and classification
- Recommendation systems

### generate_image
Create images from text descriptions using DALL-E.

**Parameters:**
- `prompt` (required): Description of desired image
- `model`: "dall-e-3" or "dall-e-2" (default: "dall-e-3")
- `size`: Image dimensions (1024x1024, 1792x1024, 1024x1792)
- `quality`: "standard" or "hd" (DALL-E 3 only)
- `n`: Number of images (1-10, only 1 for DALL-E 3)

### text_to_speech
Convert text to natural-sounding audio.

**Parameters:**
- `text` (required): Text to convert
- `voice`: alloy, echo, fable, onyx, nova, shimmer (default: "alloy")
- `model`: "tts-1" or "tts-1-hd" (default: "tts-1")
- `speed`: Speech rate 0.25-4.0 (default: 1.0)

**Returns:** Base64 encoded MP3 audio

### transcribe_audio
Transcribe audio to text using Whisper.

**Parameters:**
- `audio_file_base64` (required): Base64 encoded audio file
- `model`: "whisper-1"
- `language`: Optional language code (auto-detected if not provided)
- `response_format`: json, text, srt, vtt, verbose_json

### analyze_image
Analyze images using GPT-4 Vision.

**Parameters:**
- `image_url` (required): URL of image to analyze
- `prompt`: Question about the image (default: "What's in this image?")
- `model`: Vision model (default: "gpt-4o-mini")
- `max_tokens`: Maximum response length

### moderate_content
Check if content violates OpenAI's usage policies.

**Parameters:**
- `text` (required): Content to moderate
- `model`: "text-moderation-latest" or "text-moderation-stable"

**Returns:** Flags and scores for various content categories

### list_models
Get all available OpenAI models with metadata.

## Usage Examples

### Chat Conversation
```json
{
  "messages": [
    {"role": "system", "content": "You are a creative writing assistant."},
    {"role": "user", "content": "Write a haiku about programming."}
  ],
  "model": "gpt-4o",
  "temperature": 0.8
}
```

### Generate Marketing Image
```json
{
  "prompt": "A modern minimalist logo for a tech startup, blue and white color scheme, professional",
  "model": "dall-e-3",
  "size": "1024x1024",
  "quality": "hd"
}
```

### Create Product Description Embeddings
```json
{
  "text": "Wireless Bluetooth headphones with active noise cancellation and 30-hour battery life",
  "model": "text-embedding-3-small"
}
```

### Transcribe Meeting Recording
```json
{
  "audio_file_base64": "<base64_encoded_audio>",
  "language": "en",
  "response_format": "verbose_json"
}
```

## Model Recommendations

### Chat Models
- **gpt-4o**: Best overall, multimodal, fast
- **gpt-4o-mini**: Cost-effective, very fast
- **gpt-4-turbo**: High intelligence, good for complex tasks
- **gpt-3.5-turbo**: Fast and affordable for simple tasks

### Embedding Models
- **text-embedding-3-small**: Best price/performance (1536 dimensions)
- **text-embedding-3-large**: Highest quality (3072 dimensions)

### Image Models
- **dall-e-3**: Higher quality, better prompt following
- **dall-e-2**: More images per request, lower cost

## Error Handling

The server includes comprehensive error handling for:
- Invalid API keys
- Rate limiting
- Invalid model names
- Malformed requests
- Network timeouts

## Rate Limits

OpenAI enforces rate limits based on your account tier:
- Free tier: Limited requests per minute
- Pay-as-you-go: Higher limits based on usage
- Enterprise: Custom limits

Check your limits at: https://platform.openai.com/account/limits

## Pricing

Approximate costs (check OpenAI pricing page for current rates):
- **GPT-4o**: ~$2.50 per 1M input tokens
- **GPT-4o-mini**: ~$0.15 per 1M input tokens
- **Text Embeddings**: ~$0.02 per 1M tokens
- **DALL-E 3**: ~$0.04 per standard image
- **Whisper**: ~$0.006 per minute

## Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor usage on OpenAI dashboard
- Set spending limits in your OpenAI account

## Troubleshooting

### "Invalid API Key" Error
- Verify key is correct in `.env` file
- Ensure no extra spaces or quotes
- Check key is active at https://platform.openai.com/api-keys

### Rate Limit Errors
- Implement exponential backoff
- Upgrade account tier if needed
- Reduce request frequency

### Timeout Errors
- Increase timeout in httpx client
- Check network connectivity
- Try with smaller requests

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Pricing](https://openai.com/pricing)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT License - feel free to use in your projects!