# IMAP MCP Email Assistant

A modern, intelligent email assistant built in Python. Connects to your IMAP email (Gmail or others), automates email management, and drafts professional replies for meeting/event requests—all with a single command.

---

## 🚀 Features Overview

### 1. **IMAP Email Access**
- **Secure Connection:** Connects to Gmail or any IMAP server using SSL and app-specific passwords.
- **Flexible Config:** Easily switch between accounts by editing `config.yaml`.

### 2. **Email Browsing & Filtering**
- **List Folders:** Instantly list all folders (Inbox, Sent, Drafts, custom labels, etc.).
- **Filter Emails:** Fetch emails by status (e.g., UNSEEN, flagged) or by smart keyword matching (e.g., meeting/event requests).
- **Search:** Search emails by keyword in subject or body.

### 3. **Email Content Handling**
- **Read Emails:** View full message content, including plain text, HTML, and all attachments.
- **Attachment Support:** Download and display attachments from any email.

### 4. **Automated Draft Reply Generation**
- **Smart Filtering:** Automatically detects emails requesting meetings or event attendance using customizable keywords.
- **Professional Replies:** Generates a polite, professional reply for each detected email.
- **Draft Saving:** Saves each reply as a draft in your Gmail Drafts folder, with correct threading (In-Reply-To, References headers).
- **Customizable:** Edit the reply message and keywords in `draft_replies_json.py` to match your style.

### 5. **Draft Management**
- **Save Any Email as Draft:** Use the IMAP APPEND command to save any composed email (plain text & HTML, CC, threading headers) as a draft.
- **Threaded Replies:** Replies include proper headers for seamless conversation threading in Gmail and other clients.

### 6. **Email Actions**
- **Move:** Move emails to any folder/label by UID.
- **Delete:** Delete emails by UID.
- **Mark as Read/Unread:** Change read status of any email.
- **Flag/Unflag:** Add or remove flags (e.g., important/starred) on emails.

### 7. **JSON Output for Automation**
- **Clean JSON:** All scripts output results (filtered emails, draft details, actions) in JSON for easy integration with other tools or workflows.

### 8. **Standalone & Scriptable**
- **Ready-to-Run Scripts:**
  - `draft_replies_json.py`: Filter, draft, and save replies for meeting/event requests.
  - `read_email_by_uid.py`: Read a specific email by UID.
  - `list_folders_direct.py`: List all folders.
  - `email_actions.py`: Move, delete, mark, or flag emails by UID.
- **Easy to Extend:** Build your own automations using the IMAP client and tools in `imap_mcp/`.

---

## 🗂️ Project Structure

```
imap-mcp/
├── imap_mcp/                # Core source code (IMAP client, tools, models, etc.)
│   ├── config.py            # Configuration handling
│   ├── imap_client.py       # IMAP protocol logic (connect, fetch, search, etc.)
│   ├── models.py            # Data models for emails, addresses, attachments
│   ├── smtp_client.py       # Email composition and MIME message creation
│   ├── tools.py             # High-level tools for actions, draft saving, etc.
│   └── ...                  # Other core modules
├── tests/                   # Automated test suite
│   └── ...
├── draft_replies_json.py    # Script: filter meeting/event emails, draft & save replies
├── email_actions.py         # Script: move, delete, mark, flag emails
├── read_email_by_uid.py     # Script: read a specific email by UID
├── list_folders_direct.py   # Script: list all folders
├── config.yaml              # Your IMAP/Gmail config (user-supplied, not in repo)
├── pyproject.toml           # Project configuration and dependencies
├── README.md                # Project documentation (this file)
└── ...                      # Other supporting files (e.g., .gitignore, LICENSE)
```

**Key Points:**
- All main logic is in `imap_mcp/` (modular, reusable).
- Scripts in the root directory are ready-to-run for common tasks.
- `config.yaml` holds your email credentials/settings (never commit real credentials!).
- `tests/` ensures reliability and easy development.

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.8 or higher
- Gmail (recommended) or any IMAP-enabled email account

### Installation
1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd imap-mcp
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt  # or use pyproject.toml if using poetry/uv
   ```

### Gmail/App Password Setup
- For Gmail, create an app-specific password (see Google Account > Security > App Passwords).
- Create `config.yaml` in the project root:
  ```yaml
  imap:
    host: imap.gmail.com
    port: 993
    username: your-email@gmail.com
    password: your-app-password
    use_ssl: true
  ```

---

## ⚡ Usage Examples

### 1. **Filter and Draft Replies for Meeting/Event Requests**
```bash
python draft_replies_json.py
```
- Filters all unseen emails for meeting/event requests.
- Drafts a professional reply for each and saves it in your Gmail Drafts folder.
- Outputs a JSON list of all actions taken.

### 2. **Read a Specific Email by UID**
```bash
python read_email_by_uid.py --uid <UID>
```

### 3. **List All Folders**
```bash
python list_folders_direct.py
```

### 4. **Perform Email Actions (Move, Delete, Mark, Flag)**
```bash
python email_actions.py --action <move|delete|mark|flag> --uid <UID> [--target-folder <FOLDER>]
```

---

## 🎨 Customization & Extensibility
- **Keywords:** Edit `draft_replies_json.py` to change the keywords for meeting/event detection.
- **Reply Message:** Edit the reply body/html in the same script.
- **Add More Scripts:** Use the IMAP client and tools in `imap_mcp/` to build more automation.

---

## 🔒 Security Notes
- Store your config and app passwords securely.
- Never commit your real `config.yaml` to public repos.

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Credits
- Built with Python, IMAPClient, and standard libraries.
- Inspired by Model Context Protocol (MCP) and modern email automation needs.
