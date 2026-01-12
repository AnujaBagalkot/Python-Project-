"""
Location Intelligence Agent
Analyzes business locations for competitive insights and marketing strategy
Author: Kunal - Oct 2025
"""

import os
import requests
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Note: Using Groq instead of OpenAI for cost efficiency during development

class LocationAnalyzer:
    """Handles location data fetching and analysis"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        
    def geocode_location(self, location):
        """Convert location name to coordinates"""
        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }
        headers = {"User-Agent": "LocationIntelligence/1.0"}
        
        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                return float(data['lat']), float(data['lon'])
            return None, None
        except Exception as e:
            print(f"Geocoding failed: {e}")
            return None, None
    
    def fetch_competitors(self, lat, lon, business_type, radius=1000):
        """Get nearby competitors using Overpass API"""
        
        # Map common types to OSM tags
        type_mapping = {
            "restaurant": "restaurant",
            "cafe": "cafe", 
            "gym": "gym",
            "shop": "shop",
            "store": "shop"
        }
        
        osm_type = type_mapping.get(business_type.lower(), business_type.lower())
        
        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="{osm_type}"](around:{radius},{lat},{lon});
          way["amenity"="{osm_type}"](around:{radius},{lat},{lon});
        );
        out body;
        """
        
        try:
            response = requests.post(self.overpass_url, data={"data": query}, timeout=30)
            if response.status_code == 200:
                elements = response.json().get('elements', [])
                
                # Extract useful info
                competitors = []
                for elem in elements[:10]:  # Limit to 10
                    tags = elem.get('tags', {})
                    competitors.append({
                        'name': tags.get('name', 'Unnamed Business'),
                        'type': tags.get('amenity', 'N/A'),
                        'address': tags.get('addr:street', 'Address unknown')
                    })
                
                return competitors
            return []
        except Exception as e:
            print(f"Competitor search failed: {e}")
            return []
    
    def calculate_competition_density(self, competitors_count, radius):
        """Calculate competition per sq km"""
        area_km2 = (3.14159 * (radius/1000)**2)
        density = competitors_count / area_km2 if area_km2 > 0 else 0
        return round(density, 2)


class MarketingAgent:
    """AI agent for marketing insights and strategy"""
    
    def __init__(self, client):
        self.client = client
        
    def analyze_market(self, location, business_type, competitors, density):
        """Generate market analysis using LLM"""
        
        comp_list = "\n".join([f"- {c['name']}" for c in competitors[:5]])
        if not comp_list:
            comp_list = "No direct competitors detected"
        
        competition_level = "High" if density > 5 else "Medium" if density > 2 else "Low"
        
        prompt = f"""Analyze this business location as a marketing strategist:

Location: {location}
Business: {business_type}
Competition Density: {density} per km² ({competition_level})
Nearby Competitors:
{comp_list}

Provide analysis covering:
1. Market saturation level
2. Key opportunity areas
3. Competitive advantages to leverage
4. Risk factors

Keep response under 120 words, specific and actionable."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=250
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Analysis unavailable: {e}"
    
    def generate_campaign_strategy(self, location, business_type, analysis):
        """Create targeted advertising campaign plan"""
        
        prompt = f"""Create a practical ad campaign strategy:

Business: {business_type} in {location}
Market Context: {analysis}

Provide:
1. Top 3 advertising channels with rationale
2. Primary target segments (be specific)
3. Core messaging themes
4. Budget split recommendation

Max 100 words, focus on ROI."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Strategy generation failed: {e}"
    
    def suggest_pricing_strategy(self, competitors_count, competition_level):
        """Suggest pricing approach based on competition"""
        
        if competition_level == "High":
            return "Premium positioning or value-based differentiation recommended"
        elif competition_level == "Medium":
            return "Competitive pricing with quality emphasis"
        else:
            return "Market-leader pricing possible with strong branding"


def generate_report(location, business_type, competitors, density, analysis, strategy, pricing):
    """Create formatted report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"""
{'='*75}
LOCATION INTELLIGENCE REPORT
{'='*75}

Generated: {timestamp}
Location: {location}
Business Type: {business_type}

{'='*75}
COMPETITIVE LANDSCAPE
{'='*75}

Total Competitors Found: {len(competitors)}
Competition Density: {density} businesses per km²
Competition Level: {'High' if density > 5 else 'Medium' if density > 2 else 'Low'}

Top Competitors:
"""
    
    for i, comp in enumerate(competitors[:5], 1):
        report += f"  {i}. {comp['name']} - {comp['address']}\n"
    
    if not competitors:
        report += "  No direct competitors identified (opportunity for first-mover advantage)\n"
    
    report += f"""
{'='*75}
MARKET ANALYSIS
{'='*75}

{analysis}

{'='*75}
ADVERTISING STRATEGY
{'='*75}

{strategy}

{'='*75}
PRICING RECOMMENDATION
{'='*75}

{pricing}

{'='*75}
NEXT STEPS
{'='*75}

1. Conduct customer surveys in the area
2. Analyze foot traffic patterns (if available)
3. Test messaging with small ad budget
4. Monitor competitor pricing and promotions
5. Build local partnerships for co-marketing

{'='*75}
"""
    
    return report


def main():
    print("\n" + "="*75)
    print("LOCATION INTELLIGENCE AGENT")
    print("Competitive analysis and marketing strategy for local businesses")
    print("="*75)
    
    # User inputs
    location = input("\nLocation (city/area): ").strip()
    business_type = input("Business type: ").strip()
    
    if not location or not business_type:
        print("Error: Please provide both location and business type")
        return
    
    # Initialize components
    analyzer = LocationAnalyzer()
    agent = MarketingAgent(client)
    
    # Step 1: Geocode
    print(f"\nAnalyzing location: {location}...")
    lat, lon = analyzer.geocode_location(location)
    
    if not lat or not lon:
        print("Could not find location. Try different name or check spelling.")
        return
    
    print(f"Coordinates: {lat}, {lon}")
    
    # Step 2: Find competitors
    print(f"\nSearching for {business_type} competitors within 1km...")
    competitors = analyzer.fetch_competitors(lat, lon, business_type)
    density = analyzer.calculate_competition_density(len(competitors), 1000)
    
    print(f"Found {len(competitors)} competitors")
    print(f"Density: {density} per km²")
    
    # Step 3: Market analysis
    print("\nGenerating market analysis...")
    analysis = agent.analyze_market(location, business_type, competitors, density)
    
    # Step 4: Campaign strategy
    print("Creating advertising strategy...")
    strategy = agent.generate_campaign_strategy(location, business_type, analysis)
    
    # Step 5: Pricing suggestion
    comp_level = "High" if density > 5 else "Medium" if density > 2 else "Low"
    pricing = agent.suggest_pricing_strategy(len(competitors), comp_level)
    
    # Generate and save report
    report = generate_report(location, business_type, competitors, density, 
                            analysis, strategy, pricing)
    
    print("\n" + report)
    
    # Save to file
    filename = f"location_intel_{location.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved: {filename}")
    print("="*75)


if __name__ == "__main__":
    main()