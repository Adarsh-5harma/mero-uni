import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.conf import settings


class AIServiceError(Exception):
    pass


def extract_resource_text(resource):
    extension = Path(resource.file.name).suffix.lower()
    if extension == '.pdf':
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise AIServiceError('PDF support is not installed on this server.') from exc
        reader = PdfReader(resource.file.path)
        text = '\n\n'.join(page.extract_text() or '' for page in reader.pages)
    elif extension == '.txt':
        with resource.file.open('rb') as source:
            text = source.read().decode('utf-8', errors='replace')
    else:
        raise AIServiceError('AI analysis currently supports PDF and TXT files only.')

    text = ' '.join(text.split())
    if not text:
        raise AIServiceError('No readable text was found in this document.')
    return text[:settings.AI_MAX_SOURCE_CHARS]


def generate_summary(text):
    if not settings.GEMINI_API_KEY:
        raise AIServiceError('Gemini is not configured. Add GEMINI_API_KEY to the environment.')
    model = quote(settings.GEMINI_MODEL, safe='')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
    prompt = ('Summarize this university learning material using clear headings, key concepts, '
              'definitions, and concise revision points. Do not invent facts.\n\n' + text)
    body = json.dumps({'contents': [{'parts': [{'text': prompt}]}]}).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': settings.GEMINI_API_KEY,
    }
    request = Request(url, data=body, headers=headers, method='POST')
    try:
        with urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode('utf-8'))
        return payload['candidates'][0]['content']['parts'][0]['text'].strip()
    except (HTTPError, URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
        raise AIServiceError('The AI provider could not generate a summary. Try again later.') from exc
