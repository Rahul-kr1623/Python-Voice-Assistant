# All necessary imports
import speech_recognition as sr
import datetime
import os
import webbrowser
import winshell
import wikipedia
import pywhatkit
import pyjokes
import requests
import pygame
import threading
import math
import config

# --- CONFIGURATION: API KEY and DICTIONARIES ---
WEATHER_API_KEY = config.WEATHER_API_KEY
app_map = {"notepad": "notepad", "calculator": "calc", "chrome": "chrome"}
contacts = config.CONTACTS

# --- Global status variable ---
assistant_status = "idle"

# --- ASSISTANT'S "BRAIN" (The Backend Logic) ---

def speak(text):
    """Uses Windows' built-in PowerShell speech engine for maximum stability."""
    global assistant_status
    assistant_status = "speaking"
    print(f"Nova: {text}")
    clean_text = text.replace("'", "").replace('"', '')
    command = f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\');"'
    os.system(command)
    assistant_status = "idle"

def listen_for_command():
    global assistant_status
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        assistant_status = "listening"
        print("Listening...")
        audio = recognizer.listen(source)
    assistant_status = "processing"
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}\n")
        return command.lower()
    except Exception as e:
        return ""

def run_assistant_logic():
    global running
    speak("Hello, I am online and ready.")
    while running:
        command = listen_for_command()
        if not command:
            assistant_status = "idle"
            continue

        if "hello" in command:
            speak("Hello to you too! What can I do for you?")
        elif "what is the time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
        elif "wikipedia" in command:
            query = command.replace("search wikipedia for", "").replace("wikipedia", "").strip()
            speak(f"Searching Wikipedia for {query}")
            try:
                summary = wikipedia.summary(query, sentences=2)
                speak(summary)
            except Exception as e:
                speak(f"Sorry, I couldn't find any results for {query}.")
        elif "search" in command:
            query = command.replace("search", "").strip()
            speak(f"Searching Google for {query}")
            pywhatkit.search(query)
        elif "joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)
        elif "weather" in command:
            city = command.replace("what's the weather in", "").replace("weather in", "").replace("weather", "").strip()
            if not city: city = "Delhi"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            try:
                weather_data = requests.get(url).json()
                if str(weather_data.get("cod")) == "200":
                    temp = weather_data["main"]["temp"]
                    description = weather_data["weather"][0]["description"]
                    speak(f"The weather in {city} is currently {description} with a temperature of {temp} degrees Celsius.")
                else:
                    speak(f"Sorry, I couldn't find the weather for {city}.")
            except Exception as e:
                speak("Sorry, I am unable to connect to the weather service.")
        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        elif "open" in command and "recycle bin" not in command:
            app_to_open = command.replace("open", "").strip()
            if app_to_open in app_map:
                speak(f"Opening {app_to_open}.")
                os.system(f"start {app_map[app_to_open]}")
            else:
                speak(f"Sorry, I don't know how to open {app_to_open}.")
        elif "call" in command:
            contact_to_call = command.replace("call", "").strip()
            if contact_to_call in contacts:
                phone_number = contacts[contact_to_call].lstrip('+')
                speak(f"Opening WhatsApp to call {contact_to_call}. Please click the call button.")
                webbrowser.open(f"https://wa.me/{phone_number}")
            else:
                speak(f"Sorry, I don't have a number for {contact_to_call}.")
        
        # --- FIXED RECYCLE BIN COMMANDS ---
        elif "open" in command and "recycle bin" in command:
            speak("Opening the Recycle Bin.")
            os.system("start shell:RecycleBinFolder") # Corrected from RecycleFolder
        elif "empty the recycle bin" in command:
            speak("Emptying the Recycle Bin.")
            # Using a more reliable PowerShell command
            os.system("powershell.exe -Command Clear-RecycleBin -Force")

        elif "bye" in command:
            speak("Goodbye! Shutting down.")
            running = False
            break
        else:
            speak("I am not sure how to handle that command, please try again.")
            assistant_status = "idle"

# --- ASSISTANT'S "FACE" (PYGAME GUI) ---
if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nova Assistant")
    try:
        background_image = pygame.image.load("background.jpg").convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except FileNotFoundError:
        print("Error: background.jpg not found. Using a black background.")
        background_image = None
    font = pygame.font.SysFont('Arial', 24, True)
    BLACK, WHITE, ACCENT_COLOR, GLOW_COLOR = (0, 0, 0), (255, 255, 255), (0, 255, 150), (0, 255, 150, 60)
    
    running = True
    assistant_thread = threading.Thread(target=run_assistant_logic)
    assistant_thread.start()
    
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)
        status_text_surface = font.render(assistant_status.upper(), True, WHITE)
        screen.blit(status_text_surface, (WIDTH // 2 - status_text_surface.get_width() // 2, 50))
        center_pos = (WIDTH // 2, HEIGHT // 2)
        if assistant_status == "listening":
            pulse_radius = 50 + (math.sin(pygame.time.get_ticks() * 0.005) * 20)
            glow_surface = pygame.Surface((pulse_radius * 2, pulse_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, GLOW_COLOR, (pulse_radius, pulse_radius), pulse_radius)
            screen.blit(glow_surface, (center_pos[0] - pulse_radius, center_pos[1] - pulse_radius))
        elif assistant_status == "speaking" or assistant_status == "processing":
            angle = pygame.time.get_ticks() * 0.1
            pygame.draw.arc(screen, ACCENT_COLOR, (center_pos[0] - 60, center_pos[1] - 60, 120, 120), math.radians(angle), math.radians(angle + 120), 5)
            pygame.draw.arc(screen, WHITE, (center_pos[0] - 80, center_pos[1] - 80, 160, 160), math.radians(-angle), math.radians(-angle + 120), 5)
        pygame.draw.circle(screen, ACCENT_COLOR, center_pos, 50, 3)
        pygame.draw.circle(screen, WHITE, center_pos, 40, 1)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    assistant_thread.join()