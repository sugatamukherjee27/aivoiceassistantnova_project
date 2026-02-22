## Nova Pro AI Assistant

**Nova Pro AI** is a lightweight, Python-based virtual assistant that combines speech recognition, neural text generation, and web-scraping to provide real-time information, news briefings, and system automation.

---

### 🚀 Features

* **Neural Engine**: Uses GPT-2 via the `transformers` library for local text generation and analysis.
* **Voice Interface**: Integrates `speech_recognition` for input and `gTTS` (Google Text-to-Speech) for spoken responses.
* **Intelligent News**: Fetches the latest headlines via `feedparser` and provides AI-generated analysis of significance.
* **Web Integration**: Performs live web searches using DuckDuckGo (`DDGS`) and plays media on YouTube via `pywhatkit`.
* **Wake Word Detection**: Remains in a low-power "standby" mode until it hears "Nova," "Hey Nova," or "Hello Nova."

---

### 🛠️ Installation

1. **Clone the Repository**:
```bash
git clone https://github.com/sugatamukherjee27/aivoiceassistantnova_project.git
cd aivoiceassistantnova_project

```


2. **Set Up a Virtual Environment**:
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate

```


3. **Install Dependencies**:
```bash
pip install -r requirements.txt

```


4. **System Requirements**:
* **Microphone**: Required for voice commands.
* **Internet Connection**: Required for News, YouTube, and Google Speech Recognition APIs.
* **Audio Drivers**: Ensure `pygame` can access your system's audio output.



---

### 🖥️ Usage

Run the assistant from your terminal:

```bash
python voice.py

```

**Commands to try:**

* *"Nova, what time is it?"*
* *"Nova, give me a detailed briefing."* (Fetches news + AI analysis)
* *"Nova, play Lo-fi beats on YouTube."*
* *"Nova, how do black holes work?"* (Triggers AI search & answer)
* *"Nova, stop."* (Exits the program)

---

### 📂 Project Structure

* `voice.py`: The main application script containing the AI logic and command loop.
* `requirements.txt`: List of necessary Python libraries.
* `.gitignore`: Configured to ignore `venv/` and `.vscode/` settings.
* `README.md`: Project documentation.

---

### 📝 Note on AI Performance

The first time you run the script, it will download the **GPT-2 model weights** (approx. 500MB). Subsequent launches will be significantly faster as the model is cached locally.

Would you like me to add a section to this README on how to swap the GPT-2 model for a more advanced one like Mistral or Llama?
