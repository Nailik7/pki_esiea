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
import json




class certificate():  
    def create_ca(self, configfile):
        
        try:
            logging.info(f"Creation du certificat de l'autorite racine") 
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Certificate-CA")) #On crée le dossier contenant le certificat d'autorité racine et sa clé privé
            logging.info(f"Creation du dossier de l'autorité racine")
                                              
        except OSError as e :
            logging.info(f"Creation du dossier de l'autorite racine a echoue, le dossier existe deja")
            pass
        
        path_ca = os.path.join(os.path.dirname(sys.argv[0]),"Certificate-CA") 
        conf = get.get_conf(self,self.configfile,"CA")
        private_key = genkey.generator_private_key_rsa(self,os.path.join(path_ca,conf["privatekey"] + ".pem"))
        logging.info(f"Generation du certificat racine en cours")
        generator.generator_cert_ca(self,private_key, os.path.join(path_ca,conf["filename"] + ".pem"), conf) #On appelle la méthode pour générer un certificat CA, en paramètre on utilise notre propre clé pribe et on s'autosigne car on est l'autorité racine
        
        
    def create_ra(self,path_ca : str, configfile):  
            
        try:
            logging.info(f"Creation du certificat de l'autorite d'enregistrement") 
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA")) #On crée le dossier contenant le certificat du RA et sa clé privé
            logging.info(f"Creation du dossier de l'atorite d'enregistrement")  
        except OSError as e :
            logging.info(f"Le dossier de l'autorite d'enregistrement existe deja")
            pass

        path_ra = os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA") #On crée une variable contenant le chemin du dossier des certificats et la clé privé de l'autorité d'enregistrement
        conf= get.get_conf(self,self.configfile,"RA") #On récupère la configuration du RA dans le fichier Config_RA.json
        ra_private_key = genkey.generator_private_key_rsa(self,os.path.join(path_ra,conf["privatekey"] + ".pem"))
        
        with open(os.path.join(path_ca,get.get_conf(self,self.configfile,"CA")["filename"] + ".pem"), "rb") as ca_public_key_file :
            logging.info(f"On decode la cle publique du CA")
            ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())
        
        with open(os.path.join(path_ca,get.get_conf(self,self.configfile,"CA")["privatekey"] + ".pem"), "rb") as ca_private_key_file :
            logging.info(f"On decode la cle publique du RA")
            ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), password=None,backend= default_backend())
        
        logging.info(f"Generation du certificat d'autorite d'enregistrement en cours")    
        generator.generator_cert_ra(self,ca_public_key,ca_private_key, ra_private_key, os.path.join(path_ra,conf["filename"] + ".pem"), conf) #On appelle la méthode pour générer un certificat RA, avec en paramètre la clé privé et publique du certificat d'autorié et la clé privé et publique de l'autorité d'enregistrement

        
    def create_client(self, type_key : str, country : str, state : str, localisation : str, organisation : str, ressource : str, hostname : str, dns : str, filename : str, algo : str): 
        
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"Client")) #On crée le dossier contenant les certificats clients
            logging.info(f"Creation du dossier du dossier client")
        
        except OSError as e :
            logging.info(f"Le dossier client existe deja")
            pass
                
        path_client = os.path.join(os.path.dirname(sys.argv[0]),"Client") #On crée une variable contenant le chemin du dossier des certificats clients 
        conf = {"Country" : country, "State" :state, "Localisation" : localisation, "Organization" : organisation, "Ressource name" : ressource,  
                        "Hostname" : hostname,  "DNS" : dns, "Filename" : filename}
        
        with open("Config_client" + ".json", "wb") as file:
                file.write(json.dumps(conf).encode())
        
        if type_key == "RSA": #Si le paramètre de type_key c'est RSA
            csr_private_key = genkey.generator_private_key_rsa(self,os.path.join(path_client,get.get_conf_client(self,"client") + ".pem")) #On génère une clé privé de type RSA
        elif type_key == "DSA": #Si le paramètre de type_key c'est DSA
            csr_private_key = genkey.generator_private_key_dsa(self,os.path.join(path_client,get.get_conf_client(self,"client")+".pem")) #On génère une clé privé de type DSA
        else:
            csrpkey = type_key
            with open(csrpkey, "rb") as key:
               csr_private_key = serialization.load_pem_private_key(key.read(), password=None,backend= default_backend())
                   
        generator.create_request_client(self,csr_private_key,os.path.join(path_client,get.get_conf_client(self,"client")+"_cert.pem"),conf,algo) #On genère une requête de certificat client en appelant la méthode csr, et qui prend en paramètre la clé publique et l'aglo de hashage

        with open(os.path.join(path_client, get.get_conf_client(self,"client")+"_cert.pem"), "rb") as csr_file :
            logging.info(f"On decode la requete du certificat client")
            csr = x509.load_pem_x509_csr(csr_file.read(), default_backend()) #On récupère les données de la requête de certificat client dans la variable csr


        with open(os.path.join(get.get_path(self,"ra"),"ra_cert.pem"), "rb") as ra_public_key_file :
            logging.info(f"On decode le certificat du RA")
            ra_public_key = x509.load_pem_x509_certificate(ra_public_key_file.read(), default_backend()) #On récupère les données du certificat d'autorité d'enregistrement


        with open(os.path.join(get.get_path(self,"ra"),"ra-private-key.pem"), "rb") as ra_private_key_file  :
            logging.info(f"On decode la cle prive du RA")
            ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=None,backend= default_backend()) #On récupère la clé privé de l'autorité d'enregistrement
        
        logging.info(f"Signature certificat client par le RA")
        signing.sign_client(self,csr, ra_public_key, ra_private_key, os.path.join(path_client,get.get_conf_client(self,"client")+"_cert.pem"),algo)

    
    
    
    def create_crl(self, configfile):
        try:
            os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"crl")) #On crée le dossier de la liste révocation de certificat 
        
        except OSError as e :
            print("Le dossier existe déja") #Si le dossier existe déja on n'écrase pas l'ancien dossier
            pass
        
        conf= get.get_conf(self,configfile,"RA")

        with open(os.path.join(get.get_path(self,"ra"),conf["filename"] + ".pem"), "rb") as ra_public_key_file :
            ra_public_key = x509.load_pem_x509_certificate(ra_public_key_file.read(), default_backend()) #On recupère les données de la clé publique du certificat d'autorité d'enregistrement

        path_crl = os.path.join(os.path.dirname(sys.argv[0]),"crl")
        
        with open(os.path.join(get.get_path(self,"ra"),get.get_conf(self,self.configfile,"RA")["privatekey"] + ".pem"), "rb") as ra_private_key_file :
            ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=None,backend= default_backend()) #On recupère la clé privé du certificat d'autorité d'enregistrement
        generator.generator_crl(self,ra_private_key,ra_public_key,os.path.join(path_crl,"crl_cert.pem")) #On va générer un cerfiticat qui va contenir la liste des certificats révoqués

    

            
        