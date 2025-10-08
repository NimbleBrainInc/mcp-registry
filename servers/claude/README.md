# Anthropic Claude MCP Server

MCP server providing comprehensive access to Anthropic's Claude API.

## Features

### Core Capabilities
- **Messages API** - Full access to Claude 3.5 Sonnet, Haiku, and Claude 3 Opus
- **Simple Chat** - Easy-to-use chat interface
- **Vision** - Analyze images via URL or base64
- **Multi-turn Conversations** - Maintain conversation history
- **Token Counting** - Estimate token usage before making calls
- **Model Comparison** - Compare responses across different Claude models
- **Structured Extraction** - Extract structured data from unstructured text
- **Model Information** - Get details about Claude models and capabilities

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

## Configuration

### Get Your Anthropic API Key
1. Go to https://console.anthropic.com/settings/keys
2. Sign in or create an account
3. Click "Create Key"
4. Copy the key and add it to your `.env` file

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "claude": {
      "command": "fastmcp",
      "args": ["run", "server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### chat
Simple chat interface - send a prompt, get a response.

**Parameters:**
- `prompt` (required): Your message or question
- `model`: Claude model (default: "claude-3-5-sonnet-20241022")
- `max_tokens`: Maximum response length (default: 4096)
- `system`: Optional system prompt for context
- `temperature`: Creativity level 0-1

**Example:**
```json
{
  "prompt": "Explain quantum computing in simple terms",
  "max_tokens": 500
}
```

### create_message
Full Messages API with all parameters and features.

**Parameters:**
- `messages` (required): Conversation history
- `model`: Claude model
- `max_tokens` (required): Max response length
- `system`: System prompt
- `temperature`, `top_p`, `top_k`: Sampling parameters
- `stop_sequences`: Custom stop sequences

### analyze_image
Analyze images using Claude's vision capabilities.

**Parameters:**
- `image_url` (required): URL of image to analyze
- `prompt`: Question about the image (default: "What's in this image?")
- `model`: Vision-capable model
- `max_tokens`: Max response length

**Example:**
```json
{
  "image_url": "https://example.com/photo.jpg",
  "prompt": "Describe the architectural style of this building"
}
```

### analyze_image_base64
Analyze base64-encoded images.

**Parameters:**
- `image_base64` (required): Base64 image data
- `media_type` (required): image/jpeg, image/png, image/gif, or image/webp
- `prompt`: Question about the image
- `model`: Vision model
- `max_tokens`: Max response length

### multi_turn_conversation
Continue a conversation with context from previous messages.

**Parameters:**
- `conversation_history` (required): Previous messages
- `new_message` (required): New user message
- `model`: Claude model
- `max_tokens`: Max response length
- `system`: Optional system prompt

**Returns:** Response plus updated conversation history

**Example:**
```json
{
  "conversation_history": [
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."}
  ],
  "new_message": "What's the population?"
}
```

### count_tokens
Estimate token usage for messages.

**Parameters:**
- `messages` (required): Messages to count tokens for
- `model`: Model (affects tokenization)
- `system`: Optional system prompt

**Returns:** Input and output token counts

### get_model_info
Get information about Claude models.

**Parameters:**
- `model`: Model identifier (default: "claude-3-5-sonnet-20241022")

**Returns:** Context window, capabilities, tier, description

### compare_responses
Get responses from multiple models for comparison.

**Parameters:**
- `prompt` (required): Question or task
- `models`: List of models to compare (max 3, default: Sonnet and Haiku)
- `max_tokens`: Max tokens per response
- `system`: Optional system prompt

**Returns:** Responses from each model with usage stats

**Example:**
```json
{
  "prompt": "Write a haiku about programming",
  "models": ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"]
}
```

### extract_structured_data
Extract structured data from unstructured text.

**Parameters:**
- `text` (required): Unstructured text
- `schema_description` (required): Description of desired structure
- `model`: Claude model
- `max_tokens`: Max response length

**Example:**
```json
{
  "text": "Contact John Smith at john@example.com or call 555-1234",
  "schema_description": "Extract as JSON with fields: name, email, phone"
}
```

## Claude Models

### Claude 3.5 Family
- **claude-3-5-sonnet-20241022**: Most intelligent, best overall performance
- **claude-3-5-haiku-20241022**: Fastest model, cost-effective

### Claude 3 Family
- **claude-3-opus-20240229**: Top-tier performance for complex tasks
- **claude-3-sonnet-20240229**: Balanced intelligence and speed
- **claude-3-haiku-20240307**: Fast and economical

All models support:
- 200K context window
- Vision capabilities
- Tool use
- Multi-turn conversations

## Usage Examples

### Simple Question
```json
{
  "tool": "chat",
  "prompt": "What are the three laws of robotics?"
}
```

### Creative Writing with System Prompt
```json
{
  "tool": "chat",
  "prompt": "Write a short story about a time traveler",
  "system": "You are a creative writer specializing in science fiction",
  "temperature": 0.8,
  "max_tokens": 1000
}
```

### Image Analysis
```json
{
  "tool": "analyze_image",
  "image_url": "https://example.com/diagram.png",
  "prompt": "Explain what this technical diagram shows"
}
```

### Ongoing Conversation
```json
{
  "tool": "multi_turn_conversation",
  "conversation_history": [
    {"role": "user", "content": "I'm planning a trip to Japan"},
    {"role": "assistant", "content": "That sounds exciting! How long will you be staying?"}
  ],
  "new_message": "Two weeks in spring"
}
```

### Model Comparison
```json
{
  "tool": "compare_responses",
  "prompt": "Explain the theory of relativity",
  "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"]
}
```

### Data Extraction
```json
{
  "tool": "extract_structured_data",
  "text": "Apple Inc. reported revenue of $394.3B in fiscal 2024, up 2% YoY",
  "schema_description": "Extract as JSON: company, revenue, year, growth_rate"
}
```

## Error Handling

The server includes comprehensive error handling for:
- Invalid API keys
- Rate limiting (429 errors)
- Token limit exceeded (400 errors)
- Invalid model names
- Malformed requests
- Network timeouts

## Rate Limits

Anthropic enforces rate limits based on your account tier:
- Free tier: Limited requests per day
- Build tier: Higher daily limits
- Scale tier: Enterprise-level limits

Check your limits at: https://console.anthropic.com/settings/limits

## Pricing

Approximate costs per million tokens (input/output):
- **Claude 3.5 Sonnet**: $3 / $15
- **Claude 3.5 Haiku**: $0.80 / $4
- **Claude 3 Opus**: $15 / $75
- **Claude 3 Sonnet**: $3 / $15
- **Claude 3 Haiku**: $0.25 / $1.25

Current pricing: https://www.anthropic.com/pricing

## Best Practices

1. **Use System Prompts**: Set context and instructions for better responses
2. **Manage Context**: Keep conversation history relevant, trim old messages
3. **Choose the Right Model**: Haiku for speed, Sonnet for balance, Opus for complexity
4. **Token Management**: Use count_tokens to estimate costs before calls
5. **Error Handling**: Implement retry logic for rate limits
6. **Vision**: Images count toward token limits (analyze_image tools)

## Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor usage in Anthropic Console
- Set spending limits in your account

## Troubleshooting

### "Invalid API Key" Error
- Verify key is correct in `.env` file
- Check key is active at https://console.anthropic.com/settings/keys
- Ensure no extra spaces or quotes

### Rate Limit Errors (429)
- Implement exponential backoff
- Upgrade account tier if needed
- Monitor usage at console.anthropic.com

### Context Length Errors
- All Claude models support 200K tokens
- Count tokens before sending
- Trim old messages from conversation history

## Resources

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Messages API Reference](https://docs.anthropic.com/en/api/messages)
- [Claude Models](https://docs.anthropic.com/en/docs/about-claude/models)
- [Pricing](https://www.anthropic.com/pricing)
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT License - feel free to use in your projects!