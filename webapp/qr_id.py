import qrcode
import string
import random


qr_err_1 = qrcode.constants.ERROR_CORRECT_L
qr_err_2 = qrcode.constants.ERROR_CORRECT_M
qr_err_3 = qrcode.constants.ERROR_CORRECT_Q
qr_err_4 = qrcode.constants.ERROR_CORRECT_H


class QRandID:

    def __init__(self,qr_vers = 1, qr_err = qr_err_1 , qr_box_size = 15, qr_border = 2, 
                 qr_url = "http://verdi9-sendfiles-9ca971e160dc.herokuapp.com/mobile-upload", qr_fill = "black", qr_back = "white", id_size = 6):
        
        self.qr_vers = qr_vers
        self.qr_err = qr_err
        self.qr_box_size = qr_box_size
        self.qr_border = qr_border
        self.qr_url = qr_url
        self.qr_fill = qr_fill
        self.qr_back = qr_back
        self.id_size = id_size
    
    def generate_ID(self):

        #Minúscules, majúscules i dígits (62 possibles caràcters en total)
        #Amb combinatòria senzilla veiem que els id generables en funció de la llargada
        #són: 62 ^ (id_size) = 62 ^ 6 = 56800235584

        l = list(string.ascii_letters) + list(string.digits)
        s = ''
        for _ in range(self.id_size):
            s += l[random.randint(0,len(l)-1)]
        self.id = s
    
    def generate_QR(self,lang):
        self.qr = qrcode.QRCode(
                version=self.qr_vers,
                error_correction=self.qr_err,
                box_size=self.qr_box_size,
                border=self.qr_border,
                )
        self.qr.add_data(self.qr_url+f"?id={self.id}&lang={lang}")
        self.qr.make(fit=True)
        self.img = self.qr.make_image(fill_color="black", back_color="white")
    
    def save_QR(self, path = "C:/Users/alexc/OneDrive/Escriptori/Verdi2024/QRgenerator/"):
        self.img.save(path+f"qr{self.id}.png")
    
    def get_ID(self):
        return self.id
    
    def get_QR_img(self):
        return self.img
    
    def run(self):
        self.generate_ID()
        self.generate_QR()
        self.save_QR()


"""
>>> from qr_id import *
>>> o = QRandID()
>>> o.run()
"""