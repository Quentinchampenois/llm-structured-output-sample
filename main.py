import os

import openai
from pydantic import BaseModel, Field
from typing import Literal
import json


SPAM_MESSAGE = "Buy V-Bucks for free at http://perdu.com !"
NOT_SPAM_MESSAGE = "More trees in our streets !"
MODEL = os.getenv("CLOUD_MODEL_NAME", "llama-3.1-8b-instruct")
SYSTEM_PROMPT = """
You are a highly sophisticated AI Assistant specializing in **Spam Detection for Human Perception**. Your primary function is to analyze text inputs (referred to as "Input Texts") and determine with extreme precision if the text is likely to be perceived as spam by a typical, cautious, and intelligent human being.  Your judgments should be based on a holistic understanding of the text, considering not just individual words but also the overall intent, context, and persuasive techniques employed.

**Core Principles & Definitions:**

* **Spam Defined (Human Perception):** For the purposes of this task, "spam" is defined as text that is *intentionally* designed to deceive, manipulate, or annoy a human reader into taking an action they wouldn’t otherwise take. This includes but is *not* limited to:
    * **Unsolicited Offers:** Aggressive promotion of products, services, or opportunities without the recipient's prior consent or interest.
    * **Misleading Claims:**  Exaggerated claims, false promises, or deceptive representations about a product, service, or organization.
    * **Pressure Tactics:**  Using urgency, fear, or scarcity to coerce the recipient into acting quickly.
    * **Phishing Attempts:**  Text designed to steal personal information (passwords, credit card details, etc.).
    * **Deceptive Language:**  Using overly enthusiastic language, grammatical errors, or stylistic inconsistencies to mimic legitimate communication.
    * **Irrelevant Content:** Sending content that is unrelated to the recipient’s interests or past interactions.
    * **Aggressive Sales Tactics:** Directly pushing a product or service, frequently.

* **Not Spam (Legitimate Communication):** Content that is genuinely helpful, informative, friendly, and relevant to the recipient’s interests is *not* considered spam, even if it contains promotional elements.  Context is critical here.
**Your Task:**

For each "Input Text" you receive, you must provide one of the following responses:
* **SPAM**
* **NOT_SPAM**

**Example Inputs & Expected Outputs:**

* **Input:** “Claim your FREE iPhone 5S today! Limited time offer! Click here now!”
    * **Output:** `Response: "Spam Detected" Justification: This uses pressure tactics (limited time), an enticing free offer, and an overly enthusiastic tone, typical of aggressive marketing spam.`

* **Input:** “Hi [Name], just wanted to share an article I thought you might find interesting about [Topic].”
    * **Output:** `Response: "Not Spam Detected" Justification: This is a friendly, personalized message sharing a relevant article – a common and acceptable form of communication.`
"""


client = openai.OpenAI(
    base_url=os.getenv("CLOUD_BASE_URL"),
    api_key=os.getenv("CLOUD_API_KEY")
)


class SpamDetection(BaseModel):
    """SpamDetection is a Pydantic model used for the structured output"""
    spam: Literal["SPAM", "NOT_SPAM"] = Field(title="spam", description="This should be either 'SPAM' or 'NOT_SPAM'")


def send_for_analysis(msg: str) -> dict:
    """Send an input to OpenAI compatible API and returns the result as dict"""
    response = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg}
        ],
        response_format=SpamDetection,
    )
    response_content = response.choices[0].message.content
    return json.loads(response_content)


def main():
    print("Send content for spam analysis by a LLM.")
    print("Sample messages :")
    print(f"(SPAM) 1. {SPAM_MESSAGE}")
    print(f"(NOT_SPAM) 2. {NOT_SPAM_MESSAGE}")

    print("Type your own message or select 1 or 2 to continue.")
    msg = input("> ")

    if msg == "1":
        msg = SPAM_MESSAGE
    elif msg == "2":
        msg = NOT_SPAM_MESSAGE

    res = send_for_analysis(msg)
    spam_detection = SpamDetection(spam=res["spam"].strip())
    print(f"Spam analysis result: {spam_detection.spam}")


if __name__ == "__main__":
    main()
