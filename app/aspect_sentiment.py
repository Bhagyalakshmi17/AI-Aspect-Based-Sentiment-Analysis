from transformers import pipeline
import re

# Load sentiment analysis model
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text):
    """
    Analyze the sentiment of a piece of text.
    Returns the sentiment label and confidence score.
    """
    result = sentiment_analyzer(text)[0]

    return {
        "sentiment": result["label"],
        "confidence": round(result["score"] * 100, 2)
    }

# Common product/service aspects
ASPECTS = [
    "battery",
    "battery life",
    "camera",
    "camera quality",
    "screen",
    "display",
    "performance",
    "price",
    "design",
    "quality",
    "service",
    "delivery",
    "sound",
    "software"
]


def extract_aspects(text):
    """
    Extract known aspects mentioned in the input text
    and remove overlapping duplicate aspects.
    """
    text_lower = text.lower()

    found_aspects = []

    # Check longer aspects first
    sorted_aspects = sorted(ASPECTS, key=len, reverse=True)

    for aspect in sorted_aspects:
        if aspect in text_lower:
            # Avoid adding a shorter aspect if it is
            # already contained in a longer aspect
            if not any(aspect in existing for existing in found_aspects):
                found_aspects.append(aspect)

    return found_aspects

def analyze_aspects(text):
    """
    Analyze sentiment separately for each aspect.
    """

    results = []

    # Split the review into individual clauses
    parts = re.split(
        r'\s*(?:,|\bbut\b|\bhowever\b|\band\b)\s*',
        text
    )

    for part in parts:
        part = part.strip()

        if not part:
            continue

        # Find aspects in this clause
        aspects = extract_aspects(part)

        if not aspects:
            continue

        # Analyze only this clause
        sentiment_result = analyze_sentiment(part)

        for aspect in aspects:
            results.append({
                "aspect": aspect,
                "sentiment": sentiment_result["sentiment"],
                "confidence": sentiment_result["confidence"]
            })

    return results