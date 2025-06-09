from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode("utf-8"))


def save_private_key_encrypted(key: bytes, path: Union[str, Path], password: str) -> None:
    """Encrypt ``key`` with ``password`` and save to ``path``.

    The file format is ``salt || iv || tag || ciphertext``.
    """
    path = Path(path)
    salt = os.urandom(16)
    sym_key = _derive_key(password, salt)
    iv = os.urandom(12)
    aesgcm = AESGCM(sym_key)
    ct = aesgcm.encrypt(iv, key, None)
    ciphertext, tag = ct[:-16], ct[-16:]
    with open(path, "wb") as fh:
        fh.write(salt + iv + tag + ciphertext)


def load_private_key_encrypted(path: Union[str, Path], password: str) -> bytes:
    """Load and decrypt private key stored at ``path`` using ``password``."""
    data = Path(path).read_bytes()
    if len(data) < 44:
        raise ValueError("Invalid encrypted key file")
    salt = data[:16]
    iv = data[16:28]
    tag = data[28:44]
    ciphertext = data[44:]
    sym_key = _derive_key(password, salt)
    aesgcm = AESGCM(sym_key)
    return aesgcm.decrypt(iv, ciphertext + tag, None)
