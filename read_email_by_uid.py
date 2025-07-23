import yaml
from imap_mcp.imap_client import ImapClient
from imap_mcp.config import ImapConfig
import os

def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config["imap"]

def save_attachments(attachments, save_dir="attachments"):
    if not attachments:
        print("No attachments found.")
        return
    os.makedirs(save_dir, exist_ok=True)
    for att in attachments:
        if att.content:
            filepath = os.path.join(save_dir, att.filename)
            with open(filepath, "wb") as f:
                f.write(att.content)
            print(f"Saved attachment: {filepath} ({att.size} bytes)")
        else:
            print(f"Attachment {att.filename} has no content.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Read a specific email by UID from Gmail")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--folder", default="INBOX", help="Folder to search (default: INBOX)")
    parser.add_argument("--uid", type=int, required=True, help="UID of the email to read")
    parser.add_argument("--save-attachments", action="store_true", help="Save attachments to disk")
    args = parser.parse_args()

    imap_dict = load_config(args.config)
    imap_config = ImapConfig.from_dict(imap_dict)
    client = ImapClient(imap_config)
    client.connect()
    client.select_folder(args.folder)
    msg = client.fetch_email(args.uid)
    print(f"From: {msg.from_}")
    print(f"To: {msg.to}")
    print(f"Subject: {msg.subject}")
    print(f"Date: {msg.date}")
    # Print plain text if available, otherwise HTML, otherwise '[No body]'
    if hasattr(msg, "content"):
        if getattr(msg.content, "text", None):
            print(f"\nBody (plain text):\n{msg.content.text}")
        elif getattr(msg.content, "html", None):
            print(f"\nBody (HTML):\n{msg.content.html}")
        else:
            print("\nBody:\n[No body]")
    else:
        print("\nBody:\n[No body]")
    if msg.attachments:
        print(f"\nAttachments ({len(msg.attachments)}):")
        for i, att in enumerate(msg.attachments, 1):
            print(f"  {i}. {att.filename} ({att.content_type}, {att.size} bytes)")
        if args.save_attachments:
            save_attachments(msg.attachments)
    else:
        print("\nNo attachments.")
    client.disconnect()

if __name__ == "__main__":
    main() 