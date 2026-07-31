AUTO_SENDERS = [
    "indeed.com", "linkedin.com", "github.com", 
    "google.com", "facebookmail.com", "amazon.in",
    "amazon.com", "noreply", "no-reply", "donotreply",
]

KEYWORDS = [
    "project", "website", "development",
    "app", "budget", "quote", "proposal",
    "agency", "software", "hire", "design",
]


def should_send_to_llm(message):
    sender = message.sender_email.lower()

    if any(domain in sender for domain in AUTO_SENDERS):
        return False

    text = (message.subject + " " + message.body).lower()

    return any(keyword in text for keyword in KEYWORDS)