"""
Location-Based Ad Copy Generator
Generates targeted advertising copy using LLM based on business context
Author: Kunal
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_ad_copy(business_type, location, target_audience):
    """Generate targeted ad variations using LLM"""
    
    prompt = f"""You are an advertising copywriter. Create 3 ad copy variations for:

Business: {business_type}
Location: {location}
Target Audience: {target_audience}

Requirements:
- 50-70 words each
- Strong call-to-action
- Mention location naturally
- Engaging and persuasive
- Number each variation

Provide only the 3 ad copies."""
    
    print("Generating ad copies...")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating ads: {e}"


def calculate_estimated_reach(location):
    """Rough estimate of potential reach based on location"""
    # TODO: Integrate with real location data API
    major_cities = ["mumbai", "delhi", "bangalore", "pune", "hyderabad"]
    
    if any(city in location.lower() for city in major_cities):
        return "High (500K+ potential reach)"
    else:
        return "Medium (100K+ potential reach)"


def score_ad_quality(ad_text):
    """Score ad copy based on marketing best practices"""
    score = 0
    feedback = []
    
    # Check for call-to-action words
    cta_words = ["visit", "call", "book", "order", "try", "discover", "join", "get"]
    if any(word in ad_text.lower() for word in cta_words):
        score += 25
        feedback.append("+ Strong call-to-action")
    else:
        feedback.append("- Missing clear call-to-action")
    
    # Check for urgency
    urgency_words = ["today", "now", "limited", "exclusive", "offer"]
    if any(word in ad_text.lower() for word in urgency_words):
        score += 25
        feedback.append("+ Creates urgency")
    
    # Check length (50-70 words ideal)
    word_count = len(ad_text.split())
    if 50 <= word_count <= 70:
        score += 25
        feedback.append("+ Optimal length")
    elif word_count < 50:
        feedback.append("- Too short")
    else:
        feedback.append("- Too long")
    
    # Check for emotional words
    emotion_words = ["love", "amazing", "best", "perfect", "favorite", "trust"]
    if any(word in ad_text.lower() for word in emotion_words):
        score += 25
        feedback.append("+ Emotional appeal")
    
    return score, feedback

def main():
    print("\n" + "="*60)
    print("AD COPY GENERATOR - Location-Based Marketing")
    print("="*60)
    
    business_type = input("\nBusiness type: ")
    location = input("Location: ")
    target_audience = input("Target audience: ")
    
    # Generate ads
    print("\n" + "="*60)
    ads = generate_ad_copy(business_type, location, target_audience)
    
    print("\nGENERATED AD COPIES:\n")
    print(ads)
    
    # Analyze ad quality
    print("\n" + "-"*60)
    print("AD QUALITY ANALYSIS:")
    print("-"*60)
    
    # Score first ad
    ad_parts = ads.split('\n')
    first_ad = ""
    for line in ad_parts:
        if line.strip() and not line.strip().startswith('1.'):
            continue
        if line.strip().startswith('1.'):
            first_ad = line
            break
    
    if first_ad:
        score, feedback = score_ad_quality(first_ad)
        print(f"\nAd #1 Quality Score: {score}/100")
        for item in feedback:
            print(f"  {item}")
    
    # Show estimated reach
    reach = calculate_estimated_reach(location)
    print(f"\nEstimated Reach: {reach}")
    print("="*60)
    
    # Save results
    filename = f"ads_{business_type.replace(' ', '_').lower()}.txt"
    with open(filename, 'w') as f:
        f.write(f"Business: {business_type}\n")
        f.write(f"Location: {location}\n")
        f.write(f"Target Audience: {target_audience}\n")
        f.write(f"Estimated Reach: {reach}\n\n")
        f.write(ads)
    
    print(f"\nSaved to: {filename}")


if __name__ == "__main__":
    main()