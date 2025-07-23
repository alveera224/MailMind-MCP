import json
from imap_mcp.imap_client import ImapClient
from imap_mcp.config import ImapConfig
from imap_mcp.models import EmailAddress
from imap_mcp.smtp_client import create_reply_mime

def load_config(path):
    import yaml
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config["imap"]

def is_meeting_or_event_request(email):
    meeting_keywords = [
        "meeting", "schedule a meeting", "requested to meet", "let's meet", "appointment",
        "calendar invite", "attend event", "event invitation", "join us", "webinar", "conference",
        "workshop", "session", "invited to attend", "please attend", "invitation to", "invite you to"
    ]
    text = (email.subject + " " + (email.content.text or "") + " " + (email.content.html or "")).lower()
    return any(keyword in text for keyword in meeting_keywords)

def main():
    config = load_config("config.yaml")
    imap_config = ImapConfig.from_dict(config)
    client = ImapClient(imap_config)
    client.connect()
    folder = "INBOX"
    uids = client.search("UNSEEN", folder=folder)
    results = []
    for uid in uids:
        email = client.fetch_email(uid, folder=folder)
        if not email:
            continue
        if is_meeting_or_event_request(email):
            to = str(email.from_)
            cc = [str(addr) for addr in email.cc] if email.cc else []
            subject = f"Re: {email.subject}"
            body = f"Dear {email.from_.name or email.from_.address},\n\nThank you for your invitation. I will be attending the meeting/event as requested.\n\nBest regards,\nYour Name"
            html_body = f"<p>Dear {email.from_.name or email.from_.address},</p><p>Thank you for your invitation. I will be attending the meeting/event as requested.</p><p>Best regards,<br>Your Name</p>"
            in_reply_to = email.message_id
            references = " ".join(email.references + [email.message_id]) if email.references else email.message_id
            # Build MIME reply
            reply_to_addr = EmailAddress.parse(config["username"])
            mime_msg = create_reply_mime(
                original_email=email,
                reply_to=reply_to_addr,
                body=body,
                subject=subject,
                cc=[EmailAddress.parse(addr) for addr in cc] if cc else None,
                reply_all=False,
                html_body=html_body
            )
            # Save as draft
            draft_uid = client.save_draft_mime(mime_msg)
            results.append({
                "to": to,
                "cc": cc,
                "subject": subject,
                "body": body,
                "html_body": html_body,
                "in_reply_to": in_reply_to,
                "references": references,
                "draft_uid": draft_uid,
                "uid": uid
            })
    print(json.dumps(results, indent=2))
    client.disconnect()

if __name__ == "__main__":
    main() 