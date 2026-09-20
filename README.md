---
title: Chatterbox Voice
emoji: 🎙️
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: "6.28.0"
python_version: "3.12"
app_file: app.py
pinned: false
---

# 🎙️ Chatterbox AI Voice Generator & Voice Cloner

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6-EE4C2C.svg)](https://pytorch.org/)
[![Gradio](https://img.shields.io/badge/Web%20UI-Gradio-orange.svg)](https://gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Zero-shot AI voice cloning and speech synthesis made dead simple.** Generate realistic speech from text, clone any voice from a short audio clip, and run batch synthesis with a single click.

---

## ✨ Features

- **🎯 1-Click Launchers**: Double-click `run.bat` on Windows or execute `./run.sh` on Mac/Linux — zero manual configuration required.
- **🎨 Modern Web Interface**: Powered by Gradio with live waveform playback, direct file downloads, and emotion/tuning sliders.
- **🧬 Zero-Shot Voice Cloning**: Upload any 5+ second audio file (`.wav` or `.mp3`) to instantly clone that voice.
- **⚡ Fast Inference**: Powered by Resemble AI's `chatterbox-turbo` MeanFlow model with automatic GPU (CUDA) acceleration and CPU fallback.
- **📦 Multi-Output Batch Mode**: Synthesize entire lists of sentences or generate multiple variations/takes with one click.
- **💻 CLI & Scripting Support**: Full command-line options for automated pipelines and custom integrations.

---

## 🚀 1-Minute Quickstart

### Option A: Windows (1-Click)
Simply **double-click** on:
```text
run.bat
```
The script will automatically detect Python, set up the environment, install requirements, and open the Web UI in your browser at `http://127.0.0.1:7860`.

---

### Option B: macOS / Linux (1-Click)
Make executable and run:
```bash
chmod +x run.sh
./run.sh
```

---

### Option C: Manual Setup (Any OS)
1. **Clone the repository:**
   ```bash
   git clone https://github.com/SujalJaveri/chatterbox.git
   cd chatterbox
   ```

2. **Create a Python 3.11 virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Web UI:**
   ```bash
   python app.py
   ```
   Open your browser at `http://127.0.0.1:7860`.

---

## 💻 Command Line (CLI) Usage

You can also run speech synthesis directly from the terminal without launching the Web UI:

### 1. Simple Generation
```bash
python voice.py --text "Hello world, this is Chatterbox!" --output hello.wav
```

### 2. Custom Voice Cloning
```bash
python voice.py --text "Cloning this speaker voice." --voice my_voice.wav --output clone.wav
```

### 3. Generate Multiple Takes / Variations
Generate 3 variations to pick the best-sounding one:
```bash
python voice.py --text "Testing multiple variations" --takes 3
```
*(Outputs saved to `outputs/`)*

### 4. Batch Generation from a File
Synthesize multiple lines from a text file:
```bash
python voice.py --batch-file sample_prompts.txt
```

---

## 🎛️ Tuning Parameters

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `--temperature` | `0.8` | Creativity & variance (0.1 to 1.2). Lower is calmer; higher is more expressive. |
| `--exaggeration` | `0.0` | Emotion exaggeration (0.0 to 1.0). Adds expressive emotional variance. |
| `--device` | `auto` | Choose `cuda` for NVIDIA GPU or `cpu`. |

---

## 📂 Project Structure

```text
chatterbox/
├── app.py                 # Gradio Web UI (Browser interface)
├── voice.py               # CLI & programmatic generation script
├── download_models.py     # Automated model checkpoint downloader & verifier
├── run.bat                # 1-Click launcher for Windows
├── run.sh                 # 1-Click launcher for macOS/Linux
├── requirements.txt       # Project dependencies
├── sample_prompts.txt     # Sample prompts for batch testing
├── voice.wav              # Default reference voice sample
└── README.md              # Documentation
```

---

## 📄 License
This project is licensed under the MIT License.
