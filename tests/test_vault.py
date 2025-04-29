def test_vault_roundtrip(tmp_path):
    from cryptography.fernet import Fernet
    key=Fernet.generate_key()
    f=Fernet(key)
    data=b'secret'
    enc=f.encrypt(data)
    dec=f.decrypt(enc)
    assert dec==data
