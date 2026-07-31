from app.integrations.gmail import GmailClient

gmail = GmailClient()

messages = gmail.fetch_unread()

for m in messages:
    print(m.subject)
    print(m.sender_email)
    print(m.body[:500])