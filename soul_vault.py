"""
soul_vault.py - Encrypt+Sign or Decrypt+Verify vault memory
"""

import base64
import json
import os
import getpass
import sys
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

VAULT_ENC = "vault_memory.json.enc"
VAULT_SIG = "vault_memory.json.sig"
MEMORY_JSON = "memory.json"

def derive_key(passphrase):
    return base64.urlsafe_b64encode(hashlib.sha256(passphrase.encode()).digest())

def encrypt_signed(privkey_path):
    if not os.path.exists(MEMORY_JSON):
        print("No memory.json found.")
        return
    passphrase = getpass.getpass("Enter encryption passphrase: ")
    key = derive_key(passphrase)
    fernet = Fernet(key)
    with open(MEMORY_JSON, "rb") as f:
        data = f.read()
    enc = fernet.encrypt(data)
    with open(VAULT_ENC, "wb") as f:
        f.write(enc)
    # signing
    with open(privkey_path, "rb") as f:
        sk = serialization.load_pem_private_key(f.read(), password=None)
    sig = sk.sign(enc)
    with open(VAULT_SIG, "wb") as f:
        f.write(sig)
    print("[OK] Vault encrypted and signed.")

def decrypt_verify(pubkey_path):
    if not os.path.exists(VAULT_ENC) or not os.path.exists(VAULT_SIG):
        print("No vault or signature found.")
        return
    with open(pubkey_path, "rb") as f:
        pk = serialization.load_pem_public_key(f.read())
    enc = open(VAULT_ENC, "rb").read()
    sig = open(VAULT_SIG, "rb").read()
    try:
        pk.verify(sig, enc)
    except Exception as e:
        print(f"[ERROR] Signature verification failed: {e}")
        return
    passphrase = getpass.getpass("Enter decryption passphrase: ")
    key = derive_key(passphrase)
    fernet = Fernet(key)
    try:
        dec = fernet.decrypt(enc)
    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}")
        return
    with open(MEMORY_JSON, "wb") as f:
        f.write(dec)
    print("[OK] memory.json restored and verified.")

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("encrypt-signed", "decrypt-verify"):
        print("Usage: python soul_vault.py [encrypt-signed|decrypt-verify] keyfile.pem")
        return
    if sys.argv[1] == "encrypt-signed":
        encrypt_signed(sys.argv[2])
    else:
        decrypt_verify(sys.argv[2])

if __name__ == "__main__":
    main()
