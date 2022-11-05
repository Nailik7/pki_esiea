from distutils.command.config import config
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




class certificate():
    
    def __init__(self, configfile : list):
        
        self.configfile = configfile
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
        conf = get.get_conf(self,self.configfile,"CA")
        private_key = genkey.generator_private_key_rsa(self,os.path.join(path_ca,conf["privatekey"] + ".pem"))
        generator.generator_cert_ca(self,private_key, os.path.join(path_ca,conf["filename"] + ".pem"), conf) #On appelle la méthode pour générer un certificat CA, en paramètre on utilise notre propre clé pribe et on s'autosigne car on est l'autorité racine
        
        
    def create_ra(self,path_ca : str):       
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA"))    #On crée le dossier contenant le certificat du RA et sa clé privé
        except OSError as e :
            print("Le dossier existe déja")
            pass

        path_ra = os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA") #On crée une variable contenant le chemin du dossier des certificats et la clé privé de l'autorité d'enregistrement
        conf= get.get_conf(self,self.configfile,"RA") #On récupère la configuration du RA dans le fichier Config_CA.json
        ra_private_key = genkey.generator_private_key_rsa(self,os.path.join(path_ra,conf["privatekey"] + ".pem"))
        
        with open(os.path.join(path_ca,get.get_conf(self,self.configfile,"CA")["filename"] + ".pem"), "rb") as ca_public_key_file :
            ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())
        
        with open(os.path.join(path_ca,get.get_conf(self,self.configfile,"CA")["privatekey"] + ".pem"), "rb") as ca_private_key_file :
            ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), password=None,backend= default_backend())
            
        generator.generator_cert_ra(self,ca_public_key,ca_private_key, ra_private_key, os.path.join(path_ra,conf["filename"] + ".pem"), conf) #On appelle la méthode pour générer un certificat RA, avec en paramètre la clé privé et publique du certificat d'autorié et la clé privé et publique de l'autorité d'enregistrement

        
    def create_client(self,path_ra : str, type_key : str): 
        
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Client")) #On crée le dossier contenant les certificats clients
        
        except OSError as e :
            print("Le dossier existe déja")
            pass
        
        path_client = os.path.join(os.path.dirname(sys.argv[0]),"Client") #On crée une variable contenant le chemin du dossier des certificats clients 
        
        if type_key == "RSA": #Si le paramètre de type_key c'est RSA
            csr_private_key = genkey.generator_private_key_rsa(self,os.path.join(path_client,"cdiscount.pem")) #On généère une clé privé de type RSA
        elif type_key == "DSA": #Si le paramètre de type_key c'est DSA
            csr_private_key = genkey.generator_private_key_dsa(self,os.path.join(path_client,"cdiscount.pem")) #On génère une clé privé de type DSA
        
        conf = {"Country" : "FR", "State" :"IDF", "Localisation" : "Paris", "Organization" : "Cdiscount", "Ressource name" : "Finance",  
                        "Hostname" : "cdiscount.com",  "DNS" : "localhost"}
        
        generator.create_request_client(self,csr_private_key,os.path.join(path_client,"cdiscount_cert.pem"),conf,"MD5") #On genère une requête de certificat client en appelant la méthode csr, et qui prend en paramètre la clé publique et l'aglo de hashage

        with open(os.path.join(path_client,"cdiscount_cert.pem"), "rb") as csr_file :
            csr = x509.load_pem_x509_csr(csr_file.read(), default_backend()) #On récupère les données de la requête de certificat client dans la variable csr


        with open(os.path.join(path_ra,"ra_cert.pem"), "rb") as ra_public_key_file :
            ra_public_key = x509.load_pem_x509_certificate(ra_public_key_file.read(), default_backend()) #On récupère les données du certificat d'autorité d'enregistrement


        with open(os.path.join(path_ra,"ra-private-key.pem"), "rb") as ra_private_key_file :
            ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=None,backend= default_backend()) #On récupère la clé privé de l'autorité d'enregistrement
    
        print("\nSignature du csr par le RA :",signing.sign_client(self,csr, ra_public_key, ra_private_key, os.path.join(path_client,"cdiscount_cert.pem"),"MD5")) #Si auparavant totu est validé, alors on signe le certificat

    
    
    
    def create_crl(self,path_ra : str):
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"crl")) #On crée le dossier de la liste révocation de certificat 
        
        except OSError as e :
            print("Le dossier existe déja") #Si le dossier existe déja on n'écrase pas l'ancien dossier
            pass

        with open(os.path.join(path_ra,get.get_conf(self,self.configfile,"RA")["filename"] + ".pem"), "rb") as ra_public_key_file :
            ra_public_key = x509.load_pem_x509_certificate(ra_public_key_file.read(), default_backend()) #On recupère les données de la clé publique du certificat d'autorité d'enregistrement

        path_crl = os.path.join(os.path.dirname(sys.argv[0]),"Crl")
        
        with open(os.path.join(path_ra,get.get_conf(self,self.configfile,"RA")["privatekey"] + ".pem"), "rb") as ra_private_key_file :
            ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=None,backend= default_backend()) #On recupère la clé privé du certificat d'autorité d'enregistrement
        generator.generator_crl(self,ra_private_key,ra_public_key,os.path.join(path_crl,"crl_cert.pem")) #On va générer un cerfiticat qui va contenir la liste des certificats révoqués

    
    
def parse_args()-> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file", required=True, dest="config", nargs='+')
    return parser.parse_args()
            
        


def main():
    args = parse_args()
    configfile = args.config
    ca = certificate(configfile) #On crée une instance de la classe Certifificate 
    
if __name__ == "__main__": 
    main()