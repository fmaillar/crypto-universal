import os
import sys

# ensure src directory is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from crypto_universal.interface import generate_keypair, MessagingCrypto


def test_roundtrip():
    priv, pub = generate_keypair()
    mc_enc = MessagingCrypto.from_pem(public_pem=pub)
    mc_dec = MessagingCrypto.from_pem(private_pem=priv)
    plaintext = "secret message"
    token = mc_enc.encrypt(plaintext)
    assert mc_dec.decrypt(token) == plaintext
