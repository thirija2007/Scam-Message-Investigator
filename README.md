# Scam-Message-Investigator

### AI-Powered Scam Detection Using LLM

##  Project Overview
Scam Message Investigator is a Python-based AI application that analyzes suspicious SMS messages, emails, job offers, and online messages using a Large Language Model (LLM).

It uses **Gemma 3 1B through Ollama** to identify possible scam indicators, classify concern levels, explain warning signs, and recommend safety actions.

##  Key Features
- Accepts suspicious message text from users.
- Uses Gemma 3 1B for AI-powered analysis.
- Classifies messages into Low, Medium, and High Concern.
- Identifies suspicious links, payment requests, threats, and sensitive information requests.
- Generates structured investigation reports in JSON format.
- Provides safety recommendations.
- Supports downloading investigation reports.
- Includes basic error handling.

##  Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming |
| Streamlit | User interface |
| Ollama | Local model execution |
| Gemma 3 1B | Message analysis |
| Requests | API communication |
| JSON | Structured reports |

##  Project Structure

```text
Scam-Message-Investigator/
│
├── app.py
├── requirements.txt
└── README.md
```

##  Installation and Setup

**1. Clone the repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**2. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**3. Download the Gemma model**

```bash
ollama pull gemma3:1b
```

**4. Run the application**

```bash
python -m streamlit run app.py
```

##  How It Works

1. User enters a suspicious message.
2. Streamlit sends the message to the Python application.
3. Python connects to Ollama through its local API.
4. Gemma 3 1B analyzes the message.
5. The model generates a JSON investigation report.
6. Streamlit displays the concern level, warning signs, summary, and safety recommendations.

##  Concern Levels

-  **High Concern:** Strong scam indicators such as OTP requests, password theft, threats, and advance payment demands.
-  **Medium Concern:** Suspicious payment requests, unverified job offers, and unfamiliar links.
-  **Low Concern:** Normal messages without obvious scam indicators.

##  Sample Test Messages

| Message | Expected Result |
|---|---|
| Send your OTP to prevent bank account blocking. | High Concern |
| Pay ₹25 for parcel redelivery. | Medium Concern |
| Your practical exam is scheduled for Monday. | Low Concern |
| Pay ₹500 to claim your lottery prize. | High Concern |

##  Safety and Limitations

- AI predictions are not always accurate.
- The application analyzes message text only.
- It cannot independently verify senders or URLs.
- Low Concern does not guarantee that a message is safe.
- Never enter real OTPs, passwords, or banking details.

##  Learning Outcomes

- Understanding Large Language Models.
- Integrating Gemma using Ollama.
- Building applications with Streamlit.
- Working with REST APIs and JSON.
- Prompt engineering and error handling.

##  Conclusion

Scam Message Investigator demonstrates the practical use of Large Language Models for identifying potential online scams. By combining Python, Streamlit, Ollama, and Gemma 3 1B, the application helps users recognize suspicious messages and understand possible security risks.

**Project Type:** LLM Practical Project  
**Model:** Gemma 3 1B  
**Framework:** Streamlit  
**Language:** Python
