from contextlib import contextmanager
import os

class Bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'

@contextmanager
def open_image(path, methods):
    try:
        file = open(path, methods)
        yield file
    finally:
        file.close()

class SecretMessage(object):

    def __init__(self, image_type, image_path):
        self.image_type = image_type
        self.image_path = image_path 
        self.png_end_hex = b"\x49\x45\x4E\x44\xAE\x42\x60\x82"
        self.jpeg_end_hex = b"\xFF\xD9"    

    def add_secret_message(self, secret_message):
        with open_image(self.image_path, "ab") as f:
            f.write(secret_message.encode("utf-8"))

    def read_secret_message(self):
        with open_image(self.image_path, "rb") as f:
            if self.image_type == ".png":
                content = f.read()
                offset = content.index(self.png_end_hex)
                f.seek(offset + len(self.png_end_hex))
                secret_message = f.read()
                return secret_message
            else:
                content = f.read()
                offset = content.index(self.jpeg_end_hex)
                f.seek(offset + len(self.jpeg_end_hex))
                secret_message = f.read()
                return secret_message

def determine_image_type(image_path):
    file_name, extension = os.path.splitext(image_path)
    extension = extension.lower()
    return extension

def has_turkish_chars(input_str):
    turkish_chars = "çÇğĞıİöÖşŞüÜ"
    return any(char in turkish_chars for char in input_str)

if __name__ == "__main__":
    
    while True:
        print( Bcolors.GREEN +"""
              Resim Üzerinde Uygulamak İstediğiniz İşlem
              
              1 - Gizli Mesajı Oluştur
              
              2 - Gizli Mesaj Oku
              """ + Bcolors.ENDC)
        operation = input( Bcolors.YELLOW +"İşlem Seçiniz: " + Bcolors.ENDC).upper()

        if operation == "1":
            image_path = input( Bcolors.BLUE + "Lütfen Resim Yolunu Giriniz: " + Bcolors.ENDC)
            image_type = determine_image_type(image_path)
            sm = SecretMessage(image_type, image_path)
            secret_message = input( Bcolors.RED +"Lütfen Gizlemek İstediğiniz Mesajı Giriniz (Türkçe Karakter Kullanmayınız!):\n\n" 
                                   + Bcolors.ENDC)
            
            if has_turkish_chars(secret_message):
                print(Bcolors.RED +"TÜRKÇE KARAKTER KULLANMAYINIZ!!!" + Bcolors.ENDC)
            else:
                sm.add_secret_message(secret_message)
                print(Bcolors.RED + "\n\nGizli Mesajınız Oluşturuldu!" + Bcolors.ENDC)
                break

        elif operation == "2":
            image_path = input(Bcolors.BLUE + "Lütfen Resim Yolunu Giriniz: " + Bcolors.ENDC)
            image_type = determine_image_type(image_path)
            sm = SecretMessage(image_type, image_path)
            secret_message = sm.read_secret_message()
            
            if secret_message == b'':
                print(Bcolors.RED +"Görselde gizli mesaj bulunmamaktadır!" + Bcolors.ENDC)
                break
                
            else:
                print(Bcolors.GREEN + f"Resimde Gizli Mesaj Bulundu\n\n Mesaj: {secret_message}" + Bcolors.ENDC)
                break

        else:
            print(Bcolors.RED +"Lütfen var olan bir işlem seçiniz!!"+ Bcolors.RED)
