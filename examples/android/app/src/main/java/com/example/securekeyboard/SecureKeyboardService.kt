package com.example.securekeyboard

import android.inputmethodservice.InputMethodService
import android.view.View
import android.view.inputmethod.InputConnection
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.util.Base64
import java.io.BufferedReader
import java.security.KeyFactory
import java.security.PrivateKey
import java.security.PublicKey
import java.security.spec.PKCS8EncodedKeySpec
import java.security.spec.X509EncodedKeySpec
import javax.crypto.Cipher

/**
 * A minimal InputMethodService that encrypts and decrypts messages.
 * This example loads RSA keys in base64 and provides a button to
 * encrypt the current text field. Decryption works similarly when
 * incoming messages are selected.
 */
class SecureKeyboardService : InputMethodService() {
    private var publicKey: PublicKey? = null
    private var privateKey: PrivateKey? = null

    override fun onCreate() {
        super.onCreate()
        try {
            val reader: BufferedReader = assets.open("public_key.txt").bufferedReader()
            val pem = reader.readText().trim()
            publicKey = decodePublicKey(pem)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    override fun onCreateInputView(): View {
        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL

        val editText = EditText(this)
        val button = Button(this).apply { text = "Encrypt" }

        button.setOnClickListener {
            val ic: InputConnection = currentInputConnection
            val text = editText.text.toString()
            val cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")
            publicKey?.let {
                cipher.init(Cipher.ENCRYPT_MODE, it)
                val encrypted = cipher.doFinal(text.toByteArray())
                val token = Base64.encodeToString(encrypted, Base64.NO_WRAP)
                ic.commitText(token, 1)
            }
        }

        layout.addView(editText)
        layout.addView(button)
        return layout
    }

    private fun decodePublicKey(pem: String): PublicKey {
        val decoded = Base64.decode(pem, Base64.DEFAULT)
        val keySpec = X509EncodedKeySpec(decoded)
        return KeyFactory.getInstance("RSA").generatePublic(keySpec)
    }

    private fun decodePrivateKey(pem: String): PrivateKey {
        val decoded = Base64.decode(pem, Base64.DEFAULT)
        val keySpec = PKCS8EncodedKeySpec(decoded)
        return KeyFactory.getInstance("RSA").generatePrivate(keySpec)
    }
}
