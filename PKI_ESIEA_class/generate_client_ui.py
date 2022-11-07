from certificate import certificate
import lists

from PyQt5 import QtGui
from PyQt5.QtGui import (
    QPainter,
    QFont,
    QPen,
    QFontMetrics,
)
from PyQt5.QtCore import (
    Qt,
)
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
    QFileDialog,
    QVBoxLayout,
    QGridLayout,
    QCheckBox,
)

import pdb, sys, validators, logging

""" ------------------------------------------ """
""" On trie les imports par ordre alphabétique """
""" ------------------------------------------ """

class GenerateClientUi(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.logFile = "logs/pki.log"

        self.yes_no = ""

        self.private_k_file = ""

        self.hash_alg = ""
        self.rsa_dsa = ""

        self.dns = ""
        self.hostname = ""
        self.organisation = ""
        self.localisation = ""

        self.lang = ""
        self.cnt = ""
        self.us_state = ""
        self.fr_reg = ""

        self.filename = ""


        self.hidden = 2


        logging.basicConfig(filename=self.logFile, level=logging.INFO) 


    def initUI(self):

        self.setWindowTitle("PKI_ESIEA")                # On donne le titre de la fenetre
        self.setWindowIcon(QtGui.QIcon('UI/images/logo.png'))     # On met un beau logo
        self.resize(700,850)                            # On redéfinit la taille de la fenetre en 400 par 400
          
        self.layout_test = QVBoxLayout()
        self.private_rsa_dsa()

        self.show()


    def private_rsa_dsa(self):
        


        #Utils.paintEvent(self)


        self.checkbox()
        self.form_has_certificate()
        self.form_no_certificate()
        self.form_create_certificate()
        






    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)


        self.draw_title(qp)
        self.draw_text_has_certificate(qp)


        ''' On définit la position des champs '''

        self.label_select_file.setGeometry(75,220, 300, 50)
        self.button_browse.move(375, 274)
        self.button_browse.resize(100, 25)


        self.label_select_type_of_key.setGeometry(75, 199, 300, 30)
        self.label_form_create_certificate.setGeometry(75, 350, 400, 20)

        self.combo_box_select_lang.setGeometry(135, 400, 150, 25)
        self.combo_box_select_lang.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.combo_box_select_lang.setMaxVisibleItems(15)

        self.label_form_select_country.setGeometry(75, 400, 50, 25)

        self.combo_box_select_us_state.setGeometry(450, 400, 150, 25)
        self.combo_box_select_us_state.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.combo_box_select_us_state.setMaxVisibleItems(15)

        self.combo_box_select_fr_reg.setGeometry(450, 400, 150, 25)
        self.combo_box_select_fr_reg.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.combo_box_select_fr_reg.setMaxVisibleItems(15)


        self.label_form_select_state_or_reg.setGeometry(325, 400, 125, 25)

        self.label_form_select_localisation.setGeometry(75, 450, 150, 25)
        self.line_edit_form_select_localisation.setGeometry(160, 450, 150, 25)

        self.label_form_select_organisation.setGeometry(350, 450, 150, 25)
        self.line_edit_form_select_organisation.setGeometry(475, 450, 150, 25)

        self.label_form_select_ressource_name.setGeometry(75, 500, 150, 25)
        self.line_edit_form_select_ressource_name.setGeometry(230, 500, 150, 25)

        self.label_form_select_hostname.setGeometry(410, 500, 150, 25)
        self.line_edit_form_select_hostname.setGeometry(515, 500, 150, 25)

        self.label_form_select_dns.setGeometry(75, 550, 150, 25)
        self.line_edit_form_select_dns.setGeometry(140, 550, 150, 25)

        self.label_form_select_filename.setGeometry(160, 650, 150, 25)
        self.line_edit_form_select_filename.setGeometry(310, 650, 150, 25)

        self.button_send_clt.setGeometry(250, 750, 150, 25)
        
        


        ''' 
        Dessous self.hidden possède 3 etats :
        self.hidden == 0 --> L'utilisateur possède une clé RSA ou DSA (il coche oui)
                         --> On lui affiche donc le champ de texte et le bouton pour chercher sa clé 
                         --> On cache les champs présent dans self.hidden == 1
        self.hidden == 1 --> L'utilisateur ne possède pas de clé RSA ou DSA (il coche non)
                         --> On lui affiche donc les autres champs en cachant les champs présent dans self.hidden == 0
        self.hidden == 2 --> L'utilisateur n'a pas coché de case
                         --> On cache tout

        '''


        ''' On cache et affiche selon ce que l'utilisateur choisi '''
        if self.hidden == 0:


            self.file_zone.show()
            self.label_select_file.show()
            self.button_browse.show()

            self.checkbox_dsa.hide()
            self.checkbox_rsa.hide()

            self.checkbox_md5.setGeometry(75, 180, 100, 50)
            self.checkbox_md5.show()

            self.checkbox_sha224.setGeometry(225, 180, 100, 50)
            self.checkbox_sha224.show()
            self.checkbox_sha1.setGeometry(375, 180, 100, 50)
            self.checkbox_sha1.show()
            self.checkbox_sha256.setGeometry(525, 180, 100, 50)
            self.checkbox_sha256.show()

            self.label_select_type_of_key.hide()
            self.label_select_hash_alg.setGeometry(75, 150, 400, 50)
            self.label_select_hash_alg.show()

            self.label_form_create_certificate.show()
            self.combo_box_select_lang.show()
            self.label_form_select_country.show()
            self.label_form_select_state_or_reg.show()



            if self.combo_box_select_lang.currentText() == 'Etats-Unis d’Amérique':
                self.combo_box_select_us_state.show()
                self.combo_box_select_fr_reg.hide()
            elif self.combo_box_select_lang.currentText() == 'France':
                self.combo_box_select_fr_reg.show()
                self.combo_box_select_us_state.hide()
            else:
                self.combo_box_select_us_state.hide()
                self.combo_box_select_fr_reg.hide()


            self.line_edit_form_select_localisation.show()
            self.label_form_select_localisation.show()
            self.label_form_select_organisation.show()
            self.line_edit_form_select_organisation.show()
            
            self.label_form_select_ressource_name.show()
            self.line_edit_form_select_ressource_name.show()


            self.label_form_select_hostname.show()
            self.line_edit_form_select_hostname.show()

            self.label_form_select_dns.show()
            self.line_edit_form_select_dns.show()

            self.label_form_select_filename.show()
            self.line_edit_form_select_filename.show()

            self.button_send_clt.show()

        elif self.hidden == 1:

            # On cache la séléction de du fichier de la clé
            self.button_browse.hide()
            self.file_zone.hide()
            self.label_select_file.hide()

            self.checkbox_dsa.show()
            self.checkbox_rsa.show()

            
            self.checkbox_md5.setGeometry(75, 280, 100, 50)
            self.checkbox_md5.show()
            self.checkbox_sha224.setGeometry(225, 280, 100, 50)
            self.checkbox_sha224.show()
            self.checkbox_sha1.setGeometry(375, 280, 100, 50)
            self.checkbox_sha1.show()
            self.checkbox_sha256.setGeometry(525, 280, 100, 50)
            self.checkbox_sha256.show()

            self.label_select_type_of_key.show()
            self.label_select_hash_alg.setGeometry(75, 250, 400, 20)
            self.label_select_hash_alg.show()

            self.label_form_create_certificate.show()
            self.combo_box_select_lang.show()
            self.label_form_select_country.show()
            self.label_form_select_state_or_reg.show()


            if self.combo_box_select_lang.currentText() == 'Etats-Unis d’Amérique':
                self.combo_box_select_us_state.show()
                self.combo_box_select_fr_reg.hide()

            elif self.combo_box_select_lang.currentText() == 'France':
                self.combo_box_select_fr_reg.show()
                self.combo_box_select_us_state.hide()
            else:
                self.combo_box_select_us_state.hide()
                self.combo_box_select_fr_reg.hide()

            
            self.line_edit_form_select_localisation.show()
            self.label_form_select_localisation.show()
            self.label_form_select_organisation.show()
            self.line_edit_form_select_organisation.show()


            self.label_form_select_ressource_name.show()
            self.line_edit_form_select_ressource_name.show()

            self.label_form_select_hostname.show()
            self.line_edit_form_select_hostname.show()

            self.label_form_select_dns.show()
            self.line_edit_form_select_dns.show()

            self.label_form_select_filename.show()
            self.line_edit_form_select_filename.show()

            self.button_send_clt.show()



        else:

            self.button_browse.hide()
            self.file_zone.hide()
            self.label_select_file.hide()


            self.checkbox_dsa.hide()
            self.checkbox_rsa.hide()

            self.checkbox_md5.hide()
            self.checkbox_sha224.hide()
            self.checkbox_sha1.hide()
            self.checkbox_sha256.hide()

            self.label_select_type_of_key.hide()
            self.label_select_hash_alg.hide()

            self.label_form_create_certificate.hide()
            self.combo_box_select_lang.hide()
            self.label_form_select_country.hide()
            self.label_form_select_state_or_reg.hide()

            self.combo_box_select_us_state.hide()
            self.combo_box_select_fr_reg.hide()

            self.line_edit_form_select_localisation.hide()
            self.label_form_select_localisation.hide()
            self.label_form_select_organisation.hide()
            self.line_edit_form_select_organisation.hide()

            self.label_form_select_ressource_name.hide()
            self.line_edit_form_select_ressource_name.hide()


            self.label_form_select_hostname.hide()
            self.line_edit_form_select_hostname.hide()

            self.label_form_select_dns.hide()
            self.line_edit_form_select_dns.hide()

            self.label_form_select_filename.hide()
            self.line_edit_form_select_filename.hide()
            

            self.button_send_clt.hide()


        self.dns = self.line_edit_form_select_dns.text()
        self.hostname = self.line_edit_form_select_hostname.text()
        self.ressource_name = self.line_edit_form_select_ressource_name.text()
        self.organisation = self.line_edit_form_select_organisation.text()
        self.localisation = self.line_edit_form_select_localisation.text()

        self.filename = self.line_edit_form_select_filename.text()

        self.private_k_file = self.file_zone.text()

        qp.end()




    def draw_title(self, qp):
        '''
        On crée le titre de la page
        '''

        font = QFont()
        font.setFamily('Lato')
        font.setBold(True)
        font.setPointSize(24)
        qp.setFont(font)

        qp.drawText(170, 75, 'Générer un certificat client')




        
    def draw_text_has_certificate(self, qp):
        '''
        On crée le texte qui demande si l'utilisateur il a une clé privée
        '''
        font = QFont()
        font.setFamily('Lato')
        font.setBold(False)
        font.setPointSize(14)
        qp.setFont(font)
        qp.drawText(75, 150, 'Possédez vous déjà une clé privée RSA ou DSA ?')





    def checkbox(self):
        '''
        On crée la checkbox pour si l'on possède déjà une clé privée
        '''

        self.checkbox_no = QCheckBox("Non", self)
        self.checkbox_yes = QCheckBox("Oui", self)


        self.checkbox_yes.stateChanged.connect(self.checked_case)
        self.checkbox_no.stateChanged.connect(self.checked_case)
        

        self.checkbox_no.move(600,95)
        self.checkbox_no.resize(100,100)

        self.checkbox_yes.move(500, 95)
        self.checkbox_yes.resize(100, 100)




    def checked_case(self, state):

        '''
        Fonction permettant de gérer les changements d'etas des checboxs
        '''
        
        

        if state == Qt.Checked:

            if self.sender() == self.checkbox_yes:
                self.checkbox_no.setChecked(False)
                self.yes_no = 'yes'
                self.hidden = 0


            elif self.sender() == self.checkbox_no:
                self.checkbox_yes.setChecked(False)
                self.yes_no = 'no'
                self.hidden = 1


            elif self.sender() == self.checkbox_dsa:
                self.checkbox_rsa.setChecked(False)
                self.checkbox_md5.setChecked(False)

                self.rsa_dsa = 'DSA'

            
            elif self.sender() == self.checkbox_rsa:
                self.checkbox_dsa.setChecked(False)

                self.rsa_dsa = 'RSA'


            elif self.sender() == self.checkbox_md5:
                self.checkbox_sha224.setChecked(False)
                self.checkbox_sha1.setChecked(False)
                self.checkbox_sha256.setChecked(False)
                self.checkbox_dsa.setChecked(False)
                self.checkbox_rsa.setChecked(True)

                self.hash_alg = 'MD5'
            
            elif self.sender() == self.checkbox_sha224:
                self.checkbox_md5.setChecked(False)
                self.checkbox_sha1.setChecked(False)
                self.checkbox_sha256.setChecked(False)

                self.hash_alg = 'SHA224'
            
            elif self.sender() == self.checkbox_sha1:
                self.checkbox_md5.setChecked(False)
                self.checkbox_sha224.setChecked(False)
                self.checkbox_sha256.setChecked(False)

                self.hash_alg = 'SHA1'

            elif self.sender() == self.checkbox_sha256:
                self.checkbox_md5.setChecked(False)
                self.checkbox_sha224.setChecked(False)
                self.checkbox_sha1.setChecked(False)

                self.hash_alg = 'SHA256'

            else:
                self.hidden = 2

            
    def form_has_certificate(self):

        self.label_select_file = QLabel("Séléctionnez votre clé privé :")
        self.layout_test.addWidget(self.label_select_file)
        self.setLayout(self.layout_test)
        self.label_select_file.setFont(QFont('Lato', 14))

        self.file_zone = QLineEdit(self)
        self.file_zone.move(100, 274)
        self.file_zone.resize(250,26)
        self.file_zone.setStyleSheet("border-radius: 5px; color: blue;")

        self.button_browse = QPushButton('Rechercher', self)
        self.layout_test.addWidget(self.button_browse)
        self.setLayout(self.layout_test)
        self.button_browse.clicked.connect(self.browse_pem_key_file)
        self.button_browse.setStyleSheet("QPushButton"
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
        
        
    def browse_pem_key_file(self):
        '''
        Selection des fichiers PEM or KEY
        '''
        fname = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PEM OR KEY (*.pem *.key)')
        self.file_zone.setText(fname[0])



    def form_no_certificate(self):

        '''Création des checkboxs'''

        self.checkbox_dsa = QCheckBox("DSA", self)
        self.checkbox_rsa = QCheckBox("RSA", self)

        self.checkbox_md5 = QCheckBox("MD5", self)
        self.checkbox_sha224 = QCheckBox("SHA224", self)
        self.checkbox_sha1 = QCheckBox("SHA1", self)
        self.checkbox_sha256 = QCheckBox("SHA256", self)


        '''Action lorsque la checkbox est cochée'''

        self.checkbox_dsa.stateChanged.connect(self.checked_case)
        self.checkbox_rsa.stateChanged.connect(self.checked_case)
        
        self.checkbox_md5.stateChanged.connect(self.checked_case)
        self.checkbox_sha224.stateChanged.connect(self.checked_case)
        self.checkbox_sha1.stateChanged.connect(self.checked_case)
        self.checkbox_sha256.stateChanged.connect(self.checked_case)


        '''On définit la position des checkboxs'''

        self.checkbox_dsa.move(375,199)
        self.checkbox_rsa.move(450, 199)

        self.checkbox_md5.move(75, 290)
        self.checkbox_sha224.move(225, 290)
        self.checkbox_sha1.move(375, 290)
        self.checkbox_sha256.move(525, 290)


        '''On définit les polices et leur tailles'''

        self.checkbox_dsa.setFont(QFont('Lato', 12))
        self.checkbox_rsa.setFont(QFont('Lato', 12))

        self.checkbox_md5.setFont(QFont('Lato', 12))
        self.checkbox_sha224.setFont(QFont('Lato', 12))
        self.checkbox_sha1.setFont(QFont('Lato', 12))
        self.checkbox_sha256.setFont(QFont('Lato', 12))


        ''' Création du QLabel rsa dsa '''

        self.label_select_type_of_key = QLabel("Séléctionnez le type de clé voulu :")
        self.layout_test.addWidget(self.label_select_type_of_key)
        self.setLayout(self.layout_test)
        self.label_select_type_of_key.setFont(QFont('Lato', 14))


        ''' Création du QLabel de l'algo de hash '''
        
        self.label_select_hash_alg = QLabel("Séléctionnez l'agorithme de chiffrement voulu :")
        self.layout_test.addWidget(self.label_select_hash_alg)
        self.setLayout(self.layout_test)
        self.label_select_hash_alg.setFont(QFont('Lato', 14))
        
        
    
    def form_create_certificate(self):
        


        self.label_form_create_certificate = QLabel("Veuillez renseigner les champs ci-dessous :")
        self.layout_test.addWidget(self.label_form_create_certificate)
        self.setLayout(self.layout_test)
        self.label_form_create_certificate.setFont(QFont('Lato', 14))


        '''Création du champ pour le pays'''


        # Label pour le pays
        self.label_form_select_country = QLabel("Pays :")
        self.layout_test.addWidget(self.label_form_select_country)
        self.setLayout(self.layout_test)
        self.label_form_select_country.setFont(QFont('Lato', 14))


        #Menu deroulant pour la séléction du pays
        self.combo_box_select_lang = QComboBox(self)
        self.layout_test.addWidget(self.combo_box_select_lang)
        self.setLayout(self.layout_test)
        self.combo_box_select_lang.setEditable(False)
        self.combo_box_select_lang.addItems(sorted(lists.tabl_lang.keys()))
        self.combo_box_select_lang.update()


        
        
        # Label à coté de la séléction de l'etat/région
        self.label_form_select_state_or_reg = QLabel("Etat/Région :")
        self.layout_test.addWidget(self.label_form_select_state_or_reg)
        self.setLayout(self.layout_test)
        self.label_form_select_state_or_reg.setFont(QFont('Lato', 14))

        '''Création du champ pour les etats si on séléctionneles Etats Unis'''

        # Label à coté de la séléction de l'etat
        self.combo_box_select_us_state = QComboBox(self)
        self.layout_test.addWidget(self.combo_box_select_us_state)
        self.setLayout(self.layout_test)
        self.combo_box_select_us_state.setEditable(False)
        self.combo_box_select_us_state.addItems(sorted(lists.list_us_states))


        '''Création du champ pour les régions si on séléctionneles la France'''

        # Menu déroulant pour les régions
        self.combo_box_select_fr_reg = QComboBox(self)
        self.layout_test.addWidget(self.combo_box_select_fr_reg)
        self.setLayout(self.layout_test)
        self.combo_box_select_fr_reg.setEditable(False)
        self.combo_box_select_fr_reg.addItems(sorted(lists.list_rg))






        '''Création du champ pour l'Adresse'''

        # Label à coté du champ de texte
        self.label_form_select_localisation = QLabel("Adresse :")
        self.layout_test.addWidget(self.label_form_select_localisation)
        self.setLayout(self.layout_test)
        self.label_form_select_localisation.setFont(QFont('Lato', 14))

        # Champ de texte
        self.line_edit_form_select_localisation = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_localisation)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_localisation.setFont(QFont('Lato', 14))
        self.line_edit_form_select_localisation.setStyleSheet("border-radius: 5px; color: blue;")



        
        '''Création du champ pour l'Organisation'''

        # Label à coté du champ de texte
        self.label_form_select_organisation = QLabel("Organisation :")
        self.layout_test.addWidget(self.label_form_select_organisation)
        self.setLayout(self.layout_test)
        self.label_form_select_organisation.setFont(QFont('Lato', 14))

        # Champ de texte
        self.line_edit_form_select_organisation = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_organisation)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_organisation.setFont(QFont('Lato', 14))
        self.line_edit_form_select_organisation.setStyleSheet("border-radius: 5px; color: blue;")




        '''Création du champ pour la Ressource name'''

        # Label à coté du champ de texte
        self.label_form_select_ressource_name = QLabel("Ressource name :")
        self.layout_test.addWidget(self.label_form_select_ressource_name)
        self.setLayout(self.layout_test)
        self.label_form_select_ressource_name.setFont(QFont('Lato', 14))

        # Champ de texte
        self.line_edit_form_select_ressource_name = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_ressource_name)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_ressource_name.setFont(QFont('Lato', 14))
        self.line_edit_form_select_ressource_name.setStyleSheet("border-radius: 5px; color: blue;")



        '''Création du champ pour le Hostname'''

        # Label à coté du champ de texte
        self.label_form_select_hostname = QLabel("Hostname :")
        self.layout_test.addWidget(self.label_form_select_hostname)
        self.setLayout(self.layout_test)
        self.label_form_select_hostname.setFont(QFont('Lato', 14))

        # Champ de texte
        self.line_edit_form_select_hostname = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_hostname)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_hostname.setFont(QFont('Lato', 14))
        self.line_edit_form_select_hostname.setStyleSheet("border-radius: 5px; color: blue;") 
        

        
        

        '''Création du champ pour le DNS'''

        # Label à coté du champ de texte
        self.label_form_select_dns = QLabel("DNS :")
        self.layout_test.addWidget(self.label_form_select_dns)
        self.setLayout(self.layout_test)
        self.label_form_select_dns.setFont(QFont('Lato', 14))

        # Champ de texte
        self.line_edit_form_select_dns = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_dns)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_dns.setFont(QFont('Lato', 14))
        self.line_edit_form_select_dns.setStyleSheet("border-radius: 5px; color: blue;") 
        


        ''' Création du champ pour le nom du fichier à enregistrer '''

        # Label à coté du champ de texte
        self.label_form_select_filename = QLabel("Nom du fichier :")
        self.layout_test.addWidget(self.label_form_select_filename)
        self.setLayout(self.layout_test)
        self.label_form_select_filename.setFont(QFont('Lato', 14))

        # Champ de texte
        self.line_edit_form_select_filename = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_filename)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_filename.setFont(QFont('Lato', 14))
        self.line_edit_form_select_filename.setStyleSheet("border-radius: 5px; color: blue;") 
        


        '''Création du bouton pour envoyer les données'''

        self.button_send_clt= QPushButton('Générer le certificat', self)            
        self.button_send_clt.setToolTip('Générer le certificat ?')
        self.button_send_clt.clicked.connect(self.send_clt) 
        
        
        """ On style le bouton """
        
        self.button_send_clt.setStyleSheet("QPushButton"
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

    
    



    def err_popup(self, message: str):
        '''
        Fonction permettant d'afficher une popup d'erreur
        message -> str (Message à afficher)
        '''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Erreur critique")
        msg.setText(str(message))
        msg.exec_()

    def popup(self, message: str):
        '''
        Fonction permettant d'afficher une popup d'erreur
        message -> str (Message à afficher)
        '''
        msg = QMessageBox()
        msg.setWindowTitle("Succès")
        msg.setText(str(message))
        msg.exec_()

        

    def send_clt(self):

        '''
        Fonction permettant de vérifier et d'envoyer les donnés utilisateurs
        '''


        known_ext = False

        self.lang = self.combo_box_select_lang.currentText()
        self.cnt = lists.tabl_lang.get(self.lang)


        '''On vérifie si l'extention du dns existe'''

        for i in lists.list_extensions:
            print(self.dns.split('.')[-1])
            if i == self.dns.split('.')[-1]:
                known_ext = True

        

        '''On vérifie que tous les champs sont correctement remplis'''


        # Vérification de la longueur des champs de texte
        if len(self.localisation) > 20 or len(self.organisation) > 20 or len(self.ressource_name) > 20 or len(self.hostname) > 20:
            self.err_popup("Erreur, les champs de textes ne doivent pas dépasser 20 caractères")  

        # Vérification des champs vide 
        elif len(self.localisation) == 0 or len(self.organisation) == 0 or len(self.ressource_name) == 0 or len(self.hostname) == 0 or len(self.dns) == 0:
            self.err_popup("Erreur, tous les champs de texte doivent être rempli")

        # Vérification des checkboxs du type d'algo
        elif self.checkbox_md5.isChecked() == False and self.checkbox_sha1.isChecked() == False and self.checkbox_sha224.isChecked() == False and self.checkbox_sha256.isChecked() == False:
            self.err_popup("Erreur, veuillez cocher un algorithme de chiffrement")

        # Vérification du nom de fichier pour l'enregistrement
        elif len(self.filename) == 0 or len(self.filename) > 20:
            self.err_popup("Erreur, veuillez entrer un nom de fichier à enregistrer de moins de 20 caractères")

        # Vérification du DNS
        elif validators.domain(self.dns) == False or len(self.dns) > 20 or known_ext == False:
            self.err_popup(f"Erreur, nom de domaine '{self.dns}' invalide, veuillez ré-essayer")

        # Si tout se passe bien
        else:
            
            '''
            N'ayant pas utilisé la meme variable pour les régions en France et les Etats aux etats-unis je fais une condition 
            pour récupérer la bonne variable à envoyer
            '''
            
            if self.lang == "France":
                self.state_or_reg = self.combo_box_select_fr_reg.currentText()
                certificate.create_client(self, self.rsa_dsa, self.cnt, self.state_or_reg, self.localisation, self.organisation, self.ressource_name, self.hostname, self.dns, self.filename, self.hash_alg)
                logging.info(f"Un certificat client vient d'être créé en utilisant le type de clé '{self.rsa_dsa}', l'algorithme de hash '{self.hash_alg}', le pays '{self.lang}', l'etat ou la region '{self.state_or_reg}', l'adresse '{self.localisation}', l'organistation '{self.organisation}', ressource name '{self.ressource_name}', l'hostname '{self.hostname}' et le DNS '{self.dns}' \n")
            
            elif self.lang == "Etats-Unis d’Amérique":
                self.state_or_reg = self.combo_box_select_us_state.currentText()
                certificate.create_client(self, self.rsa_dsa, self.cnt, self.state_or_reg, self.localisation, self.organisation, self.ressource_name, self.hostname, self.dns, self.filename, self.hash_alg)
                logging.info(f"Un certificat client vient d'être créé en utilisant le type de clé '{self.rsa_dsa}', l'algorithme de hash '{self.hash_alg}', le pays '{self.lang}', l'etat ou la region '{self.state_or_reg}', l'adresse '{self.localisation}', l'organistation '{self.organisation}', ressource name '{self.ressource_name}', l'hostname '{self.hostname}' et le DNS '{self.dns}' \n")
            
            else:
                self.state_or_reg = self.lang
                if self.checkbox_yes.setChecked() == True:
                    self.rsa_dsa = None
                    certificate.create_client(self, self.rsa_dsa, self.cnt, self.state_or_reg, self.localisation, self.organisation, self.ressource_name, self.hostname, self.dns, self.filename, self.hash_alg)
                    self.popup("Le certificat a été créé avec succès")
                else:
                    if self.checkbox_rsa.isChecked() == False and self.checkbox_dsa.isChecked() == False:
                        self.err_popup("Erreur, veuillez cocher un type de clé à créer")
                    else:

                        certificate.create_client(self, self.rsa_dsa, self.cnt, self.state_or_reg, self.localisation, self.organisation, self.ressource_name, self.hostname, self.dns, self.filename, self.hash_alg)
                        self.popup("Le certificat a été créé avec succès")
                logging.info(f"Un certificat client vient d'être créé en utilisant le type de clé '{self.rsa_dsa}', l'algorithme de hash '{self.hash_alg}', le pays '{self.lang}', l'etat ou la region '{self.state_or_reg}', l'adresse '{self.localisation}', l'organistation '{self.organisation}', ressource name '{self.ressource_name}', l'hostname '{self.hostname}' et le DNS '{self.dns}' \n")



        



        
        



if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    main = GenerateClientUi()
    app.exec_()
              