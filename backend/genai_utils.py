import os
import pandas as pd
from google import generativeai as genai

# Configure API key using GOOGLE_API_KEY environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'realestate.csv')
DATAFRAME = pd.read_csv(CSV_PATH)


def ask_genai(message: str) -> str:
    """Send a question to the generative model with csv context."""
    if not message:
        return ""

    context = DATAFRAME.to_csv(index=False)
    prompt = (
        "You are an assistant that answers questions about the following real estate data.\n"
        f"{context}\n"
        f"Question: {message}"
    )

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()
