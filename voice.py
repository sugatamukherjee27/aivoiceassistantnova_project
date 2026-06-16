import os
import sys
import time
import datetime
import warnings
import subprocess
import xml.etree.ElementTree as ET
import webbrowser
import urllib.parse
import textwrap  # Used to dynamically wrap lines into custom column boundaries
from typing import List, Any, Dict

# Clear screen instantly at launch to keep the boot process tracking clean
subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

# --- MANUAL ENVIRONMENTAL FILE INJECTION OVERRIDE ---
def load_env_manually(filepath: str = ".env") -> None:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    clean_value = value.strip().strip("'").strip('"')
                    os.environ[key.strip()] = clean_value

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

load_env_manually()

# Suppress heavy machine learning initialization logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

# --- 1. CORE DEPENDENCY VERIFICATION ---
try:
    import torch
    import whisper
    import requests
except ImportError as e:
    print(f"\033[1;31m[-] Missing critical library: {e}\033[0m")
    print("\033[1;33m[*] Please ensure your requirements.txt dependencies are fully installed.\033[0m")
    sys.exit(1)

# --- 2. ANSI HIGH-TECH TERMINAL FORMATTING ---
def print_status(msg: str) -> None:
    print(f"\033[1;34m[*] {msg}\033[0m")

def print_nova(msg: str) -> None:
    """Stretches the interface to the right to maximize layout usage and reduce box height."""
    box_width = 115
    content_width = box_width - 4  # Standard text window bounds inside the borders

    # Math-aligned top and bottom border frames to match width perfectly
    header = f"\033[1;36m┌── Nova Pro AI { '─' * (box_width - 16) }┐\033[0m"
    footer = f"\033[1;36m└{ '─' * (box_width - 2) }┘\033[0m"
    
    print(f"\n{header}")
    
    # Text wrapping split engine to feed sentences cleanly onto broad horizons
    lines = textwrap.wrap(msg, width=content_width)
    for line in lines:
        padding_spaces = content_width - len(line)
        print(f"\033[1;36m│\033[0m\033[1;37m {line}{' ' * padding_spaces} \033[0m\033[1;36m│\033[0m")
        
    print(footer)

def print_user(msg: str) -> None:
    print(f"\033[1;30m👤 You said: {msg}\033[0m")

# --- 3. COGNITIVE ENGINE INITIALIZATION ---
print("\033[1;36m🚀 Loading Nova Pro AI Core Neural Architecture...\033[0m")

try:
    print_status("Loading local OpenAI Whisper Engine (base)...")
    stt_model = whisper.load_model("base")
    print("\033[1;32m[+] Neural Audio Engine Ready!\033[0m")
except Exception as e:
    print(f"\033[1;31m[CRITICAL ERROR] Failed to load Whisper core: {e}\033[0m")
    sys.exit(1)

WAKE_WORDS = ["hey nova", "hello nova", "nova"]
TEMP_INPUT_FILE = "input_capture.wav"
TEMP_OUTPUT_FILE = "output_synthesis.mp3"

# --- 4. MULTI-MODAL PIPELINE (TEXT + VOICE SUB-SYSTEMS) ---

def speak(text: str) -> None:
    """Outputs modern styled terminal panels and synthesizes audio voice output natively."""
    if not text or not text.strip(): 
        return
    
    clean_text = text.replace('*', '').replace('_', '').strip()
    print_nova(clean_text)
    
    try:
        encoded_text = urllib.parse.quote(clean_text)
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={encoded_text}"
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(tts_url, headers=headers, timeout=3)
        
        if response.status_code == 200:
            with open(TEMP_OUTPUT_FILE, "wb") as f:
                f.write(response.content)
            
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", TEMP_OUTPUT_FILE],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if os.path.exists(TEMP_OUTPUT_FILE):
                os.remove(TEMP_OUTPUT_FILE)
            return
            
    except Exception:
        pass

    # Offline engine fallback
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(clean_text)
        engine.runAndWait()
    except Exception:
        pass

def listen(duration_seconds: int = 5, prompt_hint: str = "") -> str:
    """Captures microphone array streams. If hardware is absent or empty, falls back to text input."""
    if os.path.exists(TEMP_INPUT_FILE):
        try: os.remove(TEMP_INPUT_FILE)
        except Exception: pass

    if sys.platform == "win32":
        ffmpeg_device_args = ["-f", "dshow", "-i", "audio=default"]
    elif sys.platform == "darwin":
        ffmpeg_device_args = ["-f", "avfoundation", "-i", ":0"]
    else:
        ffmpeg_device_args = ["-f", "alsa", "-i", "default"]

    cmd = ["ffmpeg", "-y", "-loglevel", "quiet"] + ffmpeg_device_args + ["-t", str(duration_seconds), TEMP_INPUT_FILE]
    
    try:
        print(f"\n\033[1;32m👂 Listening ({duration_seconds}s)... Speak now.\033[0m")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(TEMP_INPUT_FILE) and os.path.getsize(TEMP_INPUT_FILE) > 2000:
            print("\033[1;33m🧠 Processing speech models...\033[0m")
            result = stt_model.transcribe(TEMP_INPUT_FILE, fp16=torch.cuda.is_available(), language="en")
            
            if isinstance(result, dict):
                transcription = result.get("text", "")
                if isinstance(transcription, str) and transcription.strip():
                    print_user(transcription.strip())
                    return transcription.lower().strip()
        
    except Exception:
        pass 
    finally:
        if os.path.exists(TEMP_INPUT_FILE):
            try: os.remove(TEMP_INPUT_FILE)
            except Exception: pass

    print("\033[1;33m⌨️  Microphone stream unavailable/empty. Switching to input prompt...\033[0m")
    text_input = input(f"\033[1;32m⌨️  Type command {prompt_hint}: \033[0m")
    if text_input.strip():
        print_user(text_input.strip())
        return text_input.lower().strip()
    return ""

# --- 5. DATA INGESTION & COGNITIVE LOGIC ---

def get_live_news() -> List[str]:
    headlines: List[str] = []
    try:
        response = requests.get("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", timeout=4)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            if items:
                for item in items[:3]:
                    title_element = item.find("title")
                    if title_element is not None and title_element.text is not None:
                        headlines.append(str(title_element.text).strip())
    except Exception:
        pass
    return headlines

def query_problem_solver(query: str) -> str:
    """Routes cognitive requests to Groq with live context integration to handle real-time 2026 data."""
    groq_key = os.environ.get("GROQ_API_KEY")
    
    if not groq_key:
        return "My Groq neural link is missing. Please add your GROQ_API_KEY to your dot env file."

    current_date_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    # Real-time tracking triggers for live sports, updates, or current events
    timely_keywords = ["update", "ongoing", "current", "live", "latest", "now", "today", "world cup", "match", "score", "fifa", "standing"]
    live_context = ""
    
    if any(kw in query.lower() for kw in timely_keywords):
        try:
            # Query the Google News RSS search engine directly to retrieve temporary dynamic ground-truth items
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            res = requests.get(search_url, timeout=4)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                items = root.findall(".//item")
                snippets = []
                for item in items[:5]:
                    title = item.find("title")
                    if title is not None and title.text:
                        snippets.append(f"- {title.text}")
                if snippets:
                    live_context = "\n".join(snippets)
        except Exception:
            pass

    # Re-align Nova's cognitive temporal perspective so it behaves natively in 2026
    system_instruction = (
        f"You are Nova, an advanced, highly articulate real-time AI companion. "
        f"The current date is officially {current_date_str}. "
        f"You must use the provided real-time background context if available to synthesize accurate, up-to-date responses. "
        f"Never say you have a 'knowledge cutoff of 2023' or that you don't know current events—you have live data streams."
    )
    
    user_payload = f"User Query: {query}"
    if live_context:
        user_payload += f"\n\nLive Verified News Context Reference:\n{live_context}"

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.1-8b-instant",  
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_payload}
            ],
            "max_tokens": 350
        }
        res = requests.post(url, json=payload, headers=headers, timeout=6)
        
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        else:
            return "My connection to the Groq network returned an unexpected routing error."
            
    except Exception:
        return "I experienced a network timeout reaching the Groq servers."

# --- 6. CORE OPERATION ENGINE ---

def main() -> None:
    print("\033[1;36m====================================================\033[0m")
    print("\033[1;36m🤖 NOVA PRO ARCHITECTURE -- ACTIVE                  \033[0m")
    print("\033[1;36m====================================================\033[0m")
    
    speak("Nova Pro system optimization complete. Dynamic RAG search protocols activated.")
    
    while True:
        print("\033[1;30m💤 System standing by... (State command directly or say 'nova')\033[0m")
        raw_input = listen(duration_seconds=3, prompt_hint="(or type any command directly)")

        if not raw_input or not raw_input.strip():
            continue

        command = ""
        triggered_wake_words = [word for word in WAKE_WORDS if word in raw_input]

        if triggered_wake_words:
            matched_wake = max(triggered_wake_words, key=len)
            parts = raw_input.split(matched_wake, 1)
            trailing_command = parts[1].strip() if len(parts) > 1 else ""
            
            if trailing_command:
                command = trailing_command
            else:
                speak("System open. State your command.") 
                command = listen(duration_seconds=6, prompt_hint="(e.g. 'time', 'news', 'exit')")
        else:
            command = raw_input

        if not command or not command.strip():
            print("\033[1;30m[!] Empty command path. Returning to system standby.\033[0m")
            continue
            
        match command:
            case c if "time" in c:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The local system time reads exactly {current_time}.")
                
            case c if "briefing" in c or "news" in c:
                speak("Accessing live standard news feeds now.")
                headlines = get_live_news()
                if headlines:
                    for i, title in enumerate(headlines):
                        speak(f"Update {i+1}: {title}")
                else:
                    speak("Live data stream timed out. Unable to fetch structural feed channels.")
                    
            case c if "play" in c:
                song = command.replace("play", "").strip()
                speak(f"Opening standard media query paths for {song} now.")
                webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}")
                
            case c if any(exit_word in c for exit_word in ["stop", "exit", "bye", "shutdown"]):
                speak("Deactivating underlying neural cores. System shutting down.")
                sys.exit(0)
                
            case _:
                response_text = query_problem_solver(command)
                speak(response_text)

if __name__ == "__main__":
    main()
