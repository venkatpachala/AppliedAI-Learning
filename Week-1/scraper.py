from bs4 import BeautifulSoup
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def fetch_website_contents(url, max_chars=2000):
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    # IMPORTANT: use decoded text, not raw bytes
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else "No title"

    if soup.body:
        for tag in soup.body(["script", "style", "img", "input", "noscript"]):
            tag.decompose()

        text = soup.body.get_text(separator=" ", strip=True)
    else:
        text = ""

    # 🔥 Gemini-critical sanitization
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x20-\x7E]", "", text)

    content = f"{title}\n\n{text}"
    return content[:max_chars]
