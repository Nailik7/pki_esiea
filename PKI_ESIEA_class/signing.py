import cryptography
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

from cryptography import x509

from cryptography.x509.oid import NameOID

from cryptography.hazmat.primitives import hashes
import os, sys
from get import get

class signing():
    
    def sign_client(self, csr, ca_public_key, ca_private_key, new_filename, algo: str):

        valid_from = datetime.utcnow()

        valid_until = valid_from + timedelta(days=30)


        builder = (

            x509.CertificateBuilder()

            .subject_name(csr.subject)

            .issuer_name(ca_public_key.subject)

            .public_key(csr.public_key())

            .serial_number(x509.random_serial_number())

            .not_valid_before(valid_from)

            .not_valid_after(valid_until)

        )
        
        for extension in csr.extensions:

            builder = builder.add_extension(extension.value, extension.critical)

        public_key = builder.sign(private_key=ca_private_key,algorithm=get.get_algo_hash(self,algo),backend=default_backend())


        with open(new_filename, "wb") as keyfile:
            keyfile.write(public_key.public_bytes(serialization.Encoding.PEM)) 