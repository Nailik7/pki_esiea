import cryptography
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from datetime import datetime, timedelta

from cryptography import x509

from cryptography.x509.oid import NameOID

from cryptography.hazmat.primitives import hashes
import os, sys
import logging


class genkey():
    
    def generator_private_key_rsa(self,filename: str):
        logging.info("Génération de la clé privé RSA en cours")
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend()) 
        with open(filename, "wb") as file:
            file.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.TraditionalOpenSSL,encryption_algorithm=serialization.NoEncryption()))
            logging.info("Génération de la cle privé RSA termine")
        return private_key
    
    def generator_private_key_dsa(self,filename: str):
        logging.info("Génération de la clé privé DSA en cours")
        private_key = dsa.generate_private_key(key_size=2048, backend=default_backend()) 
        with open(filename, "wb") as file:
            file.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.TraditionalOpenSSL,encryption_algorithm=serialization.NoEncryption()))
            logging.info("Génération de la clé privé SA termine")
        return private_key