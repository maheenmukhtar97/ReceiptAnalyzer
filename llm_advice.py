import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)

def generate_advice(category_totals, percentages, total_spending):

    prompt = f"""
    Here is a user's spending breakdown:

    Total Spending: ${total_spending}

    Category Totals:
    {category_totals.to_string()}

    Percentage Breakdown:
    {percentages.to_string()}

    Provide personalized budgeting advice.
    Highlight overspending.
    Suggest saving strategies.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
