# Hugging Face MCP Server

MCP server for accessing the Hugging Face Inference API. Run 200,000+ machine learning models including LLMs, image generation, text classification, embeddings, and more.

## Features

- **Text Generation**: LLMs like Llama-3, Mistral, Gemma
- **Image Generation**: FLUX, Stable Diffusion XL, SD 2.1
- **Text Classification**: Sentiment analysis, topic classification
- **Token Classification**: Named entity recognition, POS tagging
- **Question Answering**: Extract answers from context
- **Summarization**: Condense long text
- **Translation**: 200+ language pairs
- **Image-to-Text**: Image captioning
- **Image Classification**: Classify images into categories
- **Object Detection**: Detect objects with bounding boxes
- **Text-to-Speech**: Convert text to audio
- **Speech Recognition**: Transcribe audio (Whisper)
- **Embeddings**: Get text/sentence embeddings
- **And more**: Fill-mask, sentence similarity

## Setup

### Prerequisites

- Hugging Face account
- API token (free or Pro)

### Environment Variables

- `HUGGINGFACE_API_TOKEN` (required): Your Hugging Face API token

**How to get an API token:**
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name and select permissions (read is sufficient for inference)
4. Copy the token (starts with `hf_`)
5. Store as `HUGGINGFACE_API_TOKEN`

## Available Tools

### Text Generation Tools

#### `text_generation`
Generate text using large language models.

**Parameters:**
- `prompt` (string, required): Input text prompt
- `model_id` (string, optional): Model ID (default: 'mistralai/Mistral-7B-Instruct-v0.3')
- `max_new_tokens` (int, optional): Maximum tokens to generate
- `temperature` (float, optional): Sampling temperature 0-2 (higher = more random)
- `top_p` (float, optional): Nucleus sampling 0-1
- `top_k` (int, optional): Top-k sampling
- `repetition_penalty` (float, optional): Penalty for repetition
- `return_full_text` (bool, optional): Return prompt + generation (default: False)

**Popular models:**
- `meta-llama/Llama-3.2-3B-Instruct` - Meta's Llama 3.2
- `mistralai/Mistral-7B-Instruct-v0.3` - Mistral 7B
- `google/gemma-2-2b-it` - Google Gemma 2
- `HuggingFaceH4/zephyr-7b-beta` - Zephyr 7B
- `tiiuae/falcon-7b-instruct` - Falcon 7B

**Example:**
```python
result = await text_generation(
    prompt="Write a Python function to calculate fibonacci numbers:",
    model_id="mistralai/Mistral-7B-Instruct-v0.3",
    max_new_tokens=200,
    temperature=0.7,
    top_p=0.9
)
```

### Classification Tools

#### `text_classification`
Classify text into categories (sentiment, topics, etc.).

**Parameters:**
- `text` (string, required): Text to classify
- `model_id` (string, optional): Model ID (default: 'distilbert-base-uncased-finetuned-sst-2-english')

**Popular models:**
- `distilbert-base-uncased-finetuned-sst-2-english` - Sentiment (positive/negative)
- `facebook/bart-large-mnli` - Zero-shot classification
- `cardiffnlp/twitter-roberta-base-sentiment-latest` - Twitter sentiment
- `finiteautomata/bertweet-base-sentiment-analysis` - Tweet sentiment

**Example:**
```python
result = await text_classification(
    text="I love this product! It exceeded my expectations.",
    model_id="distilbert-base-uncased-finetuned-sst-2-english"
)
# Returns: [{'label': 'POSITIVE', 'score': 0.9998}]
```

#### `token_classification`
Token-level classification for NER, POS tagging, etc.

**Parameters:**
- `text` (string, required): Input text
- `model_id` (string, optional): Model ID (default: 'dslim/bert-base-NER')

**Popular models:**
- `dslim/bert-base-NER` - Named Entity Recognition
- `Jean-Baptiste/roberta-large-ner-english` - Large NER model
- `dbmdz/bert-large-cased-finetuned-conll03-english` - CoNLL-2003 NER

**Example:**
```python
result = await token_classification(
    text="Apple Inc. is located in Cupertino, California.",
    model_id="dslim/bert-base-NER"
)
# Returns entities: ORG (Apple Inc.), LOC (Cupertino), LOC (California)
```

### Question Answering & Text Processing

#### `question_answering`
Answer questions based on provided context.

**Parameters:**
- `question` (string, required): Question to answer
- `context` (string, required): Context containing the answer
- `model_id` (string, optional): Model ID (default: 'deepset/roberta-base-squad2')

**Popular models:**
- `deepset/roberta-base-squad2` - RoBERTa on SQuAD 2.0
- `distilbert-base-cased-distilled-squad` - DistilBERT on SQuAD

**Example:**
```python
result = await question_answering(
    question="Where is the Eiffel Tower located?",
    context="The Eiffel Tower is a landmark in Paris, France. It was built in 1889.",
    model_id="deepset/roberta-base-squad2"
)
# Returns: {'answer': 'Paris, France', 'score': 0.98, 'start': 35, 'end': 48}
```

#### `summarization`
Summarize long text into shorter version.

**Parameters:**
- `text` (string, required): Text to summarize
- `model_id` (string, optional): Model ID (default: 'facebook/bart-large-cnn')
- `max_length` (int, optional): Maximum summary length
- `min_length` (int, optional): Minimum summary length

**Popular models:**
- `facebook/bart-large-cnn` - BART CNN summarization
- `google/pegasus-xsum` - PEGASUS XSum
- `sshleifer/distilbart-cnn-12-6` - Distilled BART

**Example:**
```python
result = await summarization(
    text="Long article text here...",
    model_id="facebook/bart-large-cnn",
    max_length=130,
    min_length=30
)
```

#### `translation`
Translate text between languages.

**Parameters:**
- `text` (string, required): Text to translate
- `model_id` (string, required): Model ID for language pair

**Popular models:**
- `Helsinki-NLP/opus-mt-en-es` - English to Spanish
- `Helsinki-NLP/opus-mt-es-en` - Spanish to English
- `Helsinki-NLP/opus-mt-en-fr` - English to French
- `Helsinki-NLP/opus-mt-en-de` - English to German
- `facebook/mbart-large-50-many-to-many-mmt` - Multilingual (50 languages)

**Example:**
```python
result = await translation(
    text="Hello, how are you?",
    model_id="Helsinki-NLP/opus-mt-en-es"
)
# Returns: "Hola, ¿cómo estás?"
```

### Image Generation Tools

#### `text_to_image`
Generate images from text prompts.

**Parameters:**
- `prompt` (string, required): Text description of desired image
- `model_id` (string, optional): Model ID (default: 'black-forest-labs/FLUX.1-dev')
- `negative_prompt` (string, optional): What to avoid in image
- `num_inference_steps` (int, optional): Number of denoising steps
- `guidance_scale` (float, optional): How closely to follow prompt

**Popular models:**
- `black-forest-labs/FLUX.1-dev` - FLUX.1 (high quality)
- `stabilityai/stable-diffusion-xl-base-1.0` - SDXL
- `stabilityai/stable-diffusion-2-1` - SD 2.1
- `runwayml/stable-diffusion-v1-5` - SD 1.5

**Example:**
```python
result = await text_to_image(
    prompt="A serene mountain landscape at sunset, photorealistic, 8k",
    model_id="black-forest-labs/FLUX.1-dev",
    negative_prompt="blurry, low quality, distorted",
    guidance_scale=7.5
)
# Returns: {'image': 'base64_encoded_image', 'format': 'base64'}
```

### Computer Vision Tools

#### `image_to_text`
Generate text descriptions from images (captioning).

**Parameters:**
- `image_base64` (string, required): Base64 encoded image
- `model_id` (string, optional): Model ID (default: 'Salesforce/blip-image-captioning-large')

**Popular models:**
- `Salesforce/blip-image-captioning-large` - BLIP large
- `nlpconnect/vit-gpt2-image-captioning` - ViT-GPT2

**Example:**
```python
result = await image_to_text(
    image_base64="base64_encoded_image_data",
    model_id="Salesforce/blip-image-captioning-large"
)
# Returns: [{'generated_text': 'a dog playing in the park'}]
```

#### `image_classification`
Classify images into categories.

**Parameters:**
- `image_base64` (string, required): Base64 encoded image
- `model_id` (string, optional): Model ID (default: 'google/vit-base-patch16-224')

**Popular models:**
- `google/vit-base-patch16-224` - Vision Transformer
- `microsoft/resnet-50` - ResNet-50

**Example:**
```python
result = await image_classification(
    image_base64="base64_encoded_image_data",
    model_id="google/vit-base-patch16-224"
)
# Returns: [{'label': 'golden retriever', 'score': 0.95}, ...]
```

#### `object_detection`
Detect objects in images with bounding boxes.

**Parameters:**
- `image_base64` (string, required): Base64 encoded image
- `model_id` (string, optional): Model ID (default: 'facebook/detr-resnet-50')

**Popular models:**
- `facebook/detr-resnet-50` - DETR with ResNet-50
- `hustvl/yolos-tiny` - YOLOS tiny

**Example:**
```python
result = await object_detection(
    image_base64="base64_encoded_image_data",
    model_id="facebook/detr-resnet-50"
)
# Returns: [{'label': 'dog', 'score': 0.98, 'box': {...}}, ...]
```

### Audio Tools

#### `text_to_speech`
Convert text to speech audio.

**Parameters:**
- `text` (string, required): Text to synthesize
- `model_id` (string, optional): Model ID (default: 'facebook/mms-tts-eng')

**Popular models:**
- `facebook/mms-tts-eng` - MMS TTS English
- `espnet/kan-bayashi_ljspeech_vits` - VITS LJSpeech

**Example:**
```python
result = await text_to_speech(
    text="Hello, this is a test of text to speech.",
    model_id="facebook/mms-tts-eng"
)
# Returns: {'audio': 'base64_encoded_audio', 'format': 'base64'}
```

#### `automatic_speech_recognition`
Transcribe audio to text (speech recognition).

**Parameters:**
- `audio_base64` (string, required): Base64 encoded audio
- `model_id` (string, optional): Model ID (default: 'openai/whisper-large-v3')

**Popular models:**
- `openai/whisper-large-v3` - Whisper large v3 (best quality)
- `openai/whisper-medium` - Whisper medium (faster)
- `facebook/wav2vec2-base-960h` - Wav2Vec 2.0

**Example:**
```python
result = await automatic_speech_recognition(
    audio_base64="base64_encoded_audio_data",
    model_id="openai/whisper-large-v3"
)
# Returns: {'text': 'transcribed audio text here'}
```

### Embedding & Similarity Tools

#### `sentence_similarity`
Compute similarity between sentences.

**Parameters:**
- `source_sentence` (string, required): Reference sentence
- `sentences` (list, required): List of sentences to compare
- `model_id` (string, optional): Model ID (default: 'sentence-transformers/all-MiniLM-L6-v2')

**Popular models:**
- `sentence-transformers/all-MiniLM-L6-v2` - Fast, good quality
- `sentence-transformers/all-mpnet-base-v2` - Best quality
- `BAAI/bge-small-en-v1.5` - BGE small

**Example:**
```python
result = await sentence_similarity(
    source_sentence="The cat sits on the mat",
    sentences=[
        "A cat is sitting on a mat",
        "The dog runs in the park",
        "Cats are great pets"
    ],
    model_id="sentence-transformers/all-MiniLM-L6-v2"
)
# Returns: [0.95, 0.23, 0.65]
```

#### `feature_extraction`
Get embeddings (feature vectors) for text.

**Parameters:**
- `text` (string, required): Input text
- `model_id` (string, optional): Model ID (default: 'sentence-transformers/all-MiniLM-L6-v2')

**Popular models:**
- `sentence-transformers/all-MiniLM-L6-v2` - 384 dimensions
- `sentence-transformers/all-mpnet-base-v2` - 768 dimensions
- `BAAI/bge-small-en-v1.5` - 384 dimensions

**Example:**
```python
result = await feature_extraction(
    text="This is a sample sentence.",
    model_id="sentence-transformers/all-MiniLM-L6-v2"
)
# Returns: [[0.012, -0.034, 0.056, ...]] (384-dimensional vector)
```

#### `fill_mask`
Fill in masked words in text.

**Parameters:**
- `text` (string, required): Text with [MASK] token
- `model_id` (string, optional): Model ID (default: 'bert-base-uncased')

**Popular models:**
- `bert-base-uncased` - BERT base
- `roberta-base` - RoBERTa base
- `distilbert-base-uncased` - DistilBERT

**Example:**
```python
result = await fill_mask(
    text="Paris is the [MASK] of France.",
    model_id="bert-base-uncased"
)
# Returns: [{'token_str': 'capital', 'score': 0.95}, ...]
```

## Model Loading & Cold Starts

**Important**: Models may take 20-60 seconds to load on first request (cold start). Subsequent requests are faster.

**Tips:**
- Use popular models for faster loading
- Implement retry logic for timeouts
- Consider caching model responses
- Use smaller models for faster inference

## Rate Limits

### Free Tier
- Rate limited to prevent abuse
- Suitable for testing and small projects
- May experience queuing during high load

### Pro Subscription ($9/month)
- No rate limits
- Priority access to models
- Faster inference
- No queuing

Visit [huggingface.co/pricing](https://huggingface.co/pricing) for details.

## Base64 Encoding

For images and audio, you need to provide base64 encoded data:

**Python example:**
```python
import base64

# Encode image
with open("image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# Encode audio
with open("audio.wav", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Decode image response
image_bytes = base64.b64decode(response['image'])
with open("generated.jpg", "wb") as f:
    f.write(image_bytes)
```

## Parameter Tuning

### Text Generation
- **temperature** (0-2): Higher = more creative/random, Lower = more focused/deterministic
- **top_p** (0-1): Nucleus sampling, typically 0.9-0.95
- **top_k**: Number of highest probability tokens to keep
- **repetition_penalty**: Penalize repeated tokens (>1.0 reduces repetition)

### Image Generation
- **guidance_scale** (1-20): Higher = follows prompt more strictly (typical: 7-7.5)
- **num_inference_steps**: More steps = higher quality but slower (typical: 20-50)
- **negative_prompt**: Describe what you don't want in the image

## Error Handling

Common errors:

- **503 Service Unavailable**: Model is loading (cold start), retry after 20-60 seconds
- **401 Unauthorized**: Invalid or missing API token
- **429 Too Many Requests**: Rate limit exceeded (upgrade to Pro)
- **400 Bad Request**: Invalid parameters or model ID
- **504 Gateway Timeout**: Model took too long to respond

**Retry logic example:**
```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        result = await text_generation(prompt="Hello")
        break
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 503 and attempt < max_retries - 1:
            time.sleep(20)  # Wait for model to load
            continue
        raise
```

## Finding Models

**Browse models:**
- Visit [huggingface.co/models](https://huggingface.co/models)
- Filter by task (Text Generation, Image Generation, etc.)
- Sort by downloads, likes, or trending
- Check model card for usage examples

**Popular categories:**
- Text Generation: 50,000+ models
- Text Classification: 30,000+ models
- Image Generation: 10,000+ models
- Translation: 5,000+ models
- Embeddings: 3,000+ models

## Best Practices

1. **Use popular models**: Faster loading and better maintained
2. **Implement timeouts**: Set appropriate timeouts (60-120 seconds)
3. **Cache responses**: Store results to reduce API calls
4. **Handle cold starts**: Implement retry logic for 503 errors
5. **Monitor usage**: Track API calls and costs
6. **Test locally**: Use Hugging Face Transformers library for testing
7. **Read model cards**: Understand model capabilities and limitations
8. **Optimize parameters**: Tune settings for your use case

## Use Cases

- **Chatbots**: LLM-powered conversational AI
- **Content Generation**: Blog posts, articles, creative writing
- **Image Creation**: Art, illustrations, product images
- **Sentiment Analysis**: Customer feedback analysis
- **Translation**: Multi-language support
- **Transcription**: Meeting notes, podcast transcripts
- **Semantic Search**: Embedding-based search
- **Data Extraction**: NER for document processing
- **Content Moderation**: Text and image classification

## API Documentation

- [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index)
- [Supported Tasks](https://huggingface.co/docs/api-inference/supported-tasks)
- [Model Hub](https://huggingface.co/models)
- [Pricing](https://huggingface.co/pricing)

## Support

- [Hugging Face Forums](https://discuss.huggingface.co/)
- [Discord Community](https://huggingface.co/join/discord)
- [Documentation](https://huggingface.co/docs)
- [Status Page](https://status.huggingface.co/)
