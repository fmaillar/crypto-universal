# Crypto Universal

Crypto Universal provides a minimal encryption interface that can be
layered on top of any messaging software.  It exposes simple functions to
encrypt and decrypt messages so they can be copied into or out of your
favourite communication app.

The library uses asymmetric RSA encryption from the
[`cryptography`](https://cryptography.io/) package. A private/public key
pair can be generated once and reused across messaging apps.

## Installation

Install the project along with its dependencies using `pip install .` from the
repository root:

```
pip install .
```

## Usage

Generate a key pair:

```
crypto_universal generate-keys
```

The first line of output is the base64 encoded private key and the second
line is the base64 encoded public key.  Encrypt a message:

```
crypto_universal encrypt <base64-public-key> "hello"
```

Decrypt a message:

```
crypto_universal decrypt <base64-private-key> <ciphertext>
```

You can integrate these calls into a custom keyboard or other overlay so
that messages are automatically encrypted before being sent and decrypted
when received.

## Android Integration

A minimal Gradle project is provided under `examples/android`. It implements a
custom keyboard service that uses Crypto Universal to encrypt outgoing text. The
keyboard exposes an "Encrypt" button which replaces the typed message with the
encrypted ciphertext.

Build the example with `./gradlew assembleDebug` and install the resulting APK
on a device. Launch the `Secure Keyboard` app to enable the input method and
then select it in the system settings. When active, you can compose a message,
press "Encrypt" and send the ciphertext through any chat app.
