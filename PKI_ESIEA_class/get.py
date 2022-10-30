from cryptography.hazmat.primitives import hashes
import os, sys, json

class get():
    
    def get_algo_hash(self,algorithm : str):
               
        if algorithm == "SHA256":
            return hashes.SHA256()
        elif algorithm == "MD5":
            return hashes.MD5()
        elif algorithm == "SHA1":
            return hashes.SHA1()
        elif algorithm == "SHA224":
            return hashes.SHA224()
        
        
    def get_path(self,type : str):
        
        if type == "ca":
            return os.path.join(os.path.dirname(sys.argv[0]),"Certificate-CA")
        elif type == "ra":
            return os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA")
        elif type == "client":
            return os.path.join(os.path.dirname(sys.argv[0]),"client")
        elif type == "crl":
            return os.path.join(os.path.dirname(sys.argv[0]),"crl")
        
    
    def get_conf(self,type : str):
        
        if type == "CA":
            with open("Config_CA.json", "r") as file :
                config = json.loads(file.read())
                return config
        
        elif type == "RA":
            with open("Config_RA.json", "r") as file :
                config = json.loads(file.read())
                return config
            
            