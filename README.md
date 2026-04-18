# CodeNest — Offline AI Coding Assistant 🚀

> **100% Offline** · **Privacy-First** · **No Internet Required**

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-Phi3-orange?style=flat-square)

## 🎯 What is CodeNest?

**CodeNest** is your personal AI coding assistant that runs **completely offline** on your Windows PC. Upload code files, ask questions, run Python code, get instant help—all without internet or subscriptions.

**Perfect for:**
- Code explanation & debugging
- Writing algorithms
- Code reviews
- Learning new languages
- Job interview prep

## 📥 Quick Start (Windows Users - 5 minutes)

### Prerequisites (One-Time Setup)
1. Download & install [Python 3.11+](https://python.org/downloads) ✓ **Add to PATH**
2. Download & install [Ollama](https://ollama.com/download) ✓ **Windows installer**

### Download & Run
```
1. Download ZIP from GitHub Releases/Downloads
2. Extract to Desktop (e.g. Desktop/codenest)
3. Double-click start.bat
4. Wait for "✓ Model: phi3" (downloads 2.3GB first time)
5. Open browser: http://localhost:8000
```

**That's it!** Ready to chat with your AI coding assistant.

## 🎮 Features

| Feature | Description |
|---------|-------------|
| **Offline AI** | Phi-3 model (2.3GB) - works without internet |
| **File Upload** | Upload .py, .js, .java files for analysis |
| **Live Code Run** | Execute Python code in browser |
| **Streaming Chat** | Real-time responses like ChatGPT |
| **Model Switch** | phi3, qwen2.5-coder, codellama |
| **Syntax Highlight** | Beautiful code blocks + copy/run |

## 📱 Screenshot
*(Add screenshot of UI here)*
<img width="1918" height="935" alt="image" src="https://github.com/user-attachments/assets/feca67ae-e23a-4cf7-a456-310bc8414c56" />

## 🔧 Advanced Usage

### Custom Models
```bash
# Before running start.bat, set environment variable:
set CODENEST_MODEL=qwen2.5-coder
start.bat
```

### Docker (Any OS)
```bash
git clone https://github.com/yourusername/codenest
cd codenest
docker build -t codenest .
docker run -p 8000:8000 codenest
```

### Manual Start (Dev)
```cmd
cd codenest
call venv\Scripts\activate.bat
uvicorn app_fixed:app --host 0.0.0.0 --port 8000 --reload
```

## 💻 Hardware Requirements
- **Minimum**: 6GB RAM (phi3 model)
- **Recommended**: 8GB+ RAM, SSD
- **First run**: ~2.3GB download (offline after)

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ollama not found" | Reinstall Ollama from ollama.com |
| "Model not found" | First run downloads automatically |
| Port 8000 busy | Kill other servers or change port |
| Slow responses | Use phi3 model, close other apps |

## 📂 Folder Structure
```
codenest/
├── app_fixed.py      # Main FastAPI app (fixed)
├── templates/        # HTML UI
├── static/           # Assets  
├── start.bat         # 🖱️ Double-click to run
├── requirements.txt  # Dependencies
└── README.md
```

## 🚀 Share with Friends
1. Zip the **entire folder**
2. Send via USB/Dropbox
3. They just double-click `start.bat`

## 🤝 Contributing
1. Fork repo
2. `git clone + code`
3. `start.bat` for dev server
4. PR improvements!

## 📄 License
MIT — Free for personal/commercial use.

**Made with ❤️ for developers who value privacy**

---
*Your local AI coding copilot. No data leaves your machine.*
