"""NLP preprocessing service for phishing detection."""
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download required NLTK data (idempotent)
for resource in ("stopwords", "punkt", "wordnet", "punkt_tab"):
    try:
        nltk.download(resource, quiet=True)
    except Exception:  # pragma: no cover
        pass


class TextPreprocessor:
    """Cleans and normalises raw text for ML classification."""

    URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
    EMAIL_PATTERN = re.compile(r"\b[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
    PHONE_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}\b")
    MONEY_PATTERN = re.compile(r"(?:[\$€£₹]\s?\d+[.,]?\d*|\b\d+\s?(?:k|m|b|million|billion|thousand)\b)", re.I)
    HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
    NUM_PATTERN = re.compile(r"\b\d+\b")
    WHITESPACE_PATTERN = re.compile(r"\s+")

    SUSPICIOUS_KEYWORDS = [
        "verify", "verification", "suspend", "suspended", "locked", "restrict",
        "click here", "click the link", "click below", "urgent", "immediately",
        "congratulations", "won", "winner", "prize", "lottery", "claim",
        "free", "gift", "reward", "bonus", "offer", "limited time",
        "account", "password", "login", "credential", "confirm", "update",
        "bank", "mpesa", "paypal", "amazon", "fedex", "irs", "tax", "refund",
        "kyc", "otp", "pin", "ssn", "social security", "credit card", "cvv",
        "wire transfer", "bitcoin", "crypto", "wallet", "invoice",
    ]

    def __init__(self, use_lemmatization: bool = True):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.use_lemmatization = use_lemmatization
        self.stop_words = set(stopwords.words("english"))

    def clean(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        text = text.lower()
        text = self.HTML_TAG_PATTERN.sub(" ", text)
        text = self.URL_PATTERN.sub(" URLTOKEN ", text)
        text = self.EMAIL_PATTERN.sub(" EMAILTOKEN ", text)
        text = self.PHONE_PATTERN.sub(" PHONETOKEN ", text)
        text = self.MONEY_PATTERN.sub(" MONEYTOKEN ", text)
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
        text = self.NUM_PATTERN.sub(" ", text)
        text = self.WHITESPACE_PATTERN.sub(" ", text).strip()
        return text

    def tokenize(self, text: str) -> list:
        try:
            return nltk.word_tokenize(text)
        except Exception:
            return text.split()

    def remove_stopwords(self, tokens: list) -> list:
        return [t for t in tokens if t and t not in self.stop_words and len(t) > 2]

    def stem_or_lemmatize(self, tokens: list) -> list:
        if self.use_lemmatization:
            return [self.lemmatizer.lemmatize(t) for t in tokens]
        return [self.stemmer.stem(t) for t in tokens]

    def preprocess(self, text: str) -> str:
        cleaned = self.clean(text)
        tokens = self.tokenize(cleaned)
        tokens = self.remove_stopwords(tokens)
        tokens = self.stem_or_lemmatize(tokens)
        return " ".join(tokens)

    def extract_suspicious_keywords(self, text: str) -> list:
        if not text:
            return []
        lowered = text.lower()
        found = []
        for kw in self.SUSPICIOUS_KEYWORDS:
            if kw in lowered:
                found.append(kw)
        return sorted(set(found))

    def extract_features(self, text: str) -> dict:
        """Heuristic features that boost interpretability."""
        if not text:
            return {
                "num_urls": 0, "num_emails": 0, "num_phones": 0,
                "num_money": 0, "num_uppercase_words": 0, "num_exclamations": 0,
                "num_suspicious": 0, "length": 0,
            }
        return {
            "num_urls": len(self.URL_PATTERN.findall(text)),
            "num_emails": len(self.EMAIL_PATTERN.findall(text)),
            "num_phones": len(self.PHONE_PATTERN.findall(text)),
            "num_money": len(self.MONEY_PATTERN.findall(text)),
            "num_uppercase_words": sum(1 for w in text.split() if w.isupper() and len(w) > 2),
            "num_exclamations": text.count("!"),
            "num_suspicious": len(self.extract_suspicious_keywords(text)),
            "length": len(text),
        }


preprocessor = TextPreprocessor()
