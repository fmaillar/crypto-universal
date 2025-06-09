import argparse
import base64
import getpass
import shutil
import subprocess
from pathlib import Path

from cryptography.hazmat.primitives import serialization

from src.crypto_universal.interface import generate_keypair
from src.crypto_universal.key_storage import (
    load_private_key_encrypted,
    save_private_key_encrypted,
)


def build_project(user: str, key_file: Path, install: bool) -> None:
    root = Path(__file__).parent
    src_dir = root / "examples" / "android"
    dest_dir = root / "build" / user
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)

    assets = dest_dir / "app" / "src" / "main" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy(key_file, assets / "public_key.txt")

    subprocess.check_call(["gradle", "wrapper"], cwd=dest_dir)
    subprocess.check_call(["./gradlew", "assembleDebug"], cwd=dest_dir)

    if install:
        apk = dest_dir / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
        subprocess.check_call(["adb", "install", str(apk)], cwd=dest_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and install the Android app")
    parser.add_argument("--user", required=True, help="username for build directory")
    parser.add_argument("--public", help="path to public key file")
    parser.add_argument(
        "--private", default="private_key.enc", help="encrypted private key path"
    )
    parser.add_argument("--install", action="store_true", help="install the APK with adb")
    args = parser.parse_args()

    pub_file = Path(args.public) if args.public else Path("public_key.txt")
    priv_file = Path(args.private)

    if priv_file.exists():
        password = getpass.getpass("Private key password: ")
        priv_pem = load_private_key_encrypted(priv_file, password)
        priv = serialization.load_pem_private_key(priv_pem, password=None)
        pub_pem = priv.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    else:
        priv_pem, pub_pem = generate_keypair()
        password = getpass.getpass("Create password for private key: ")
        save_private_key_encrypted(priv_pem, priv_file, password)
        print(f"Encrypted private key saved to {priv_file}")

    pub_file.write_bytes(base64.b64encode(pub_pem))
    print("Public key written to", pub_file)

    build_project(args.user, pub_file, args.install)

    if not args.public:
        pub_file.unlink()


if __name__ == "__main__":
    main()
