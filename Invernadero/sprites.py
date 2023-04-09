
from PIL import Image,ImageTk



def cargarimagen(pixel,opcion):
    if (opcion=="planta"):
        img = (Image.open("./assets/planta.png"))
    if (opcion == "grifo"):
        img = (Image.open("./assets/grifo.png"))
    if (opcion == "paredb"):
        img = (Image.open("./assets/paredblanca.jpg"))
    if (opcion == "walle"):
        img = (Image.open("./assets/walle.png"))
    if (opcion == "eva"):
        img = (Image.open("./assets/eva.png"))
    if (opcion == "transparente"):
        img = (Image.open("./assets/transparente.jpg"))
    if (opcion=="puerta"):
        img = (Image.open("./assets/puerta.png"))
    if (opcion == "arduino"):
        img = (Image.open("./assets/ESP32.png"))
    resized_image = img.resize((pixel,pixel), Image.Resampling.LANCZOS)
    new_image = ImageTk.PhotoImage(resized_image)
    return new_image




