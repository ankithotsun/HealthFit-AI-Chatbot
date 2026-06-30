"""
HealthFit AI Chatbot — Text Preprocessor

This module implements the complete text preprocessing
pipeline used before feeding user input into the TF-IDF
vectorizer and Logistic Regression classifier.

Pipeline Steps
--------------
1. Contraction expansion  — "can't" → "cannot"
2. Lowercase conversion   — "Hello" → "hello"
3. Punctuation removal    — "great!" → "great"
4. Tokenization           — split sentence into word tokens
5. Stopword removal       — remove "the", "is", "a", etc.
6. Lemmatization          — "running" → "run", "better" → "good"

Why Lemmatization over Stemming?
---------------------------------
Stemming is faster but crude — it chops word endings using
fixed rules, which can produce non-words (e.g., "running"
→ "runn"). Lemmatization uses a vocabulary and part-of-speech
analysis to return the actual base form of a word (the lemma),
resulting in cleaner, more interpretable features for the
TF-IDF vectorizer. For a relatively small intent dataset,
the slight speed difference is negligible.

Functions
---------
preprocess(text)
    Full pipeline: expand → lowercase → clean → tokenize
    → remove stopwords → lemmatize → rejoin.
expand_contractions(text)
    Replace common English contractions with full forms.
tokenize(text)
    Split text into a list of word tokens using NLTK.
remove_stopwords(tokens)
    Filter out English stopwords, preserving fitness-specific
    negation words such as 'not' and 'no'.
lemmatize(tokens)
    Return the base (lemma) form of each token.
"""

import re
import string
import logging

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from rapidfuzz import process, fuzz

logger = logging.getLogger(__name__)

# ============================================================
# NLTK Resource Management
# ============================================================
# These resources are downloaded once and cached locally.
# The download calls are idempotent — they skip if already
# present.
# ============================================================

def _ensure_nltk_resources() -> None:
    """Download required NLTK corpora if not already present.

    Checks for: punkt (tokenizer), punkt_tab (tokenizer),
    stopwords (stopword list), and wordnet (lemmatizer lexicon).
    """
    import os
    if "VERCEL" in os.environ:
        nltk_data_dir = "/tmp/nltk_data"
        os.makedirs(nltk_data_dir, exist_ok=True)
        if nltk_data_dir not in nltk.data.path:
            nltk.data.path.append(nltk_data_dir)
    else:
        nltk_data_dir = None

    resources = {
        "tokenizers/punkt": "punkt",
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4",
    }
    for path, package in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            if nltk_data_dir:
                nltk.download(package, download_dir=nltk_data_dir, quiet=True)
            else:
                nltk.download(package, quiet=True)


_ensure_nltk_resources()

# ============================================================
# Module-level Singletons
# ============================================================
# Instantiate once at import time to avoid repeated object
# creation on every call — important for response latency.

_lemmatizer = WordNetLemmatizer()

# English stopwords — but we preserve negation words because
# "not tired" and "tired" have opposite meanings that the
# classifier should differentiate.
_STOP_WORDS = stopwords.words("english")
_NEGATION_WORDS = {"not", "no", "never", "nor", "neither"}
_FILTERED_STOP_WORDS = set(_STOP_WORDS) - _NEGATION_WORDS

# Core concepts for WordNet-based synonym normalization
_CONCEPTS = {
    "fat": {"fat", "adipose", "overweight", "obese", "corpulence", "flab"},
    "weight": {"weight", "heaviness", "poundage"},
    "slim": {"slim", "slender", "thin", "skinny", "lean", "fit"},
    "muscle": {"muscle", "muscular", "brawn", "sinew", "strength"},
    "bulk": {"bulk", "bulking", "mass", "size", "volume"},
    "gain": {"gain", "increase", "acquire", "grow", "add"}
}

# ============================================================
# Contraction Map
# ============================================================
# A curated dictionary of the most common English contractions
# relevant to health/fitness chat inputs.

_CONTRACTIONS = {
    "i'm": "i am",
    "i've": "i have",
    "i'll": "i will",
    "i'd": "i would",
    "you're": "you are",
    "you've": "you have",
    "you'll": "you will",
    "you'd": "you would",
    "he's": "he is",
    "she's": "she is",
    "it's": "it is",
    "we're": "we are",
    "we've": "we have",
    "we'll": "we will",
    "they're": "they are",
    "they've": "they have",
    "they'll": "they will",
    "can't": "cannot",
    "cannot": "cannot",
    "won't": "will not",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "wouldn't": "would not",
    "shouldn't": "should not",
    "couldn't": "could not",
    "what's": "what is",
    "where's": "where is",
    "how's": "how is",
    "that's": "that is",
    "there's": "there is",
    "who's": "who is",
    "let's": "let us",
    "i'm not": "i am not",
}

# Build a compiled regex pattern for fast replacement.
# Sorted by length (longest first) to match greedy phrases
# before shorter sub-patterns.
_CONTRACTION_PATTERN = re.compile(
    r"\b(" +
    "|".join(re.escape(k) for k in sorted(
        _CONTRACTIONS.keys(), key=len, reverse=True)
    ) + r")\b",
    re.IGNORECASE
)

# Common spelling typos mapped directly to correct forms for guaranteed accuracy
_COMMON_TYPOS = {
    "protien": "protein",
    "protin": "protein",
    "goodevening": "good evening",
    "hiydration": "hydration",
    "excersise": "exercise",
    "muscel": "muscle",
    "weigth": "weight"
}

# The target vocabulary for general rapidfuzz spelling correction
_TARGET_VOCAB = {
    "protein", "proteins", "hydration", "exercise", "exercises", "workout", "workouts",
    "muscle", "muscles", "weight", "weights", "height", "heights", "calorie", "calories",
    "stretching", "stretch", "yoga", "cardio", "strength", "training", "beginner", "obesity",
    "underweight", "overweight", "hydration", "dehydration", "sleep", "recovery", "diet", "diets",
    "breakfast", "lunch", "dinner", "snack", "snacks", "motivation", "consistent", "consistency",
    "pushup", "pushups", "squat", "squats", "deadlift", "deadlifts", "pullup", "pullups",
    "benchpress", "plank", "planks", "lunge", "lunges", "apple", "apples", "banana", "bananas",
    "orange", "oranges", "grape", "grapes", "berries", "oats", "oatmeal", "quinoa", "pasta",
    "bread", "chicken", "turkey", "beef", "steak", "fish", "salmon", "tuna", "egg", "eggs",
    "tofu", "paneer", "tempeh", "beans", "lentils", "broccoli", "spinach", "milk", "yogurt",
    "cheese", "avocado", "avocados", "almond", "almonds", "whey", "hello", "hi", "hey",
    "morning", "afternoon", "evening", "nice", "meet", "you", "good"
}


def correct_spelling(text: str) -> str:
    """Fuzzy corrects common spelling mistakes using lookup and RapidFuzz (similarity > 90%)."""
    if not text or not isinstance(text, str):
        return ""
        
    words = text.split()
    corrected_words = []
    
    for word in words:
        # Strip punctuation for matching
        clean_word = word.strip(".,!?\"'")
        clean_word_lower = clean_word.lower()
        
        # Skip numeric tokens and very short words
        if clean_word.isdigit() or len(clean_word) <= 3:
            corrected_words.append(word)
            continue
            
        # Skip if word is already a valid term in our target vocabulary
        if clean_word_lower in _TARGET_VOCAB:
            corrected_words.append(word)
            continue
            
        # 1. Exact typo check
        if clean_word_lower in _COMMON_TYPOS:
            corrected = _COMMON_TYPOS[clean_word_lower]
            logger.info(f"Spelling corrected (exact lookup): '{clean_word}' -> '{corrected}'")
            corrected_words.append(word.replace(clean_word, corrected))
            continue
            
        # 2. General RapidFuzz similarity check
        match = process.extractOne(clean_word_lower, list(_TARGET_VOCAB), scorer=fuzz.ratio)
        if match:
            matched_vocab, score, _ = match
            if score >= 90.0:
                logger.info(f"Spelling corrected (Fuzzy similarity {score:.1f}%): '{clean_word}' -> '{matched_vocab}'")
                corrected_words.append(word.replace(clean_word, matched_vocab))
                continue
                
        corrected_words.append(word)
        
    return " ".join(corrected_words)


# ============================================================
# Public API
# ============================================================

def preprocess_classifier(text: str) -> str:
    """Preprocess text for the intent classifier (lowercase, punctuation, whitespace).

    Does NOT remove stopwords and does NOT lemmatize.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Correct spelling first
    text = correct_spelling(text)
    
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove punctuation and normalize whitespace
    return _remove_punctuation(text)


def preprocess_keywords(text: str) -> str:
    """Preprocess text for keyword matching and entity extraction.

    Performs: lowercase, punctuation removal, stopword removal, lemmatization,
    and synonym expansion.
    """
    if not text or not isinstance(text, str):
        return ""

    # Correct spelling first
    text = correct_spelling(text)

    # Step 1: Expand contractions
    text = expand_contractions(text)

    # Step 2: Convert to lowercase
    text = text.lower()

    # Step 3: Remove punctuation and special characters
    text = _remove_punctuation(text)

    # Step 4: Tokenize into individual words
    tokens = tokenize(text)

    # Step 5: Remove stopwords
    tokens = remove_stopwords(tokens)

    # Step 6: Lemmatize each token to its base form
    tokens = lemmatize(tokens)

    # Step 6.5: Normalize synonyms using WordNet
    tokens = normalize_synonyms(tokens)

    # Step 7: Rejoin tokens into a single string
    return " ".join(tokens)


def preprocess(text: str) -> str:
    """Run the full text preprocessing pipeline (alias for preprocess_keywords).

    This is kept for backward compatibility with other scripts.
    """
    return preprocess_keywords(text)


def expand_contractions(text: str) -> str:
    """Replace English contractions with their full forms.

    Uses a precompiled regex for efficiency. The replacement
    is case-insensitive and preserves the original case of
    the surrounding text.

    Parameters
    ----------
    text : str
        Input text that may contain contractions.

    Returns
    -------
    str
        Text with contractions expanded.

    Example
    -------
    >>> expand_contractions("I can't sleep and I don't know why")
    'I cannot sleep and I do not know why'
    """
    def _replace(match):
        return _CONTRACTIONS.get(match.group(0).lower(),
                                 match.group(0))

    return _CONTRACTION_PATTERN.sub(_replace, text)


def tokenize(text: str) -> list:
    """Split text into a list of word tokens.

    Uses NLTK's word_tokenize which handles punctuation and
    hyphenated words more intelligently than a simple split().

    Parameters
    ----------
    text : str
        Cleaned, lowercased text.

    Returns
    -------
    list[str]
        List of individual word tokens.

    Example
    -------
    >>> tokenize("how many calories do i need")
    ['how', 'many', 'calories', 'do', 'i', 'need']
    """
    return word_tokenize(text)


def remove_stopwords(tokens: list) -> list:
    """Filter out common English stopwords from a token list.

    Negation words ('not', 'no', 'never') are preserved
    because they carry important semantic meaning in
    health-related queries.

    Parameters
    ----------
    tokens : list[str]
        List of word tokens.

    Returns
    -------
    list[str]
        Filtered list with stopwords removed.

    Example
    -------
    >>> remove_stopwords(['how', 'many', 'calories', 'do', 'i', 'need'])
    ['many', 'calories', 'need']
    """
    return [
        token for token in tokens
        if token not in _FILTERED_STOP_WORDS
        and len(token) > 1  # Remove single-character tokens
    ]


def lemmatize(tokens: list) -> list:
    """Convert each token to its base (lemma) form.

    The WordNetLemmatizer looks up the dictionary base form
    of each word. For example:
    - "running" → "run"
    - "workouts" → "workout"
    - "calories" → "calorie"
    - "healthier" → "healthy"

    Parameters
    ----------
    tokens : list[str]
        List of word tokens (after stopword removal).

    Returns
    -------
    list[str]
        List of lemmatized tokens.

    Example
    -------
    >>> lemmatize(['calories', 'burning', 'workouts'])
    ['calorie', 'burning', 'workout']
    """
    return [_lemmatizer.lemmatize(token) for token in tokens]


# Blacklist of common/functional words that should not undergo synonym expansion.
# This prevents words with obscure WordNet senses (like 'going' or 'run' mapping to 'fit' -> 'slim')
# from causing false positive intent boosts.
_SYNONYM_BLACKLIST = {
    # Common functional/generic verbs
    "go", "going", "run", "running", "walk", "walking", "do", "doing", "get", "getting",
    "take", "taking", "make", "making", "come", "coming", "have", "having", "meet", "meeting",
    "suit", "suiting", "match", "matching", "agree", "agreeing", "fill", "filling", "answer",
    "answering", "conform", "conforming", "satisfy", "satisfying", "look", "looking",
    # Greeting/Conversational words
    "hello", "hi", "hey", "how", "why", "where", "when", "who", "what", "good", "nice", "fine",
    "morning", "afternoon", "evening", "day", "time", "about", "around", "thing", "things",
    "mass", "strength", "body"
}



def normalize_synonyms(tokens: list) -> list:
    """Normalize terms to core health/fitness concepts using WordNet.

    For example, if a token or any of its WordNet synonyms match synonyms
    of our target concept words (e.g. 'obese' shares meaning with 'fat',
    'slender' with 'slim'), the token is replaced by the concept.

    Parameters
    ----------
    tokens : list[str]
        List of lemmatized word tokens.

    Returns
    -------
    list[str]
        List of tokens with key terms expanded/normalized.
    """
    normalized_tokens = []
    for token in tokens:
        if token in _SYNONYM_BLACKLIST:
            normalized_tokens.append(token)
            continue

        syns = {token}
        try:
            for syn in wordnet.synsets(token):
                for lemma in syn.lemmas():
                    syns.add(lemma.name().lower().replace('_', ' '))
        except Exception:
            pass

        # Check intersection with our core fitness concepts
        mapped = False
        for concept_name, concept_syns in _CONCEPTS.items():
            if syns.intersection(concept_syns):
                normalized_tokens.append(concept_name)
                mapped = True
                break
        if not mapped:
            normalized_tokens.append(token)

    return normalized_tokens


# ============================================================
# Private Helpers
# ============================================================

def _remove_punctuation(text: str) -> str:
    """Remove punctuation and non-alphabetic characters.

    Preserves spaces and alphanumeric characters only.
    Numbers are kept because they appear in health queries
    (e.g., "I weigh 70 kg").

    Parameters
    ----------
    text : str
        Lowercased input text.

    Returns
    -------
    str
        Text with punctuation stripped.
    """
    # Replace punctuation with a space (not empty string)
    # to avoid accidentally merging adjacent words.
    translator = str.maketrans(string.punctuation,
                               " " * len(string.punctuation))
    text = text.translate(translator)

    # Collapse multiple spaces into one
    return re.sub(r"\s+", " ", text).strip()
