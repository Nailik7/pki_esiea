from generator_key import generate_private_key, generate_public_key
from generator_key import generate_public_key, generate_private_key
from csr import generate_csr
from csr import sign_csr

from getpass import getpass
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def generate_ca_and_ra():

  private_key = generate_private_key("ca_private-key.pem", "capassword")


  generate_public_key(
    private_key,
    filename="ca_cert.pem",
    country="FR",
    state="IDF",
    locality="Paris",
    org="CA Novaly",
    hostname="novaly-ca.com",
  )
  
  #Genreate RA
  ra_private_key = generate_private_key(
    "ra-private-key.pem", "rapassword"
  )
  ra_private_key

  generate_csr(
    ra_private_key,
    filename="ra_cert.pem",
    country="FR",
    state="ARA",
    locality="Lyon",
    org="Encrtypt",
    alt_names=["localhost"],
    hostname="encrypt.com",
  )

    
  pwd = "capassword"
  passo = pwd.encode("utf_8")
  csr_file = open("ra_cert.pem", "rb")
  csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())
  print("csr:",csr)
  ca_public_key_file = open("ca_cert.pem", "rb")
  ca_public_key = x509.load_pem_x509_certificate(
    ca_public_key_file.read(), default_backend())
  print("\nca public key :",ca_public_key)

  ca_private_key_file = open("ca_private-key.pem", "rb")

  ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), password=passo,backend= default_backend())
  print("Ici c'est correcte")
  print("\nprivate_key: ",ca_private_key)

  print("\nSignature du RA par le CA :",sign_csr(csr, ca_public_key, ca_private_key, "ra_cert.pem"))