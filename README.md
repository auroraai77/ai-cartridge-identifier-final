# 🖨️ AI Cartridge Identifier

A demo project that:
- Extracts text from cartridge images (OCR via Tesseract + Pillow).
- Uses OpenAI GPT to identify the most probable ink cartridge model.
- Provides candidates and confidence score.
- Built with **Streamlit**, dark theme UI.

## 🚀 Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-cartridge-identifier.git
cd ai-cartridge-identifier

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🔑 Set OpenAI Key
```bash
export OPENAI_API_KEY="your_api_key_here"
```

## ▶️ Run App
```bash
streamlit run src/ui/app.py
```

Then open browser at: http://localhost:8501
