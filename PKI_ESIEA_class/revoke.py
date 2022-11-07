
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import os, sys
from cryptography import *
from get import get 

class revoke():
    def add_revoke(self, client_cert):
        
        with open(os.path.join(get.get_path(self,"ra"),"ra-private-key.pem"), "rb") as ra_private_key_file : #On charge la clé prive du RA
            ra_private_key = serialization.load_pem_private_key(ra_private_key_file.read(), password=None,backend= default_backend())
        
        with open(os.path.join(get.get_path(self,"crl"),"crl_cert.pem"), "rb") as crl_file: #On charge le certificat de revocation
            crl = x509.load_pem_x509_crl(crl_file.read(), default_backend())            
        
        builder = (
                    x509.CertificateRevocationListBuilder()

                    .issuer_name(crl.issuer)

                    .last_update(crl.last_update)

                    .next_update(datetime.now() + timedelta(1, 0, 0))) #On ajouter qu'on ajoute une datde maj, qui montre qu'on modifie le certificat de revocation
        for i in range(0, len(crl)):
            builder = builder.add_revoked_certificate(crl[i]) 
            
        revoke = crl.get_revoked_certificate_by_serial_number(client_cert.serial_number)  #On recupere le numero de serie du certificat client (celui qu'on verifie)
        if not isinstance(revoke, x509.RevokedCertificate): #Si le certificat n'est pas encore revoqué 
            revoke_cert = x509.RevokedCertificateBuilder().serial_number(client_cert.serial_number).revocation_date(datetime.now()).build(backend=default_backend())   #On révoque le certificat client 
            builder = builder.add_revoked_certificate(revoke_cert) #On l'ajoute dans le certificat de revocation  
            
        crl_sign = builder.sign(private_key= ra_private_key,algorithm=hashes.SHA256(),backend=default_backend()) #Enfin on signe le certificat par l'autorité d'enregistrement
        with open(os.path.join(get.get_path(self,"crl"),"crl_cert.pem"), "wb") as file:

                    file.write(crl_sign.public_bytes(serialization.Encoding.PEM)) #On ecrase le fichier, avec le nouveau 
        
        
    def check_cert_is_revoke(self,client_cert : str): #Permet de savoir si le cerificat est déja revoqué 
        with open(os.path.join(get.get_path(self,"crl"),"crl_cert.pem"), "rb") as crl_file: #On charge le certificat de revocation 
            crl = x509.load_pem_x509_crl(crl_file.read(), default_backend())  
            
        with open(client_cert, 'rb+') as client_file: #On charge le certificat client 
            client = x509.load_pem_x509_certificate(client_file.read(), default_backend())
        
        revoke = crl.get_revoked_certificate_by_serial_number(client.serial_number) #On recupère son numéro de série 
        if isinstance(revoke, x509.RevokedCertificate): #Et on compare son numero de série s'il est déja présent
            print("Le certificat n'est plus valide, il est revoqué !")
            
        else :
            print("Le certificat est encore valide !")