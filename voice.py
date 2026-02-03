import sys
import os
import time
import datetime
import warnings
import pygame 
import requests
from gtts import gTTS 
import speech_recognition as sr
import feedparser
import pywhatkit 
from newspaper import Article
import nltk
from transformers import pipeline, logging as transformers_logging
from ddgs import DDGS

# --- 1. CONFIGURATION ---
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" 
warnings.filterwarnings("ignore")
transformers_logging.set_verbosity_error()

try:
    nltk.download('punkt', quiet=True)
except:
    pass

# --- 2. INITIALIZATION ---
print("Initializing Nova Pro AI...")

def load_ai():
    try:
        print(" - Loading Neural Engine (GPT-2)...", end=" ", flush=True)
        # Using text-generation for maximum compatibility
        engine = pipeline("text-generation", model="gpt2", device=-1)
        print("Ready!")
        return engine
    except Exception as e:
        print(f"\n[CRITICAL ERROR] AI failed: {e}")
        return None

ai_engine = load_ai()
WAKE_WORDS = ["nova", "hey nova", "hello nova"]

# --- 3. CORE FUNCTIONS ---

def speak(text):
    if not text or not text.strip(): return
    clean_text = text.replace('*', '').replace('_', '').strip()
    print(f"[Nova]: {clean_text}")
    try:
        tts = gTTS(text=clean_text, lang='en', slow=False)
        filename = f"voice_{int(time.time())}.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        time.sleep(0.1)
        if os.path.exists(filename): os.remove(filename)
    except Exception as e:
        print(f"Audio Error: {e}")

def get_detailed_briefing():
    speak("Gathering the latest headlines for your briefing.")
    feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
    
    if not feed.entries:
        speak("I couldn't retrieve any news at the moment.")
        return

    for i, entry in enumerate(feed.entries[:3]):
        # The title often includes the source (e.g., "Title - Source")
        # Let's clean it up for the AI
        raw_title = entry.title
        
        speak(f"Story {i+1}: {raw_title}")
        
        if ai_engine:
            # We use the title and the summary provided by the RSS feed itself
            # This avoids the need to download external web pages
            snippet = entry.get('summary', 'No description available.')
            prompt = f"Explain the significance of this news headline in one sentence: {raw_title}\n\nAnalysis:"
            
            summary = ai_engine(prompt, max_new_tokens=50, do_sample=True, pad_token_id=50256)
            gen_text = summary[0]['generated_text'].split("Analysis:")[-1].strip()
            speak(gen_text)
        print("-" * 30)

def ai_answer(query):
    if not ai_engine: return "AI system is offline."
    try:
        search_data = list(DDGS().text(query, max_results=2))
        context = " ".join([r['body'] for r in search_data])
        prompt = f"Question: {query}\nFact: {context[:500]}\n\nDetailed Expert Answer:"
        response = ai_engine(prompt, max_new_tokens=150, do_sample=True, temperature=0.8, pad_token_id=50256)
        return response[0]['generated_text'].split("Detailed Expert Answer:")[-1].strip()
    except:
        return "I encountered an error analyzing that."

# --- 4. FIXED LISTEN FUNCTION ---

def listen(prompt_mode=False):
    """Now correctly accepts prompt_mode to change listening behavior"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            if prompt_mode:
                print("👂 Listening for command...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            # Short timeout for wake word, longer for commands
            timeout_limit = 5 if not prompt_mode else 8
            audio = r.listen(source, timeout=timeout_limit, phrase_time_limit=6)
            return r.recognize_google(audio).lower()
        except:
            return ""

# --- 5. MAIN LOOP ---

def main():
    speak("Nova Pro is online.")
    
    while True:
        print("💤 Standing by... (Say 'Nova')")
        # Step 1: Wait for wake word
        voice_input = listen(prompt_mode=False)

        if any(word in voice_input for word in WAKE_WORDS):
            # Step 2: Acknowledge
            speak("Yes?") 
            
            # Step 3: Listen for actual command
            command = listen(prompt_mode=True)
            
            if command:
                if 'time' in command:
                    speak(f"It's {datetime.datetime.now().strftime('%I:%M %p')}.")
                elif 'briefing' in command or 'detailed news' in command:
                    get_detailed_briefing()
                elif 'news' in command:
                    feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
                    for entry in feed.entries[:3]: speak(entry.title)
                elif 'play' in command:
                    song = command.replace('play', '').strip()
                    speak(f"Playing {song} on YouTube.")
                    pywhatkit.playonyt(song)
                elif any(word in command for word in ['stop', 'exit', 'bye']):
                    speak("Goodbye!")
                    sys.exit()
                else:
                    speak("Searching for a detailed answer...")
                    speak(ai_answer(command))
            else:
                print("No command detected.")

if __name__ == "__main__":
    main()