import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def classification(name: str, company: str):

    prompt = f"""
    You are a CRM AI assistant.

    Analyze this lead and classify as:
    hot, warm, or cold.

    Lead Name: {name}
    Company: {company}

    Return ONLY one of these values:
    hot
    warm
    cold
    
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip().lower()