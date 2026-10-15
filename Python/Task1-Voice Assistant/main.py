import os
import re
import json
import time
import threading
import smtplib
import webbrowser
from datetime import datetime
from email.message import EmailMessage
from urllib.parse import quote_plus
import requests
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from nltk import NaiveBayesClassifier

from knowledge import answer_question

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "")

COMMANDS_FILE = "commands.json"

recognizer = sr.Recognizer()
speech_engine = pyttsx3.init()
speech_engine.setProperty("rate", 175)
speech_engine.setProperty("volume", 1.0)

# Protect text-to-speech when reminders run in background.
speech_lock = threading.RLock()

# Prevent reminders from disappearing while scheduled.
reminder_threads = []


# --------------------------------------------------
# TEXT TO SPEECH
# --------------------------------------------------

def speak(message):
    print(f"\nAssistant: {message}")

    with speech_lock:
        speech_engine.say(message)
        speech_engine.runAndWait()


# --------------------------------------------------
# SPEECH RECOGNITION
# --------------------------------------------------

def listen(prompt=None, timeout=8, phrase_time_limit=15):
    if prompt:
        speak(prompt)

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(
                source, duration=0.5
            )
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        text = recognizer.recognize_google(
            audio, language="en-US"
        ).strip()

        print("You:", text)
        return text

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please repeat.")
    except sr.RequestError:
        speak(
            "Speech recognition is unavailable. "
            "Please check your internet connection."
        )
    except (OSError, AttributeError) as error:
        print("Microphone error:", error)
        speak("I cannot access the microphone. Check its permissions.")

    return ""


# --------------------------------------------------
# CUSTOM COMMANDS
# --------------------------------------------------

def load_commands():
    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}


def save_commands(commands):
    with open(COMMANDS_FILE, "w", encoding="utf-8") as file:
        json.dump(commands, file, indent=4, ensure_ascii=False)


def add_custom_command():
    phrase = listen("Say the phrase for your new command.")

    if not phrase:
        return

    response = listen("Now say the response I should give.")

    if not response:
        speak("The command was not saved because no response was received.")
        return

    commands = load_commands()
    commands[phrase.lower().strip()] = response.strip()
    save_commands(commands)

    speak("Your custom command has been saved.")


# --------------------------------------------------
# NLP INTENT CLASSIFIER USING NLTK
# --------------------------------------------------

TRAINING_EXAMPLES = {
    "greeting": [
        "hello", "hi", "hey assistant", "good morning",
        "hello there", "how are you"
    ],
    "time": [
        "what time is it", "tell me the time",
        "current time please", "can you tell me the time"
    ],
    "date": [
        "what is today's date", "tell me the date",
        "what day is it", "current date please"
    ],
    "search": [
        "search for Python tutorials", "google machine learning",
        "look up artificial intelligence", "find information about Python"
    ],
    "weather": [
        "what is the weather in Karachi", "check the weather",
        "weather forecast for Sukkur", "is it raining in Lahore"
    ],
    "reminder": [
        "remind me in ten minutes to study",
        "set a reminder for five seconds",
        "remind me to drink water in one hour"
    ],
    "email": [
        "send an email", "compose an email",
        "I want to email my manager", "please send a message by email"
    ],
    "knowledge": [
        "who is Albert Einstein", "what is machine learning",
        "tell me about Pakistan", "explain artificial intelligence"
    ],
    "add_command": [
        "add a custom command", "create a new command",
        "teach yourself a new response"
    ],
    "capabilities": [
        "what can you do", "help me", "show your features"
    ],
    "exit": [
        "exit assistant", "stop assistant",
        "goodbye", "quit the program"
    ]
}


def word_features(text):
    """Extract simple word-presence features for NLTK."""
    words = set(re.findall(r"[a-z0-9']+", text.lower()))
    return {word: True for word in words}


def train_intent_classifier():
    training_data = []

    for intent, examples in TRAINING_EXAMPLES.items():
        for example in examples:
            training_data.append(
                (word_features(example), intent)
            )

    return NaiveBayesClassifier.train(training_data)


intent_classifier = train_intent_classifier()


def detect_intent(text):
    if not text.strip():
        return "unknown"

    intent = intent_classifier.classify(word_features(text))

    # Avoid treating unrelated speech as a valid intent.
    # A classifier trained on a small example set needs a
    # conservative vocabulary-overlap check.
    words = set(re.findall(r"[a-z0-9']+", text.lower()))
    known_words = set()

    for examples in TRAINING_EXAMPLES.values():
        for example in examples:
            known_words.update(
                re.findall(r"[a-z0-9']+", example.lower())
            )

    if not words.intersection(known_words):
        return "unknown"

    return intent


# --------------------------------------------------
# TIME AND DATE
# --------------------------------------------------

def tell_time():
    speak(f"The current time is {datetime.now().strftime('%I:%M %p')}.")


def tell_date():
    speak(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.")


# --------------------------------------------------
# WEB SEARCH
# --------------------------------------------------

def web_search(query):
    query = query.strip()

    if not query:
        query = listen("What would you like me to search for?")

    if query:
        webbrowser.open(
            "https://www.google.com/search?q=" + quote_plus(query)
        )
        speak(f"Opening search results for {query}.")


# --------------------------------------------------
# WEATHER
# --------------------------------------------------

def get_weather(city):
    if not WEATHER_API_KEY:
        speak(
            "Weather is not configured. Add your OpenWeatherMap "
            "API key to the environment file."
        )
        return

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": WEATHER_API_KEY,
                "units": "metric"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        speak(
            f"In {city}, the weather is {description}. "
            f"The temperature is {temperature} degrees Celsius, "
            f"and it feels like {feels_like} degrees."
        )

    except requests.HTTPError as error:
        print("Weather API error:", error)
        speak("The weather service rejected the request. Check your API key and city.")
    except (requests.RequestException, KeyError, IndexError, TypeError) as error:
        print("Weather error:", error)
        speak("I could not retrieve the current weather.")


def extract_city(command):
    match = re.search(
        r"(?:weather|forecast)\s+(?:in|for)\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip(" .?!")

    return "Karachi"


# --------------------------------------------------
# TIMED REMINDERS
# --------------------------------------------------

NUMBER_WORDS = {
    "a": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "fifteen": 15,
    "twenty": 20,
    "thirty": 30
}


def parse_number(value):
    if value.isdigit():
        return int(value)

    return NUMBER_WORDS.get(value.lower())


def set_reminder(seconds, message):
    def alert():
        time.sleep(seconds)
        speak(f"Reminder: {message}")

    thread = threading.Thread(target=alert, daemon=True)
    thread.start()
    reminder_threads.append(thread)

    speak(f"I will remind you in {seconds} seconds to {message}.")


def handle_reminder(command):
    match = re.search(
        r"(?:remind me|set a reminder)\s+"
        r"(?:in\s+)?(\w+)\s+"
        r"(seconds?|minutes?|hours?)"
        r"(?:\s+to\s+(.+))?",
        command,
        re.IGNORECASE
    )

    if not match:
        speak(
            "Please say, remind me in ten minutes to study."
        )
        return

    amount = parse_number(match.group(1))
    unit = match.group(2).lower()
    message = (match.group(3) or "complete your task").strip()

    if amount is None or amount <= 0:
        speak("I could not understand the reminder duration.")
        return

    if unit.startswith("second"):
        multiplier = 1
    elif unit.startswith("minute"):
        multiplier = 60
    else:
        multiplier = 3600

    seconds = amount * multiplier

    # Safety limit for this simple in-memory implementation.
    if seconds > 30 * 24 * 3600:
        speak("Please set a reminder within the next 30 days.")
        return

    set_reminder(seconds, message)


# --------------------------------------------------
# VOICE-BASED EMAIL
# --------------------------------------------------


def normalize_email(text):
    """Normalize common speech-recognition mistakes in email addresses."""

    text = text.lower().strip()

    # Convert spoken symbols into email characters.
    replacements = {
        " at sign ": "@",
        " at the rate ": "@",
        " at rate ": "@",
        " at ": "@",
        " dot ": ".",
        " period ": ".",
        " underscore ": "_",
        " hyphen ": "-",
        " dash ": "-",
    }

    for spoken, symbol in replacements.items():
        text = text.replace(spoken, symbol)

    # Remove spaces introduced by speech recognition.
    text = re.sub(r"\s+", "", text)

    # Common speech recognition substitutions.
    # Apply only to the local part, not the domain.
    if "@" not in text:
        text = text.replace("8", "@", 1) if "8" in text else text
    elif text.count("@") > 1:
        text = text.replace("@", "", text.count("@") - 1)

    if "@" in text:
        local, domain = text.split("@", 1)

        # Commonly misrecognized spoken "gmail".
        domain = domain.replace("gamil.com", "gmail.com")
        domain = domain.replace("gmai.com", "gmail.com")

        text = local + "@" + domain

    return text


def is_valid_email(email):
    """Basic email format validation."""
    return bool(
        re.fullmatch(
            r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
            r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+",
            email
        )
    )


def compose_email_by_voice():
    speak(
        "Please say the recipient email address slowly. "
        "You can say the word at and then the word dot."
    )

    recipient_text = listen(phrase_time_limit=20)

    if not recipient_text:
        speak("I could not hear the email address.")
        return

    recipient = normalize_email(recipient_text)

    # Never silently assume that a guessed correction is correct.
    while True:
        speak(f"I recognized the email address as {recipient}.")

        if is_valid_email(recipient):
            speak(
                "If this address is correct, say confirm address. "
                "Otherwise say correct address."
            )
        else:
            speak(
                "The email address does not look valid. "
                "Please say correct address and try again."
            )

        choice = listen(phrase_time_limit=10).lower().strip()

        if choice == "confirm address" and is_valid_email(recipient):
            break

        if choice in ("cancel email", "cancel"):
            speak("Email cancelled.")
            return

        if choice in ("correct address", "try again", "repeat"):
            recipient_text = listen(
                "Please repeat the email address slowly.",
                phrase_time_limit=20
            )

            if not recipient_text:
                speak("No address was received. Email cancelled.")
                return

            recipient = normalize_email(recipient_text)
            continue

        speak("I did not understand. Please say confirm address, correct address, or cancel email.")

    subject = listen("Please say the email subject.")

    if not subject:
        speak("No subject was captured. Email cancelled.")
        return

    body = listen(
        "Please dictate the email message.",
        phrase_time_limit=60
    )

    if not body:
        speak("No message was captured. Email cancelled.")
        return

    speak(
        f"The recipient is {recipient}. "
        f"The subject is {subject}. "
        f"The message is {body}. "
        "Say confirm send to send the email, or cancel email to cancel."
    )

    confirmation = listen(phrase_time_limit=10).lower().strip()

    if confirmation == "confirm send":
        send_email(recipient, subject, body)
    else:
        speak("Email cancelled. Nothing was sent.")


def send_email(recipient, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        speak("Email is not configured. Please check your environment file.")
        return False

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", recipient):
        speak("That email address does not look valid. Email cancelled.")
        return False

    message = EmailMessage()
    message["From"] = EMAIL_ADDRESS
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL(
                "smtp.gmail.com", 465, timeout=15
        ) as server:
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(message)

        speak("Your email has been sent.")
        return True

    except (smtplib.SMTPException, OSError) as error:
        print("Email error:", error)
        speak("I could not send the email. Check your email configuration.")
        return False


def compose_email_by_voice():
    recipient_text = listen(
        "Say the recipient's email address. "
        "You can say at and dot for the symbols.",
        phrase_time_limit=20
    )

    recipient = normalize_email(recipient_text)

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", recipient):
        speak(
            "I could not recognize a valid email address. "
            "Please try again or cancel the email."
        )
        recipient_text = listen("Please spell or repeat the email address.")
        recipient = normalize_email(recipient_text)

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", recipient):
        speak("The email address is still invalid. Email cancelled.")
        return

    subject = listen("Please say the email subject.")
    if not subject:
        speak("No subject was captured. Email cancelled.")
        return

    body = listen(
        "Please dictate the email message.",
        phrase_time_limit=60
    )
    if not body:
        speak("No email message was captured. Email cancelled.")
        return

    speak(
        f"You are about to send an email to {recipient}. "
        f"The subject is {subject}. "
        f"The message is: {body}. "
        "Say confirm send to send it, or cancel email to cancel."
    )

    confirmation = listen("Please confirm your choice.")

    if confirmation.lower().strip() == "confirm send":
        send_email(recipient, subject, body)
    else:
        speak("Email cancelled. Nothing was sent.")


# --------------------------------------------------
# GENERAL KNOWLEDGE
# --------------------------------------------------

def handle_question(command):
    question = re.sub(
        r"^(please\s+)?(tell me about|explain|who is|what is|"
        r"what are|where is|when did|when was|why is|how does)\s+",
        "",
        command,
        flags=re.IGNORECASE
    ).strip()

    if not question:
        question = listen("What would you like to know?")

    if question:
        speak("Let me look that up.")
        answer = answer_question(question)
        speak(answer)


# --------------------------------------------------
# COMMAND HANDLER
# --------------------------------------------------

def handle_command(command):
    if not command:
        return True

    normalized = command.lower().strip()

    # Exact user-created commands take priority.
    custom_commands = load_commands()

    if normalized in custom_commands:
        speak(custom_commands[normalized])
        return True

    intent = detect_intent(normalized)
    print("Detected intent:", intent)

    if intent == "exit":
        speak("Goodbye! Have a great day.")
        return False

    if intent == "greeting":
        speak("Hello! How can I help you?")
        return True

    if intent == "time":
        tell_time()
        return True

    if intent == "date":
        tell_date()
        return True

    if intent == "search":
        query = re.sub(
            r"^(search for|google|look up|find information about)\s*",
            "",
            normalized,
            flags=re.IGNORECASE
        ).strip()
        web_search(query)
        return True

    if intent == "weather":
        get_weather(extract_city(normalized))
        return True

    if intent == "reminder":
        handle_reminder(normalized)
        return True

    if intent == "email":
        compose_email_by_voice()
        return True

    if intent == "knowledge":
        handle_question(normalized)
        return True

    if intent == "add_command":
        add_custom_command()
        return True

    if intent == "capabilities":
        speak(
            "I can greet you, tell the time and date, search the web, "
            "read current weather, set timed reminders, compose and send "
            "emails with your confirmation, answer general knowledge "
            "questions, and save custom commands."
        )
        return True

    speak(
        "I could not identify that request. "
        "Please repeat it or try asking in another way."
    )
    return True


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

def main():
    speak("Python voice assistant is ready.")
    speak(
        "Try saying hello, what time is it, search for Python, "
        "or what is the weather in Karachi."
    )

    running = True

    while running:
        command = listen()

        if command:
            running = handle_command(command)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Voice assistant stopped.")
