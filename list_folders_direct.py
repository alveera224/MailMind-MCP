import yaml
from imap_mcp.imap_client import ImapClient
from imap_mcp.config import ImapConfig

def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config["imap"]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="List all folders in your mailbox")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    imap_dict = load_config(args.config)
    imap_config = ImapConfig.from_dict(imap_dict)
    client = ImapClient(imap_config)
    client.connect()
    folders = client.list_folders()
    print("Available folders:")
    for folder in folders:
        print("-", folder)
    client.disconnect()

if __name__ == "__main__":
    main() 