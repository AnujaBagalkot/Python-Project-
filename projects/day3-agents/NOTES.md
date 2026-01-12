# Development Notes - Location Intelligence Agent

## Oct 8, 2025

### Project Goal
Build an AI agent that analyzes business locations and provides competitive intelligence + marketing strategy. 


### Technical Decisions

**API Choice: OpenStreetMap vs Google Places**
- Initially planned Google Places but hit billing requirement
- Switched to OpenStreetMap (Nominatim + Overpass API)
- Benefits: Free, no auth needed, good enough data
- Tradeoff: Less business detail than Google but acceptable for POC

**Architecture: Class-based vs Functional**
- Used classes (LocationAnalyzer, MarketingAgent) instead of standalone functions
- Reason: Better separation of concerns, easier to test, more professional
- Makes code modular - can swap different analyzers later

**LLM Usage**
- Two separate LLM calls: market analysis + campaign strategy
- Could combine into one but separate gives better focused prompts
- Temperature 0.5 for analysis (factual), 0.7 for strategy (creative)

### Challenges Faced

**Problem 1: API Rate Limits**
- OpenStreetMap has usage limits
- Solution: Added timeouts, limited results to 10 competitors
- Future: Add caching for repeated queries

**Problem 2: Business Type Mapping**
- User might say "coffee shop" but OSM uses "cafe"
- Created type_mapping dict for common variations
- Still needs expansion for more business types

**Problem 3: Empty Results**
- Some areas have no competitors in OSM
- Handled gracefully with "No competitors found"
- Agent treats this as low competition opportunity

**Problem 4: Geocoding Accuracy**
- Generic locations like "Mumbai" give city center coords
- Better with specific areas like "Andheri Mumbai"
- Added user guidance in prompts

### Key Features

**1. Competition Density Metric**
- Calculates competitors per km²
- Gives objective measure beyond just count
- Helps quantify market saturation

**2. Multi-Step Analysis**
- Geocode → Fetch → Analyze → Strategize
- Shows agent orchestration capability
- Each step builds on previous

**3. Structured Reports**
- Professional formatting
- Actionable next steps
- Timestamp and metadata
- Saves to file for reference

**4. Pricing Recommendations**
- Based on competition level
- Simple but practical logic
- Could expand with actual price data

### What I Learned

**About APIs:**
- Free APIs exist but have constraints
- Always need fallback handling
- User-agent headers matter for some APIs

**About LLM Agents:**
- Breaking tasks into steps improves quality
- Context matters - giving LLM competition data helps
- Temperature tuning makes big difference

**About Production Code:**
- Error handling everywhere
- Input validation critical
- Timeouts prevent hanging
- Classes make code maintainable

### If I Had More Time

**Improvements needed:**
- [ ] Add caching layer (Redis or simple dict)
- [ ] Batch process multiple locations
- [ ] Integrate real foot traffic data
- [ ] Add seasonal analysis (peak times)
- [ ] Competitor pricing scraping
- [ ] Visual map output
- [ ] API key for higher limits
- [ ] Database to track historical data

**Advanced Features:**
- [ ] ML model to predict business success
- [ ] Sentiment analysis of competitor reviews
- [ ] Demographic data integration
- [ ] A/B test recommendation based on location
- [ ] Budget optimization across locations

### Business Value

For a company like GroundTruth:
- Automates competitive research (saves hours)
- Data-driven campaign planning
- Location-specific insights at scale
- Measurable market opportunity assessment

Could be part of:
- Campaign planning tool for clients
- Location selection for new stores
- Ad budget allocation system
- Performance prediction model

### Resources Used
- OpenStreetMap Nominatim API docs
- Overpass API query language
- LangChain concepts (didn't use library, understood principles)
- Marketing best practices research

### Mistakes & Fixes

**Mistake 1:** Tried to fetch too much data initially (100 competitors)
**Fix:** Limited to 10, much faster response

**Mistake 2:** Single LLM call for everything - too generic
**Fix:** Split into focused calls - better results

**Mistake 3:** Didn't handle location not found
**Fix:** Added validation and clear error messages

### Code Quality Notes

**What I focused on:**
- Descriptive variable names (not x, y, z)
- Docstrings for every function
- Error messages that actually help
- Comments only where logic isn't obvious
- Consistent formatting

**What makes it production-ready:**
- Exception handling everywhere
- Timeout limits on API calls
- Input validation
- Structured output format
- Logging-ready (print statements could become logs)

### Testing Approach

Tested with:
- Mumbai (high density area)
- Small town names (low competition)
- Misspelled locations (error handling)
- Different business types
- API failures (disconnect wifi)

All scenarios handled gracefully.

---

**Time spent:** ~3 hours (including research + debugging)
**Lines of code:** ~300
**API calls per run:** 2-3 (geocode + overpass + LLM)
**Cost:** ₹0