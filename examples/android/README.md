# Android Secure Keyboard Example

This directory now contains a minimal Gradle project that builds a secure
keyboard leveraging Crypto Universal's RSA encryption. The keyboard provides an
"Encrypt" button that replaces the typed text with a base64 ciphertext.

The project structure mirrors a typical Android application and can be opened
directly in Android Studio.

## Quick Start

1. Generate a key pair with the Crypto Universal CLI and store the keys in your
   app (implementation left to the developer).
2. From this directory, build and install the debug APK:
   ```
   ./gradlew installDebug
   ```
3. Launch the app and tap **Enable Secure Keyboard**. This opens the system
   input method settings where you can enable the keyboard.
4. Select **Secure Keyboard** as your input method. Compose a message, press the
   **Encrypt** button and the keyboard will insert the encrypted text.

Incoming ciphertext can be decrypted in a similar way by loading the private
key and calling the RSA decrypt function.
