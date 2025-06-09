# agent.md – Crypto-Universal

## Objective  
Create a universal encryption overlay that allows text messages to be encrypted/decrypted for any communication channel (WhatsApp, SMS, email, etc.), independently of the underlying transport application.

## Expected Features
- Each user possesses an asymmetric key pair.
- Messages are encrypted locally using the recipient's public key.
- Contacts are stored in a local JSON file (`contacts.json`).
- No third-party servers: all encryption is done offline.
- Encrypted messages are generated using a dedicated custom keyboard designed for this application.

## Constraints
- Use `PyNaCl` or `Age` for cryptographic operations.
- Code must be clean, minimalistic, and compatible with Python 3.10+.
- No use of network dependencies.
- The private key must **never** be written to disk or persist beyond memory.

## Target Interfaces
- CLI commands:
  - `encrypt` – encrypt a message for a recipient
  - `decrypt` – decrypt a received message
  - `add-contact` – register a public key for a contact
  - `list-contacts` – view registered recipients

## Support Files
- `main.py`
- `contacts.json`
- `contacts_schema.json`
- `encryption.py`
- `agent.md`

## Interaction Rules
- Always provide complete, executable code snippets.
- Avoid abstractions unless explicitly requested.
- Ensure security, clarity, and user control in all suggestions.
- Focus on empowering the user with transparent, auditable encryption logic.

## Usage Example

```bash
# Encrypt a message
$ python main.py encrypt --to alice@example.com --message "Hello, world"

# Decrypt a received message
$ python main.py decrypt --file msg.enc

# Add a new contact
$ python main.py add-contact --id alice@example.com --key BASE64_KEY

# List known contacts
$ python main.py list-contacts
```
