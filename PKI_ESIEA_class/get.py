from cryptography.hazmat.primitives import hashes
import os, sys, json

class get():
    
    def get_algo_hash(self,algorithm : str): #La fonction renvoie les différents algo de chiffrement en fonction du paramètre
        
        if algorithm == "SHA256":
            return hashes.SHA256()
        elif algorithm == "MD5":
            return hashes.MD5()
        elif algorithm == "SHA1":
            return hashes.SHA1()
        elif algorithm == "SHA224":
            return hashes.SHA224()
        
        
    def get_path(self,type : str): #La fonction renvoi le chemin des dossiers des certificat en fonction du paramètre
        
        if type == "ca":
            return os.path.join(os.path.dirname(sys.argv[0]),"Certificate-CA")
        elif type == "ra":
            return os.path.join(os.path.dirname(sys.argv[0]),"Certificate-RA")
        elif type == "client":
            return os.path.join(os.path.dirname(sys.argv[0]),"Client")
        elif type == "crl":
            return os.path.join(os.path.dirname(sys.argv[0]),"crl")
        
    
    def get_conf(self, conf : list, type : str): #La fonction renvoie un dictionnaire, la configuration des autorités
        
        for file in conf :
            if type == "CA" and "CA" in file:
                with open("Config_CA.json", "r") as file :
                    config = json.loads(file.read())
                    return config
            
            elif type == "RA" and "RA" in file:
                with open("Config_RA.json", "r") as file :
                    config = json.loads(file.read())
                    return config
                
            
    
    def get_conf_client(self,name : str): #La fonction renvoie le nom du fichier du client, en parsant un fichier Json 
        
        if name == "client":
            if os.path.exists("Config_client.json"):
                with open("Config_client.json") as file :
                    config = json.loads(file.read())
                return str(config["Filename"])
        else :
            print("Fichier de config client n'existe pas")
            