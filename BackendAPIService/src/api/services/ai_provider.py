from typing import Optional

import httpx

from src.api.core.config import get_settings

settings = get_settings()


# PUBLIC_INTERFACE
async def generate_blog(topic: str, style: Optional[str] = None) -> dict:
    """Generate a blog post title and content using an OpenAI-compatible API.

    If AI_API_KEY is not set, returns a deterministic placeholder response.
    """
    if not settings.AI_API_KEY:
        title = f"AI Generated Blog on {topic}"
        content = f"# {title}\n\nThis is a placeholder generated article about {topic}.\n\nStyle: {style or 'default'}.\n\nContent goes here..."
        return {"title": title, "content": content}

    # OpenAI-compatible format
    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional blog writer."},
            {"role": "user", "content": f"Write a detailed blog post about: {topic}. Style: {style or 'default'}"},
        ],
        "temperature": 0.7,
    }

    # Common OpenAI base URL; allow environment to set proxy via OPENAI_BASE_URL if needed
    base_url = getattr(settings, "OPENAI_BASE_URL", None) or "https://api.openai.com/v1"
    url = f"{base_url}/chat/completions"

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        # Simple title extraction: first heading or first line up to 80 chars
        title = f"{topic} - An AI Perspective"
        return {"title": title, "content": text}
