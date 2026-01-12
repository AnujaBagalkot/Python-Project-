import requests
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_location(location, business_type):
    # Geocode
    try:
        geo_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": location, "format": "json", "limit": 1}
        headers = {"User-Agent": "Portfolio/1.0"}
        
        response = requests.get(geo_url, params=params, headers=headers, timeout=10)
        if not response.json():
            return {"error": "Location not found"}
        
        data = response.json()[0]
        lat, lon = data['lat'], data['lon']
        
        # Get competitors
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f'[out:json];(node["amenity"="{business_type}"](around:1000,{lat},{lon}););out body;'
        
        comp_response = requests.post(overpass_url, data={"data": query}, timeout=30)
        competitors = comp_response.json().get('elements', [])[:5]
        
        comp_count = len(competitors)
        density = round(comp_count / 3.14, 2)
        
        # LLM analysis
        comp_list = "\n".join([f"- {c.get('tags', {}).get('name', 'Unnamed')}" for c in competitors])
        if not comp_list:
            comp_list = "No competitors found"
        
        prompt = f"""Analyze this location:
Location: {location}
Business: {business_type}
Competitors: {comp_count}
Density: {density} per km²

Nearby:
{comp_list}

Provide brief analysis (100 words):
1. Competition level
2. Market opportunity
3. 2 marketing strategies"""

        llm_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=250
        )
        
        analysis = llm_response.choices[0].message.content
        
        return {
            "competitors": comp_count,
            "density": density,
            "analysis": analysis,
            "competitor_list": [c.get('tags', {}).get('name', 'Unnamed') for c in competitors]
        }
        
    except Exception as e:
        return {"error": str(e)}