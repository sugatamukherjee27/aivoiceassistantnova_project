
# Nova Pro AI Assistant

**Nova Pro AI** is a highly optimized, modern Python-based virtual assistant. Shifting from localized text generation to an advanced Cloud-based RAG architecture, it leverages deep-learning audio models alongside real-time dynamic web verification pipelines to serve as a fast, low-latency contextual operations layer.

---

### 🚀 Features

* **Cognitive Inference Engine**: Powered by the **Llama 3.1 8B** model hosted via Groq Cloud API for immediate, high-fidelity conversational text processing.
* **Local Neural Transcription**: Utilizes OpenAI's local **Whisper (Base)** model via `torch` for exceptionally accurate Speech-to-Text parsing.
* **Dynamic RAG Ingestion**: Automatically intercepts real-time/time-sensitive requests (e.g., live events, news) and pairs them with automated, live Google News XML RSS queries before processing to eliminate knowledge cutoffs.
* **Native Audio Pipelines**: Leverages a reliable multi-layered response matrix utilizing streaming network TTS with an automated offline fallback engine via `pyttsx3`.
* **Flexible Hardware Handshakes**: Intelligently captures microphone streams via local system terminal hooks (`ffmpeg`) across Windows, macOS, and Linux, with an automatic keyboard input fallback when hardware arrays are unavailable.

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

4. **Environment Configuration**:
Nova Pro requires an API token to communicate with the Groq inference engine. Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_actual_groq_api_token_here

```

5. **External System Infrastructure**:

* **FFmpeg**: The pipeline relies on `ffmpeg` and `ffplay` binaries explicitly mapped into your system's global environment `PATH` variables to enable audio capture and native stream playback.
* **Microphone Input Array**: Required for voice activation loops.

---

### 🖥️ Usage

Execute the system backbone directly from your terminal:

```bash
python voice.py

```

**Commands to try:**

* *"Nova, what time is it?"*
* *"Nova, give me a news briefing."* (Fetches and reads out the latest global headlines)
* *"Nova, play lofi beats."* (Launches an automatic web handler targeting multimedia pipelines)
* *"Nova, give me the current updates on the FIFA World Cup."* (Triggers real-time RAG web-scraping context injections)
* *"Nova, stop."* (Safely terminates all underlying threads and system loops)

---

### 📂 Project Structure

* `voice.py`: The main runtime codebase housing initialization structures, hardware listeners, and intelligence loops.
* `requirements.txt`: Curated dependency index isolating core AI framing arrays (`torch`, `whisper`) and platform-specific audio shims.
* `.env`: Storage layer protecting core network routing tokens.
* `README.md`: System architectural manual.

---

### 📝 Core Architecture Changes Note

> [!NOTE]
> This project has moved away from localized GPT-2 models to a cloud-based **Llama 3.1 8B** endpoint. This completely removes the local 500MB download and heavy hardware execution requirements, allowing the assistant to execute smoothly even on lower-end local machines while granting it access to 2026 ground-truth internet contexts.
