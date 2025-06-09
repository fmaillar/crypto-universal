from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def generate_keypair() -> Tuple[bytes, bytes]:
    """Generate a new RSA private/public key pair.

    Returns a tuple ``(private_pem, public_pem)`` containing the keys in PEM
    format.
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


@dataclass
class MessagingCrypto:
    """Wrapper for asymmetric RSA encryption and decryption."""

    private_key: rsa.RSAPrivateKey | None = None
    public_key: rsa.RSAPublicKey | None = None

    def __post_init__(self) -> None:
        if self.private_key is None and self.public_key is None:
            raise ValueError("At least one of private_key or public_key is required")
        if self.private_key and not self.public_key:
            self.public_key = self.private_key.public_key()

    @classmethod
    def from_pem(cls, private_pem: bytes | None = None, public_pem: bytes | None = None) -> "MessagingCrypto":
        private = (
            serialization.load_pem_private_key(private_pem, password=None)
            if private_pem
            else None
        )
        public = (
            serialization.load_pem_public_key(public_pem) if public_pem else None
        )
        return cls(private_key=private, public_key=public)

    def encrypt(self, plaintext: str) -> str:
        if not self.public_key:
            raise ValueError("Public key is required for encryption")
        ciphertext = self.public_key.encrypt(
            plaintext.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return base64.b64encode(ciphertext).decode("utf-8")

    def decrypt(self, token: str) -> str:
        if not self.private_key:
            raise ValueError("Private key is required for decryption")
        ciphertext = base64.b64decode(token.encode("utf-8"))
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext.decode("utf-8")
