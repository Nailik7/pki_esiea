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

from get import get 


class generator():
    def generator_cert_ca(self,private_key, filename, conf): 
        subject = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, conf["Country"]),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, conf["State"]),
                x509.NameAttribute(NameOID.LOCALITY_NAME, conf["Localisation"]),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, conf["Organization"]),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, conf["Ressource name"]),
                x509.NameAttribute(NameOID.COMMON_NAME, conf["Hostname"]),
            ]) #On ajoute la configuration au certificat, le CN, le nom le pays ect 



        builder = (

                x509.CertificateBuilder()

                .subject_name(subject)

                .issuer_name(subject)

                .public_key(private_key.public_key())

                .serial_number(x509.random_serial_number())

                .not_valid_before(datetime.utcnow())

                .not_valid_after(datetime.utcnow() + timedelta(days=360))

                .add_extension(x509.BasicConstraints(ca=True,path_length=None), critical=True))  #On construit le certificat avec la conf au-dessus, ainsi on lui ajout les attributs d'expirations et sa clé publique, la conf sera stocké dans la variable builder



        public_key = builder.sign(private_key, hashes.SHA256(), default_backend()) #Le certificat d'atorite, s'auto signe avec sa cle prive
        with open(filename, "wb") as certfile:

            certfile.write(public_key.public_bytes(serialization.Encoding.PEM)) #On gén_re le fichier de certificat de l'autorité d'enregistrement

        return public_key
        
            
            

    def generator_cert_ra(self,ca_public_key,private_key_ca,private_key, filename, conf):

        subject = x509.Name(

           [
                x509.NameAttribute(NameOID.COUNTRY_NAME, conf["Country"]),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, conf["State"]),
                x509.NameAttribute(NameOID.LOCALITY_NAME, conf["Localisation"]),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, conf["Organization"]),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, conf["Ressource name"]),
                x509.NameAttribute(NameOID.COMMON_NAME, conf["Hostname"]),
           ]) #On ajoute la configuration au certificat, le CN, le nom le pays ect 

        builder = (
                x509.CertificateBuilder()

                .subject_name(subject)

                .issuer_name(ca_public_key.subject)

                .public_key(private_key.public_key())

                .serial_number(x509.random_serial_number())

                .not_valid_before(datetime.utcnow())

                .not_valid_after(datetime.utcnow() + timedelta(days=360))

                .add_extension(x509.BasicConstraints(ca=False,path_length=None), critical=True))


        public_key = builder.sign(private_key, hashes.SHA256(), default_backend()) #On signe le certificat d'autorité d'enregistrement par lui même
        public_key = builder.sign(private_key_ca, hashes.SHA256(), default_backend())  #Le certfificat est également signé oar l'autorité 
        with open(filename, "wb") as certfile:

            certfile.write(public_key.public_bytes(serialization.Encoding.PEM)) #On genère le fichier certificat RA 


        return public_key



    def create_request_client(self,private_key, filename, conf, algo : str):

        subject = x509.Name(

           [
                x509.NameAttribute(NameOID.COUNTRY_NAME, conf["Country"]),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, conf["State"]),
                x509.NameAttribute(NameOID.LOCALITY_NAME, conf["Localisation"]),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, conf["Organization"]),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, conf["Ressource name"]),
                x509.NameAttribute(NameOID.COMMON_NAME, conf["Hostname"]),
           ]) #On ajoute la configuration au certificat, le CN, le nom le pays ect 
        dns_names = []
        for name in conf.get("DNS", []):

            dns_names.append(x509.DNSName(name))

        dns = x509.SubjectAlternativeName(dns_names)


        builder = (x509.CertificateSigningRequestBuilder().subject_name(subject).add_extension(dns, critical=False)) #Toute la configuration sera contenu dans la variable builder
        
        
        client = builder.sign(private_key,get.get_algo_hash(self,algo), default_backend()) #Le client auto-signe le certificat avec sa clé privé
        

        with open(filename, "wb") as clientfile:

            clientfile.write(client.public_bytes(serialization.Encoding.PEM)) #On genère le fichier du certificat client 

        return client  
    
    def generator_crl(self,ra_private_key,ra_public_key, filename): #Cette fonction va permetter de generer un certificat de revocation
        builder = (
                x509.CertificateRevocationListBuilder()

                .issuer_name(ra_public_key.subject)

                .last_update(datetime.now()-timedelta(hours=1))

                .next_update(datetime.now() + timedelta(1) - timedelta(hours=1))) #On lui rajoute une autorité qui est le RA (l'autorité d'enregsitrement), également on lui rajoute les dèrenières maj
        
        crl = builder.sign(ra_private_key, hashes.SHA256(), default_backend()) 
        
        with open(filename, "wb") as crlfile:

                crlfile.write(crl.public_bytes(serialization.Encoding.PEM)) #On génère le fichier du certificat de revocation 

        

        