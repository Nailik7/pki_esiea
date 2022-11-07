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
from verif_parse import verif_parse
from generate_client_ui import GenerateClientUi
import pdb, sys, validators, logging

""" ------------------------------------------ """
""" On trie les imports par ordre alphabétique """
""" ------------------------------------------ """

class OtherOptions(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

        self.status = 0



    def initUI(self):

        self.setWindowTitle("PKI_ESIEA")                # On donne le titre de la fenetre
        self.setWindowIcon(QtGui.QIcon('UI/images/logo.png'))     # On met un beau logo
        self.resize(700,850)                            # On redéfinit la taille de la fenetre en 400 par 400
          
        self.layout_test = QVBoxLayout()
        self.other_opt()

        self.show()


    def other_opt(self):
        

        #Utils.paintEvent(self)

        self.checkbox()
        self.form_issuer()
        self.form_parse()
        self.form_validity()
        






    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self.draw_title(qp)
        self.draw_text_has_certificate(qp)


        self.label_form_select_issuercertificate.setGeometry(75, 250, 450, 25)
        self.file_issuer.setGeometry(75, 300, 200, 25)
        self.button_browse_issuer.setGeometry(300, 300, 100, 25)
        

        self.label_form_select_subject_certificate.setGeometry(75, 350, 450, 25)
        self.file_subject.setGeometry(75, 400, 200, 25)
        self.button_browse_subject.setGeometry(300, 400, 100, 25)

        self.label_form_select_parse_certif.setGeometry(75, 250, 450, 25)
        self.file_to_parse.setGeometry(75, 300, 200, 25)
        self.button_browse_file_to_parse.setGeometry(300, 300, 100, 25)

        
        self.label_form_select_validity.setGeometry(75, 250, 475, 25)
        self.file_to_check_validity.setGeometry(75, 300, 200, 25)
        self.button_browse_file_validate.setGeometry(300, 300, 100, 25)

        self.button_validate_issuer.setGeometry(275, 500, 150, 25)
            


        if self.status == 1:
            self.label_form_select_issuercertificate.show()
            self.file_issuer.show()
            self.button_browse_issuer.show()
            self.label_form_select_subject_certificate.show()
            self.file_subject.show()
            self.button_browse_subject.show()

            self.label_form_select_parse_certif.hide()
            self.file_to_parse.hide()
            self.button_browse_file_to_parse.hide()

            self.label_form_select_validity.hide()
            self.file_to_check_validity.hide()
            self.button_browse_file_validate.hide()

            self.button_validate_issuer.show()


        
        elif self.status == 2:
            self.label_form_select_issuercertificate.hide()
            self.file_issuer.hide()
            self.button_browse_issuer.hide()
            self.label_form_select_subject_certificate.hide()
            self.file_subject.hide()
            self.button_browse_subject.hide()

            self.label_form_select_parse_certif.show()
            self.file_to_parse.show()
            self.button_browse_file_to_parse.show()

            self.label_form_select_validity.hide()
            self.file_to_check_validity.hide()
            self.button_browse_file_validate.hide()

            self.button_validate_issuer.show()
            

        elif self.status == 3:

            self.label_form_select_issuercertificate.hide()
            self.file_issuer.hide()
            self.button_browse_issuer.hide()
            self.label_form_select_subject_certificate.hide()
            self.file_subject.hide()
            self.button_browse_subject.hide()

            self.label_form_select_parse_certif.hide()
            self.file_to_parse.hide()
            self.button_browse_file_to_parse.hide()

            self.label_form_select_validity.show()
            self.file_to_check_validity.show()
            self.button_browse_file_validate.show()

            self.button_validate_issuer.show()


        else:
            self.label_form_select_issuercertificate.hide()
            self.file_issuer.hide()
            self.button_browse_issuer.hide()
            self.label_form_select_subject_certificate.hide()
            self.file_subject.hide()
            self.button_browse_subject.hide()

            self.label_form_select_parse_certif.hide()
            self.file_to_parse.hide()
            self.button_browse_file_to_parse.hide()

            self.label_form_select_validity.hide()
            self.file_to_check_validity.hide()
            self.button_browse_file_validate.hide()

            self.button_validate_issuer.hide()
            
            

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

        qp.drawText(170, 75, 'Autres options')





        



        
    def draw_text_has_certificate(self, qp):
        '''
        On crée le texte qui demande si l'utilisateur il a une clé privée
        '''
        font = QFont()
        font.setFamily('Lato')
        font.setBold(False)
        font.setPointSize(14)
        qp.setFont(font)
        qp.drawText(75, 150, 'Que voulez vous faire ?')





    def checkbox(self):
        '''
        On crée la checkbox pour si l'on possède déjà une clé privée
        '''

        self.checkbox_issuer = QCheckBox("VerifyIssuer", self)
        self.checkbox_parse = QCheckBox("Parser un certificat", self)
        self.checkbox_validity = QCheckBox("Vérifier la validité d'un certificat", self)


        self.checkbox_issuer.stateChanged.connect(self.checked_case)
        self.checkbox_parse.stateChanged.connect(self.checked_case)
        self.checkbox_validity.stateChanged.connect(self.checked_case)

        self.checkbox_issuer.move(75,200)
        self.checkbox_issuer.resize(200,25)

        self.checkbox_parse.move(220, 200)
        self.checkbox_parse.resize(250, 25)

        self.checkbox_validity.move(425, 200)
        self.checkbox_validity.resize(250, 25)


    def checked_case(self, state):

        '''
        Fonction permettant de gérer les changements d'etas des checboxs
        '''
        
        if state == Qt.Checked:

            if self.sender() == self.checkbox_issuer:
                self.checkbox_parse.setChecked(False)
                self.checkbox_validity.setChecked(False)
                self.status = 1
            
            elif self.sender() == self.checkbox_parse:
                self.checkbox_issuer.setChecked(False)
                self.checkbox_validity.setChecked(False)
                self.status = 2
            
            elif self.sender() == self.checkbox_validity:
                self.checkbox_issuer.setChecked(False)
                self.checkbox_parse.setChecked(False)
                self.status = 3
            

  
        
    def form_issuer(self):

        self.label_form_select_issuercertificate = QLabel("Veuillez séléctionner le path vers l'issuerCertificate :")
        self.layout_test.addWidget(self.label_form_select_issuercertificate)
        self.setLayout(self.layout_test)
        self.label_form_select_issuercertificate.setFont(QFont('Lato', 14))

        self.file_issuer = QLineEdit(self)
        self.file_issuer.move(100, 274)
        self.file_issuer.resize(250,26)
        self.file_issuer.setStyleSheet("border-radius: 5px; color: blue;")

        self.button_browse_issuer = QPushButton('Rechercher', self)
        self.layout_test.addWidget(self.button_browse_issuer)
        self.setLayout(self.layout_test)
        self.button_browse_issuer.clicked.connect(self.browse_file_issuer)
        self.button_browse_issuer.setStyleSheet("QPushButton"
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


        self.label_form_select_subject_certificate = QLabel("Veuillez séléctionner le path vers le Subject certificate :")
        self.layout_test.addWidget(self.label_form_select_subject_certificate)
        self.setLayout(self.layout_test)
        self.label_form_select_subject_certificate.setFont(QFont('Lato', 14))

        self.file_subject = QLineEdit(self)
        self.file_subject.move(100, 274)
        self.file_subject.resize(250,26)
        self.file_subject.setStyleSheet("border-radius: 5px; color: blue;")

        self.button_browse_subject = QPushButton('Rechercher', self)
        self.layout_test.addWidget(self.button_browse_subject)
        self.setLayout(self.layout_test)
        self.button_browse_subject.clicked.connect(self.browse_file_subject)
        self.button_browse_subject.setStyleSheet("QPushButton"
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

        self.button_validate_issuer = QPushButton('Valider', self)
        self.layout_test.addWidget(self.button_validate_issuer)
        self.setLayout(self.layout_test)
        self.button_validate_issuer.clicked.connect(self.validate_issuer)
        self.button_validate_issuer.setStyleSheet("QPushButton"
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

    def browse_file_issuer(self):
        '''
        Selection des fichiers PEM or KEY
        '''
        fname = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PEM, KEY OR CRT (*.pem *.key *.crt)')
        self.file_issuer.setText(fname[0])

    def browse_file_subject(self):
        '''
        Selection des fichiers PEM or KEY
        '''
        fname = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PEM, KEY OR CRT (*.pem *.key *.crt)')
        self.file_subject.setText(fname[0])

    def form_parse(self):


        self.label_form_select_parse_certif = QLabel("Veuillez séléctionner le path vers le certificat à parser :")
        self.layout_test.addWidget(self.label_form_select_parse_certif)
        self.setLayout(self.layout_test)
        self.label_form_select_parse_certif.setFont(QFont('Lato', 14))

        self.file_to_parse = QLineEdit(self)
        self.file_to_parse.move(100, 274)
        self.file_to_parse.resize(250,26)
        self.file_to_parse.setStyleSheet("border-radius: 5px; color: blue;")

        self.button_browse_file_to_parse = QPushButton('Rechercher', self)
        self.layout_test.addWidget(self.button_browse_file_to_parse)
        self.setLayout(self.layout_test)
        self.button_browse_file_to_parse.clicked.connect(self.browse_file_to_parse)
        self.button_browse_file_to_parse.setStyleSheet("QPushButton"
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

    def browse_file_to_parse(self):
        '''
        Selection des fichiers PEM or KEY
        '''
        fname = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PEM (*.pem)')
        self.file_to_parse.setText(fname[0])



    def form_validity(self):


        self.label_form_select_validity = QLabel("Veuillez séléctionner le path vers le certificat à analyser :")
        self.layout_test.addWidget(self.label_form_select_validity)
        self.setLayout(self.layout_test)
        self.label_form_select_validity.setFont(QFont('Lato', 14))

        self.file_to_check_validity = QLineEdit(self)
        self.file_to_check_validity.move(100, 274)
        self.file_to_check_validity.resize(250,26)
        self.file_to_check_validity.setStyleSheet("border-radius: 5px; color: blue;")

        self.button_browse_file_validate = QPushButton('Rechercher', self)
        self.layout_test.addWidget(self.button_browse_file_validate)
        self.setLayout(self.layout_test)
        self.button_browse_file_validate.clicked.connect(self.browse_file_to_check_validity)
        self.button_browse_file_validate.setStyleSheet("QPushButton"
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

    def browse_file_to_check_validity(self):
        '''
        Selection des fichiers PEM or KEY
        '''
        fname = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PEM (*.pem)')
        self.file_to_check_validity.setText(fname[0])






    def validate_issuer(self):

        if self.checkbox_issuer.isChecked() == True:
            issuer_cert = self.file_issuer.text()
            subjet_cert = self.file_subject.text()

            if issuer_cert == "" or subjet_cert == "":
                GenerateClientUi.err_popup(self, "Erreur, veuillez entrer un chemin vers un fichier valide")
            else:
                logging.info(f"Vérification que le fichier : '{subjet_cert}' est bien signé par le fichier : '{issuer_cert}' et  \n")
                GenerateClientUi.popup(self, "Le certificat est bien signé par l'autorité d'enregistrement")
                verif_parse.verifyIssuer(self, issuer_cert, subjet_cert)
                print(f"issuer cert {issuer_cert} subject cert {subjet_cert}")

        elif self.checkbox_parse.isChecked() == True:
            cert_to_parse = self.file_to_parse.text()
            if cert_to_parse == "":
                GenerateClientUi.err_popup(self, "Erreur, le chemin saisi est invalide")
            else:
                logging.info(f"On parse le fichier {cert_to_parse} \n")
                parse = verif_parse.parse(self, cert_to_parse)
                GenerateClientUi.popup(self,parse)
                print(f"cert to parse {cert_to_parse}")

        elif self.checkbox_validity.isChecked() == True:
            validity = self.file_to_check_validity.text()
            if validity == "":
                GenerateClientUi.err_popup(self, "Erreur, le chemin saisi est invalide")
            else:
                logging.info(f"On parse le fichier {validity} \n")
                verif_parse.expiration(self, validity)
            print("validity")
        else:
            GenerateClientUi.err_popup(self, "Erreur, veuillez séléctionner une action")



if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    main = OtherOptions()
    app.exec_()
              