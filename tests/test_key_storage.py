import base64
from pathlib import Path

from crypto_universal.interface import generate_keypair, MessagingCrypto
from crypto_universal.key_storage import save_private_key_encrypted, load_private_key_encrypted


def test_key_roundtrip(tmp_path):
    priv, pub = generate_keypair()
    key_file = tmp_path / "priv.enc"
    save_private_key_encrypted(priv, key_file, "pw")
    loaded = load_private_key_encrypted(key_file, "pw")
    assert loaded == priv


def test_integration_decrypt(tmp_path):
    priv, pub = generate_keypair()
    key_file = tmp_path / "priv.enc"
    save_private_key_encrypted(priv, key_file, "pw")
    mc_enc = MessagingCrypto.from_pem(public_pem=pub)
    mc_dec_priv = load_private_key_encrypted(key_file, "pw")
    mc_dec = MessagingCrypto.from_pem(private_pem=mc_dec_priv)
    token = mc_enc.encrypt("hello")
    assert mc_dec.decrypt(token) == "hello"

