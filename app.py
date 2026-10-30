import streamlit as st
import requests
import json

MODEL_NAME = "gemma3:1b"
LOCAL_AI_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Scam Message Investigator",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Scam Message Investigator")

st.write(
    "An AI-based tool to examine suspicious SMS, emails, "
    "job advertisements and online messages."
)

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = None

if API_KEY:
    st.info("AI analysis is running through the hosted API.")
else:
    st.info("AI analysis is using the local Gemma model.")

user_input = st.text_area(
    "Enter a message for checking:",
    placeholder="Paste a suspicious message here...",
    height=180
)

# Instructions for the AI model
PROMPT = """
You are an AI Scam Message Investigator.

Examine the given message and provide the result ONLY in valid JSON.

Follow this JSON format:

{
  "concern_level": "Low Concern, Medium Concern, or High Concern",
  "message_type": "SMS, Email, Job Offer, or Other",
  "summary": "Brief explanation of the message",
  "warning_signs": ["Warning sign 1"],
  "recommended_actions": ["Recommended action 1"],
  "limitations": ["Limitation 1"]
}

Analysis guidelines:
- Check for suspicious links and urgent requests.
- Look for OTP, password and money-related requests.
- Identify requests for private or personal details.
- Give reasons based on the actual message.
- Do not label every unknown message as a scam.
- Do not guarantee that any message is completely safe.
- Return only JSON without additional text.
"""


def check_scam(text):

    chat_messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": text}
    ]

    # Use Groq when an API key is available
    if API_KEY:

        result = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": chat_messages,
                "response_format": {"type": "json_object"}
            },
            timeout=120
        )

        result.raise_for_status()

        ai_result = result.json()["choices"][0]["message"]["content"]

    # Otherwise, use the local Gemma model
    else:

        result = requests.post(
            LOCAL_AI_URL,
            json={
                "model": MODEL_NAME,
                "messages": chat_messages,
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        result.raise_for_status()

        ai_result = result.json()["message"]["content"]

    # Convert AI response into a Python dictionary
    report = json.loads(ai_result)

    # Check whether all required details are present
    required_keys = [
        "concern_level",
        "message_type",
        "summary",
        "warning_signs",
        "recommended_actions",
        "limitations"
    ]

    for key in required_keys:
        if key not in report:
            raise ValueError("Required information is missing: " + key)

    if report["concern_level"] not in [
        "Low Concern",
        "Medium Concern",
        "High Concern"
    ]:
        raise ValueError("The AI returned an invalid concern level.")

    return report


# Analyze button
if st.button("🔍 Analyze Message", type="primary"):

    if not user_input.strip():
        st.warning("Please enter a message before starting the analysis.")

    else:
        try:
            with st.spinner("Please wait... AI is checking the message."):

                result = check_scam(user_input)

            st.success("Message analysis completed!")

            st.subheader("Scam Investigation Report")

            level = result["concern_level"]

            if level == "High Concern":
                st.error("🚨 " + level)

            elif level == "Medium Concern":
                st.warning("⚠️ " + level)

            else:
                st.success("✅ " + level)

            st.write("**Message Category:**", result["message_type"])

            st.subheader("Message Summary")
            st.write(result["summary"])

            st.subheader("Identified Warning Signs")
            for item in result["warning_signs"]:
                st.write("⚠️", item)

            st.subheader("Suggested Safety Actions")
            for item in result["recommended_actions"]:
                st.write("✔️", item)

            st.subheader("Analysis Limitations")
            for item in result["limitations"]:
                st.write("•", item)

            # Display complete report
            with st.expander("View Complete JSON Output"):
                st.json(result)

        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the AI service. Please check the service connection.")

        except requests.exceptions.Timeout:
            st.error("The AI service took too long to respond. Try again.")

        except requests.exceptions.HTTPError as error:
            st.error("API request failed: " + str(error))

        except (json.JSONDecodeError, KeyError, ValueError) as error:
            st.error("Unable to process the AI response: " + str(error))

        except Exception as error:
            st.error("An unexpected problem occurred: " + str(error))


# Footer information
st.divider()

st.caption(
    "Scam Message Investigator | Python, Streamlit, "
    "Ollama, Gemma 3 1B and Groq API"
)

st.caption(
    "AI predictions may not always be accurate. "
    "Confirm suspicious messages using official sources. "
    "Never share your real OTP, password or PIN."
)
