"""Small, dependency-free text utilities: tokenizing, stemming and synonyms."""
import re

STOPWORDS = set("""
a an the and or but if to of in on at for from by with about into over after before is are was were be been
being do does did doing have has had i me my we our you your it its this that these those can could would should
will just how what when where why which who whom please hi hello hey there am so not no any some get got still
""".split())

# Customers rarely use the same words as help articles. Map common phrasings to article vocabulary.
SYNONYMS = {
    "parcel": "package", "packag": "package", "shipment": "package", "box": "package",
    "money": "refund", "reimburs": "refund", "refunded": "refund",
    "send": "return", "sent": "return",
    "swap": "exchange", "switch": "exchange",
    "broken": "damaged", "cracked": "damaged", "faulty": "defective", "torn": "damaged",
    "stolen": "missing", "lost": "missing", "never": "missing",
    "card": "payment", "visa": "payment", "mastercard": "payment", "paypal": "payment",
    "rejected": "declined", "fail": "declined", "failed": "declined", "denied": "declined",
    "coupon": "discount", "promo": "discount", "voucher": "discount",
    "login": "password", "log": "password", "sign": "password", "locked": "password",
    "deliver": "delivery", "arrive": "delivery", "arrival": "delivery", "eta": "delivery",
    "abroad": "international", "usa": "international", "us": "international", "overseas": "international",
    "duti": "customs", "customs": "customs",
    "where": "track",
    "wrong": "change", "moved": "change",
    "renewal": "subscription", "membership": "subscription", "skip": "subscription", "pause": "subscription",
    "cheaper": "price", "drop": "price", "dropped": "price", "sale": "price",
    "fit": "size", "fits": "size", "measurement": "size",
    "phone": "contact", "hours": "contact", "open": "contact", "reach": "contact",
    "giftcard": "gift",
}


def stem(word: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def tokenize(text: str, expand: bool = True) -> list:
    words = re.findall(r"[a-z0-9]+", text.lower())
    tokens = []
    for w in words:
        if w in STOPWORDS:
            continue
        s = stem(w)
        tokens.append(s)
        if expand:
            mapped = SYNONYMS.get(w) or SYNONYMS.get(s)
            if mapped and mapped != s:
                tokens.append(stem(mapped))
    return tokens
