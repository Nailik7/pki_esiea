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

import pdb, sys

""" ------------------------------------------ """
""" On trie les imports par ordre alphabétique """
""" ------------------------------------------ """

class GenerateClientUi(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

        self.hidden = 2


    def initUI(self):

        self.setWindowTitle("PKI_ESIEA")                # On donne le titre de la fenetre
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))     # On met un beau logo
        self.resize(700,850)                            # On redéfinit la taille de la fenetre en 400 par 400
          
        self.layout_test = QVBoxLayout()
        self.private_rsa_dsa()

        self.show()


    def private_rsa_dsa(self):
        

        self.file_zone = QLineEdit(self)
        self.file_zone.move(100, 274)
        self.file_zone.resize(250,26)
        self.file_zone.setStyleSheet("border-radius: 5px; color: blue;")


        #Utils.paintEvent(self)

        self.draw_text_select_file()
        self.draw_button_select_file()

        self.checkbox()
        self.form_no_certificate()
        self.form_create_certificate()
        



    def browse_pem_key_file(self):
        '''
        Selection des fichiers PEM or KEY
        '''
        fname = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PEM OR KEY (*.pem *.key)')
        self.file_zone.setText(fname[0])




    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)


        self.draw_title(qp)
        self.draw_text_has_certificate(qp)


        self.label_select_file.move(75,30)
        self.button_browse.move(375, 274)
        self.button_browse.resize(100, 25)


        self.label_select_type_of_key.setGeometry(75, 199, 300, 30)
        self.label_select_hash_alg.setGeometry(75, 250, 400, 20)
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
        
        
        ''' On cache et affiche selon ce que l'utilisateur choisi '''
        if self.hidden == 0:


            self.file_zone.show()
            self.label_select_file.show()
            self.button_browse.show()

            self.checkbox_dsa.hide()
            self.checkbox_rsa.hide()

            self.checkbox_md5.hide()
            self.checkbox_sha224.hide()
            self.checkbox_sha1.hide()
            self.checkbox_sha256.hide()

            self.label_select_type_of_key.hide()
            self.label_select_hash_alg.hide()

            self.label_form_create_certificate.show()
            self.combo_box_select_lang.show()
            self.label_form_select_country.show()
            self.label_form_select_state_or_reg.show()

            self.line_edit_form_select_localisation.show()
            self.label_form_select_localisation.show()
            self.label_form_select_organisation.show()
            self.line_edit_form_select_organisation.show()

            if self.combo_box_select_lang.currentText() == 'Etats-Unis d’Amérique':
                self.combo_box_select_us_state.show()
                self.combo_box_select_fr_reg.hide()
            elif self.combo_box_select_lang.currentText() == 'France':
                self.combo_box_select_fr_reg.show()
                self.combo_box_select_us_state.hide()
            else:
                self.combo_box_select_us_state.hide()
                self.combo_box_select_fr_reg.hide()

            



        elif self.hidden == 1:

            # On cache la séléction de du fichier de la clé
            self.button_browse.hide()
            self.file_zone.hide()
            self.label_select_file.hide()

            self.checkbox_dsa.show()
            self.checkbox_rsa.show()

            self.checkbox_md5.show()
            self.checkbox_sha224.show()
            self.checkbox_sha1.show()
            self.checkbox_sha256.show()

            self.label_select_type_of_key.show()
            self.label_select_hash_alg.show()

            self.label_form_create_certificate.show()
            self.combo_box_select_lang.show()
            self.label_form_select_country.show()
            self.label_form_select_state_or_reg.show()

            self.line_edit_form_select_localisation.show()
            self.label_form_select_localisation.show()
            self.label_form_select_organisation.show()
            self.line_edit_form_select_organisation.show()

            if self.combo_box_select_lang.currentText() == 'Etats-Unis d’Amérique':
                self.combo_box_select_us_state.show()
                self.combo_box_select_fr_reg.hide()

            elif self.combo_box_select_lang.currentText() == 'France':
                self.combo_box_select_fr_reg.show()
                self.combo_box_select_us_state.hide()
            else:
                self.combo_box_select_us_state.hide()
                self.combo_box_select_fr_reg.hide()



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





    def draw_text_select_file(self):
        '''
        On crée le texte de séléction de la clé
        '''

        self.label_select_file = QLabel("Séléctionnez votre clé privé :")
        self.layout_test.addWidget(self.label_select_file)
        self.setLayout(self.layout_test)
        self.label_select_file.setFont(QFont('Lato', 14))


    def draw_button_select_file(self):
        '''
        On crée le bouton de séléction de la clé
        '''

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
        On paramètre le check de case
        '''
        
        

        if state == Qt.Checked:

            if self.sender() == self.checkbox_yes:
                self.checkbox_no.setChecked(False)
                self.hidden = 0


            elif self.sender() == self.checkbox_no:
                self.checkbox_yes.setChecked(False)
                self.hidden = 1


            elif self.sender() == self.checkbox_dsa:
                self.checkbox_rsa.setChecked(False)
                self.checkbox_md5.setChecked(False)
            
            elif self.sender() == self.checkbox_rsa:
                self.checkbox_dsa.setChecked(False)

            elif self.sender() == self.checkbox_md5:
                self.checkbox_sha224.setChecked(False)
                self.checkbox_sha1.setChecked(False)
                self.checkbox_sha256.setChecked(False)
                self.checkbox_dsa.setChecked(False)
                self.checkbox_rsa.setChecked(True)
            
            elif self.sender() == self.checkbox_sha224:
                self.checkbox_md5.setChecked(False)
                self.checkbox_sha1.setChecked(False)
                self.checkbox_sha256.setChecked(False)
            
            elif self.sender() == self.checkbox_sha1:
                self.checkbox_md5.setChecked(False)
                self.checkbox_sha224.setChecked(False)
                self.checkbox_sha256.setChecked(False)

            elif self.sender() == self.checkbox_sha256:
                self.checkbox_md5.setChecked(False)
                self.checkbox_sha224.setChecked(False)
                self.checkbox_sha1.setChecked(False)

            else:
                self.hidden = 2

            


    def form_no_certificate(self):

        # On cré la checkbox rsa et dsa
        self.checkbox_dsa = QCheckBox("DSA", self)
        self.checkbox_rsa = QCheckBox("RSA", self)

        self.checkbox_md5 = QCheckBox("MD5", self)
        self.checkbox_sha224 = QCheckBox("SHA224", self)
        self.checkbox_sha1 = QCheckBox("SHA1", self)
        self.checkbox_sha256 = QCheckBox("SHA256", self)



        self.checkbox_dsa.stateChanged.connect(self.checked_case)
        self.checkbox_rsa.stateChanged.connect(self.checked_case)
        
        self.checkbox_md5.stateChanged.connect(self.checked_case)
        self.checkbox_sha224.stateChanged.connect(self.checked_case)
        self.checkbox_sha1.stateChanged.connect(self.checked_case)
        self.checkbox_sha256.stateChanged.connect(self.checked_case)



        self.checkbox_dsa.move(375,199)
        self.checkbox_rsa.move(450, 199)

        self.checkbox_md5.move(75, 290)
        self.checkbox_sha224.move(225, 290)
        self.checkbox_sha1.move(375, 290)
        self.checkbox_sha256.move(525, 290)



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


        self.label_form_select_country = QLabel("Pays :")
        self.layout_test.addWidget(self.label_form_select_country)
        self.setLayout(self.layout_test)
        self.label_form_select_country.setFont(QFont('Lato', 14))


        self.combo_box_select_lang = QComboBox(self)
        self.layout_test.addWidget(self.combo_box_select_lang)
        self.setLayout(self.layout_test)
        self.combo_box_select_lang.setEditable(False)
        self.combo_box_select_lang.addItems(sorted(lists.tabl_lang.keys()))



        self.combo_box_select_us_state = QComboBox(self)
        self.layout_test.addWidget(self.combo_box_select_us_state)
        self.setLayout(self.layout_test)
        self.combo_box_select_us_state.setEditable(False)
        self.combo_box_select_us_state.addItems(sorted(lists.list_us_states))

        self.combo_box_select_fr_reg = QComboBox(self)
        self.layout_test.addWidget(self.combo_box_select_fr_reg)
        self.setLayout(self.layout_test)
        self.combo_box_select_fr_reg.setEditable(False)
        self.combo_box_select_fr_reg.addItems(sorted(lists.list_rg))




        self.label_form_select_state_or_reg = QLabel("Etat/Région :")
        self.layout_test.addWidget(self.label_form_select_state_or_reg)
        self.setLayout(self.layout_test)
        self.label_form_select_state_or_reg.setFont(QFont('Lato', 14))


        self.label_form_select_localisation = QLabel("Adresse :")
        self.layout_test.addWidget(self.label_form_select_localisation)
        self.setLayout(self.layout_test)
        self.label_form_select_localisation.setFont(QFont('Lato', 14))


        self.line_edit_form_select_localisation = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_localisation)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_localisation.setFont(QFont('Lato', 14))
        self.line_edit_form_select_localisation.setStyleSheet("border-radius: 5px; color: blue;")

        
        self.label_form_select_organisation = QLabel("Organisation :")
        self.layout_test.addWidget(self.label_form_select_organisation)
        self.setLayout(self.layout_test)
        self.label_form_select_organisation.setFont(QFont('Lato', 14))


        self.line_edit_form_select_organisation = QLineEdit(self)
        self.layout_test.addWidget(self.line_edit_form_select_organisation)
        self.setLayout(self.layout_test)
        self.line_edit_form_select_organisation.setFont(QFont('Lato', 14))
        self.line_edit_form_select_organisation.setStyleSheet("border-radius: 5px; color: blue;")




        
        
        



        




if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    main = GenerateClientUi()
    app.exec_()
              