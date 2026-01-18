import speech_recognition as sr
import re
import os
import time
import requests 
import datetime
import webbrowser
import pyttsx3
from pytube import Search
from google import genai

def speak(text, rate=150):
    global IS_SPEAKING
    IS_SPEAKING = True

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)
    IS_SPEAKING = False

def clean_response(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # *italic* or bullet
    text = re.sub(r"`(.*?)`", r"\1", text)        # `code`
    text = re.sub(r"\n+", " ", text)              # Collapse multiple newlines
    return text.strip()

def ai_response(prompt):
    try:
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        response = client.models.generate_content(
            model="gemma-3-4b-it",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        speak("I'm having trouble reaching the AI service right now.")
        return ""

def play_youtube_video(query):
    try:
        search = Search(query)
        video = search.results[0]
        webbrowser.open(video.watch_url)
        speak(f"Playing {query} on YouTube.")
    except Exception as e:
        speak("Sorry, I couldn't find that video.")

def fetch_news(api_key):
    try:
        url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=in&max=7&apikey={api_key}"
        response = requests.get(url)
        print(response.text)
        data = response.json()
        if 'articles' not in data:
            speak("I could not find news articles")
            return []
        articles = data['articles']
        titles = [article['title'] for article in articles[:7]]
        return titles
    except Exception as e:
        print(f"[News Error - US] {e}")
        return []

WAKE_WORDS = ["nova", "hey nova", "hello nova"]
def process_command(command):
    command = command.lower()

    if 'introduce yourself' in command:
        speak("Hi, I'm Nova, your AI voice assistant. I can play videos, fetch news, and answer almost anything.")

    elif 'current date and time' in command:
        now = datetime.datetime.now()
        speak(f"Date: {now.strftime('%B %d, %Y')}, Time: {now.strftime('%I:%M %p')}")

    elif 'open google' in command:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    
    elif 'open youtube' in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    
    elif 'open linkedin' in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn.")

    elif 'news' in command:
        api_key = "News_api_key"
        speak("Fetching top news...")   
        headlines = fetch_news(api_key)
        if headlines:
            speak("Here are the top news headlines:")
            for idx, title in enumerate(headlines, 1):
                speak(f"Headline {idx}: {title}")
        else:
            speak("Sorry, I couldn't find any news right now.")

    elif command.startswith("play"):
        query = command.replace("play", "").strip()
        play_youtube_video(query)

    else:
        try:
            reply = ai_response(command)
            clean_reply = clean_response(reply)
            if clean_reply:
                speak(clean_reply)
            else:
                speak("Sorry, I couldn't understand that.")
        except Exception as e:
            print(f"[AI Error] {e}")
            speak("Something went wrong with the AI response.")

def listen_for_command():
    global IS_SPEAKING
    if IS_SPEAKING:
        return ""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            print("Listening...")
            audio = recognizer.listen(source, timeout=8)
        query = recognizer.recognize_google(audio).lower()
        print(f"[Heard]: {query}")
        return query
    except Exception as e:
        print(f"[Listen Error] {e}")
        return ""
    
# Main Loop
if __name__ == "__main__":
    print("Nova is ready. Say 'Nova' to start.")
    speak("Nova is ready. Say 'Nova' to start.")
    while True:
        wake = listen_for_command()
        if not wake:
            continue
        def is_wake_word(text):
            return any(re.search(rf"\b{w}\b", text) for w in WAKE_WORDS)
        if not is_wake_word(wake):
            continue
        speak("Yes?")
        command = listen_for_command()
        if not command:
            speak("I didn't hear a command.")
            continue
        print(f"Command received: {command}")
        process_command(command)
        # cooldown to prevent re-trigger
        time.sleep(2.5)

