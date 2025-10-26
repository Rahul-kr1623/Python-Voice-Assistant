# Nova: A Python Voice Assistant 🤖

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green?logo=pygame&logoColor=white)
![GitHub repo size](https://img.shields.io/github/repo-size/Rahul-kr1623/Python-Voice-Assistant)
![License](https://img.shields.io/github/license/Rahul-kr1623/Python-Voice-Assistant)

A desktop voice assistant with a custom, animated GUI built using Python and Pygame. It understands voice commands to perform tasks, fetch live data from APIs, and control desktop applications, inspired by advanced personal assistants like "Nova".

## 📸 Demo

*A quick look at the animated GUI in action.*

<img width="796" height="633" alt="image" src="https://github.com/user-attachments/assets/06676fc7-5280-4ce9-85da-7ad2a6b54c04" />


---

## ✨ Key Features

* **🎙️ Voice-Activated:** Hands-free control with continuous "listening" and "speaking" states.
* **💻 System Control:**
    * Open any application (e.g., "Open Notepad").
    * Open and empty the Recycle Bin.
* **🌐 Web & API Integration:**
    * Get live weather for any city (via OpenWeatherMap API).
    * Search Google ("Search for...").
    * Search Wikipedia ("Wikipedia...").
    * Play any song on YouTube ("Play...").
* **🤵 Personal Assistant:**
    * Tells the time ("What is the time?").
    * Tells jokes ("Tell me a joke").
    * Opens WhatsApp chats for specific contacts ("Call Mummy").
* **🎨 Animated GUI:**
    * A multithreaded Pygame interface that runs alongside the assistant's "brain."
    * Displays the assistant's current status (Idle, Listening, Speaking, Processing).
    * Features dynamic, futuristic animations for each state.

---

## 🛠️ Tech Stack & Libraries

* **Python 3**
* **Speech & Voice:**
    * `speechrecognition`: For converting speech to text.
    * Windows SAPI5 (via PowerShell): For stable text-to-speech.
* **GUI & Graphics:**
    * `pygame`: For the animated graphical interface.
* **Functionality:**
    * `requests`: For making API calls (Weather).
    * `wikipedia`: For fetching summaries.
    * `pywhatkit`: For Google Search and playing YouTube videos.
    * `pyjokes`: For telling jokes.
    * `winshell`: For Recycle Bin access.
    * `threading`: To run the GUI and assistant logic simultaneously without freezing.

---

## 🚀 Getting Started

Follow these instructions to get your own copy of the project up and running on your local machine.

### 1. Prerequisites

You must have **Python 3** installed on your system.

### 2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Rahul-kr1623/Python-Voice-Assistant.git](https://github.com/Rahul-kr1623/Python-Voice-Assistant.git)
    cd Python-Voice-Assistant
    ```

2.  **Install all required libraries:**
    ```bash
    pip install speechrecognition wikipedia pywhatkit pyjokes requests pygame winshell
    ```

3.  **Create your configuration file:**
    In the main project folder, create a new file named `config.py`.

4.  **Add your secrets to `config.py`:**
    You must add your own OpenWeatherMap API key and contact list for the assistant to work.

    ```python
    # Inside config.py
    
    WEATHER_API_KEY = "your_own_api_key_from_openweathermap"
    
    CONTACTS = {
        "mummy": "+911234567890",
        "dad": "+911234567891"
    }
    ```

5.  **Run the assistant:**
    ```bash
    python nova_gui.py
    ```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details. You are free to modify, distribute, and use this project as you wish.
