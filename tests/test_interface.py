import os
import sys

import pytest
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

def test_requires_key():
    try:
        MessagingCrypto()
    except ValueError:
        pass
    else:
        assert False, 'ValueError not raised'


def test_encrypt_decrypt_errors():
    priv, pub = generate_keypair()
    mc = MessagingCrypto.from_pem(private_pem=priv)
    # force missing public key
    mc.public_key = None
    with pytest.raises(ValueError):
        mc.encrypt('hi')
    mc = MessagingCrypto.from_pem(public_pem=pub)
    mc.private_key = None
    with pytest.raises(ValueError):
        mc.decrypt('token')
