from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import os
from time import *

from config import *


class bot:
    def __init__(self):
        self.iniciar_bot()

    def iniciar_bot(self):
        # cargar chrome
        self.driver = webdriver.Chrome()

        # carga la página
        self.driver.get("https://www.burgerking.es/carta")

        # pantalla completa
        self.driver.maximize_window()
        sleep(1)

        # click para login
        self.clickon('/html/body/app-root/app-header/header/div/nav/div/button')

        # mete usuario
        self.enter('/html/body/div[3]/div[2]/div/mat-dialog-container/app-login-dialog/mat-dialog-content/section/div[2]/div[1]/div/form/div[1]/input', get("username"))
        # mete contraseña
        self.enter('/html/body/div[3]/div[2]/div/mat-dialog-container/app-login-dialog/mat-dialog-content/section/div[2]/div[1]/div/form/div[2]/div[1]/input', get("password"))

        # intenta entrar a la cuenta
        self.clickon('/html/body/div[3]/div[2]/div/mat-dialog-container/app-login-dialog/mat-dialog-content/section/div[2]/div[1]/div/form/div[3]/button')

        sleep(5)

        # entra a menus de parrilla
        self.clickon('/html/body/app-root/app-carta/section/div/div[2]/a[2]')
        self.clickon('/html/body/app-root/app-carta/section/div/div[2]/a[2]')

    def seleccionar_elemento(self,text,elements,leftpath,rightpath):
        encontrado = False
        i = 0

        while not encontrado and i < len(elements):
            i += 1
            xpath = leftpath + str(i) + rightpath
            element = self.driver.find_element_by_xpath(xpath)
            mess = element.text
            if element.text == "Patatas Supreme\nSour cream":
                mess = "Patatas Supreme"
            if text == mess:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                sleep(1)
                for i in range(10):
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.UP)
                sleep(1)
                element.click()
                sleep(1)
                encontrado = True

    def obtener_elementos(self, leftpath, rightpath):
        elementos = []

        haymaselementos = True
        i = 1

        while haymaselementos:
            xpath = leftpath + str(i) + rightpath
            if self.check_element_by_xpath(xpath):
                element = self.driver.find_element_by_xpath(xpath)
                if element.text == "Patatas Supreme\nSour cream":
                    elementos.append("Patatas Supreme")
                else:
                    elementos.append(element.text)
                i += 1
            else:
                haymaselementos = False

        return elementos

    def seleccionar_menu(self,menu):
        self.seleccionar_elemento(menu,self.menus,'/html/body/app-root/app-carta-menus/div/section/div/div[2]/div[',']/a/div/h4')

    def seleccionar_complemento(self,complemento):
        self.seleccionar_elemento(complemento,self.complementos,'/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/div[1]/div/div[',']/label/span[1]')
        if complemento == "Patatas Supreme":
            self.clickon('/html/body/ngb-modal-window/div/div/div[3]/a[2]')

        element = self.driver.find_element_by_xpath('/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/button')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(1)
        element.click()
        sleep(1)

    def seleccionar_bebida(self,bebida):
        self.seleccionar_elemento(bebida,self.bebidas,'/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/div/div/div[',']/label/span[1]')

    def obtener_menus(self):
        self.menus = self.obtener_elementos('/html/body/app-root/app-carta-menus/div/section/div/div[2]/div[',']/a/div/h4')

    def obtener_complementos(self):
        element = self.driver.find_element_by_xpath('/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/button')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(1)
        element.click()
        sleep(1)
        self.clickon('/html/body/ngb-modal-window/div/div/div[3]/a[1]')

        self.complementos = self.obtener_elementos('/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/div[1]/div/div[',']/label/span[1]')

    def obtener_bebidas(self):
        self.bebidas = self.obtener_elementos('/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/div/div/div[',']/label/span[1]')

    def precio_menu(self):
        return self.get_text_by_xpath('/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/button/span')

    def añadir_al_carrito(self):
        element = self.driver.find_element_by_xpath('/html/body/app-root/app-logged-menu/div/section/div/div[2]/div[2]/div/ngb-tabset/div/div/button')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(1)
        element.click()

    def ir_al_carrito(self):
        self.driver.get('https://www.burgerking.es/carta/summary-order-b')
        sleep(1)

    def direccion_de_envio(self):
        return self.get_text_by_xpath('/html/body/app-root/app-resumen-pedido-b/div/div[1]/div/div/div[2]/div[1]/div[1]/h3')

    def tiempo_de_envio(self):
        return self.get_text_by_xpath('/html/body/app-root/app-resumen-pedido-b/div/div[1]/div/div/div[2]/div[1]/div[1]/p/span')

    def precio_total(self):
        return self.get_text_by_xpath('/html/body/app-root/app-resumen-pedido-b/div/div[1]/div/div/div[2]/div[2]/div/div[2]/p')

    def tramitar_pedido(self):
        self.clickon('/html/body/app-root/app-resumen-pedido-b/div/div[1]/div/div/div[2]/div[3]/div/button')

    def pagar_en_efectivo(self):
        self.clickon('/html/body/app-root/app-tarjeta-a/div/div/div/div[2]/div/form/div/div/div[1]')
        element = self.driver.find_element_by_xpath('/html/body/app-root/app-tarjeta-a/div/div/div/div[5]/div[2]/button')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(1)
        element.click()
        print("order completed")

    def get_text_by_xpath(self,xpath):
        return self.driver.find_element_by_xpath(xpath).text

    def clickon(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()
        sleep(1)

    def enter(self, xpath, text):
        self.driver.find_element_by_xpath(xpath).send_keys(text)
        sleep(1)

    def check_element_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True