import os

import openai
from pydantic import BaseModel, Field
from typing import Literal
import json


SPAM_MESSAGE = "Buy V-Bucks for free at http://perdu.com !"
NOT_SPAM_MESSAGE = "More trees in our streets !"
MODEL = os.getenv("CLOUD_MODEL_NAME", "llama-3.1-8b-instruct")

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
            {"role": "system", "content": "You are a helpful assistant designed to output structured data."},
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
