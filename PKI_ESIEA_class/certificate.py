import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography import x509
import os, sys
import logging
from generator import generator
from key import genkey
from signing import signing
from get import get
from argparse import ArgumentParser, Namespace
#from parse_test import parse_test



class certificate():
    
    def __init__(self):
        self.create_ca()
        self.create_ra(get.get_path(self,"ca"))
        self.create_client(get.get_path(self,"ra"),"RSA")
        self.create_crl(get.get_path(self,"ra"))
        self.filelog = "certificate.log"
        logging.basicConfig(filename=self.filelog, level=logging.DEBUG) 
       
    
    def create_ca(self):
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Certificate-CA"))
                                              
        except OSError as e :
            print("Le dossier existe déja")
            pass
        
        path_ca = os.path.join(os.path.dirname(sys.argv[0]),"Certificate-CA") 
        private_key = genkey.generator_private_key_rsa(self,os.path.join(path_ca,"ca_private-key.pem"))
        conf = get.get_conf(self,"CA")
        generator.generator_cert_ca(self,private_key, os.path.join(path_ca,"ca_cert.pem"), conf)
  
        
        
    def create_ra(self,path_ca : str):       
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA"))       
        except OSError as e :
            print("Le dossier existe déja")
            pass

        path_ra = os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA")
        ra_private_key = genkey.generator_private_key_rsa(self,os.path.join(path_ra,"ra-private-key.pem"))
        conf= get.get_conf(self,"RA")
        
        with open(os.path.join(path_ca,"ca_cert.pem"), "rb") as ca_public_key_file :
            ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())

        
        with open(os.path.join(path_ca,"ca_private-key.pem"), "rb") as ca_private_key_file :
            ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), password=None,backend= default_backend())
            
        generator.generator_cert_ra(self,ca_public_key,ca_private_key, ra_private_key, os.path.join(path_ra,"ra_cert.pem"), conf)

        
    def create_client(self,path_ra : str, type_key : str):
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Client"))
        
        except OSError as e :
            print("Le dossier existe déja")
            pass
        path_client = os.path.join(os.path.dirname(sys.argv[0]),"Client")
        if type_key == "RSA":
            csr_private_key = genkey.generator_private_key_rsa(self,os.path.join(path_client,"cdiscount.pem"))
        elif type_key == "DSA":
            csr_private_key = genkey.generator_private_key_dsa(self,os.path.join(path_client,"cdiscount.pem"))
        
        conf = {"Country" : "FR", "State" :"IDF", "Localisation" : "Paris", "Organization" : "Cdiscount", "Ressource name" : "Finance",  
                        "Hostname" : "cdiscount.com",  "DNS" : "localhost"}
        
        generator.create_request_client(self,csr_private_key,os.path.join(path_client,"cdiscount_cert.pem"),conf,"MD5")

        with open(os.path.join(path_client,"cdiscount_cert.pem"), "rb") as csr_file :
            csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())


        with open(os.path.join(path_ra,"ra_cert.pem"), "rb") as ra_public_key_file :
            ra_public_key = x509.load_pem_x509_certificate(ra_public_key_file.read(), default_backend())


        with open(os.path.join(path_ra,"ra-private-key.pem"), "rb") as ra_private_key_file :
            ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=None,backend= default_backend())
    
        print("\nSignature du csr par le RA :",signing.sign_client(self,csr, ra_public_key, ra_private_key, os.path.join(path_client,"cdiscount_cert.pem"),"MD5"))

    
    
    
    def create_crl(self,path_ra : str):
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"crl"))
        
        except OSError as e :
            print("Le dossier existe déja")
            pass

        with open(os.path.join(path_ra,"ra_cert.pem"), "rb") as ra_public_key_file :
            ra_public_key = x509.load_pem_x509_certificate(ra_public_key_file.read(), default_backend())

        path_crl = os.path.join(os.path.dirname(sys.argv[0]),"Crl")
        
        with open(os.path.join(path_ra,"ra-private-key.pem"), "rb") as ra_private_key_file :
            ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=None,backend= default_backend())
        generator.generator_crl(self,ra_private_key,ra_public_key,os.path.join(path_crl,"crl_cert.pem"))

    
    
def parse_args()-> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file", required=True, dest="config")
    return parser.parse_args()
            
        


def main():
    ca = certificate()
    
if __name__ == "__main__": 
    main()