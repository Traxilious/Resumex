import re
from collections import Counter

# Overused cliché/buzzword dictionary commonly found in templates
OVERUSED_BUZZWORDS = [
    "spearheaded", "synergy", "paradigm shift", "game-changer", "thought leader",
    "leverage", "results-driven", "detail-oriented", "hardworking", "team player",
    "out-of-the-box", "passionate professional", "dynamic leader", "proven track record",
    "strategic thinker", "visionary", "deep dive", "seamless integration", "cutting-edge"
]

def analyze_authenticity_score(text):
    """
    Analyzes resume text for generic buzzword density, sentence structure uniformity,
    and vocabulary variance.
    Returns a dictionary containing risk_level, score (100% = authentic), and color code.
    """
    if not text or len(text.strip()) == 0:
        return {
            "ai_percentage": 98,
            "risk_level": "Natural Phrasing",
            "color": "emerald",
            "buzzword_matches": []
        }

    text_lower = text.lower()

    # 1. Check Buzzword Density
    found_buzzwords = []
    for word in OVERUSED_BUZZWORDS:
        matches = len(re.findall(r'\b' + re.escape(word) + r'\b', text_lower))
        if matches > 0:
            found_buzzwords.append({"word": word, "count": matches})

    total_buzzwords = sum(item["count"] for item in found_buzzwords)

    # 2. Vocabulary Variety Ratio (Unique words / Total words)
    words = re.findall(r'\b\w+\b', text_lower)
    total_words = len(words)
    unique_words = len(set(words))
    vocab_ratio = (unique_words / total_words) if total_words > 0 else 1.0

    # 3. Sentence Length Uniformity
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 5]
    sentence_lengths = [len(s.split()) for s in sentences]
    
    uniformity_penalty = 0
    if len(sentence_lengths) > 3:
        avg_len = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((x - avg_len) ** 2 for x in sentence_lengths) / len(sentence_lengths)
        if variance < 15:
            uniformity_penalty = 15

    # Calculate raw pattern risk %
    buzzword_score = min(total_buzzwords * 8, 35)
    vocab_penalty = max(0, int((0.55 - vocab_ratio) * 100)) if vocab_ratio < 0.55 else 0

    risk_percentage = min(buzzword_score + vocab_penalty + uniformity_penalty, 90)
    authenticity_score = 100 - risk_percentage

    if authenticity_score >= 75:
        risk_level = "Natural Phrasing"
        color = "emerald"
    elif authenticity_score >= 50:
        risk_level = "Moderate Cliché Density"
        color = "amber"
    else:
        risk_level = "High Buzzword Density"
        color = "rose"

    return {
        "ai_percentage": authenticity_score, # Return Authenticity % (95-98% for natural resumes)
        "risk_level": risk_level,
        "color": color,
        "buzzword_matches": found_buzzwords
    }
