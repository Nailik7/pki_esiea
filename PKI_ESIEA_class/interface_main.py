from generate_client_ui import GenerateClientUi
from other_options import OtherOptions
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
    QComboBox,
    QHBoxLayout,
)
#from generate_client_ui import GenerateClientUi as gc
import pdb, sys

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        self.zone_texte_longueur = 50
        self.zone_texte_largeur = 20
        
        self.initUI()


        
    def initUI(self):

        self.setWindowTitle("PKI_ESIEA")                # On donne le titre de la fenetre
        self.setWindowIcon(QtGui.QIcon('UI/images/logo.png'))     # On met un beau logo
        self.resize(700,850)                            # On redéfinit la taille de la fenetre en 400 par 400
        
        
        #self.zone_ip()      # On appelle les fonctions permettant d'afficher la zone de texte correspondant à l'IP
        #self.zone_api()     # On appelle les fonctions permettant d'afficher la zone de texte correspondant à l'API
        #self.zone_host()    # On appelle les fonctions permettant d'afficher la zone de texte correspondant à l'host
               
        
        """ On crée le bouton qui va s'occuper du certificat racine """
        
        button_generate_auth = QPushButton('Générer le certificat racine', self)        # On définit le titre du bouton      
        button_generate_auth.setToolTip('Générer le certificat racine ?')    # On configure ce qui va s'afficher lorsque l'on passe la souris au dessus du bouton
        button_generate_auth.move(275,300)                                     # On séléctionne la position du bouton
        button_generate_auth.clicked.connect(self.on_click_generate_auth)      # On appelle la fonction "on_click" lorsque l'on clique sur le bouton
        """ On style le bouton """
        
        button_generate_auth.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #7dbdda;"      # On définit un fond pour le bouton dans les tons bleus
                             "}"
                             "QPushButton::hover"               # Losque l'on passe la souris sur le bouton
                             "{"
                             "background-color : #7dda99;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
                             "QPushButton::pressed"             # Lorsque le bouton est appuyé 
                             "{"
                             "background-color : #48d873;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
                             )

        button_generate_clt = QPushButton('Générer le certificat client', self)        # On définit le titre du bouton      
        button_generate_clt.setToolTip('Générer le certificat client ?')    # On configure ce qui va s'afficher lorsque l'on passe la souris au dessus du bouton
        button_generate_clt.move(275,400)                                     # On séléctionne la position du bouton
        button_generate_clt.clicked.connect(self.on_click_generate_clt)      # On appelle la fonction "on_click" lorsque l'on clique sur le bouton
        """ On style le bouton """
        
        button_generate_clt.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #7dbdda;"      # On définit un fond pour le bouton dans les tons bleus
                             "}"
                             "QPushButton::hover"               # Losque l'on passe la souris sur le bouton
                             "{"
                             "background-color : #7dda99;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
                             "QPushButton::pressed"             # Lorsque le bouton est appuyé 
                             "{"
                             "background-color : #48d873;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
                             )


        button_parse= QPushButton('Parser ou tester un certificat', self)        # On définit le titre du bouton      
        button_parse.setToolTip('Parser ou tester un certificat ?')    # On configure ce qui va s'afficher lorsque l'on passe la souris au dessus du bouton
        button_parse.move(275,500)                                     # On séléctionne la position du bouton
        button_parse.clicked.connect(self.on_click_others_options)      # On appelle la fonction "on_click" lorsque l'on clique sur le bouton
        """ On style le bouton """
        
        button_parse.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #7dbdda;"      # On définit un fond pour le bouton dans les tons bleus
                             "}"
                             "QPushButton::hover"               # Losque l'on passe la souris sur le bouton
                             "{"
                             "background-color : #7dda99;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
                             "QPushButton::pressed"             # Lorsque le bouton est appuyé 
                             "{"
                             "background-color : #48d873;"      # On définit un fond pour le bouton dans les tons verts
                             "}"
        )
        self.show()                                             # On affiche la fenetre 
     



    @pyqtSlot()
    def on_click_generate_auth(self):
        
        """On définit la fonction qui va gérer l'appui sur le bouton"""
        print("generation du certificat racine")
        #self.close()


        
        
        '''
        ip = self.zone_texte_ip.text()                                   # On prend le résultat de la zone de texte ip qu'on stocke dans une variable
        api = self.zone_texte_api.text()                                 # On prend le résultat de la zone de texte api qu'on stocke dans une variable
        host = self.zone_texte_hostname.text()                           # On prend le résultat de la zone de texte hostname qu'on stocke dans une variable
        '''


        '''
        if not validators.url(ping) or not requests.ConnectionError:            # On regarde si l'url est valide si on arrive à contacter correctement l'host.
            QMessageBox.about(self, "Erreur critique",  "host invalide")
        '''


    def show_clt_child_window_clt(self):
        self.child_clt_window = GenerateClientUi()
        self.child_clt_window.show()

    def show_clt_child_window_other(self):
        self.child_clt_window = OtherOptions()
        self.child_clt_window.show()

    def on_click_generate_clt(self):
        
        self.show_clt_child_window_clt()
        self.close()


    def on_click_others_options(self):
        self.show_clt_child_window_other()
        self.close()
        print('Parse or test')
        #self.close()
       
                         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()