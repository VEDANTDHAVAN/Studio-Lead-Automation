QUALIFIED_PROMPT = """
You are a professional creative agency.

Write a friendly follow-up email.

The lead has already been qualified.

Goals:
- Thank them
- Mention their project briefly
- Mention budget and deadline if available
- Invite them to schedule a discovery call
- Keep it under 200 words.

Return only the email body.
"""

REVIEW_PROMPT = """
You are a professional creative agency.

Write a follow-up email asking for the missing information.

Use the missing fields provided.

Keep it under 200 words.

Return only the email body.
"""

DECLINE_PROMPT = """
Write a polite email declining the opportunity.

Thank the prospect.

Keep the door open for future collaboration.

Return only the email body.
"""