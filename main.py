import speech_recognition as sr
import re
import requests 
import datetime
import webbrowser
import pyttsx3
from pytube import Search
import google.generativeai as genai

def speak(text, rate=150):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

def clean_response(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # *italic* or bullet
    text = re.sub(r"`(.*?)`", r"\1", text)        # `code`
    text = re.sub(r"\n+", " ", text)              # Collapse multiple newlines
    return text.strip()

def ai_response(prompt):
    try:
        genai.configure(api_key="AIzaSyAUXQFnSSPinZY-hFLFU6U187Nuo5hehwc")  
        model = genai.GenerativeModel('gemini-2.5-flash')  
        response = model.generate_content(prompt)
        if response.text:
            return response.text.strip()
        else:
            return "Sorry, I couldn't generate a response."       
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return f"Sorry, I encountered an error: {str(e)}"

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
        api_key = "0704bae53cc3b9fa8a127956804009d8"
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
        query = listen_for_command()
        if any(wake in query for wake in WAKE_WORDS):
            print("Yes?")
            speak("Yes?")
            user_command = listen_for_command()
            print(f"Command received: {user_command}")
            if user_command:
                process_command(user_command)