from fileinput import filename
from generator_key import *
from csr import *
from getpass import getpass
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def generate_csr():
    csr_private_key = generator_private_key("cdiscount.pem", "cpassword")
    tab_name_csr = ["Country : ", "FR", "State : ","IDF", "Localisation : ", "Paris", "Organization : ","Cdiscount", "Nom ressource : ", "Finance",  "alt_names :", "localhost", 
                    "Hostname : ", "cdiscount.com"]
    create_csr(csr_private_key,"cdiscount_cert.pem",tab_name_csr)

    pwd = "rapassword"
    passo = pwd.encode("utf_8")
    with open("cdiscount_cert.pem", "rb") as csr_file :
        csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())
        print("csr:",csr)

    with open("ra_cert.pem", "rb") as ra_public_key_file :
        ra_public_key = x509.load_pem_x509_certificate(ra_public_key_file.read(), default_backend())
        print("\nra public key :",ra_public_key)


    with open("ra-private-key.pem", "rb") as ra_private_key_file :
        ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=passo,backend= default_backend())


        print("\nprivate_key: ",ra_private_key)
        print("\nSignature du csr par le RA :",sign_csr(csr, ra_public_key, ra_private_key, "ra_cert.pem"))