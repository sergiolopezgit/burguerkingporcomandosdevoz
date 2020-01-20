import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from browser import *
from text import *

class Menu:
    def __init__(self, hamburguesa, complemento, bebida, precio):
        self.hamburguesa = hamburguesa
        self.complemento = complemento
        self.bebida = bebida
        self.precio = precio

def speakbypath(path):
    playsound.playsound(path)

def speak(text):
    tts = gTTS(text=text, lang="es")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio, language="es")
            print("Has dicho: " + said)
        except:
            print("No se entiende")
        return said

def getmessage():
    funciona = False
    message = ""
    while not funciona:
        message = get_audio()
        if message == "":
            speakbypath("noseentiende.mp3")
        else:
            funciona = True

    return message

def getelement(path,elements):
    element = ""
    while element == "":
        speakbypath(path)
        message = getmessage()
        element = searchtext(message, elements)
    return element

while True:
    command = get_audio()
    if command == "pedir hamburguesa":
        speakbypath("entrandoalacuenta.mp3")
        bot = bot()
        break

otromenu = True
pedido = []

while otromenu:

    bot.obtener_menus()

    hamburguesa = getelement("cualquieres.mp3",bot.menus)

    bot.seleccionar_menu(hamburguesa)
    bot.obtener_complementos()

    complemento = getelement("quecomplementoquieres.mp3",bot.complementos)

    bot.seleccionar_complemento(complemento)
    bot.obtener_bebidas()

    bebida = getelement("quebebidaquieres.mp3",bot.bebidas)

    bot.seleccionar_bebida(bebida)
    precio = bot.precio_menu()
    bot.añadir_al_carrito()

    pedido.append(Menu(hamburguesa, complemento, bebida, precio))

    respuestaotromenu = getelement("quieresotromenu.mp3",["si","no"])

    if respuestaotromenu.lower() == "no":
        otromenu = False

bot.ir_al_carrito()

resumenpedido = ""


for menu in pedido:
    resumenpedido += menu.hamburguesa + " con " + menu.complemento + " y " + menu.bebida + " cuesta " + menu.precio + "."

if len(pedido) > 1:
    resumenpedido += " en total " + bot.precio_total() + "."

resumenpedido += " se enviará a " + bot.direccion_de_envio() + ", tardará " + bot.tiempo_de_envio()
resumenpedido = resumenpedido.replace('®','')

speak(resumenpedido)

bot.tramitar_pedido()
bot.pagar_en_efectivo()