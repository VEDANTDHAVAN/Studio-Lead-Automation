from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from email.utils import parseaddr
from typing import List, Optional
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
]

@dataclass
class GmailMessage:
    id: str
    thread_id: str
    sender: str
    sender_email: str
    subject: str
    body: str

class GmailClient:
    def __init__(
        self, token_file: str = "token.json",
        credentials_file: str = "credentials.json",
    ):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(
                self.token_file, SCOPES,
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES,
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    def fetch_unread(
        self, max_results: int = 10,
    ) -> List[GmailMessage]:
        response = (
            self.service.users().messages().list(
                userId="me", 
                q=f"is:unread in:inbox",
                maxResults=max_results,
            ).execute()
        )

        messages = response.get("messages", [])

        return [self.get_message(m["id"]) for m in messages]

    def get_message(
        self, message_id: str,
    ) -> GmailMessage:
        raw = (
            self.service.users().messages().get(
                userId="me", id=message_id, format="full",
            ).execute()
        )

        headers = raw["payload"]["headers"]

        subject = ""
        sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]

            elif h["name"] == "From":
                sender = h["value"]

        name, email = parseaddr(sender)

        body = self._extract_body(raw["payload"])

        return GmailMessage(
            id=raw["id"], thread_id=raw["threadId"],
            sender=name, sender_email=email,
            subject=subject, body=body,
        )

    def _extract_body(self, payload) -> str:
        if "parts" in payload:
            for part in payload["parts"]:
                mime = part.get("mimeType")

                if mime == "text/plain":
                    return self._decode(part["body"]["data"])

                if mime == "text/html":
                    html = self._decode(part["body"]["data"])
                    return BeautifulSoup(html, "html.parser").get_text(separator="\n")

        if payload["body"].get("data"):
            return self._decode(payload["body"]["data"])

        return ""

    def send_reply(
        self, thread_id: str, to_email: str, 
        subject: str, body: str,
    ):
        message = MIMEText(body)

        message["To"] = to_email
        message["Subject"] = (
            subject if subject.lower().startswith("re:")
            else f"Re: {subject}"
        )

        raw = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        self.service.users().messages().send(
            userId="me", body={
                "raw": raw, "threadId": thread_id,
            },
        ).execute()

    @staticmethod
    def _decode(data: str) -> str:
        return base64.urlsafe_b64decode(data).decode("utf-8")

    def mark_as_read(self, message_id: str):
        (
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]},
            ).execute()
        )

    def add_label(
        self, message_id: str, label_id: str,
    ):
        (
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"addLabelIds": [label_id]},
            ).execute()
        )

    def get_label_id(self, label_name: str) -> str | None:
        labels = (
            self.service.users().labels().list(userId="me")
            .execute().get("labels", [])
        )

        for label in labels:
            if label["name"].lower() == label_name.lower():
                return label["id"]

        return None

    def add_processed_label(self, message_id: str):
        label_id = self.get_label_id("Processed")

        if label_id:
            self.add_label(message_id, label_id)