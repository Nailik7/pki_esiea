import sys, os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
import cryptography
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography import *
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from revoke import revoke


class verif_parse():
    
    def __init__(self):
        path_client = os.path.join(os.path.dirname(sys.argv[0]),"Client")
        path_ra = os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA") 
        self.verifyIssuer(os.path.join(path_ra,"ra_cert.pem"), os.path.join(path_client,"cdiscount_cert.pem"))
        self.parse(os.path.join(os.path.join(path_client,"cdiscount_cert.pem")))
        self.expiration(os.path.join(path_client,"cdiscount_cert.pem"))
        revoke.check_cert_is_revoke(self, os.path.join(path_client,"cdiscount_cert.pem"))
    
    def verifyIssuer(self,issuerCertificate, subjectCertificate) :
        
        with open(issuerCertificate, "rb") as issuer_file:
            issuer_public_key = x509.load_pem_x509_certificate(issuer_file.read(), default_backend())
            
        with open(subjectCertificate, "rb") as subject_file :
            subject_public_key = x509.load_pem_x509_certificate(subject_file.read(), default_backend())
        
        issuerPublicKey = issuer_public_key.public_key()    
        verifier = issuerPublicKey.verify(data = subject_public_key.tbs_certificate_bytes, signature=subject_public_key.signature, 
                                          padding = padding.PKCS1v15(),algorithm =subject_public_key.signature_hash_algorithm)
        print(type(subject_public_key.tbs_certificate_bytes))
        if verifier == None :
            print("Le certificat est bien signe par l'autorite d'enregistrement")
        else :
            print("ajout",revoke.add_revoke(self,subject_public_key))
    
    def expiration(self,cert_file : str):
        with open(cert_file, 'rb+') as file :
            X509_cert = x509.load_pem_x509_certificate(file.read(),default_backend())
        if X509_cert.not_valid_after <= datetime.utcnow() :
            print("Le certificat a expiré ")
            revoke.add_revoke(self,X509_cert)
        else :
            print("Le certificat n'a pas encore expiré")
            
          
    def parse(self,cert_file : str):
        with open(cert_file, 'rb+') as file : #On charge le certificat à parser 
            X509_cert = x509.load_pem_x509_certificate(file.read(),default_backend()) 
            subject = str(X509_cert.subject).replace("<","").replace(">","").replace("Name","").replace("(", "").replace(")", "").split(",") #On crée une varaible qui recupère tous ses attributs en string, et on supprilme tous les caractères spéciaux 
            
            if X509_cert.issuer is not None : #Si le certificat est issu d'une autorité 
                Issuer = str(X509_cert.issuer).replace("<","").replace(">","").replace("Name","").replace("(", "").replace(")", "").split(",")
                issuer_dict = { 
                                'Country ' : Issuer[0][Issuer[0].find('='):].replace("=",""), 
                                'State' : Issuer[1][Issuer[1].find('='):].replace("=",""),
                                'Localisation' : Issuer[2][Issuer[2].find('='):].replace("=",""),
                                'Organisation' : Issuer[3][Issuer[3].find('='):].replace("=",""),
                                'Organisation unit' : Issuer[4][Issuer[4].find('='):].replace("=",""),
                                'Common Name' : Issuer[5][Issuer[5].find('='):].replace("=","")
                            
                            } #On afffiche dans un dictionnaire tous les attributs de l'autorité, et on supprime le signe "=" et tout ce qui est avant pour un meilleur affichage 

            subject_dict = {
                
                            'Country ' : subject[0][subject[0].find('='):].replace("=",""),
                            'State' : subject[1][subject[1].find('='):].replace("=",""),
                            'Localisation' : subject[2][subject[2].find('='):].replace("=",""),
                            'Organisation' : subject[3][subject[3].find('='):].replace("=",""),
                            'Organisation unit' : subject[4][subject[4].find('='):].replace("=",""),
                            'Common Name' : subject[5][subject[5].find('='):].replace("=",""),
                            'Signature algorithm ' : X509_cert.signature_algorithm_oid._name,
                            'Algorithm hash ' : X509_cert.signature_hash_algorithm.name,
                            'Serial Number' : X509_cert.serial_number,
                            'Cerfificate expire after ' : str(X509_cert.not_valid_after)    
                        } #On afffiche dans un dictionnaire tous les attributs du certificat, et on supprime le signe "=" et tout ce qui est avant pour un meilleur affichage 
            print(subject_dict,issuer_dict)
            
        
def main():
    a = verif_parse()
    
    
if __name__ == "__main__": 
    main()