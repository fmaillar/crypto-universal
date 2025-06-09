# agents.md – Crypto-Universal

## Objective  
Create a universal encryption overlay that allows text messages to be encrypted/decrypted for any communication channel (WhatsApp, SMS, email, etc.), independently of the underlying transport application.

## Expected Features
- Each user possesses an asymmetric key pair.
- Messages are encrypted locally using the recipient's public key.
- Contacts are stored in a local JSON file (`contacts.json`).
- No third-party servers. All encryption is performed entirely offline.
- Encrypted messages are generated using a dedicated custom keyboard designed for the application.

## Constraints
- Use `PyNaCl` or `Age` for cryptographic operations.
- Code must be clean, minimalistic, and compatible with Python 3.10+.
- No use of network dependencies.
- The private key must **never** be written to disk or persist beyond memory.

## Target Interfaces
- CLI commands (`encrypt`, `decrypt`, `add-contact`, `list-contacts`)
- Support files: `contacts.json`, `contacts_schema.json`

## Interaction Rules
- Always provide complete, executable code.
- Responses must prioritize clarity and security.
- Suggestions should empower user digital autonomy.
