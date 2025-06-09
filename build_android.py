import argparse
import base64
import shutil
import subprocess
from pathlib import Path

from src.crypto_universal.interface import generate_keypair


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
    parser.add_argument("--key", help="path to public key file")
    parser.add_argument("--install", action="store_true", help="install the APK with adb")
    args = parser.parse_args()

    if args.key:
        key_path = Path(args.key)
    else:
        priv, pub = generate_keypair()
        key_path = Path("public_key.txt")
        key_path.write_bytes(base64.b64encode(pub))
        print("Generated new key pair. Private key:\n" + base64.b64encode(priv).decode())
        print("Public key written to", key_path)

    build_project(args.user, key_path, args.install)

    if not args.key:
        key_path.unlink()


if __name__ == "__main__":
    main()
