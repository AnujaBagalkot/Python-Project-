# Development Notes - Ad Copy Generator

## Day 2 - October 8, 2025

### Initial Build
Started with basic LLM integration using Groq API. Chose Groq over OpenAI because:
- Free tier with good limits
- Fast inference
- Good for learning

### Challenges Faced

**Problem 1: API Key Management**
- Initially hardcoded API key (bad practice)
- Fixed by using python-dotenv
- Learned about environment variables

**Problem 2: Generic Output**
- First version just generated ads without analysis
- Added quality scoring to make it business-relevant

**Problem 3: Prompt Engineering**
- Temperature too high (1.0) = inconsistent results
- Settled on 0.7 for good balance

### Features Added

1. **Estimated Reach Calculator**
   - Basic logic for now
   - TODO: Integrate real location API (Google Places?)

2. **Ad Quality Scoring System**
   - Checks for CTA, urgency, length, emotion
   - Gives 0-100 score with feedback
   - Helps users understand what makes good ads

### What I Learned
- LLM APIs are surprisingly simple to use
- Prompt engineering matters more than I thought
- Business context > just technical implementation
- GroundTruth would care about reach + quality metrics

### Next Improvements
- [ ] Add A/B testing suggestions
- [ ] Compare multiple ad variations automatically
- [ ] Add competitor analysis
- [ ] Integrate real location data APIs
- [ ] Add cost estimation per campaign

### Resources Used
- Groq API Documentation
- LangChain basics (for future projects)
- Prompt engineering guides

---

**Time spent:** ~2 hours (including learning + debugging)