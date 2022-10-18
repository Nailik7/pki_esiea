import sys, os
nb = 0
tab_name = ["Country : ", "FR", "State","IDF", "Localisation : ", "Paris", "Organization :","CA Novaly", "Nom ressource", "Administrateur", "Hostname :", "novaly-ca.com"]
def test(tab : list ):
    print(tab[0:12][11])
    
test(tab_name)