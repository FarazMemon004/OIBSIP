# 🎙️ Voice Assistant – Python (OIBSIP Task 1)

A Python-based voice assistant that uses speech recognition and text-to-speech to interact with users, answer basic questions, perform web searches, retrieve weather information, and send emails.

This project was developed as part of the **Oasis Infobyte Internship Program (OIBSIP)**.

## ✨ Features

- 🎤 Voice input using speech recognition.
- 🔊 Spoken responses using text-to-speech.
- 👋 Responds to greetings such as "Hello".
- 🕒 Tells the current time and date.
- 🌐 Opens a browser and performs web searches.
- 🌦️ Retrieves weather information using the OpenWeather API.
- 📧 Sends emails using SMTP.
- 🧠 Includes additional natural language processing capabilities.
- 🔁 Asks the user to repeat a command when speech is not understood.
- 🔐 Uses environment variables to keep credentials out of source code.

## 🛠️ Technologies Used

- Python
- SpeechRecognition
- OpenAI Whisper (speech recognition, if configured)
- pyttsx3 (text-to-speech)
- Requests
- NLTK / Transformers (depending on the enabled features)
- SMTP
- OpenWeather API
- python-dotenv

## 📁 Project Structure

```text
OIBSIP-Python-Task1-Voice-Assistant/
├── main.py
├── requirements.txt
├── .env
├── .commond.json
├── .knowledge.py
├── .gitignore
└── README.md
```

Your actual project may contain additional Python files or folders.

## ⚙️ Requirements

- Python 3.10 or 3.11 recommended.
- A working microphone.
- Internet connection for online speech recognition, web searches, and weather requests.
- An email account with SMTP access if you want to use the email feature.
- An OpenWeather API key for weather information.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/FarazMemon004/OIBSIP/tree/main/Python/Task1-Voice%20Assistant
cd OIBSIP-Python-Task1-Voice-Assistant
```


### 2. Create a virtual environment

For macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a package requires additional system dependencies, install the appropriate dependencies for your macOS version.

### 4. Create your `.env` file

For privacy and security reasons, **email credentials and API tokens are not included in this GitHub repository**. You must create your own `.env` file and enter your own credentials.

In the project root, create a file named `.env`:

```bash
touch .env
```

Open the file and add:

```dotenv
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_email_app_password
OPENWEATHER_API_KEY=your_openweather_api_key
```

Replace the example values with your actual credentials.

**Important:** These are example environment variable names. Make sure they match the names your Python code reads using `os.getenv()` or `os.environ`.

### 5. Configure email access

If you use Gmail, generate an **App Password** through your Google Account's security settings if your account supports it. Use that App Password instead of your normal Gmail password.

Never publish your email password, App Password, or API token in your source code or GitHub repository.

### 6. Get an OpenWeather API key

1. Visit https://openweathermap.org/api
2. Create an account or sign in.
3. Obtain an API key.
4. Add it to your `.env` file as `OPENWEATHER_API_KEY`.

The key may need time to become active, depending on the provider.

### 7. Protect your credentials with `.gitignore`

Create or update `.gitignore` in the project root:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
.DS_Store
```

This prevents Git from tracking your local environment file and other unnecessary files.

**GitHub privacy note:** The credentials are intentionally excluded from the repository. Each person cloning the project must create their own `.env` file and supply their own email configuration and OpenWeather API key. Do not commit secrets, even in a private repository.

### 8. Run the voice assistant

```bash
python main.py
```

Follow the prompts and grant microphone permissions if macOS requests them.

## 🔑 Environment Variables in Python

Use `python-dotenv` to load your local configuration:

```python
import os
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
weather_api_key = os.getenv("OPENWEATHER_API_KEY")
```

If any required credential is missing, display a helpful error message instead of attempting the relevant operation.

## 🧪 Troubleshooting

- **Microphone not working:** Check macOS microphone permissions and your selected input device.
- **Speech recognition errors:** Check your internet connection and verify that the configured recognition engine and dependencies are installed.
- **Text-to-speech issues:** Confirm that the required audio libraries and system speech services are available.
- **Email sending fails:** Verify SMTP settings, recipient addresses, and your email App Password.
- **Weather requests fail:** Check the API key, network connection, API usage limits, and provider response.
- **Missing environment variables:** Ensure `.env` is in the project root and the variable names match your Python code.
- **Package installation errors:** Verify your Python version and consult the relevant package documentation.

## 🔒 Security

- Never commit `.env` to GitHub.
- Never share your email password or API keys.
- Use App Passwords or an appropriate authenticated email method.
- If a credential is accidentally published, revoke or rotate it immediately.
- Request only the permissions the application needs.

## 🎯 Learning Objectives

This project demonstrates practical experience with Python programming, voice interaction, speech recognition, text-to-speech, API integration, SMTP email delivery, environment configuration, and error handling.

## 👨‍💻 Author

**Muhammad Faraz**

Software Engineering | Python Development | AI Projects

## 📄 License

This project is intended for educational and learning purposes. Add a license file if you want to specify the terms under which others may use or modify the code.
