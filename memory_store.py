import json, uuid, os, re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher

MEMORY_FILE = "data/issue_memory.json"
stemmer = PorterStemmer()

# Optional: You can expand this dictionary
SYNONYMS = {
    "create": "add",
    "return": "retrieve",
    "fetch": "retrieve",
    "store": "save",
    "delete": "remove",
    "add": "create",
    "get": "retrieve"
}

def normalize_tokens(text):
    tokens = word_tokenize(text.lower())
    stems = []
    for token in tokens:
        norm = SYNONYMS.get(token, token)
        stems.append(stemmer.stem(norm))
    return set(stems)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE) as f:
        return json.load(f)

def save_to_memory(issue, solution, source="User", category="General", feedback="Pending"):
    data = load_memory()
    data.append({
        "id": str(uuid.uuid4()),
        "issue": issue,
        "solution": solution,
        "category": category,
        "source": source,
        "feedback": feedback
    })
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def fuzzy_score(a, b):
    return SequenceMatcher(None, a, b).ratio()

def search_memory(query, category=None, threshold=0.75):
    data = load_memory()
    query_lower = query.lower()
    results = []

    for item in data:
        issue_text = item.get("issue", "").lower()
        ratio = SequenceMatcher(None, query_lower, issue_text).ratio()

        category_match = category is None or item.get("category", "").lower() == category.lower()

        if ratio >= threshold and category_match:
            results.append(item)

    return results
