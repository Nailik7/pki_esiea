from generator_key import *
from csr import *

from getpass import getpass
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def generate_ca_and_ra():

  private_key = generator_private_key("ca_private-key.pem", "capassword")
  tab_name_ca = ["Country : ", "FR", "State","IDF", "Localisation : ", "Paris", "Organization :","CA Novaly", "Nom ressource", "Administrateur :", "Hostname :", "novaly-ca.com"]
  
  
  generator_public_key(private_key,"ca_cert.pem", tab_name_ca)  
  ra_private_key = generator_private_key("ra-private-key.pem", "rapassword")

  tab_name_ra = ["Country : ", "FR", "State : ","IDF", "Localisation : ", "Paris", "Organization : ","RA Encrypt", "Nom ressource : ", "RH",  "alt_names :", "localhost", "Hostname : ",
                 "encrypt.com"]
  
  create_csr(ra_private_key, "ra_cert.pem", tab_name_ra)
  
   
  pwd = "capassword"
  passo = pwd.encode("utf_8")
  with open("ra_cert.pem", "rb") as csr_file :
    csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())
    print("csr:",csr)
  
  with open("ca_cert.pem", "rb") as ca_public_key_file :
    ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())
    print("\nca public key :",ca_public_key)

  
  with open("ca_private-key.pem", "rb") as ca_private_key_file :
    ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), password=passo,backend= default_backend())
    
 
  print("\nprivate_key: ",ca_private_key)
  print("\nAuto signature du CA :",sign_csr(ca_public_key, ca_public_key, ca_private_key, "ca_cert.pem"))
  print("\nSignature du RA par le CA :",sign_csr(csr, ca_public_key, ca_private_key, "ra_cert.pem"))
  