import logging
import time

from app.integrations.gmail import GmailClient
from app.workflow.lead_pipeline import LeadPipeline
from app.utils.email_cleaner import clean_email

logger = logging.getLogger(__name__)

LEAD_KEYWORDS = {
    "website", "app", "project", "budget", "quote", "proposal", 
    "agency", "design", "development", "software", "hire", "freelance",
}

def is_probable_lead(subject: str, body: str) -> bool:
    text = (subject + " " + body).lower()

    return any(keyword in text for keyword in LEAD_KEYWORDS)


class GmailPipeline:
    def __init__(self):
        self.gmail = GmailClient()
        self.pipeline = LeadPipeline()

    def process_once(self):
        messages = self.gmail.fetch_unread()

        if not messages:
            logger.info("No unread emails.")
            return

        logger.info("Found %d unread email(s).", len(messages))

        for message in messages:
            try:
                logger.info(
                    "Processing: %s <%s>",
                    message.sender, message.sender_email,
                )

                email_text = clean_email(f"""
Subject: {message.subject}

From: {message.sender} <{message.sender_email}>

{message.body}
""")
                if not is_probable_lead(message.subject, message.body):
                    logger.info(
                        "Skipping non-lead email: %s", message.subject,
                    )

                    self.gmail.mark_as_read(message.id)
                    continue
                
                result = self.pipeline.run(email_text)

                if not result["processed"]:
                    self.gmail.mark_as_read(message.id)
                    logger.info("Skipped: %s", result["reason"])
                    continue

                reply = result["reply_email"]

                AUTO_SENDERS = (
                    "noreply", "no-reply",
                    "donotreply", "mailer-daemon",
                )

                email = message.sender_email.lower()

                if any(s in email for s in AUTO_SENDERS):
                    logger.info("Skipping auto reply.")
                else:
                    self.gmail.send_reply(
                        thread_id=message.thread_id, to_email=message.sender_email,
                        subject=message.subject, body=reply,
                    )

                    self.gmail.mark_as_read(message.id)

                    logger.info(
                        "Successfully processed %s", message.sender_email,
                    )

                logger.info(
                    "Lead Status: %s", result["qualification"]["status"],
                )
                # Temporarily only mark as read.
                # Sending replies will be added next.
                self.gmail.mark_as_read(message.id)
                self.gmail.add_processed_label(message.id)

            except Exception:
                logger.exception(
                    "Failed processing email %s", message.id,
                )

    def start(self, interval: int = 30):
        logger.info("Starting Gmail Lead Automation...")

        try:
            while True:
                self.process_once()
                time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("Stopping Gmail Worker")