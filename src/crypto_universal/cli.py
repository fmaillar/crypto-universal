import argparse
import base64

from .interface import MessagingCrypto, generate_keypair


def main():
    parser = argparse.ArgumentParser(description="Crypto Universal CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("generate-keys")

    enc = sub.add_parser("encrypt")
    enc.add_argument("public_key", help="base64 encoded public key")
    enc.add_argument("message", help="plaintext message")

    dec = sub.add_parser("decrypt")
    dec.add_argument("private_key", help="base64 encoded private key")
    dec.add_argument("token", help="base64 ciphertext")

    args = parser.parse_args()

    if args.command == "generate-keys":
        priv, pub = generate_keypair()
        print(base64.b64encode(priv).decode("utf-8"))
        print(base64.b64encode(pub).decode("utf-8"))
    elif args.command == "encrypt":
        pub = base64.b64decode(args.public_key.encode("utf-8"))
        mc = MessagingCrypto.from_pem(public_pem=pub)
        print(mc.encrypt(args.message))
    elif args.command == "decrypt":
        priv = base64.b64decode(args.private_key.encode("utf-8"))
        mc = MessagingCrypto.from_pem(private_pem=priv)
        print(mc.decrypt(args.token))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
