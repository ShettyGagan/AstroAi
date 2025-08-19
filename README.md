# ✨ AstroGuru: Your Personal AI Astrologer ✨

AstroGuru is a sophisticated web application that generates personalized Vedic (Sidereal) astrology readings using a powerful combination of a professional-grade astrological engine and a state-of-the-art Large Language Model (LLM).

Enter your birth details to generate a beautiful visual of your natal chart and receive a concise, insightful interpretation of your personality, strengths, and challenges. You can then engage in a conversation with the AI to explore your chart in more detail.

---

## 🚀 Features

- **Vedic (Sidereal) Calculations**: Utilizes the highly accurate Swiss Ephemeris (swisseph) with the Lahiri Ayanamsa for authentic Vedic chart generation.
- **Comprehensive Chart Data**: Calculates positions for all major planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto), the Ascendant (Lagna), and Midheaven (MC).
- **Dynamic Natal Chart Visualization**: Renders a beautiful and clear polar plot of your natal chart using Matplotlib, showing planet positions, signs, and major aspects (Conjunction, Square, Trine, etc.).
- **AI-Powered Interpretations**: Leverages the power of Groq's Llama 3 70B model via LangChain to provide nuanced, synthesized, and concise readings.
- **Knowledge-Grounded AI**: The AI's responses are grounded in a curated Vedic knowledge base (RAG pattern) for more authentic and consistent interpretations.
- **Conversational Chat Interface**: Ask follow-up questions and explore your chart's details in a natural, conversational way.
- **Automatic Geolocation & Timezone**: Simply enter your birth city, and the application automatically fetches the correct latitude, longitude, and timezone for precise calculations.
- **Interactive Web UI**: A clean, responsive, and user-friendly interface built with Streamlit.

---

## 🛠️ Tech Stack

| Category             | Technology / Library |
|----------------------|----------------------|
| Web Framework        | Streamlit            |
| Astrology Engine     | swisseph             |
| LLM & Orchestration  | langchain, langchain-groq (Llama 3 70B) |
| Geolocation          | geopy, timezonefinder, requests |
| Visualization        | matplotlib, numpy    |
| Core Language        | Python 3.10+         |
| Env Management       | python-dotenv, pytz  |

---

## ⚙️ Setup and Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/ShettyGagan/AstroAi.git
cd astroguru
```

### 3. Set Up a Virtual Environment
```bash
# For Windows
python -m venv venv
.env\Scriptsctivate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Create a `requirements.txt` file with the content below and install the packages:

```
streamlit
python-dotenv
matplotlib
numpy
langchain
langchain-groq
geopy
timezonefinder
swisseph
pytz
requests
pydantic>=2.0
```

Install using pip:
```bash
pip install -r requirements.txt
```

### 5. Configure API Keys
You will need an API key from **Groq** to use the LLM.  
Create a file named `.env` in the root of your project directory and add your API key:

```
GROQ_API_KEY="gsk_YourActualKeyHere"
```

### 6. Run the Application
```bash
streamlit run app.py
```

---

## 🏗️ How It Works

- **User Input (app.py)**: Collects user’s birth name, date, time, and place.  
- **Geolocation (utils.py)**: Fetches latitude & longitude using Nominatim API, timezone via `timezonefinder`.  
- **Astrological Calculation (astro_engine.py)**: Uses Swiss Ephemeris with Lahiri Ayanamsa for planetary calculations.  
- **AI Context Building (llm_chain.py)**: Builds chart interpretation context from data + knowledge base.  
- **LLM Interaction (llm_chain.py)**: Sends structured context to Groq LLM for interpretation.  
- **UI Rendering (visualizer.py)**: Displays natal chart visualization and AI interpretations.  

---

## 📂 Project Structure

```
.
├── .env                # Stores API keys (not committed to git)
├── app.py              # Main Streamlit application UI and logic
├── astro_engine.py     # Core astrological calculations using Swisseph
├── llm_chain.py        # LangChain setup, prompt engineering, and AI interaction
├── knowledge.py        # The Vedic knowledge base for grounding the AI
├── utils.py            # Helper functions, primarily for geolocation
├── visualizer.py       # Renders the natal chart using Matplotlib
└── requirements.txt    # List of Python dependencies
```

---

## 🔮 Future Improvements

- 🎙️ Speech-to-Text/Text-to-Speech for conversational experience.  
- 🌑 Add calculations for **Rahu/Ketu (Lunar Nodes), Chiron**, etc.  
- 🏠 Support different house systems (Whole Sign, Koch, etc.).  
- 💾 User accounts for saving/loading charts.  
- 📈 Predictive techniques: transits, progressions, dashas.  

---

## 📜 License
This project is licensed under the MIT License.
