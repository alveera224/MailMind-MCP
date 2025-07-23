import yaml
from imap_mcp.imap_client import ImapClient
from imap_mcp.config import ImapConfig

def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config["imap"]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Perform actions on emails (move, delete, mark, flag)")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--folder", default="INBOX", help="Source folder")
    parser.add_argument("--uid", type=int, required=True, help="UID of the email")
    parser.add_argument("--action", required=True, choices=["move", "delete", "read", "unread", "flag", "unflag"], help="Action to perform")
    parser.add_argument("--target-folder", help="Target folder for move action")
    args = parser.parse_args()

    imap_dict = load_config(args.config)
    imap_config = ImapConfig.from_dict(imap_dict)
    client = ImapClient(imap_config)
    client.connect()

    if args.action == "move":
        if not args.target_folder:
            print("Target folder required for move action.")
        else:
            success = client.move_email(args.uid, args.folder, args.target_folder)
            print("Moved." if success else "Move failed.")
    elif args.action == "delete":
        success = client.delete_email(args.uid, args.folder)
        print("Deleted." if success else "Delete failed.")
    elif args.action == "read":
        success = client.mark_email(args.uid, args.folder, r"\Seen", True)
        print("Marked as read." if success else "Failed to mark as read.")
    elif args.action == "unread":
        success = client.mark_email(args.uid, args.folder, r"\Seen", False)
        print("Marked as unread." if success else "Failed to mark as unread.")
    elif args.action == "flag":
        success = client.mark_email(args.uid, args.folder, r"\Flagged", True)
        print("Flagged." if success else "Failed to flag.")
    elif args.action == "unflag":
        success = client.mark_email(args.uid, args.folder, r"\Flagged", False)
        print("Unflagged." if success else "Failed to unflag.")
    client.disconnect()

if __name__ == "__main__":
    main() 