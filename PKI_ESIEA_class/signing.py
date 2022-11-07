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
    
    def sign_client(self, client, ra_public_key, ra_private_key, new_filename, algo: str):

        builder = ( #La variable builder va contenir les attributs du certificat client 

            x509.CertificateBuilder()

            .subject_name(client.subject)

            .issuer_name(ra_public_key.subject) #On ajoute la configuration de l'autorité d'enregistrement, qui est en contenu dans le fichier du certificat RA

            .public_key(client.public_key())

            .serial_number(x509.random_serial_number())

            .not_valid_before(datetime.utcnow())

            .not_valid_after( datetime.utcnow()+ timedelta(days=30))

        ) 
        
        for extension in client.extensions:

            builder = builder.add_extension(extension.value, extension.critical)

        public_key = builder.sign(private_key=ra_private_key,algorithm=get.get_algo_hash(self,algo),backend=default_backend()) #On signe le certificat client par l'autorité 


        with open(new_filename, "wb") as keyfile:
            keyfile.write(public_key.public_bytes(serialization.Encoding.PEM))  #On écrase l'ancien certificat client par celui qui est signé par l'autorité d'enregistrement 