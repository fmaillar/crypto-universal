# Android Secure Keyboard Example

This directory contains a minimal example of an `InputMethodService` that
integrates Crypto Universal's RSA encryption. The service exposes a simple
"Encrypt" button that takes the text you have typed and replaces it with a
base64-encoded ciphertext.

The snippet in `SecureKeyboardService.kt` demonstrates:

1. Loading a base64 public/private key pair.
2. Encrypting the current input field when the button is pressed.
3. Committing the encrypted text back to the host application.

To use it:

1. Add this service to an Android project and register it in `AndroidManifest.xml`.
2. Load your keys from app storage or a secure location.
3. Build and install the app. When the keyboard is selected, you can encrypt
   messages before sending them from any messaging application.

Decryption can be added in a similar manner by reading the ciphertext from the
message field and calling the RSA decrypt routine with the private key.
