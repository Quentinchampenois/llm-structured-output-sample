# Spam Detection with Large Language Models

This Python script utilizes a Large Language Model (LLM) to classify messages as either "SPAM" or "NOT_SPAM". It provides a simple interactive interface to test the model's capabilities.

## Installation

1.  **Install OpenAI Python Library:**

    ```bash
    uv sync
    ```

## Prerequisites

*   **OpenAI API Key:**  You'll need an OpenAI API key to run this script. Obtain one from [https://platform.openai.com/](https://platform.openai.com/).
*   **Environment Variables:**  Set the following environment variables:
    *   `CLOUD_MODEL_NAME`: The name of the LLM to use (default: `llama-3.1-8b-instruct`).
    *   `CLOUD_BASE_URL`: The base URL of the OpenAI API endpoint.
    *   `CLOUD_API_KEY`: Your OpenAI API key.

    You can set these environment variables in your terminal before running the script, or in your `.bashrc` or equivalent configuration file.

## Usage

1.  **Run the script:**

    ```bash
    uv run --env-file .env main.py
    ```

2.  **Interactive Input:** The script will prompt you to enter a message. You can:

    *   Type your own message to be analyzed.
    *   Enter "1" to use the sample spam message: `Buy V-Bucks for free at http://perdu.com !`
    *   Enter "2" to use the sample non-spam message: `More trees in our streets !`

3.  **Output:**  The script will print the classification result (either "SPAM" or "NOT_SPAM") based on the message you provided.

## Code Description

*   **`SpamDetection` Class:**  This Pydantic model defines the structure of the output data from the LLM. It has one field, `spam`, which must be either "SPAM" or "NOT_SPAM".
*   **`send_for_analysis(msg)` Function:**
    *   Takes a message (`msg`) as input.
    *   Uses the OpenAI API to send the message to the LLM.
    *   Parses the LLM's response (which is expected to be in JSON format) and returns it as a Python dictionary.
*   **`main()` Function:**
    *   Prints an introductory message and a list of sample messages.
    *   Takes user input to determine which message to send to the LLM.
    *   Calls the `send_for_analysis()` function to get the classification result.
    *   Prints the classification result to the console.

## Configuration

*   **`MODEL`**:  The LLM to use. Defaults to `llama-3.1-8b-instruct`.  You can override this by setting the `CLOUD_MODEL_NAME` environment variable.

## Example

If you enter "1" (the spam message), the output will be:
`SPAM`

## Resources

* [Scaleway Generative API](https://www.scaleway.com/en/docs/generative-apis/)
* [Pydantic doc](https://docs.pydantic.dev/2.11/)
* [uv repository](https://github.com/astral-sh/uv)
* 