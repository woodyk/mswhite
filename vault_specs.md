# SOULPACK Vault Format Specification

## Purpose
Vaults protect critical memories and long-term knowledge with both:
- **Encryption** (AES-256, passphrase-derived)
- **Signature** (Ed25519, private signing key)

## Files
- `vault_memory.json.enc` → Encrypted memory
- `vault_memory.json.sig` → Detached signature of encrypted vault
- `pubkey.pem` → Public key for verification

## Creation Workflow
1. Encrypt memory.json → vault_memory.json.enc
2. Sign vault_memory.json.enc → vault_memory.json.sig

## Verification on Boot
- Decrypt encrypted vault with user passphrase.
- Verify signature using pubkey.pem.
- Fail boot if signature check fails.

## Rationale
Memory confidentiality (encrypt) and memory integrity (sign) are orthogonal protections.
