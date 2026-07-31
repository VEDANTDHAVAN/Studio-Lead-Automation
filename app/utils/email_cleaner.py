import re

MAX_EMAIL_CHARS = 4000

def clean_email(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+", "", text)

    unsubscribe = text.lower().find("unsubscribe")
    if unsubscribe != -1:
        text = text[:unsubscribe]

    return text[:MAX_EMAIL_CHARS].strip()