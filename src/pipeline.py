import os
import openai
from PIL import Image

try:
    import pytesseract
except ImportError:
    pytesseract = None


def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image using Tesseract OCR"""
    if pytesseract is None:
        return "[Error] pytesseract is not installed. Please run: pip install pytesseract pillow"
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"[OCR Error] {str(e)}"


def process(input_text: str) -> dict:
    """Send text to OpenAI model and get cartridge classification"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "Missing OpenAI API key. Run: export OPENAI_API_KEY=your_key_here"}

    try:
        openai.api_key = api_key
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that identifies printer cartridge models."},
                {"role": "user", "content": input_text},
            ],
        )
        result = response.choices[0].message.content.strip()
        return {"model": result, "confidence": 0.9, "candidates": [result]}
    except Exception as e:
        return {"error": f"[OpenAI API Error] {str(e)}"}
