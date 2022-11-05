from generate_client_ui import GenerateClientUi
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
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))     # On met un beau logo
        self.resize(700,850)                            # On redéfinit la taille de la fenetre en 400 par 400
        self.centrer()                                  # On appelle la fonction pour centrer la fenetre
        
        
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
        button_parse.clicked.connect(self.on_click_parse_or_test)      # On appelle la fonction "on_click" lorsque l'on clique sur le bouton
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


    def show_clt_child_window(self):
        self.child_clt_window = GenerateClientUi()
        self.child_clt_window.show()


    def on_click_generate_clt(self):
        
        self.show_clt_child_window()
        self.close()


    def on_click_parse_or_test(self):

        print('Parse or test')
        #self.close()

    def centrer(self):
        
        """On définit la fonction qui va gérer le centrage de la fenetre """
        
        geometrie_fenetre = self.frameGeometry()                            # On obtient la géometrie de la fenetre
        pointer_fenetre = QDesktopWidget().availableGeometry().center()     # On bouge le pointer au milieu de l'écran
        geometrie_fenetre.moveCenter(pointer_fenetre)                       # On définit la géométrie de la fenetre au centre de l'écran
        self.move(geometrie_fenetre.topLeft())                              # On bouge la fenetre au centre de l'écran


      
    def zone_ip(self):
        
        """ On crée la première zone de texte consacré à l'IP """
        # creating a combo box widget
        self.combo_box = QComboBox(self)
  
        # setting geometry of combo box
        self.combo_box.setGeometry(200, 150, 400, 100)
        lang_list = ["FR", "EN", "RU", "CH"]
  
        # making it editable
        self.combo_box.setEditable(False)
  
        # adding list of items to combo box
        self.combo_box.addItems(lang_list)
  
        # adjusting the size according to the maximum sized element
        self.combo_box.adjustSize()

           
                         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()