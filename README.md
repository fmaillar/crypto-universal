# Crypto Universal

Crypto Universal provides a minimal encryption interface that can be
layered on top of any messaging software.  It exposes simple functions to
encrypt and decrypt messages so they can be copied into or out of your
favourite communication app.

The library uses asymmetric RSA encryption from the
[`cryptography`](https://cryptography.io/) package. A private/public key
pair can be generated once and reused across messaging apps.

## Installation

```
pip install cryptography
```

## Usage

Generate a key pair:

```
python -m crypto_universal generate-keys
```

The first line of output is the base64 encoded private key and the second
line is the base64 encoded public key.  Encrypt a message:

```
python -m crypto_universal encrypt <base64-public-key> "hello"
```

Decrypt a message:

```
python -m crypto_universal decrypt <base64-private-key> <ciphertext>
```

You can integrate these calls into a custom keyboard or other overlay so
that messages are automatically encrypted before being sent and decrypted
when received.
