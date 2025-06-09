from __future__ import annotations

import argparse
import base64
import getpass
from pathlib import Path

from src.crypto_universal.interface import generate_keypair, MessagingCrypto
from src.crypto_universal.key_storage import (
    save_private_key_encrypted,
    load_private_key_encrypted,
)


def _prompt_password(confirm: bool = False) -> str:
    pwd = getpass.getpass("Password: ")
    if confirm:
        if pwd != getpass.getpass("Confirm: "):
            raise ValueError("Passwords do not match")
    return pwd


def cmd_generate(args: argparse.Namespace) -> None:
    priv, pub = generate_keypair()
    password = _prompt_password(confirm=True)
    save_private_key_encrypted(priv, args.path, password)
    print(f"Encrypted private key written to {args.path}")
    if args.public_out:
        Path(args.public_out).write_bytes(base64.b64encode(pub))
        print(f"Public key written to {args.public_out}")
    else:
        print(base64.b64encode(pub).decode())


def cmd_show(args: argparse.Namespace) -> None:
    password = _prompt_password()
    priv = load_private_key_encrypted(args.path, password)
    print(base64.b64encode(priv).decode())


def cmd_decrypt(args: argparse.Namespace) -> None:
    password = _prompt_password()
    priv = load_private_key_encrypted(args.path, password)
    mc = MessagingCrypto.from_pem(private_pem=priv)
    token = Path(args.infile).read_text().strip()
    plaintext = mc.decrypt(token)
    Path(args.out).write_text(plaintext)


def main() -> None:
    parser = argparse.ArgumentParser(description="Private key manager")
    sub = parser.add_subparsers(dest="cmd")

    g = sub.add_parser("generate")
    g.add_argument("--path", default="private.key", help="Encrypted key path")
    g.add_argument("--public-out", help="File to write public key")

    s = sub.add_parser("show")
    s.add_argument("--path", default="private.key", help="Encrypted key path")

    d = sub.add_parser("decrypt")
    d.add_argument("--path", default="private.key", help="Encrypted key path")
    d.add_argument("--in", dest="infile", required=True, help="Ciphertext file")
    d.add_argument("--out", required=True, help="Plaintext output file")

    args = parser.parse_args()
    if args.cmd == "generate":
        cmd_generate(args)
    elif args.cmd == "show":
        cmd_show(args)
    elif args.cmd == "decrypt":
        cmd_decrypt(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
