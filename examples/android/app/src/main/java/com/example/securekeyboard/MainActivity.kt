package com.example.securekeyboard

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.provider.Settings

import android.widget.Button

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val button = Button(this).apply {
            text = "Enable Secure Keyboard"
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_INPUT_METHOD_SETTINGS))

            }
        }
        setContentView(button)
    }
}
