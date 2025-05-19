# Define the 7 categories and their color codes
CATEGORIES = ["Sports", "Politics & Policy", "Economy & Finance", "Tech & Innovation", "Culture & Celebrities", "Crisis & War", "Religion & Holidays"]

def categorize_event(title, description):
    # Simple keyword-based categorization
    title = title.lower() + " " + description.lower()
    if "nba" in title or "nfl" in title or "mlb" in title:
        return "Sports"
    elif "election" in title or "senate" in title:
        return "Politics & Policy"
    elif "fed" in title or "gdp" in title or "cpi" in title:
        return "Economy & Finance"
    elif "apple" in title or "wwdc" in title:
        return "Tech & Innovation"
    elif "oscars" in title or "academy" in title:
        return "Culture & Celebrities"
    elif "war" in title or "peace" in title:
        return "Crisis & War"
    elif "pope" in title or "christmas" in title:
        return "Religion & Holidays"
    else:
        return "Other"

# Keywords for categorization
CATEGORY_KEYWORDS = {
    "Sports": [
        "nfl", "football", "basketball", "nba", "baseball", "mlb", "soccer", "hockey", "nhl", 
        "tennis", "golf", "olympic", "world cup", "super bowl", "championship", "game", 
        "match", "race", "tournament", "team", "player", "coach", "athlete"
    ],
    "Politics & Policy": [
        "president", "election", "vote", "congress", "senate", "house", "democrat", "republican", 
        "policy", "bill", "law", "government", "administration", "campaign", "candidate", 
        "political", "prime minister", "parliament", "legislation", "supreme court", "cabinet"
    ],
    "Economy & Finance": [
        "fed", "federal reserve", "interest rate", "inflation", "stock", "market", "economy", 
        "gdp", "economic", "recession", "financial", "bank", "dollar", "euro", "yuan", "currency", 
        "crypto", "bitcoin", "ethereum", "investment", "debt", "treasury", "unemployment"
    ],
    "Crisis & War": [
        "war", "conflict", "military", "attack", "terrorist", "terrorism", "invasion", "troops", 
        "battle", "defense", "weapon", "missile", "bomb", "disaster", "emergency", "crisis", 
        "earthquake", "hurricane", "flood", "outbreak", "pandemic", "hostage", "refugee"
    ],
    "Culture & Celebrities": [
        "movie", "film", "actor", "actress", "singer", "celebrity", "award", "oscar", "grammy", 
        "album", "concert", "performance", "hollywood", "tv", "television", "show", "series", 
        "music", "festival", "celebrity", "star", "famous", "entertainment", "media"
    ],
    "Tech & Innovation": [
        "tech", "technology", "ai", "artificial intelligence", "software", "app", "startup", 
        "innovation", "digital", "internet", "web", "online", "cyber", "computer", "mobile", 
        "smartphone", "device", "product", "launch", "release", "update", "silicon valley", 
        "google", "apple", "microsoft", "facebook", "meta", "amazon", "tesla"
    ],
    "Religion & Holidays": [
        "christmas", "easter", "ramadan", "eid", "diwali", "hanukkah", "religious", "holiday", 
        "festival", "celebration", "pope", "vatican", "church", "mosque", "temple", "prayer", 
        "worship", "faith", "spiritual", "holy", "sacred", "thanksgiving", "new year"
    ]
}

def categorize_event(title, description=""):
    """
    Categorize an event based on its title and description
    Returns the most likely category
    """
    # Combine title and description for better categorization
    text = (title + " " + description).lower()
    
    # Count keywords for each category
    category_scores = {category: 0 for category in CATEGORIES}
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                category_scores[category] += 1
    
    # Find category with highest score
    max_score = 0
    best_category = list(CATEGORIES.keys())[0]  # Default to first category
    
    for category, score in category_scores.items():
        if score > max_score:
            max_score = score
            best_category = category
    
    # If no clear match, try some heuristics
    if max_score == 0:
        # Finance-related terms
        if any(term in text for term in ["price", "market", "trading", "investment", "fund", "stock"]):
            return "Economy & Finance"
        
        # Default to Politics if unclear
        return "Politics & Policy"
    
    return best_category

def get_category_examples(category):
    """Return examples of events for each category"""
    examples = {
        "Sports": [
            "Super Bowl LVIII",
            "NBA Finals Game 7",
            "FIFA World Cup Final",
            "Tokyo Olympics Opening Ceremony",
            "Wimbledon Men's Final"
        ],
        "Politics & Policy": [
            "US Presidential Election",
            "State of the Union Address",
            "UK Parliamentary Elections",
            "UN General Assembly Meeting",
            "Presidential Debate"
        ],
        "Economy & Finance": [
            "Federal Reserve Interest Rate Decision",
            "Jerome Powell Speech",
            "US Jobs Report Release",
            "Quarterly GDP Announcement",
            "Annual Budget Announcement"
        ],
        "Crisis & War": [
            "UN Security Council Emergency Meeting",
            "Peace Treaty Signing Ceremony",
            "Climate Change Summit",
            "International Aid Conference",
            "Evacuation Deadline"
        ],
        "Culture & Celebrities": [
            "Academy Awards Ceremony",
            "Grammy Awards",
            "Met Gala",
            "Major Movie Premiere",
            "Music Festival Headliner Performance"
        ],
        "Tech & Innovation": [
            "Apple iPhone Launch Event",
            "Google I/O Developer Conference",
            "SpaceX Rocket Launch",
            "CES Technology Exhibition",
            "Major Software Release"
        ],
        "Religion & Holidays": [
            "Christmas Day",
            "Easter Sunday",
            "Start of Ramadan",
            "Diwali Festival",
            "Thanksgiving Day"
        ]
    }
    
    return examples.get(category, ["No examples available"])
