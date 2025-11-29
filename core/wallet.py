import ecdsa
import hashlib
import base64

class Wallet:
    def __init__(self, private_key_hex=None):
        if private_key_hex:
            self.private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
        else:
            self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
        pub_key_bytes = self.public_key.to_string()
        sha256_bpk = hashlib.sha256(pub_key_bytes).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        return 'H' + base64.b32encode(ripemd160_bpk).decode('utf-8')[:30]

    def get_private_key(self):
        return self.private_key.to_string().hex()