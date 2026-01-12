import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_ads(business, location, audience):
    """Generate ad copies using LLM"""
    
    prompt = f"""Create 3 ad copy variations for:
Business: {business}
Location: {location}
Target Audience: {audience}

Requirements:
- 50-70 words each
- Strong call-to-action
- Mention location
- Number each (1, 2, 3)

Provide only the 3 ad copies."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"