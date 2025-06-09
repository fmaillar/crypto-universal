# Android Secure Keyboard Example

This directory contains a minimal Gradle project that builds a custom
`InputMethodService` using Crypto Universal. The keyboard exposes an
**Encrypt** button which replaces the typed text with a base64
ciphertext.

## Building

1. From this directory run `./gradlew assembleDebug` or open the project in
   Android Studio.
2. Install `app/build/outputs/apk/debug/app-debug.apk` on your device.

## Onboarding Flow

After installing, launch the `Secure Keyboard` app. The only screen
contains a button that opens the system input method settings. Enable the
**Secure Keyboard** service and switch to it. When the keyboard is active
you can type a message, press **Encrypt**, and send the resulting token
through any chat application.
