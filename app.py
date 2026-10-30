import streamlit as st
import requests
import json

# Application Configuration
MODEL = "gemma3:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

# Page Configuration
st.set_page_config(
    page_title="Scam Message Investigator",
    page_icon="🔍",
    layout="centered"
)

# Application Title
st.title("🔍 Scam Message Investigator")
st.write(
    "Analyze suspicious SMS messages, emails, job offers "
    "and online messages using a local AI model."
)

st.info("Your message is analyzed using Ollama and Gemma locally.")

# Function to investigate messages
def investigate_message(message):

    prompt = f"""
You are an expert scam message investigator.

Analyze the following message and return a JSON object.

Message:
{message}

Return ONLY valid JSON using this structure:

{{
    "concern_level": "Low Concern, Medium Concern, or High Concern",
    "message_type": "SMS, Email, Job Offer, or Other",
    "summary": "Brief explanation of the message",
    "warning_signs": [
        "Warning sign 1",
        "Warning sign 2"
    ],
    "recommended_actions": [
        "Safety action 1",
        "Safety action 2"
    ],
    "limitations": "Explain what cannot be verified"
}}

Use evidence from the message.
Do not assume that every message is a scam.
Do not treat a low concern result as proof of safety.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "format": "json"
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    ai_response = result["message"]["content"]

    report = json.loads(ai_response)

    return report


# User Input
st.subheader("📩 Enter Your Message")

message = st.text_area(
    "Paste the suspicious message here:",
    height=180,
    placeholder="Enter SMS, email, job offer or online message..."
)

# Investigation Button
if st.button("🔍 Investigate Message", use_container_width=True):

    if not message.strip():
        st.warning("Please enter a message before investigating.")

    else:
        with st.spinner("AI is analyzing your message..."):

            try:
                report = investigate_message(message)

                st.success("Investigation Completed!")

                # Display Concern Level
                st.subheader("📊 Investigation Report")

                concern = report.get(
                    "concern_level",
                    "Not available"
                )

                if concern == "High Concern":
                    st.error(f"🚨 {concern}")

                elif concern == "Medium Concern":
                    st.warning(f"⚠️ {concern}")

                else:
                    st.success(f"✅ {concern}")

                # Display Message Details
                st.write("**Message Type:**",
                         report.get("message_type", "Not available"))

                st.write("**Summary:**",
                         report.get("summary", "Not available"))

                # Warning Signs
                st.subheader("⚠️ Warning Signs")

                for sign in report.get("warning_signs", []):
                    st.write("•", sign)

                # Recommended Actions
                st.subheader("🛡️ Recommended Safety Actions")

                for action in report.get(
                    "recommended_actions", []
                ):
                    st.write("•", action)

                # Limitations
                st.subheader("ℹ️ Limitations")

                st.write(
                    report.get("limitations", "Not available")
                )

                # Download Report
                report_json = json.dumps(
                    report,
                    indent=4,
                    ensure_ascii=False
                )

                st.download_button(
                    label="⬇️ Download Investigation Report",
                    data=report_json,
                    file_name="scam_investigation_report.json",
                    mime="application/json"
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to Ollama. "
                    "Please make sure Ollama is running."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The AI model took too long to respond. "
                    "Please try again."
                )

            except requests.exceptions.RequestException as e:
                st.error(f"Ollama API Error: {e}")

            except (json.JSONDecodeError, KeyError, TypeError):
                st.error(
                    "Invalid AI response. Please try investigating again."
                )

            except Exception as e:
                st.error(f"Unexpected Error: {e}")


# Footer
st.divider()

st.caption(
    "Scam Message Investigator | Week 8 LLM Practical Project"
)

st.caption(
    "Disclaimer: AI-generated results are not a guarantee "
    "that a message is genuine or fraudulent. Always verify "
    "through official sources."
)