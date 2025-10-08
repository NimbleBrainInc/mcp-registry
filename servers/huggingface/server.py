"""
Hugging Face MCP Server
Provides tools for accessing Hugging Face Inference API for ML models.
"""

import os
from typing import Optional, Dict, Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Hugging Face MCP Server")

# Get API token from environment
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
BASE_URL = "https://api-inference.huggingface.co"


def get_headers() -> dict:
    """Get headers for Hugging Face API requests."""
    if not HUGGINGFACE_API_TOKEN:
        raise ValueError("HUGGINGFACE_API_TOKEN environment variable is required")
    return {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json",
    }


@mcp.tool()
async def text_generation(
    prompt: str,
    model_id: str = "mistralai/Mistral-7B-Instruct-v0.3",
    max_new_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    repetition_penalty: Optional[float] = None,
    return_full_text: bool = False
) -> dict:
    """
    Generate text using large language models.

    Args:
        prompt: Input text prompt
        model_id: Model ID (default: 'mistralai/Mistral-7B-Instruct-v0.3')
        max_new_tokens: Maximum tokens to generate (optional)
        temperature: Sampling temperature 0-2 (higher = more random, optional)
        top_p: Nucleus sampling parameter 0-1 (optional)
        top_k: Top-k sampling parameter (optional)
        repetition_penalty: Penalty for repetition (optional)
        return_full_text: Return full text including prompt (default: False)

    Returns:
        Dictionary with generated text

    Popular models: meta-llama/Llama-3.2-3B-Instruct, mistralai/Mistral-7B-Instruct-v0.3, google/gemma-2-2b-it
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {"inputs": prompt}
        parameters = {}

        if max_new_tokens is not None:
            parameters["max_new_tokens"] = max_new_tokens
        if temperature is not None:
            parameters["temperature"] = temperature
        if top_p is not None:
            parameters["top_p"] = top_p
        if top_k is not None:
            parameters["top_k"] = top_k
        if repetition_penalty is not None:
            parameters["repetition_penalty"] = repetition_penalty
        if not return_full_text:
            parameters["return_full_text"] = False

        if parameters:
            payload["parameters"] = parameters

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def text_classification(
    text: str,
    model_id: str = "distilbert-base-uncased-finetuned-sst-2-english"
) -> dict:
    """
    Classify text into categories (sentiment, topic, etc.).

    Args:
        text: Input text to classify
        model_id: Model ID (default: 'distilbert-base-uncased-finetuned-sst-2-english')

    Returns:
        Dictionary with classification labels and scores

    Popular models: distilbert-base-uncased-finetuned-sst-2-english (sentiment), facebook/bart-large-mnli (zero-shot)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"inputs": text}

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def token_classification(
    text: str,
    model_id: str = "dslim/bert-base-NER"
) -> dict:
    """
    Token classification for named entity recognition, POS tagging, etc.

    Args:
        text: Input text
        model_id: Model ID (default: 'dslim/bert-base-NER')

    Returns:
        Dictionary with token entities and labels

    Popular models: dslim/bert-base-NER, Jean-Baptiste/roberta-large-ner-english
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"inputs": text}

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def question_answering(
    question: str,
    context: str,
    model_id: str = "deepset/roberta-base-squad2"
) -> dict:
    """
    Answer questions based on provided context.

    Args:
        question: Question to answer
        context: Context containing the answer
        model_id: Model ID (default: 'deepset/roberta-base-squad2')

    Returns:
        Dictionary with answer, score, start/end positions

    Popular models: deepset/roberta-base-squad2, distilbert-base-cased-distilled-squad
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "inputs": {
                "question": question,
                "context": context
            }
        }

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def summarization(
    text: str,
    model_id: str = "facebook/bart-large-cnn",
    max_length: Optional[int] = None,
    min_length: Optional[int] = None
) -> dict:
    """
    Summarize long text into shorter version.

    Args:
        text: Input text to summarize
        model_id: Model ID (default: 'facebook/bart-large-cnn')
        max_length: Maximum summary length (optional)
        min_length: Minimum summary length (optional)

    Returns:
        Dictionary with summary text

    Popular models: facebook/bart-large-cnn, google/pegasus-xsum, sshleifer/distilbart-cnn-12-6
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"inputs": text}
        parameters = {}

        if max_length is not None:
            parameters["max_length"] = max_length
        if min_length is not None:
            parameters["min_length"] = min_length

        if parameters:
            payload["parameters"] = parameters

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def translation(
    text: str,
    model_id: str = "Helsinki-NLP/opus-mt-en-es"
) -> dict:
    """
    Translate text between languages.

    Args:
        text: Input text to translate
        model_id: Model ID (default: 'Helsinki-NLP/opus-mt-en-es' for English to Spanish)

    Returns:
        Dictionary with translated text

    Popular models: Helsinki-NLP/opus-mt-en-es (en->es), Helsinki-NLP/opus-mt-es-en (es->en),
    Helsinki-NLP/opus-mt-en-fr (en->fr), facebook/mbart-large-50-many-to-many-mmt (multilingual)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"inputs": text}

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def text_to_image(
    prompt: str,
    model_id: str = "black-forest-labs/FLUX.1-dev",
    negative_prompt: Optional[str] = None,
    num_inference_steps: Optional[int] = None,
    guidance_scale: Optional[float] = None
) -> dict:
    """
    Generate images from text prompts.

    Args:
        prompt: Text description of desired image
        model_id: Model ID (default: 'black-forest-labs/FLUX.1-dev')
        negative_prompt: What to avoid in image (optional)
        num_inference_steps: Number of denoising steps (optional, default varies by model)
        guidance_scale: How closely to follow prompt (optional, default varies by model)

    Returns:
        Dictionary with base64 encoded image

    Popular models: black-forest-labs/FLUX.1-dev, stabilityai/stable-diffusion-xl-base-1.0,
    stabilityai/stable-diffusion-2-1, runwayml/stable-diffusion-v1-5
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {"inputs": prompt}
        parameters = {}

        if negative_prompt is not None:
            parameters["negative_prompt"] = negative_prompt
        if num_inference_steps is not None:
            parameters["num_inference_steps"] = num_inference_steps
        if guidance_scale is not None:
            parameters["guidance_scale"] = guidance_scale

        if parameters:
            payload["parameters"] = parameters

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()

        # Image is returned as bytes
        import base64
        image_bytes = response.content
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        return {
            "image": image_base64,
            "format": "base64",
            "content_type": response.headers.get("content-type", "image/jpeg")
        }


@mcp.tool()
async def image_to_text(
    image_base64: str,
    model_id: str = "Salesforce/blip-image-captioning-large"
) -> dict:
    """
    Generate text descriptions from images (image captioning).

    Args:
        image_base64: Base64 encoded image
        model_id: Model ID (default: 'Salesforce/blip-image-captioning-large')

    Returns:
        Dictionary with generated caption

    Popular models: Salesforce/blip-image-captioning-large, nlpconnect/vit-gpt2-image-captioning
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        import base64
        image_bytes = base64.b64decode(image_base64)

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"},
            content=image_bytes,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def image_classification(
    image_base64: str,
    model_id: str = "google/vit-base-patch16-224"
) -> dict:
    """
    Classify images into categories.

    Args:
        image_base64: Base64 encoded image
        model_id: Model ID (default: 'google/vit-base-patch16-224')

    Returns:
        Dictionary with classification labels and scores

    Popular models: google/vit-base-patch16-224, microsoft/resnet-50
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        import base64
        image_bytes = base64.b64decode(image_base64)

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"},
            content=image_bytes,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def object_detection(
    image_base64: str,
    model_id: str = "facebook/detr-resnet-50"
) -> dict:
    """
    Detect objects in images with bounding boxes.

    Args:
        image_base64: Base64 encoded image
        model_id: Model ID (default: 'facebook/detr-resnet-50')

    Returns:
        Dictionary with detected objects, labels, scores, and bounding boxes

    Popular models: facebook/detr-resnet-50, hustvl/yolos-tiny
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        import base64
        image_bytes = base64.b64decode(image_base64)

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"},
            content=image_bytes,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def text_to_speech(
    text: str,
    model_id: str = "facebook/mms-tts-eng"
) -> dict:
    """
    Convert text to speech audio.

    Args:
        text: Input text to synthesize
        model_id: Model ID (default: 'facebook/mms-tts-eng')

    Returns:
        Dictionary with base64 encoded audio

    Popular models: facebook/mms-tts-eng, espnet/kan-bayashi_ljspeech_vits
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"inputs": text}

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()

        # Audio is returned as bytes
        import base64
        audio_bytes = response.content
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

        return {
            "audio": audio_base64,
            "format": "base64",
            "content_type": response.headers.get("content-type", "audio/flac")
        }


@mcp.tool()
async def automatic_speech_recognition(
    audio_base64: str,
    model_id: str = "openai/whisper-large-v3"
) -> dict:
    """
    Transcribe audio to text (speech recognition).

    Args:
        audio_base64: Base64 encoded audio file
        model_id: Model ID (default: 'openai/whisper-large-v3')

    Returns:
        Dictionary with transcribed text

    Popular models: openai/whisper-large-v3, openai/whisper-medium, facebook/wav2vec2-base-960h
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        import base64
        audio_bytes = base64.b64decode(audio_base64)

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"},
            content=audio_bytes,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def sentence_similarity(
    source_sentence: str,
    sentences: list[str],
    model_id: str = "sentence-transformers/all-MiniLM-L6-v2"
) -> dict:
    """
    Compute similarity between sentences using embeddings.

    Args:
        source_sentence: Reference sentence
        sentences: List of sentences to compare
        model_id: Model ID (default: 'sentence-transformers/all-MiniLM-L6-v2')

    Returns:
        Dictionary with similarity scores

    Popular models: sentence-transformers/all-MiniLM-L6-v2, sentence-transformers/all-mpnet-base-v2
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "inputs": {
                "source_sentence": source_sentence,
                "sentences": sentences
            }
        }

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def fill_mask(
    text: str,
    model_id: str = "bert-base-uncased"
) -> dict:
    """
    Fill in masked words in text (use [MASK] token).

    Args:
        text: Input text with [MASK] token
        model_id: Model ID (default: 'bert-base-uncased')

    Returns:
        Dictionary with predicted tokens and scores

    Popular models: bert-base-uncased, roberta-base, distilbert-base-uncased

    Example: "Paris is the [MASK] of France."
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"inputs": text}

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def feature_extraction(
    text: str,
    model_id: str = "sentence-transformers/all-MiniLM-L6-v2"
) -> dict:
    """
    Get embeddings (feature vectors) for text.

    Args:
        text: Input text
        model_id: Model ID (default: 'sentence-transformers/all-MiniLM-L6-v2')

    Returns:
        Dictionary with embedding vectors

    Popular models: sentence-transformers/all-MiniLM-L6-v2, sentence-transformers/all-mpnet-base-v2,
    BAAI/bge-small-en-v1.5
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"inputs": text}

        response = await client.post(
            f"{BASE_URL}/models/{model_id}",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
